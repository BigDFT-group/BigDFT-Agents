# BigDFT-Agents — Agent Instructions

This repository is the public marketplace/distribution layer for HPC agentic
plugins. It currently includes:

- `plugins/irene`: TGCC Irene skills and MCP launch metadata.
- `server/irene_mcp`: Python implementation for the Irene MCP servers.
- `plugins/remotemanager`: marketplace plugin for the external
  `remotemanager-MCP` Python package.
- `plugins/bigdft`: skills-only plugin for using the BigDFT electronic
  structure code as an end user (install, input generation, PyBigDFT
  systems, pseudopotentials, linear scaling, logfile parsing).
- `plugins/bigdft-dev`: skills-only plugin of developer guides for BigDFT's
  Fortran internals (Futile, ATlab, liborbs, PSolver, KB projectors, the
  input-variable pipeline). Kept separate from `plugins/bigdft` so a user
  running calculations doesn't have to install six library-internals
  skills, and a BigDFT source contributor doesn't get input-file skills
  they don't need.
- `plugins/laraq`: generates, validates, dry-runs, and executes BigDFT
  Python code from natural-language queries via RAG research and
  subagent-driven analysis. `server/laraq_mcp` (a sibling Python package to
  `server/irene_mcp`, same `server/pyproject.toml`) provides the
  deterministic MCP tools (`check_server`, `research`, `validate`,
  `dry_run`, `execute` — always in-process); the LLM-calling analysis steps
  are Claude Code subagents (`plugins/laraq/agents/*.md`), with manual-
  install Codex TOML mirrors at `plugins/laraq/codex-agents/*.toml` since
  Codex has no plugin-bundling field for custom agents yet.

## Design Rules

- Keep marketplace metadata general, portable, and free of user-specific values.
- User-specific information belongs in documented local config URIs, usually
  `~/.config/<plugin-name>/config.yaml`, not in `.mcp.json` or marketplace JSON.
- Each plugin that needs user information must provide a configuring skill that
  names the config URI, checks first-use prerequisites, explains local override
  files, and exposes a validation sequence before real remote work.
- Workflow guidance belongs in plugin `skills/`, not long MCP tool docstrings.
- MCP stdio servers must not print ordinary diagnostics to stdout.
- Do not commit private passfiles, project/account IDs, private install prefixes,
  or user-local runtime paths except as clearly marked examples.

## Marketplace Structure

A plugin directory should normally contain:

```text
plugins/<plugin-name>/.codex-plugin/plugin.json
plugins/<plugin-name>/.claude-plugin/plugin.json
plugins/<plugin-name>/.mcp.json        # only when the plugin starts MCP servers
plugins/<plugin-name>/skills/...       # at least one usage/configuring skill
```

Register plugins in both marketplace manifests:

```text
.agents/plugins/marketplace.json
.claude-plugin/marketplace.json
```

Plugin manifests should include display metadata, repository, keywords, skills,
and `mcpServers` only if `.mcp.json` exists.

Skill directories and their `name:` frontmatter must be prefixed with the
plugin name (`irene-configuring`, `remotemanager-dataset-promotion`,
`bigdft-install`, `bigdft-dev-futile`), even though the skill is invoked as
`/<plugin>:<skill-name>` and the prefix repeats the plugin name. This keeps
skill names unambiguous when multiple plugins are installed together. If a
plugin's skills split into more than one logical group (for example BigDFT's
end-user vs. Fortran-developer skills), prefer a second plugin over deeper
prefixing or subdirectories — skill discovery expects a flat `skills/*/SKILL.md`
layout, and a second plugin lets users install only the group they need.

## MCP Launcher Pattern

Prefer generic launch metadata such as:

```json
{
  "command": "uv",
  "args": ["tool", "run", "--quiet", "--from", "<package-source>", "<entrypoint>"],
  "env": {}
}
```

If a server needs user paths or credentials, the Python package should resolve
those from its own local config file. If an environment variable is needed, limit
it to selecting the config URI, for example `PLUGIN_CONFIG=/path/to/config.yaml`.

## Updating Existing Plugins

1. Fetch and inspect repository status before editing.
2. Read the plugin manifest, `.mcp.json`, and relevant skills.
3. Keep MCP launch metadata generic. Prefer config files over static env vars.
4. Update plugin-specific skills when behavior or setup changes.
5. Validate JSON manifests and run affected MCP package tests.
6. Commit and push changes, then refresh/reinstall the plugin in the client.

## Adding A New Computer

For a new machine that only needs RemoteManager campaign execution, prefer a
RemoteManager machine configuration rather than a new full MCP server:

