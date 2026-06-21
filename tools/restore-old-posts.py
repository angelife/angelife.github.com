#!/usr/bin/env python3
"""Restore 70 historical posts from git commit fd8c614 into current working tree.
Removes missing cover references, keeps categories/series/tags from the last known good state.
"""
import os
import subprocess
import re
import sys

GIT_DIR = "/workspace/angelife.github.com"
SOURCE_COMMIT = "fd8c614"

def git_list_files(commit):
    """List all files at a commit. Returns list of paths (may be quoted octal-encoded)."""
    r = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", commit],
        capture_output=True, text=True, cwd=GIT_DIR
    )
    return [l for l in r.stdout.split("\n") if l.strip()]

def git_show_content(commit, filepath):
    """Get file content at a commit."""
    r = subprocess.run(
        ["git", "show", f"{commit}:{filepath}"],
        capture_output=True, text=True, cwd=GIT_DIR
    )
    if r.returncode != 0:
        # Try with quoted path
        r = subprocess.run(
            ["git", "show", f'{commit}:"{filepath}"'],
            capture_output=True, text=True, cwd=GIT_DIR
        )
    return r.stdout

def remove_cover_refs(content):
    """Remove cover block from frontmatter."""
    content = re.sub(r'cover:\n  image:.*?\n  alt:.*?\n', '', content, count=1)
    # Also handle cover without alt
    content = re.sub(r'cover:\n  image:.*?\n', '', content, count=1)
    return content

def set_draft_true(content):
    """Set draft: true in frontmatter."""
    content = content.replace('draft: false', 'draft: true', 1)
    return content

def clean_path(p):
    """Remove surrounding quotes from path if present."""
    p = p.strip()
    if p.startswith('"') and p.endswith('"'):
        p = p[1:-1]
        # Decode octal escape sequences
        p = p.encode('ascii').decode('unicode-escape')
    return p

def main():
    all_files = git_list_files(SOURCE_COMMIT)
    
    # Find old post index.md files (2011-2014, not the 2014 reference posts)
    old_mds = []
    for f in all_files:
        cleaned = clean_path(f)
        if cleaned.endswith('/index.md') and 'content/posts/' in cleaned:
            # Extract the post directory name
            parts = cleaned.split('/')
            # Find the actual post directory name in the path
            post_dir = None
            for i, p in enumerate(parts):
                if p == 'posts' and i+1 < len(parts):
                    post_dir = parts[i+1]
                    break
            if post_dir and (post_dir.startswith('2011-') or post_dir.startswith('2012-')):
                if '2014-04-13-reference' not in cleaned and '2014-04-16-ref2' not in cleaned:
                    old_mds.append((cleaned, f))
    
    print(f"Found {len(old_mds)} old article files to restore", flush=True)
    
    restored = 0
    skipped = 0
    failed = 0
    
    for cleaned_path, raw_path in sorted(old_mds):
        target = os.path.join(GIT_DIR, cleaned_path)
        
        if os.path.exists(target):
            skipped += 1
            continue
        
        content = git_show_content(SOURCE_COMMIT, raw_path)
        if not content:
            failed += 1
            print(f"  FAIL (no content): {cleaned_path[:60]}...", flush=True)
            continue
        
        os.makedirs(os.path.dirname(target), exist_ok=True)
        
        content = remove_cover_refs(content)
        content = set_draft_true(content)
        
        with open(target, 'w', encoding='utf-8') as f:
            f.write(content)
        
        restored += 1
        name = os.path.basename(os.path.dirname(cleaned_path))
        print(f"  OK: {name}", flush=True)
    
    print(f"\n=== Summary ===", flush=True)
    print(f"Restored: {restored}", flush=True)
    print(f"Skipped (already exist): {skipped}", flush=True)
    print(f"Failed: {failed}", flush=True)

if __name__ == "__main__":
    main()
