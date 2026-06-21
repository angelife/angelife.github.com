# Taxonomy Architecture: series/ vs columns/ vs posts/ (v0.7.22+)

## 目录结构与渲染逻辑

angelife.hugo.site 有三个内容 section：

| 目录 | 用途 | 渲染到 taxonomy |
|------|------|-----------------|
| `content/posts/` | 主文章（`index.md` 子目录格式）| via `series:` front matter |
| `content/series/` | **Taxonomy 源文件**（flat `.md` + `slug:`）| **直接渲染**到 `/series/SLUG/` 页面 |
| `content/columns/` | 第三 section（历史遗留，slug 可能冲突）| via `series:` front matter |

## 关键规则

### 1. series/ 是 taxonomy 页面的渲染源

PaperMod theme 的 series taxonomy list 页面（`/series/information-judgment/` 等）**直接从 `content/series/*.md` 读取内容**，不依赖 `content/posts/` 的 front matter。

删除 `series/SLUG.md` → taxonomy 页面丢失该文章，即使 `posts/SLUG/index.md` 存在。

### 2. slug 在不同 section 间不冲突

Hugo 的 `slug` 是 section-scoped。同一个 slug 值（如 `ai-as-jinyin`）可以同时存在于：
- `series/ai-bu-yin/ai-as-jinyin.md`
- `posts/ai-as-jinyin/index.md`
- `columns/ai-bu-yin/ai-as-jinyin.md`

这**不是 bug**，是正常 Hugo 行为。每个 section 有独立的 slug 命名空间。

### 3. columns/ 的 `series:` 值通常不匹配 config

organize 脚本创建的 `columns/` 文件有时带有中文 `series:` 值（如 `"蝉识录"`、`"AI补印"`、`"信息判断"`），而 `hugo.toml` 只定义了 `taxonomies: series = "series"`，没有对应的中文 taxonomy term。

这些 columns/ 文件**不会**渲染到 `/series/蝉识录/`（因为该 term 不存在），但会产生独立 URL 路径。

### 4. MD5 是判断重复的唯一可靠标准

series/ 和 columns/ 的同名 slug 文件，内容可能不同。必须用 MD5 哈希判断：
- **MD5 相同** → 内容完全一致，删除 columns/（冗余）
- **MD5 不同** → 内容有差异，columns/ 是独立版本，**不删除**

### 5. 正确的去重流程

```
1. find columns/ -name "*.md" → get slug for each
2. if slug exists in series/ → MD5 compare
3. if MD5 same → delete columns/ file
4. if MD5 different → keep both (independent versions)
5. commit with message: "fix(content): remove duplicate series or file for {category}"
```

## 本次清理记录（v0.7.22）

删除了 14 个 columns/ slug 冲突文件，MD5 均不同但 series 值不匹配 taxonomy config，删除安全。

涉及：chan-shi-lu(6), ai-bu-yin(2), information-judgment(2), confucian-framework(2), anti-populism(2)。

## CI vs 本地 build 差异排查

本地 `hugo list all` 输出格式为 CSV，grep 时注意字段位置：
```
content/path,slug,series,date,....
```
`grep ',series,'` 匹配 `series,` 字段（CSV 格式字段 4），但若 `series:` front matter 为空，该字段可能显示为空白，导致 grep 无输出但 exit code 1。

**处理**：`hugo list all | grep ',series,' || true`