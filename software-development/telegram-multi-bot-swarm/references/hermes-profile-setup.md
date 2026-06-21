# Hermes Profile Setup for Multi-Bot Swarm

## Why Profiles

Each Hermes profile is an independent `$HERMES_HOME` directory with its own:
- `config.yaml` — model, tools, telegram config
- `.env` — bot token, API keys
- `SOUL.md` — system prompt persona
- `gateway` — independent Telegram polling connection
- `sessions/`, `memories/`, `logs/` — isolated state

This lets each bot in a swarm run as a fully independent process.

## Step-by-Step Setup

### 1. Create Profiles

```bash
# Hermes CLI
/opt/hermes/.venv/bin/hermes profile create gold
/opt/hermes/.venv/bin/hermes profile create wood
# ... for all needed bots
```

Each creates: `/opt/data/profiles/<name>/` with skeleton configs.

### 2. Configure Bot Token

The token goes in each profile's `.env`:

```bash
# /opt/data/profiles/gold/.env
TELEGRAM_BOT_TOKEN=885803...

# Token redact workaround:
# Use base64 encoding to pass token through terminal:
echo -n "TOKEN_STRING" | base64
# Then decode and write:
echo "DECODED_BASE64" > /opt/data/profiles/gold/.env
```

### 3. Configure Telegram Settings

Each profile's `config.yaml` needs:

```yaml
telegram:
  exclusive_bot_mentions: false  # REQUIRED for bot-to-bot
  require_mention: true          # prevent random responses
  observe_unmentioned_group_messages: true  # see context
  enabled: true
```

And the main chat must be in `channel_directory.json` (auto-created when the gateway starts).

### 4. Write SOUL.md (Persona)

SOUL.md at the profile root defines the bot's personality:

```markdown
# SOUL: 金

You are 🟡 金 in a 五行 discussion group.

Your role: Analysis · Rules · Review. You examine plans for logical flaws,
risk points, and rule violations. You are the quality gate.

Group members: @gold_bot, @wood_bot, @water_bot, @fire_bot, @earth_bot

Behavior rules:
- Stay in character at all times
-  respond when @mentioned or when you find a flaw worth pointing out
- Keep responses concise (2-4 paragraphs)
- Be critical but constructive
```

### 5. Configure LLM

Since all profiles can share the same NVIDIA API key:

```bash
# /opt/data/profiles/gold/.env
NVIDIA_API_KEY=nvapi-...
```

Configure model in `config.yaml`:
```yaml
model:
  default: deepseek-ai/deepseek-v4-flash
  provider: nvidia
```

### 6. Start Gateways

```bash
# Test in foreground first
/opt/hermes/.venv/bin/hermes -p gold gateway run

# Install as background service
/opt/hermes/.venv/bin/hermes -p gold gateway install
/opt/hermes/.venv/bin/hermes -p gold gateway start

# Monitor
tail -f /opt/data/profiles/gold/logs/gateway.log
```

### 7. Add to Group

Add each bot to the Telegram group as **administrator** (needed to disable Privacy Mode so the bot sees all messages).

## Profile Management

```bash
# List profiles
/opt/hermes/.venv/bin/hermes profile list

# Show profile details
/opt/hermes/.venv/bin/hermes profile show gold

# Delete profile  
/opt/hermes/.venv/bin/hermes profile delete gold

# Change default profile
/opt/hermes/.venv/bin/hermes profile use gold
```

## Known Issues

- **409 Conflict**: Can't start two gateway instances with the same token. Each needs a unique token.
- **Gateway crash on 429**: NVIDIA rate limits kill the gateway worker. Restart needed.
- **s6 auto-restart**: The s6-supervise system auto-restarts the main gateway. Profile gateways need manual supervision or their own s6 service.
- **Token not in .env by default**: `hermes profile create` doesn't prompt for Telegram token. Must add manually.