"""CSS Cascade Resolution — selector-first matching strategy.

Connects DOM computed styles to CSS source rules using:
1. Selector matching (tag, class, id, descendant, specificity)
2. Property existence confirmation
3. Variable trace (when the selector resolves via var())
4. Color-delta analysis (reported but NOT a match criterion)

Confidence levels: HIGH / MEDIUM / LOW / UNKNOWN
"""

import math
import re
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

from ..models.issue import Issue
from .parser import CSSRule, normalize_color, parse_all_css, _HEX_RE
from .variables import resolve_all_var_references, VariableScope, build_scope, resolve_value
from .source_index import SourceIndex, build_source_index, SelectorEntry
from .selector_match import find_best_match, specificity, parse_element_selector


class MappingResult:
    """Result of resolving one visual issue to a CSS source rule."""

    def __init__(self, issue_selector: str, computed_color: str):
        self.issue_selector = issue_selector
        self.computed_color = computed_color
        self.css_source_file = ""
        self.css_selector = ""
        self.css_line = 0
        self.variable = ""
        self.variable_resolved = ""
        self.source_color = ""
        self.specificity = 0
        self.confidence = "UNKNOWN"  # HIGH / MEDIUM / LOW / UNKNOWN
        self.color_delta = ""  # "exact" / "close" / "different" / "unknown"
        self.color_status = "unknown"
        self.theme = ""

    def to_dict(self) -> dict:
        return {
            "issue_selector": self.issue_selector,
            "computed_color": self.computed_color,
            "css_source_file": self.css_source_file,
            "css_selector": self.css_selector,
            "css_line": self.css_line,
            "variable": self.variable,
            "variable_resolved": self.variable_resolved,
            "source_color": self.source_color,
            "specificity": self.specificity,
            "confidence": self.confidence,
            "color_delta": self.color_delta,
            "color_status": self.color_status,
            "theme": self.theme,
        }


_COLOR_DELTA_THRESHOLD = 20  # channel difference below which is "close"


def color_delta(hex1: str, hex2: str) -> Tuple[int, str]:
    """Compute per-channel difference between two hex colors.

    Returns (max_channel_delta, label) where label is:
    - "exact": hex1 == hex2
    - "close": max delta < _COLOR_DELTA_THRESHOLD
    - "different": max delta >= _COLOR_DELTA_THRESHOLD
    - "unknown": can't parse
    """
    try:
        h1 = hex1.lstrip("#").lower()
        h2 = hex2.lstrip("#").lower()
        if len(h1) == 3:
            h1 = "".join(c * 2 for c in h1)
        if len(h2) == 3:
            h2 = "".join(c * 2 for c in h2)
        if len(h1) != 6 or len(h2) != 6:
            return (999, "unknown")

        r1, g1, b1 = int(h1[:2], 16), int(h2[2:4], 16), int(h1[4:], 16)
        r2, g2, b2 = int(h2[:2], 16), int(h2[2:4], 16), int(h2[4:], 16)

        max_delta = max(abs(r1 - r2), abs(g1 - g2), abs(b1 - b2))

        if h1 == h2:
            return (0, "exact")
        elif max_delta < _COLOR_DELTA_THRESHOLD:
            return (max_delta, "close")
        else:
            return (max_delta, "different")
    except (ValueError, IndexError):
        return (999, "unknown")


class CascadeReport:
    """Report with cascade mapping statistics and confidence distribution."""

    def __init__(self):
        self.total_issues = 0
        self.mapped = 0  # All confidence levels except UNKNOWN
        self.confidence_counts: Dict[str, int] = {"HIGH": 0, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0}
        self.matched_details: List[MappingResult] = []
        self.unmatched: List[Issue] = []

    @property
    def mapped_accuracy(self) -> float:
        if self.total_issues == 0:
            return 1.0
        return self.mapped / self.total_issues

    def to_dict(self) -> dict:
        return {
            "total_issues": self.total_issues,
            "mapped": self.mapped,
            "unmatched_count": len(self.unmatched),
            "mapped_accuracy": f"{round(self.mapped_accuracy * 100, 1)}%",
            "confidence_distribution": self.confidence_counts,
        }


