# Hugo Template Override Pitfalls (Angelife Site)

## Pitfall 1: `baseof.html` with `{{ block }}` blocks all `{{ define }}` overrides

**Symptom:** You create `layouts/_default/single.html` with `{{ define "main" }}` or override PaperMod's `single.html`, but Hugo never uses your override. A test marker `<!-- TEST -->` added to your `single.html` never appears in the built output.

**Root cause:** When a custom `baseof.html` exists in `layouts/_default/` and uses `{{ block "main" . }}{{ end }}`, it defines its own block rendering context. Hugo's template lookup then finds the custom `baseof.html` first and uses it exclusively — it never searches for `{{ define "main" }}` blocks in `layouts/_default/single.html` because the block system requires a matching `{{ template }}` call, not a `{{ define }}` block.

**Diagnosis:**
```bash
# Check if baseof.html exists in your layouts override
ls layouts/_default/baseof.html

# Add a unique marker to YOUR single.html
echo "<!-- TEST-UNIQUE-MARKER-123 -->" >> layouts/_default/single.html
hugo
grep "TEST-UNIQUE-MARKER" public/posts/some-article/index.html
# If marker doesn't appear → baseof.html is blocking the override
```

**Three valid fix approaches (in order of preference):**

### Fix A: Delete the custom `baseof.html` (RECOMMENDED)
The simplest fix. Remove `layouts/_default/baseof.html` entirely and let Hugo use the theme's `baseof.html`. Then your `layouts/_default/single.html` (with `{{ define "main" }}`) will work normally.

```bash
rm layouts/_default/baseof.html
hugo
# Verify: grep "YOUR-MARKER" public/posts/some-article/index.html
```

### Fix B: Modify theme template files directly
If you can't delete `baseof.html` (e.g., it has custom Kindle detection logic you need to keep), modify the theme's `single.html` directly:

```bash
# Copy theme single to layouts override first
cp themes/PaperMod/layouts/_default/single.html layouts/_default/single.html
# Then modify the copy at layouts/_default/single.html
# But this requires Fix A to actually work (see above)
```

### Fix C: Modify theme template files in place (ONLY if A and B fail)
Only for changes that must survive `baseof.html` blocking — like injecting source links. Edit directly in `themes/PaperMod/layouts/_default/`:

```bash
# This bypasses the override system entirely
# Use when template-based approaches don't work
patch themes/PaperMod/layouts/_default/single.html << 'EOF'
...patch content...
EOF
hugo
```

### Why template param access sometimes fails

Even when Fix A is applied, `{{ .Param "source.blogger_url" }}` may render nothing while `{{ index .Params "source" }}` works. This is a Hugo template scoping issue with nested param names (containing dots). Use index access as fallback:

```go
{{- with index .Params "source" }}
  {{- with index . "blogger_url" }}
    <a href="{{ . }}">{{ . }}</a>
  {{- end }}
{{- end }}
```

## Pitfall 2: Hugo template debug — always verify output, not just syntax

Hugo's template system is complex. A successful build (0 errors) does NOT guarantee your template override is being used. **Always verify by checking the actual generated HTML**, not just that Hugo didn't error.

```bash
# WRONG: assume template is working because hugo exits 0
hugo && echo "built OK"

# RIGHT: check the actual output
hugo
grep "YOUR-TEST-MARKER" public/posts/some-article/index.html && echo "override is working"
```

## Pitfall 3: GitHub Pages does NOT run Hugo

GitHub Pages serves static files directly from the repo root's `master` branch. It has **no Hugo binary installed**. This has critical consequences:

1. Whatever is in git is what gets served — `public/` is regenerated locally and never in git
2. After `cp -a hugo-site/public/. /repo/`, the new files are in the filesystem but not in git yet
3. `git add <specific files>` — NOT `git add .` or `git add -u` (misses new directories)
4. Commit and push → GitHub Pages serves the committed files immediately

**Diagnosis for "404 on live site but files exist locally":**
```bash
# 1. Is it in git?
git ls-files path/to/file

# 2. Is it in Hugo's output?
ls hugo-site/public/path/to/file

# 3. If in public/ but not in git → found the issue
git add path/to/file
```

## The Blogger Migration Slug Problem (v0.7.6 incident)

**Problem:** Title `[推荐]人性的弱点` → Hugo slug `推荐人性的弱点` (strips `[]` and joins). Migration script used filename `推荐-人性的弱点` → URL mismatch → 404.

**Rule:** When migrating from Blogger, strip `[]` / `（）` brackets from titles BEFORE generating slug. Test by comparing:

```bash
# What Hugo generates
ls hugo-site/public/kindle/posts/ | grep 推荐

# What frontmatter says
grep "^slug:" hugo-site/content/posts/2012-*/index.md | grep 推荐
```

Fix scripts: `/opt/data/fix_slugs.py` (adds missing slugs), `/opt/data/fix_slug_hyphens.py` (removes incorrect hyphens from bracket-prefixed titles).