# Telegram Bot Ecosystem on GitHub

Survey of notable Telegram bot frameworks and multi-agent projects found on GitHub (June 2026).

## Big Frameworks (general-purpose Telegram bot building)

| Project | Stars | Language | Strength |
|---------|-------|----------|----------|
| **AstrBot** | 35K | Python | Multi-IM (QQ/Telegram/Discord), plugin system, LLM + MCP support. Chinese community. "openclaw alternative" |
| **python-telegram-bot** | 29K | Python | The classic — stable, mature, full Bot API coverage |
| **aiogram** | 5.7K | Python | Modern async-native Telegram framework, lighter than PTB |
| **pyrogram** | 4.6K | Python | MTProto protocol (not HTTP Bot API) — can act as user account, not just bot |
| **teelebot** | 178 | Python | Plugin system with hot-reload, Chinese docs |

Links:
- https://github.com/AstrBotDevs/AstrBot
- https://github.com/python-telegram-bot/python-telegram-bot
- https://github.com/aiogram/aiogram
- https://github.com/pyrogram/pyrogram
- https://github.com/plutobell/teelebot

## Telegram + AI / Multi-Agent / MCP

Projects that combine Telegram with LLM agents, multi-agent orchestration, and MCP tools — closest pattern to our Hermes multi-bot setup.

| Project | Stars | Language | Description |
|---------|-------|----------|-------------|
| **magec** | 96 | Go | Multi-agent AI platform, voice control, visual workflows, Telegram integration, MCP servers |
| **DuDuClaw** | 43 | Rust+Python | 80+ MCP tools, 7 channels (Slack/Discord/LINE/Telegram), self-hostable |
| **opencrow** | 21 | TypeScript | Self-hosted multi-agent orchestration, Telegram/WhatsApp/Web, 90+ tools |
| **SoulFlow-Orchestrator** | 21 | TypeScript | Cloud-independent self-hosted AI agent runtime, Slack/Telegram/Discord/Web, multi-provider |
| **cogitum** | 11 | Python | CLI + Textual TUI, multi-provider LLM mesh, persistent sessions, MCP, Telegram gateway |
| **ErisPulse** | 47 | Python | Event-driven multi-platform bot framework — QQ/Telegram/Kook/Matrix/email 10+ platforms |

Links:
- https://github.com/achetronic/magec
- https://github.com/zhixuli0406/DuDuClaw
- https://github.com/gokhantos/opencrow
- https://github.com/berrzebb/SoulFlow-Orchestrator
- https://github.com/StarryCod/cogitum
- https://github.com/ErisPulse/ErisPulse

## Findings Summary

- **AstrBot** (35K ⭐) is the most relevant large framework — Chinese-friendly, plugin system, multi-IM, MCP. Worth evaluating if we want a second bot infrastructure.
- **DuDuClaw** and **opencrow** are the closest to our multi-bot MCP pattern. Both are small but actively maintained.
- **magec** stands out for voice control + visual workflow — unique offering.
- No project found that directly competes with or exceeds Hermes Agent's Telegram gateway for our use case (multi-profile multi-bot SOUL.md-driven persona agents). Hermes remains the most capable for this specific pattern.
