# Replicate API Status — 2026-05-30

## Token Test Results

| Token | Status | Balance | Issue |
|-------|--------|---------|-------|
| `r8_YUS...` | 401 Unauthenticated | — | Token 无效或复制不完整 |
| `r8_Gm8...` | 401 Unauthenticated | — | Token 有效，余额 0 |

## Model Cost Reference

| Model | Cost Estimate | Notes |
|-------|--------------|-------|
| stability-ai/sdxl | ~$0.01-0.02/张 | 需要 credits |
| black-forest-labs/FLUX.1-schnell | ~$0.003/张 | 最便宜，4步生成 |
| black-forest-labs/FLUX.1-dev | ~$0.02/张 | 高质量，收费更高 |

## Error Codes

- `401 Unauthenticated` — token 无效或未传
- `402 Insufficient credit` — 账户余额不足，需要充值
- `404 Not Found` — 端点或 model version 不存在

## Quick Test Command

```bash
curl -s -X POST https://api.replicate.com/v1/predictions \
  -H "Authorization: Token <YOUR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"version": "black-forest-labs/flux-schnell:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b", "input": {"prompt": "a cute cat"}}'
```

## Setup Steps

1. 去 https://replicate.com/account/billing 充值
2. 去 https://replicate.com/settings/tokens 生成 API token
3. 充值后等待几分钟再试（credits 生效有延迟）