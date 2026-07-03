---
name: remotemanager-configuring
description: Use when setting up or troubleshooting the RemoteManager plugin for first use, especially the user-local ~/.config/remotemanager-mcp/config.yaml, function registry, machine database, overrides, runtime roots, and MCP startup behavior.
---

# Configuring RemoteManager Plugin

The marketplace plugin is generic: it starts `remotemanager-generic-mcp` with
`uv tool run` from the external `remotemanager-MCP` package and does not pass
user-specific environment variables in `.mcp.json`.

User-specific information must live under a documented local config URI. The
default config file is:

```text
~/.config/remotemanager-mcp/config.yaml
```

At first use, check whether this file exists. If it is absent, warn the user and
prepare it before trying to create campaigns. A minimal config is:

```yaml
function_registry: ~/.config/remotemanager-mcp/function-registry.yaml
machine_db: ~/.config/remotemanager-mcp/machines
overrides: ~/.config/remotemanager-mcp/user-overrides.local.yaml
runtime_root: /tmp/remotemanager-mcp-runtime
remote_root: /scratch/$USER/remotemanager-mcp
```

The config file should point to reusable local files. It should not contain raw
passwords. Put private or user-specific execution details in the overrides file,
for example:

```yaml
irene:
  project: gen12345
  frontend:
    host: irene
    passfile: /tmp/irene
  batch:
    host: irene
    passfile: /tmp/irene
```

Recommended first-use checks:

1. Ensure `uv` is available to the host process that starts MCP servers.
2. Ensure `~/.config/remotemanager-mcp/config.yaml` exists.
3. Ensure `function_registry` points to a YAML file with a top-level `functions` mapping.
4. Ensure `machine_db` points to a directory containing machine YAML files such as `irene.yaml`.
5. Ensure `overrides` exists when authentication, project accounts, or private install paths are required.
6. Use `describe_server_config` if the MCP server is active; it reports config status without exposing file contents.
7. Use `list_functions`, `list_computers`, and `describe_computer` before creating campaigns.
8. Use `test_campaign_connection` and `remote_command` before submitting real remote jobs.

Scope of generic use:

- The plugin can run any function declared in the configured function registry.
- The plugin can target any host/platform/application combination declared in the configured machine database.
- The marketplace does not own the Python implementation; `remotemanager-MCP` remains in its external repository and can evolve independently.
- The marketplace does own skill guidance and the stable plugin/MCP launch metadata.

For Irene campaigns, do not rely on implicit project defaults. Check available
projects through the Irene plugin or `ccc_compuse`, then pass the selected
project explicitly in campaign `run_options`.
