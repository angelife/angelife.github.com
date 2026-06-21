# 五行分类系统 — Five-Element Category Reference

The site's five-element (五行) classification system. Every article migrated from Blogger must be assigned exactly one 五行 category.

## 五行 Category Map

| 五行 | 含义 | 包含主题 |
|------|------|---------|
| 金·判断 | Discernment, judgment, critical analysis | 心理学、哲学、方法、社会、杂文、经验、推荐、笔记、感言、病症、分析、志愿服务（非历史类） |
| 木·蝉识 | Recorded knowledge, history, systematic learning | 教会史、个人知识资产 |
| 水·易理 | Change, transformation, patterns | 易理 |
| 火·AI | Technology, automation, AI-era topics | AI时代、一人公司、系统主控 |
| 土·正见 | Correct view, faith, foundation | 信仰、反民粹与反邪、儒家与正见 |

## Reclassification Script

When articles need reclassification (e.g., after migrating from old Blogger categories):

```python
import re
from pathlib import Path

OLD_TO_WUXING = {
    '信仰': '土·正见',
    '教会史': '木·蝉识',
    '志愿服务': '金·判断',
    '心理学': '金·判断',
    '哲学': '金·判断',
    '方法': '金·判断',
    '社会': '金·判断',
    '杂文': '金·判断',
    '经验': '金·判断',
    '推荐': '金·判断',
    '笔记': '金·判断',
    '感言': '金·判断',
    '病症': '金·判断',
    '分析': '金·判断',
    'AI时代': '火·AI',
    '一人公司': '火·AI',
    '系统主控': '火·AI',
    '反民粹与反邪': '土·正见',
    '个人知识资产': '木·蝉识',
}

WUXING_SET = {'金·判断', '木·蝉识', '水·易理', '火·AI', '土·正见'}

for post_dir in Path('/repo/hugo-site/content/posts').iterdir():
    if not post_dir.is_dir(): continue
    idx = post_dir / 'index.md'
    if not idx.exists(): continue
    c = idx.read_text(encoding='utf-8')
    cats_m = re.search(r'^categories:\s*\n((?:\s*-\s*[^\n]+\n)*)', c, re.MULTILINE)
    if not cats_m: continue
    cats = re.findall(r'^\s*-\s*"([^"]+)"', cats_m.group(1))

    # Find target
    target = None
    for old, new in OLD_TO_WUXING.items():
        if old in cats:
            target = new
            break
    if not target: continue

    # Replace old cats with target 五行 (keep non-old, non-五行 cats)
    keep = [x for x in cats if x not in set(OLD_TO_WUXING.keys()) and x not in WUXING_SET]
    keep.append(target)

    new_c = re.sub(
        r'^categories:\s*\n((?:\s*-\s*[^\n]+\n)*)',
        'categories:\n' + '\n'.join(f'  - "{cat}"' for cat in keep) + '\n',
        c, count=1, flags=re.MULTILINE
    )
    idx.write_text(new_c, encoding='utf-8')
```

## URL Behavior

- 五行 category names with `·` (middle dot) get URL-encoded: `金·判断` → `/categories/金判断/` (middle dot removed by URL normalization)
- The Hugo `categories/` directory uses URL-safe names: `categories/金判断/`, `categories/木蝉识/`, etc.
- Hugo build generates `public/categories/` with the URL-safe names
- The middle dot is cosmetic in the UI but not in URLs — this is expected behavior

## Verification

After reclassification:
```bash
cd /repo/hugo-site && /opt/data/hugo
ls public/categories/  # should show: 金判断, 木蝉识, 土正见, 火ai, 易理
for cat in 金判断 木蝉识 土正见 火ai 易理; do
  count=$(grep -c 'article' "public/categories/$cat/index.html")
  echo "$cat: $count articles"
done
```

Also verify all articles have a 五行 category:
```python
import re
from pathlib import Path
WUXING = {'金·判断', '木·蝉识', '水·易理', '火·AI', '土·正见'}
for post_dir in Path('/repo/hugo-site/content/posts').iterdir():
    if not post_dir.is_dir(): continue
    idx = post_dir / 'index.md'
    if not idx.exists(): continue
    c = idx.read_text(encoding='utf-8')
    cats_m = re.search(r'^categories:\s*\n((?:\s*-\s*[^\n]+\n)*)', c, re.MULTILINE)
    if not cats_m: continue
    cats = re.findall(r'^\s*-\s*"([^"]+)"', cats_m.group(1))
    if not any(w in cats for w in WUXING):
        print(f"MISSING 五行: {cats}")
```