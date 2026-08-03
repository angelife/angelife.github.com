#!/usr/bin/env python3
"""Find how Hermes reads custom provider key"""
import os, glob

root = "/root/.hermes"
for base_dir in [
    os.path.join(root, "venv/lib/python3.11/site-packages"),
    os.path.join(root, "hermes-agent/venv/lib/python3.11/site-packages"),
]:
    if not os.path.isdir(base_dir):
        continue
    for f in glob.glob(f"{base_dir}/**/*.py", recursive=True):
        fn = os.path.basename(f)
        if any(x in fn.lower() for x in ["provider", "llm", "model", "custom"]):
            # Check if it references AGNES or api_key or custom provider
            with open(f) as fh:
                content = fh.read()
                if "custom" in content.lower() or "AGNES_API_KEY" in content or "api_key" in content.lower():
                    print(f"--- {f} ---")
                    for i, line in enumerate(content.split("\n")):
                        if any(x in line.lower() for x in ["api_key", "agnes", "custom", "provider", "base_url", "auth"]):
                            print(f"  {i+1}: {line[:150]}")
                    print()
