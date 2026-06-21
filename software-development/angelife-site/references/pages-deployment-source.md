# GitHub Pages Deployment Source — Critical Distinction (v0.7.22+)

## Two Independent Deployment Paths

GitHub Pages has **two separate build systems** that can冲突:

### Path A: GitHub Actions Artifact (what we think we're using)
```
push → Actions workflow → hugo build → upload-pages-artifact → deploy-pages
```
- Our workflow uploads `hugo-site/public/` as a Pages artifact
- `deploy-pages` step deploys that artifact to the CDN edge
- **This is what we control and verify**

### Path B: GitHub Pages Native Build (what Pages actually uses when configured this way)
```
push → GitHub Pages detects source change → Pages own Hugo runner → deploys its own output
```
- Pages reads `hugo-site/content/` directly from the repo
- Runs its own `hugo` command (version may differ from ours)
- Serves its own output at `*.github.io/`
- **We cannot see or verify this build — no artifact, no Actions log**

## How to Check Which Path Is Active

In the repo, go to **Settings → Pages → Source**:

| Source Setting | Deployment Path | Artifact Used? |
|---|---|---|
| **GitHub Actions** | Path A (our workflow) | ✅ Yes — our artifact |
| **Deploy from a branch** (gh-pages or master) | Path B | ❌ No — Pages builds from source |
| **GitHub Actions** with no valid workflow | Path B fallback | ❌ Pages own runner |

## Symptom of Path B Conflict

- Our Actions workflow completes with `success`
- `upload-pages-artifact` step succeeds
- `deploy-pages` step succeeds
- Live site content **never changes** from what Pages built the first time
- Live site serves the same old content (wrong taxonomy count) despite Actions being green
- `_ci_diagnostic.txt` (which we upload to the artifact) returns **404** on the live site
- → Pages is serving its own build, not ours

## Why This Is Hard to Diagnose

1. GitHub Actions UI shows our workflow as `success` — misleading
2. The Pages build doesn't appear anywhere in Actions
3. Pages has its own internal build log (not accessible via API)
4. Pages runner may use different Hugo version, different submodule state

## The Shallow Clone Submodule Problem (Path B consequence)

If GitHub Pages is using Path B (source build), it needs the PaperMod submodule in `themes/PaperMod/`. But:

- Our workflow uses `fetch-depth: 1` (shallow clone)
- GitHub Pages, when building from source, may also do a shallow clone
- Submodule comes in **empty** → PaperMod not loaded → Hugo build generates wrong output

## Verification Checklist

```bash
# 1. Is our workflow actually running?
curl -s "https://api.github.com/repos/angelife/angelife.github.com/actions/runs?per_page=1" \
  -H "Accept: application/vnd.github+json" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); r=d['workflow_runs'][0]; print('SHA:', r['head_sha'][:7], 'Status:', r['status'], 'Conclusion:', r['conclusion'])"

# 2. Is our diagnostic file in the artifact?
curl -s -I "https://angelife.github.io/_ci_diagnostic.txt" -m 10 | head -1
# If 404 → Pages is NOT using our artifact

# 3. What does Pages think it's serving?
curl -s -I "https://angelife.github.io/series/information-judgment/" -m 15 | head -5
# Compare content-length with our local Hugo build
```

## If Path B Is Active — Fix

**Option 1 (Recommended): Switch Pages Source to GitHub Actions**
- Settings → Pages → Source → **GitHub Actions**
- This makes Pages use our Actions artifact (Path A) exclusively

**Option 2: Fix Path B (make Pages own build correct)**
- Ensure `fetch-depth: 0` in workflow AND Pages source build also does full clone
- Ensure submodule is initialized: `git submodule update --init --recursive` in the build step
- This requires understanding what version/args Pages uses internally

## Key Insight

> **Having a valid Actions workflow and valid artifact does NOT guarantee GitHub Pages uses them.**
> Pages may be configured to build from source independently, rendering our entire workflow irrelevant.
> Always check the Pages Source setting first when troubleshooting deployment issues.

This is the root cause of the v0.7.21-22 "44 articles locally but 2 on live site" mystery:
- Our Actions workflow was building correctly (artifact had 328 pages)
- GitHub Pages was configured to build from source (its own Hugo runner, with submodule problems)
- Pages' own build was what actually got served