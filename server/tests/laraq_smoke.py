"""Live smoke test for the laraq MCP server over stdio.

Usage: python tests/laraq_smoke.py [--execute]
"""
import argparse
import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_DIR = Path(__file__).resolve().parent.parent
RUN_SH = SERVER_DIR / "run.sh"


async def call(session: ClientSession, tool: str, args: dict | None = None) -> str:
    result = await session.call_tool(tool, args or {})
    text = "\n".join(c.text for c in result.content if c.type == "text")
    status = "ERROR" if result.isError else "ok"
    print(f"--- {tool} [{status}] ---\n{text[:1200]}\n")
    if result.isError:
        raise RuntimeError(f"{tool} failed: {text}")
    return text


async def laraq_checks(execute: bool) -> None:
    params = StdioServerParameters(command=str(RUN_SH), args=["laraq_mcp.server"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print(f"laraq-mcp tools: {[t.name for t in (await session.list_tools()).tools]}\n")

            await call(session, "check_server")
            await call(session, "research", {"queries": ["Atom class", "get_position method"]})

            good_code = "def f():\n    return 1\n"
            validate_result = await call(session, "validate", {"code": good_code})
            code = json.loads(validate_result)["code"]

            await call(session, "dry_run", {"code": code})

            if not execute:
                return

            out = await call(session, "execute", {"code": code})
            assert out == "1", f"expected '1', got {out!r}"


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="Also run execute() on trivial code.")
    args = parser.parse_args()
    await laraq_checks(execute=args.execute)
    print("SMOKE TEST PASSED")


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
