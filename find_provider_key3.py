#!/usr/bin/env python3
"""Find how Hermes resolves api_key for custom provider"""
import os

base = "/root/.hermes/hermes-agent/venv/lib/python3.11/site-packages"
# Focus on the agent package
agent_dir = os.path.join(base, "hermes_agent")  # might also be just "agent"
if not os.path.isdir(agent_dir):
    # Try other names
    for d in os.listdir(base):
        if "agent" in d.lower() and os.path.isdir(os.path.join(base, d)):
            agent_dir = os.path.join(base, d)
            break

print(f"Agent dir: {agent_dir}")

# Find relevant files
for root, dirs, files in os.walk(agent_dir):
    for f in files:
        if not f.endswith(".py"):
            continue
        fp = os.path.join(root, f)
        with open(fp) as fh:
            content = fh.read()
            # Look for "provider" or "api_key" or "custom"
            if any(x in content.lower() for x in ["provider ==", "api_key", "custom", "base_url"]):
                lines = content.split("\n")
                hits = [(i+1, line) for i, line in enumerate(lines) 
                        if any(x in line.lower() for x in ["api_key", "provider", "custom", "base_url"])]
                if hits:
                    rel = os.path.relpath(fp, agent_dir)
                    print(f"\n--- {rel} ({len(hits)} hits) ---")
                    for num, line in hits[:15]:
                        print(f"  {num}: {line[:200]}")
