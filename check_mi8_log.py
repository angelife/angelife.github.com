#!/usr/bin/env python3
"""Check Mi8 gateway log for auth errors and model calls"""
with open("/root/.hermes/logs/gateway.log") as f:
    lines = f.readlines()

# Check total 401 count
count_401 = sum(1 for l in lines if "401" in l)
print(f"Total 401s: {count_401}")

# Show relevant recent lines
relevant = []
for i, line in enumerate(lines):
    if any(x in line for x in ["response ready", "api_calls", "API call", "Auth", "auth"]):
        if "check_fn" not in line and "registry" not in line:
            relevant.append(f"{i+1}:{line.rstrip()}")

print(f"\nRelevant entries ({len(relevant)}):")
for r in relevant[-20:]:
    print(r)
