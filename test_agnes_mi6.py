#!/usr/bin/env python3
"""Test Agnes API from Mi6, reading key from .env"""
import json, os, sys

# Read key from .env
key = None
with open("/root/.hermes/.env") as f:
    for line in f:
        if line.startswith("AGNES_API_KEY="):
            key = line.strip().split("=", 1)[1]
            break

if not key:
    print("NO_KEY_FOUND")
    sys.exit(1)

print(f"KEY_LEN={len(key)}")

import urllib.request

# Test WITHOUT proxy first
req = urllib.request.Request(
    "https://apihub.agnes-ai.com/v1/chat/completions",
    data=json.dumps({
        "model": "agnes-2.0-flash",
        "messages": [{"role": "user", "content": "OK"}],
        "max_tokens": 5
    }).encode(),
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}"
    }
)
try:
    resp = urllib.request.urlopen(req, timeout=30)
    body = json.loads(resp.read())
    print(f"DIRECT_TEST: HTTP {resp.status}: {body['choices'][0]['message']['content'][:50]}")
except urllib.request.HTTPError as e:
    print(f"DIRECT_TEST: HTTP {e.code}: {e.read().decode()[:200]}")
except Exception as e:
    print(f"DIRECT_TEST: FAILED - {e}")

# Test WITH proxy
proxy = urllib.request.ProxyHandler({
    "https": "http://192.168.1.8:10808",
    "http": "http://192.168.1.8:10808"
})
opener = urllib.request.build_opener(proxy)
try:
    resp = opener.open(req, timeout=30)
    body = json.loads(resp.read())
    print(f"PROXY_TEST: HTTP {resp.status}: {body['choices'][0]['message']['content'][:50]}")
except urllib.request.HTTPError as e:
    print(f"PROXY_TEST: HTTP {e.code}: {e.read().decode()[:200]}")
except Exception as e:
    print(f"PROXY_TEST: FAILED - {e}")
