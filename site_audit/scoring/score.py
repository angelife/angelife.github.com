"""Scoring system — computes site health score.

Scoring rules (graded normalized):
  critical:  -10 each, max -50
  major:      -3 each, max -30
  minor:      -1 per 100 issues, max -20

Score ranges:
  90-100  ✅ Excellent
  70-89   ⚠️  Needs improvement
  50-69   🔴 Poor
  <50     ❌ Critical
"""

from typing import List
from ..models.issue import Issue, Severity

INITIAL_SCORE = 100

# Max penalties per severity (capped)
MAX_PENALTY = {
    Severity.CRITICAL: 50,  # -10 each, max 50
    Severity.MAJOR: 30,     # -3 each, max 30
    Severity.MINOR: 20,     # -1 per 100 issues, max 20
}

PENALTY_PER_ISSUE = {
    Severity.CRITICAL: 10,
    Severity.MAJOR: 3,
    Severity.MINOR: 0.01,  # -1 per 100 issues
}


def compute_score(issues: List[Issue]) -> int:
    """Compute overall audit score from 0-100 with capped severity penalties."""
    penalty = 0

    # critical: -10 each, capped at -50
    n_critical = sum(1 for i in issues if i.severity == Severity.CRITICAL)
    penalty += min(n_critical * 10, MAX_PENALTY[Severity.CRITICAL])

    # major: -3 each, capped at -30
    n_major = sum(1 for i in issues if i.severity == Severity.MAJOR)
    penalty += min(n_major * 3, MAX_PENALTY[Severity.MAJOR])

    # minor: -1 per 100, capped at -20
    n_minor = sum(1 for i in issues if i.severity == Severity.MINOR)
    penalty += min(n_minor // 100, MAX_PENALTY[Severity.MINOR])

    score = max(INITIAL_SCORE - penalty, 0)
    return score


def severity_counts(issues: List[Issue]) -> dict:
    """Count issues by severity level."""
    return {
        "critical": sum(1 for i in issues if i.severity == Severity.CRITICAL),
        "major": sum(1 for i in issues if i.severity == Severity.MAJOR),
        "minor": sum(1 for i in issues if i.severity == Severity.MINOR),
        "total": len(issues),
    }


def grade(score: int) -> str:
    """Return letter grade for a score."""
    if score >= 90:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 50:
        return "C"
    else:
        return "D"
