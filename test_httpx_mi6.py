#!/usr/bin/env python3
"""Test httpx connectivity from Mi6 chroot similar to how Hermes would"""
try:
    import httpx
except ImportError:
    print("httpx not installed directly, checking if available via Hermes venv")
    import sys
    sys.path.insert(0, "/root/.hermes/hermes-agent/venv/lib/python3.11/site-packages")
    try:
        import httpx
        print("httpx found in hermes venv")
    except ImportError:
        sys.path.insert(0, "/root/.hermes/venv/lib/python3.11/site-packages")
        try:
            import httpx
            print("httpx found in hermes venv (alt)")
        except ImportError:
            print("httpx NOT FOUND")
            import subprocess
            r = subprocess.run(["find", "/root/.hermes", "-name", "httpx", "-type", "d"], capture_output=True, text=True)
            print(r.stdout[:200])
            r = subprocess.run(["find", "/root/.hermes", "-path", "*/site-packages/httpx*", "-maxdepth", "5"], capture_output=True, text=True)
            print(r.stdout[:500])
            import sys
            sys.exit(1)

import json, os

# Read keys from .env
env = {}
with open("/root/.hermes/.env") as f:
    for line in f:
        if "=" in line:
            k, v = line.strip().split("=", 1)
            env[k] = v

TELEGRAM_TOKEN = env.get("TELEGRAM_BOT_TOKEN", "")
AGNES_KEY = env.get("AGNES_API_KEY", "")
PROXY = "http://192.168.1.8:10808"

# Test 1: httpx with proxy to Telegram
print(f"httpx version: {httpx.__version__}")
print(f"Testing Telegram via httpx proxy...")

try:
    with httpx.Client(proxy=PROXY, timeout=15) as client:
        r = client.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getMe")
        print(f"TELEGRAM: HTTP {r.status_code}, elapsed={r.elapsed}")
        data = r.json()
        if data.get("ok"):
            print(f"  bot={data['result']['username']}")
        else:
            print(f"  error={data.get('description')}")
except Exception as e:
    print(f"TELEGRAM FAILED (httpx): {type(e).__name__}: {e}")

# Test 2: httpx with proxy to Agnes model API
print(f"Testing Agnes model via httpx proxy...")
try:
    with httpx.Client(proxy=PROXY, timeout=30) as client:
        r = client.post(
            "https://apihub.agnes-ai.com/v1/chat/completions",
            json={"model": "agnes-2.0-flash", "messages": [{"role": "user", "content": "OK"}], "max_tokens": 5},
            headers={"Authorization": f"Bearer {AGNES_KEY}"}
        )
        print(f"MODEL: HTTP {r.status_code}, elapsed={r.elapsed}")
        if r.status_code == 200:
            print(f"  reply={r.json()['choices'][0]['message']['content']}")
        else:
            print(f"  error={r.text[:200]}")
except Exception as e:
    print(f"MODEL FAILED (httpx): {type(e).__name__}: {e}")
