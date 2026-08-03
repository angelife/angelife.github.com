#!/usr/bin/env python3
"""Test model API from config.yaml api_key"""
import json, urllib.request, yaml

# Read api_key from config.yaml
with open("/root/.hermes/config.yaml") as f:
    cfg = yaml.safe_load(f)
key = cfg["model"]["api_key"]
url = cfg["model"]["base_url"] + "/chat/completions"
print(f"Key: {key[:12]}...{key[-4:]}")
print(f"URL: {url}")

req = urllib.request.Request(
    url,
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
proxy = urllib.request.ProxyHandler({
    "https": "http://192.168.1.8:10808"
})
opener = urllib.request.build_opener(proxy)
try:
    resp = opener.open(req, timeout=30)
    body = json.loads(resp.read())
    print(f"HTTP {resp.status}: {body['choices'][0]['message']['content']}")
except urllib.request.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()[:200]}")
except Exception as e:
    print(f"FAILED: {e}")
