#!/bin/bash
set -e

python3 - <<'EOF'
from chat import Chat

chat = Chat()

assert chat.run_command("/calculate 2+3") == "5"
assert "chat.py" in chat.run_command("/ls")
assert "def cat(path):" in chat.run_command("/grep def tools/cat.py")

print("integration tests passed")
EOF