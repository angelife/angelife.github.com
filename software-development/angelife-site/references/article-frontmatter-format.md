# Hugo 文章 Frontmatter 格式规范

> v0.6.42 更新。增加 PaperMod cover 嵌套格式说明（血训：hugo build 报错 `can't evaluate field image in type string`）。
> 本文档定义 angelife 网站文章的 frontmatter 标准格式。

---

## 正确格式（多行 YAML）

```yaml
---
title: "文章标题"
date: 2026-05-29
draft: false
slug: article-slug-here
categories:
  - "火·AI"
  - "栏目名"
tags:
  - 标签1
  - 标签2
---
```

## 错误格式（数组 JSON 风格）

```yaml
# ❌ 错误：JSON 风格数组
categories: ["AI时代"]
tags: ["标签A", "标签B"]
```

**问题**：JSON 风格数组与现有文章的 multi-line YAML 格式不一致，且可能在某些 Hugo 版本下解析异常。

---

## cover 字段格式（PaperMod 嵌套结构，必须！）

当文章有真实封面图时，**必须使用 PaperMod 嵌套格式**：

```yaml
# ✅ 正确格式（嵌套结构）
cover:
  image: /images/posts/article-slug/cover.png
  alt: "封面图描述文字"

# ❌ 错误格式（普通字符串）—— 会导致 Hugo 报错：
#   execute of template failed: ... executing "_partials/cover.html" at <.Params.cover.image>:
#   can't evaluate field image in type string
cover: /images/posts/article-slug/cover.png
```

**封面图文件存放路径**：`hugo-site/static/images/posts/<slug>/cover.png`

**封面图生成**：
1. 用 `free-image-generation` skill 生成图片
2. 存放图片：`hugo-site/static/images/posts/<slug>/cover.png`
3. 更新 front matter（如上格式）
4. Hugo rebuild 后验证页面正常加载

---

## 必须遵守的字段

| 字段 | 要求 | 说明 |
|------|------|------|
| `title` | 必须 | 文章标题，用双引号包住 |
| `date` | 必须 | YYYY-MM-DD 格式 |
| `draft` | 必须 | `false`（草稿用 `true`） |
| `slug` | 必须 | URL 友好，用 `-` 分隔 |
| `categories` | 必须 | multi-line YAML 格式，至少一个 |
| `tags` | 必须 | multi-line YAML 格式 |

---

## cover_status 规则（仅在无真实图片时使用）

| 值 | 含义 |
|-----|------|
| `prompt_ready` | 有 AI 生图 prompt，暂无真实封面图 |
| `draft` | 未完成 |

**无真实封面图时**：
- 只写 `cover_status: prompt_ready`
- **不要**写 `cover.image` 或 `cover: ...`（写会导致 Hugo 报错）
- 不创建 fake cover 文件
- 不写不存在的图片路径

---

## 现有文章分类参考

**主分类（categories 第一个）**：

| 分类 | 说明 |
|------|------|
| `火·AI` | AI 时代相关文章 |
| `易理` | 易经相关 |
| `一人公司` | 一人公司叙事文章 |
| `文章` | 通用文章 |
| `日课` | 每日更新 |
| `个人知识资产` | 知识管理 |

**标签（tags）示例**：

```
一人公司、大衍神君、AI时代、机器人、智能体、马斯克、凡人修仙
易经、震卦、随卦、判断力、AI时代、不失正见
NVIDIA、自动化施工
信息筛选、个人成长、低摩擦、AI写作
```

---

## 发布文章前检查清单

写完 frontmatter 后，确认：

- [ ] categories 是 multi-line YAML 格式，不是 `["值"]`
- [ ] tags 是 multi-line YAML 格式，不是 `["值"]`
- [ ] `cover.image` 使用嵌套格式（不是普通字符串）
- [ ] 封面图文件路径存在：`hugo-site/static/images/posts/<slug>/cover.png`
- [ ] slug 符合 `a-b-c` 格式（全是小写字母和连字符）
- [ ] `draft: false`（要发布的文章）

---

*本文档由 NVIDIA 于 2026-05-29 生成，v0.6.42 更新 PaperMod cover 格式。*