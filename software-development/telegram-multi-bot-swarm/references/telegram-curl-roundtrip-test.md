# Telegram Bot Round-Trip Test via curl

Quick way to verify a Telegram bot's **bidirectional** connectivity without Python scripts or gateway inspection. Tests both outbound (CLI → Telegram) and inbound (Telegram → CLI via polling) in one sequence.

## Why This Exists

The `sendMessage` API call alone is insufficient — it proves the token works and the API is reachable, but tells you nothing about whether the gateway polling path is alive. A bot can have a valid token with no gateway attached (or a dead gateway). This test catches that gap by verifying both directions.

## Prerequisites

- Bot token accessible via `source /opt/data/.env` (or directly as `TELEGRAM_BOT_TOKEN`)
- User chat ID (typically `TELEGRAM_ALLOWED_USERS` or `TELEGRAM_HOME_CHANNEL` from `.env`)

## One-Liner Outbound Test

```bash
source /opt/data/.env && curl -s -X POST \
  "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d "chat_id=${TELEGRAM_ALLOWED_USERS:-780486548}" \
  -d "text=Test from Hermes at $(date)"
```

Expected: `{"ok":true,"result":{...}}` with a `message_id`.

## Full Round-Trip Test

This sends a message to the user, then polls for their reply with offset tracking:

```bash
source /opt/data/.env

# Step 1: Send test message
echo "=== Outbound ==="
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d "chat_id=780486548" \
  -d "text=🔄 Round-trip test: reply to this message"

# Step 2: Get current latest update_id as starting offset
LAST_OFFSET=$(curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getUpdates" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); rs=d.get('result',[]); print(rs[-1]['update_id'] if rs else '0')")

# Step 3: Poll for the reply (5 retries, 3s apart)
echo "=== Awaiting reply... ==="
OFFSET=$LAST_OFFSET
for i in 1 2 3 4 5; do
  sleep 3
  RESULT=$(curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getUpdates" \
    --data-urlencode "offset=$((OFFSET+1))" \
    --data-urlencode "timeout=5")
  NEW_MSGS=$(echo "$RESULT" | python3 -c "
import sys,json
data=json.load(sys.stdin)
msgs=[u['message'] for u in data.get('result',[]) if u.get('message')]
for m in msgs:
    print(f\"[@\\u200b{m['from']['username']}] {m.get('text','(non-text)')}\")
print(f'count={len(msgs)}')
")
  echo "$NEW_MSGS" | grep -v '^count='
  COUNT=$(echo "$NEW_MSGS" | grep '^count=' | cut -d= -f2)
  [ "$COUNT" -gt 0 ] && echo "=== Reply received! ✅ ===" && break
  OFFSET=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); rs=d.get('result',[]); print(rs[-1]['update_id'] if rs else '$OFFSET')")
done
```

### How Offset Management Works

Telegram's `getUpdates` uses an **offset** parameter to acknowledge and skip already-seen updates:
1. Read current `update_id` from the last update you've seen
2. Call `getUpdates?offset=last_id+1` — Telegram returns only NEWER updates and marks everything up to `last_id` as confirmed
3. After each poll, update the offset with the newest `update_id` received

This prevents:
- Re-processing old messages
- Infinite loops on the same update
- The need for manual `update_id` tracking across sessions

The `timeout` parameter enables **long polling** — the API holds the connection open for N seconds waiting for new data, rather than returning immediately empty.

## Integration with Gateway Troubleshooting

When diagnosing "bot not responding", use this pattern to isolate the fault:

| Test | If it fails | Root cause |
|------|-------------|------------|
| `sendMessage` (outbound) | Token invalid, API unreachable | Wrong/corrupted token, network issue |
| `getUpdates` returns your test reply | Inbound polling works independently | Issue is in gateway processing, not Telegram connectivity |
| `getUpdates` returns empty (you replied) | Gateway not polling, or wrong token | `TELEGRAM_BOT_TOKEN` mismatch, polling process dead |

If both `sendMessage` and `getUpdates` work via curl but the gateway doesn't respond:
- Gateway is running but provider API calls are failing (check gateway logs for auth errors)
- Gateway is dead but s6-supervise shows (check `ps aux | grep "hermes gateway run"`)
- `exclusive_bot_mentions: true` is blocking messages

## Cleanup: Acknowledge Consumed Updates

After testing, mark all seen updates as consumed so they don't re-appear:

```bash
source /opt/data/.env
LAST=$(curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getUpdates" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); rs=d.get('result',[]); print(rs[-1]['update_id'] if rs else '')")
[ -n "$LAST" ] && curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getUpdates?offset=$((LAST+1))" > /dev/null
```

## Common Errors

| Error | Meaning | Fix |
|-------|---------|-----|
| `{"ok":false,"error_code":404,"description":"Not Found"}` | Wrong URL pattern | Check `bot${TOKEN}` — missing `bot` prefix or bad token |
| `{"ok":false,"error_code":400,"description":"Bad Request: chat not found"}` | Wrong chat_id | Verify `TELEGRAM_ALLOWED_USERS` value |
| `curl: (6) Could not resolve host` | No internet in Docker | Check container DNS / network |
| Empty `getUpdates` after you replied | Offset too high, or different bot token being polled | Reset offset to 0 to test: `?offset=0` |
