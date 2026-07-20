"""Maintainer-only script: build a shipped embedding index under data/docs_index/.

Not a console script — run directly against a live embedding endpoint:

    uv run python -m laraq_mcp.ingest --provider ollama --model qwen3-embedding --base-url http://localhost:11434
    uv run python -m laraq_mcp.ingest --provider openai-compatible --model text-embedding-3-small --base-url https://api.openai.com/v1 --api-key sk-...
    uv run python -m laraq_mcp.ingest --provider google --model text-embedding-004 --api-key ...

Re-run whenever docs/ changes materially — the shipped index is a point-in-time
build, not auto-refreshed at runtime (get_or_build_index falls back to a
user-local cache + rebuild only when chunk_size/chunk_overlap don't match or
the shipped index is missing/corrupt, not on corpus content changes).
"""

import argparse

from laraq_mcp.embeddings import (
    EmbeddingClient,
    GoogleEmbeddingClient,
    OllamaEmbeddingClient,
    OpenAICompatibleEmbeddingClient,
)
from laraq_mcp.research import DOCS_DIR, DOCS_INDEX_DIR, build_index, docs_mtime, save_index, slugify_model


def _build_client(provider: str, model: str, base_url: str | None, api_key: str | None) -> EmbeddingClient:
    if provider == "ollama":
        if not base_url:
            raise ValueError("--base-url is required for provider=ollama")
        return OllamaEmbeddingClient(base_url=base_url, model=model)
    elif provider == "openai-compatible":
        if not base_url or not api_key:
            raise ValueError("--base-url and --api-key are required for provider=openai-compatible")
        return OpenAICompatibleEmbeddingClient(base_url=base_url, api_key=api_key, model=model)
    elif provider == "google":
        if not api_key:
            raise ValueError("--api-key is required for provider=google")
        return GoogleEmbeddingClient(api_key=api_key, model=model)
    raise ValueError(f"Unknown provider: {provider}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a shipped embedding index for laraq-mcp.")
    parser.add_argument("--provider", required=True, choices=["ollama", "openai-compatible", "google"])
    parser.add_argument("--model", required=True)
    parser.add_argument("--base-url", default=None, help="Required for ollama and openai-compatible")
    parser.add_argument("--api-key", default=None, help="Required for openai-compatible and google")
    parser.add_argument("--chunk-size", type=int, default=500)
    parser.add_argument("--chunk-overlap", type=int, default=50)
    args = parser.parse_args()

    client = _build_client(args.provider, args.model, args.base_url, args.api_key)
    slug = slugify_model(args.provider, args.model)
    index_dir = DOCS_INDEX_DIR / slug

    print(f"Building index '{slug}' from {DOCS_DIR} ...")
    chunks, sources, embeddings = build_index(client, DOCS_DIR, args.chunk_size, args.chunk_overlap)
    save_index(index_dir, chunks, sources, embeddings, args.chunk_size, args.chunk_overlap, docs_mtime(DOCS_DIR))
    print(f"Wrote {len(chunks)} chunks, embeddings shape {embeddings.shape}, to {index_dir}")


if __name__ == "__main__":
    main()
