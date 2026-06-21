# Hugo Section vs Taxonomy URL Conflict

## The Problem

When you register a taxonomy in `hugo.toml`:
```toml
[taxonomies]
  series = "series"
```

And you have posts with `series: ["信息判断"]` frontmatter...

But the series taxonomy pages (e.g., `/series/信息判断/`) show **zero posts** even though posts have matching frontmatter.

## Root Cause

Hugo uses a **single URL namespace** for both:
- **Section**: directory-based page tree (`content/series/_index.md` → `/series/`)
- **Taxonomy**: taxonomy term pages (`/series/信息判断/`)

When both exist, Hugo resolves `/series/` to the Section, and the taxonomy term pages at `/series/<term>/` are shadowed.

## Diagnosis

```bash
# Check if content/series/ exists (Section interference)
ls content/series/

# Check taxonomy registration in hugo.toml
grep -A2 'taxonomies' hugo.toml

# Check if series taxonomy pages are generating at all
ls public/series/ 2>/dev/null || echo "No series taxonomy output"
```

## Solution: Rename Section Directory

### Step 1: Rename the content directory

```bash
git mv content/series content/columns
```

### Step 2: Update hugo.toml menu URLs

Before:
```toml
[[menu.main]]
  url = "/series/information-judgment/"
```

After:
```toml
[[menu.main]]
  url = "/columns/information-judgment/"
```

Also update `mainSections`:
```toml
mainSections = ["columns", "posts"]
```

### Step 3: Clear column _index.md descriptions

Each column's `_index.md` may have `description:` or `summary:` that pollutes list pages. Clear them:
```yaml
---
title: "金·判断"
description: ""
---
```

### Step 4: Create custom `layouts/columns/list.html`

PaperMod's default Section list only shows sub-pages of the Section directory (e.g., `content/columns/information-judgment/index.md`). It does **not** show posts with matching `series` frontmatter.

The custom template must:
1. Iterate ALL `site.Pages` of type `posts`
2. Filter where `Params.series` contains the current section's title
3. Sort by date

```go
{{- define "main" -}}
{{- $sectionName := .Title -}}
{{- $matched := slice -}}

{{- range site.Pages -}}
  {{- if and (eq .Type "posts") .Params.series -}}
    {{- $s := .Params.series -}}
    {{- if in $s $sectionName -}}
      {{- $matched = $matched | append . -}}
    {{- end -}}
  {{- end -}}
{{- end -}}

{{- $sorted := sort $matched "Date" -}}
{{- range $sorted -}}
  <article class="post-entry">
    <h2><a href="{{ .RelPermalink }}">{{ .Title }}</a></h2>
    <time>{{ .Date.Format "2006-01-02" }}</time>
  </article>
{{- end -}}
{{- end -}}
```

### Step 5: Git commit the rename

```bash
git add content/columns/ hugo.toml layouts/columns/list.html
git commit -m "v0.7.17: resolve series Section/Taxonomy URL conflict

- Rename content/series/ → content/columns/
- Update menu URLs from /series/* to /columns/*
- Add custom columns/list.html to aggregate posts by series frontmatter"
git tag v0.7.17
git push origin master
git push origin v0.7.17
```

## Key Points

| Concept | Detail |
|---------|--------|
| `series` frontmatter format | Always a **list**: `series: ["信息判断"]` |
| `in $s $sectionName` | List membership check, not string equality |
| `sort $matched "Date"` | Ascending (oldest first) — Hugo has no reverse sort method |
| Section directory title | Matches taxonomy term name for `in` check to work |
| Column sub-pages | Can exist at `content/columns/<slug>/index.md` as "featured" list entry |

## Related Incidents

- **v0.7.17**: 83 posts (42+20+1+9+11 across 5 columns) were showing 0 on `/columns/` pages until this pattern was identified and fixed.