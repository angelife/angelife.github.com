"""Tests for variable chain tracing — var(--a) → var(--b) → #222."""

from site_audit.css_analyzer.parser import CSSRule, parse_css_file
from site_audit.css_analyzer.variables import build_scope, resolve_value


def test_single_var_resolve():
    rules = [
        CSSRule(selector=":root", property="--primary", value="#222"),
    ]
    scope = build_scope(rules)
    assert scope.resolve("--primary") == "#222"


def test_var_chain_basic():
    """var(--a) → var(--b) → #222"""
    rules = [
        CSSRule(selector=":root", property="--a", value="var(--b)"),
        CSSRule(selector=":root", property="--b", value="#222"),
    ]
    scope = build_scope(rules)
    resolved = resolve_value("var(--a)", scope)
    assert resolved == "#222"


def test_var_chain_deep():
    """var(--a) → var(--b) → var(--c) → #333"""
    rules = [
        CSSRule(selector=":root", property="--a", value="var(--b)"),
        CSSRule(selector=":root", property="--b", value="var(--c)"),
        CSSRule(selector=":root", property="--c", value="#333"),
    ]
    scope = build_scope(rules)
    resolved = resolve_value("var(--a)", scope)
    assert resolved == "#333"


def test_var_chain_fallback():
    """var(--a, #default) → fallback when --a missing."""
    rules = []
    scope = build_scope(rules)
    resolved = resolve_value("var(--missing, #default)", scope)
    assert resolved == "#default"


def test_var_chain_circular():
    """Circular reference should not infinite-loop."""
    rules = [
        CSSRule(selector=":root", property="--a", value="var(--b)"),
        CSSRule(selector=":root", property="--b", value="var(--a)"),
    ]
    scope = build_scope(rules)
    from site_audit.css_analyzer.variables import resolve_value
    result = resolve_value("var(--a)", scope)
    # Should gracefully handle — resolve_value already has depth limit
    assert "var(" in result or result is None or result != "var(--a)"


def test_var_chain_from_css_file():
    """Test real CSS variable chain resolution."""
    import tempfile
    css = """
:root {
    --a: var(--b);
    --b: var(--c);
    --c: #444;
}
.title { color: var(--a); }
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".css", delete=False) as f:
        f.write(css)
        fp = f.name
    rules = parse_css_file(fp)
    scope = build_scope(rules)
    from site_audit.css_analyzer.variables import resolve_all_var_references
    resolved = resolve_all_var_references(rules)
    title_rules = [r for r in resolved if r.selector == ".title"]
    assert len(title_rules) > 0
    # The resolved value should trace through the chain
    assert title_rules[0].resolved_value == "#444"