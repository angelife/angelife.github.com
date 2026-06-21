# Chinese Filename GitHub Push Failure (v0.7.19)

## Symptom

Files with Chinese characters in their names pass `git commit` successfully and appear in `git ls-tree HEAD`, but GitHub's raw content URL returns HTTP 404. ASCII-named files pushed in the same commit work correctly.

## Reproduction

```bash
# Push succeeds (git says "Everything up-to-date" or "push successful"):
git add hugo-site/content/series/information-judgment/
git commit -m "add chinese-named files"
git push origin master

# But GitHub raw URL fails:
curl -sI "https://raw.githubusercontent.com/angelife/angelife.github.com/master/hugo-site/content/series/information-judgment/2011-10-16-%E5%85%AC%E7%9B%8A%E5%92%A8%E8%AE%AF%E5%B0%8F%E7%BB%93.md"
# → HTTP/2 404

# ASCII-named file in same directory works:
curl -sI "https://raw.githubusercontent.com/angelife/angelife.github.com/master/hugo-site/content/series/information-judgment/test-marker.md"
# → HTTP/2 200
```

## Verification Commands

```bash
# 1. Check if file is in git HEAD:
git ls-tree -r --name-only HEAD | grep "公益咨询小结"

# 2. Check GitHub API for directory contents:
curl -s "https://api.github.com/repos/angelife/angelife.github.com/contents/hugo-site/content/series/information-judgment?ref=master" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Files: {len(d)}')"
# Expected: 46 (or actual count). If only 2 → files missing.

# 3. Check GitHub raw URL:
curl -sI "https://raw.githubusercontent.com/angelife/angelife.github.com/master/path/to/file.md" | head -1
```

## Workaround

Rename files with Chinese characters to pinyin before committing:

```python
# Example renames:
"2011-10-16-公益咨询小结.md" → "2011-10-16-gongyi-zixun-xiaojie.md"
"2011-10-16-改变.md"         → "2011-10-16-gai-bian.md"
```

**Do NOT use automated transliteration that produces double-date prefixes** (e.g. `2012-02-09-2012-02-09---19.md.md`). Always use explicit pinyin mapping.

## Root Cause

GitHub's raw content CDN does not handle URL-encoded Chinese characters in file paths consistently. The files exist in the git repository (git ls-tree confirms this) but the raw content endpoint returns 404 for Chinese-named files.

## Impact

- Hugo build on GitHub Actions cannot access Chinese-named content files
- Section pages show fewer articles than expected (only ASCII-named files are processed)
- The bug affects all Chinese-named files pushed to GitHub via git

## Status

**Unresolved as of v0.7.19.** GitHub raw content CDN does not serve Chinese-named files. Rename is the only reliable workaround.