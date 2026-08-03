#!/usr/bin/env python3
"""Test TLS connectivity from Mi6 chroot"""
import ssl, socket, json, urllib.request, sys

# Test 1: Direct TLS connection to api.telegram.org through proxy
# First test with cert verification
ctx = ssl.create_default_context()
print(f"SSL_VERIFY_MODE: {ctx.verify_mode}")

# Test direct connection (no proxy) to verify TLS
test_hosts = [
    ("api.telegram.org", 443),
    ("apihub.agnes-ai.com", 443),
]

for host, port in test_hosts:
    # Test via proxy (HTTP CONNECT tunnel)
    try:
        proxy_sock = socket.create_connection(("192.168.1.8", 10808), timeout=10)
        proxy_sock.sendall(f"CONNECT {host}:{port} HTTP/1.1\r\nHost: {host}:{port}\r\n\r\n".encode())
        resp = proxy_sock.recv(4096, socket.MSG_PEEK)
        if b"200" in resp:
            tls = ctx.wrap_socket(proxy_sock, server_hostname=host)
            cert = tls.getpeercert()
            print(f"TLS_OK {host}: issuer={cert['issuer'][0][0][1]}, notBefore={cert['notBefore']}, notAfter={cert['notAfter']}")
            tls.close()
        else:
            print(f"PROXY_REFUSED {host}: {resp[:100]}")
            proxy_sock.close()
    except Exception as e:
        print(f"TLS_FAIL {host}: {e}")

# Test 2: HTTP GET through proxy to check if cert issue
proxy_handler = urllib.request.ProxyHandler({
    "https": "http://192.168.1.8:10808"
})
opener = urllib.request.build_opener(proxy_handler)
try:
    r = opener.open("https://api.telegram.org/bot8743263149:AAFr9ibTKi3VQ1o6xn-mNFn7QC4EzWKGhcA/getMe", timeout=15)
    data = json.loads(r.read())
    print(f"HTTPS_OK: bot={data['result']['username']}")
except Exception as e:
    print(f"HTTPS_FAIL: {e}")
