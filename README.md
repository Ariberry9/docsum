# docsum

A command-line AI assistant that lets you explore and understand any codebase using natural language — just `cd` into a project and start asking questions.

[![doctests](https://github.com/Ariberry9/docsum/actions/workflows/doctests.yml/badge.svg)](https://github.com/Ariberry9/docsum/actions/workflows/doctests.yml)
[![flake8](https://github.com/Ariberry9/docsum/actions/workflows/flake8.yml/badge.svg)](https://github.com/Ariberry9/docsum/actions/workflows/flake8.yml)
[![integration](https://github.com/Ariberry9/docsum/actions/workflows/integration.yml/badge.svg)](https://github.com/Ariberry9/docsum/actions/workflows/integration.yml)
[![PyPI](https://img.shields.io/pypi/v/cmc-csci005-ariberry9)](https://pypi.org/project/cmc-csci005-ariberry9/)
<!--
This coverage badge is definitely wrong.
You don't have enough test cases to have 90% coverage,
and you aren't even doing coverage checks in your actions.
![coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)
-->

<!--
You demo gif below does not show your project actually running and working :(
-->
![demo](img/demo.gif)

<!--
anyone using github knows how to install from pypi
-->

## Tools

The assistant can call the following tools automatically, or you can run them manually with `/command`:

| Command | Description |
|---|---|
| `/ls [folder]` | List files in the current or specified folder |
| `/cat <file>` | Print the contents of a file |
| `/grep <pattern> <path>` | Search for a regex across files |
| `/calculate <expression>` | Evaluate a math expression |

<!-- 

Minor problem: READMEs should generally start with examples first and then "reference documentation" later

Major problem: Your examples were just copy/pasted from the instructions.  You were supposed to create your own examples to use with your own program's output
-->
