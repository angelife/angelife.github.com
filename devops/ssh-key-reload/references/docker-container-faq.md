# Docker Container FAQ

Common gotchas when debugging Docker containers (especially Hermes Agent containers).

## Date / Time Verification

Docker containers can have drifted or wrong system clocks. **Never trust a container's date without verification.**

```bash
# Check container time
date && date -u && TZ='Asia/Shanghai' date

# Verify against an external source
curl -s "https://timeapi.io/api/Time/current/zone?timeZone=UTC" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['dateTime'])"
```

**Pitfall**: Logs with wrong timestamps will mislead forensic analysis. Always cross-check with network time before drawing conclusions from log dates.

## Process Management

```bash
# Find all python processes
ps aux | grep python | grep -v grep

# Find lingering gateway/agent processes
ps aux | grep -E "hermes|gateway" | grep -v grep

# Kill a specific process
kill <PID>

# Check container uptime
cat /proc/uptime | awk '{printf "Uptime: %.0f hours\n", $1/3600}'
```

## Disk / Memory

```bash
# Container resource limits
cat /sys/fs/cgroup/memory/memory.limit_in_bytes 2>/dev/null
cat /sys/fs/cgroup/cpu/cpu.cfs_quota_us 2>/dev/null

# Current usage
free -h
df -h
```

## Network

```bash
# Check if internet is reachable (some containers have no network)
curl -s --max-time 5 https://google.com -o /dev/null -w "%{http_code}"
echo ""

# DNS resolution test
getent hosts google.com 2>/dev/null || nslookup google.com 2>/dev/null
```

## Hermes Agent Specific

- Config: `/opt/data/config.yaml`
- Env: `/opt/data/.env`
- Logs: `/opt/data/logs/gateway.log`
- Skills: `/opt/data/skills/`