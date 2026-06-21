# Hermes STT Capabilities (Speech-to-Text)

Assessment of available STT options for Hermes Agent deployments, covering local and cloud-based solutions.

## Hermes Built-in STT Providers

Hermes config.yaml supports these STT backends (under `stt:` section):

| Provider | Model | Cost | GPU Required | Notes |
|----------|-------|------|--------------|-------|
| `local` | faster-whisper (base/small/medium/large) | Free | No (CPU) | Already installed in Docker container (faster-whisper 1.2.1) |
| `openai` | whisper-1 | $0.006/min | No | Requires OpenAI API key with billing |
| `mistral` | voxtral-mini-latest | Paid | No | Mistral API key needed |
| `elevenlabs` | scribe_v2 | Paid | No | ElevenLabs API key needed |

### faster-whisper (Local CPU)

- Pre-installed in the Hermes Docker image (voice extras: `faster-whisper==1.2.1`)
- Uses CTranslate2 for efficient CPU inference
- Model sizes: tiny (~75MB), **base (~150MB)** ← default, small (~500MB), medium (~1.5GB), large-v3 (~3GB)
- The base model is cached at `/opt/data/home/.cache/huggingface/hub/models--Systran--faster-whisper-base/`
- No GPU needed — runs entirely on CPU (slower but functional)
- `sounddevice` (recording library) is NOT installed — audio must be provided as files, not recorded live

### Config Example

```yaml
stt:
  enabled: true
  provider: local          # or: openai, mistral, elevenlabs
  local:
    model: base            # tiny/base/small/medium/large-v3
    language: ''           # auto-detect, or set 'zh'/'en'
  openai:
    model: whisper-1
  mistral:
    model: voxtral-mini-latest
  elevenlabs:
    model_id: scribe_v2
    language_code: ''
voice:
  record_key: ctrl+b       # Hermes TUI record shortcut
  max_recording_seconds: 120
```

## User Environment Constraints (Reference: Low-Version Telegram on Mac)

From a real deployment assessment:

- **No GPU**: Neither the Docker container nor the Mac has usable GPU for local STT models. Mac is a 2015 Intel MacBook Pro (16GB RAM, 2GB GPU) — insufficient for GPU-based models.
- **Low-version Telegram client**: Cannot send voice messages natively. All audio must be sent as files (.mp3/.wav).
- **User preference**: Minimal complexity. The practical solution is to use 豆包输入法 (Doubao keyboard input method) on the Mac for voice-to-text, then paste the text into Telegram.

## STT Workflow for Low-Version Telegram

1. User installs 豆包输入法 on Mac
2. Speaks — 豆包 transcribes locally or via server
3. Pastes transcribed text into Telegram chat
4. No Hermes-side processing needed

## External Free STT APIs (Credit Card Required)

| Platform | Free Tier | Limits |
|----------|-----------|--------|
| Google Cloud STT | 60 min/month | Needs credit card, good Chinese support |
| Azure Speech | 5 hrs/month | Needs credit card |
| Deepgram | $200 credit | Chinese support weak |
| AssemblyAI | $50 credit | Chinese support weak |

These add unnecessary complexity for a workflow where 豆包 input method already solves the problem directly at the user's end.

## Recommendation for This User

- **Skip server-side STT** — no GPU, low-version Telegram, and 豆包 covers the need
- Docker's faster-whisper is available if ever needed (e.g., processing a pre-recorded audio file)
- External STT APIs are not worth the credit card registration overhead
