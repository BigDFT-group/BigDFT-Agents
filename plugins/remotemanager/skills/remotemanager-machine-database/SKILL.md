---
name: remotemanager-machine-database
description: Use when defining or revising machine YAML files and user_overrides.yaml for remotemanager-MCP, including platform/application structure, override layering, and remotemanager template placeholder syntax.
---

# Remotemanager Machine Database

Use this skill when an agent needs to create or update a machine database entry such as `localhost.yaml` or `irene.yaml`, or when it needs to separate official machine data from user-specific overrides.

## Goal

Produce two coherent inputs for the MCP server:

1. a machine YAML file in the machine database directory
2. an optional `user_overrides.yaml` file keyed by host name

The machine YAML should describe reusable machine facts. The override file should carry user-specific or site-specific adjustments.

## What belongs where

Put these in the machine YAML:

- scheduler templates
- platform names and connection mode
- generic shell / submitter / host information
- application names
- generic modules, preamble blocks, and interpreter names
- machine- or application-level runtime roots that are broadly valid for users of that machine

Put these in `user_overrides.yaml`:

- `passfile`
- user-specific `prefix` or install paths
- project/account names
- transport choice when it is user- or environment-dependent
- platform-specific authentication details

Do not put private user credentials or one-off paths in the machine YAML.

## Machine YAML structure

A machine file is keyed by top-level objects plus a `platforms:` mapping.

Minimal pattern:

```yaml
frontend_template: |
  #!/bin/bash
  #command:optional=False:default=ls#

batch_template: |
  #!/bin/bash
  #mpi:optional=False#
  #omp:default=1#
  #time:optional=False#
  #project:optional=False#
  #command:default=#

intel_oneapi_mpi:
  python_interpreter: python
  modules: python3 cmake inteloneapi mpi/intelmpi mkl
  remote_runtime_root: /scratch/$USER/remotemanager-mcp
  sourcedir: /scratch/$USER/project
  preamble: |
    export PREFIX=/scratch/$USER/binaries/current/suite
    source $PREFIX/bin/bigdftvars.sh

platforms:
  frontend:
    host: irene
    submitter: bash
    shell: bash
    kwargs:
      template: frontend_template
  batch:
    host: irene
    submitter: ccc_msub
    shell: bash
    kwargs:
      template: batch_template
```

## Meaning of the sections

- top-level `*_template` strings are referenced from `platforms.*.kwargs.template`
- top-level application entries such as `intel_oneapi_mpi` are selected by the MCP `application` argument
- `platforms` entries define how the remote `Computer` is instantiated
- `kwargs` is used to inject referenced top-level objects, especially templates

## Override file structure

The preferred override file is `user_overrides.yaml` in the machine database directory. It is keyed by host name.

Example:

```yaml
localhost:
  platform:
    shell: bash

irene:
  project: gen12049
  frontend:
    host: irene
    passfile: /tmp/irene
  batch:
    host: irene
    passfile: /tmp/irene
```

Supported forms under each host key:

- `platform:` merged into the resolved platform specs
- `application:` merged into the resolved application specs
- `combined:` merged after platform+application combination
- platform-named sections such as `frontend:` or `batch:` merged into the resolved platform
- application-named sections merged into the resolved application
- plain scalar keys such as `project:` merged into `combined`

## Template placeholder syntax

`remotemanager` templates use `#...#` placeholders.

Basic forms:

- `#name#`
- `#name:default=value#`
- `#name:optional=False#`
- `#name:default={expr}#`

Common options:

- `default=...` sets a default value
- `optional=False` makes a value required
- `hidden=True` keeps an internal variable out of the rendered script while still allowing dependent expressions
- `format=...` applies a formatter such as time formatting when supported by the template engine
- `requires=foo` declares dependency on another variable
- `static=True` freezes evaluation against later changes

Dynamic defaults use Python-like expressions in braces:

- `#nodes:default={(mpi*omp)/cores_per_node}#`
- `#jobname:default=RUN_{mpi}_{omp}#`

Escaping matters in defaults containing `:` or `=`. Use backslashes when needed.

## Practical template rules

For MCP campaigns, templates should normally expose:

- `command` for frontend execution templates
- scheduler resources such as `mpi`, `omp`, `time`, `nodes` for batch templates
- scheduler/account fields such as `project`, `queue`, `filesystem` when the machine requires them
- optional environment hooks such as `modules`, `module_preload`, `preamble`

The exposed placeholder names become candidate `append_campaign_run(..., run_options=...)` keys through `dataset.url.args`.

## Authoring checklist

Before finalizing a machine YAML:

1. ensure each platform points to a real template via `kwargs.template`
2. ensure at least one application entry exists
3. ensure the application provides `python_interpreter` if the remote Python is not implicit
4. keep user-specific values out of the machine YAML when possible
5. verify that required template placeholders correspond to the run options the campaign will need
6. test promotion with `get_machine_context(...)` and `build_computer(...)`
7. test `dataset.url.test_connection()` on a live campaign when remote connectivity matters

## Validation expectations

A valid machine definition should support these checks:

- `get_machine_context(host, platform, application)` resolves correctly
- `build_computer(context)` exposes the expected template args
- `resolve_runtime_layout(...)` produces sensible local and remote paths
- `test_campaign_connection` succeeds for a real configured campaign
