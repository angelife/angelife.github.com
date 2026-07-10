#!/usr/bin/env python3
"""Test async httpx with proxy (same as gateway)"""
import asyncio, httpx, json, os

TELEGRAM_TOKEN = ""
AGNES_KEY = ""
with open("/root/.hermes/.env") as f:
    for line in f:
        if "=" in line:
            k, v = line.strip().split("=", 1)
            if k == "TELEGRAM_BOT_TOKEN":
                TELEGRAM_TOKEN = v
            elif k == "AGNES_API_KEY":
                AGNES_KEY = v

PROXY = "http://192.168.1.8:10808"

async def test_async():
    print(f"httpx version: {httpx.__version__}")
    
    # Test 1: AsyncHTTPTransport with proxy
    transport = httpx.AsyncHTTPTransport(proxy=PROXY)
    async with httpx.AsyncClient(transport=transport, timeout=30) as client:
        try:
            r = await client.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getMe")
            print(f"ASYNC_TRANSPORT_PROXY: HTTP {r.status_code}")
            if r.status_code == 200:
                print(f"  bot={r.json()['result']['username']}")
        except Exception as e:
            print(f"ASYNC_TRANSPORT_PROXY failed: {type(e).__name__}: {e}")
    
    # Test 2: AsyncClient with proxy kwarg
    try:
        async with httpx.AsyncClient(proxy=PROXY, timeout=30) as client:
            r = await client.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getMe")
            print(f"ASYNC_CLIENT_PROXY: HTTP {r.status_code}")
            if r.status_code == 200:
                print(f"  bot={r.json()['result']['username']}")
    except Exception as e:
        print(f"ASYNC_CLIENT_PROXY failed: {type(e).__name__}: {e}")
    
    # Test 3: No proxy (should fail - no internet from Mi6)
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getMe")
            print(f"NO_PROXY: HTTP {r.status_code}")
    except Exception as e:
        print(f"NO_PROXY expected failure: {type(e).__name__}: {e}")

    # Test 4: Agnes model via async proxy
    transport2 = httpx.AsyncHTTPTransport(proxy=PROXY)
    async with httpx.AsyncClient(transport=transport2, timeout=30) as client:
        try:
            r = await client.post(
                "https://apihub.agnes-ai.com/v1/chat/completions",
                json={"model": "agnes-2.0-flash", "messages": [{"role": "user", "content": "OK"}], "max_tokens": 5},
                headers={"Authorization": f"Bearer {AGNES_KEY}"}
            )
            print(f"MODEL_ASYNC: HTTP {r.status_code}")
            if r.status_code == 200:
                print(f"  reply={r.json()['choices'][0]['message']['content']}")
        except Exception as e:
            print(f"MODEL_ASYNC failed: {type(e).__name__}: {e}")

asyncio.run(test_async())
