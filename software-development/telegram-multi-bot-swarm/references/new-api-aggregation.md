# New API — Central API Key Management for Multi-Bot Swarms

## What is New API

[New API](https://github.com/Calcium-Ion/new-api) (now maintained as `QuantumNous/new-api`) is an open-source LLM gateway and AI asset management system. It aggregates multiple upstream API keys into a single OpenAI-compatible endpoint, then distributes access via per-token sub-keys with granular model and quota controls.

## Why It Matters for Multi-Bot Setups

In a multi-bot swarm (e.g. 五行 group with 5+ bots), each bot needs its own API keys. With 10+ upstream accounts across platforms like OpenCode Zen, NVIDIA NIM, 智谱 AI (2000万 tokens), 中国移动云能 (2500万 tokens), Agnes AI, OpenRouter Free, 硅基流动, and 讯飞星辰 MaaS, managing keys per-bot becomes unwieldy. New API solves this by providing a single management plane.

## Architecture

```
Upstream API Keys (10+ accounts)
         │
         ▼
    New API Server
         │
         ├─ Sub-key for 木 bot
         ├─ Sub-key for 土 bot
         ├─ Sub-key for 金 bot
         ├─ Sub-key for 火 bot
         └─ Sub-key for 水 bot
```

Each bot gets its own sub-key. The admin controls which upstream models each sub-key can access, quota limits, rate limits, and can view usage statistics per bot.

## Key Benefits

- **Centralized management**: Add/rotate upstream keys in one place. All bots automatically benefit.
- **Automatic failover**: If one upstream key runs out of quota or fails, New API routes to the next available key.
- **Per-bot visibility**: See exactly how many tokens each bot consumed, from which upstream.
- **Reduced configuration**: Each bot only needs one API endpoint (New API) plus its sub-key — no need to configure 10 platforms per bot.

## Deployment

### Docker (Recommended)

```bash
# Pull the image
docker pull calciumion/new-api:latest

# Run with SQLite (simplest)
docker run --name new-api -d --restart always \
  -p 3000:3000 \
  -e TZ=Asia/Shanghai \
  -v ./data:/data \
  calciumion/new-api:latest
```

Then visit `http://localhost:3000` to configure.

### Initial Setup

1. **Admin account**: First-time setup creates an admin account
2. **Add channels**: Each upstream API key is a "channel" (OpenAI-compatible endpoint, API key, model mapping)
3. **Create tokens**: Generate sub-keys for each bot, assign model group permissions and quota
4. **Configure bots**: Point each bot's Hermes `config.yaml` to `http://new-api:3000/v1` with its sub-key

## Configuration for Hermes Bots

Each bot (Hermes profile) connects to New API as a standard OpenAI-compatible provider:

```yaml
# /opt/data/profiles/<name>/config.yaml
custom_providers:
  new-api:
    base_url: http://<new-api-host>:3000/v1
    api_key: sk-<sub-key-for-this-bot>
```

Reference models by the upstream name in Hermes model config.

## Pitfalls

- **New API is a management layer, not a model provider.** It cannot create model capabilities — it only distributes what you've plugged in.
- **Single point of failure.** If New API goes down, all bots lose API access. Consider Docker auto-restart + health checks.
- **SQLite for evaluation, MySQL for production.** SQLite is fine for light usage; for 5+ bots with heavy traffic, use MySQL for concurrent read/write.
- **Sub-key leak is not a full breach.** If a sub-key leaks, the attacker can only use the models/quota you assigned — but still rotate it immediately.
