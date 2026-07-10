"""Data models for site audit issues."""

from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict
from enum import Enum


class Severity(Enum):
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"

    def score_penalty(self) -> int:
        return {"critical": 10, "major": 3, "minor": 1}.get(self.value, 1)


@dataclass
class Issue:
    rule: str
    severity: Severity
    message: str
    file: str = ""
    line: int = 0
    context: str = ""
    suggestion: str = ""
    evidence_path: str = ""
    data: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["severity"] = self.severity.value
        return d

    def fingerprint(self) -> str:
        """Stable identifier for dedup across scans.

        Source issues: rule:file:line
        Visual issues:  rule:selector:fg:bg (contrast) or rule:page:selector:width (overflow)
        """
        rule = self.rule
        if rule.startswith("visual/"):
            if rule == "visual/contrast" and self.data:
                sel = self.data.get("selector", self.context)[:60]
                fg = self.data.get("fg", "?")
                bg = self.data.get("bg", "?")
                ratio = round(self.data.get("ratio", 0), 1)
                return f"contrast:{sel}:{fg}:{bg}:{ratio}"
            if rule == "visual/overflow" and self.data:
                page = self.file[:60]
                sel = self.data.get("selector", "?")
                w = self.data.get("width", "?")
                return f"overflow:{page}:{sel}:{w}"
            if rule == "visual/font-size" and self.data:
                return f"fontsize:{self.context[:50]}:{self.data.get('fontSize','?')}"
            return f"{rule}:{self.file}:{self.context[:40]}"

        # Source issue
        return f"{rule}:{self.file}:{self.line}"


@dataclass
class AuditSummary:
    timestamp: str = ""
    target: str = ""
    files_scanned: int = 0
    pages_scanned: int = 0
    score: int = 100
    issue_count: int = 0
    source_layer_issues: List[Issue] = field(default_factory=list)
    visual_layer_issues: List[Issue] = field(default_factory=list)
    summary_by_selector: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        d = {
            "timestamp": self.timestamp,
            "target": self.target,
            "files_scanned": self.files_scanned,
            "pages_scanned": self.pages_scanned,
            "score": self.score,
            "issue_count": self.issue_count,
            "source_layer_issues": [i.to_dict() for i in self.source_layer_issues],
            "visual_layer_issues": [i.to_dict() for i in self.visual_layer_issues],
            "summary_by_selector": self.summary_by_selector,
        }
        return d
