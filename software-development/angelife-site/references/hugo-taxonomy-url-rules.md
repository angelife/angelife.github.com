# Hugo Taxonomy URL 生成规则 — v0.7.19 纠正版

## ⚠️ 重大纠正（v0.7.19）

**之前的"中文 taxonomy URL + 静态重定向"方案存在根本性缺陷，已废弃。**

错误方案：
- 菜单指向中文 taxonomy URL（`/series/信息判断/`）
- Hugo 未生成中文 taxonomy 页面（404）
- 用静态 HTML 重定向作为补偿
- 结果：静态重定向与 Hugo 内容冲突，导致重定向循环

**已验证的真正根因**：`content/series/english-slug/_index.md` 创建 **Section** 页面（`/series/english-slug/`），posts 里的 `series: [中文]` 创建 **Taxonomy** 页面（`/series/中文/`）。GitHub Pages 构建版本中 taxonomy 页面未生成。Section 页面正常工作且有内容。

**正确的修复**：菜单 URL 改为 Section 路径，不使用 taxonomy 路径。

## 正确的菜单配置

```toml
[[menu.main]]
  identifier = "phase-metal"
  name = "金·判断"
  url = "/series/information-judgment/"   # Section 路径（非 taxonomy 路径）
  weight = 10
```

所有栏目使用对应的 section 路径：
| 栏目 | 菜单 URL |
|------|---------|
| 金·判断 | `/series/information-judgment/` |
| 木·蝉识 | `/series/chan-shi-lu/` |
| 水·易理 | `/series/yi-notes/` |
| 火·AI | `/series/ai-bu-yin/` |
| 土·正见 | `/series/confucian-framework/` |
| 反民粹 | `/series/anti-populism/` |

## Hugo Section vs Taxonomy 的区别

```
content/series/information-judgment/
├── _index.md           ← 创建 Section 页面 /series/information-judgment/
├── article-a.md        ← 文章 slug: information-quality-framework
└── article-b.md        ← 文章 slug: information-source-slimming

Frontmatter:
  series: ["信息判断"]

Hugo 生成:
  /series/information-judgment/          ← Section 页面（内容来自 _index.md）
  /series/information-quality-framework/ ← 文章页面（slug 决定）
  /series/信息判断/                       ← Taxonomy 页面（series: [中文] 中的词决定）
```

两者是**不同的 URL**，指向不同的内容：
- Section 页面：`_index.md` 的 description + 栏目内所有文章列表
- Taxonomy 页面：由 Hugo 自动聚合所有 `series: [信息判断]` 的文章

## 旧版架构问题（已废弃）

v0.7.18 尝试的架构：
```
菜单 URL (/series/信息判断/) → Taxonomy 页面（但 GitHub Pages 未生成）
英文 slug (/series/information-judgment/) → Section 页面（正常）
```

这个架构的问题是 GitHub Pages 的 Hugo 构建未生成中文 taxonomy 页面。

## 验证命令

```bash
# Section 页面（正确）
curl -s -o /dev/null -w "%{http_code}" "https://angelife.github.io/series/information-judgment/"

# Taxonomy 页面（404，应改用 section URL）
curl -s -o /dev/null -w "%{http_code}" "https://angelife.github.io/series/%E4%BF%A1%E6%81%AF%E5%88%A4%E6%96%AD/"

# 所有栏目页批量检查
for slug in information-judgment chan-shi-lu yi-notes ai-bu-yin confucian-framework anti-populism; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "https://angelife.github.io/series/$slug/")
  echo "$slug: $code"
done
```

## 踩坑记录

### `series = "columns"` 实验失败（v0.7.18）

企图让 taxonomy 生成 `/columns/xxx/` URL，但 `content/columns/` 目录作为 Section shadow 了 `static/columns/` 下的静态文件。结论：`[taxonomies] series = "series"` 是唯一正确配置。

### 静态重定向导致循环（v0.7.18）

`static/series/information-judgment/index.html`（meta refresh）存在时，Hugo 同时生成 `public/series/information-judgment/index.html`，URL 冲突导致重定向循环。**禁止用静态文件做 Hugo URL 的重定向。**

### 不要删除 `content/series/` 目录

v0.7.19 早期误删 `content/series/`（22 个文件），需要从 git 恢复：`git checkout bf1acd5 -- hugo-site/content/series/`。这个目录是 section 内容的来源，删除后 section 页面会 404。