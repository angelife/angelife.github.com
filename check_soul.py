#!/usr/bin/env python3
"""Check for existing soul/identity files on Mi8 and Mi6"""
import os

devices = {
    "Mi8": "/root/.hermes",
    "Mi6": "/root/.hermes",
}

for name, home in devices.items():
    print(f"\n=== {name} ({home}) ===")
    for target in [home, "/root"]:
        if os.path.isdir(target):
            for f in os.listdir(target):
                if any(x in f.lower() for x in ["soul", "identity", "persona", "角色", "自我", "profile", "readme"]):
                    fp = os.path.join(target, f)
                    print(f"  {fp} ({os.path.getsize(fp)} bytes)")
