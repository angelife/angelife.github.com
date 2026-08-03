#!/usr/bin/env python3
"""Read resolve_proxy_url function"""
import os

bp = "/root/.hermes/venv/lib/python3.11/site-packages/gateway/platforms/base.py"
with open(bp) as f:
    lines = f.readlines()

# Find resolve_proxy_url function
capture = False
captured = []
for i, line in enumerate(lines):
    if "def resolve_proxy_url" in line:
        capture = True
    if capture:
        captured.append(f"{i+1}:{line}")
        # Stop at next top-level def
        if len(captured) > 1 and line.strip() and not line.startswith(" ") and not line.startswith("\n") and not line.startswith("#"):
            if "def " in line:
                captured.pop()  # don't include the next function
                break

print("".join(captured[:80]))
