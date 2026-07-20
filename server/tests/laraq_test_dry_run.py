import os

from laraq_mcp.dry_run import run_dry_run


def test_negative_mpi_processes_fails_immediately():
    success, message = run_dry_run("def f():\n    return 1\n", mpi_processes=0)
    assert success is False
    assert "mpi_processes must be a positive integer" in message


def test_success_sets_env_var_and_restores_it():
    os.environ.pop("BIGDFT_MPIDRYRUN", None)

    success, message = run_dry_run("def f():\n    return 1\n", mpi_processes=4)
    assert success is True
    assert "BIGDFT_MPIDRYRUN=4" in message
    assert os.environ.get("BIGDFT_MPIDRYRUN") is None


def test_raising_code_reports_traceback():
    code = "def f():\n    raise ValueError('boom')\n"
    success, message = run_dry_run(code)
    assert success is False
    assert "ValueError" in message
    assert "boom" in message
    assert "Traceback" in message


def test_missing_f_reports_specific_error():
    success, message = run_dry_run("x = 1\n")
    assert success is False
    assert "did not define a callable function f()" in message


def test_env_and_path_restored_even_on_exception():
    os.environ["BIGDFT_MPIDRYRUN"] = "999"
    import sys

    path_before = sys.path.copy()

    success, _ = run_dry_run("def f():\n    raise RuntimeError('x')\n", mpi_processes=2)
    assert success is False
    assert os.environ.get("BIGDFT_MPIDRYRUN") == "999"
    assert sys.path == path_before

    os.environ.pop("BIGDFT_MPIDRYRUN", None)
