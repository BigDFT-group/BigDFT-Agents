"""Deterministic RAG retrieval: chunking, embedding-index caching, cosine search.

Query expansion is NOT here — that's the `query-expander` subagent now. This
module only does retrieval: given one or more query strings (already
expanded by the caller), embed and rank chunks. Multi-query aggregation
(max score per chunk across query variants) lives here too, in
`research_multi`, since it's deterministic array/dict logic.
"""

import json
import re
from pathlib import Path

import numpy as np

from laraq_mcp.config import Config
from laraq_mcp.embeddings import EmbeddingClient

DATA_DIR = Path(__file__).parent / "data"
DOCS_DIR = DATA_DIR / "docs"
DOCS_INDEX_DIR = DATA_DIR / "docs_index"
USER_CACHE_DIR = Path.home() / ".cache" / "laraq-mcp" / "embeddings"

_CORPUS_SUFFIXES = (".txt", ".md", ".py")


def chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    """Split text into overlapping chunks, preferring to break at a newline
    or space near the target chunk_size boundary."""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        if end < len(text):
            newline_pos = text.rfind("\n", start, end)
            if newline_pos > start + chunk_size // 2:
                end = newline_pos + 1
            else:
                space_pos = text.rfind(" ", start, end)
                if space_pos > start + chunk_size // 2:
                    end = space_pos + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        start = end - chunk_overlap

    return chunks


def load_corpus(docs_path: Path) -> tuple[list[str], list[str]]:
    """Load all .txt/.md/.py files under docs_path. Returns (documents, sources)."""
    if not docs_path.exists():
        raise FileNotFoundError(f"Documents path not found: {docs_path}")

    documents = []
    sources = []
    for file_path in docs_path.rglob("*"):
        if file_path.is_file() and file_path.suffix in _CORPUS_SUFFIXES:
            documents.append(file_path.read_text())
            sources.append(str(file_path))

    return documents, sources


def docs_mtime(docs_path: Path) -> float:
    """Latest modification time across all corpus files under docs_path."""
    latest = 0.0
    for file_path in docs_path.rglob("*"):
        if file_path.is_file() and file_path.suffix in _CORPUS_SUFFIXES:
            mtime = file_path.stat().st_mtime
            if mtime > latest:
                latest = mtime
    return latest


def cosine_similarity(query: np.ndarray, embeddings: np.ndarray) -> np.ndarray:
    """Cosine similarity between a single query embedding and a 2D embeddings array."""
    query_norm = query / (np.linalg.norm(query) + 1e-8)
    embedding_norms = np.linalg.norm(embeddings, axis=1, keepdims=True) + 1e-8
    embeddings_normalized = embeddings / embedding_norms
    return np.dot(embeddings_normalized, query_norm)


def slugify_model(provider: str, model: str) -> str:
    """Build a filesystem-safe directory slug from a provider+model pair."""
    raw = f"{provider}-{model}"
    return re.sub(r"[^a-zA-Z0-9]+", "-", raw).strip("-").lower()


def shipped_index_dir(slug: str) -> Path | None:
    """Return the shipped index directory for `slug` if a complete one exists."""
    candidate = DOCS_INDEX_DIR / slug
    if (
        (candidate / "embeddings.npy").exists()
        and (candidate / "chunks.json").exists()
        and (candidate / "meta.json").exists()
    ):
        return candidate
    return None


def load_index(
    index_dir: Path,
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
    check_mtime_against: Path | None = None,
) -> tuple[list[str], list[str], np.ndarray] | None:
    """Load a chunks/sources/embeddings index from disk if it's valid.

    Validity: files exist, chunk_size/chunk_overlap match (if given), and if
    check_mtime_against is given, the corpus hasn't been modified since the
    index was built. Any failure (missing files, bad JSON, stale) -> None,
    treated as a cache miss by the caller.
    """
    embeddings_file = index_dir / "embeddings.npy"
    chunks_file = index_dir / "chunks.json"
    meta_file = index_dir / "meta.json"

    if not (embeddings_file.exists() and chunks_file.exists() and meta_file.exists()):
        return None

    try:
        with open(meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)

        if chunk_size is not None and meta.get("chunk_size") != chunk_size:
            return None
        if chunk_overlap is not None and meta.get("chunk_overlap") != chunk_overlap:
            return None
        if check_mtime_against is not None:
            current_mtime = docs_mtime(check_mtime_against)
            if current_mtime > meta.get("docs_mtime", 0):
                return None

        with open(chunks_file, "r", encoding="utf-8") as f:
            chunks_data = json.load(f)

        embeddings = np.load(embeddings_file)
        return chunks_data["chunks"], chunks_data["sources"], embeddings

    except Exception:
        return None


