# Docker Hermes Vision Capability — Technical Notes

## Status: This container (hermes-minimaxlab) does NOT have vision tools

### Container environment facts

- The hermes-minimaxlab Docker image is a **stripped-down execution environment**
  — No `hermes` CLI binary in PATH
  — No `~/.hermes/` config directory
  — No `hermes config set` command available inside the container
  — `hermes` commands run on the **host Mac** affect only the host's Hermes install, not the container

- `auxiliary.vision.provider` + `auxiliary.vision.model` in config.yaml only work
  when the **vision toolset is already enabled** in the base image.
  Configuration alone cannot add a missing toolset — it's a prerequisite, not a lever.

### Three方案 (from 剑妈)

**方案一 — Vision API（推荐起步）**
Docker 内 Python 脚本：image → base64 → vision model API → text reasoning output
最小改动，1 天内可上线。不依赖容器内有 vision 工具，外部 API 负责图像理解。

```
Task
  → detect image input
  → image path / volume
  → base64 encode
  → vision model API (GPT-4o / Qwen-VL / provider vision endpoint)
  → structured reasoning output
  → Hermes tool execution
```

Dependencies inside container:
```
apt-get install -y curl jq
pip install pillow requests
```

**方案二 — Local vision model in Docker**
LLaVA / Qwen2-VL / InternVL inside container. GPU required, more complex.

**方案三 — Hermes native multimodal (long-term)**
Unified input: `{text, images, files}` → Input Router → Vision Encoder → Unified Reasoning → Tools

### Recommended architecture (minimal change path)

```
           ┌──────────────┐
           │   Hermes      │
           │ controller   │
           └──────┬───────┘
                  │
       ┌──────────┼──────────┐
   text       vision      tools
   model      module      docker
   (MiniMax   (API or     (CLI/git/
    M2)       local VL)   repo ops)
```

Vision module is **pluggable** — swap API provider without changing Hermes.

### Minimal viable implementation (方案一)

Inside container, need:
1. Read image files (Telegram image cache path or mounted volume)
2. `image_to_base64(path)` — Python stdlib
3. `ask_vision(image_b64, prompt)` — POST to vision API endpoint
4. API key via environment variable or mounted secret

### Key constraints for this project

- NVIDIA Docker container uses MiniMax M2 model — check if it supports vision API
  before building a custom client
- Vision module files should go somewhere like `/opt/data/vision_client.py` in the container
- Telegram images arrive in the container via the messaging gateway pipeline, not as file paths
  the container controls directly