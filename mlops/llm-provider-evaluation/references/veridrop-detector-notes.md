# Veridrop Detector Notes

Real-world observations from testing freemodel.dev (scored 96.25/100).

## Detectors and what they mean

### 基础请求 (Basic Request) — weight 15
Tests if the endpoint responds at all to a simple chat completion. Pass = model name returned matches, `finish_reason: stop`.

### 模型一致性 (Model Consistency) — weight 15
Makes 3+ requests and checks the response model name stays stable. `stability_cv` < 0.05 is stable. If it fluctuates between different models, the relay is routing requests to different backends.

### 函数调用 (Function Calling) — weight 15
Verifies `tool_calls` support works — proper `id` prefix, `function` block, `finish_reason: tool_calls`.

### 结构化输出 (Structured Output) — weight 15
Tests JSON mode. Checks: `json_parse: True` (valid JSON), `schema_match: True` (fields match requested schema), `markdown_json_seen: False` (no code fences around JSON — indicates proper native JSON mode).

### 流式一致性 (Streaming Consistency) — weight 15
Compares stream vs non-stream responses. Checks: `text_match`, `finish_match`, `usage_match`. If mismatch, the relay handles stream and non-stream differently (bad sign). `stream_chunk_count` — abnormally low = truncated output.

### Token 计费 (Token Billing) — weight 10
**Most common partial-fail detector.** Checks reported `usage` tokens vs expected. Score < 100 with `risk_level: medium` means token counts are slightly inflated — relay markup, not model swapping. Doesn't affect quality but costs more over time. Score < 50 = significant inflation (likely relay padding aggressively).

### 协议规范性 (Protocol Compliance) — weight 15
Checks response shape: `object` field, `id` prefix format, `created` timestamp, `model` field. `critical_issue_count: 0` + `major_issue_count: 0` = clean.

### 长上下文真实性 (Long Context) — weight 15
SKIPS in standard mode (`skip_reason: mode-excluded`). Requires `include_long_context=true` or `include_long_context_extreme=true` at submit time. Costs extra from your API key ($0.05-$8 depending on depth). Only run when verifying advertised context window (32K, 128K, 1M).

## Score interpretation

| Score | Meaning |
|-------|---------|
| 90-100 | Genuine relay, all protocol/behavior checks pass |
| 70-89 | Real relay but billing quirks or minor protocol deviations |
| <70 | Likely model swapping, stripped capabilities, or dead endpoint |

## Veridrop API quick ref

```bash
# Submit OpenAI detection
curl -s -X POST https://veridrop.org/api/detect/openai \
  -d "base_url=$URL" -d "api_key=$KEY" -d "model=$MODEL" -d "mode=standard"

# Get JSON results
curl -s https://veridrop.org/api/result/$JOB_ID.json

# Claude protocol
curl -s -X POST https://veridrop.org/api/detect/claude \
  -d "base_url=$URL" -d "api_key=$KEY" -d "model=$MODEL"

# Gemini protocol
curl -s -X POST https://veridrop.org/api/detect/gemini \
  -d "base_url=$URL" -d "api_key=$KEY" -d "model=$MODEL"

# Pre-submit probe (check /v1/models)
curl -s -X POST https://veridrop.org/api/probe \
  -d "base_url=$URL" -d "api_key=$KEY"
```
