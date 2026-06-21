# Telegram Bot Group Mention / Privacy Mode Troubleshooting

## Symptom

User `@HermesAgentBot` in a Telegram group, but the bot doesn't respond — no message seen at all. DM works fine.

## Root Cause

Telegram bots have **Privacy Mode** enabled by default. In privacy mode, a bot only receives messages that:
1. Start with `/` (slash commands)
2. Explicitly `@mention` the bot by username

However, even `@mentions` can be silently dropped if the bot is **not a group administrator**. Without admin status, Telegram may not deliver the message to the bot at all.

## Fix

**Add the bot as a group administrator:**

1. Open the Telegram group
2. Go to Group Info → Administrators → Add Admin
3. Search for `@HermesAgentBot`
4. Add it — **no special permissions are needed** (all can be left off). The admin role just disables Privacy Mode so the bot can see messages that mention it.

## Verification

After adding as admin, test by sending:
```
@HermesAgentBot hello
```
The bot should respond within a few seconds.

## Config Check (Server Side)

On the Hermes server, verify the Telegram config allows group chats:

```bash
hermes config show 2>&1 | grep -A5 "telegram"
```

Key settings to check in `/opt/data/config.yaml`:

```yaml
telegram:
  reactions: false        # optional, cosmetic
  allowed_chats: ''       # empty = allow all chats (public groups, DMs, etc.)
```

If `allowed_chats` is empty (`''`), all chats are permitted. If it has specific chat IDs separated by commas, the bot will ignore messages from other chats.

## Common Pitfalls

- **Bot works in DM but not in group** → Almost certainly Privacy Mode / admin status. Fix: add as admin.
- **Bot was working, then stopped** → Bot may have been removed from admins (group admin change). Re-add.
- **Bot sees messages but doesn't respond** → Different problem. Check gateway logs (`~/.hermes/logs/gateway.log`) for errors.
- **Only some users' @mentions work** → Group settings may restrict who can @mention bots. Check group permissions.