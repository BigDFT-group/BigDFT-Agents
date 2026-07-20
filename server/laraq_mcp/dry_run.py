"""Dry-run execution: exercises generated code with BIGDFT_MPIDRYRUN set.

BigDFT reads BIGDFT_MPIDRYRUN to fake a given rank count and go through
startup/input validation without running a real simulation.
"""

import os
import sys
import traceback
from io import StringIO


def run_dry_run(code: str, mpi_processes: int = 1) -> tuple[bool, str]:
    """Execute code in dry-run mode with BIGDFT_MPIDRYRUN set to a rank count.

    Args:
        code: Python source defining f().
        mpi_processes: Value to assign to BIGDFT_MPIDRYRUN.

    Returns:
        (success, message).
    """
    if mpi_processes <= 0:
        return (False, "Dry run failed: mpi_processes must be a positive integer")

    original_value = os.environ.get("BIGDFT_MPIDRYRUN")
    old_stdout = sys.stdout
    old_path = sys.path.copy()

    try:
        os.environ["BIGDFT_MPIDRYRUN"] = str(mpi_processes)
        sys.stdout = StringIO()

        cwd = os.getcwd()
        if cwd not in sys.path:
            sys.path.insert(0, cwd)

        exec_globals: dict = {}
        exec(code, exec_globals)

        if "f" in exec_globals and callable(exec_globals["f"]):
            exec_globals["f"]()
        else:
            return (False, "ERROR: Code did not define a callable function f()")

        return (True, f"Dry run completed successfully with BIGDFT_MPIDRYRUN={mpi_processes}")

    except Exception as e:
        return (False, f"Dry run failed: {type(e).__name__}: {str(e)}\n\n{traceback.format_exc()}")

    finally:
        if original_value is None:
            os.environ.pop("BIGDFT_MPIDRYRUN", None)
        else:
            os.environ["BIGDFT_MPIDRYRUN"] = original_value
        sys.stdout = old_stdout
        sys.path = old_path
