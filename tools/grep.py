"""
Tool for searching for regular expressions inside safe text files.
"""

import glob
import re

from tools.path_safety import is_path_safe


def grep(pattern, path):
    """
    Return all matching lines from files that match the given glob.

    >>> grep("def cat", "../*.py")
    'Error: unsafe path'

    >>> grep("^def cat", "tools/cat.py")
    'def cat(path):'

    >>> output = grep("return", "tools/cat.py")
    >>> "return f.read()" in output
    True
    >>> 'return "Error: unsafe path"' in output
    True

    >>> grep("zzzxxyyqqq_not_found_987654321", "tools/cat.py")
    ''

    >>> grep("def ", "img/demo.gif")
    ''
    """
    if not is_path_safe(path):
        return "Error: unsafe path"

    matches = []

    for filename in sorted(glob.glob(path)):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                for line in f:
                    if re.search(pattern, line):
                        matches.append(line.rstrip("\n"))
        except UnicodeDecodeError:
            try:
                with open(filename, "r", encoding="utf-16") as f:
                    for line in f:
                        if re.search(pattern, line):
                            matches.append(line.rstrip("\n"))
            except Exception:
                pass
        except Exception:
            pass

    return "\n".join(matches)
