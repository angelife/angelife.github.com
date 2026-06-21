# Hugo Build Debug — Docker Bind Mount + hermes User Ownership

## Symptom

New article file created in `/repo/hugo-site/content/posts/<slug>/`:
- File visible on Mac (`ls` shows directory exists)
- Hugo build reports **0 errors** but the article does NOT appear in `public/posts/`
- Result: HTTP 404 on the live site

## Root Cause

Docker bind mount uses `rprivate` propagation. Files created by the container's `hermes` user (uid 10000, gid 10000) appear on the Mac host with mismatched ownership — typically showing as `macos:staff` but with **truncated size** (e.g., 96 bytes instead of 5000+ bytes), indicating the Mac kernel cannot read the hermes-owned inode through the bind mount.

Hugo silently skips unreadable files — no error, no warning, article simply disappears.

## Diagnostic Steps

```bash
# Step 1: Check from inside the Docker container — does the file exist and have real size?
docker exec <container> ls -la /repo/hugo-site/content/posts/<slug>/
docker exec <container> wc -c /repo/hugo-site/content/posts/<slug>/index.md

# Step 2: Check from Mac — if size is tiny (< 200 bytes), file is unreadable on host
ls -la /Users/macos/angelife.github.com/hugo-site/content/posts/<slug>/
wc -c /Users/macos/angelife.github.com/hugo-site/content/posts/<slug>/index.md

# Step 3: If Mac shows tiny size — fix ownership on Mac
sudo chown -R macos:staff /Users/macos/angelife.github.com/hugo-site/content/posts/<slug>/
```

## Prevention

- For new articles created by NVIDIA inside the container, Mac user must run `chown` after the file is visible
- Check file size with `wc -c` immediately after creation — healthy article is 2000–8000 bytes
- The problem does NOT affect files created directly on Mac (macos:staff ownership) — only files created by container hermes user

## Why Hugo Is Silent

Hugo calls `os.Open` on the markdown file. If the bind mount renders the file unreadable to the Mac kernel, `Open` returns an error Hugo treats as "skip this file" — not as a build failure. No error in `hugo` output. Check `public/posts/` after every build to confirm expected articles appear.

## Other Articles Build Fine

If two articles build and one doesn't, and the broken one was created most recently by the container user, ownership is the prime suspect. Compare:
```bash
ls -la /Users/macos/angelife.github.com/hugo-site/content/posts/
```
Ownership should be `macos:staff` for all. If one shows `10000` or `hermes`, it's the broken one.

## Fix Verification

After `chown`, re-run Hugo build:
```bash
cd /Users/macos/angelife.github.com
hugo -s hugo-site --gc --cleanDestinationDir --minify
ls public/posts/  # should now include the previously missing article
```