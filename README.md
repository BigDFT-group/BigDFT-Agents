# BigDFT-Agents

Claude Code and Codex plugin marketplace for the [BigDFT](https://bigdft.org)
electronic structure code: install and use BigDFT, generate and run BigDFT
calculations from natural language, and drive RemoteManager campaigns, all
from the agent.

## Cluster access moved to HPC Rookery

Submitting and monitoring jobs on TGCC **Irene** used to live here as the
`irene` plugin. It now lives in
[HPC Rookery](https://github.com/william-dawson/hpc-rookery), which serves
Irene alongside every other machine through one server, with this repo's
Irene guide, facts and skill content merged into it.

Install the two Rookery plugins next to these:

```
/plugin marketplace add william-dawson/hpc-rookery
/plugin install hpc@hpc-marketplace
/plugin install hpc-irene@hpc-marketplace
```

Rookery's tools take a facility argument, so an Irene call is
`get_resources(facility="irene")` rather than `get_resources()`. Settings move
from `~/.hpc-agent/irene.json`'s old shape to Rookery's — the same file path,
and `irene-configuring` there walks through it.

See [`AGENTS.md`](AGENTS.md) for the design rules an agent working on this
repo should know.

## Included Plugins

This marketplace currently distributes four plugins:

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
- `laraq`: generate, validate, dry-run, and execute BigDFT Python code from
  natural-language queries, via RAG research over the BigDFT documentation
  and subagent-driven analysis (intent extraction, physics-parameter
  extraction, feasibility checking, query expansion, code generation).
  Execution is always in-process; remote/HPC submission of the generated
  code uses the `remotemanager` plugin above, same as `bigdft`.

Project-wide marketplace maintenance rules live in `AGENTS.md`.

## Install

### Prerequisite: uv

The `remotemanager` and `laraq` plugins start their MCP servers with
`uv tool run`, so [`uv`](https://docs.astral.sh/uv/) must be installed and on
your `PATH` before Claude Code or Codex starts them:

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
/plugin install bigdft@bigdft-agents-marketplace
/reload-plugins
```

Swap `bigdft` for `bigdft-dev`, `remotemanager`, or `laraq` to install the
other plugins. `bigdft` and `bigdft-dev` are skills only -- no `uv`, MCP
server, or `PATH` setup needed.

### Codex

```text
codex plugin marketplace add BigDFT-group/BigDFT-Agents
```

Then open `/plugins`, install the plugins you want, and start a new thread.

For Irene jobs, add HPC Rookery's marketplace as shown at the top of this
file and run `/irene-demo` from there.
