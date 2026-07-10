"""Tests for heading level and spacing checks."""

import pytest
from pathlib import Path
import markdown_it

from site_audit.scanner.headings import check_heading_levels, check_heading_spacing
from site_audit.models.issue import Severity


def _parse(content: str):
    md = markdown_it.MarkdownIt()
    return md.parse(content)


def test_heading_skip_level():
    """H1 → H3 should flag a skipped H2."""
    md = "# Title\n\n## Section\n\n### Subsection\n\nSome text"
    tokens = _parse(md)
    issues = check_heading_levels(Path("test.md"), tokens)
    assert len(issues) == 0, f"Should have no skipped levels in valid hierarchy: {issues}"

    md_skip = "# Title\n\n### Subsection\n\nSome text"
    tokens = _parse(md_skip)
    issues = check_heading_levels(Path("test.md"), tokens)
    assert len(issues) == 1, "Should detect H1→H3 skip"
    assert issues[0].rule == "markdown/heading-level"
    assert issues[0].severity == Severity.MAJOR


def test_heading_no_skip_with_hr():
    """Headings separated by --- should not flag a skip (different sections)."""
    md = "# Section One\n\nSome text\n\n---\n\n### Section Three"
    tokens = _parse(md)
    issues = check_heading_levels(Path("test.md"), tokens)
    assert len(issues) == 0, "HR separator should reset heading continuity"


def test_heading_spacing_blank_before():
    """Missing blank line before heading should be flagged."""
    md = "Some text\n## Subheading\n\nBody"
    tokens = _parse(md)
    issues = check_heading_spacing(Path("test.md"), tokens, content=md)
    assert len(issues) >= 1
    assert issues[0].rule == "markdown/heading-spacing"
