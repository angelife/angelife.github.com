#!/usr/bin/env python3
"""Find the telegram adapter code that creates HTTPXRequest"""
import os, glob

base = "/root/.hermes/venv/lib/python3.11/site-packages"
targets = [
    os.path.join(base, "hermes_plugins/telegram_platform"),
    os.path.join(base, "plugins/platforms/telegram"),
]
for d in targets:
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            if f.endswith(".py") and not f.startswith("__"):
                fp = os.path.join(d, f)
                print(f"--- {fp} ---")
                with open(fp) as fh:
                    for i, line in enumerate(fh):
                        if "HTTPXRequest" in line or "transport" in line.lower() or "proxy" in line.lower():
                            print(f"  {i+1}: {line.rstrip()}")
