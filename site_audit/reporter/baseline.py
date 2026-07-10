"""Baseline comparison — diff new audit against a stored baseline."""

import json
from pathlib import Path
from typing import List, Tuple

from ..models.issue import Issue


def save_baseline(issues: list, path: str) -> None:
    """Save issue fingerprints as a baseline JSON file."""
    fingerprints = [i.fingerprint() for i in issues]
    data = {
        "format": "site-audit-baseline-v1",
        "count": len(fingerprints),
        "fingerprints": sorted(set(fingerprints)),
    }
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def load_baseline(path: str) -> list:
    """Load a baseline JSON file and return list of fingerprints.

    Supports both baseline format and old report format.
    """
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        if data.get("format") == "site-audit-baseline-v1":
            return data.get("fingerprints", [])
        # Old report format
        fps = []
        for issue in data.get("source_layer_issues", []) + data.get("visual_layer_issues", []):
            if isinstance(issue, dict):
                fps.append(_legacy_fingerprint(issue))
        return fps

    # Old format: just a list of fingerprints
    return data


def filter_new_issues(issues: List[Issue], baseline_fingerprints: list) -> Tuple[list, int]:
    """Filter out issues that exist in the baseline.

    Returns (new_issues, matched_count).
    """
    baseline_set = set(baseline_fingerprints)
    new = []
    matched = 0
    for i in issues:
        fp = i.fingerprint()
        if fp in baseline_set:
            matched += 1
        else:
            new.append(i)
    return new, matched


def aggregate_by_selector(issues: List[Issue]) -> dict:
    """Group visual issues by selector/rule for summary."""
    groups = {}
    for i in issues:
        key = i.rule
        if i.data:
            sel = i.data.get("selector") or i.data.get("page", "")
            if sel:
                key = f"{i.rule}:{sel}"
        groups[key] = groups.get(key, 0) + 1
    return groups


def _legacy_fingerprint(issue: dict) -> str:
    """Create fingerprint from a legacy report dict."""
    rule = issue.get("rule", "")
    file = issue.get("file", "")
    line = issue.get("line", 0)
    if rule.startswith("visual/"):
        ctx = issue.get("context", "")[:40]
        return f"{rule}:{file}:{ctx}"
    return f"{rule}:{file}:{line}"
