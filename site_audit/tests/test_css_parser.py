"""Tests for CSS parser — selectors, variables, color normalization."""

import tempfile
from pathlib import Path

from site_audit.css_analyzer.parser import (
    parse_css_file, normalize_color, hex_to_rgb, find_css_files,
)
from site_audit.css_analyzer.variables import build_variable_graph, resolve_all_variables


def _write_css(content: str) -> str:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".css", delete=False) as f:
        f.write(content)
        return f.name


def test_parse_basic_rules():
    css = """
.post-title { color: #888888; }
.post-meta { font-size: 14px; color: var(--secondary); }
"""
    fp = _write_css(css)
    rules = parse_css_file(fp)
    assert len(rules) == 2
    assert rules[0].selector == ".post-title"
    assert rules[0].property == "color"
    assert rules[0].value == "#888888"
    assert rules[0].variables == []


def test_parse_variable_reference():
    css = """
:root { --secondary: #777777; }
.post-meta { color: var(--secondary); }
"""
    fp = _write_css(css)
    rules = parse_css_file(fp)
    assert len(rules) == 2

    # :root definition
    assert rules[0].property == "--secondary"
    assert rules[0].value == "#777777"

    # Variable reference
    assert rules[1].selector == ".post-meta"
    assert rules[1].variables == ["--secondary"]


def test_parse_background_color():
    css = """.card { background-color: #eee; }"""
    fp = _write_css(css)
    rules = parse_css_file(fp)
    assert len(rules) == 1
    assert rules[0].property == "background-color"
    assert normalize_color(rules[0].value) == "#eeeeee"


def test_normalize_color_hex():
    assert normalize_color("#888") == "#888888"
    assert normalize_color("#888888") == "#888888"
    assert normalize_color("#ffffff") == "#ffffff"
    assert normalize_color("#abc") == "#aabbcc"


def test_normalize_color_rgb():
    assert normalize_color("rgb(136, 136, 136)") == "#888888"
    assert normalize_color("rgba(255, 255, 255, 0.5)") == "#ffffff"


def test_normalize_color_named():
    assert normalize_color("white") == "#ffffff"
    assert normalize_color("black") == "#000000"
    assert normalize_color("transparent") is None


def test_hex_to_rgb():
    assert hex_to_rgb("#888888") == (136, 136, 136)
    assert hex_to_rgb("#ffffff") == (255, 255, 255)
    assert hex_to_rgb("invalid") is None


def test_build_variable_graph():
    css1 = _write_css(":root { --primary: #333; --secondary: var(--primary); }")
    css2 = _write_css(".x { color: var(--secondary); }")
    rules = parse_css_file(css1) + parse_css_file(css2)
    var_map = build_variable_graph(rules)
    assert "--primary" in var_map
    assert var_map["--primary"] == "#333"


def test_resolve_all_variables():
    var_css = _write_css(":root { --secondary: #777; }")
    rule_css = _write_css(".post { color: var(--secondary); }")
    rules = parse_css_file(var_css) + parse_css_file(rule_css)
    var_map = build_variable_graph(rules)
    resolved = resolve_all_variables(rules, var_map)
    assert len(resolved) > 0
    for r in resolved:
        assert "var(" not in r.resolved_value


def test_find_css_files():
    with tempfile.TemporaryDirectory() as td:
        Path(td, "style.css").write_text("a { color: red; }")
        Path(td, "sub").mkdir()
        Path(td, "sub", "theme.css").write_text("b { color: blue; }")
        files = find_css_files(td)
        assert len(files) == 2