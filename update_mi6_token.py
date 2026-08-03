#!/usr/bin/env python3
import sys

NEW_TOKEN = "8743263149:AAFr9ibTKi3VQ1o6xn-mNFn7QC4EzWKGhcA"

# Update .env
with open("/root/.hermes/.env") as f:
    lines = f.readlines()
with open("/root/.hermes/.env", "w") as f:
    for line in lines:
        if line.startswith("TELEGRAM_BOT_TOKEN="):
            f.write(f"TELEGRAM_BOT_TOKEN={NEW_TOKEN}\n")
        else:
            f.write(line)

# Update config.yaml
with open("/root/.hermes/config.yaml") as f:
    lines = f.readlines()
with open("/root/.hermes/config.yaml", "w") as f:
    for line in lines:
        if "bot_token:" in line and not line.strip().startswith("#"):
            f.write(f"  bot_token: {NEW_TOKEN}\n")
        else:
            f.write(line)

print("TOKEN_UPDATED")
# Verify
for p in ["/root/.hermes/.env", "/root/.hermes/config.yaml"]:
    with open(p) as f:
        for line in f:
            if "TELEGRAM_BOT" in line or "bot_token" in line:
                print(f"  {p}: {line.strip()}")
