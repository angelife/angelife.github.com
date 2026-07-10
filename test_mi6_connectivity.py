#!/usr/bin/env python3
"""Test proxy connectivity from Mi6 chroot to Telegram"""
import urllib.request, json, sys

# Test 1: proxy connectivity to Telegram
proxy = urllib.request.ProxyHandler({
    "https": "http://192.168.1.8:10808",
    "http": "http://192.168.1.8:10808"
})
opener = urllib.request.build_opener(proxy)

# Test getMe
try:
    r = opener.open("https://api.telegram.org/bot8743263149:AAFr9ibTKi3VQ1o6xn-mNFn7QC4EzWKGhcA/getMe", timeout=15)
    data = json.loads(r.read())
    print(f"TELEGRAM_TEST: HTTP {r.status}, bot={data['result']['username']}")
except urllib.request.HTTPError as e:
    print(f"TELEGRAM_TEST: HTTP {e.code} - {e.read().decode()[:100]}")
except Exception as e:
    print(f"TELEGRAM_TEST: FAILED - {e}")

# Test 2: model API via same proxy
try:
    req = urllib.request.Request(
        "https://apihub.agnes-ai.com/v1/chat/completions",
        data=json.dumps({
            "model": "agnes-2.0-flash",
            "messages": [{"role": "user", "content": "OK"}],
            "max_tokens": 5
        }).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer sk-PLACEHOLDER"
        }
    )
    r = opener.open(req, timeout=30)
    body = json.loads(r.read())
    print(f"MODEL_TEST: HTTP {r.status}, reply={body['choices'][0]['message']['content']}")
except urllib.request.HTTPError as e:
    print(f"MODEL_TEST: HTTP {e.code} - {e.read().decode()[:200]}")
except Exception as e:
    print(f"MODEL_TEST: FAILED - {e}")
