"""
Tools package for the chat agent.

This package provides local tools that the chat agent can use to interact
with files and perform computations, including:
- ls: list files in a directory
- cat: read file contents
- grep: search text using regular expressions
- calculate: evaluate mathematical expressions
- is_path_safe: validate file paths for security
"""

from .ls import ls
from .cat import cat
from .grep import grep
from .calculate import calculate
from .path_safety import is_path_safe

__all__ = [
    "ls",
    "cat",
    "grep",
    "calculate",
    "is_path_safe",
]