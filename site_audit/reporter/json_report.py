"""JSON report generation (v1.0 unified format)."""

import json
from pathlib import Path
from typing import Dict, List, Optional

from ..models.issue import Issue, AuditSummary, Severity
from ..models.evidence import Report as UnifiedReport, issue_to_evidence
from ..scoring.score import severity_counts


def generate_json(summary: AuditSummary, output_path: str,
                  css_token_issues: Optional[List[Dict]] = None) -> Path:
    """Write the audit report as JSON (legacy v0.x format).

    Kept for backward compatibility. New code should use generate_report().
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = summary.to_dict()
    if css_token_issues:
        data["css_token_issues"] = css_token_issues
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def generate_report(report: UnifiedReport, output_path: str) -> Path:
    """Write the audit report as JSON in v1.0 unified format.

    Args:
        report: Unified Report with Evidence[] array
        output_path: Where to write the JSON file
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = report.to_dict()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path