---
name: laraq-configuring
description: Configure the laraq plugin — set the embedding provider. Use when the plugin is first installed, when tool calls report a missing config file, or when check_server fails.
---

# laraq: Configuration

## 1. Config file location

`~/.laraq/config.toml`, or set `LARAQ_CONFIG` to point at a different path.
There is no CLI flag for this — the MCP server resolves its own config path
at tool-call time.

## 2. Minimal config

Pick one embedding provider and fill in its section. Example with Ollama:

```toml
embedding_provider = "ollama"

[ollama]
base_url = "http://localhost:11434"
embedding_model = "qwen3-embedding"
```

Other providers:

```toml
[openai_compatible]
base_url = "https://api.openai.com/v1"
api_key = "sk-..."
embedding_model = "text-embedding-3-small"
```

```toml
[google]
api_key = "..."
embedding_model = "text-embedding-004"
```

## 3. Execution

`execute` always runs generated code in-process on the machine running this
MCP server — no config toggle, no `[remote]` section, no job template.

For remote/HPC execution, see the `remotemanager` plugin instead
(`remotemanager-configuring` skill) — laraq itself only runs code
in-process. See laraq-generating's "Running on a remote HPC cluster
instead" section for the hand-off workflow.

## 4. Verify

Call `check_server` (or run `laraq-doctor` from a shell outside a session).
If `ready: false`, read the `checks` list for the first failing entry:
- `config`: the file is missing or malformed — fix the path/TOML syntax.
- `embedding`: the embedding provider is unreachable or misconfigured.
- `bigdft`: PyBigDFT is not importable in the environment running this
  server — install PyBigDFT/BigDFT there (see
  https://gitlab.com/l_sim/bigdft-suite), not in the plugin itself.
