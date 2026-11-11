# BigDFT-Agents — Agent Instructions

This repository is the public marketplace/distribution layer for HPC agentic
plugins. It currently includes:

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
  same `server/pyproject.toml`) provides the
  deterministic MCP tools (`check_server`, `research`, `validate`,
  `dry_run`, `execute` — always in-process); the LLM-calling analysis steps
  are Claude Code subagents (`plugins/laraq/agents/*.md`), with manual-
  install Codex TOML mirrors at `plugins/laraq/codex-agents/*.toml` since
  Codex has no plugin-bundling field for custom agents yet.

(Note: this repository has been renamed twice — `HPC-Agentic-SDK` →
`IreneAgent` → `BigDFT-Agents`. Some older external references may still
use an earlier name; GitHub redirects both.)

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

If the machine needs more than that — live status, filesystem, documentation
or scheduler tools — it belongs in HPC Rookery as a facility, not here as a
plugin. See the next section.

## Cluster access lives in HPC Rookery

Irene used to be served from this repo as the `irene` plugin and
`server/irene_mcp`. Both are gone: Irene is now one facility in
[HPC Rookery](https://github.com/william-dawson/hpc-rookery), which serves
every machine through a single facility-parametrized server, and this repo's
Irene guide, facts and skill content were merged into it first so nothing was
lost.

Consequences for work in this repo:

- Do not add cluster plugins or machine MCP servers here. A new machine is a
  pull request against Rookery adding one `facilities/<slug>/` directory; see
  its `PORTING.md`.
- There is no `hpc-agent-core` dependency any more. `server/pyproject.toml`
  carries only `laraq_mcp`'s own dependencies.
- Rookery's tools take a facility argument, so Irene examples in these skills
  read `facility="irene"`. A skill written against the old single-machine
  signature is wrong, not merely dated.
- BigDFT and RemoteManager still reference Irene as a *target* — rcfile names
  like `rcfiles/irene.rc`, machine-database entries like `irene.yaml`, a
  `passfile` path. Those are about BigDFT builds and RemoteManager machine
  records, not about a plugin here, and they stay.

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
- `server/laraq_mcp` is the only package in the
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
