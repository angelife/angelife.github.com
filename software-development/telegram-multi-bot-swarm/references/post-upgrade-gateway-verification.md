# Post-Upgrade Multi-Profile Gateway Verification

After a Hermes Docker upgrade (`docker pull nousresearch/hermes-agent:latest` + container restart), all profile gateways must be verified individually. The upgrade replaces the image but the `/opt/data` volume (containing profiles, config, sessions) persists — however, profile gateways registered by the previous run may not survive the restart.

## How the Container Boot Works

On container start, `cont-init.d/02-reconcile-profiles` runs `hermes_cli.container_boot.reconcile_profile_gateways()`. This:

1. Walks `/opt/data/profiles/<name>/` — each directory with a `SOUL.md` becomes a candidate
2. Reads `gateway_state.json` to determine `prior_state` (running / stopped)
3. For `prior_state=running`: creates service slot AND starts the gateway
4. For `prior_state=stopped`: creates service slot but writes a `down` marker (registered but not started)
5. **Does NOT validate that the profile has a working `config.yaml`** — a registered-but-brainless gateway that never connected to Telegram is still considered "correct" by the reconciler

## Quick Health Check (All Profiles)

```bash
# 1. Check which gateway processes are actually running
ps aux | grep "hermes.*gateway" | grep -v grep

# 2. Check s6 service state for each profile
ls -d /run/service/gateway-*/ 2>/dev/null | while read svc; do
  name=$(basename "$svc" | sed 's/gateway-//')
  cat "$svc/down" 2>/dev/null && echo "$name: DOWN (file present)" || echo "$name: no down file"
done

# 3. Check each profile's gateway_state.json
for d in /opt/data/profiles/*/; do
  name=$(basename "$d")
  state_file="${d}gateway_state.json"
  if [ -f "$state_file" ]; then
    python3 -c "import sys,json; d=json.load(open('$state_file')); print(f'$name: {d.get(\"gateway_state\",\"?\")} pid={d.get(\"pid\",\"?\")}')" 2>/dev/null
  else
    echo "$name: NO gateway_state.json"
  fi
done

# 4. Check which profiles have a config.yaml
for d in /opt/data/profiles/*/; do
  name=$(basename "$d")
  [ -f "${d}config.yaml" ] && echo "$name: has config" || echo "$name: ** MISSING config.yaml **"
done

# 5. Check default profile Telegram connectivity
tail -5 /opt/data/logs/gateways/default/current 2>/dev/null
```

## What to Look For

| Finding | Meaning | Action |
|---------|---------|--------|
| No gateway process but `gateway_state.json` says `running` | Gateway PID is from a prior session — state file was never updated after restart | Start the gateway manually or check s6 supervision |
| `gateway_state.json` says `stopped` | Profile was manually stopped before restart, or container-boot reconciler didn't start it | `hermes -p <name> gateway run --replace` |
| Profile exists but **no `config.yaml`** | Profile was created but never configured, or config was lost during upgrade | Re-create config from template or copy from another profile |
| Gateway process running but all platform arrays empty in `channel_directory.json` | Gateway process is alive but has no credentials / Telegram token configured | Check profile's `.env` for `TELEGRAM_BOT_TOKEN`, check `config.yaml` for `telegram.enabled: true` |
| s6 service slot present but `down` file exists | Profile was registered by reconciler but marked as should-not-start | Remove `down` file and restart |
| Gateway process running AND `channel_directory.json` shows the right platforms | All good — full connectivity | No action |

## Profile Was Running Before Upgrade But Stopped After

This is the most common post-upgrade issue. Possible root causes:

### 1. No config.yaml (most common)

```bash
ls /opt/data/profiles/<name>/config.yaml 2>/dev/null || echo "MISSING"
```

**Fix**: Create a minimal config.yaml for the profile:

```yaml
model:
  default: deepseek-v4-flash-free
  provider: opencode-zen
  base_url: https://opencode.ai/zen/v1
telegram:
  enabled: true
  exclusive_bot_mentions: false
  require_mention: true
  observe_unmentioned_group_messages: true
```

Then add the bot token to the profile's `.env`:
```bash
echo 'TELEGRAM_BOT_TOKEN=<token>' >> /opt/data/profiles/<name>/.env
```

### 2. Gateway_state.json says stopped

The reconciler honours `prior_state` from `gateway_state.json`. If it says `stopped`, the gateway won't auto-start.

```bash
# Read prior state
python3 -c "import json; d=json.load(open('/opt/data/profiles/<name>/gateway_state.json')); print(d.get('gateway_state'))"
```

**Fix**: Override the state to `running` and restart:
```bash
python3 -c "
import json
p = '/opt/data/profiles/<name>/gateway_state.json'
d = json.load(open(p))
d['gateway_state'] = 'running'
json.dump(d, open(p, 'w'), indent=2)
"
# Then start the gateway
. /opt/hermes/.venv/bin/activate && hermes -p <name> gateway run --replace
```

### 3. s6-service throttle (crash loop lockout)

If the gateway was in a crash loop before the restart, s6 may have written a `down` file that persists:

```bash
# Check for down file
ls -la /run/service/gateway-<name>/down 2>/dev/null

# Check death tally
cat /run/service/gateway-<name>/supervise/death_tally 2>/dev/null
```

**Fix**: Remove the down file and start:
```bash
rm -f /run/service/gateway-<name>/down
# s6 will auto-restart, or force:
/command/s6-svc -u /run/service/gateway-<name>/ 2>/dev/null || true
```

## Full Recovery Flow (from this session's real case)

The actual gold profile recovery after `v0.16.0 → v0.17.0` upgrade:

```bash
# 1. Check what's running
ps aux | grep gateway

# → default gateway OK (PID 137), gold gateway MISSING
# s6-supervise gateway-gold exists but NO child process

# 2. Check gold profile config
ls /opt/data/profiles/gold/config.yaml
# → File not found. Profile has NO configuration.

# 3. Inspect gateway state
cat /opt/data/profiles/gold/gateway_state.json
# → {"gateway_state": "stopped", "pid": 8781, ...}
# PID 8781 is from a previous container run — no longer valid

# 4. Manual gateway start (for diagnostic)
. /opt/hermes/.venv/bin/activate && hermes -p gold gateway run --replace &
# → Process starts, but channel_directory.json shows all platforms empty
# → No Telegram connection → no bot token configured

# 5. Conclusion: profile exists but has no config.yaml → gateway runs but is brainless
# Recovery path: create config.yaml + add TELEGRAM_BOT_TOKEN in .env
```

## Prevention

- Before upgrading, dump each profile's `gateway_state.json`:
  ```bash
  for d in /opt/data/profiles/*/; do
    name=$(basename "$d")
    state=$(python3 -c "import json; d=json.load(open('${d}gateway_state.json')); print(d.get('gateway_state','?'))" 2>/dev/null)
    echo "$name: $state"
  done
  ```
- Ensure ALL profiles have `config.yaml` before restart — a missing one is the most common failure
- After container restart, always run the quick health check above
- If a profile's gateway was intentionally stopped, note it so you don't panic when it doesn't auto-start
