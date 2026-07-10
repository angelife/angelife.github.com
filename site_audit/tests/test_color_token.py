"""Tests for color token aggregation and suggestion."""

from site_audit.css_analyzer.parser import CSSRule, ColorToken, normalize_color, hex_to_rgb
from site_audit.css_analyzer.colors import build_color_tokens, rank_tokens, compute_contrast_for_token


def test_build_single_color_token():
    rules = [
        CSSRule(selector=".title", property="color", value="#888888",
                resolved_value="#888888", source_file="a.css", line=1),
    ]
    tokens = build_color_tokens(rules)
    assert "#888888" in tokens
    t = tokens["#888888"]
    assert t.usage_count == 1
    assert t.selectors == [".title"]


def test_build_multiple_selectors_same_color():
    rules = [
        CSSRule(selector=".title", property="color", value="#888",
                resolved_value="#888", source_file="a.css", line=1),
        CSSRule(selector=".meta", property="color", value="var(--secondary)",
                resolved_value="#888", source_file="a.css", line=5),
    ]
    tokens = build_color_tokens(rules)
    assert "#888888" in tokens
    t = tokens["#888888"]
    assert t.usage_count == 2
    assert len(t.selectors) == 2


def test_rank_tokens():
    rules = [
        CSSRule(selector=".a", property="color", value="#111", resolved_value="#111",
                source_file="a.css", line=1),
        CSSRule(selector=".b", property="color", value="#222", resolved_value="#222",
                source_file="a.css", line=2),
        CSSRule(selector=".c", property="color", value="#111", resolved_value="#111",
                source_file="a.css", line=3),
    ]
    tokens = build_color_tokens(rules)
    ranked = rank_tokens(tokens)
    assert len(ranked) == 2
    assert ranked[0].value == "#111111"  # most used


def test_contrast_for_token_white():
    """#888888 against white should be about 3.3:1 (below AA)."""
    t = ColorToken(value="#888888")
    ratio = compute_contrast_for_token(t)
    assert 3.0 < ratio < 4.0, f"Expected ~3.3:1, got {ratio}"


def test_contrast_for_token_black():
    """Black against white is 21:1."""
    t = ColorToken(value="#000000")
    ratio = compute_contrast_for_token(t)
    assert ratio > 20


def test_hex_to_rgb():
    assert hex_to_rgb("#888888") == (136, 136, 136)
    assert hex_to_rgb("#ff0000") == (255, 0, 0)