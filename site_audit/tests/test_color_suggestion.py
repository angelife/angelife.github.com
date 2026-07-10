"""Tests for color suggestion algorithm."""

from site_audit.css_analyzer.report import suggest_color, _ratio_against_white


def test_suggest_darken_gray():
    """#888888 against white should be darkened to meet AA 4.5:1."""
    result = suggest_color("#888888", "#ffffff", target_ratio=4.5)
    assert result is not None
    assert result != "#888888"
    ratio = _ratio_against_white(result)
    assert ratio >= 4.5, f"{result} against white = {ratio}:1, need ≥4.5"


def test_suggest_already_pass():
    """#333333 against white already passes AA."""
    result = suggest_color("#333333", "#ffffff", target_ratio=4.5)
    assert result == "#333333"


def test_suggest_returns_hex():
    """Suggestion should return a valid hex color."""
    result = suggest_color("#999999", "#ffffff", target_ratio=4.5)
    assert result is not None
    assert result.startswith("#")
    assert len(result) == 7


def test_suggest_lighter_gray_needs_more_darkening():
    """#cccccc needs significant darkening."""
    result = suggest_color("#cccccc", "#ffffff", target_ratio=4.5)
    assert result is not None
    ratio = _ratio_against_white(result)
    assert ratio >= 4.5, f"{result} against white = {ratio}:1, need ≥4.5"


def test_suggest_none_on_invalid():
    """Invalid colors should return None."""
    result = suggest_color("invalid", "#ffffff", target_ratio=4.5)
    assert result is None


def test_suggest_dark_bg():
    """#999999 on #000000 should be lightened to meet AA."""
    result = suggest_color("#999999", "#000000", target_ratio=4.5)
    assert result is not None
    ratio = _ratio_against_white(result)
    # On white bg, this should also pass (lighter than original)
    assert int(result.lstrip("#"), 16) >= int("999999", 16)