#!/usr/bin/env python3
"""Extend Hugo's index.json with old-site page entries for unified search.
Usage: python3 extend-search-index.py [hugo-site/public/ path]
Defaults to ./hugo-site/public/ relative to CWD."""
import os, glob, json, re, sys

PUBLIC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.getcwd(), "hugo-site", "public")
OLD_SITE = os.path.join(PUBLIC, "old-site")
INDEX_PATH = os.path.join(PUBLIC, "index.json")

print(f"Reading index from: {INDEX_PATH}")
print(f"Scanning old-site:  {OLD_SITE}")

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    index = json.load(f)

existing_urls = {e.get("permalink", "") for e in index}
added = 0

for html_path in sorted(glob.glob(os.path.join(OLD_SITE, "**", "*.html"), recursive=True)):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    m = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    title = m.group(1).strip() if m else os.path.basename(html_path)

    rel_path = os.path.relpath(html_path, PUBLIC)
    permalink = f"https://angelife.github.io/{rel_path}"

    if permalink in existing_urls:
        continue

    summary = ""
    body_m = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
    if body_m:
        text = re.sub(r'<[^>]+>', '', body_m.group(1))
        text = re.sub(r'\s+', ' ', text).strip()
        summary = text[:200] if text else ""

    index.append({
        "categories": "旧站存档",
        "content": "",
        "description": summary[:160] if summary else "旧站存档文章",
        "permalink": permalink,
        "summary": summary,
        "tags": "旧站,存档",
        "title": title
    })
    existing_urls.add(permalink)
    added += 1

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    json.dump(index, f, ensure_ascii=False)

print(f"Extended search index: {added} old-site entries added (total {len(index)})")
