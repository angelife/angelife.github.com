#!/usr/bin/env python3
"""Test Agnes API key from Mi8 chroot"""
import urllib.request, json, os, sys

key = os.environ.get("AGNES_API_KEY")
if not key:
    # read from .env
    with open("/root/.hermes/.env") as f:
        for line in f:
            if line.startswith("AGNES_API_KEY="):
                key = line.strip().split("=", 1)[1]
                break

if not key:
    print("NO_KEY_FOUND")
    sys.exit(1)

print(f"KEY_FOUND: {key[:12]}...{key[-4:]}")

req = urllib.request.Request(
    "https://apihub.agnes-ai.com/v1/chat/completions",
    data=json.dumps({
        "model": "agnes-2.0-flash",
        "messages": [{"role": "user", "content": "回复这个字就好：OK"}],
        "max_tokens": 10
    }).encode(),
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"
    }
)

# Use proxy
proxy_handler = urllib.request.ProxyHandler({
    "http": "http://192.168.1.8:10808",
    "https": "http://192.168.1.8:10808"
})
opener = urllib.request.build_opener(proxy_handler)

try:
    resp = opener.open(req, timeout=30)
    body = resp.read().decode()
    print(f"HTTP {resp.status}")
    print(body[:500])
except urllib.request.HTTPError as e:
    print(f"HTTP_ERROR {e.code}: {e.read().decode()[:300]}")
except Exception as e:
    print(f"ERROR: {e}")
