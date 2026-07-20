---
name: laraq-generating
description: Generate, validate, dry-run, and execute BigDFT Python code from a natural-language query, using laraq's subagents and MCP tools.
---

# laraq: BigDFT Python Code Generation

## Pipeline order

### 1. check_server() [MCP tool]
Call first in a fresh session. If `ready: false`, stop and report the issue —
do not continue.

### 2. Task → laraq:intent-extractor
Pass the user's query as the prompt. Read its response for `Intent:`,
`Calculation type:`, `Search hints:` — keep these as plain text for later steps.

### 3. Task → laraq:physics-params
Pass the user's query. Read its labeled-line response (or "No physics
parameters found").

### 4. Task → laraq:module-mapper
Pass the user's query. If `Feasible: no`, stop and report `Reason:` to the
user — do not proceed to research or code generation.

### 5. Task → laraq:query-expander
Pass the user's query. Collect its 3 output lines.

### 6. research(queries, top_k=3) [MCP tool]
Call once with `queries` = [the original user query] + the search hints from
step 2 + the 3 terms from step 5. Do not call research multiple times for a
single attempt — the tool aggregates internally.

### 7. Task → laraq:code-generator
Build a prompt containing: the user's query, intent + calculation type
(step 2), physics parameters (step 3), relevant modules (step 4), and the
research context (step 6). On retry (see below), also include the
previously failed code and its error.

Extract the code from the single ```python ... ``` fenced block in the
response. Do not execute it yourself.

### 8. validate(code) [MCP tool]
Pass the extracted code. Always use the returned `code` field (not your own
copy) in subsequent steps.
If `valid: false`: go back to step 5 with a more targeted query (include the
error), redo steps 6-7, then retry validate once. Do not retry with identical
inputs. Give up after one retry and report the failure to the user.

### 9. dry_run(code, mpi_processes=1) [MCP tool]
Pass validate's returned code. Same retry policy as step 8 on failure.
After success, find and read the BigDFT log file (log-*.yaml) written to the
current working directory — do this immediately, since later runs may
overwrite it — and report memory usage/warnings to the user. The reported
memory is per MPI process.

### 10. Show code + get approval
Show the full generated code in a code block (do not summarize it). Ask
"Shall I run this?" and wait for the user's explicit response. Do not skip or
abbreviate this — mandatory before step 11.

### 11. execute(code) [MCP tool]
Only after step 10's explicit approval. `execute` always runs the code
in-process on the machine running this MCP server — it takes no parameters
beyond `code`. If the user wants this run on an HPC cluster instead, do not
call `execute` — see "Running on a remote HPC cluster instead" below.

## Code contract
All generated code defines a single f() with no arguments; all imports go
inside f(); it must return its result (no print()); f() is called
automatically by dry_run and execute; file paths must be relative.

## Rules
- Never call execute without showing the code and receiving explicit approval.
- Never write or run BigDFT code yourself outside this pipeline.
- Always run steps 2-5 (all four subagents) before research — their output
  directly improves retrieval quality and code correctness.
- Each of steps 8 and 9 allows exactly one retry cycle (steps 5-7 redone)
  before giving up and reporting to the user.

## Running on a remote HPC cluster instead

laraq's own `execute` tool only ever runs code in-process. For HPC/cluster
submission, hand off to the separate `remotemanager` plugin instead of
calling `execute`:

1. Register the validated, dry-run-passed code as a function in
   `~/.config/remotemanager-mcp/function-registry.yaml` under `functions:`,
   using a `file:` entry (since it's extracted code, not a permanent module)
   pointing at a saved copy of the code, with `function: f`, a
   `description`, and `file_args: []` (laraq's f() takes no arguments, so
   `file_args` is normally empty; if the code needs input files, have it
   read them via relative paths and stage them through remotemanager's own
   Dataset extra_files mechanism instead of adding arguments to f()).
2. Then follow the `remotemanager` plugin's own MCP tool sequence (from its
   `remotemanager-dataset-promotion` skill): `describe_server_config` ->
   `list_computers` -> `describe_computer(host, platform, application)` ->
   `test_campaign_connection` -> `create_campaign(function_name, host,
   platform, application)` -> `append_campaign_run(args={})` ->
   `run_campaign` -> `wait_campaign` -> `fetch_campaign_results` ->
   `get_campaign_results`.
3. laraq's own `dry_run` tool (BIGDFT_MPIDRYRUN) checks a different thing
   than the two checks `remotemanager-dataset-promotion` documents before a
   real cluster submission: a BigDFT-specific local check with
   `SystemCalculator(dry_run=True)`, and remotemanager's own
   `Dataset.run(dry_run=True)` submission-plumbing check. Consider all
   three — laraq's BIGDFT_MPIDRYRUN dry run, remotemanager's SystemCalculator
   dry-run advice, and remotemanager's own submission dry-run — before a
   real cluster run, not just laraq's.
4. See the `remotemanager-dataset-promotion` skill for the full workflow —
   this section is a hand-off pointer, not a reimplementation.
