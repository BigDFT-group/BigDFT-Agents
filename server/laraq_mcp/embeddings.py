"""Embedding clients for the providers laraq-mcp supports."""

from abc import ABC, abstractmethod

import httpx
import numpy as np

from laraq_mcp.config import Config


class EmbeddingClient(ABC):
    """Abstract base class for embedding clients."""

    @abstractmethod
    def embed(self, texts: list[str]) -> np.ndarray:
        """Embed a list of texts. Returns shape (len(texts), embedding_dim)."""

    def embed_one(self, text: str) -> np.ndarray:
        """Embed a single text. Returns shape (embedding_dim,)."""
        return self.embed([text])[0]


class OllamaEmbeddingClient(EmbeddingClient):
    """Embedding client for Ollama."""

    BATCH_SIZE = 50

    def __init__(self, base_url: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self._client = httpx.Client(timeout=httpx.Timeout(timeout=600.0, connect=10.0, pool=10.0))

    def embed(self, texts: list[str]) -> np.ndarray:
        all_embeddings = []
        for i in range(0, len(texts), self.BATCH_SIZE):
            batch = texts[i : i + self.BATCH_SIZE]
            response = self._client.post(
                f"{self.base_url}/api/embed",
                json={"model": self.model, "input": batch},
            )
            # Some texts produce NaN embeddings which Ollama can't JSON-encode.
            # Fall back to one-at-a-time for the failing batch.
            if response.status_code == 500:
                for text in batch:
                    single = self._client.post(
                        f"{self.base_url}/api/embed",
                        json={"model": self.model, "input": [text]},
                    )
                    if single.status_code == 500:
                        dim = len(all_embeddings[0]) if all_embeddings else self._probe_dim()
                        all_embeddings.append([0.0] * dim)
                    else:
                        single.raise_for_status()
                        all_embeddings.extend(single.json()["embeddings"])
            else:
                response.raise_for_status()
                all_embeddings.extend(response.json()["embeddings"])
        return np.array(all_embeddings)

    def _probe_dim(self) -> int:
        response = self._client.post(
            f"{self.base_url}/api/embed",
            json={"model": self.model, "input": ["hello"]},
        )
        response.raise_for_status()
        return len(response.json()["embeddings"][0])


class OpenAICompatibleEmbeddingClient(EmbeddingClient):
    """Embedding client for OpenAI-compatible APIs."""

    BATCH_SIZE = 50

    def __init__(self, base_url: str, api_key: str, model: str):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self._client = httpx.Client(
            timeout=httpx.Timeout(timeout=600.0, connect=10.0, pool=10.0),
            headers={"Authorization": f"Bearer {api_key}"},
        )

    def embed(self, texts: list[str]) -> np.ndarray:
        all_embeddings = []
        for i in range(0, len(texts), self.BATCH_SIZE):
            batch = texts[i : i + self.BATCH_SIZE]
            response = self._client.post(
                f"{self.base_url}/embeddings",
                json={"model": self.model, "input": batch},
            )
            response.raise_for_status()
            data = response.json()
            sorted_data = sorted(data["data"], key=lambda x: x["index"])
            all_embeddings.extend(item["embedding"] for item in sorted_data)
        return np.array(all_embeddings)


class GoogleEmbeddingClient(EmbeddingClient):
    """Embedding client for Google's API.

    embedContent only accepts a single text per request, so batching is done
    client-side by looping.
    """

    BATCH_SIZE = 50

    def __init__(self, api_key: str, model: str):
        self.model = model
        self._client = httpx.Client(
            timeout=httpx.Timeout(timeout=600.0, connect=10.0, pool=10.0),
            headers={
                "x-goog-api-key": api_key,
                "Content-Type": "application/json",
            },
        )

    def embed(self, texts: list[str]) -> np.ndarray:
        all_embeddings = []
        for text in texts:
            response = self._client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:embedContent",
                json={"content": {"parts": [{"text": text}]}},
            )
            response.raise_for_status()
            data = response.json()
            all_embeddings.append(data["embedding"]["values"])
        return np.array(all_embeddings)


def create_embedding_client(cfg: Config) -> EmbeddingClient:
    """Create an embedding client from a loaded Config."""
    provider = cfg.embedding_provider
    provider_config = cfg.get_embedding_config()

    if provider == "ollama":
        return OllamaEmbeddingClient(base_url=provider_config.base_url, model=provider_config.embedding_model)
    elif provider == "openai-compatible":
        return OpenAICompatibleEmbeddingClient(
            base_url=provider_config.base_url,
            api_key=provider_config.api_key,
            model=provider_config.embedding_model,
        )
    elif provider == "google":
        return GoogleEmbeddingClient(api_key=provider_config.api_key, model=provider_config.embedding_model)
    else:
        raise ValueError(f"Unknown embedding provider: {provider}")
