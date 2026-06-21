# Blogger → Hugo Migration Pipeline

## Overview

全自动 pipeline：抓取 Blogger Atom feed → 解析 → 转换 HTML→Markdown → 生成 Hugo 文章 → Hugo build → git push。

脚本位置：`/opt/data/blogger_migrate.py`

## Prerequisites

```bash
eval $(ssh-agent) && ssh-add ~/.ssh/id_ed25519
git config --global user.email "nvidia@angelife.ai"
git config --global user.name "NVIDIA (Docker Hermes)"
```

## Usage

```bash
cd /repo && python3 /opt/data/blogger_migrate.py
```

## Key Design Decisions

### Atom feed parsing — use URI notation, not namespace prefix maps

Python's `xml.etree.ElementTree` fails with `SyntaxError: prefix 'openSearch' not found in prefix map` when using namespace maps in `find()` / `findall()`. Use URI notation instead:

```python
# Wrong
root.find('.//openSearch:totalResults', ns)   # fails
root.findall('atom:entry', ns)                  # fails

# Correct — URI notation
root.find('.//{http://a9.com/-/spec/opensearchrss/1.0/}totalResults')
root.findall('{http://www.w3.org/2005/Atom}entry')
```

### Blogger pagination — extract start-index from next link href

Do NOT calculate `start_index = page * 50`. Extract it from the `href` of the `<link rel="next">` element:

```python
next_link = root.find('{http://www.w3.org/2005/Atom}link[@rel="next"]')
href = next_link.get('href', '')
m = re.search(r'start-index=(\d+)', href)
start_index = int(m.group(1))
```

Blogger's second page starts at `start-index=51`, not `start-index=51` as a simple calculation would suggest.

### Git add — use directory add for new content, precise add for modified

`git status --porcelain` output with special characters (spaces in Chinese filenames) causes `git add` parsing failures. Use directory-level adds:

```bash
# For untracked new posts — add by directory
git add "hugo-site/content/posts/"

# For modified public/ files — glob or direct
git add categories/index.html categories/index.xml changelog/index.html index.html ...
```

Never parse `git status --porcelain` line-by-line with string splitting — Chinese characters and spaces break `git add <path>` parsing.

### HTML → Markdown — use regex chain, handle Blogger's broken HTML

Blogger HTML is often malformed (unclosed tags, nested divs, `<br/>` instead of `<br>`). A regex chain with `html.unescape()` is more robust than a proper parser for this:

```python
import html, re

def html_to_markdown(html_content):
    text = html.unescape(html_content)
    # Strip Blogger/WordPress artifacts
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<p[^>]*>', '\n\n', text)
    text = re.sub(r'</p>', '', text)
    text = re.sub(r'<h2[^>]*>', '\n\n### ', text, flags=re.IGNORECASE)
    text = re.sub(r'</h2>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<a[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', r'[\2](\1)', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<[^>]+>', '', text)  # strip remaining tags
    return text.strip()
```

### Slug generation — preserve Chinese characters, STRIP [] brackets

Hugo processes title strings and removes `[]` / `（）` / `「」` bracket markers when generating the URL slug. The slug must match what Hugo produces.

**Correct approach — strip bracket content first, then slugify:**

```python
import re

def strip_brackets(text):
    """Remove all [] and （） bracket markers and their enclosed content."""
    # Remove ASCII [] content
    text = re.sub(r'\[[^\]]*\]', '', text)
    # Remove （） content
    text = re.sub(r'（[^）]*）', '', text)
    return text.strip()

def generate_slug(title):
    cleaned = strip_brackets(title)
    slug = re.sub(r'[^\w\u4e00-\u9fff]+', '-', cleaned)
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-').lower()[:80]
```

**Example:**
- Title: `[推荐]人性的弱点` (after bracket strip: `人性的弱点`)
- Hugo URL slug: `推荐人性的弱点` (no hyphen between "推荐" and "人性")
- Wrong slug (with hyphen): `推荐-人性的弱点` → 404 on GitHub Pages

**Verification after migration:** Run Hugo build, then compare directory names in `public/kindle/posts/` with frontmatter slugs. Any mismatch = slug was generated incorrectly.

### Duplicate detection — compare word overlap

```python
def check_duplicate(title, existing_slugs):
    words = set(re.findall(r'[\w]{2,}', title.lower()))
    for slug in existing_slugs:
        slug_words = set(re.findall(r'[\w]+', slug.lower()))
        if len(words & slug_words) >= 3 and len(words) >= 3:
            return True, slug
    return False, None
```

## Pipeline Steps

