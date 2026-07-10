"""Tests for patch preview generation."""

from site_audit.css_analyzer.patch import Patch, generate_patch
from site_audit.css_analyzer.parser import ColorToken


def test_patch_creation():
    """Patch should store all fields correctly."""
    p = Patch(
        variable="--secondary", source_file="style.css", line=12,
        old_value="#888888", new_value="#6b6b6b",
        selectors=[".post-meta", ".post-title"], issue_count=68,
    )
    assert p.variable == "--secondary"
    assert p.old_value == "#888888"
    assert p.new_value == "#6b6b6b"
    assert p.line == 12
    assert p.issue_count == 68


def test_patch_to_dict():
    """Patch.to_dict should return a serializable dict."""
    p = Patch("--x", "f.css", 1, "#888", "#666", [".a"], 5)
    d = p.to_dict()
    assert d["variable"] == "--x"
    assert d["old_value"] == "#888"


def test_generate_patch_no_variable():
    """Token without variable should return None."""
    t = ColorToken(value="#888888", source_files=["a.css"])
    result = generate_patch(t, "#666666")
    assert result is None


def test_generate_patch_no_files():
    """Token without source files should return None."""
    t = ColorToken(value="#888888", variable="--x")
    result = generate_patch(t, "#666666")
    assert result is None


def test_generate_patch_file_not_found():
    """Token with non-existent source file should return None."""
    t = ColorToken(value="#888888", variable="--x", source_files=["/nonexistent/file.css"])
    result = generate_patch(t, "#666666")
    assert result is None