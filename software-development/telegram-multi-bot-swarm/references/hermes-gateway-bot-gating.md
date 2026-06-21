# Hermes Gateway Bot-Message Gating

This document details the Hermes Gateway mechanism that controls whether Hermes sees and processes messages from other Telegram bots in a group. Discovered during multi-bot swarm development (2026-06-07).

## Source File

`/opt/hermes/gateway/platforms/telegram.py` (~5861 lines)

## The Gating Chain

### Entry Point: `_should_process_message` (line 4837)

Every incoming message passes through this gate. For the first time a non-command message is seen, it calls `_handle_text_message` (line 4950) which calls `_should_process_message`. If that returns False, the message goes to `_should_observe_unmentioned_group_message` which only stores it as context (does not dispatch).

### The Bot-Exclusion Gate: `exclusive_bot_mentions` (line 4408)

```python
def _telegram_exclusive_bot_mentions(self) -> bool:
    configured = self.config.extra.get("exclusive_bot_mentions")
    if configured is not None:
        if isinstance(configured, str):
            return configured.lower() in {"true", "1", "yes", "on"}
        return bool(configured)
    return os.getenv("TELEGRAM_EXCLUSIVE_BOT_MENTIONS", "true").lower() in {"true", "1", "yes", "on"}
```

**DEFAULT: `true`**. This means by default, Hermes IGNORES messages that mention other bots without also mentioning Hermes.

### The Exclusion Logic: `_explicit_bot_mentions_exclude_self` (line 4661)

```python
def _explicit_bot_mentions_exclude_self(self, message: Message) -> bool:
    mentioned_bot_usernames = self._extract_bot_mention_usernames(message)
    return bool(mentioned_bot_usernames) and bot_username not in mentioned_bot_usernames
```

Logic:
1. Extract all @...bot usernames from the message text (entities preferred, regex fallback)
2. If ANY bot usernames found AND Hermes's own username is NOT among them → return True (exclude)
3. This means: "Other bots are talking among themselves, this message is not for me"

### Where the Gate Is Applied (2 places)

**Place 1: Line 4887** — `_should_process_message`:
```python
if self._telegram_exclusive_bot_mentions() and self._explicit_bot_mentions_exclude_self(message):
    return False  # Entire message is skipped — no dispatch, no observe
```

**Place 2: Line 4733** — `_should_observe_unmentioned_group_message`:
```python
if self._telegram_exclusive_bot_mentions() and self._explicit_bot_mentions_exclude_self(message):
    return False  # Not even stored as observed context
```

This means: when `exclusive_bot_mentions=true` (default), Hermes **completely ignores** any group message that mentions other bots. The message is neither dispatched to the agent nor stored as observed context.

## Bot Username Detection: `_extract_bot_mention_usernames` (line 4552)

```python
@staticmethod
def _extract_bot_mention_usernames(message: Message) -> set[str]:
    # Entity-based: prefers Telegram server-side entities (authoritative)
    for entity in entities:
        if entity_type == "mention":
            handle = text[offset:offset+length].lstrip("@").lower()
            if re.fullmatch(r"[a-z0-9_]{2,29}bot", handle):  # MUST end in "bot"
                mentioned.add(handle)
        elif entity_type == "bot_command":
            at_index = text.find("@")
            if at_index >= 0:
                target = text[at_index+1:].lower()
                if re.fullmatch(r"[a-z0-9_]{2,29}bot", target):
                    mentioned.add(target)
    
    # Raw-text fallback (only if NO entities for this source)
    for match in re.finditer(r"@([A-Za-z0-9_]{2,29}bot)\b", text):
        mentioned.add(match.group(1).lower())
    
    return mentioned
```

**The regex `[a-z0-9_]{2,29}bot` is critical**: Only usernames ending in "bot" are detected. This is Telegram's requirement for bot usernames.

## Configuration Options

### Option A: Disable `exclusive_bot_mentions`

```yaml
# /opt/data/config.yaml
telegram:
  exclusive_bot_mentions: false
```

**Effect**: Hermes will process ALL group messages, including those mentioning other bots. The `_should_process_message` gate at line 4887 is bypassed entirely.

**Trade-off**: Without `require_mention`, Hermes may respond to every group message. You likely want:
```yaml
telegram:
  exclusive_bot_mentions: false
  require_mention: true  # Still requires @Hermes to respond
  observe_unmentioned_group_messages: true  # BUT still sees context
```

### Option B: Keep default, use @Hermes in multi-bot conversations

When 金 says:
```
@HermesAgent 我觉得 AI 对人类来说...
```
Hermes will process this message because `bot_username` will be in `mentioned_bot_usernames`.

## Implications for Multi-Bot Swarm

### Pattern A (Hermes-Mediated Ad-hoc): WORKS
- Hermes is a group member, sees messages natively
- Need `observe_unmentioned_group_messages: true` and `require_mention: false`
- Or use @Hermes in each invocation
- Then Hermes decides and calls other bots via API

### Pattern B (Single-Polling Multi-Bot): BLOCKED
- The polling bot IS Hermes Gateway
- If 金 sends a message → Gateway receives it ✓
- Gateway checks `exclusive_bot_mentions` → 金's message mentions 金, not Hermes → blocked ✗
- Fix: Set `exclusive_bot_mentions: false` in config

### Pattern C (Single-Bot Labels): WORKS (no multi-bot)
- Only one bot, no other bot usernames → gate never triggers

## Verification

```bash
# Check current setting
grep "exclusive_bot_mentions" /opt/data/config.yaml

# After change: restart gateway
pkill -f "hermes gateway run"
# s6 will auto-restart
```