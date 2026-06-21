# Tested LLM Providers

## OpenCode Zen (opencode.ai/zen)

- **Endpoint:** `https://opencode.ai/zen/v1`
- **Auth:** `OPENCODE_ZEN_API_KEY` in `.env`
- **Format:** OpenAI Chat Completions
- **Status:** Active primary provider

### Free models (as of 2026-06-21)

| Model | Status | Upstream | Quality | Notes |
|-------|--------|----------|---------|-------|
| `deepseek-v4-flash-free` | ✅ Working | DeepSeek | Excellent | Current default. Fast, good Chinese, good code. |
| `nemotron-3-ultra-free` | ✅ Working | NVIDIA 550B | Excellent | Best quality. Full reasoning chain. Free, $0 cost. |
| `mimo-v2.5-free` | ⚠️ Rate-limited | Xiaomi | Good | Rate limit after 2-3 fast calls. Decent Chinese + code. |
| `north-mini-code-free` | ⚠️ English-only | North | Poor | English-only, ignores Chinese instructions. |
| `qwen3.6-plus-free` | ❌ Expired | Alibaba | — | "Free promotion has ended" |
| `minimax-m3-free` | ❌ Expired | MiniMax | — | "Free promotion has ended" |

### Paid models (partial list)

`gpt-5.5`, `gpt-5.4`, `gpt-5.4-pro`, `gpt-5.4-mini`, `gpt-5.4-nano`, `gpt-5.3-codex`, `gpt-5.2`, `gpt-5.1`, `claude-opus-4-8`, `claude-sonnet-4`, `claude-haiku-4-5`, `gemini-3.5-flash`, `gemini-3.1-pro`, `glm-5.1`, `kimi-k2.6`, `big-pickle`, `grok-build-0.1`

---

## FreeModel.dev (freemodel.dev)