```text
~/.config/remotemanager-mcp/machines/<machine>.yaml
~/.config/remotemanager-mcp/user-overrides.local.yaml
```

Create a new facility plugin only when the machine needs custom live status,
filesystem, documentation, or scheduler tools beyond generic RemoteManager
campaign execution.

## Irene Rules

- Irene is CPU-first. Default normal jobs to `rome`.
- Batch scripts use TGCC Bridge `#MSUB` directives and submit with `ccc_msub`.
- Parallel work launches with `ccc_mprun`.
- Job submissions require explicit `-q <partition>`, `-A <project>`, and
  `-m <filesystems>`.
- Before submitting an Irene job, check available projects and ask the user when
  no project was explicitly specified.
- Live status comes from Bridge commands such as `ccc_mpinfo`, `ccc_mpp`,
  `ccc_mstat`, `ccc_macct`, `ccc_mqinfo`, `ccc_compuse`, and `ccc_myproject`.
- Do not encourage frequent scheduler polling; TGCC prohibits `watch` on
  scheduler commands.

## Irene Development

The Irene guide is `server/irene_mcp/data/irene_guide.md`. Rebuild the BM25
index with:

```bash
cd server
python -m irene_mcp.rag.ingest --no-embed
```

Embeddings are optional and not committed by default.

```bash
cd server
python3 -m venv .venv
.venv/bin/pip install -e .
.venv/bin/python -m irene_mcp.doctor
.venv/bin/python tests/smoke.py
```

`tests/smoke.py --job` submits a real job and consumes allocation time.

## BigDFT Rules

- `plugins/bigdft` and `plugins/bigdft-dev` skills follow the authoring
  conventions from the upstream `bigdft-skills` source repo: YAML
  frontmatter, ask the user one question at a time, auto-detect what's
  possible before asking, include code building blocks as fenced
  Python/Fortran, and use `# FILL` comments for values the agent should
  customize.
- Do not add a RemoteManager connection/dataset skill to `plugins/bigdft` or
  `plugins/bigdft-dev`. That responsibility belongs to `plugins/remotemanager`
  (MCP-backed campaign tools). The upstream `bigdft-skills` repo's `remote`
  and `dataset` skills were intentionally dropped when integrating into this
  marketplace because they duplicated raw-Python RemoteManager guidance that
  `plugins/remotemanager` already covers through MCP tools and machine-database
  conventions. BigDFT-specific remote-execution advice (for example,
  validating input locally with `SystemCalculator(dry_run=True)` before
  submitting) lives in `plugins/remotemanager`'s
  `remotemanager-dataset-promotion` skill instead.

## laraq Rules

- `plugins/laraq`'s own `execute` tool always runs in-process. Do not add
  remote/HPC submission logic to `server/laraq_mcp` — that responsibility
  belongs to `plugins/remotemanager`, same principle as the BigDFT Rules
  above. `laraq-generating`'s "Running on a remote HPC cluster instead"
  section is a hand-off pointer to `remotemanager`'s own MCP tools and
  `remotemanager-dataset-promotion` skill, not a reimplementation.
- `server/laraq_mcp` is a sibling package to `server/irene_mcp` in the same
  `server/pyproject.toml` (broadened `packages.find.include`, merged
  dependencies) — not a separate repo, not a uv workspace. Follow this
  pattern for any future in-house (non-externally-owned) MCP server added
  to this marketplace; reserve the `remotemanager`-style external-repo
  pattern for code genuinely owned/maintained elsewhere.
- Codex has no `agents`-bundling manifest field (only `skills`/`mcpServers`/
  `apps`/`hooks`), so laraq's Codex subagents at `plugins/laraq/codex-agents/
  *.toml` are not auto-installed — `laraq-configuring`/the README document a
  manual copy into `~/.codex/agents/` or `<project>/.codex/agents/`. Update
  these TOML mirrors any time `plugins/laraq/agents/*.md` changes; keep the
  `name`/`description`/prompt content in sync by hand (same "two copies,
  synced by hand" pattern as bundled documentation elsewhere in this repo).

## laraq Development

```bash
cd server
uv run pytest tests/laraq_test_*.py -v
uv run python -m laraq_mcp.doctor
uv run python tests/laraq_smoke.py [--execute]
```

`tests/laraq_smoke.py --execute` runs a trivial `def f(): return 1` snippet
through `execute` — harmless, unlike Irene's `--job`, which consumes real
allocation time.

## Refresh Procedure

After pushing marketplace changes, users may need to refresh/reinstall the
marketplace/plugin and start a new session. MCP tools are loaded at session
startup; updating files in the repository does not add tools to an already
running session.
