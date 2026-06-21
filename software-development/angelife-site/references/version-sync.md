# Version Sync — Source of Truth

## The Problem

Git tags (`v0.7.13`, `v0.7.14`) do NOT appear on the live site. The version number a visitor sees comes from **Hugo-generated HTML built from source files**.

If the source files say `v0.6.42` and the git tag says `v0.7.14`, the site still shows `v0.6.42`.

## Which Files Contain Hardcoded Version Strings

These are the **only files** that control what version visitors see:

```
hugo-site/content/about/index.md   ← "当前工作流（vX.Y.Z 更新）"
README.md                          ← "当前版本 **vX.Y.Z**"
```

Everything else (changelog.yaml, git tags, commit messages) is for maintainers — not displayed to readers.

## Vault Commit Behavior

vault commits (e.g. `bfb3b60`, `5ab4c9d`) run `hugo build` and commit only the build artifacts to `public/`. They do **NOT** touch source files.

```
vault push:  hugo build → cp public/. /repo/ → git add public/ → commit
NVIDIA:     update source (about/index.md, README.md) → hugo build → git add source → commit → tag → push
```

**Consequence:** If `about/index.md` says `v0.6.42` when vault runs its build, the live site shows `v0.6.42` until someone updates the source.

## Correct Version Update Sequence

When releasing vX.Y.Z:

1. Update `hugo-site/content/about/index.md` → replace `v0.X.Y` with `vX.Y.Z`
2. Update `README.md` → replace `v0.X.Y` with `vX.Y.Z`
3. Run `hugo` in `hugo-site/`
4. Run `cp -a hugo-site/public/. /repo/`
5. `git add hugo-site/content/about/index.md about/ README.md`
6. Commit with message `vX.Y.Z: ...`
7. Tag: `git tag vX.Y.Z`
8. Push both master and tag
9. Verify: `curl -s 'https://angelife.github.io/about/' | grep -i 'vX.Y'`

## Diagnosing Version Mismatch on Live Site

**Symptom:** Live site shows old version, but git tag is new.

```bash
# 1. Check what version the source says
grep -n 'v0\.' hugo-site/content/about/index.md | head -5
grep -n 'v0\.' README.md | head -5

# 2. Check what git tag points to current HEAD
git describe --tags

# 3. Check vault commits — they may have rebuilt on old source
git log --oneline -10 | grep vault

# 4. Check if source was committed after last vault push
git log --oneline origin/master | head -5

# 5. Verify live site content
curl -s 'https://angelife.github.io/about/' | grep -o 'v0\.[0-9]*\.[0-9]*' | head -3
```

**Fix:** Update the source files (about/index.md + README.md) to the correct version, rebuild, commit, push.

## Historical Incidents

- v0.7.13 tag was pushed but live site showed v0.6.42 → about/index.md still had old version string → fixed by updating source and pushing v0.7.14.