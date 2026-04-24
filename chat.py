"""
Main program for a local chat agent with manual and automatic tool support.
"""

import json
import os
import re

from dotenv import load_dotenv
from groq import Groq

from tools.ls import ls
from tools.cat import cat
from tools.grep import grep
from tools.calculate import calculate
from tools.doctests import doctests
from tools.write_files import write_files, write_file
from tools.rm import rm

load_dotenv()


class Chat:
    """
    A chat client that stores conversation history and supports local tools.
    """

    def __init__(self):
        """
        Initialize the client, tools, and conversation history.
        """
        if not os.path.isdir(".git"):
            raise Exception("Must run inside a git repo")

        api_key = os.environ.get("GROQ_API_KEY")
        if api_key:
            self.client = Groq(api_key=api_key)
        else:
            self.client = None

        system_content = (
            "You are a helpful assistant for answering questions about "
            "the user's current project folder. Use tools when needed."
        )

        if os.path.exists("AGENTS.md"):
            agents_text = cat("AGENTS.md")
            system_content += (
                "\n\nThe following AGENTS.md file contains project-specific "
                "instructions. Follow these instructions:\n\n"
                + agents_text
            )

        self.messages = [
            {
                "role": "system",
                "content": system_content,
            },
        ]

        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "ls",
                    "description": (
                        "List files in the current folder or a relative "
                        "subfolder."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Relative folder path",
                            }
                        },
                        "required": [],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "cat",
                    "description": "Read the contents of a text file.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Relative file path",
                            }
                        },
                        "required": ["path"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "grep",
                    "description": (
                        "Search for a regular expression in files matching "
                        "a relative glob."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pattern": {
                                "type": "string",
                                "description": (
                                    "Regular expression to search for"
                                ),
                            },
                            "path": {
                                "type": "string",
                                "description": "Relative file path or glob",
                            },
                        },
                        "required": ["pattern", "path"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "calculate",
                    "description": "Evaluate a mathematical expression.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "Math expression to evaluate",
                            }
                        },
                        "required": ["expression"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "doctests",
                    "description": (
                        "Run doctests on a Python file with verbose output."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Relative path to Python file",
                            }
                        },
                        "required": ["path"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "write_file",
                    "description": (
                        "Write one file, add it to git, commit it, and run "
                        "doctests if it is a Python file."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Relative file path",
                            },
                            "contents": {
                                "type": "string",
                                "description": "New file contents",
                            },
                            "commit_message": {
                                "type": "string",
                                "description": "Git commit message",
                            },
                        },
                        "required": [
                            "path",
                            "contents",
                            "commit_message",
                        ],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "write_files",
                    "description": (
                        "Write multiple files, add them to git, commit them, "
                        "and run doctests for Python files."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "files": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "path": {"type": "string"},
                                        "contents": {"type": "string"},
                                    },
                                    "required": ["path", "contents"],
                                },
                            },
                            "commit_message": {
                                "type": "string",
                                "description": "Git commit message",
                            },
                        },
                        "required": ["files", "commit_message"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "rm",
                    "description": (
                        "Remove one or more files using a relative path or "
                        "glob, then commit the removal."
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Relative file path or glob",
                            },
                        },
                        "required": ["path"],
                    },
                },
            },
        ]

    def execute_tool(self, tool_name, arguments):
        """
        Execute a local tool from a tool name and parsed JSON arguments.
        """
        if tool_name == "ls":
            return ls(arguments.get("path"))

        if tool_name == "cat":
            return cat(arguments["path"])

        if tool_name == "grep":
            return grep(arguments["pattern"], arguments["path"])

        if tool_name == "calculate":
            return calculate(arguments["expression"])

        if tool_name == "doctests":
            return doctests(arguments["path"])

        if tool_name == "write_file":
            return write_file(
                arguments["path"],
                arguments["contents"],
                arguments["commit_message"],
            )

        if tool_name == "write_files":
            return write_files(
                arguments["files"],
                arguments["commit_message"],
            )

        if tool_name == "rm":
            return rm(arguments["path"])

        return "Error: unknown tool"

    def send_message(self, message):
        """
        Send a user message to the model and return the assistant response.
        """
        if self.client is None:
            return "Error: API key not set"

        self.messages.append({
            "role": "user",
            "content": message,
        })

        while True:
            chat_completion = self.client.chat.completions.create(
                messages=self.messages,
                model="llama-3.1-8b-instant",
                tools=self.tools,
                tool_choice="auto",
            )

            assistant_message = chat_completion.choices[0].message

            if (
                hasattr(assistant_message, "tool_calls")
                and assistant_message.tool_calls
            ):
                self.messages.append(assistant_message)

                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)
                    tool_result = self.execute_tool(tool_name, arguments)

                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_name,
                        "content": tool_result,
                    })

                continue

            content = assistant_message.content
            if isinstance(content, str):
                match = re.search(
                    r'function=(\w+)>\s*(\{.*?\})\s*</function>',
                    content.strip(),
                    re.DOTALL,
                )
                if match:
                    tool_name = match.group(1)
                    raw_arguments = match.group(2).strip()

                    try:
                        arguments = json.loads(raw_arguments)
                    except json.JSONDecodeError:
                        return "Error: invalid tool arguments"

                    tool_result = self.execute_tool(tool_name, arguments)

                    self.messages.append({
                        "role": "assistant",
                        "content": content,
                    })
                    self.messages.append({
                        "role": "tool",
                        "name": tool_name,
                        "content": tool_result,
                    })

                    continue

            self.messages.append({
                "role": "assistant",
                "content": content,
            })
            return content

    def run_command(self, command):
        """
        Run a manual slash command.
        """
        parts = command.strip().split(maxsplit=1)

        if not parts:
            return ""

        command_name = parts[0]
        argument = parts[1] if len(parts) > 1 else ""

        if command_name == "/ls":
            return ls(argument or None)

        if command_name == "/cat":
            return cat(argument)

        if command_name == "/grep":
            grep_parts = argument.split(maxsplit=1)
            if len(grep_parts) != 2:
                return "Error: usage /grep PATTERN PATH"
            return grep(grep_parts[0], grep_parts[1])

        if command_name == "/calculate":
            return calculate(argument)

        if command_name == "/doctests":
            return doctests(argument)

        return "Error: unknown command"


def main():
    """
    Run the command line chat loop.
    """
    try:
        chat = Chat()
    except Exception as error:
        print(f"Error: {error}")
        return

    while True:
        try:
            message = input("chat> ")
        except KeyboardInterrupt:
            print()
            break

        if message.startswith("/"):
            print(chat.run_command(message))
        else:
            print(chat.send_message(message))


if __name__ == "__main__":
    main()
    