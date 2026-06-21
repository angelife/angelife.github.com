# Disabled Workflow Debug (v0.7.18 incident)

## Problem

GitHub Pages stopped generating Hugo taxonomy pages (e.g. `/series/信息判断/` → 404) even though:
- Local Hugo build generates them correctly (247 pages)
- GitHub Actions reports `success` for the commit
- English slug pages work (`/series/information-judgment/` → 200)
- Chinese taxonomy pages 404 on live site

## Root Cause

The `.github/workflows/hugo.yml` was moved/disabled at some point:

```
.repo/
  .github/workflows/hugo.yml           ← MISSING (was removed/moved)
  docs/disabled-workflows/hugo.yml.disabled  ← workflow file here but INACTIVE
```

GitHub Actions still shows "pages build and deployment | success" because GitHub Pages has a built-in Hugo runner that activates when it detects a Hugo site. However, this fallback runner:
1. May not load PaperMod submodule correctly
2. May use a different Hugo version than specified in the disabled workflow
3. May not generate Chinese taxonomy URLs the same way

## Diagnosis Commands

```bash
# Check if workflows directory exists at repo root
ls -la /repo/.github/workflows/

# List actual workflows in GitHub
curl -s "https://api.github.com/repos/angelife/angelife.github.com/actions/workflows" \
  -H "Accept: application/vnd.github+json" | python3 -c "import sys,json; [print(w['path'], w['name']) for w in json.load(sys.stdin).get('workflows',[])]"

# Check the disabled workflow content
cat /repo/docs/disabled-workflows/hugo.yml.disabled | head -30
```

## The Working Workflow (from docs/disabled-workflows/)

```yaml
name: Deploy Hugo site
on:
  push:
    branches: [master]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: recursive   # ← CRITICAL: loads PaperMod submodule

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v3
        with:
          hugo-version: '0.147.4'  # matches local v0.147.0
          extended: true

      - name: Build
        working-directory: hugo-site
        run: hugo --cleanDestinationDir --minify

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: hugo-site/public

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v4
```

## Fix Required

1. Copy `docs/disabled-workflows/hugo.yml.disabled` → `.github/workflows/hugo.yml` at repo root
2. Commit and push
3. Wait ~2-3 min for Actions to run
4. Verify: `curl -I "https://angelife.github.io/series/信息判断/" -m 15` → 200

## Verification After Fix

```bash
# Should show: .github/workflows/hugo.yml
ls -la /repo/.github/workflows/

# Actions API should show hugo.yml workflow
curl -s "https://api.github.com/repos/angelife/angelife.github.com/actions/workflows" \
  -H "Accept: application/vnd.github+json" | python3 -c \
  "import sys,json; [print(w['path'], w['state']) for w in json.load(sys.stdin).get('workflow_runs',[])]"

# Target taxonomy pages should be 200
curl -s -o /dev/null -w "%{http_code}\n" "https://angelife.github.io/series/信息判断/" -m 15
curl -s -o /dev/null -w "%{http_code}\n" "https://angelife.github.io/series/蝉识录/" -m 15
curl -s -o /dev/null -w "%{http_code}\n" "https://angelife.github.io/series/易理笔记/" -m 15
```