- **Endpoint:** `https://api.freemodel.dev/v1`
- **Auth:** API key `fe_oa_...` (per-account)
- **Format:** OpenAI Chat Completions
- **Status:** Tested, all models quality ✅
- **Veridrop score:** 96.25/100 (passed — genuine relay, no model swapping, protocol compliant)
- **Veridrop note:** Token billing scored 70/100 (medium risk — token counts slightly inflated, likely relay markup, doesn't affect capability)

### Models

| Model | Chinese | Code | Notes |
|-------|---------|------|-------|
| `gpt-5.5` | ✅ Excellent | ✅ Excellent | Fast, full reasoning. Best for general use. |
| `gpt-5.4` | ✅ Excellent | ✅ Excellent | Comparable to gpt-5.5. |
| `gpt-5.4-mini` | ✅ Good | ✅ Good | Fastest, best for high-frequency simple tasks. |
| `gpt-5.3-codex` | ✅ Good | ✅ Excellent | Code-optimized. Outputs code w/o markdown fences. |

### Pricing

- Plan: Pro (1-month free on verification)
- Balance: $10 credit confirmed on dashboard
- No `/v1/billing` endpoint exposed

### Hermes config

```yaml
custom_providers:
  freemodel:
    base_url: https://api.freemodel.dev/v1
    api_key: fe_oa_44ed7934a8592e61ec082e767d9bd3ce78a0cee949356f91
```

---

## NVIDIA NIM (nvidia.com)

- **Endpoint:** Via Hermes NVIDIA provider or direct REST
- **Auth:** `NVIDIA_API_KEY` in `.env`
- **Format:** OpenAI Chat Completions / custom REST
- **Status:** Primary vision provider

Key model: `meta/llama-3.2-11b-vision-instruct` — used for image analysis via custom `vision_client.py`. Uses NVIDIA NIM cloud API, NOT local GPU.

---

## OpenModel.ai (api.openmodel.ai)

- **Endpoint:** `https://api.openmodel.ai`
- **Status:** Added 2026-06-21, active fallback
- **Transparency:** ⚠️ Low — no privacy policy or ToS pages, WHOIS privacy, developer identity unknown

### Supported API protocols

OpenModel supports **multiple API protocols**, each with different models available:

| Protocol | Endpoint | Auth header | Extra headers |
|----------|----------|-------------|---------------|
| OpenAI Responses API | `POST /v1/responses` | `Authorization: Bearer om-*` | — |
| Anthropic Messages API | `POST /v1/messages` | `X-Api-Key: om-*` (recommend) or `Authorization: Bearer om-*` | `anthropic-version: 2023-06-01` |
| Gemini API | Various `/v1beta/models/...` | `X-Goog-Api-Key: om-*` | — |

### Models tested

| Model | Responses API | Anthropic API | Result |
|-------|:---:|:---:|--------|
| `gpt-5.5` | ✅ Works | ❌ N/A | General use, fast, good quality (regular pricing) |
| `gpt-5.4-mini` | ✅ Works | ❌ N/A | Fastest, good for simple tasks (regular pricing) |
| `deepseek-v4-flash` | ❌ No channel | ✅ Works | 🎯 **FREE during limited-time event** (10 RPM / 100K TPM) |
| `deepseek-v4-pro` | ❌ No channel | — | Listed but untested (2.5折 paid) |
| `claude-sonnet-4-6` | ❌ No channel | — | Listed but no working route found (95折 paid) |

**37 models total listed in `/v1/models`** but only GPT-5.5, GPT-5.4-mini via Responses, and DeepSeek V4 Flash via Anthropic are confirmed usable.

### Free event details (DeepSeek V4 Flash)

- **Event:** Limited-time free promotion (end date TBD, "恢复常规定价时另行通知")
- **Free model:** `deepseek-v4-flash` — input & output both $0 during event
- **Rate limits:** 10 RPM per key, 100K TPM per key
- **Protocol:** Anthropic Messages API only (`POST /v1/messages`)
- **Thinking:** Returns `thinking` blocks with reasoning chains + `text` blocks with answer (Claude-like output format)

### Responses API format (GPT models)

```python
# Request
POST /v1/responses
Authorization: Bearer om-...
Content-Type: application/json

{"model": "gpt-5.5", "input": "your prompt here"}

# Response
{
  "output": [{"content": [{"text": "response text"}], "role": "assistant"}],
  "model": "gpt-5.5-provider",
  "usage": {...}
}
```

### Anthropic API format (DeepSeek V4 Flash)

```python
# Request
POST /v1/messages
X-Api-Key: om-...
Content-Type: application/json
anthropic-version: 2023-06-01

{"model": "deepseek-v4-flash", "max_tokens": 1024,
 "messages": [{"role": "user", "content": "hello"}]}

# Response
{
  "content": [
    {"type": "thinking", "thinking": "...", "signature": "..."},
    {"type": "text", "text": "response text"}
  ],
  "model": "deepseek-v4-flash",
  "stop_reason": "end_turn"
}
```

### Pricing (non-free models)

New users get **$1 credit**. All non-free models are discounted during the event (2折-95折):

| Model | Original in | Original out | Event in | Event out |
|-------|:-------:|:--------:|:-----:|:------:|
| `gpt-5.5` | $5.00 | $30.00 | $3.50 | $21.00 |
| `gpt-5.4-mini` | $0.75 | $4.50 | $0.52 | $3.15 |
| `deepseek-v4-pro` | $1.74 | $3.48 | $0.43 | $0.87 |

### Hermes config

```yaml
custom_providers:
  openmodel:
    base_url: https://api.openmodel.ai
    api_key: om-<first-key>
    timeout: 30
  openmodel2:
    base_url: https://api.openmodel.ai
    api_key: om-<second-key>
    timeout: 30
```

Two keys added as separate providers for double rate limit (2× 10 RPM = 20 RPM combined). Both in fallback chain after `opencode`.

### Verdict

⚠️ **Limited — useful as DeepSeek V4 Flash free fallback.** The free DeepSeek V4 Flash event is genuine but time-limited. Transparency is poor (no privacy policy, no ToS, unknown operator). Only use for non-sensitive queries.

---

## Fallback Chain (current config)

1. `opencode` — OpenCode Zen (primary)
2. `openmodel` — OpenModel.ai key 1 (free DeepSeek)
3. `openmodel2` — OpenModel.ai key 2 (free DeepSeek, backup)
4. freemodel.dev also available as custom_provider (not in auto-fallback, switch manually)
