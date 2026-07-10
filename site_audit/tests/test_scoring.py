"""Tests for scoring and grade."""

from site_audit.models.issue import Issue, Severity
from site_audit.scoring.score import compute_score, severity_counts, grade


def test_perfect_score():
    """No issues should give 100."""
    score = compute_score([])
    assert score == 100
    assert grade(score) == "A"


def test_critical_penalty():
    """One critical issue should deduct 10."""
    issues = [Issue(rule="test", severity=Severity.CRITICAL, message="test")]
    score = compute_score(issues)
    assert score == 90


def test_critical_capped():
    """10+ critical issues should cap at -50 (score=50)."""
    issues = [Issue(rule="test", severity=Severity.CRITICAL, message="x") for _ in range(10)]
    score = compute_score(issues)
    assert score == 50


def test_major_capped():
    """15 major issues should cap at -30 (score=70)."""
    issues = [Issue(rule="test", severity=Severity.MAJOR, message="x") for _ in range(15)]
    score = compute_score(issues)
    assert score == 70


def test_minor_graded():
    """Minor issues: -1 per 100, capped at -20."""
    # 50 minor -> 0 deduction
    issues = [Issue(rule="test", severity=Severity.MINOR, message="x") for _ in range(50)]
    score = compute_score(issues)
    assert score == 100

    # 150 minor -> -1 (one 100 bucket)
    issues = [Issue(rule="test", severity=Severity.MINOR, message="x") for _ in range(150)]
    score = compute_score(issues)
    assert score == 99

    # 2500 minor -> capped at -20
    issues = [Issue(rule="test", severity=Severity.MINOR, message="x") for _ in range(2500)]
    score = compute_score(issues)
    assert score == 80


def test_mixed_scenario():
    """Realistic mix: 0 critical, 20 major, 6883 minor."""
    issues = (
        [Issue(rule="test", severity=Severity.MAJOR, message="m") for _ in range(20)]
        + [Issue(rule="test", severity=Severity.MINOR, message="n") for _ in range(6883)]
    )
    score = compute_score(issues)
    # major: 20*3=60 → capped at -30
    # minor: 6883//100=68 → capped at -20
    # total: 100-30-20 = 50
    assert score == 50


def test_severity_counts():
    issues = [
        Issue(rule="c", severity=Severity.CRITICAL, message=""),
        Issue(rule="c", severity=Severity.CRITICAL, message=""),
        Issue(rule="m", severity=Severity.MAJOR, message=""),
        Issue(rule="n", severity=Severity.MINOR, message=""),
    ]
    counts = severity_counts(issues)
    assert counts["critical"] == 2
    assert counts["major"] == 1
    assert counts["minor"] == 1
    assert counts["total"] == 4


def test_grade_thresholds():
    assert grade(95) == "A"
    assert grade(80) == "B"
    assert grade(60) == "C"
    assert grade(30) == "D"
    assert grade(0) == "D"
