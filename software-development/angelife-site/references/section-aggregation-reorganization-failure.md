# Section Aggregation Reorganization Failure

> ⚠️ **v0.7.20 update**: Moving posts to series directory does NOT work as a content reorganization strategy. This file explains why AND documents the organize script's `.md.md` side-effect discovered during the 46-article migration.

## Why Moving Posts to Series Directory Fails

Hugo section pages (`list.html`) only show `.md` files **directly in the section root directory**.

- `content/series/information-judgment/` — section root
- `content/series/information-judgment/subdir/` — NOT listed in section page
- `content/series/information-judgment/2011-10-16-xxx.md` — IS listed

Files in subdirectories are invisible to the section's list page, regardless of frontmatter.

**Do not reorganize content by moving files into subdirectories.** The correct approach is either:
1. Keep files at section root with correct frontmatter
2. Use taxonomy-based aggregation (separate from section pages)

## The organize Script's `.md.md` Side-Effect

When the organize script processes entry names that already end in `.md` (e.g., `"历史轨迹-二千年教会史续7.md"`), it appends `.md` to create the filename, producing `xxx.md.md`.

### Symptom

After running the organize script:
```
content/series/chan-shi-lu/2012-02-09-历史的轨迹-二千年教会史-续7.md       # clean, correct
content/series/chan-shi-lu/2012-02-09-2012-02-09---7.md.md                  # malformed duplicate
```

Both files exist with **identical content** (MD5 hash: `2e7e7917849814c28467a546d642c150`).

### Impact

- `.md.md` files are valid markdown and may be committed to git
- Hugo parses behavior is undefined for `.md.md` extension
- Pollutes the section listing with duplicate entries
- Increases build artifact size

### Fix

```bash
# Delete all .md.md files (they are duplicates of the clean-named version)
find hugo-site/content/series -name "*.md.md" -delete

# Also delete other malformed double-date filenames
find hugo-site/content/series -name "2012-02-09-2012-02-09*" -delete
find hugo-site/content/series -name "2012-06-25-2012-06-25*" -delete
```

### Verification

```bash
# Confirm no .md.md files remain
find hugo-site/content/series -name "*.md.md" | wc -l
# Must be 0

# Verify clean file counts per section
for d in content/series/*/; do
  echo "$(ls "$d"*.md 2>/dev/null | wc -l) $d"
done
```

## The Git Tree vs Working Directory Divergence (v0.7.20 Critical Finding)

**Most dangerous trap in batch file operations:**

1. Organize script creates 80 new files
2. `git add -A` is run — it reports success but only adds 6 files (Chinese filename pipe failure)
3. `git commit` is run — it succeeds with SHA
4. `git status --short` shows **clean** (no tracked changes)
5. CI builds — only 2 articles appear (not 46)

**Root cause:** `git status --short` shows **tracked file changes only**. The 80 untracked files are invisible to `--short` output. The commit's git tree only contains the 6 files that were successfully added.

**Diagnosis:**
```bash
# Compare git tree file count vs local
git ls-tree -r HEAD -- hugo-site/content/series/information-judgment | grep "\.md$" | wc -l
ls hugo-site/content/series/information-judgment/*.md | wc -l
# Mismatch = files not in commit

# Check untracked
git status --short -uall | grep -c "series"
# > 0 = untracked files exist
```

**Prevention:** After any batch file operation + `git add`, always verify `git ls-tree` counts before assuming the commit is complete.