"""WCAG contrast ratio checking using Playwright.

Phase 8A: Exports structured DOMEvidence for each scanned element.
Phase 8B (future): Cascade Engine consumes DOMEvidence instead of guessing.
"""

import json
import re
from pathlib import Path
from typing import List, Optional
from playwright.sync_api import Page

from ..models.issue import Issue, Severity
from ..models.evidence import (
    Evidence, ElementInfo, ComputedInfo, SourceInfo,
    Finding, Recommendation,
    build_dom_evidence,
)
from .browser import get_content_element


def _relative_luminance(r: float, g: float, b: float) -> float:
    def linearize(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def _contrast_ratio(fg: float, bg: float) -> float:
    lighter = max(fg, bg)
    darker = min(fg, bg)
    return (lighter + 0.05) / (darker + 0.05)


_JS_EVIDENCE = r"""
(el) => {
    // --- 1. DOM ancestor chain ---
    let ancestors = [];
    let cur = el.parentElement;
    while (cur && cur !== document.body && cur !== document.documentElement) {
        ancestors.push({
            tag: cur.tagName.toLowerCase(),
            id: cur.id || '',
            classes: cur.classList ? [...cur.classList] : [],
        });
        cur = cur.parentElement;
    }

    // --- 2. CSS path (human-readable) ---
    let pathParts = [];
    cur = el;
    while (cur && cur !== document.body && cur !== document.documentElement) {
        let seg = cur.tagName.toLowerCase();
        if (cur.id) seg += '#' + cur.id;
        else if (cur.classList && cur.classList.length > 0) {
            seg += '.' + [...cur.classList].filter(Boolean).slice(0, 3).join('.');
        }
        pathParts.unshift(seg);
        cur = cur.parentElement;
    }
    const cssPath = pathParts.join(' > ');

    // --- 3. Computed styles ---
    const cs = window.getComputedStyle(el);

    // --- 4. Selector (best-effort, Playwright-style) ---
    let sel = el.tagName.toLowerCase();
    if (el.id) sel = '#' + el.id;
    else if (el.className && typeof el.className === 'string') {
        const cls = el.className.trim().split(/\s+/).filter(Boolean).slice(0, 2).join('.');
        if (cls) sel += '.' + cls;
    }

    return {
        tag: el.tagName.toLowerCase(),
        id: el.id || '',
        classList: el.classList ? [...el.classList] : [],
        ancestors: ancestors,
        cssPath: cssPath,
        computed: {
            color: cs.color,
            background_color: cs.backgroundColor,
            font_size: cs.fontSize,
            font_weight: cs.fontWeight,
            opacity: cs.opacity,
            line_height: cs.lineHeight,
        },
        selector: sel,
    };
}
"""

_JS_CSS_SOURCE_MAP = r"""
() => {
    const map = {};
    try {
        for (const sheet of document.styleSheets) {
            let href = sheet.href || 'inline';
            try {
                for (const rule of sheet.cssRules || []) {
                    if (rule.selectorText) {
                        map[rule.selectorText] = href;
                    }
                }
            } catch(e) { /* CORS-blocked */ }
        }
    } catch(e) {}
    return JSON.stringify(map);
}
"""


def check_contrast(
    page: Page,
    page_url: str,
    evidence_dir: Path,
    contrast_screenshot: bool = False,
    export_evidence: Optional[Path] = None,
) -> List[Issue]:
    """Check WCAG text contrast on the page.

    If export_evidence is provided, writes a PageEvidence JSON to that path.
    """
    issues: List[Issue] = []
    page.goto(page_url, wait_until="domcontentloaded", timeout=15000)

    content_el = get_content_element(page)
    if not content_el:
        return issues

    # Build CSS source map once
    css_map = {}
    try:
        raw = page.evaluate(_JS_CSS_SOURCE_MAP)
        if raw:
            css_map = json.loads(raw)
    except Exception:
        pass

    text_elements = content_el.query_selector_all(
        "p, h1, h2, h3, h4, h5, h6, li, span, a, td, th, label, blockquote, figcaption"
    )

    # Phase 8A evidence collection
    page_evidence_list: List[Evidence] = []

    screenshot_selectors = set()

    for idx, el in enumerate(text_elements[:200]):
        try:
            # --- Phase 8A: collect structured DOM evidence ---
            raw_evidence = page.evaluate(_JS_EVIDENCE, el)
            if not raw_evidence:
                continue

            evidence = build_dom_evidence(raw_evidence, idx)
            page_evidence_list.append(evidence)

            text = el.text_content()
            if not text or len(text.strip()) < 3:
                continue

            style = raw_evidence.get("computed", {})
            fg_rgb = _parse_rgb(style.get("color", ""))
            bg_rgb = _parse_rgb(style.get("background_color", ""))
            if not fg_rgb or not bg_rgb:
                continue

            ratio = _contrast_ratio(
                _relative_luminance(*fg_rgb), _relative_luminance(*bg_rgb)
            )

            source = css_map.get(raw_evidence.get("selector", ""), "")

            if ratio < 4.5:
                sev = Severity.CRITICAL if ratio < 3.0 else Severity.MAJOR
                label = "Very low" if ratio < 3.0 else "Low"

                evidence_path = ""
                if contrast_screenshot and raw_evidence.get("selector", "") not in screenshot_selectors:
                    slug = Path(page_url).stem or "index"
                    safe_sel = raw_evidence["selector"].replace(".", "_").replace("#", "_").replace(" ", "")
                    ep = evidence_dir / f"contrast-{slug}-{idx}-{safe_sel}.png"
                    page.screenshot(path=str(ep), full_page=False)
                    evidence_path = str(ep)
                    screenshot_selectors.add(raw_evidence["selector"])

                issues.append(Issue(
                    rule="visual/contrast", severity=sev,
                    message=f"{label} contrast: {ratio:.2f}:1 ({style.get('font_size','?')})",
                    file=page_url,
                    context=f"Color: {style['color']} on {style.get('background_color','')} | '{text[:50].strip()}'",
                    suggestion=f"Target at least 4.5:1. Current: {ratio:.2f}:1",
                    evidence_path=evidence_path,
                    data={
                        "ratio": round(ratio, 2),
                        "fg": style["color"],
                        "bg": style.get("background_color", ""),
                        "fontSize": style.get("font_size", ""),
                        "selector": raw_evidence.get("selector", ""),
                        "css_source": source,
                        # Phase 8A: link to evidence
                        "element_index": idx,
                    }
                ))
        except Exception:
            continue

    # Export Phase 8A evidence if requested
    if export_evidence and page_evidence_list:
        p = export_evidence / f"evidence-{Path(page_url).stem or 'index'}.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        # Export as simple dict list
        export = {"url": page_url, "elements": [e.to_dict() for e in page_evidence_list]}
        p.write_text(json.dumps(export, indent=2, ensure_ascii=False))

    return issues


def check_font_size(page: Page, page_url: str) -> List[Issue]:
    """Detect overly small font sizes."""
    issues: List[Issue] = []
    content_el = get_content_element(page)
    if not content_el:
        return issues

    elements = content_el.query_selector_all("p, li, td, th, span, div, figcaption")
    for el in elements[:100]:
        try:
            text = el.text_content()
            if not text or len(text.strip()) < 5:
                continue
            size = page.evaluate("(el) => window.getComputedStyle(el).fontSize", el)
            size_px = float(size.replace("px", ""))
            if size_px < 12:
                issues.append(Issue(
                    rule="visual/font-size", severity=Severity.MAJOR,
                    message=f"Very small body text: {size}",
                    file=page_url,
                    context=f"'{text[:40].strip()}'",
                    suggestion="Increase to at least 14px for body text.",
                    data={"fontSize": size}
                ))
        except Exception:
            continue

    return issues


_RGB_RE = re.compile(r"rgba?\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)")


def _parse_rgb(css: str):
    m = _RGB_RE.search(css)
    if m:
        return (int(m.group(1)) / 255.0, int(m.group(2)) / 255.0, int(m.group(3)) / 255.0)
    return None