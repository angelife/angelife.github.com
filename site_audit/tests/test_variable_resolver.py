"""Tests for enhanced CSS variable resolver (recursive, local scope)."""

import tempfile
from pathlib import Path

from site_audit.css_analyzer.parser import parse_css_file, CSSRule
from site_audit.css_analyzer.variables import (
    VariableScope, build_scope, resolve_value, resolve_all_var_references
)


def test_build_scope_global():
    css = ":root { --primary: #333; --secondary: #888; }"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".css", delete=False) as f:
        f.write(css)
        fp = f.name
    rules = parse_css_file(fp)
    scope = build_scope(rules)
    assert scope.resolve("--primary") == "#333"
    assert scope.resolve("--secondary") == "#888"


def test_build_scope_local():
    css = """
:root { --global: #333; }
.dark { --accent: #eee; }
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".css", delete=False) as f:
        f.write(css)
        fp = f.name
    rules = parse_css_file(fp)
    scope = build_scope(rules)
    assert scope.resolve("--global") == "#333"
    # Local variable accessible with context
    assert scope.resolve("--accent") == "#eee"


def test_resolve_value_simple():
    rules = [CSSRule(selector=":root", property="--x", value="#888", source_file="a.css")]
    scope = build_scope(rules)
    result = resolve_value("var(--x)", scope)
    assert result == "#888"


def test_resolve_value_nested():
    """var(--a) where --a = var(--b) and --b = #666 should resolve to #666."""
    rules = [
        CSSRule(selector=":root", property="--a", value="var(--b)", source_file="a.css"),
        CSSRule(selector=":root", property="--b", value="#666", source_file="a.css"),
    ]
    scope = build_scope(rules)
    result = resolve_value("var(--a)", scope)
    assert result == "#666"


def test_resolve_value_depth_limit():
    """Deeply nested should not infinite-loop."""
    rules = [CSSRule(selector=":root", property="--x", value="var(--x)", source_file="a.css")]
    scope = build_scope(rules)
    result = resolve_value("var(--x)", scope)
    # Should gracefully contain var() or fail but not hang
    assert "var(" in result


def test_resolve_value_fallback():
    result = resolve_value("var(--nonexistent, #default)", VariableScope())
    assert result == "#default"


def test_resolve_all_var_references():
    css = """
:root { --secondary: #777; }
.title { color: var(--secondary); }
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".css", delete=False) as f:
        f.write(css)
        fp = f.name
    rules = parse_css_file(fp)
    resolved = resolve_all_var_references(rules)
    assert any(r.resolved_value == "#777" for r in resolved)