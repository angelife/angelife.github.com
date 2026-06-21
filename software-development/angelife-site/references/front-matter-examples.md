# Hugo Front Matter Examples

## Example 1: Article with Cover Image (tested 2026-05-29)

```yaml
---
title: "大衍神君的第一人"
date: 2026-05-29
draft: false
slug: the-future-is-one-person-company
categories:
  - "火·AI"
  - "一人公司"
tags:
  - 一人公司
  - 大衍神君
  - AI时代
  - 机器人
  - 智能体
  - 马斯克
  - 凡人修仙
cover: /images/posts/the-future-is-one-person-company.png
cover_alt: "大衍神君孤身立于虚空，万千机械傀儡环绕发光"
---
```

Key rules:
- `categories` uses valid YAML list format (not inline `["A", "B"]`)
- `cover` path is absolute from `static/`: `/images/posts/...` → `static/images/posts/...`
- `cover_alt` is required for accessibility
- Do NOT use `cover_status: prompt_ready` — must be actual image path or omitted

## Categories in Use

| Category | Chinese |
|----------|---------|
| AI时代 / 火·AI | AI-related articles |
| 一人公司 | One-person company theme |
| 认知·方法 | Methods and cognition |
| 译文 | Translations |
| 概念·人物 | Concepts and figures |

## Tags Conventions

- Lowercase Chinese / English mixed
- No dashes or underscores in Chinese tags
- Max 7 tags per article
- Include key concepts, names, themes for discoverability