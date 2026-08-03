#!/usr/bin/env python3
"""Trace proxy resolution in the actual gateway environment"""
import os, sys

# Simulate what the gateway does
os.environ.setdefault("HTTPS_PROXY", "")
os.environ.setdefault("HTTP_PROXY", "")
os.environ.setdefault("NO_PROXY", "")

print("=== ENV check ===")
for k in ["HTTPS_PROXY", "HTTP_PROXY", "NO_PROXY", "https_proxy", "http_proxy", "no_proxy", "TELEGRAM_PROXY"]:
    print(f"  {k}={os.environ.get(k, '<not set>')}")

# Now try resolve_proxy_url
sys.path.insert(0, "/root/.hermes/venv/lib/python3.11/site-packages")
from gateway.platforms.base import resolve_proxy_url, should_bypass_proxy

proxy_targets = ["api.telegram.org", "149.154.166.110", "149.154.167.220"]

print(f"\n=== should_bypass_proxy check ===")
print(f"  targets={proxy_targets}")
print(f"  bypass={should_bypass_proxy(proxy_targets)}")

print(f"\n=== resolve_proxy_url results ===")
url = resolve_proxy_url("TELEGRAM_PROXY", target_hosts=proxy_targets)
print(f"  with TELEGRAM_PROXY: {url}")

url2 = resolve_proxy_url(target_hosts=proxy_targets)
print(f"  without platform var: {url2}")
