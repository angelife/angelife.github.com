#!/usr/bin/env python3
"""Check Mi6 gateway log for auth errors"""
with open("/root/.hermes/logs/gateway.log") as f:
    lines = f.readlines()
count_401 = sum(1 for l in lines if "401" in l)
print(f"Total 401s: {count_401}")
relevant = [(i+1, l.rstrip()) for i, l in enumerate(lines) 
            if any(x in l for x in ["response ready", "api_calls", "API call", "auth", "Auth"]) 
            and "check_fn" not in l and "registry" not in l]
for num, line in relevant[-10:]:
    print(f"  {num}: {line}")
