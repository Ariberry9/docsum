# docsum

[![doctests](https://github.com/Ariberry9/docsum/actions/workflows/doctests.yml/badge.svg)](https://github.com/Ariberry9/docsum/actions/workflows/doctests.yml)
[![flake8](https://github.com/Ariberry9/docsum/actions/workflows/flake8.yml/badge.svg)](https://github.com/Ariberry9/docsum/actions/workflows/flake8.yml)
[![integration](https://github.com/Ariberry9/docsum/actions/workflows/integration.yml/badge.svg)](https://github.com/Ariberry9/docsum/actions/workflows/integration.yml)
[![PyPI](https://img.shields.io/pypi/v/cmc-csci005-ariberry9)](https://pypi.org/project/cmc-csci005-ariberry9/)
[![coverage](https://github.com/Ariberry9/docsum/actions/workflows/coverage.yml/badge.svg)](https://github.com/Ariberry9/docsum/actions/workflows/coverage.yml)

A command-line AI assistant that lets you explore and understand any codebase using natural language — just `cd` into a project and start asking questions.

![demo](img/demo.gif)
## Example Usage

Below is an example of the assistant running locally:

```bash
$ chat
chat> what files are in the tools folder?
It seems like the tools folder includes the following files: 

1. __init__.py 
2. calculate.py 
3. cat.py 
4. grep.py 
5. ls.py 
6. path_safety.py
chat> what does the calculate tool do?
It appears that the calculate tool can evaluate simple mathematical expressions. It supports basic arithmetic operations like addition, subtraction, multiplication, and division, as well as exponentiation. However, it does not support more complex mathematical operations or functions.
chat> show me the contents of tools/cat.py
The contents of tools.cat.py show a function called cat that can safely read the contents of a text file. It uses a function is_path_safe to check if the file path is safe before trying to open the file. If the path is not safe, it returns an error message. If the file cannot be opened due to encoding issues, it tries to decode it with a different encoding.
