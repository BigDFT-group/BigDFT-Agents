"""Health checks for the IreneAgent configuration.

    python -m irene_mcp.doctor

Reuses hpc_agent_core.doctor's config/guide/index/embedding checks, but
defines its own SSH+scheduler check rather than calling
hpc_agent_core.doctor.main() directly: that helper's check_ssh() expects a
single scheduler_probe command whose output *starts with* the scheduler's
name (e.g. "slurm 24.05.8"), which fits Slurm/Grid Engine but not Bridge —
there's no one Bridge command shaped like that, just several (ccc_msub,
ccc_mprun, ccc_mpp, ccc_mpinfo) that need to simply exist. Per
hpc_agent_core.doctor's own docstring, this is the expected way to diverge:
reuse the independently-callable check_* functions that fit, write a local
replacement for the one that doesn't. The commands-on-PATH loop itself now
comes from hpc_agent_core.doctor.check_commands_on_path(), promoted there
after this and Fugaku's PJM check independently reimplemented the same
~15 lines.
"""
import sys

from hpc_agent_core.doctor import (
    OK,
    FAIL,
    check_commands_on_path,
    check_config_file,
    check_docs_guide_bundled,
    check_docs_index,
    check_embedding,
)
from hpc_agent_core.middleware import is_local_host, run_command
from irene_mcp import config  # noqa: F401 -- registers via configure()

_BRIDGE_COMMANDS = {"ccc_msub", "ccc_mprun", "ccc_mpp", "ccc_mpinfo"}


def check_ssh_and_bridge() -> bool:
    host = config.ssh_host()
    # "ssh (host): connected" would be misleading when host is localhost/
    # 127.* — is_local_host matches middleware.get_frontend()'s own routing
    # (a bare local shell, no ssh subprocess at all).
    label = f"local ({host})" if is_local_host(host) else f"ssh ({host})"
    try:
        output = run_command("echo irene-doctor-ok && hostname")
    except Exception as e:
        print(f"{FAIL} {label}: {e}")
        return False
    if "irene-doctor-ok" not in output:
        print(f"{FAIL} {label}: unexpected response: {output[:200]}")
        return False
    print(f"{OK} {label}: connected to {output.strip().splitlines()[-1]}")
    return check_commands_on_path(_BRIDGE_COMMANDS, "bridge commands")


def main() -> int:
    results = [
        check_config_file(),
        check_ssh_and_bridge(),
        check_docs_guide_bundled(),
        check_docs_index(),
        check_embedding(),
    ]
    if all(results):
        print("\nAll checks passed.")
        return 0
    print("\nSome checks FAILED — see above.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
