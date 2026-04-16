"""
Tool for evaluating simple mathematical expressions.
"""


def calculate(expression):
    """
    Evaluate a mathematical expression and return the result as a string.

    >>> calculate("2 + 3")
    '5'
    >>> calculate("10 / 2")
    '5.0'
    >>> calculate("2 ** 3")
    '8'
    >>> calculate("hello")
    'Error'
    """
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception:
        return "Error"
