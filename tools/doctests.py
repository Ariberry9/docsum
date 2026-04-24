import subprocess
from tools.path_safety import is_path_safe

def doctests(path: str) -> str:
    if not is_path_safe(path):
        return "Error: unsafe path"

    result = subprocess.run(
        ["python3", "-m", "doctest", "-v", path],
        capture_output=True,
        text=True,
    )

    return result.stdout + result.stderr