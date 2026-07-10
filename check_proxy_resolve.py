#!/usr/bin/env python3
"""Trace how Hermes resolves proxy URL for Telegram"""
import os, sys

# Find and read the base module
for p in ["/root/.hermes/venv/lib/python3.11/site-packages", 
          "/root/.hermes/hermes-agent/venv/lib/python3.11/site-packages"]:
    bp = os.path.join(p, "gateway/platforms/base.py")
    if os.path.exists(bp):
        print(f"Found: {bp}")
        # Read just the resolve_proxy_url function
        with open(bp) as f:
            lines = f.readlines()
        in_func = False
        brace_depth = 0
        for i, line in enumerate(lines):
            if "def resolve_proxy_url" in line:
                in_func = True
            if in_func:
                print(f"  {i+1}: {line}", end="")
                brace_depth += line.count("{") - line.count("}")
                if brace_depth <= 0 and line.strip() and "def " not in line:
                    # Check if next line starts a new function
                    if i+1 < len(lines) and lines[i+1].strip() and not lines[i+1].startswith(" ") and not lines[i+1].startswith("\n"):
                        break
        break
