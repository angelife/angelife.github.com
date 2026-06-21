# Hugo-Authoring Pitfalls (Angelife Site)

> Common bugs, edge cases, and process failures specific to this site's Hugo workflow.
> Add entries here when a non-obvious failure mode is discovered during a session.

---

## Pitfall 1: `baseof.html` with `{{ block }}` blocks all `{{ define }}` overrides

**Symptom:** You create `layouts/_default/single.html` with `{{ define "main" }}` or override PaperMod's `single.html`, but Hugo never uses your override. A test marker `<!-- TEST -->` added to your `single.html` never appears in the built output.

**Root cause:** When a custom `baseof.html` exists in `layouts/_default/` and uses `{{ block "main" . }}{{ end }}`, it defines its own block rendering context. Hugo's template lookup then finds the custom `baseof.html` first and uses it exclusively — it never searches for `{{ define "main" }}` blocks in `layouts/_default/single.html`.

**Fix A (recommended):** Delete `layouts/_default/baseof.html` entirely. Let Hugo use the theme's `baseof.html`.

**Fix B:** Modify the theme's `single.html` directly at `themes/PaperMod/layouts/_default/single.html`.

**Diagnosis:**
```bash
echo "<!-- TEST-UNIQUE-123 -->" >> layouts/_default/single.html
hugo && grep "TEST-UNIQUE-123" public/posts/some-article/index.html
# If missing → baseof.html is blocking
```

---

## Pitfall 2: GitHub Pages does NOT run Hugo

GitHub Pages serves static files directly from the repo root's `master` branch — it has **no Hugo binary**. Whatever is in git gets served as-is.

**Consequences:**
- `hugo-site/public/` is regenerated locally each build and is never in git
- `cp -a public/. /repo/` syncs to filesystem but those files aren't in git yet
- `git add .` or `git add -u` can miss new untracked directories — use `git add path/to/dir/` with trailing slash
- A file that exists locally but returns 404 online = not in git (check: `git ls-files path`)

**Diagnosis:**
```bash
# Is it in git?
git ls-files path/to/file

# Is it in Hugo output?
ls hugo-site/public/path/to/file

# In public/ but not in git → add it
git add path/to/file/
```

---

## Pitfall 3: Hugo template debug — verify output, not just exit code

Hugo exits 0 even when your override template is completely ignored. **Always check the generated HTML.**

```bash
# WRONG: assumes working because build succeeded
hugo && echo "built OK"

# RIGHT: check the actual output
hugo
grep "YOUR-TEST-MARKER" public/posts/some-article/index.html && echo "override active"
```

---

## Pitfall 4: The Blogger Migration Slug Problem (v0.7.6 incident)

**Problem:** Title `[推荐]人性的弱点` → Hugo slug `推荐人性的弱点` (strips `[]`). Migration script used filename `推荐-人性的弱点` → URL mismatch → 404.

**Rule:** When migrating from Blogger, strip `[]` / `（）` brackets from titles BEFORE generating slug.

**Fix scripts:** `/opt/data/fix_slugs.py` (adds missing slugs), `/opt/data/fix_slug_hyphens.py` (removes incorrect hyphens from bracket-prefixed titles).

---

## Pitfall 5: Version Numbers in Source Files Don't Auto-Sync (v0.7.14 incident)

**Symptom:** Git tag is `v0.7.13` but `angelife.github.io/about/` still shows `v0.6.42`. The source file `about/index.md` reads `当前工作流（v0.6.42 更新）`.

**Root cause:** `hugo` only regenerates HTML — it does not scan or update version strings embedded in prose. A rebuild from stale source produces fresh HTML with the old version number. When someone commits only the Hugo build output (no source file change), `git add .` picks up nothing for the stale source markdown.

**This happened because:**
- `vault` (Mac) committed a Hugo build at `v0.7.13` tag
- `about/index.md` still contained `v0.6.42` in its prose
- `hugo` rebuilt the same stale source into fresh HTML
- No error, no warning — version silently desynchronized

**Diagnosis:**
```bash
# Check source version
grep -n 'v0\.6\|v0\.7' hugo-site/content/about/index.md | head -5

# Compare with current git tag
git describe --tags

# Disagreement = source is stale
```

**Prevention — pre-tag checklist:**
```bash
# Files that commonly embed version numbers
grep -rn '当前工作流（v0\.' hugo-site/content/
grep -rn 'v0\.6\|v0\.7' hugo-site/content/about/

# If shown version < intended tag → update source first, then rebuild
```

**Fix:** Edit the source file, then `hugo && git add hugo-site/content/about/index.md about/`.

**"vault" commit heuristic:** Commit messages containing "vault" or "Hugo build 产物同步" usually mean only HTML was regenerated — source was not touched. After such a commit at a version tag, always run the diagnosis above to confirm source version is current.

---

## Pitfall 6: buildFuture — Future-Dated Articles Silently Missing

**Symptom:** Article exists with `draft: false`, readable file, correct front matter, but `hugo build` produces 0 new pages and the article never appears in `public/posts/`.

**Root cause:** Hugo does not publish articles with a `date` in the future relative to the build machine clock. No error, no warning — silently excluded.

**Fix in hugo.toml:**
```toml
buildFuture = true
```
Remove it after the article is published, or leave it if regularly scheduling posts ahead.

---

*Maintained by NVIDIA. Add new pitfall entries whenever a non-obvious failure is diagnosed and fixed.*