```
[1/6] 抓取 Blogger 内容 (Atom feed, paginated)
[2/6] 扫描现有文章 slug (去重)
[3/6] 生成 Hugo 文章文件 (date-slug/index.md)
[4/6] Hugo build 验证
[5/6] 同步 public → repo 根目录 (cp -a)
[6/6] git add / commit / tag / push
```

## Post-Migration Content Deduplication

After importing old articles into the Hugo site as drafts, compare them against existing published articles to decide what to keep.

### Dedup Decision Logic

| Condition | Action |
|-----------|--------|
| Old article has same content as existing new article (different title) | Delete old, keep new (short 7-10 char title) |
| Old article content is genuinely new (new site doesn't cover it) | Keep old article |

### Dedup Workflow

```bash
# 1. List untracked (newly imported) article directories
cd hugo-site/content/posts
git ls-files --others --exclude-standard --directory

# 2. Read titles from old articles
for d in 2011-* 2012-*; do
  [ -d "$d" ] || continue
  title=$(grep -m1 '^title:' "$d/index.md" 2>/dev/null)
  echo "$d|$title"
done

# 3. Read titles from existing (tracked) articles
for f in $(git ls-tree -r HEAD --name-only | grep '/index.md$' | sort); do
  title=$(grep -m1 '^title:' "$f" 2>/dev/null)
  echo "$(dirname $f)|$title"
done

# 4. Search for keyword overlap (unique phrases from old articles in existing site)
#    This identifies content that already exists under a different title.
grep -rl "独特短语" --include='*.md' . | grep -v '2011-\|2012-'

# 5. For potential matches, read both articles and compare content
#    Key signal: existing articles marked "由旧稿整理而来" (rewritten from old drafts)
#    → Check if rewritten versions replaced the old source content.
```

### Category-Specific Comparison

When the old articles and existing site share the same category or series name (e.g. both use `information-judgment` series for 金·判断 content), content overlap is more likely. Focus comparison on:

1. **同系列比较** — identical series name in both old and new articles
2. **同分类比较** — identical categories (e.g. 金·判断 in both old and new)
3. **同主题关键字搜索** — unique topic phrases that appear in both old and new

### Content Signature Comparison

To quickly identify potential duplicates without reading every article:

```python
# Compare article sizes — nearly identical sizes may indicate duplicate content
# Article sizes can also serve as a content "fingerprint"
# Distribution: tiny (<1KB), short (1-5KB), medium (5-20KB), long (>20KB)
# Very different sizes = certainly different content
```

### Common Overlap Patterns in Angelife Migration

| Pattern | Old Article (2011-2012) | Existing New Article | Verdict |
|---------|------------------------|---------------------|---------|
| 反邪教·旧稿改写 | 邪教东方闪电的新动向 (35KB, first-hand account) | 从反邪到反操弄 (3.5KB, framework) | **Keep both** — different content (detail vs framework) |
| 反邪教·家庭修复 | 公益咨询小结 (5.7KB, counseling notes) | 反操弄与家庭 (3.1KB, family guide) | **Keep both** — different content |
| AI/tech | No old equivalent | 2026 articles | **Keep new only** — old site had no AI content |
| New site internal | No old equivalent | workflow logs, CI incidents | **Keep new only** |

### Cleanup

After dedup decision:

```bash
# Remove confirmed-duplicate old articles
rm -rf hugo-site/content/posts/2012-XX-XX-duplicate-slug/

# Remove the draft flag from kept old articles (or leave as draft for review)
# Edit index.md: draft: true → draft: false

# Verify after cleanup: tracked vs untracked counts
git ls-tree -r HEAD --name-only content/posts/ | wc -l
git ls-files --others --exclude-standard content/posts/ | wc -l
```

### Pitfalls

- **"由旧稿整理而来" rewriting ≠ content duplicate** — Rewritten articles (2025+) are short analytical frameworks; the original old articles (2011-2012) are long first-hand accounts with different content. Both have independent value.
- **Same series name ≠ same content** — Both old and new articles may use the `information-judgment` series but cover different topics.
- **Draft status check** — Kept old articles stay as `draft: true` until user confirms publication. Don't auto-publish.
- **Git status won't show untracked count** — `git status --short` only shows tracked file changes, not untracked count. Use `git ls-files --others` for untracked inventory.

## Known Limitations

- Images referenced in Blogger posts (external URLs like `img3.douban.com`) are NOT downloaded — image links remain as URLs in Markdown
- Complex tables are converted to plain pipe-syntax Markdown (table HTML → `| col | col |` rows), not full Markdown tables
- `<embed>` and `<object>` for video/audio become plain links
- Posts with only `title` (no content) produce empty articles — acceptable for migration completeness