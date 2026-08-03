"""Tests for 3-tier color candidates."""

from site_audit.css_analyzer.parser import ColorToken
from site_audit.css_analyzer.candidates import generate_candidates


def test_candidates_structure():
    """Each candidate should have level, color, ratio, delta, description."""
    t = ColorToken(value="#888888", variable="--secondary")
    cands = generate_candidates(t)
    assert len(cands) > 0
    for c in cands:
        assert "level" in c
        assert "color" in c
        assert "ratio" in c
        assert c["color"].startswith("#")
        assert len(c["color"]) == 7


def test_candidates_three_ordered():
    """Candidates should be light, balanced, strong in order."""
    t = ColorToken(value="#888888")
    cands = generate_candidates(t)
    if len(cands) >= 3:
        assert cands[0]["level"] == "light"
        assert cands[1]["level"] == "balanced"
        assert cands[2]["level"] == "strong"


def test_candidates_improving_ratio():
    """Each candidate should have higher ratio than the previous."""
    t = ColorToken(value="#888888")
    cands = generate_candidates(t)
    for i in range(1, len(cands)):
        assert cands[i]["ratio"] >= cands[i - 1]["ratio"]


def test_candidates_black_passes():
    """A color that already passes AA should not produce candidates."""
    t = ColorToken(value="#333333")
    cands = generate_candidates(t)
    assert len(cands) == 0