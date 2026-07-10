"""Tests for media query parsing and viewport filtering."""

from site_audit.css_analyzer.cascade_engine import (
    parse_media_query, media_is_active, media_text_matches, MediaCondition
)


def test_media_min_width():
    cond = parse_media_query("(min-width: 768px)")
    assert cond.min_width == 768
    assert cond.max_width == 99999


def test_media_max_width():
    cond = parse_media_query("(max-width: 480px)")
    assert cond.min_width == 0
    assert cond.max_width == 480


def test_media_range():
    cond = parse_media_query("(min-width: 768px) and (max-width: 1024px)")
    assert cond.min_width == 768
    assert cond.max_width == 1024


def test_media_prefers_dark():
    cond = parse_media_query("(prefers-color-scheme: dark)")
    assert cond.prefers_dark == True


def test_media_prefers_light():
    cond = parse_media_query("(prefers-color-scheme: light)")
    assert cond.prefers_dark == False


def test_media_active_min():
    cond = MediaCondition(min_width=768)
    assert media_is_active(cond, (1024, 768))
    assert not media_is_active(cond, (375, 812))


def test_media_active_max():
    cond = MediaCondition(max_width=480)
    assert media_is_active(cond, (375, 812))
    assert not media_is_active(cond, (1024, 768))


def test_media_active_dark():
    cond = MediaCondition(prefers_dark=True)
    assert media_is_active(cond, (375, 812), prefers_dark=True)
    assert not media_is_active(cond, (375, 812), prefers_dark=False)


def test_media_text_matches():
    assert media_text_matches("(min-width: 100px)", (375, 812), False)
    assert not media_text_matches("(min-width: 1000px)", (375, 812), False)


def test_media_text_dark():
    assert media_text_matches("(prefers-color-scheme: dark)", (375, 812), True)
    assert not media_text_matches("(prefers-color-scheme: dark)", (375, 812), False)