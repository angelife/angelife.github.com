#!/usr/bin/env python3
"""Inject Giscus comment section into all old-site HTML pages."""
import os, glob

OLD_SITE = os.path.expanduser("~/angelife.github.com/hugo-site/static/old-site")
GISCUS_HTML = '''  <style>
    #giscus { margin: 2em auto; max-width: 760px; padding: 0 1em; }
    .old-site-comment-sep { max-width: 760px; margin: 0 auto; padding: 0 1em; }
  </style>
  <hr class="old-site-comment-sep">
  <div id="giscus"></div>
  <script src="https://giscus.app/client.js"
    data-repo="angelife/angelife.github.com"
    data-repo-id="MDEwOlJlcG9zaXRvcnkyOTMyMTIw"
    data-category="General"
    data-category-id="DIC_kwDOACy9mM4DAgq0"
    data-mapping="pathname"
    data-strict="0"
    data-reactions-enabled="1"
    data-emit-metadata="0"
    data-input-position="bottom"
    data-theme="preferred_color_scheme"
    data-lang="zh-CN"
    data-loading="lazy"
    crossorigin="anonymous"
    async>
  </script>'''

count_ok = 0
count_skip = 0

for html_path in sorted(glob.glob(os.path.join(OLD_SITE, "**", "*.html"), recursive=True)):
    rel = os.path.relpath(html_path, OLD_SITE)
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    if 'giscus.app' in content:
        print(f"  ⏭ {rel} (already has giscus)")
        count_skip += 1
        continue

    if '</body>' not in content:
        print(f"  ⚠ {rel} (no </body> found)")
        count_skip += 1
        continue

    new_content = content.replace('</body>', GISCUS_HTML + '\n</body>', 1)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"  ✅ {rel}")
    count_ok += 1

print(f"\nDone: {count_ok} updated, {count_skip} skipped")
