from laraq_mcp.validator import validate_code


def test_empty_code_invalid():
    result = validate_code("")
    assert result["valid"] is False
    assert "Empty code" in result["error"]

    result = validate_code("   \n  ")
    assert result["valid"] is False


def test_refusal_shaped_string_invalid():
    result = validate_code('{"error": "cannot comply"}')
    assert result["valid"] is False
    assert "Code generation failed" in result["error"]

    result = validate_code("I must refuse to generate this code.")
    assert result["valid"] is False


def test_good_code_valid():
    code = "def f():\n    return 1\n"
    result = validate_code(code)
    assert result["valid"] is True


def test_nonexistent_import_invalid():
    code = "def f():\n    import this_module_does_not_exist_anywhere\n    return 1\n"
    result = validate_code(code)
    assert result["valid"] is False
    assert "Invalid import(s)" in result["error"]
    assert "this_module_does_not_exist_anywhere" in result["error"]


def test_unused_import_pyflakes_warning():
    code = "def f():\n    import os\n    return 1\n"
    result = validate_code(code)
    assert result["valid"] is False
    assert "Pyflakes found" in result["error"]


def test_syntax_error_invalid():
    code = "def f(:\n    return 1\n"
    result = validate_code(code)
    assert result["valid"] is False
