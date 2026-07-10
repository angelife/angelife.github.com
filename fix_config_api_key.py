#!/usr/bin/env python3
"""Add api_key from .env into config.yaml for custom provider"""
import os, sys, re

ENV_PATH = "/root/.hermes/.env"
CFG_PATH = "/root/.hermes/config.yaml"

# 1. Read AGNES_API_KEY from .env
key = None
with open(ENV_PATH) as f:
    for line in f:
        if line.startswith("AGNES_API_KEY="):
            key = line.strip().split("=", 1)[1]
            break

if not key:
    print("ERROR: AGNES_API_KEY not found in .env")
    sys.exit(1)

print(f"Key found: {key[:12]}...{key[-4:]}")

# 2. Read config.yaml
with open(CFG_PATH) as f:
    content = f.read()

# 3. Check if api_key already exists in model section
if "api_key:" in content:
    # Check if it's in the model section or elsewhere
    lines = content.split("\n")
    in_model = False
    for i, line in enumerate(lines):
        if line.strip().startswith("model:"):
            in_model = True
            continue
        if in_model and not line.startswith(" ") and not line.startswith("\n"):
            in_model = False
        if in_model and "api_key:" in line:
            print("api_key already exists in model section, updating...")
            lines[i] = "  api_key: " + key
            content = "\n".join(lines)
            break
    else:
        # api_key not found in model section - add it
        print("Adding api_key to model section...")
        # Find the model section and add after base_url
        for i, line in enumerate(lines):
            if "base_url:" in line and in_model:
                lines.insert(i + 1, "  api_key: " + key)
                content = "\n".join(lines)
                break
            if line.strip().startswith("model:"):
                in_model = True
else:
    print("No api_key in config, adding...")
    lines = content.split("\n")
    in_model = False
    for i, line in enumerate(lines):
        if line.strip().startswith("model:"):
            in_model = True
            continue
        if in_model and "base_url:" in line:
            lines.insert(i + 1, "  api_key: " + key)
            content = "\n".join(lines)
            break

# 4. Write back
with open(CFG_PATH, "w") as f:
    f.write(content)

print("Config updated successfully")
# Show model section
with open(CFG_PATH) as f:
    lines = f.readlines()
in_model = False
for line in lines:
    if line.strip().startswith("model:"):
        in_model = True
    if in_model:
        print(f"  {line.rstrip()}")
        if in_model and not line.startswith(" ") and line.strip() != "model:":
            break
