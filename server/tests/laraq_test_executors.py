from laraq_mcp.executors import local_execute


def test_local_execute_good_code():
    result = local_execute("def f():\n    return 42\n")
    assert result == 42


def test_local_execute_raising_code():
    result = local_execute("def f():\n    raise ValueError('boom')\n")
    assert isinstance(result, str)
    assert result.startswith("ERROR:")
    assert "boom" in result


def test_local_execute_missing_f():
    result = local_execute("x = 1\n")
    assert result == "ERROR: Code did not define a callable function f()"
