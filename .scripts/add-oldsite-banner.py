#!/usr/bin/env python3
"""Add return-link banner + search box to all old-site HTML pages."""
import os, glob, re

OLD_SITE = os.path.expanduser("~/angelife.github.com/hugo-site/static/old-site")

RETURN_BANNER = '''<div style="background:#fff8e1;border-bottom:1px solid #ffe082;padding:8px 16px;text-align:center;font:14px/1.5 -apple-system,BlinkMacSystemFont,sans-serif">
  <a href="https://angelife.github.io/" style="color:#b8860b;text-decoration:none;font-weight:600">← 返回安知生新站</a>
  <span style="color:#aaa;margin:0 10px">|</span>
  <a href="https://angelife.github.io/search/" style="color:#b8860b;text-decoration:none" onclick="var q=prompt('搜索全站（含旧站）：');if(q)location.href='https://angelife.github.io/search/?q='+encodeURIComponent(q);return false">🔍 搜索全站</a>
</div>'''

count = 0
for html_path in sorted(glob.glob(os.path.join(OLD_SITE, "**", "*.html"), recursive=True)):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Skip if already has the banner
    if '返回安知生新站' in content:
        continue

    # Inject after <body> or <body ...>
    content = re.sub(r'(<body[^>]*>)', r'\1\n' + RETURN_BANNER, content, count=1)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)
    count += 1

print(f"Added return-link banner to {count} old-site pages")
