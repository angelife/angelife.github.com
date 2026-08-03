#!/usr/bin/env python3
"""Find Hermes packages and provider code"""
import os, glob

base = "/root/.hermes/hermes-agent/venv/lib/python3.11/site-packages"

# List hermes/hermes_agent related packages
print("=== Hermes packages ===")
for d in sorted(os.listdir(base)):
    if "hermes" in d.lower() and os.path.isdir(os.path.join(base, d)):
        print(f"  {d}/")
        for f in sorted(os.listdir(os.path.join(base, d))):
            if f.endswith(".py"):
                print(f"    {f}")

# Find the config/model provider module
print("\n=== Searching for provider config ===")
for root, dirs, files in os.walk(base):
    for f in files:
        if not f.endswith(".py"):
            continue
        fp = os.path.join(root, f)
        # Skip large irrelevant directories
        if any(x in root for x in ["openai/", "starlette/", "fastapi/", "pydantic/", "fire/", "requests/", "pip/", "certifi/"]):
            continue
        if "hermes" not in root and "agent" not in root:
            continue
        with open(fp, errors="ignore") as fh:
            try:
                content = fh.read()
            except:
                continue
            if "provider" in content and "custom" in content and "api_key" in content:
                rel = os.path.relpath(fp, base)
                lines = content.split("\n")
                hits = [(i+1, line) for i, line in enumerate(lines) 
                        if any(x in line.lower() for x in ["api_key", "provider", "custom", "base_url"])]
                if hits:
                    print(f"\n--- {rel} ---")
                    for num, line in hits[:10]:
                        print(f"  {num}: {line[:200]}")
