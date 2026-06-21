# NVIDIA 文章写作工作流（v0.6.42 确立，v0.6.43 更新）

> 本文档定义 NVIDIA 写 Hugo 文章的完整工作流。
> v0.6.43 更新：增加 changelog.yaml 更新步骤、Docker 文件系统同步说明、changelog patch vs append 区分。

---

## 触发条件

用户说「自由发挥 / 边摸索边成长 / 写一篇 / 你自己决定」时，NVIDIA 按本流程执行。

---

## 工作流

### 第一步：确认文章基本信息

在脑中或草稿中确定：
- **标题**：中文，有冲击力
- **slug**：英文小写字母+连字符
- **主分类**：先 `grep` 现有文章的 categories，确认已有分类才用
- **标签**：从现有 tags 选取，无合适的选择新标签

### 第二步：写文件

路径：`/repo/hugo-site/content/posts/{slug}/index.md`

```bash
mkdir -p /repo/hugo-site/content/posts/{slug}/
```

Frontmatter 格式（multi-line YAML，禁止 JSON 风格）：

```yaml
---
title: "文章标题"
date: 2026-05-29
draft: false
slug: article-slug
categories:
  - "火·AI"
  - "新分类"
tags:
  - 标签1
  - 标签2
---
```

> **封面图**：如需封面图，生成后按 PaperMod 嵌套格式加入 front matter（`cover.image` + `cover.alt`），不要用 `cover_status`（那是旧格式）。详见 `references/article-frontmatter-format.md`。

### 第三步：生成配图（如需封面图）

**首选：Pollinations（免费，无需 API key，CPU 容器可用）**

Docker 内无 GPU/ComfyUI 时，Pollinations 是正确工程选择，不要强求 ComfyUI。

```bash
# 检测连通性
curl -s "https://image.pollinations.ai/prompt/test" -o /tmp/test.png --max-time 30 -w "%{http_code}"
# 应返回 200 + 有效图片文件（~60-70KB）

# 生成封面图（1024×1024，约 60-120s）
mkdir -p /repo/hugo-site/static/images/posts/{slug}/
curl -s "https://image.pollinations.ai/prompt/<URL编码的prompt>" \
  -o /repo/hugo-site/static/images/posts/{slug}/cover.png \
  --max-time 120 -w "%{http_code}"
ls -lh /repo/hugo-site/static/images/posts/{slug}/cover.png
```

**prompt 写作原则**：英文，长句，画面感强；包含主体姿态、光影风格、氛围关键词、构图角度、技术质量词（`hyperdetailed, 8k, masterpiece`）。

风格参考：`A lone master in flowing dark robes... dramatic low-angle cinematic shot, dark xianxia fantasy meets cyberpunk sci-fi, volumetric fog, hyperdetailed, 8k, masterpiece`

**PaperMod 封面格式（必须嵌套 YAML）**：
```yaml
cover:
  image: /images/posts/{slug}/cover.png
  alt: "图片描述"
```
❌ 错误（字符串格式，Hugo 报错 `can't evaluate field image in type string`）：
```yaml
cover: /images/posts/{slug}.png
cover_alt: "图片描述"
```

**prompt 存档**：保存到文章同目录 `prompt.txt`，方便以后复用或升级到 ComfyUI。

**次选：ComfyUI**（本地有 GPU 时）。详见 `comfyui` skill。

### 第四步：更新 changelog.yaml

NVIDIA 可以更新 `hugo-site/data/changelog.yaml`（约束是「禁止 `cat >>` 盲目追加」，**不是禁止修改**）。两种合法场景：

| 场景 | 操作方式 | 示例 |
|------|---------|------|
| 补全现有条目 | `patch` 精确替换该条目 | v0.6.33 条目已有，补全文章+配图 |
| 插入新条目 | 在 `site.Data.changelog` 数组正确位置按版本顺序插入 | 新版本 v0.6.XX |

```bash
# patch 前验证 YAML 格式
python3 -c "import yaml; yaml.safe_load(open('/repo/hugo-site/data/changelog.yaml')); print('YAML valid')"
```

❌ 禁止：`cat block.yaml >> changelog.yaml`（盲目尾部追加会破坏 YAML 结构）

### 第五步：追加内部日志

```bash
# SITE_CHANGELOG.md（内部详细版本日志）
cat >> /repo/SITE_CHANGELOG.md << 'EOF'

## v0.6.XX — 2026-05-29

**标题**：文章标题

**摘要**：一句话描述

**标签**：标签1、标签2
EOF

# DAILY_WORK_LOG.md（每日工作日志）
cat >> /repo/DAILY_WORK_LOG.md << 'EOF'

## 2026-05-29｜v0.6.XX｜文章标题

### 执行链

- 总控 / 设计：NVIDIA（自由发挥授权）
- 文章写作：NVIDIA
- 发布：待本地 Mac
EOF
```

### 第六步：通知本地 Mac 重建

**关键约束（v0.6.42 血训）**：NVIDIA 在 Docker 内 `write_file /repo/...` 的文件，通过 Docker volume mount 写入宿主机文件系统，本地 Mac 理论上可以读到。但 Hugo 的增量 watch 有时会漏检新文件/新目录。

**新文章 Hugo 404 时**：
```bash
# 在本地 Mac 终端执行 Hugo 全量构建
hugo -s hugo-site --gc --cleanDestinationDir --minify
# 然后重启 hugo server
```

Hugo 全量构建后文章仍未进 `public/` → 说明文件没有真正写入 Mac 能读到的路径（不是容器内 `ls` 看到就完事）。见 SKILL.md 主体「Docker /repo 与本地 Mac 文件系统隔离」节。

### 第七步：等用户验收

写完后报告：
- 文件路径
- 标题和摘要
- 分类和标签
- 配图（如有）
- 等用户说「发 / 改 / 重写」

---

## 禁止事项

- ❌ 不等验收就重写
- ❌ `cat >> changelog.yaml` 盲目追加（正确做法见第四步）
- ❌ 执行 Hugo 构建
- ❌ 执行 git 操作（git add / commit / tag / push）

---

## 常见问题

**Q：分类不确定用什么？**
A：用「火·AI」做主分类，备选「一人公司」（新标签，需用户确认）。

**Q：用户说「写」但没具体要求？**
A：先确认格式/分类问题，不要直接重写整篇。

**Q：新写的文章 Hugo 404 怎么办？**
A：本地 Mac 重启 Hugo 或执行 `hugo -s hugo-site --gc --cleanDestinationDir --minify` 全量构建。

**Q：文章 Hugo 报错 `can't evaluate field image in type string`？**
A：cover 字段用了字符串格式，正确格式是嵌套 YAML：
```yaml
cover:
  image: /images/posts/slug/cover.png
  alt: "描述"
```

---

*本文档由 NVIDIA 于 2026-05-29 生成，v0.6.43 更新 changelog 更新步骤和 Docker 同步说明。*