"""Code execution: local in-process only.

Remote/HPC execution is handled by the separate `remotemanager` plugin, not
by laraq itself — see laraq-generating's "Running on a remote HPC cluster
instead" section.
"""

import traceback


def local_execute(code: str) -> object:
    """Execute code in-process by calling f().

    Returns the raw return value of f(), or an "ERROR: ..." string on failure.
    """
    try:
        namespace: dict = {}
        exec(code, namespace)
        if "f" not in namespace or not callable(namespace["f"]):
            return "ERROR: Code did not define a callable function f()"
        return namespace["f"]()
    except Exception as e:
        return f"ERROR: {type(e).__name__}: {e}\n\n{traceback.format_exc()}"
