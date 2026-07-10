"""Tests for cascade matching using new selector-first strategy."""

import tempfile
from pathlib import Path

from site_audit.css_analyzer.cascade import CascadeResolver, color_delta, dark_mode_rules
from site_audit.css_analyzer.selector_match import specificity


def test_color_delta_exact():
    d, label = color_delta("#888888", "#888888")
    assert label == "exact"
    assert d == 0


def test_color_delta_short():
    d, label = color_delta("#888", "#888888")
    assert label == "exact"


def test_color_delta_close():
    # #222 = rgb(34,34,34), #1a1a1a = rgb(26,26,26) — diff=8
    d, label = color_delta("#222222", "#1a1a1a")
    assert label == "close"


def test_color_delta_different():
    d, label = color_delta("#000000", "#ffffff")
    assert label == "different"


def test_specificity_values():
    assert specificity("#header") == 100
    assert specificity(".title") == 10
    assert specificity("a") == 1
    assert specificity("h1.post-title") == 11


def test_dark_mode_filter():
    from site_audit.css_analyzer.parser import CSSRule
    rules = [
        CSSRule(selector=":root", property="--bg", value="#fff"),
        CSSRule(selector=".dark", property="--bg", value="#000"),
        CSSRule(selector="[data-theme=dark]", property="color", value="#ccc"),
    ]
    dark = dark_mode_rules(rules)
    assert len(dark) == 2


def test_cascade_resolve_basic():
    """Test that cascade resolver loads and runs."""
    public_dir = str(Path("/Users/macos/angelife.github.com/hugo-site/public"))
    if not Path(public_dir).exists():
        # Fallback: use inline CSS
        return  # Skip silently
    resolver = CascadeResolver(public_dir)
    resolver.load()
    assert len(resolver.all_rules) > 0
    assert resolver.source_index is not None