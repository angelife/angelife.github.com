# Telegram Group Topic Visibility Debugging

Debugging whether Hermes can see and respond to messages in a Telegram topic (threads) group.

## Symptom

- Bot responds in DM but seems invisible in group
- User says "群里看不到你的回复消息"
- Messages sent from thread (topic) don't appear in main chat

## Root Cause Checklist

### 1. Privacy Mode (Telegram-side)

Bot must be added as **group admin** (no special permissions needed). Without this, Telegram's Privacy Mode drops @mentions silently.

**Fix**: Group Info → Administrators → Add Admin → pick bot.

### 2. Config Check (`config.yaml`)

```yaml
telegram:
  require_mention: true           # true: only reply when @mentioned
  observe_unmentioned_group_messages: true  # see messages without replying
  exclusive_bot_mentions: false   # false: see messages mentioning other bots
  allowed_chats: ''               # '' = allow all chats
  enabled: false                  # IS THIS TRUE? (common misconfig — need gateway, not this)
```

Key: `telegram.enabled: false` is NORMAL — the Telegram platform adapter is enabled via `gateway` not this field.

### 3. Log Forensics

```bash
# Find all activity for a specific group
grep "chat=-1003926068725" /opt/data/logs/gateway.log | tail -30

# Check inbound messages (with or without thread_id)
grep "inbound message" /opt/data/logs/gateway.log | grep "chat=-1003926068725"

# Check outbound responses (where did replies go?)
grep "response ready\|Sending response" /opt/data/logs/gateway.log | grep "chat=-1003926068725"

# Check if messages have thread_id suffix
# chat=-1003926068725        = general/main topic (no thread)
# chat=-1003926068725:348    = thread 348
# chat=-1003926068725:1      = thread 1 (often = general in topic groups)
```

### 4. Thread ID Tracing

Messages from **main chat** (no `/reply` context) show as `chat=-1003926068725` (no thread_id).
Messages from **a thread** (replies within a topic) show as `chat=-1003926068725:348`.

Gateway replies to the **same chat key** it received from. So:
- Main chat message → reply goes to main chat
- Thread message → reply goes to that thread

**Trap**: If user is in a thread, they won't see replies sent to main chat, and vice versa.

### 5. Direct Verification

Send a test message explicitly to a specific thread:

```python
# In Hermes session, send to thread 1 (main topic)
send_message(target="telegram:-1003926068725:1", message="Test — can you see this?")
```

Then ask user if they see it in the group.

## Pitfalls

- **`enabled: false` scares people** but is normal for gateway deployments — the platform adapter is managed by gateway, not the `enabled` field.
- **Thread_id in logs is subtle**: `chat=-1003926068725` vs `chat=-1003926068725:348` are different destinations. Miss the colon and you'll think replies are going to the wrong place.
- **Container date confusion**: Docker containers may have drifted system clocks. Always verify with `curl -s "https://timeapi.io/api/Time/current/zone?timeZone=UTC"` before trusting log timestamps for forensics.