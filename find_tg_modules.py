#!/usr/bin/env python3
"""Find telegram network modules in Hermes"""
import os, glob

for root, dirs, files in os.walk("/root/.hermes"):
    for f in files:
        if "telegram_network" in f or "telegram_platform" in f:
            fp = os.path.join(root, f)
            print(fp)
