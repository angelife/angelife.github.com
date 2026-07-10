"""Unified Evidence Model — single data model for all analyzers.

v1.0 Architecture:
  All analyzers (source, visual, CSS, typography, overflow)
  produce Evidence. All consumers (report, patch, HTML inspector)
  read Evidence.

This replaces the v0.x pattern where each analyzer had its own
Issue/Data/Result struct.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime


# ═══════════════════════════════════════════════════
# Enums
# ═══════════════════════════════════════════════════

class EvidenceKind(str, Enum):
    """What kind of analyzer produced this evidence."""
    SOURCE = "source"          # Markdown scanner
    VISUAL = "visual"          # Render-layer contrast/overflow/font
    CSS_TOKEN = "css_token"    # CSS Design Token audit
    CASCADE = "cascade"        # CSS Cascade resolution


class Severity(str, Enum):
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    INFO = "info"


class Confidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"


class AnalyzerKind(str, Enum):
    MARKDOWN = "markdown"
    CONTRAST = "contrast"
    OVERFLOW = "overflow"
    FONT_SIZE = "font_size"
    CSS_TOKEN = "css_token"
    CASCADE = "cascade"


# ═══════════════════════════════════════════════════
# Location — where in source/HTML the evidence lives
# ═══════════════════════════════════════════════════

@dataclass
class SourceLocation:
    """Location in a source file."""
    file: str = ""
    line: int = 0
    column: int = 0


# ═══════════════════════════════════════════════════
# Element — DOM node identity
# ═══════════════════════════════════════════════════

@dataclass
class ElementInfo:
    """DOM element that the evidence relates to."""
    tag: str = ""
    id: str = ""
    classes: List[str] = field(default_factory=list)
    css_path: str = ""             # e.g. "body > main > article > h1"
    ancestor_chain: List[Dict] = field(default_factory=list)  # [{tag, id, classes}]

    def to_dict(self) -> dict:
        return {
            "tag": self.tag,
            "id": self.id,
            "classes": list(self.classes),
            "css_path": self.css_path,
            "ancestor_chain": list(self.ancestor_chain),
        }


# ═══════════════════════════════════════════════════
# Computed — browser-computed values (render layer)
# ═══════════════════════════════════════════════════

@dataclass
class ComputedInfo:
    """Browser-computed property values."""
    property: str = ""
    value: str = ""
    color: str = ""
    background_color: str = ""
    font_size: str = ""
    font_weight: str = ""
    opacity: str = ""
    line_height: str = ""

    def to_dict(self) -> dict:
        return {
            "property": self.property,
            "value": self.value,
            "color": self.color,
            "background_color": self.background_color,
            "font_size": self.font_size,
            "font_weight": self.font_weight,
            "opacity": self.opacity,
            "line_height": self.line_height,
        }


# ═══════════════════════════════════════════════════
# Source — CSS source rule (static analysis)
# ═══════════════════════════════════════════════════

@dataclass
class SourceInfo:
    """CSS source rule that affects the element."""
    css_file: str = ""
    selector: str = ""
    property: str = ""
    value: str = ""
    variable_chain: List[str] = field(default_factory=list)
    resolved_value: str = ""
    specificity: str = ""   # "(a,b,c)" string
    line: int = 0

    def to_dict(self) -> dict:
        return {
            "css_file": self.css_file,
            "selector": self.selector,
            "property": self.property,
            "value": self.value,
            "variable_chain": list(self.variable_chain),
            "resolved_value": self.resolved_value,
            "specificity": self.specificity,
            "line": self.line,
        }


# ═══════════════════════════════════════════════════
# Finding — what the analyzer detected
# ═══════════════════════════════════════════════════

@dataclass
class Finding:
    """The diagnostic finding."""
    rule: str = ""               # e.g. "visual/contrast", "source/heading-order"
    severity: str = "info"       # critical / major / minor / info
    confidence: str = "low"      # high / medium / low / unknown
    message: str = ""
    suggestion: str = ""

    def to_dict(self) -> dict:
        return {
            "rule": self.rule,
            "severity": self.severity,
            "confidence": self.confidence,
            "message": self.message,
            "suggestion": self.suggestion,
        }


# ═══════════════════════════════════════════════════
# Recommendation — actionable fix
# ═══════════════════════════════════════════════════

@dataclass
class Recommendation:
    """An actionable fix recommendation."""
    patch: str = ""              # CSS patch code
    file: str = ""               # target file
    line: int = 0
    description: str = ""

    def to_dict(self) -> dict:
        return {
            "patch": self.patch,
            "file": self.file,
            "line": self.line,
            "description": self.description,
        }


# ═══════════════════════════════════════════════════
# Evidence — single unified evidence record
# ═══════════════════════════════════════════════════

@dataclass
class Evidence:
    """Single atomic evidence record from any analyzer.

    Every analyzer (source, visual, CSS) produces this.
    Every consumer (report, HTML inspector, CI gate) reads this.
    """
    # Identity
    id: str = ""
    kind: str = ""               # source / visual / css_token / cascade
    analyzer: str = ""           # markdown / contrast / overflow / css_token

    # Context
    page: str = ""
    viewport: str = ""
    theme: str = "light"
    timestamp: str = ""

    # Element (DOM)
    element: ElementInfo = field(default_factory=ElementInfo)

    # Computed (browser)
    computed: ComputedInfo = field(default_factory=ComputedInfo)

    # Source (CSS)
    source: SourceInfo = field(default_factory=SourceInfo)

    # Finding
    finding: Finding = field(default_factory=Finding)

    # Recommendation
    recommendation: Recommendation = field(default_factory=Recommendation)

    # Free-form metadata (analyzer-specific)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "kind": self.kind,
            "analyzer": self.analyzer,
            "page": self.page,
            "viewport": self.viewport,
            "theme": self.theme,
            "timestamp": self.timestamp,
            "element": self.element.to_dict() if self.element else {},
            "computed": self.computed.to_dict() if self.computed else {},
            "source": self.source.to_dict() if self.source else {},
            "finding": self.finding.to_dict() if self.finding else {},
            "recommendation": self.recommendation.to_dict() if self.recommendation else {},
            "metadata": dict(self.metadata),
        }


# ═══════════════════════════════════════════════════
# Report — top-level report structure
# ═══════════════════════════════════════════════════

@dataclass
class ReportMetadata:
    """Metadata about the scan."""
    version: str = "1.0"
    timestamp: str = ""
    target: str = ""
    duration_seconds: float = 0.0
    pages_scanned: int = 0
    files_scanned: int = 0

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "timestamp": self.timestamp,
            "target": self.target,
            "duration_seconds": self.duration_seconds,
            "pages_scanned": self.pages_scanned,
            "files_scanned": self.files_scanned,
        }


@dataclass
class Metrics:
    """Aggregated health metrics."""
    score: int = 100
    total_issues: int = 0
    by_severity: Dict[str, int] = field(default_factory=dict)
    by_analyzer: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "score": self.score,
            "total_issues": self.total_issues,
            "by_severity": dict(self.by_severity),
            "by_analyzer": dict(self.by_analyzer),
        }


@dataclass
class Report:
    """Unified site audit report."""
    metadata: ReportMetadata = field(default_factory=ReportMetadata)
    evidence: List[Evidence] = field(default_factory=list)
    metrics: Metrics = field(default_factory=Metrics)
    history: List[Dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "metadata": self.metadata.to_dict(),
            "evidence": [e.to_dict() for e in self.evidence],
            "metrics": self.metrics.to_dict(),
            "history": list(self.history),
        }


def build_dom_evidence(raw: dict, element_index: int) -> Evidence:
    """Convert raw JS evaluate output to v1.0 Evidence (backward compat).

    This is the Phase 8A factory function — converts browser-side
    JavaScript evaluation results into structured evidence.
    """
    ancestors = []
    for a in raw.get("ancestors", []):
        ancestors.append({
            "tag": a.get("tag", ""),
            "id": a.get("id", ""),
            "classes": list(a.get("classes", [])),
        })

    comp = raw.get("computed", {})
    computed = ComputedInfo(
        color=comp.get("color", ""),
        background_color=comp.get("background_color", ""),
        font_size=comp.get("font_size", ""),
        font_weight=comp.get("font_weight", ""),
        opacity=comp.get("opacity", ""),
        line_height=comp.get("line_height", ""),
    )

    class_list = list(raw.get("classList", []))
    selector = raw.get("selector", "")
    css_path = raw.get("cssPath", "")

    element = ElementInfo(
        tag=raw.get("tag", ""),
        id=raw.get("id", ""),
        classes=class_list,
        css_path=css_path,
        ancestor_chain=ancestors,
    )

    return Evidence(
        kind="visual",
        analyzer="contrast",
        element=element,
        computed=computed,
    )


# ═══════════════════════════════════════════════════
# Backward-compat conversion helpers
# ═══════════════════════════════════════════════════

def issue_to_evidence(old_issue: Any) -> Evidence:
    """Convert a v0.x Issue to v1.0 Evidence.

    Used during migration so both old and new consumers work.
    """
    data = getattr(old_issue, "data", {}) or {}
    ev = Evidence(
        id=old_issue.fingerprint() if hasattr(old_issue, "fingerprint") else "",
        kind=_infer_kind(old_issue.rule),
        page=old_issue.file if hasattr(old_issue, "file") else "",
        finding=Finding(
            rule=old_issue.rule if hasattr(old_issue, "rule") else "",
            severity=old_issue.severity.value if hasattr(old_issue, "severity") else "info",
            message=old_issue.message if hasattr(old_issue, "message") else "",
            suggestion=old_issue.suggestion if hasattr(old_issue, "suggestion") else "",
        ),
        element=ElementInfo(
            tag="",
            classes=[],
            css_path=data.get("selector", ""),
        ),
        computed=ComputedInfo(
            color=data.get("fg", ""),
            background_color=data.get("bg", ""),
            font_size=data.get("fontSize", ""),
        ),
        recommendation=Recommendation(
            file=old_issue.file if hasattr(old_issue, "file") else "",
        ),
        metadata={"old_line": old_issue.line if hasattr(old_issue, "line") else 0},
    )
    return ev


def _infer_kind(rule: str) -> str:
    if rule.startswith("visual/"):
        return "visual"
    if rule.startswith("css/"):
        return "css_token"
    if rule.startswith("source/") or rule.startswith("heading") or rule.startswith("spacing"):
        return "source"
    return "source"