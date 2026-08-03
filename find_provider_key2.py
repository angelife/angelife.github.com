#!/usr/bin/env python3
"""Find Hermes agent model provider / LLM code"""
import os, glob

base = "/root/.hermes/hermes-agent/venv/lib/python3.11/site-packages"
target_files = []
for root, dirs, files in os.walk(base):
    for f in files:
        if not f.endswith(".py"):
            continue
        fp = os.path.join(root, f)
        # Skip irrelevant packages
        if any(x in fp for x in ["openai/", "pydantic/", "fire/", "requests/", "pip/", "certifi/", "idna/", "charset"]):
            continue
        # Look in agent/ or hermes/ directories
        if "agent" in fp or "hermes" in fp or "provider" in fp or "llm" in fp:
            target_files.append(fp)

# Now check each file for "custom" provider + api_key pattern
for fp in target_files:
    with open(fp) as fh:
        content = fh.read()
        if "api_key" in content.lower() and ("provider" in content.lower() or "model" in content.lower()):
            # Only show relevant lines
            lines = content.split("\n")
            relevant = []
            for i, line in enumerate(lines):
                if any(x in line.lower() for x in ["api_key", "provider", "custom", "base_url", "auth"]):
                    relevant.append(f"{os.path.basename(fp)}:{i+1}: {line[:200]}")
            if relevant:
                print(f"--- {fp} ---")
                for r in relevant:
                    print(r)
                print()
