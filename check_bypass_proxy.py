#!/usr/bin/env python3
"""Read should_bypass_proxy function"""
import os

bp = "/root/.hermes/venv/lib/python3.11/site-packages/gateway/platforms/base.py"
with open(bp) as f:
    lines = f.readlines()

# Find should_bypass_proxy function
capture = False
for i, line in enumerate(lines):
    if "def should_bypass_proxy" in line:
        j = i
        while j < len(lines) and (lines[j].startswith(" ") or lines[j].startswith("\n") or lines[j].strip() == "" or "def " not in lines[j] or j == i):
            if j > i and lines[j].strip() and not lines[j].startswith(" ") and not lines[j].startswith("\n"):
                if "def " in lines[j]:
                    break
            print(f"{j+1}:{lines[j]}", end="")
            j += 1
            if j - i > 80:
                break
        break
