"""Playwright browser driver — calls Node.js Playwright via subprocess.

Uses the npm-installed Playwright at ~/node_modules/.bin/playwright.
"""

import json
import os
import subprocess
from pathlib import Path
from typing import List, Optional

_RUNNER = Path(__file__).parent / "playwright_runner.js"


def _run_playwright(action: str, args: dict) -> dict:
    """Execute a Playwright action via the Node.js runner."""
    node = _find_node()
    runner = str(_RUNNER.resolve())

    payload = json.dumps({**args, "action": action})
    result = subprocess.run(
        [node, runner, payload],
        capture_output=True, text=True, timeout=60,
    )

    if result.returncode != 0:
        return {"ok": False, "error": f"Node exit code {result.returncode}: {result.stderr[:200]}"}

    # Parse last line of stdout (may have WebSocket/chromium warnings before)
    lines = result.stdout.strip().splitlines()
    for line in reversed(lines):
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            continue

    return {"ok": False, "error": f"No JSON output: {result.stdout[:200]}"}


def _find_node() -> str:
    """Find Node.js binary."""
    candidates = [
        shutil_which("node"),
        "/usr/local/bin/node",
        "/opt/homebrew/bin/node",
    ]
    for c in candidates:
        if c and os.path.isfile(c):
            return c
    raise RuntimeError("Node.js not found")


def shutil_which(cmd: str) -> Optional[str]:
    """Minimal which implementation."""
    for p in os.environ.get("PATH", "").split(":"):
        f = os.path.join(p, cmd)
        if os.path.isfile(f) and os.access(f, os.X_OK):
            return f
    return None


def get_page_urls(base_url: str, max_pages: int = 100) -> List[str]:
    """Discover page URLs from sitemap.xml or crawling."""
    result = _run_playwright("pages", {"baseUrl": base_url, "maxPages": max_pages})
    if result.get("ok"):
        return result.get("urls", [])
    return []


def check_overflow(page_url: str, evidence_dir: Path) -> List[dict]:
    """Check for horizontal overflow at 375px."""
    evidence_path = str(evidence_dir / f"overflow-{Path(page_url).stem or 'index'}-os.png")
    result = _run_playwright("overflow", {
        "url": page_url,
        "screenshot": evidence_path,
    })

    if not result.get("ok"):
        return [{
            "rule": "visual/overflow", "severity": "major",
            "message": f"Overflow check failed: {result.get('error', 'unknown')}",
            "file": page_url
        }]

    issues = []
    for item in result.get("overflows", [])[:10]:
        selector = item.get("tag", "") + ("#" + item["id"] if item.get("id") else "")
        issues.append({
            "rule": "visual/overflow", "severity": "critical",
            "message": f"Overflow at 375px: <{item['tag']}> width={item['width']}px",
            "file": page_url,
            "context": f"Element: <{item['tag']}>",
            "suggestion": "Set max-width: 100% on this element or its parent.",
            "data": {
                "page": page_url, "selector": selector,
                "width": item["width"], "viewport": 375,
                "screenshot": result.get("screenshot", ""),
            }
        })

    return issues


def check_contrast(page_url: str) -> List[dict]:
    """Check WCAG contrast ratio on page."""
    result = _run_playwright("contrast", {"url": page_url})

    if not result.get("ok"):
        return [{
            "rule": "visual/contrast", "severity": "major",
            "message": f"Contrast check failed: {result.get('error', 'unknown')}",
            "file": page_url
        }]

    from .contrast import _parse_rgb, _relative_luminance, _contrast_ratio

    issues = []
    for el in result.get("issues", []):
        fg_rgb = _parse_rgb(el.get("color", ""))
        bg_rgb = _parse_rgb(el.get("bg", ""))
        if not fg_rgb or not bg_rgb:
            continue

        ratio = _contrast_ratio(
            _relative_luminance(*fg_rgb), _relative_luminance(*bg_rgb)
        )

        if ratio < 3.0:
            issues.append({
                "rule": "visual/contrast", "severity": "critical",
                "message": f"Very low contrast: {ratio:.2f}:1",
                "file": page_url,
                "context": f"<{el['tag']}> '{el.get('text','')[:40]}' on {page_url}",
                "suggestion": "Increase contrast to at least 4.5:1.",
                "data": {"ratio": round(ratio, 2), "fg": el["color"], "bg": el["bg"]}
            })
        elif ratio < 4.5:
            issues.append({
                "rule": "visual/contrast", "severity": "major",
                "message": f"Low contrast: {ratio:.2f}:1",
                "file": page_url,
                "context": f"<{el['tag']}> '{el.get('text','')[:40]}'",
                "suggestion": "Target at least 4.5:1 for body text.",
                "data": {"ratio": round(ratio, 2), "fg": el["color"], "bg": el["bg"]}
            })

    return issues


def check_font_size(page_url: str) -> List[dict]:
    """Check for small font sizes."""
    result = _run_playwright("contrast", {"url": page_url})

    if not result.get("ok"):
        return []

    issues = []
    for el in result.get("issues", []):
        try:
            size = float(el.get("fontSize", "16px").replace("px", ""))
            if size < 12:
                issues.append({
                    "rule": "visual/font-size", "severity": "major",
                    "message": f"Very small text: {el.get('fontSize', '?')}",
                    "file": page_url,
                    "context": f"'{el.get('text','')[:30]}'",
                    "suggestion": "Increase to at least 14px.",
                    "data": {"fontSize": el.get("fontSize")}
                })
        except ValueError:
            continue

    return issues


def take_screenshot(page_url: str, output_path: str, full_page: bool = False) -> Optional[str]:
    """Take a screenshot of a page."""
    result = _run_playwright("screenshot", {
        "url": page_url, "output": output_path, "fullPage": full_page
    })
    if result.get("ok"):
        return output_path
    return None
