"""
Tool for reading the contents of a file safely.
"""

from tools.path_safety import is_path_safe


def cat(path):
    """
    Return the contents of a safe text file.

    >>> cat("../secret.txt")
    'Error: unsafe path'
    >>> cat("this_file_should_not_exist_123.txt").startswith("Error:")
    True
    >>> "def cat(path):" in cat("tools/cat.py")
    True
    """
    if not is_path_safe(path):
        return "Error: unsafe path"

    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(path, "r", encoding="utf-16") as f:
                return f.read()
        except Exception as e:
            return f"Error: {e}"
    except Exception as e:
        return f"Error: {e}"
