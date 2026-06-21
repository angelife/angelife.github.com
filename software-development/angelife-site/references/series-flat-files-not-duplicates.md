# series/ Flat Files Are NOT Duplicates — Content Recovery Log (v0.7.21)

## Incident Summary

During a "cleanup" operation meant to remove duplicate flat files from `content/series/`, the organize script's `find content/series -name '*.md' -not -name '_index.md' -delete` command deleted **173 primary article files**. The operation was based on the false assumption that `content/series/SLUG/*.md` files were duplicates of `content/posts/SLUG/index.md` files.

They are not duplicates. They are DIFFERENT content.

## The False Assumption

**What was believed:** `content/posts/SLUG/index.md` = article source, `content/series/SLUG/*.md` = flat copy. Cleanup = safe.

**What is actually true:** The two directories contain DIFFERENT articles:

| Directory | Content | Role |
|---|---|---|
| `content/posts/<slug>/index.md` | Blogger-era migrated posts (82 subdirs) | Historical content |
| `content/series/<slug>/*.md` | Primary articles organized by 五行 taxonomy (173 flat files) | PRIMARY article source |

After `git checkout 437b9be -- content/series/`, the recovered content:
- `information-judgment/`: 96 `.md` files (2011-2014 Blogger-era articles)
- `chan-shi-lu/`: 46 `.md` files
- `confucian-framework/`: 20 `.md` files
- `ai-bu-yin/`: 12 `.md` files
- `yi-notes/`: 2 `.md` files
- `anti-populism/`: 3 `.md` files

These are original, irreplaceable articles — NOT duplicates of posts/.

## The Organize Script Behavior

The organize script (commit `7b71242`) copied posts from `content/posts/` to `content/series/SLUG/` flat files AND created additional structure in series/. Over time it generated:
- `.md.md` double-extension files (corrupted filenames, safe to delete)
- Flat `.md` files that are primary articles (MUST keep)

## Recovery Command

```bash
git checkout 437b9be -- content/series/
```

Where `437b9be` = the last commit before the organize script's cleanup operation removed the original files.

## Verification After Recovery

```bash
# Count recovered files per taxonomy
for d in content/series/*/; do
  echo "$(basename $d): $(ls "$d" | wc -l) files"
done

# Expected output (after recovery):
# information-judgment: 96+ files
# chan-shi-lu: 46 files
# confucian-framework: 20 files
# ai-bu-yin: 12 files
# yi-notes: 2 files
# anti-populism: 3 files
```

## Lessons Learned

1. **Never delete content without MD5 comparison.** Before any bulk delete of "duplicate" files, compare content hashes. Files with identical hashes are duplicates — files with different content are distinct.

2. **The organize script created dual content structures.** Both `posts/` subdirectories AND `series/` flat files contain original content. They are not redundant — they represent different organizational views of different content.

3. **Git history is not a backup.** While `git checkout <old-commit> -- path` can recover deleted files, it recovers the state at that commit — which may be before later improvements. The safest approach is to verify content before deleting anything.

4. **The cleanup criteria "same MD5 = duplicate" was applied incorrectly.** The `.md.md` files (31 of them) had identical MD5 to clean-named counterparts — those WERE safe to delete. The regular `.md` files had different content and MUST NOT be deleted.

## v0.7.22 Addendum: MD5-Identical Slug + Chinese Filename Pairs

After restoring the 173 flat files (v0.7.21), a second organize script artifact was discovered: **paired files with slug and Chinese filenames, sharing identical content (same MD5)**.

Example pair:
```
2012-02-09-wangshi-meifa-...md    (slug version)
2012-02-09-王石没法跟乔布斯比...md  (Chinese version)
MD5: identical
```

Hugo treats both as separate articles → taxonomy counts inflated (94→44 after cleanup).

**Verification:**
```bash
cd /repo/hugo-site/content/series
for dir in */; do
  cd "$dir"
  md5sum *.md 2>/dev/null | sort -k1,1 | uniq -w32 --all-repeated=separate | grep -v '^$' | head -20
  cd ..
done
```

**Result (v0.7.22):** 75 duplicate files removed across 5 taxonomies → Pages 403→328.

## v0.7.22 Critical Addendum: Slug Sharing Between series/ and posts/ Is NOT a Hugo Conflict

### The Incident (v0.7.22 session)

During a \"slug conflict cleanup\", a scan revealed that ALL 42 files in `content/series/information-judgment/` shared their `slug:` value with a file in `content/posts/`. The same pattern appeared across all taxonomies:

| Taxonomy | Slug conflicts found |
|----------|---------------------|
| information-judgment | 42 |
| chan-shi-lu | 20 |
| ai-bu-yin | 9 |
| confucian-framework | 10 |
| **Total** | **81** |

**Initial false conclusion:** These 81 files are duplicates. Delete the series/ versions, keep posts/.

**This conclusion is WRONG.** Deleting them caused taxonomy page article counts to drop from 44→2 (verified locally).

### Why Slug Sharing Is NOT a Conflict

In Hugo, `slug:` controls the article's URL path, not its identity. When the same slug appears in DIFFERENT Hugo sections:

| File | Section | URL generated |
|------|---------|---------------|
| `content/posts/wangshi-.../index.md` | posts | `https://site/posts/wangshi-.../` |
| `content/series/information-judgment/wangshi-....md` | series | `https://site/series/wangshi-.../` |

**Hugo treats them as completely different articles.** They have different `permalink` values, different `section` values, and appear in different URL namespaces. They do NOT overwrite each other.

### What Controls Taxonomy Pages

**Key architectural fact:** Hugo builds taxonomy pages by scanning all sections (posts/, series/, etc.) for articles whose `series: [...]` front matter matches the taxonomy term. Both the series/ flat file AND the posts/ subdirectory file can contribute to the same taxonomy page — but as distinct, non-conflicting entries.

The **series/ flat files ARE the primary content source** for the taxonomy pages. They contain:
- `series: ["information-judgment"]` front matter
- Full article body content
- Organized under the taxonomy directory structure

The posts/ subdirectory files are separate articles (often Blogger-era migrated content) that share some thematic classification but are structurally independent.

### Verification: Taxonomy Page Rendering Source

```bash
# After deleting all 81 series/ flat files (WRONG):
cd /repo/hugo-site
/tmp/hugo --cleanDestinationDir --minify 2>/dev/null
grep -c 'post-entry' public/series/information-judgment/index.html
# → Returns 4 (= 2 articles, each appearing 2x in HTML)

# With series/ flat files restored (CORRECT):
grep -c 'post-entry' public/series/information-judgment/index.html
# → Returns 10 (= 5 articles on first page, rest paginated)
```

### Lesson

**Never delete series/ flat files because they share slug values with posts/ subdirectories.** In Hugo, slug is scoped to section+URL, not globally unique. The test is not "same slug" but "same Hugo section AND same slug." Only files in the same Hugo section with the same slug truly conflict.

**Correct deduplication check:** Use MD5 content hash comparison, not slug comparison. Files with identical content (identical MD5) in the same directory are duplicates — delete one. Files with different content, even with identical slug values, are distinct articles — keep both.

### Recovery After Wrong Deletion

```bash
# Restore from pre-deletion commit (e.g. d773538):
git checkout d773538 -- hugo-site/content/series/

# Then re-delete only true duplicates (MD5-identical pairs in same dir):
# Keep the slug-version, delete the Chinese-version
```