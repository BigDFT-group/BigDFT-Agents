"""FastMCP server for laraq-mcp.

Exposes the deterministic half of the laraq pipeline as MCP tools:
check_server, research, validate, dry_run, execute. Everything that calls an
LLM (intent extraction, physics-parameter extraction, feasibility mapping,
query expansion, code generation) is a Claude Code / Codex subagent instead,
living in plugins/laraq/agents/ and plugins/laraq/codex-agents/ — not part
of this server.

Config is loaded lazily (first tool call, never at import) so a missing or
malformed config surfaces as a check_server/tool-call-time error, never a
server startup crash.

`execute` always runs code in-process. Remote/HPC execution is handled by
the separate `remotemanager` plugin, not by laraq itself.
"""

import threading
from typing import Any

from mcp.server.fastmcp import FastMCP

from laraq_mcp.config import Config, load_config
from laraq_mcp.dry_run import run_dry_run
from laraq_mcp.embeddings import create_embedding_client
from laraq_mcp.executors import local_execute
from laraq_mcp.research import get_or_build_index, research_multi
from laraq_mcp.validator import validate_code

mcp = FastMCP("laraq-mcp")

_lock = threading.Lock()
_config: Config | None = None
_embedding_client = None
_index = None  # (chunks, sources, embeddings)


def _get_config() -> Config:
    global _config
    if _config is None:
        _config = load_config()
    return _config


def _get_embedding_client():
    global _embedding_client
    if _embedding_client is None:
        _embedding_client = create_embedding_client(_get_config())
    return _embedding_client


def _get_index():
    global _index
    if _index is None:
        _index = get_or_build_index(_get_config(), _get_embedding_client())
    return _index


def run_checks() -> dict:
    """Run laraq-mcp's readiness checks: config, embedding, BigDFT import.
    Shared by the check_server tool and doctor.py so there's exactly one
    implementation of "is this server ready?"."""
    try:
        cfg = _get_config()
    except Exception as e:
        return {"ready": False, "checks": [{"name": "config", "ok": False, "message": str(e)}]}

    results: dict[str, Any] = {
        "ready": False,
        "embedding_provider": cfg.embedding_provider,
        "checks": [],
    }

    try:
        embedding_client = create_embedding_client(cfg)
        embedding = embedding_client.embed_one("test")
        results["checks"].append(
            {"name": "embedding", "ok": True, "message": f"Embedding dimension: {len(embedding)}"}
        )
    except Exception as e:
        results["checks"].append({"name": "embedding", "ok": False, "message": str(e)})
        return results

    try:
        import BigDFT  # noqa: F401

        results["checks"].append({"name": "bigdft", "ok": True, "message": "BigDFT import succeeded"})
    except Exception as e:
        results["checks"].append({"name": "bigdft", "ok": False, "message": str(e)})
        return results

    results["ready"] = True
    return results


@mcp.tool()
def check_server() -> dict:
    """Verify that laraq-mcp is ready to use.

    Call this first in a fresh session, before research or code generation.

    This checks embedding connectivity and BigDFT importability.

    If ready is false, stop and report the setup issue to the user instead of
    continuing. If the failure is a BigDFT import error, tell the user they
    need PyBigDFT and BigDFT installed in the environment running this server.
    """
    with _lock:
        return run_checks()


@mcp.tool()
def research(queries: list[str], top_k: int | None = None) -> str:
    """Search the BigDFT documentation for context relevant to one or more queries.

    Pass the original user query plus search hints and expanded search terms
    from the intent-extractor and query-expander subagents as separate
    entries in `queries` — this tool aggregates results across all of them
    internally (max score per chunk), so call it once per attempt rather than
    once per query variant.

    Call check_server first. Call this before invoking code-generator; pass
    the returned context string into code-generator's prompt.

    If validate or dry_run later fails, call this again (with a more targeted
    query informed by the error) before retrying code-generator.
    """
    with _lock:
        cfg = _get_config()
        client = _get_embedding_client()
        chunks, sources, embeddings = _get_index()
        k = top_k if top_k is not None else cfg.research.top_k
        return research_multi(queries, chunks, sources, embeddings, client, k)


@mcp.tool()
def validate(code: str) -> dict:
    """Validate generated code using pyflakes static analysis and an import check.

    Call this after extracting code from code-generator's response and
    before dry_run. Pass the code exactly as extracted from the fenced
    ```python block — do not modify it yourself.

    Returns:
        {"valid": true, "code": "<code>"} on success.
        {"valid": false, "error": "<message>", "code": "<code>"} on failure.

    Always use the returned "code" field (not your own copy) for dry_run and
    execute.

    If valid is false, call research again then code-generator again with
    fresh context (including this error) before retrying validate.
    """
    with _lock:
        result = validate_code(code)
        if result["valid"]:
            return {"valid": True, "code": code}
        return {"valid": False, "error": result["error"], "code": code}


@mcp.tool()
def dry_run(code: str, mpi_processes: int = 1) -> dict:
    """Test code execution with BIGDFT_MPIDRYRUN set to an MPI rank count.

    Call this after validate succeeds. Pass the "code" field from validate's
    response.

    This catches runtime import errors, missing attributes, and BigDFT
    configuration issues without running a full simulation. The default
    mpi_processes=1 is the standard dry run; use a larger value to have
    BigDFT estimate requirements for a larger MPI count.

    Dry run writes its log files into the current working directory. Reported
    memory is per MPI process. Read the dry-run log immediately after
    success — later runs may overwrite the same filename.

    Returns:
        {"success": true} on success — proceed to showing the user the code.
        {"success": false, "error": "<message>"} on failure — call research
        and code-generator again with fresh context before retrying.
    """
    with _lock:
        success, message = run_dry_run(code, mpi_processes=mpi_processes)
        if success:
            return {"success": True, "message": message, "mpi_processes": mpi_processes}
        return {"success": False, "error": message, "mpi_processes": mpi_processes}


@mcp.tool()
def execute(code: str) -> str:
    """Execute validated Python code and return the result.

    Only call this after validate and dry_run have succeeded and you have
    shown the user the generated code and received their explicit approval.
    Pass the "code" field from validate's response.

    Do NOT skip validate or dry_run before calling this — skipping them
    risks running broken code against the real BigDFT runtime.

    Returns the string result of f(), or an ERROR:-prefixed message on
    failure. This always runs in-process. For HPC/cluster execution, use
    the remotemanager plugin instead — see laraq-generating's "Running on
    a remote HPC cluster instead" section.
    """
    with _lock:
        return str(local_execute(code))


def main() -> None:
    """Run the FastMCP server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
