# OpenCode Zen Models & Pricing

Source: https://opencode.ai/docs/zen/
Verified: 2026-06-19

## API

- **Base URL**: `https://opencode.ai/zen/v1`
- **Model format**: `opencode/<model-id>` (e.g. `opencode/gpt-5.5-pro`)
- **Auth**: Bearer token via `OPENCODE_ZEN_API_KEY` env var or `auth.json`

## Auth File Format

`~/.local/share/opencode/auth.json`:
```json
{
  "opencode": {
    "api_key": "<key>",
    "base_url": "https://opencode.ai/zen/v1"
  }
}
```

## Free Models (No Balance Needed)

| Model ID | Notes |
|----------|-------|
| `big-pickle` | Generic, works for simple tasks |
| `deepseek-v4-flash-free` | Decent coding |
| `mimo-v2.5-free` | Small model |
| `nemotron-3-ultra-free` | NVIDIA model |
| `north-mini-code-free` | Code-optimized |

## Paid Models (Need $20+ Balance)

### GPT Series
| Model ID | Input ($/1M) | Output ($/1M) |
|----------|-------------|--------------|
| `gpt-5.5-pro` | 30.00 | 180.00 |
| `gpt-5.5` | 5.00 (≤272K) / 10.00 (>272K) | 30.00 / 45.00 |
| `gpt-5.4-pro` | 30.00 | 180.00 |
| `gpt-5.4` | 2.50 (≤272K) | 15.00 |
| `gpt-5.4-mini` | 0.75 | 4.50 |
| `gpt-5.4-nano` | 0.20 | 1.25 |
| `gpt-5.3-codex` | — | — |
| `gpt-5.2-codex` | — | — |
| `gpt-5.1-codex-max` | — | — |
| `gpt-5-codex` | — | — |

### Claude Series
| Model ID | Input ($/1M) | Output ($/1M) |
|----------|-------------|--------------|
| `claude-fable-5` | 10.00 | 50.00 |
| `claude-opus-4-8` thru `claude-opus-4-1` | 5.00 (4.5-4.8) / 15.00 (4.1) | 25.00 / 75.00 |
| `claude-sonnet-4-6` | 3.00 | 15.00 |
| `claude-sonnet-4-5` | 3.00 (≤200K) / 6.00 (>200K) | 15.00 / 22.50 |
| `claude-haiku-4-5` | 1.00 | 5.00 |

### Other
| Model ID | Input ($/1M) | Output ($/1M) |
|----------|-------------|--------------|
| `deepseek-v4-pro` | 1.74 | 3.48 |
| `deepseek-v4-flash` | 0.14 | 0.28 |
| `qwen3.7-max` | 2.50 | 7.50 |
| `qwen3.7-plus` | 0.40 | 1.60 |
| `gemini-3.5-flash` | 1.50 | 9.00 |
| `gemini-3.1-pro` | 2.00 (≤200K) / 4.00 (>200K) | 12.00 / 18.00 |
| `minimax-m2.7` | — | — |

### ⚠️ Important: `opencode/zen` Is NOT a Model

A common mistake — `zen` is the subscription plan name, not a valid model ID.
Use `opencode/<actual-model-name>` from the lists above.

## Hermes Fallback Provider

The Zen key doubles as a **Hermes backup provider**. Configure in `config.yaml`:

```yaml
providers:
  opencode:
    base_url: https://opencode.ai/zen/v1
    api_key: ''  # key lives in .env as OPENCODE_ZEN_API_KEY
fallback_providers:
  - opencode
```

When the main provider (e.g. NVIDIA) fails after retries, Hermes auto-falls back to OpenCode Zen. Model names are resolved through opencode's model mapping — a `deepseek-ai/deepseek-v4-flash` model name from the main provider becomes `opencode/deepseek-v4-flash` resolved through Zen's API.

## Verification

```bash
# Quick API test
curl -s --max-time 15 -X POST "https://opencode.ai/zen/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENCODE_ZEN_API_KEY" \
  -d '{"model":"deepseek-v4-flash-free","messages":[{"role":"user","content":"Say: OK"}],"max_tokens":10}'

# OpenCode smoke test
opencode run 'Respond with exactly: OPENCODE_ZEN_OK'
```
