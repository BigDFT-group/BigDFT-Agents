# BigDFT-Agents

Claude Code and Codex plugin marketplace for the [BigDFT](https://bigdft.org)
electronic structure code and the TGCC **Irene** supercomputer at CEA: install
and use BigDFT, run remote calculations with RemoteManager, and submit/monitor
Bridge jobs on Irene, all from the agent.

Irene is CPU-first. The normal target is the `rome` partition: 2,286 AMD Rome
nodes with 128 cores per node. Specialized `xlarge` and V100-family partitions
cover large-memory and GPU workloads. Built as a thin machine-specific "skin"
on top of [`hpc-agent-core`](https://pypi.org/project/hpc-agent-core/) — see
[hpc-agent-core's `PORTING.md`](https://github.com/william-dawson/hpc-agent-core/blob/main/PORTING.md)
for the general porting guide this repo follows, and
[`AGENTS.md`](AGENTS.md) for the design rules and cluster facts an agent
working on this repo should know.

## Included Plugins

This marketplace currently distributes four plugins:

- `irene`: live TGCC Irene status, filesystem, job, and documentation tools.
- `remotemanager`: RemoteManager Dataset campaign tools. The Python MCP server
  remains in the external `remotemanager-MCP` repository and is installed at
  launch time with `uv tool run`. User-specific paths are read from
  `~/.config/remotemanager-mcp/config.yaml`, not from marketplace metadata.
- `bigdft`: skills for using the BigDFT electronic structure code as an end
  user -- install from source, generate input files, build PyBigDFT systems,
  configure pseudopotentials and linear scaling, and parse logfile output.
  Skills only, no MCP server. Remote execution of BigDFT calculations uses
  the `remotemanager` plugin above.
- `bigdft-dev`: developer guides for BigDFT's Fortran internals -- Futile,
  ATlab, liborbs, PSolver, KB projectors, and the input-variable pipeline.
  Skills only, no MCP server.

Project-wide marketplace maintenance rules live in `AGENTS.md`. Everything
below is about the `irene` plugin specifically.

## Configure

Settings live in `~/.hpc-agent/irene.json` (the common directory shared by
every hpc-agent-core plugin):

```json
{
  "ssh": {"host": "irene"},
  "computer": {"passfile": "/tmp/irene"},
  "defaults": {"account": "gen12345", "filesystems": "scratch,work"}
}
```

- `ssh.host` is a `~/.ssh/config` alias, TGCC-provided `user@host`, or
  `"localhost"` if the agent is running directly on an Irene front-end node
  (no SSH needed at all). `IRENE_HOST` overrides it.
- `computer.passfile` is an optional password file for SSH auth (only
  needed if Irene requires it for your account). If you configured this
  plugin before it moved onto hpc-agent-core, move this value here from
  its old location, `ssh.passfile` — that location is no longer read.
- `defaults.account` is the TGCC project charged when a job doesn't set
  `attributes.account` explicitly (the backend still validates it against
  `ccc_compuse` at submit time). The old top-level `account` key still
  works too. `IRENE_ACCOUNT` overrides both.
- `defaults.filesystems` is the default Bridge `-m` value; every Irene job
  submission must declare filesystems. The old top-level `filesystems` key
  still works too. `IRENE_FILESYSTEMS` overrides both.
- A legacy `~/.irene/config.json` is still read if it's the only config
  present.

Docs search works offline with BM25 over the packaged guide (no shared
embedding endpoint is configured for Irene).

## Install

### Prerequisite: uv

The plugin starts its MCP servers with `uv tool run` from this repository's
`main` branch, so [`uv`](https://docs.astral.sh/uv/) must be installed and
on your `PATH` before Claude Code or Codex starts the plugin:

```bash
brew install uv        # or: curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart Claude Code or Codex after installing uv so the plugin process
inherits the updated `PATH`. If the host application is launched from a
desktop menu rather than a shell, it may not inherit `PATH` at all — in
that case, use the manual `.mcp.json` form below with an absolute path to
`uv` instead of relying on `PATH`.

### Claude Code

```text
/plugin marketplace add BigDFT-group/BigDFT-Agents
/plugin install irene@bigdft-agents-marketplace
/reload-plugins
```

Swap `irene` for `remotemanager`, `bigdft`, or `bigdft-dev` to install the other
plugins. `bigdft` and `bigdft-dev` are skills only -- no `uv`, MCP server, or
`PATH` setup needed.

### Codex

```text
codex plugin marketplace add BigDFT-group/BigDFT-Agents
```

Then open `/plugins`, install `irene`, start a new thread, and run
`/irene-demo` to verify the connection end-to-end.

### Manual (any MCP-compatible client)

Both options below only register the MCP servers — copy `plugins/irene/skills/`
into wherever your client loads skills from too (this varies by client).

#### Option A — Using Hatch!

[Hatch!](https://github.com/CrackingShells/Hatch) registers MCP servers on any
supported host from a single command. Install it once, then configure both
servers — replace `<host>` with your target platform (`claude-code`, `codex`,
`cursor`, `vscode`, `claude-desktop`, `kiro`, `gemini`, `lmstudio`, or any other
[supported host](https://github.com/CrackingShells/Hatch#supported-mcp-hosts)):

```bash
pip install hatch-xclam

hatch mcp configure irene-hpc --host <host> \
  --command uv \
  --args "tool run --quiet --from git+https://github.com/BigDFT-group/BigDFT-Agents.git@main#subdirectory=server irene-hpc-mcp"

hatch mcp configure irene-docs --host <host> \
  --command uv \
  --args "tool run --quiet --from git+https://github.com/BigDFT-group/BigDFT-Agents.git@main#subdirectory=server irene-docs-mcp"
```

To replicate the same configuration to additional hosts:

```bash
hatch mcp sync --from-host <host> --to-host cursor,vscode
```

#### Option B — Edit `.mcp.json` directly

Create or edit `.mcp.json` in your project root:

```json
{
  "mcpServers": {
    "irene-hpc": {
      "command": "uv",
      "args": ["tool", "run", "--quiet", "--from", "git+https://github.com/BigDFT-group/BigDFT-Agents.git@main#subdirectory=server", "irene-hpc-mcp"],
      "env": {}
    },
    "irene-docs": {
      "command": "uv",
      "args": ["tool", "run", "--quiet", "--from", "git+https://github.com/BigDFT-group/BigDFT-Agents.git@main#subdirectory=server", "irene-docs-mcp"],
      "env": {}
    }
  }
}
```

If `uv` isn't reliably on `PATH` for the process that starts MCP servers,
replace `"command": "uv"` with an absolute path (e.g.
`/home/you/.local/bin/uv`) in either option above.

## Verify

```bash
uv tool run --quiet --from git+https://github.com/BigDFT-group/BigDFT-Agents.git@main#subdirectory=server irene-doctor
```

All lines should read `✓` except possibly embedding (this machine has no
shared endpoint configured at all, so it's expected to read `!`, not `✗` —
docs search falls back to BM25 keyword search regardless).

## Development

```bash
cd server
uv run python -m irene_mcp.doctor          # health check
uv run python tests/smoke.py               # read-only MCP stdio test
uv run python tests/smoke.py --job         # + submits a real tiny job
```

Rebuilding the docs index after editing `irene_guide.md`:

```bash
cd server
uv run python -m irene_mcp.ingest --no-embed
```

Commit the resulting `irene_mcp/data/docs_index/` (just `chunks.json` — no
`embeddings.npy`, since no embedding endpoint is configured for Irene).

**No live Irene SSH access was available while porting this plugin onto
hpc-agent-core** — see `AGENTS.md`'s "hpc-agent-core migration — validation
status" section for exactly what was and wasn't verified before treating
this as production-ready.
