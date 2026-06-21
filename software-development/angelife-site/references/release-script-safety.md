# Release Script Safety Rules — Quick Reference

> Condensed from `/repo/RELEASE_SCRIPT_SAFETY_RULES.md`. For full version including crash recovery SOP, see the source file.

## NUL-Safe Git Add (v0.6.41 — MANDATORY)

Chinese paths break when passed through shell pipes. This is the **root cause of v0.6.40 release failure**.

### ❌ WRONG — breaks Chinese/special-character paths

```bash
# All of these break on Chinese characters:
git status --short | awk '{print $2}' | while read f; do git add "$f"; done
git diff --name-only | while read f; do git add "$f"; done
git status | grep '^??' | cut -d' ' -f2 | while read f; do git add "$f"; done
```

### ✅ CORRECT — NUL-safe

```bash
# For tracked modified files:
git diff --name-only -z | while IFS= read -r -d '' file; do
    git add -- "$file"
done

# For untracked files:
git ls-files -z --others --exclude-standard | while IFS= read -r -d '' file; do
    [[ "$file" != "_incoming/"* && "$file" != ".reasonix/"* ]] && git add -- "$file"
done
```

## rsync Silent Logging (v0.6.41 — MANDATORY)

### ❌ WRONG — floods terminal/Telegram, causes crash

```bash
rsync -av hugo-site/public/ ./
```

### ✅ CORRECT — log to file

```bash
RSYNC_LOG="/tmp/angelife-release-rsync-${VERSION}.log"
mkdir -p "$(dirname "$RSYNC_LOG")"
rsync -a --delete hugo-site/public/ ./ > "$RSYNC_LOG" 2>&1
echo "rsync log: $RSYNC_LOG"
```

## Crash Recovery (v0.6.41)

If release script crashes mid-run, **do NOT blindly re-run**. Check state first:

```bash
# Step 1: What happened?
git status -sb

# Step 2: Any staged but uncommitted files?
git diff --cached --name-only

# Step 3: Last commit?
git log -1 --oneline

# Step 4: Tag pointing to current commit?
git rev-parse v0.6.XX^{commit}  # compare with HEAD
```

## tag-already-exists Rules

| Situation | Action |
|-----------|--------|
| Same version, same commit | `Everything up-to-date` — skip tag |
| Same version, different commit | Force tag after confirming |
| Different version | Normal create |

## Everything up-to-date Rule

If `git push` returns "Everything up-to-date": the remote already has this commit. Do not re-run anything. The previous release succeeded.