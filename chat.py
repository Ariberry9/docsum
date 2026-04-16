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

load_dotenv()


class Chat:
    """
    A chat client that stores conversation history and supports local tools.

    >>> chat = Chat()
    >>> isinstance(chat.messages, list)
    True
    >>> chat.run_command("/calculate 2+2")
    '4'
    >>> chat.run_command("/ls ..")
    'Error: unsafe path'
    """

    def __init__(self):
        """
        Initialize the client, tools, and conversation history.
        """
        api_key = os.environ.get("GROQ_API_KEY")
        if api_key:
            self.client = Groq(api_key=api_key)
        else:
            self.client = None

        self.messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant for answering questions about "
                    "the user's current project folder. Use tools when needed."
                ),
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
        ]

    def execute_tool(self, tool_name, arguments):
        """
        Execute a local tool from a tool name and parsed JSON arguments.

        >>> chat = Chat()
        >>> chat.execute_tool("calculate", {"expression": "3*3"})
        '9'
        >>> chat.execute_tool("ls", {"path": ".."})
        'Error: unsafe path'
        >>> chat.execute_tool("unknown", {})
        'Error: unknown tool'
        """
        if tool_name == "ls":
            return ls(arguments.get("path"))

        if tool_name == "cat":
            return cat(arguments["path"])

        if tool_name == "grep":
            return grep(arguments["pattern"], arguments["path"])

        if tool_name == "calculate":
            return calculate(arguments["expression"])

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
                match = re.fullmatch(
                    r'function=(\w+)>(\{.*\})</function>',
                    content.strip(),
                )
                if match:
                    tool_name = match.group(1)
                    arguments = json.loads(match.group(2))
                    tool_result = self.execute_tool(tool_name, arguments)

                    self.messages.append({
                        "role": "assistant",
                        "content": content,
                    })
                    self.messages.append({
                        "role": "user",
                        "content": f"Tool result:\n{tool_result}",
                    })
                    continue

            result = assistant_message.content
            if result is None:
                result = "Error: model returned no final text response."

            self.messages.append({
                "role": "assistant",
                "content": result,
            })
            return result

    def run_command(self, line):
        """
        Run a local slash command and return its output.

        >>> chat = Chat()
        >>> chat.run_command("/calculate 2+2")
        '4'
        >>> chat.run_command("/ls ..")
        'Error: unsafe path'
        >>> "def cat(path):" in chat.run_command("/grep def tools/cat.py")
        True
        >>> chat.run_command("/unknown")
        'Error: unknown command /unknown'
        """
        parts = line.strip().split(maxsplit=2)
        command = parts[0][1:]

        if command == "ls":
            if len(parts) == 1:
                return ls()
            return ls(parts[1])

        if command == "cat":
            if len(parts) < 2:
                return "Error: cat requires 1 argument"
            return cat(parts[1])

        if command == "grep":
            if len(parts) < 3:
                return "Error: grep requires 2 arguments"
            return grep(parts[1], parts[2])

        if command == "calculate":
            if len(parts) < 2:
                return "Error: calculate requires 1 argument"
            return calculate(parts[1])

        return f"Error: unknown command /{command}"


if __name__ == "__main__":
    chat = Chat()
    try:
        while True:
            user_input = input("chat> ")

            if user_input.startswith("/"):
                response = chat.run_command(user_input)
                print(response)
                chat.messages.append({
                    "role": "user",
                    "content": user_input,
                })
                chat.messages.append({
                    "role": "assistant",
                    "content": response,
                })
            else:
                response = chat.send_message(user_input)
                print(response)
    except KeyboardInterrupt:
        print()
