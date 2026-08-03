"""Mobile overflow detection and font-size checks using Playwright."""

import json
import time
from pathlib import Path
from typing import List
from playwright.sync_api import Page

from ..models.issue import Issue, Severity
from .browser import get_content_element


_OVERFLOW_JS = """
() => {
    const docWidth = document.documentElement.offsetWidth;
    const all = document.querySelectorAll('*');
    const overflows = [];
    for (const el of all) {
        const ow = el.offsetWidth;
        if (ow > docWidth && !['script','style','svg','pre','code'].includes(el.tagName.toLowerCase())) {
            overflows.push({
                tag: el.tagName, id: el.id || '',
                className: (el.className && typeof el.className === 'string') ? el.className : '',
                width: ow, text: (el.textContent || '').trim().substring(0, 60)
            });
        }
    }
    return overflows.slice(0, 50);
}
"""


def check_overflow(page: Page, page_url: str, evidence_dir: Path) -> List[Issue]:
    """Detect horizontal overflow at 375px viewport width."""
    issues: List[Issue] = []

    # Set mobile viewport
    page.set_viewport_size({"width": 375, "height": 812})
    page.goto(page_url, wait_until="domcontentloaded", timeout=15000)
    time.sleep(0.5)

    try:
        overflows = page.evaluate(_OVERFLOW_JS)

        if overflows:
            slug = Path(page_url).stem or "index"
            evidence_path = evidence_dir / f"overflow-{slug}-{int(time.time())}.png"
            page.screenshot(path=str(evidence_path), full_page=True)

            for item in overflows[:10]:
                sel = item.get("tag", "")
                if item.get("id"):
                    sel += f"#{item['id']}"

                issues.append(Issue(
                    rule="visual/overflow", severity=Severity.CRITICAL,
                    message=f"Overflow at 375px: <{item['tag']}> width={item['width']}px",
                    file=page_url,
                    context=f"Element: <{item['tag']}> '{item.get('text','')[:40]}'",
                    suggestion="Set max-width: 100% on this element or its parent.",
                    evidence_path=str(evidence_path),
                    data={
                        "page": page_url, "selector": sel,
                        "width": item["width"], "viewport": 375,
                        "screenshot": str(evidence_path),
                    }
                ))
    except Exception as e:
        issues.append(Issue(
            rule="visual/overflow", severity=Severity.MAJOR,
            message=f"Overflow detection failed: {e}",
            file=page_url, suggestion="Check for JS errors on the page."
        ))

    # Restore desktop viewport
    page.set_viewport_size({"width": 1920, "height": 1080})

    return issues