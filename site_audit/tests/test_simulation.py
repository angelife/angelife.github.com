"""Tests for contrast simulation."""

from site_audit.css_analyzer.parser import ColorToken
from site_audit.css_analyzer.simulation import simulate_fix, SimulationResult


def test_simulation_fix_improves_ratio():
    """Fixing #888888 to #666666 should improve contrast."""
    t = ColorToken(value="#888888", variable="--secondary")
    sim = simulate_fix(t, "#666666", original_issue_count=68)
    assert sim.after_ratio > sim.before_ratio
    assert sim.after_ratio >= 4.5  # WCAG AA


def test_simulation_before_after_failures():
    """After fix, failures should drop to 0."""
    t = ColorToken(value="#888888", variable="--x")
    sim = simulate_fix(t, "#555555", original_issue_count=50)
    assert sim.before_failures == 50
    assert sim.after_failures == 0


def test_simulation_to_dict():
    """SimulationResult.to_dict should be serializable."""
    s = SimulationResult("--x", "#888888", "#666666", 3.9, 5.7, 68, 0)
    d = s.to_dict()
    assert d["variable"] == "--x"
    assert d["before_failures"] == 68
    assert d["after_failures"] == 0