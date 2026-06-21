# Batch Cover Generation Reference

Scripts and patterns for generating multiple article covers in bulk against Pollinations AI.

---

## Current Working Script (`/opt/data/regen_covers.py`)

**Key fixes from v0.7.17 incident:**
1. URL 必须加 `format=png`，否则 Pollinations 默认返回 JPEG（magic `FF D8 FF`）
2. 验证 header 同时接受 PNG (`\x89PNG\r\n\x1a\n`) 和 JPEG (`\xff\xd8\xff`)
3. curl 下载后要检查文件大小和 magic bytes，不能仅凭 HTTP 200 判断成功
4. 每次请求间隔 2.5s，有错误时指数退避 5s → 12.5s
5. 后台运行时用 `python3 -u`（unbuffered）确保日志实时写入

```python
#!/usr/bin/env python3
"""Regenerate all post covers with unique prompts based on title + category."""
import os, re, hashlib, subprocess, time, urllib.parse

POSTS_DIR = "/workspace/angelife.github.com/hugo-site/content/posts"
COVERS_DIR = "/workspace/angelife.github.com/images/posts"

STYLE_KEYWORDS = {
    "金·判断": "analytical framework logic cognitive bias pattern recognition",
    "木·蝉识": "bamboo forest nature growth zen mindfulness organic",
    "水·易理": "water flow yijing hexagram taoist water divination",
    "火·AI": "artificial intelligence neural network circuit data flow",
    "土·正见": "confucian ethics earth ground wisdom scholarly",
}

def get_title_and_cat(md_file):
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()
    title_match = re.search(r'^title:\s*"?([^"\n]+)"?', content, re.MULTILINE)
    title = title_match.group(1) if title_match else ""
    cat = None
    for c in ["金·判断", "木·蝉识", "水·易理", "火·AI", "土·正见"]:
        if c in content:
            cat = c
            break
    return title, cat

def gen_cover(slug_dir, title, cat):
    seed = int(hashlib.md5(slug_dir.encode()).hexdigest()[:8], 16) % 1000000
    style = STYLE_KEYWORDS.get(cat, "abstract art")
    prompt = f"{title} {style} no text no people abstract digital art minimalist"
    encoded_prompt = urllib.parse.quote(prompt)

    # format=png ensures PNG output; accept both PNG and valid JPEG (fallback)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=800&height=600&seed={seed}&nologo=true&format=png"

    cover_dir = os.path.join(COVERS_DIR, slug_dir)
    os.makedirs(cover_dir, exist_ok=True)
    out_path = os.path.join(cover_dir, "cover.png")

    # Check if valid image already exists
    if os.path.exists(out_path) and os.path.getsize(out_path) > 5000:
        with open(out_path, 'rb') as f:
            header = f.read(8)
        # Accept PNG or JPEG magic bytes
        if header[:8] == b'\x89PNG\r\n\x1a\n' or header[:3] == b'\xff\xd8\xff':
            return "skip", None

    # Download with retry + exponential backoff
    backoff = 5.0
    for attempt in range(1, 4):
        result = subprocess.run(
            ["curl", "-s", "--max-time", "30", "-L", "-o", out_path, url],
            capture_output=True
        )
        if os.path.exists(out_path) and os.path.getsize(out_path) > 5000:
            with open(out_path, 'rb') as f:
                header = f.read(8)
            if header[:8] == b'\x89PNG\r\n\x1a\n' or header[:3] == b'\xff\xd8\xff':
                return "ok", out_path
        if attempt < 3:
            print(f"    retry {attempt}/3 in {backoff}s...")
            time.sleep(backoff)
            backoff *= 2.5

    return "fail", None

def main():
    slugs = sorted(os.listdir(POSTS_DIR))
    total = len(slugs)
    ok = skip = fail = 0

    for i, slug_dir in enumerate(slugs):
        md_file = os.path.join(POSTS_DIR, slug_dir, "index.md")
        if not os.path.exists(md_file):
            continue

        title, cat = get_title_and_cat(md_file)
        if not cat:
            print(f"[{i+1}/{total}] SKIP {slug_dir} (no category)")
            continue

        status, path = gen_cover(slug_dir, title, cat)
        if status == "ok":
            ok += 1
            print(f"[{i+1}/{total}] OK {slug_dir}")
        elif status == "skip":
            skip += 1
            print(f"[{i+1}/{total}] SKIP {slug_dir} (exists)")
        else:
            fail += 1
            print(f"[{i+1}/{total}] FAIL {slug_dir}")

        if i < total - 1:
            time.sleep(2.5)

    print(f"\n=== Results: {ok} ok, {skip} skip, {fail} fail ===")

if __name__ == "__main__":
    main()
```

## Running the Script

```bash
# Clear old covers (force regenerate)
find /workspace/angelife.github.com/images/posts -name "cover.png" -type f | xargs rm -f

# Run with unbuffered output (required for real-time log monitoring)
cd /opt/data
nohup python3 -u regen_covers.py >> /opt/data/regen_covers.log 2>&1 &
echo "PID: $!"

# Monitor progress
tail -f /opt/data/regen_covers.log
```

## Expected Output Timeline (85 posts)

- 无错误时：每篇 ~3-5s（含 2.5s 间隔）
- 有 1 次重试：~18-20s
- 有 2 次重试：~30-35s
- 85 篇总计：约 25-30 分钟

## Categories & Style Keywords

| Category | Style Keywords |
|----------|---------------|
| 金·判断 | analytical framework logic cognitive bias pattern recognition |
| 木·蝉识 | bamboo forest nature growth zen mindfulness organic |
| 水·易理 | water flow yijing hexagram taoist water divination |
| 火·AI | artificial intelligence neural network circuit data flow |
| 土·正见 | confucian ethics earth ground wisdom scholarly |

## Root Cause of v0.7.17 Incident

**问题**：83 篇封面全部 FAIL，文件实际是有效的 JPEG  
**根因**：Pollinations 默认返回 JPEG，验证逻辑只检查 PNG magic bytes  
**修复**：`format=png` URL 参数 + 双重 magic bytes 验证 + 指数退避重试  
**教训**：Pollinations 不保证 PNG 输出，必须在 URL 加 `format=png` 并在验证时兼容 JPEG fallback

---

*Last updated: 2026-06-01 (v0.7.17 incident)*