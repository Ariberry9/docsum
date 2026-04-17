"""
Tool for reading the contents of a file safely.
"""

from tools.path_safety import is_path_safe


def cat(path):
    """
    Return the contents of a safe text file.

    >>> cat("../secret.txt")
    'Error: unsafe path'

    >>> missing = cat("this_file_should_not_exist_123.txt")
    >>> missing.startswith("Error:")
    True

    >>> output = cat("tools/cat.py")
    >>> output.startswith('""')
    True
    >>> "def cat(path):" in output
    True
    >>> "Return the contents of a safe text file." in output
    True

    >>> cat("img/demo.gif").startswith("Error:")
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