class CascadeResolver:
    """Resolves computed styles back to CSS source rules (selector-first)."""

    def __init__(self, public_dir: str):
        self.public_dir = public_dir
        self.all_rules: List[CSSRule] = []
        self.var_scope: Optional[VariableScope] = None
        self.source_index: Optional[SourceIndex] = None
        self.resolved_rules: List[CSSRule] = []
        self._loaded = False

    def load(self):
        if self._loaded:
            return
        self.all_rules = parse_all_css(self.public_dir)
        self.var_scope = build_scope(self.all_rules)
        self.source_index = build_source_index(self.all_rules)
        self.resolved_rules = resolve_all_var_references(self.all_rules)
        self._loaded = True

    def resolve_issue(self, issue: Issue) -> Optional[MappingResult]:
        """Resolve a visual issue to its most likely CSS source rule.

        Strategy: selector-first → property match → specificity → color-delta
        """
        if issue.rule != "visual/contrast":
            return None

        data = issue.data or {}
        element_selector = data.get("selector", "")
        computed_color = normalize_color(data.get("fg", ""))

        if not element_selector or not computed_color:
            return None

        result = MappingResult(element_selector, computed_color)

        # Phase 1: Find matching CSS rules by selector
        if self.source_index:
            matches = find_best_match(element_selector, self.source_index, "color")
        else:
            matches = []

        if not matches:
            # Fallback: try direct color search in resolved rules
            for rule in self.resolved_rules:
                rule_color = normalize_color(rule.resolved_value or rule.value)
                if rule_color == computed_color:
                    sp = specificity(rule.selector)
                    matches.append((SelectorEntry(rule.selector, rule.source_file,
                                                  rule.line, {"color": rule.resolved_value or rule.value}),
                                    sp, 0))

        if matches:
            best_entry, best_spec, _ = matches[0]
            result.css_source_file = best_entry.source_file
            result.css_selector = best_entry.selector
            result.css_line = best_entry.line
            result.specificity = best_spec

            source_raw = best_entry.properties.get("color", "")
            result.source_color = normalize_color(source_raw) or source_raw

            # Variable trace
            if "var(" in source_raw:
                var_name = _extract_var(source_raw)
                if var_name:
                    result.variable = var_name
                    if self.var_scope:
                        resolved = self.var_scope.resolve(var_name)
                        result.variable_resolved = resolved or ""

            # Color delta (informational only)
            if computed_color and result.source_color:
                delta, label = color_delta(computed_color, result.source_color)
                result.color_delta = label
                if label == "exact":
                    result.color_status = "match"
                elif label == "close":
                    result.color_status = "cascade-adjusted"
                else:
                    result.color_status = f"cascade-adjusted (delta~{delta})"

            # Theme detection
            if ".dark" in best_entry.selector or "[data-theme" in best_entry.selector:
                result.theme = "dark"
            elif "@media" in best_entry.selector and "dark" in best_entry.selector:
                result.theme = "dark"

            # Set confidence
            if result.variable:
                # Selector + variable trace is always HIGH — we know the source
                result.confidence = "HIGH"
            elif result.color_delta == "exact":
                result.confidence = "HIGH"
            elif result.color_delta == "close":
                result.confidence = "MEDIUM"
            else:
                # Selector match but color cascade-adjusted: LOW
                result.confidence = "LOW"

            return result

        # Phase 2: No selector match — try theme-based (dark mode) fallback
        for rule in self.resolved_rules:
            if ".dark" in rule.selector or "[data-theme" in rule.selector:
                rule_color = normalize_color(rule.resolved_value or rule.value)
                if rule_color and color_delta(computed_color, rule_color)[0] < 10:
                    result.css_source_file = rule.source_file
                    result.css_selector = rule.selector
                    result.css_line = rule.line
                    result.source_color = rule_color
                    result.theme = "dark"
                    result.confidence = "LOW"
                    result.color_delta = "close"
                    return result

        return None

    def batch_resolve(self, issues: List[Issue]) -> CascadeReport:
        report = CascadeReport()
        report.total_issues = len(issues)

        for issue in issues:
            result = self.resolve_issue(issue)
            if result and result.confidence != "UNKNOWN":
                report.mapped += 1
                report.confidence_counts[result.confidence] += 1
                report.matched_details.append(result)
            else:
                report.unmatched.append(issue)

        return report


def _extract_var(value: str) -> str:
    m = re.search(r"var\((--[\w-]+)", value)
    return m.group(1) if m else ""


def dark_mode_rules(rules: List[CSSRule]) -> List[CSSRule]:
    return [r for r in rules if ".dark" in r.selector or "[data-theme" in r.selector
            or ("@media" in r.selector and "dark" in r.selector)]


def light_mode_rules(rules: List[CSSRule]) -> List[CSSRule]:
    return [r for r in rules
            if ".dark" not in r.selector and "[data-theme" not in r.selector
            and not ("@media" in r.selector and "dark" in r.selector)]