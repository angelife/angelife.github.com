"""Main scanner orchestration."""

from pathlib import Path
from typing import List

from ..models.issue import Issue, Severity
from .markdown import scan
from .headings import check_heading_levels, check_heading_spacing
from .spacing import check_spacing


def scan_source(path: str) -> List[Issue]:
    """Run all source-layer audits on the project at `path`.

    Returns a flat list of issues.
    """
    all_issues: List[Issue] = []
    parsed = scan(path)

    for file_path, tokens in parsed:
        # Heading hierarchy
        all_issues.extend(check_heading_levels(file_path, tokens))
        all_issues.extend(check_heading_spacing(file_path, tokens))

        # CJK spacing on raw content
        try:
            raw = file_path.read_text(encoding="utf-8")
            all_issues.extend(check_spacing(file_path, raw))
        except Exception as e:
            print(f"  [WARN] spacing scan failed for {file_path}: {e}")

    return all_issues
