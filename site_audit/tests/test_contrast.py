"""Tests for contrast checking logic (unit tests of utility functions, no browser needed)."""

from site_audit.renderer.contrast import _relative_luminance, _contrast_ratio, _parse_rgb


def test_relative_luminance_white():
    """White should have luminance ~1.0."""
    lum = _relative_luminance(1.0, 1.0, 1.0)
    assert abs(lum - 1.0) < 0.01


def test_relative_luminance_black():
    """Black should have luminance ~0.0."""
    lum = _relative_luminance(0.0, 0.0, 0.0)
    assert abs(lum - 0.0) < 0.01


def test_contrast_ratio_black_white():
    """Black on white should be 21:1."""
    ratio = _contrast_ratio(0.0, 1.0)
    assert abs(ratio - 21.0) < 0.1


def test_contrast_ratio_same():
    """Same color should be 1:1."""
    ratio = _contrast_ratio(0.5, 0.5)
    assert abs(ratio - 1.0) < 0.01


def test_parse_rgb():
    result = _parse_rgb("rgb(255, 0, 0)")
    assert result is not None
    r, g, b = result
    assert abs(r - 1.0) < 0.01
    assert abs(g - 0.0) < 0.01
    assert abs(b - 0.0) < 0.01


def test_parse_rgba():
    result = _parse_rgb("rgba(0, 128, 255, 0.5)")
    assert result is not None
    r, g, b = result
    assert abs(r - 0.0) < 0.01
    assert abs(g - 0.502) < 0.01
    assert abs(b - 1.0) < 0.01
