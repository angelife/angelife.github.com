# columns/ vs series/ Slug Conflicts — Chinese Taxonomy Values in Wrong Directory (v0.8.x)

## Pattern Discovered (2026-06-02)

### What was found

`content/columns/<category>/<slug>.md` files were created alongside `content/series/<category>/<slug>.md` files. They share the same `slug:` value but have **different `series:` front matter values**.

### Example (from ai-as-jinyin)

| Location | `series:` value | `slug:` |
|----------|----------------|---------|
| `columns/ai-bu-yin/ai-as-jinyin.md` | `series: ["AI补印"]` | `ai-as-jinyin` |
| `series/ai-bu-yin/ai-as-jinyin.md` | `series: ["ai-bu-yin"]` | `ai-as-jinyin` |

### Why these are NOT true duplicates (but still problematic)

The two files have **different content** (different MD5). The `columns/` version uses Chinese taxonomy values like `series: ["AI补印"]` which does not map to any configured taxonomy in `hugo.toml`:

```toml
[taxonomies]
  series = "series"
  categories = "categories"
  tags = "tags"
```

"AI补印" is not a configured taxonomy term — it maps nowhere. Hugo renders the `series: ["ai-bu-yin"]` taxonomy page from `series/ai-bu-yin/` directory files; the `columns/` file's `series: ["AI补印"]` contributes nothing to any page.

### Decision: Delete columns/ conflicts

If a `columns/<cat>/<slug>.md` file has the same `slug:` as a `series/<cat>/<slug>.md` file:
1. Compare MD5 — if identical, delete the columns/ copy
2. If different content: the `series/` version is the taxonomy source (it has the correct slug-frontmatter pairing). Delete the columns/ copy regardless.

### Batch diagnosis command

```bash
cd /repo/hugo-site
python3 -c "
import os, hashlib, re

def get_fm(path):
    lines = open(path, errors='ignore').read().split('\n')[:50]
    in_fm = False
    fm = {}
    for line in lines:
        stripped = line.strip()
        if stripped == '---':
            in_fm = not in_fm
            continue
        if not in_fm:
            break
        m = re.match(r'^slug:\s*\"([^\"]+)\"', line)
        if m:
            fm['slug'] = m.group(1)
        m = re.match(r'^series:\s*\[([^\]]+)\]', line)
        if m:
            fm['series'] = re.findall(r'\"([^\"]+)\"', m.group(1))
    return fm

# Find slug conflicts between series/ and columns/
series_slugs = {}
cols_slugs = {}

for base, index in [('content/series', series_slugs), ('content/columns', cols_slugs)]:
    for root, dirs, files in os.walk(base):
        for f in files:
            if not f.endswith('.md'):
                continue
            fm = get_fm(os.path.join(root, f))
            if 'slug' in fm:
                index.setdefault(fm['slug'], []).append(os.path.join(root, f))

conflicts = []
for slug, cpaths in cols_slugs.items():
    if slug in series_slugs:
        for cp in cpaths:
            conflicts.append((cp, series_slugs[slug][0], slug))

for cp, sp, slug in conflicts:
    col_md5 = hashlib.md5(open(cp,'rb').read()).hexdigest()
    ser_md5 = hashlib.md5(open(sp,'rb').read()).hexdigest()
    print(f'COLLISION: {cp}')
    print(f'  slug={slug} | columns MD5={col_md5[:8]} | series MD5={ser_md5[:8]}')
"
```

### Safe deletion command (after confirming conflicts)

```bash
cd /repo/hugo-site
# 14 files identified for deletion in v0.8.x:
rm content/columns/chan-shi-lu/jiedan-as-inner-system.md
rm content/columns/chan-shi-lu/from-clever-to-system.md
rm content/columns/chan-shi-lu/yuanying-as-personal-system.md
rm content/columns/chan-shi-lu/boundary-first.md
rm content/columns/chan-shi-lu/ai-era-personal-restart.md
rm content/columns/chan-shi-lu/ai-native-knowledge-system.md
rm content/columns/ai-bu-yin/ai-as-jinyin.md
rm content/columns/ai-bu-yin/kindle-koreader-ai-reading-loop.md
rm content/columns/information-judgment/information-source-slimming.md
rm content/columns/information-judgment/information-quality-framework.md
rm content/columns/confucian-framework/confucianism-as-base-ai-as-use.md
rm content/columns/confucian-framework/right-view-in-complex-age.md
rm content/columns/anti-populism/public-reason-against-manipulation.md
rm content/columns/anti-populism/anti-populism-not-anti-people.md

git add -A && git commit -m "fix(content): remove duplicate series or file for yi-li-bi-ji"
```

## Key Lesson

**Not all MD5-identical files are the problem, and not all MD5-different files are safe.** The columns/ files had different content and different `series:` values. The danger was not that they'd create duplicate taxonomy entries (the wrong `series:` value would prevent that), but that they'd clutter the content tree and cause confusion during future audits. Always check both MD5 AND front matter `series:` value.