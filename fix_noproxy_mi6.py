#!/usr/bin/env python3
"""Remove Telegram-related NO_PROXY entries from .env"""
ENV_PATH = "/root/.hermes/.env"

with open(ENV_PATH) as f:
    lines = f.readlines()

filtered = []
removed = []
for line in lines:
    stripped = line.strip()
    # Remove NO_PROXY/no_proxy entries that include api.telegram.org
    if stripped.lower().startswith("no_proxy=") and "api.telegram.org" in stripped:
        removed.append(stripped)
        continue
    filtered.append(line)

with open(ENV_PATH, "w") as f:
    f.writelines(filtered)

print(f"Removed {len(removed)} line(s):")
for r in removed:
    print(f"  {r}")

# Verify remaining NO_PROXY entries
with open(ENV_PATH) as f:
    for line in f:
        if line.strip().lower().startswith("no_proxy="):
            print(f"  Remaining: {line.strip()}")
