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

    >>> "chat.py" in ls()
    True
    >>> "tools/ls.py" in ls("tools")
    True
    >>> ls("..")
    'Error: unsafe path'
    """
    if folder is None:
        folder = "."

    if not is_path_safe(folder):
        return "Error: unsafe path"

    paths = sorted(glob.glob(folder + "/*"))
    return " ".join(paths)
