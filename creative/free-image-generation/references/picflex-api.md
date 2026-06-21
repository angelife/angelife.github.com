# PicFlex API Reference

**Base URL:** `https://www.picflex.app`
**Auth:** `Authorization: Bearer {PICFLEX_API_KEY}` (bare key, no `Bearer ` prefix in the env value)
**Content-Type:** `application/json` for POST bodies

**API Key storage:** `~/.hermes/.env` (container: `/opt/data/home/.hermes/.env`). Read with `grep PICFLEX_API_KEY ... | tail -1 | cut -d= -f2`.

---

## Credits Pre-Check

```
GET /api/open/credits/balance
```

Response:
```json
{
  "availableCredits": 50,
  "reservedCredits": 0,
  "spendableCredits": 50,
  "wechatCredits": 0,
  "plan": { "tier": "free", "label": "Free Plan" }
}
```

**Key field for quota checks:** `spendableCredits`

If `401 invalid_api_key` → check the key is the bare `pflex_...` value, not `PICFLEX_API_KEY=pflex_...` and not prefixed with `Bearer`.

---

## Model Pricing (credits per generation)

### 文生图 (Text-to-Image)

| Model | Credits |
|-------|---------|
| `gpt-image-2-text-to-image` | **12** |
| `nano-banana-2` (1k) / (2k) / (4k) | 15 / 18 / 22 |
| `nano-banana-pro` (1k) / (2k) / (4k) | 6 / 6 / 12 |
| `google/nano-banana` | 3 |
| `seedream/4.5-text-to-image` (1k) / (4k) | 7 / 14 |
| `bytedance/seedream-v4-text-to-image` | 3.5 |
| `bytedance/seedream` | 3.5 |
| `grok-imagine/text-to-image` | 4 |
| `google/imagen4-ultra` | 12 |
| `ideogram/v3-text-to-image` | 1 |
| `qwen/text-to-image` | 4 |
| `z-image` | 1 |

### 图生图 (Image-to-Image)

| Model | Credits |
|-------|---------|
| `gpt-image-2-image-to-image` | **12** |
| `nano-banana-2` (1k) / (2k) / (4k) | 15 / 18 / 22 |
| `nano-banana-pro` (1k) / (2k) / (4k) | 15 / 18 / 20 |
| `google/nano-banana` | 2 |
| `seedream/4.5-text-to-image` | 7 |
| `bytedance/seedream-v4-text-to-image` | 3 |
| `qwen/text-to-image` | 4 |
| `topaz/image-upscale` (1k/2k/4k/8k) | 10/10/20/40 |
| `recraft/remove-background` | 1 |

---

## Endpoints

### Create Text-to-Image Task

```
POST /api/open/text2image/tasks
```

```json
{
  "prompt": "A clean tech poster, deep navy background, cyan circuit patterns",
  "model": "gpt-image-2-text-to-image",
  "aspectRatio": "auto",
  "resolution": "1k",
  "outputFormat": "png"
}
```

Response:
```json
{
  "taskId": "1694c4729094fa460b971dc08fd33c6b",
  "status": "queued",
  "requiredCredits": 12,
  "availableCredits": 50,
  "reservedCredits": 12,
  "spendableCredits": 38
}
```

### Query Task Status

```
GET /api/open/text2image/tasks/{taskId}
```

Poll every 5s. Complete when `status: "completed"`.

Response (completed):
```json
{
  "taskId": "...",
  "status": "completed",
  "consumedCredits": 12,
  "resultUrls": ["https://image.picflex.app/users/.../text2image/...png"],
  "previewResultUrls": ["https://tempfile.aiquickdraw.com/images/chatgpt/..."],
  "createdAt": "2026-05-30T10:05:47.086Z",
  "updatedAt": "2026-05-30T10:07:30.268Z"
}
```

### Image-to-Image

```
POST /api/open/image2image/tasks
```

```json
{
  "referenceUrl": "https://uploaded-image-url.png",
  "prompt": "Transform this into a premium product visual",
  "model": "gpt-image-2-image-to-image",
  "ratio": "auto"
}
```

### Upload Reference Image

```
POST /api/open/uploads/image
Content-Type: multipart/form-data
Field: file
```

Response: `{ "downloadUrl": "https://..." }` — use this URL as `referenceUrl` in image-to-image tasks.

---

## Error Codes

| HTTP | Meaning | Action |
|------|---------|--------|
| 401 | `invalid_api_key` | Key is wrong or malformed — check bare `pflex_...` format |
| 402 | `insufficient_credits` | Not enough `spendableCredits` — stop, report balance |
| 404 | `task_not_found` | Task ID wrong or belongs to different API key |
| Task `failed` | Generation failed | Check `failCode` and `failMessage` in response |

---

## Working Curl Patterns

**Balance check:**
```bash
curl -s -X GET "https://www.picflex.app/api/open/credits/balance" \
  -H "Authorization: Bearer $KEY" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  -H "Accept: application/json"
```

**Create task:**
```bash
curl -s -X POST "https://www.picflex.app/api/open/text2image/tasks" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: Mozilla/5.0" \
  -d '{"prompt":"...","model":"gpt-image-2-text-to-image","aspectRatio":"16:9"}'
```

**Poll status:**
```bash
curl -s "https://www.picflex.app/api/open/text2image/tasks/$TASK_ID" \
  -H "Authorization: Bearer $KEY" \
  -H "User-Agent: Mozilla/5.0"
```

**Download result:**
```bash
curl -s -o /repo/hugo-site/static/images/article-slug.png \
  "https://image.picflex.app/..." \
  -H "Authorization: Bearer $KEY"
```

**Python alternative (when curl has SSL issues):**
```python
import urllib.request, json, ssl
key = open('/opt/data/home/.hermes/.env').read().strip().split('=',1)[1]
ctx = ssl.create_default_context()
req = urllib.request.Request(url, headers={
    'Authorization': f'Bearer {key}',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
    'Accept': 'application/json'
})
with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
    data = json.loads(r.read())
```

If Python still throws `ssl.SSLEOFError` or gets 403, fall back to curl — the `User-Agent` header is the critical difference.