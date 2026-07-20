"""Standalone health check for laraq-mcp, runnable outside a Claude Code session.

    laraq-doctor

Reuses server.run_checks() so there is exactly one implementation of
"is this server ready?" shared with the check_server MCP tool.
"""

import sys

from laraq_mcp.server import run_checks


def main() -> int:
    results = run_checks()

    for check in results.get("checks", []):
        status = "OK  " if check["ok"] else "FAIL"
        print(f"[{status}] {check['name']}: {check['message']}")

    if results.get("ready"):
        print(f"\nready: embedding_provider={results['embedding_provider']}")
        return 0

    print("\nNOT READY")
    return 1


if __name__ == "__main__":
    sys.exit(main())
