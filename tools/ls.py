"""
Tool for listing files in a directory.
"""

import glob

from tools.path_safety import is_path_safe


def ls(folder=None):
    """
    Return a space-separated list of files in the current folder or a given folder.

    If no folder is provided, list the files in the current folder.
    If a folder is provided, list the files in that folder.
    Unsafe paths return an error message.

    >>> ls("..")
    'Error: unsafe path'

    >>> output = ls()
    >>> isinstance(output, str)
    True
    >>> "chat.py" in output
    True
    >>> "tools" in output
    True

    >>> output = ls("tools")
    >>> "tools/ls.py" in output
    True
    >>> "tools/cat.py" in output
    True
    """
    if folder is None:
        folder = "."

    if not is_path_safe(folder):
        return "Error: unsafe path"

    paths = sorted(glob.glob(folder + "/*"))
    return " ".join(paths)
