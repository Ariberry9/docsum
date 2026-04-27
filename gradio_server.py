#!/usr/bin/env python
'''
A bare-bones web interface for conversations with LLMs served from openai-compatible endpoints.
'''
import os
import argparse
import gradio as gr
from openai import OpenAI

parser = argparse.ArgumentParser()
parser.add_argument("--url")
parser.add_argument("--apikey")
parser.add_argument("--model", default='llama-3.3-70b-versatile')
parser.add_argument("--port", type=int, default=7860)
args = parser.parse_args()

api_key = args.apikey or os.getenv("GROQ_API_KEY")

client = OpenAI(
    base_url=args.url or "https://api.groq.com/openai/v1", 
    api_key=api_key
)

def chat(message, history):
    import json
    from chat import Chat
    bot = Chat() 

    messages = []
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model=args.model,
        messages=messages,
        tools=bot.tools,
        tool_choice="auto"
    )

    response_message = response.choices[0].message

    if response_message.tool_calls:
        messages.append(response_message)

        for tool_call in response_message.tool_calls:
            # 1. Get the name
            name = tool_call.function.name
            # 2. Parse the arguments string into a dict
            args_dict = json.loads(tool_call.function.arguments)
            
            # 3. Call your partner's function correctly
            result = bot.execute_tool(name, args_dict)
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": name,
                "content": str(result)
            })

        final_response = client.chat.completions.create(
            model=args.model,
            messages=messages
        )
        return final_response.choices[0].message.content

    return response_message.content
gr.ChatInterface(chat).launch(server_port=args.port)