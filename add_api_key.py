#!/usr/bin/env python3
"""Insert api_key into model section of config.yaml"""
import sys

ENV_PATH = "/root/.hermes/.env"
CFG_PATH = "/root/.hermes/config.yaml"

# Read key from .env
key = None
with open(ENV_PATH) as f:
    for line in f:
        if line.startswith("AGNES_API_KEY="):
            key = line.strip().split("=", 1)[1]
            break
if not key:
    print("FAIL: no AGNES_API_KEY in .env")
    sys.exit(1)

# Read config
with open(CFG_PATH) as f:
    lines = f.readlines()

# Find base_url line and insert api_key after it
found = False
for i, line in enumerate(lines):
    s = line.strip()
    if s == "model:":
        found = True
    if found and s.startswith("base_url:"):
        # Check if api_key already present in model block
        j = i + 1
        while j < len(lines) and lines[j].startswith("  "):
            if "api_key:" in lines[j]:
                print("api_key already present, skipping")
                sys.exit(0)
            j += 1
        # Insert api_key line
        indent = "  " if line.startswith("  ") else ""
        lines.insert(i + 1, f"{indent}api_key: {key}\n")
        break

with open(CFG_PATH, "w") as f:
    f.writelines(lines)

print("OK: api_key added")
# Show relevant section
for line in lines:
    if any(x in line for x in ["model:", "default:", "provider:", "base_url:", "api_key:", "max_tokens:"]):
        print(f"  {line.rstrip()}")
