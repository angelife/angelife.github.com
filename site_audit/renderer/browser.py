"""Playwright browser controller for render-layer audit.

Uses Playwright Python API (sync).
"""

from pathlib import Path
from typing import List, Optional, Tuple
from playwright.sync_api import sync_playwright, Browser, Page


_PLAYWRIGHT = None  # singleton


def _get_playwright():
    global _PLAYWRIGHT
    if _PLAYWRIGHT is None:
        _PLAYWRIGHT = sync_playwright().start()
    return _PLAYWRIGHT


def launch_browser(headless: bool = True) -> Tuple[object, Browser, Page]:
    """Launch Chromium and return (playwright, browser, page)."""
    p = _get_playwright()
    browser = p.chromium.launch(headless=headless)
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="zh-CN",
        ignore_https_errors=True,
    )
    page = context.new_page()
    return p, browser, page


def close_browser(browser, playwright=None) -> None:
    """Clean up."""
    try:
        browser.close()
    except Exception:
        pass


def get_page_urls(page: Page, base_url: str, max_pages: int = 100) -> List[str]:
    """Discover page URLs from sitemap.xml or by crawling."""
    urls: List[str] = []

    # 1. Try sitemap
    try:
        page.goto(f"{base_url}/sitemap.xml", wait_until="domcontentloaded", timeout=10000)
        locs = page.locator("loc").all()
        for loc in locs:
            u = loc.text_content()
            if u and u.strip().startswith(base_url):
                urls.append(u.strip())
    except Exception:
        pass

    # 2. Fallback: crawl homepage
    if not urls:
        try:
            page.goto(base_url, wait_until="domcontentloaded", timeout=10000)
            page.wait_for_load_state("networkidle", timeout=15000)
            links = page.evaluate("""
                (baseUrl) => {
                    const seen = new Set();
                    return [...document.querySelectorAll('a[href]')]
                        .map(a => a.href.split('#')[0].replace(/\\/$/, ''))
                        .filter(h => h.startsWith(baseUrl) && !seen.has(h) && seen.add(h));
                }
            """, base_url)
            if links:
                urls = list(links)
        except Exception:
            pass

    # Deduplicate and limit
    seen = set()
    unique = []
    for u in urls:
        norm = u.rstrip("/")
        if norm not in seen:
            seen.add(norm)
            unique.append(u)

    return unique[:max_pages]


_CONTENT_SELECTORS = [
    "article",
    ".post-content",
    ".entry-content",
    "main",
    ".content",
    "#content",
]


def get_content_element(page: Page) -> object:
    """Find the main content element."""
    for sel in _CONTENT_SELECTORS:
        el = page.query_selector(sel)
        if el:
            return el
    return page.query_selector("body")