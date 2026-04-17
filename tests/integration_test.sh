#!/bin/bash
set -e

# this is a good format for an integration test
# but it's not really testing anything interesting about your class
# because you are only using / commands and not actually testing the
# LLM's functionality

python3 - <<'EOF'
from chat import Chat

chat = Chat()

assert chat.run_command("/calculate 2+3") == "5"
assert "chat.py" in chat.run_command("/ls")
assert "def cat(path):" in chat.run_command("/grep def tools/cat.py")

print("integration tests passed")
EOF
