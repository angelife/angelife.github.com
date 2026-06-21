# PicFlex API Reference

## 基础信息

- **API 端点**: `https://api.picflex.app/v1/text2image`
- **Key 环境变量**: `PICFLEX_API_KEY=pflex_...`（38字符，存储在 `~/.hermes/.env`）
- **模型**: ChatGPT-Image2（默认）
- **费用**: 1积分/图（余额足够时才生成）

## API Key 保存（不覆盖现有内容）

```bash
# 读取现有内容（如有）
cat ~/.hermes/.env 2>/dev/null || echo ""

# 追加一行（不用 >> 盲目追加——先检查是否已存在）
grep -q "PICFLEX_API_KEY=" ~/.hermes/.env && \
  sed -i 's|PICFLEX_API_KEY=.*|PICFLEX_API_KEY=pflex_MeuJdKdDf5a-qBRJi_p6RPCPmsWUPZF6|' ~/.hermes/.env || \
  echo 'PICFLEX_API_KEY=pflex_MeuJdKdDf5a-qBRJi_p6RPCPmsWUPZF6' >> ~/.hermes/.env
```

## 余额验证（先于任何生成）

```python
import urllib.request, json

key = "pflex_MeuJdKdDf5a-qBRJi_p6RPCPmsWUPZF6"
req = urllib.request.Request(
    "https://api.picflex.app/v1/credits",
    headers={"Authorization": f"Bearer {key}", "Content-Length": "0"},
    method="GET"
)
with urllib.request.urlopen(req, timeout=15) as r:
    data = json.loads(r.read())
balance = data["credits"]  # 或 data["data"]["balance"] — 按实际返回结构
print(f"余额: {balance}")
assert balance >= 1, f"余额不足: {balance}"
```

**余额不足或 key 无效 → 立即停止，不要尝试生成。**

## 生成流程（3步）

### Step 1 — 创建任务

```python
import urllib.request, json, ssl

ctx = ssl.create_default_context()

payload = json.dumps({
    "model": "chatgpt-image-2",
    "prompt": "dark tech poster, minimal, ...",  # 英文 prompt
    "aspect_ratio": "1:1",
    "style": "vibrant",
    "resolution": "1024x1024"
}).encode()

req = urllib.request.Request(
    "https://api.picflex.app/v1/text2image",
    data=payload,
    headers={
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    },
    method="POST"
)
with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
    result = json.loads(r.read())

task_id = result["task_id"]   # 例: "89490c3ce5f556c784d0e5f12ab24796"
print(f"Task created: {task_id}")
```

### Step 2 — 轮询状态（等完成）

```python
import urllib.request, time, json, ssl

ctx = ssl.create_default_context()
status_url = f"https://api.picflex.app/v1/text2image/{task_id}/status"

for attempt in range(20):
    req = urllib.request.Request(status_url, headers={"Authorization": f"Bearer {key}"}, method="GET")
    with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
        status_data = json.loads(r.read())
    state = status_data.get("state") or status_data.get("status")
    print(f"[{attempt+1}] state: {state}")
    if state in ("completed", "done", "success"):
        image_url = status_data["image_url"] or status_data["url"]
        print(f"Done: {image_url}")
        break
    if state in ("failed", "error"):
        print(f"Failed: {status_data}")
        break
    time.sleep(5)
else:
    print("Timeout after 20 attempts")
```

**不要用长循环轮询**（最多 20 次 × 5s = 100s）。若超时，报用户而不卡死。

### Step 3 — 下载

```python
import urllib.request, ssl, os

ctx = ssl.create_default_context()
req = urllib.request.Request(image_url, method="GET")
with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
    content = r.read()

out_path = "/repo/hugo-site/static/images/from-clever-to-system.png"
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "wb") as f:
    f.write(content)
print(f"Saved {len(content)} bytes → {out_path}")
```

## 文章配图落盘位置

| 类型 | 路径 |
|------|------|
| `posts/` 文章 | `/repo/hugo-site/static/images/posts/<slug>.png` |
| `series/` 文章 | `/repo/hugo-site/static/images/<slug>.png` |
| 备份副本（可选） | `/repo/images/<slug>.png` |

## frontmatter 更新

- **posts/**: `cover: { image: /images/posts/<slug>.png, alt: "..." }`
- **series/**: `images: ["/images/<slug>.png"]`

## 已知限制

- 网络限制：Docker 内可能无法直接访问 picflex.app（需绕过 Cloudflare 等防护）
- 若 curl 失败，尝试 Python urllib（某些环境下更稳定）
- Task ID 和 image_url 都是临时访问凭证，不要硬编码到规则文件