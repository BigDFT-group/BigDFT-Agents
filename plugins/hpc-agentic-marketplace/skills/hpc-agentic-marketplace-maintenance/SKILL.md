---
name: hpc-agentic-marketplace-maintenance
description: Use when adding, updating, validating, or documenting plugins in the HPC-Agentic-SDK marketplace, including plugin-specific skills, MCP launch metadata, public-vs-user-local configuration boundaries, and refresh/reinstall procedures.
---

# HPC-Agentic-SDK Marketplace Maintenance

Use this skill for any change to the marketplace repository, including existing
plugin updates and new plugin additions.

## Core Rule

Marketplace metadata must be general and portable. User-specific information
must live in a separate, documented local URI such as:

```text
~/.config/<plugin-name>/config.yaml
```

Do not put these in plugin `.mcp.json`, marketplace manifests, or public skills:

- passfiles or passwords
- private project/account IDs
- private installation prefixes
- user home paths
- personal SSH aliases unless clearly examples
- local runtime directories that are not examples

Each plugin that needs user information must provide a configuring skill that:

1. names the default config URI,
2. checks whether the config exists at first use,
3. prepares a minimal config when absent,
4. explains which values belong in local overrides,
5. exposes a validation sequence before real remote work.

## Updating An Existing Plugin

1. Fetch and inspect the repository status before editing.
2. Read the plugin manifest, `.mcp.json`, and relevant skills.
3. Keep MCP launch metadata generic. Prefer config files over static env vars.
4. Update plugin-specific skills when behavior or setup changes.
5. Validate JSON manifests and run any package tests for affected MCP servers.
6. Commit and push changes, then refresh/reinstall the plugin in the client.

## Adding A New Plugin

A plugin directory should have:

```text
plugins/<plugin-name>/.codex-plugin/plugin.json
plugins/<plugin-name>/.claude-plugin/plugin.json
plugins/<plugin-name>/.mcp.json        # only when the plugin starts MCP servers
plugins/<plugin-name>/skills/...       # at least one usage/configuring skill
```

Add it to:

```text
.agents/plugins/marketplace.json
.claude-plugin/marketplace.json
```

Plugin manifests should include display metadata, repository, keywords, skills,
and `mcpServers` only if `.mcp.json` exists.

## MCP Launcher Pattern

Prefer a generic launcher like:

```json
{
  "command": "uv",
  "args": ["tool", "run", "--quiet", "--from", "<package-source>", "<entrypoint>"],
  "env": {}
}
```

If the server needs user paths or credentials, the server should resolve them
from its own local config file. If an env var is needed, limit it to selecting
the config URI, for example `PLUGIN_CONFIG=/path/to/config.yaml`.

## Skill Expectations

Each plugin should include skills for its actual scope:

- configuring skill: first-use checks, config URI, validation steps
- usage skill: normal workflows and safe defaults
- reference skill when the plugin wraps a specific facility or API
- maintenance notes only when the plugin has external package or schema coupling

## Refresh Procedure

After pushing marketplace changes, users may need to refresh/reinstall the
marketplace/plugin and start a new session. MCP tools are loaded at session
startup; updating files in the repository does not add tools to an already
running session.
