"""Configuration models and loading for laraq-mcp.

Config is resolved from LARAQ_CONFIG (a full path) if set, else
~/.laraq/config.toml. There is no CLI to pass a path explicitly — this server
only ever runs as an MCP server, so the path must be self-resolving.
"""

import os
import sys
from pathlib import Path
from typing import Literal

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

from pydantic import BaseModel, Field, ValidationError

DEFAULT_CONFIG_PATH = Path.home() / ".laraq" / "config.toml"


class LaraqError(Exception):
    """Base exception for laraq-mcp."""


class ConfigError(LaraqError):
    """Exception raised for configuration errors."""


class ConfigFileNotFoundError(ConfigError):
    """Exception raised when the configuration file is not found."""


class ConfigParseError(ConfigError):
    """Exception raised when the configuration file cannot be parsed."""


class ConfigValidationError(ConfigError):
    """Exception raised when configuration validation fails."""


class OllamaEmbeddingConfig(BaseModel):
    """Configuration for embeddings via Ollama."""

    base_url: str = Field(..., description="Base URL for the Ollama API")
    embedding_model: str = Field(..., description="Model name to use for embeddings")


class OpenAICompatibleEmbeddingConfig(BaseModel):
    """Configuration for embeddings via an OpenAI-compatible API."""

    base_url: str = Field(..., description="Base URL for the OpenAI-compatible API")
    api_key: str = Field(..., description="API key for authentication")
    embedding_model: str = Field(..., description="Model name to use for embeddings")


class GoogleEmbeddingConfig(BaseModel):
    """Configuration for embeddings via Google's Gemini API."""

    api_key: str = Field(..., description="Google API key")
    embedding_model: str = Field(..., description="Model name to use for embeddings, e.g. text-embedding-004")


class ResearchConfig(BaseModel):
    """Configuration for RAG retrieval."""

    top_k: int = Field(3, description="Number of chunks to return per research call")
    chunk_size: int = Field(500, description="Chunk size in characters")
    chunk_overlap: int = Field(50, description="Overlap between adjacent chunks in characters")


class Config(BaseModel):
    """Main configuration container for laraq-mcp."""

    embedding_provider: Literal["ollama", "openai-compatible", "google"] = Field(
        ..., description="Provider to use for embeddings"
    )
    ollama: OllamaEmbeddingConfig | None = None
    openai_compatible: OpenAICompatibleEmbeddingConfig | None = None
    google: GoogleEmbeddingConfig | None = None
    research: ResearchConfig = Field(default_factory=ResearchConfig)
    config_path: str | None = Field(None, exclude=True, description="Path to the loaded config file")

    def model_post_init(self, __context) -> None:
        """Validate that the selected embedding provider has configuration."""
        if self.embedding_provider == "ollama" and self.ollama is None:
            raise ValueError("Ollama embedding provider selected but [ollama] configuration is missing")
        elif self.embedding_provider == "openai-compatible" and self.openai_compatible is None:
            raise ValueError("OpenAI-compatible embedding provider selected but [openai_compatible] configuration is missing")
        elif self.embedding_provider == "google" and self.google is None:
            raise ValueError("Google embedding provider selected but [google] configuration is missing")

        embedding_config = self.get_embedding_config()
        if embedding_config.embedding_model is None:
            raise ValueError(
                f"Embedding provider '{self.embedding_provider}' selected but no embedding_model specified"
            )

    def get_embedding_config(self) -> OllamaEmbeddingConfig | OpenAICompatibleEmbeddingConfig | GoogleEmbeddingConfig:
        """Get the configuration for the selected embedding provider."""
        if self.embedding_provider == "ollama":
            if self.ollama is None:
                raise ValueError("Ollama embedding provider selected but [ollama] configuration is missing")
            return self.ollama
        elif self.embedding_provider == "openai-compatible":
            if self.openai_compatible is None:
                raise ValueError("OpenAI-compatible embedding provider selected but [openai_compatible] configuration is missing")
            return self.openai_compatible
        elif self.embedding_provider == "google":
            if self.google is None:
                raise ValueError("Google embedding provider selected but [google] configuration is missing")
            return self.google
        raise ValueError(f"Unknown embedding provider: {self.embedding_provider}")


def resolve_config_path() -> Path:
    """Resolve the config file path: LARAQ_CONFIG env var, else the default."""
    env_path = os.environ.get("LARAQ_CONFIG")
    if env_path:
        return Path(env_path)
    return DEFAULT_CONFIG_PATH


def load_config(config_path: str | Path | None = None) -> Config:
    """Load and validate configuration from a TOML file.

    Args:
        config_path: Explicit path to the config file. If omitted, resolves
            via LARAQ_CONFIG or the default ~/.laraq/config.toml.

    Raises:
        ConfigFileNotFoundError: If the config file doesn't exist.
        ConfigParseError: If the TOML file is malformed.
        ConfigValidationError: If the configuration is invalid.
    """
    path = Path(config_path) if config_path is not None else resolve_config_path()

    if not path.exists():
        raise ConfigFileNotFoundError(f"Configuration file not found: {path}")

    try:
        with open(path, "rb") as f:
            data = tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        raise ConfigParseError(f"Failed to parse TOML file: {e}") from e
    except OSError as e:
        raise ConfigParseError(f"Failed to read config file: {e}") from e

    try:
        config = Config(**data)
        config.config_path = str(path)
    except ValidationError as e:
        error_messages = []
        for error in e.errors():
            loc = " -> ".join(str(part) for part in error["loc"])
            error_messages.append(f"  {loc}: {error['msg']}")
        raise ConfigValidationError("Configuration validation failed:\n" + "\n".join(error_messages)) from e
    except ValueError as e:
        raise ConfigValidationError(str(e)) from e

    return config
