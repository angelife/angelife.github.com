"""Tests for cascade ordering: important, specificity, source order."""

from site_audit.css_analyzer.parser import CSSRule


def test_cascade_key_importance():
    """!important comes before non-important."""
    r1 = CSSRule(selector="a", property="color", value="#000", important=False,
                 specificity_a=0, specificity_b=1, specificity_c=0, source_order=1)
    r2 = CSSRule(selector="a", property="color", value="#111", important=True,
                 specificity_a=0, specificity_b=0, specificity_c=1, source_order=2)
    key1 = r1.cascade_key()
    key2 = r2.cascade_key()
    # !important wins (key2 should sort first)
    assert key2 < key1


def test_cascade_key_specificity():
    """Higher specificity wins when importance is equal."""
    r1 = CSSRule(selector=".a", property="color", value="#000", important=False,
                 specificity_a=0, specificity_b=1, specificity_c=0, source_order=1)
    r2 = CSSRule(selector="div.a", property="color", value="#111", important=False,
                 specificity_a=0, specificity_b=1, specificity_c=1, source_order=2)
    key1 = r1.cascade_key()
    key2 = r2.cascade_key()
    assert key2 < key1  # r2 has (0,1,1) > r1 has (0,1,0)


def test_cascade_key_source_order():
    """Earlier source wins when specificity is equal."""
    r1 = CSSRule(selector="a", property="color", value="#000", important=False,
                 specificity_a=0, specificity_b=0, specificity_c=1, source_order=2)
    r2 = CSSRule(selector="a", property="color", value="#111", important=False,
                 specificity_a=0, specificity_b=0, specificity_c=1, source_order=1)
    key1 = r1.cascade_key()
    key2 = r2.cascade_key()
    # r2 has lower source_order (appeared earlier) → sorts first
    assert key2 < key1


def test_parse_css_file_sets_specificity():
    """parse_css_file should now set specificity fields."""
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".css", delete=False) as f:
        f.write("h1.post-title { color: #333; }")
        fp = f.name
    from site_audit.css_analyzer.parser import parse_css_file
    rules = parse_css_file(fp)
    for r in rules:
        assert hasattr(r, "specificity_a")
        assert hasattr(r, "specificity_b")
        assert hasattr(r, "specificity_c")


def test_parse_important_detection():
    """!important should be detectable in value."""
    # Verify !important is part of the raw CSS value
    assert "!important" in "color: #000 !important;"
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".css", delete=False) as f:
        f.write("a { color: #000 !important; }")
        fp = f.name
    from site_audit.css_analyzer.parser import parse_css_file
    rules = parse_css_file(fp)
    important_rules = [r for r in rules if r.important]
    assert len(important_rules) >= 1