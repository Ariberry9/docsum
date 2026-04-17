#!/bin/bash
set -e

python3 - <<'EOF'
from chat import Chat

chat = Chat()

# Test tool command (basic functionality)
assert "def cat(path):" in chat.run_command("/grep def tools/cat.py")

# Simulate LLM-style question but route through tools manually
response = chat.run_command("/ls tools")
assert "cat.py" in response

# Simulate reasoning about project (lightweight "LLM-like" behavior)
response2 = chat.run_command("/cat README.md")
assert "AI assistant" in response2 or "docsum" in response2

print("integration tests passed")
EOF