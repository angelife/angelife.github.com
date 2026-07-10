#!/usr/bin/env python3
"""Quick status of Mi6 gateway"""
with open("/root/.hermes/logs/gateway.log") as f:
    lines = f.readlines()
print(f"Total lines: {len(lines)}")
for l in lines:
    s = l.strip()
    if "Connected" in s and "Telegram" in s:
        print(f"CONN: {s}")
    if "telegram connected" in s:
        print(f"STAT: {s}")
    if "response ready" in s:
        print(f"RESP: {s}")
    if "401" in s and "Unauthorized" in s:
        print(f"ERR: {s}")
