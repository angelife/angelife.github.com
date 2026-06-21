# Hugo Template Bypass — HTML Injection Workaround

## When to Use This

When you need to add visible content (like source links, attribution blocks, custom metadata) to posts but the Hugo template system is inaccessible due to:

1. A custom `baseof.html` that intercepts `{{ block }}` rendering and bypasses `{{ define }}` overrides
2. `.Param` returning empty for nested param names (e.g., `source.blogger_url`)
3. Theme template files that can't be safely overridden without breaking other layouts

## The Pattern

Extract data from Hugo source front matter, then inject a visible HTML block into the generated post HTML **before committing to git**.

```python
import re
from pathlib import Path

def get_blogger_url(post_slug):
    md = Path(f'/repo/hugo-site/content/posts/{post_slug}/index.md')
    if md.exists():
        content = md.read_text(encoding='utf-8')
        m = re.search(r'^\s*blogger_url:\s*(.+)$', content, re.MULTILINE)
        if m:
            return m.group(1).strip().strip('"\'')
    return None

for html_path in sorted(Path('/repo/posts').glob('*/index.html')):
    slug = html_path.parent.name
    blogger_url = get_blogger_url(slug)
    if not blogger_url:
        continue
    html = html_path.read_text(encoding='utf-8')
    if 'SOURCE-LINK-INJECTED' in html:
        continue
    source_div = f'\n<!-- SOURCE-LINK-INJECTED -->\n<div style="margin-bottom:1.5rem;padding:0.6rem 1rem;background:#f8f9fa;border-radius:6px;font-size:0.875rem;"><a href="{blogger_url}">📎 原文</a></div>\n'
    m = re.search(r'(<footer[^>]*class="post-footer"[^>]*>)', html)
    if m:
        html = html[:m.start()] + source_div + html[m.start():]
        html_path.write_text(html, encoding='utf-8')
```

## Critical Constraint — Do NOT Rebuild After Injecting

**Hugo rebuild overwrites `/repo/posts/` every time.** If you run `hugo` after injecting HTML, all injected content is lost.

Correct sequence:
1. `hugo` → generates initial HTML
2. Inject content into `/repo/posts/` HTML files
3. `git add -f posts/` → commit the injected HTML
4. **Never run `hugo` again** without re-injecting after

## The Proper Fix (When Baseof.html Is Deletable)

If you don't need custom `baseof.html` logic, delete it:
```bash
rm hugo-site/layouts/_default/baseof.html
hugo  # {{ define "main" }} overrides now work
```

Then future template changes work normally without HTML surgery.