def save_index(
    index_dir: Path,
    chunks: list[str],
    sources: list[str],
    embeddings: np.ndarray,
    chunk_size: int,
    chunk_overlap: int,
    docs_mtime_value: float,
) -> None:
    """Save an index to disk. Failures are logged-and-swallowed, non-fatal —
    a failed cache write just means the next call rebuilds."""
    try:
        index_dir.mkdir(parents=True, exist_ok=True)
        np.save(index_dir / "embeddings.npy", embeddings)
        with open(index_dir / "chunks.json", "w", encoding="utf-8") as f:
            json.dump({"chunks": chunks, "sources": sources}, f)
        with open(index_dir / "meta.json", "w", encoding="utf-8") as f:
            json.dump(
                {"chunk_size": chunk_size, "chunk_overlap": chunk_overlap, "docs_mtime": docs_mtime_value},
                f,
            )
    except Exception:
        pass


def build_index(
    embedding_client: EmbeddingClient,
    docs_path: Path,
    chunk_size: int,
    chunk_overlap: int,
) -> tuple[list[str], list[str], np.ndarray]:
    """Chunk and embed the corpus at docs_path from scratch."""
    documents, doc_sources = load_corpus(docs_path)
    if not documents:
        raise ValueError(f"No documents found in {docs_path}")

    chunks: list[str] = []
    chunk_sources: list[str] = []
    for doc, source in zip(documents, doc_sources):
        doc_chunks = chunk_text(doc, chunk_size, chunk_overlap)
        chunks.extend(doc_chunks)
        chunk_sources.extend([source] * len(doc_chunks))

    embeddings = embedding_client.embed(chunks)
    return chunks, chunk_sources, embeddings


def get_or_build_index(cfg: Config, embedding_client: EmbeddingClient) -> tuple[list[str], list[str], np.ndarray]:
    """Get the chunks/sources/embeddings index for cfg's embedding provider+model.

    Tries a shipped pre-built index first, then a user-local cache, and
    finally builds (and caches) one from scratch.
    """
    embedding_config = cfg.get_embedding_config()
    slug = slugify_model(cfg.embedding_provider, embedding_config.embedding_model)
    chunk_size = cfg.research.chunk_size
    chunk_overlap = cfg.research.chunk_overlap

    shipped = shipped_index_dir(slug)
    if shipped is not None:
        result = load_index(shipped, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        if result is not None:
            return result

    user_cache = USER_CACHE_DIR / slug
    result = load_index(user_cache, chunk_size=chunk_size, chunk_overlap=chunk_overlap, check_mtime_against=DOCS_DIR)
    if result is not None:
        return result

    chunks, sources, embeddings = build_index(embedding_client, DOCS_DIR, chunk_size, chunk_overlap)
    save_index(user_cache, chunks, sources, embeddings, chunk_size, chunk_overlap, docs_mtime(DOCS_DIR))
    return chunks, sources, embeddings


def search(
    query_embedding: np.ndarray,
    chunks: list[str],
    sources: list[str],
    embeddings: np.ndarray,
    top_k: int,
) -> list[tuple[str, str, float]]:
    """Rank chunks by cosine similarity to a single query embedding."""
    if embeddings is None or len(chunks) == 0:
        return []

    similarities = cosine_similarity(query_embedding, embeddings)
    top_indices = np.argsort(similarities)[-top_k:][::-1]

    return [(chunks[i], sources[i], float(similarities[i])) for i in top_indices]


def research_multi(
    queries: list[str],
    chunks: list[str],
    sources: list[str],
    embeddings: np.ndarray,
    embedding_client: EmbeddingClient,
    top_k: int,
) -> str:
    """Search with each query variant and aggregate by max score per chunk.

    This is what today's rag_research.py's __call__ did across LLM-expanded
    query variants — here the variants are supplied by the caller (the
    orchestrating skill, having already called intent-extractor/query-expander)
    instead of being generated internally.
    """
    non_empty_queries = [q for q in queries if q and q.strip()]
    if not non_empty_queries:
        return "No query provided."

    all_results: dict[str, tuple[str, float]] = {}
    for query in non_empty_queries:
        query_embedding = embedding_client.embed_one(query)
        for chunk, source, score in search(query_embedding, chunks, sources, embeddings, top_k):
            if chunk not in all_results or score > all_results[chunk][1]:
                all_results[chunk] = (source, score)

    if not all_results:
        return "No relevant context found."

    sorted_results = sorted(all_results.items(), key=lambda item: item[1][1], reverse=True)[:top_k]
    parts = [f"[Source: {source}, Score: {score:.3f}]\n{chunk}" for chunk, (source, score) in sorted_results]
    return "\n\n---\n\n".join(parts)
