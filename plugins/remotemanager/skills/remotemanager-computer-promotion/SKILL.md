---
name: remotemanager-computer-promotion
description: Use when host and platform dictionaries, or remotecomputer-derived specs, must be turned into a validated remotemanager Computer before any Dataset or MCP workflow is built. Covers Computer construction, default completion, transport selection, connection testing, and safe promotion from machine dictionaries into execution-ready Computer objects.
---

# Remotemanager Computer Promotion

Use this skill when the task is to turn Python dictionaries describing a machine, host, or platform into a validated `remotemanager.Computer`.

This skill should be used before Dataset promotion when the machine definition itself is still being assembled or checked.

## Scope

The input can come from:

- plain Python dictionaries,
- `remotecomputer.get_platform_specs(...)`,
- `remotecomputer.get_machine_context(...)["platform"]`,
- a host dictionary plus a platform dictionary that must be merged.

The output is a `Computer` object that has been validated before it is used in a `Dataset` or MCP server.

## Core rule

Do not create a `Dataset` until the `Computer` definition has been tested.

The first validation step is `Computer.test_connection()`.

## Required fields

At minimum, a usable `Computer` usually needs:

- `host`
- `submitter`
- `template` or a resolved template string

In practice, you often also need:

- `python`
- `shell`
- `user`
- `port`
- `passfile`, `keyfile`, or another credential path
- scheduler-exposed parameters such as `nodes`, `mpi`, `omp`, and `time`

If the source dictionaries do not provide these explicitly, fill them with deliberate defaults. Do not leave them implicit without checking whether the target machine can use those defaults.

## Promotion pattern

Given a platform dictionary:

```python
from copy import deepcopy
from remotemanager import Computer


def promote_computer(platform_specs, defaults=None):
    specs = deepcopy(platform_specs)
    defaults = defaults or {}
    for key, value in defaults.items():
        specs.setdefault(key, value)
    return Computer(**specs)
```

Typical defaults are:

```python
defaults = {
    "python": "python3",
    "shell": "bash",
    "submitter": "bash",
}
```

## When using `remotecomputer`

If the machine information comes from `remotecomputer`, prefer this pattern:

```python
from remotecomputer import get_machine_context

ctx = get_machine_context(
    "irene",
    platform="frontend",
    application="1.9.7-RC_oneapi25",
)
platform_specs = ctx["platform"]
application_specs = ctx["application"]
```

Then promote the `Computer` from `platform_specs`, but use application data when needed to fill execution details such as the remote Python interpreter.

Pattern:

```python
specs = dict(platform_specs)
if "python" not in specs and application_specs.get("python_interpreter"):
    specs["python"] = application_specs["python_interpreter"]
machine = Computer(**specs)
```

## Transport rule

Do not force a localhost-only transport for remote hosts.

If you patch transport selection for localhost examples, restrict that patch to hosts like:

- `localhost`
- `127.0.0.1`

Remote hosts should keep the normal `remotemanager` transport resolution.

## Validation workflow

Use this order:

1. construct the `Computer`,
2. print or inspect the generated job script if needed,
3. call `Computer.test_connection()`,
4. only after that, build a `Dataset`.

Pattern:

```python
machine = Computer(**specs)
status = machine.test_connection(verbose=True)
print(status)
```

Use `test_connection()` to verify:

- the host can be reached,
- authentication files exist,
- the remote shell works,
- the Python executable is valid,
- the scheduler or submitter path is coherent,
- the selected transport can stage files.

## Interpreting failures

If `test_connection()` fails, stop and fix the machine definition first.

Common causes:

- missing `passfile` or `keyfile`
- wrong hostname or unresolved SSH alias
- local-only Python path incorrectly reused as remote `python`
- forcing `cp` transport on a non-local host
- missing `template`
- invalid submitter or shell

## Safe defaults for MCP servers

When promoting a `Computer` inside an MCP server, use explicit defaults and report them back to the caller.

Recommended summary fields:

- `host`
- `submitter`
- `python`
- `shell`
- `template_present`
- `connection_test_status`

If the server supports application-aware configuration, include:

- `application`
- `python_source`: whether `python` came from platform specs, application specs, or a fallback default

## Recommended agent workflow

If an agent is assembling a remote execution target from dictionaries, the intended sequence is:

1. resolve or merge the source dictionaries,
2. fill explicit defaults,
3. promote them to a `Computer`,
4. call `test_connection()`,
5. only then hand the `Computer` to `Dataset` or MCP lifecycle code.

This keeps machine-definition errors separate from Dataset errors.
