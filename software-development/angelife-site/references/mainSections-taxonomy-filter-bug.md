# mainSections Taxonomy Filter — Critical PaperMod Behavior

## What is `mainSections`?

`mainSections` is a Hugo configuration array in `hugo.toml` that tells PaperMod theme which content sections to treat as "primary" for list/taxonomy rendering purposes.

```toml
mainSections = ["columns", "posts", "series"]
```

## The Bug — Posts Invisible to Taxonomy Pages (v0.7.20)

**Symptom:**
- Taxonomy pages (e.g. `/series/information-judgment/`) show **0 posts** despite content existing
- Local Hugo build shows correct post count (42 posts)
- CI rebuild completes successfully but live site still shows 0 posts
- `sitemap.xml` contains only 3 URLs instead of 42+

**Root Cause (discovered 2026-06-02):**
PaperMod's `layouts/_default/taxonomy.html` and `list.html` templates filter pages through `mainSections`. If a section (e.g. `series`) is **NOT** in `mainSections`, all posts in that section are invisible to taxonomy list templates — even though they exist in `content/` and appear in local builds.

This is a **PaperMod theme behavior**, not a Hugo core bug. The theme uses `where .Kind "page"` combined with section filtering.

**Why local build shows correct count:**
- Local Hugo may use a different PaperMod version or configuration
- GitHub Actions CI runner uses Hugo 0.147.4 with strict PaperMod section filtering
- The discrepancy only appears in CI, not always locally

## How to Diagnose

```bash
# 1. Check what's in mainSections
grep -A5 "mainSections" /repo/hugo-site/hugo.toml

# 2. Check if "series" is listed
grep "series" /repo/hugo-site/hugo.toml

# 3. Local build — does it show posts?
cd /repo/hugo-site && /opt/data/hugo
grep -c "information-judgment" public/series/information-judgment/index.html

# 4. CI check — did it rebuild after the fix?
curl -s "https://api.github.com/repos/angelife/angelife.github.com/actions/runs?per_page=1" \
  -H "Accept: application/vnd.github+json" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); r=d['workflow_runs'][0]; print(r['head_sha'], r['status'], r['conclusion'])"

# 5. Live site — does taxonomy page show posts?
curl -s "https://angelife.github.io/series/information-judgment/" | grep -c 'class="post-entry"'
```

## The Fix

```toml
# hugo.toml — ADD "series" to mainSections
mainSections = ["columns", "posts", "series"]
```

**Note:** The order matters. `mainSections` should contain all sections that have taxonomy-tagged content you want to display in list pages.

## Why This Was Hard to Find

1. Local Hugo build showed correct 42 posts — suggested the bug was in CI, not content
2. CI rebuild appeared to succeed (`conclusion: success`) — suggested the problem wasn't build-related
3. GitHub Actions logs showed no errors — PaperMod silently filters, it doesn't error
4. Taxonomy pages returned HTTP 200 (not 404) — suggested content existed but was empty
5. Multiple layers of confusion: Chinese taxonomy values → English slug mismatch, then organize script duplicates, then flat file pollution — each obscured the real `mainSections` root cause

## Related Symptoms That Point to This Bug

| Symptom | Why It Misleads |
|---------|----------------|
| Local build correct, CI wrong | Suggests CI config issue, not content/theme |
| CI says success, live site empty | Hard to distinguish CI failure from content filtering |
| Sitemap has 3 URLs (not 0) | The 3 came from old series/ flat files, not posts/ subdirectories |
| Section page shows 2 posts | PaperMod section list template (`list.html`) is less strict than taxonomy list |

## Prevention

When adding a new content section (e.g., `announcements/`), always add it to `mainSections`:

```toml
mainSections = ["columns", "posts", "series", "announcements"]
```

## GitHub Actions CI Debug Step Pitfall

When adding debug steps to CI workflow that use `grep -c` inside `set -e`:

```yaml
- name: Debug page count
  run: |
    set -e  # This makes grep -c return exit code 1 when count = 0
    COUNT=$(grep -c "information-judgment" public/series/information-judgment/index.html)
    echo "Found $COUNT matches"
```

**Problem:** `grep -c` returns exit code 1 when count is 0. With `set -e`, this terminates the job. If this step is before the deploy step, the deploy is **silently skipped** — no error message, just `skipped` or missing from the workflow run.

**Fix:** Remove `set -e` before debug grep commands, or use `|| true` to suppress non-zero exit codes.