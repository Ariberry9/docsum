"""
Utility functions for checking whether a file path is safe to access locally.
"""

import os


def is_path_safe(path):
    """
    Return True only if a path is relative and does not contain directory traversal.

    >>> is_path_safe("README.md")
    True
    >>> is_path_safe("tools/ls.py")
    True
    >>> is_path_safe("/etc/passwd")
    False
    >>> is_path_safe("../secret.txt")
    False
    >>> is_path_safe("tools/../chat.py")
    False
    """
    if os.path.isabs(path):
        return False

    parts = path.split("/")
    if ".." in parts:
        return False

    return True