---
name: docker-vision-module
description: "Vision module for Docker Hermes — analyze images using NVIDIA Llama 3.2 vision model"
version: 1.0.0
author: NVIDIA/Docker Hermes
platforms: [docker, linux]
tags: [vision, image-analysis, nvidia, docker]
---

# Docker Vision Module

## Status
✅ WORKING — `meta/llama-3.2-11b-vision-instruct` on NVIDIA API

## Vision Client

**Location:** `/opt/data/vision_client.py`

```bash
python3 /opt/data/vision_client.py <image_path> [prompt]
```

**Examples:**
```bash
# Default prompt
python3 /opt/data/vision_client.py /path/to/image.jpg

# Custom prompt
python3 /opt/data/vision_client.py /path/to/image.jpg "What errors are shown?"
```

## API Key
- NVIDIA key: `NVIDIA_API_KEY` in `/opt/data/.env`
- Model: `meta/llama-3.2-11b-vision-instruct` (supports vision)
- Endpoint: `https://integrate.api.nvidia.com/v1/chat/completions`

## Integration Notes

### How to call from Hermes
Use `terminal()` or `execute_code` to invoke:
```python
# From execute_code:
from hermes_tools import terminal
result = terminal('python3 /opt/data/vision_client.py /opt/data/image_cache/img_xxx.jpg')
```

### Image paths for Telegram images
Telegram images are cached at: `/opt/data/image_cache/`

### Google Gemini (auxiliary.vision) — NOT WORKING
- `auxiliary.vision.provider: google` in config.yaml
- `GOOGLE_API_KEY=AQ.Ab8...` in .env
- Problem: 429 quota exceeded (limit: 0) — Google Cloud billing not enabled
- `AIzaSy...` key format is Google Cloud API key, doesn't work with Generative Language API
- **Do not use auxiliary.vision for now — use vision_client.py instead**

### NVIDIA models checked
Working vision models on NVIDIA Integrate API:
- `meta/llama-3.2-11b-vision-instruct` ✅ (in use)
- `meta/llama-3.2-90b-vision-instruct` (larger, slower)
- `microsoft/phi-3-vision-128k-instruct`
- `nvidia/llama-3.1-nemotron-nano-8b-v1`
- `google/deplot`

### Tested on real images
- Docker Desktop UI screenshots ✅
- WeChat/微信 chat screenshots (green bubbles, Chinese text) ✅
- Telegram image cache files ✅

## Chinese Text Extraction (Chat Screenshots)

Llama 3.2 vision 有时会给出"方法论"而非直接读文字，需要用特定 prompt 技巧触发 OCR：

**有效 prompt 模式：**
```
描述图中所有可见文字
请完整列出图中所有绿色和蓝色气泡内的中文文字内容
```

**无效 prompt（会触发"我是 LLM 无法做 OCR"拒绝）：**
```
请 OCR 识别 / Please perform OCR
提取图中文字
```

**实测有效流程：**
1. 先用通用描述 prompt 测试，看返回内容
2. 如果是方法论说明而非文字列表，换用"描述图中所有可见文字"
3. 目标明确时加颜色/位置限定：`绿色气泡内的中文文字`

## Image Generation — NOT on NVIDIA API

**NVIDIA Integrate API has ZERO image generation models.** Scanned all 118 models — none support text-to-image (no SD, FLUX, DALL-E, Ideogram, etc.).

## Image Generation

See `free-image-generation` skill — has full Pollinations docs, prompt engineering tips, Hugo article workflow, and upgrade path.

**Quick Pollinations URL:**
```
https://image.pollinations.ai/prompt/{URL-encoded-description}?width=1024&height=1024&nologo=true
```

**Verified working (2026-05-30):** JPEG/PNG output, 1024×1024, `&nologo=true` removes watermark. Use vision_client.py to verify output.

**⚠️ Replicate token status (2026-05-30):** Token `r8_Gm8...` — 认证有效，但账户余额 0 credits。优先用 Pollinations。

## References

- `references/nvidia-rate-limit-curl.md` — 40 RPM 硬性上限 + time.sleep(2) 控频机制 + curl 替代 requests 实现（2026-05-30 血训）
- `references/nous-hermes-vision-evaluation.md` — Why NousResearch/Nous-Hermes-2-Vision-Alpha is not needed
- `references/replicate-api-status.md` — Replicate token test results, model costs, credits situation

## Troubleshooting

**Empty response:** Check NVIDIA_API_KEY is set and valid in .env
**Timeout:** Image may be too large; NVIDIA has ~60s timeout
**JSON parse error:** API returned non-JSON; check stderr