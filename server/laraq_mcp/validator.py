"""Static validation for generated BigDFT code: pyflakes + import check.

No LLM involved. Code arrives here as plain text extracted from a subagent's
fenced ```python block, so unlike laraq's original validator this does not
need to unwrap JSON-string escaping — there is none to undo.
"""

import ast
import importlib.util
import sys
from io import StringIO
from typing import Any

try:
    from pyflakes.api import check as pyflakes_check
    from pyflakes.reporter import Reporter
    PYFLAKES_AVAILABLE = True
except ImportError:
    PYFLAKES_AVAILABLE = False


def validate_code(code: str) -> dict[str, Any]:
    """Validate Python code using pyflakes (or AST as a fallback).

    Args:
        code: Python source code to validate.

    Returns:
        {"valid": True} on success, or {"valid": False, "error": <message>}.
    """
    if not code or not code.strip():
        return {"valid": False, "error": "Empty code provided"}

    code_stripped = code.strip()
    if code_stripped.startswith('{"error"') or "refusal" in code_stripped.lower():
        return {"valid": False, "error": f"Code generation failed: {code_stripped[:100]}"}

    import_check = _check_imports(code)
    if not import_check["valid"]:
        return import_check

    if PYFLAKES_AVAILABLE:
        return _validate_with_pyflakes(code)
    return _validate_with_ast(code)


def _validate_with_pyflakes(code: str) -> dict[str, Any]:
    output = StringIO()
    reporter = Reporter(output, sys.stderr)

    warning_count = pyflakes_check(code, "<generated>", reporter=reporter)

    if warning_count == 0:
        return {"valid": True}

    errors = output.getvalue().strip()
    error_lines = errors.split("\n")
    if len(error_lines) > 5:
        error_summary = "\n".join(error_lines[:5]) + f"\n... and {len(error_lines) - 5} more errors"
    else:
        error_summary = "\n".join(error_lines)

    return {"valid": False, "error": f"Pyflakes found {warning_count} issue(s):\n{error_summary}"}


def _validate_with_ast(code: str) -> dict[str, Any]:
    try:
        ast.parse(code)
        return {"valid": True}
    except SyntaxError as e:
        return {"valid": False, "error": f"SyntaxError at line {e.lineno}: {e.msg}"}
    except Exception as e:
        return {"valid": False, "error": f"{type(e).__name__}: {str(e)}"}


def _check_imports(code: str) -> dict[str, Any]:
    """Check that every top-level import in `code` resolves in this environment.

    Notably this means BigDFT/PyBigDFT must actually be importable wherever
    the laraq-mcp server process runs for validation of real BigDFT code to
    pass.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError:
        # Let pyflakes/AST validation below report the syntax error.
        return {"valid": True}

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    invalid_imports = []
    for module_name in imports:
        try:
            spec = importlib.util.find_spec(module_name)
            if spec is None:
                invalid_imports.append(module_name)
        except (ModuleNotFoundError, ValueError, ImportError):
            invalid_imports.append(module_name)

    if invalid_imports:
        return {
            "valid": False,
            "error": f"Invalid import(s): {', '.join(invalid_imports)}. These modules are not installed or do not exist.",
        }

    return {"valid": True}
