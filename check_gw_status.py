#!/usr/bin/env python3
"""Check gateway status"""
with open("/root/.hermes/logs/gateway.log") as f:
    c = f.read()

if "Connected to Telegram (polling mode)" in c:
    print("TELEGRAM: CONNECTED")
else:
    print("TELEGRAM: NOT CONNECTED")

if "401" in c:
    # Check if 401 is in an error context
    if "HTTP 401" in c or "InvalidToken" in c or "Unauthorized" in c:
        print("WARNING: Has 401 errors")
    else:
        print("401 strings found but not in error context")

# Check for SOUL.md loading
if "SOUL" in c or "soul" in c:
    for line in c.split("\n"):
        if "SOUL" in line or "soul" in line:
            print(f"SOUL_REF: {line.strip()}")

lines = c.strip().split("\n")
print(f"\nLast lines ({len(lines)} total):")
for l in lines[-5:]:
    print(f"  {l}")
