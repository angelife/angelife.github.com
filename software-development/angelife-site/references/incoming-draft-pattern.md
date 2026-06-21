# _incoming/ 草稿目录机制

作者希望**先收集内容，后整理格式**。当发来一篇 Markdown 文章（如 Kindle 越狱指南）要求发到网站时：

## 用户偏好

- ❌ 不要添加 Hugo frontmatter
- ❌ 不要直接放入 `content/posts/`
- ✅ 放入 `_incoming/<slug>/index.md`（纯 Markdown，无 frontmatter）
- ✅ 用户会**自己回来整理**成 Hugo 文章

## 操作流程

```bash
# 1. scp 文章到 Mac（从 Docker）
scp -o StrictHostKeyChecking=no -i /opt/data/home/.ssh/id_ed25519 \
  /path/to/article.md \
  macos@host.docker.internal:/tmp/article.md

# 2. 创建 _incoming 目录并放置
REPO="/Users/macos/angelife.github.com"
mkdir -p "$REPO/_incoming/<slug>"
cp /tmp/article.md "$REPO/_incoming/<slug>/index.md"
# 或直接 cp 已 scp 的文件：
cp /tmp/article.md "$REPO/_incoming/"

# 3. 验证
ls -la "$REPO/_incoming/"
```

## 格式要求

- **纯 Markdown** — 不加 YAML frontmatter
- 保留原文的标题层级、列表、代码块
- 文件名用 slug：`kindle-k3w-koreader-2026.md`
- 如果用户指定了固定路径（如 `_incoming/kindle-k3w-koreader-2026/index.md`），按用户要求