import time

import numpy as np
import pytest

from laraq_mcp.embeddings import EmbeddingClient
from laraq_mcp.research import (
    build_index,
    chunk_text,
    cosine_similarity,
    docs_mtime,
    load_corpus,
    load_index,
    research_multi,
    save_index,
    search,
    slugify_model,
)


class FakeEmbeddingClient(EmbeddingClient):
    """Deterministic embedding: hashes each text into a fixed-size vector so
    identical/similar text yields identical/similar vectors, with no network."""

    DIM = 8

    def embed(self, texts: list[str]) -> np.ndarray:
        return np.array([self._vec(t) for t in texts])

    def _vec(self, text: str) -> list[float]:
        # Bag-of-words-ish: count occurrences of a few marker words per dim.
        markers = ["atom", "position", "class", "method", "unrelated", "banana", "quux", "zzz"]
        return [float(text.lower().count(m)) for m in markers]


def test_chunk_text_breaks_at_newline_when_available():
    text = "a" * 40 + "\n" + "b" * 40
    chunks = chunk_text(text, chunk_size=45, chunk_overlap=5)
    assert chunks[0].endswith("a")
    assert "\n" not in chunks[0]


def test_chunk_text_falls_back_to_space():
    text = ("word " * 20).strip()
    chunks = chunk_text(text, chunk_size=45, chunk_overlap=5)
    for c in chunks[:-1]:
        assert not c.endswith("wor")  # didn't hard-cut mid-word


def test_chunk_text_hard_cuts_when_no_break_point():
    text = "x" * 100
    chunks = chunk_text(text, chunk_size=30, chunk_overlap=5)
    assert all(len(c) <= 30 for c in chunks)
    assert "".join(chunks).replace("", "") != ""  # non-empty


def test_load_corpus_filters_by_suffix(tmp_path):
    (tmp_path / "a.md").write_text("markdown doc")
    (tmp_path / "b.txt").write_text("text doc")
    (tmp_path / "c.py").write_text("python doc")
    (tmp_path / "d.json").write_text("{}")  # should be ignored

    documents, sources = load_corpus(tmp_path)
    assert len(documents) == 3
    assert not any(s.endswith("d.json") for s in sources)


def test_cosine_similarity_identical_vectors_score_one():
    v = np.array([1.0, 2.0, 3.0])
    embeddings = np.array([[1.0, 2.0, 3.0], [3.0, 2.0, 1.0]])
    sims = cosine_similarity(v, embeddings)
    assert sims[0] == pytest.approx(1.0, abs=1e-4)
    assert sims[0] > sims[1]


def test_search_returns_top_k_sorted_desc():
    chunks = ["about atoms", "about bananas", "about atom positions"]
    sources = ["a.md", "b.md", "c.md"]
    client = FakeEmbeddingClient()
    embeddings = client.embed(chunks)
    query_embedding = client.embed_one("atom position")

    results = search(query_embedding, chunks, sources, embeddings, top_k=2)
    assert len(results) == 2
    assert results[0][2] >= results[1][2]


def test_index_cache_round_trip(tmp_path):
    chunks = ["chunk one", "chunk two"]
    sources = ["a.md", "b.md"]
    embeddings = np.array([[1.0, 0.0], [0.0, 1.0]])
    index_dir = tmp_path / "index"

    save_index(index_dir, chunks, sources, embeddings, chunk_size=500, chunk_overlap=50, docs_mtime_value=123.0)
    result = load_index(index_dir, chunk_size=500, chunk_overlap=50)

    assert result is not None
    loaded_chunks, loaded_sources, loaded_embeddings = result
    assert loaded_chunks == chunks
    assert loaded_sources == sources
    assert np.allclose(loaded_embeddings, embeddings)


def test_index_cache_invalidated_by_chunk_size_change(tmp_path):
    index_dir = tmp_path / "index"
    save_index(index_dir, ["c"], ["s"], np.array([[1.0]]), chunk_size=500, chunk_overlap=50, docs_mtime_value=1.0)

    assert load_index(index_dir, chunk_size=500, chunk_overlap=50) is not None
    assert load_index(index_dir, chunk_size=999, chunk_overlap=50) is None
    assert load_index(index_dir, chunk_size=500, chunk_overlap=1) is None


def test_index_cache_invalidated_by_docs_mtime_bump(tmp_path):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "a.md").write_text("hello")

    index_dir = tmp_path / "index"
    save_index(
        index_dir, ["c"], ["s"], np.array([[1.0]]),
        chunk_size=500, chunk_overlap=50, docs_mtime_value=docs_mtime(docs_dir),
    )
    assert load_index(index_dir, check_mtime_against=docs_dir) is not None

    time.sleep(0.01)
    (docs_dir / "a.md").write_text("hello again, modified")
    assert load_index(index_dir, check_mtime_against=docs_dir) is None


def test_build_index_chunks_and_embeds(tmp_path):
    (tmp_path / "doc.md").write_text("about atoms and their positions " * 5)
    client = FakeEmbeddingClient()

    chunks, sources, embeddings = build_index(client, tmp_path, chunk_size=50, chunk_overlap=10)
    assert len(chunks) > 0
    assert len(sources) == len(chunks)
    assert embeddings.shape[0] == len(chunks)


def test_research_multi_aggregates_max_score_across_queries():
    chunks = ["atom class documentation", "banana unrelated content", "get_position method docs"]
    sources = ["a.md", "b.md", "c.md"]
    client = FakeEmbeddingClient()
    embeddings = client.embed(chunks)

    result = research_multi(
        ["atom class", "get_position method"],
        chunks, sources, embeddings, client, top_k=2,
    )
    assert "[Source:" in result
    assert "banana unrelated content" not in result


def test_research_multi_no_queries_returns_message():
    assert research_multi([], [], [], np.array([]), FakeEmbeddingClient(), top_k=3) == "No query provided."


def test_slugify_model():
    assert slugify_model("ollama", "qwen3-embedding:latest") == "ollama-qwen3-embedding-latest"
    assert slugify_model("openai-compatible", "text-embedding-3-small") == "openai-compatible-text-embedding-3-small"
