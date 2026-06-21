#!/usr/bin/env python3
"""
Slug conflict scanner for Hugo series/ vs posts/ directories.

Purpose: Detect whether series/ and posts/ files share the same slug: value.
NOT a deduplication tool — slug sharing between different Hugo sections is
intentional and non-conflicting in Hugo (slug is section-scoped, not global).

Use this to:
1. Audit taxonomy sources (which files contribute to which taxonomy page)
2. Identify genuinely duplicate content (same MD5 in same dir)
3. Verify front matter series: values match URL slugs

Run from hugo-site/ directory.
"""
import os, re, hashlib, sys

def get_slugs_from_dir(base_dir):
    """Return dict: slug -> [list of file paths with that slug]"""
    slugs = {}
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if not f.endswith('.md'):
                continue
            path = os.path.join(root, f)
            try:
                lines = open(path, errors='ignore').read().split('\n')[:30]
            except:
                continue
            slug = None
            for line in lines:
                m = re.match(r'^slug:\s*"?([^"\n]+)"?', line)
                if m:
                    slug = m.group(1).strip()
                    break
            if slug:
                slugs.setdefault(slug, []).append(path)
    return slugs

def md5(path):
    try:
        return hashlib.md5(open(path, 'rb').read()).hexdigest()
    except:
        return ''

def main():
    base = 'content'
    series_base = os.path.join(base, 'series')
    posts_base = os.path.join(base, 'posts')

    if not os.path.exists(series_base):
        print(f"ERROR: {series_base} not found. Run from hugo-site/ directory.")
        sys.exit(1)

    print("=== Slug Conflict Scan: series/ vs posts/ ===\n")

    all_conflicts = {}
    for series_cat in os.listdir(series_base):
        series_path = os.path.join(series_base, series_cat)
        if not os.path.isdir(series_path):
            continue

        series_slugs = get_slugs_from_dir(series_path)
        posts_slugs = get_slugs_from_dir(posts_base) if os.path.exists(posts_base) else {}

        conflicts = []
        for slug, s_paths in series_slugs.items():
            if slug in posts_slugs:
                conflicts.append({
                    'slug': slug,
                    'series_files': s_paths,
                    'posts_files': posts_slugs[slug]
                })

        if conflicts:
            print(f"【{series_cat}】{len(conflicts)} slug-sharing files:")
            for c in conflicts[:5]:
                print(f"  slug={c['slug']}")
                print(f"    series: {c['series_files'][0]}")
                print(f"    posts:  {c['posts_files'][0]}")
            if len(conflicts) > 5:
                print(f"  ... and {len(conflicts)-5} more")
            print()
            all_conflicts[series_cat] = len(conflicts)
        else:
            print(f"【{series_cat}】无 slug 冲突 ✓\n")

    total = sum(all_conflicts.values())
    print(f"=== 总结 ===")
    print(f"Slug 共享总数：{total} (NOT duplicates — Hugo section-scoped slugs)")
    print(f"分类明细：{all_conflicts}")

    # True duplicate check: MD5-identical files in same directory
    print("\n=== MD5 真实重复检查（同一目录内）===\n")
    for series_cat in os.listdir(series_base):
        series_path = os.path.join(series_base, series_cat)
        if not os.path.isdir(series_path):
            continue
        hashes = {}
        for f in os.listdir(series_path):
            if not f.endswith('.md'):
                continue
            path = os.path.join(series_path, f)
            h = md5(path)
            hashes.setdefault(h, []).append(f)
        dups = {h: files for h, files in hashes.items() if len(files) > 1}
        if dups:
            print(f"【{series_cat}】{len(dups)} 组 MD5 重复:")
            for h, files in dups.items():
                print(f"  {h}: {files}")
        else:
            print(f"【{series_cat}】无 MD5 重复 ✓")

if __name__ == '__main__':
    main()