"""Tests for cascade mapping confidence levels."""

from site_audit.css_analyzer.cascade import (
    CascadeResolver, MappingResult, color_delta, _extract_var
)
from site_audit.css_analyzer.selector_match import specificity


def test_color_delta_exact():
    d, label = color_delta("#888888", "#888888")
    assert label == "exact"


def test_color_delta_close():
    d, label = color_delta("#222222", "#1a1a1a")
    # #222 = rgb(34,34,34), #1a1a1a = rgb(26,26,26) — diff = 8 per channel
    assert label == "close"


def test_color_delta_different():
    d, label = color_delta("#000000", "#ffffff")
    assert label == "different"


def test_color_delta_short_hex():
    d, label = color_delta("#888", "#888888")
    assert label == "exact"


def test_color_delta_invalid():
    d, label = color_delta("invalid", "#ffffff")
    assert label == "unknown"


def test_specificity_id_highest():
    assert specificity("#header") > specificity(".title")
    assert specificity(".title") > specificity("a")


def test_specificity_multiple_classes():
    assert specificity(".a.b.c") == 30
    assert specificity(".a.b") == 20


def test_extract_var():
    assert _extract_var("var(--primary)") == "--primary"
    assert _extract_var("color: var(--secondary)") == "--secondary"
    assert _extract_var("rgb(0,0,0)") == ""


def test_mapping_result_to_dict():
    r = MappingResult("a.post-title", "#1a1a1a")
    r.confidence = "HIGH"
    r.css_source_file = "style.css"
    r.css_selector = ".post-title"
    r.variable = "--primary"
    r.color_delta = "close"
    d = r.to_dict()
    assert d["confidence"] == "HIGH"
    assert d["variable"] == "--primary"
    assert d["color_delta"] == "close"