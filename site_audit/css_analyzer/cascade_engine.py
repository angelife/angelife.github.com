"""CSS Cascade Engine — simulate browser cascade ordering.

DOM
 ↓
all matching rules (selector match)
 ↓
cascade ordering (important → specificity → source order)
 ↓
winning declaration + variable resolution
 ↓
source evidence
"""

import re
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from ..models.issue import Issue
from .parser import CSSRule, normalize_color, parse_all_css, _HEX_RE
from .variables import resolve_all_var_references, VariableScope, build_scope
from .source_index import SourceIndex, build_source_index, SelectorEntry
from .selector_match import selector_contains, parse_element_selector, match_selector
from .specificity import specificity as compute_spec

# ── Media Query Support ──────────────────────────────────────────────

_MEDIA_FEATURE_RE = re.compile(r'\(([^)]+)\)')


@dataclass
class MediaCondition:
    """Parsed media condition with viewport range."""
    min_width: int = 0
    max_width: int = 99999
    prefers_dark: Optional[bool] = None  # None = not specified


def parse_media_query(media_text: str) -> MediaCondition:
    """Parse a media query string into a MediaCondition."""
    cond = MediaCondition()
    features = _MEDIA_FEATURE_RE.findall(media_text)
    for feat in features:
        if 'prefers-color-scheme' in feat:
            cond.prefers_dark = 'dark' in feat
        elif 'min-width' in feat:
            m = re.search(r'min-width\s*:\s*(\d+)', feat)
            if m:
                cond.min_width = int(m.group(1))
        elif 'max-width' in feat:
            m = re.search(r'max-width\s*:\s*(\d+)', feat)
            if m:
                cond.max_width = int(m.group(1))
    return cond


def media_is_active(cond: MediaCondition, viewport: Tuple[int, int] = (0, 0),
                    prefers_dark: bool = False) -> bool:
    """Check if a media condition is active for given viewport and theme."""
    width = viewport[0] if viewport else 9999
    if width < cond.min_width or width > cond.max_width:
        return False
    if cond.prefers_dark is not None and cond.prefers_dark != prefers_dark:
        return False
    return True


def media_text_matches(media_text: str, viewport: Tuple[int, int],
                       prefers_dark: bool) -> bool:
    """Convenience: parse and check in one step."""
    return media_is_active(parse_media_query(media_text), viewport, prefers_dark)


# ── Theme Context ────────────────────────────────────────────────────

@dataclass
class ThemeContext:
    theme: str = "light"  # "light" | "dark"
    viewport: Tuple[int, int] = (375, 812)  # (width, height) in CSS pixels


def theme_selectors_matched(rule: CSSRule, ctx: ThemeContext) -> bool:
    """Check if a rule's selector matches the theme context."""
    sel = rule.selector
    if ctx.theme == "dark":
        if ".dark" in sel or "[data-theme" in sel:
            return True
        if "@media" in sel and "dark" in sel:
            return True
        return True  # Allow non-themed rules in dark mode too
    else:
        if ".dark" in sel or "[data-theme" in sel:
            return False  # Only light-themed or neutral rules
        if "@media" in sel and "dark" in sel:
            return False
        return True


# ── Cascade Engine ───────────────────────────────────────────────────

@dataclass
class CascadeWinner:
    """Result of cascade resolution for one element + property."""
    selector: str = ""
    property: str = ""
    value: str = ""
    important: bool = False
    specificity: Tuple[int, int, int] = (0, 0, 0)
    source_file: str = ""
    source_line: int = 0
    source_order: int = 0
    media_context: str = ""
    variable_chain: List[str] = field(default_factory=list)
    resolved_value: str = ""
    confidence: str = "UNKNOWN"

    def to_dict(self) -> dict:
        return {
            "selector": self.selector,
            "property": self.property,
            "value": self.value,
            "important": self.important,
            "specificity": list(self.specificity),
            "source_file": self.source_file,
            "source_line": self.source_line,
            "variable_chain": self.variable_chain,
            "resolved_value": self.resolved_value,
            "confidence": self.confidence,
        }


@dataclass
class CascadeTrace:
    """Full cascade trace for one element + property."""
    element_selector: str = ""
    property_name: str = ""
    winner: Optional[CascadeWinner] = None
    overridden: List[CascadeWinner] = field(default_factory=list)
    matched_rules: int = 0
    computed_color: str = ""

    def to_dict(self) -> dict:
        return {
            "element": self.element_selector,
            "property": self.property_name,
            "computed_color": self.computed_color,
            "matched_rules": self.matched_rules,
            "winner": self.winner.to_dict() if self.winner else None,
            "overridden": [w.to_dict() for w in self.overridden],
        }


class CascadeEngine:
    """Full cascade resolution: selector match → cascade order → winner."""

    def __init__(self, public_dir: str):
        self.public_dir = public_dir
        self.all_rules: List[CSSRule] = []
        self.var_scope: Optional[VariableScope] = None
        self.source_index: Optional[SourceIndex] = None
        self.resolved_rules: List[CSSRule] = []
        self._loaded = False
        self._source_order_counter = 0

    def load(self):
        if self._loaded:
            return
        self.all_rules = parse_all_css(self.public_dir)
        # Assign source_order, compute specificity
        for rule in self.all_rules:
            rule.source_order = self._source_order_counter
            self._source_order_counter += 1
            a, b, c = compute_spec(rule.selector)
            rule.specificity_a = a
            rule.specificity_b = b
            rule.specificity_c = c
            # Detect !important
            if "!important" in rule.value:
                rule.important = True
                rule.value = rule.value.replace("!important", "").strip()

        self.var_scope = build_scope(self.all_rules)
        self.source_index = build_source_index(self.all_rules)
        self.resolved_rules = resolve_all_var_references(self.all_rules)
        self._loaded = True

    def resolve(self, element_selector: str, property_name: str = "color",
                computed_color: str = "",
                ctx: Optional[ThemeContext] = None) -> CascadeTrace:
        """Resolve an element+property through the cascade.

        Returns a CascadeTrace with winner, overridden rules, and variable chain.
        """
        if ctx is None:
            ctx = ThemeContext()

        trace = CascadeTrace()
        trace.element_selector = element_selector
        trace.property_name = property_name
        trace.computed_color = computed_color

        # Collect all matching rules
        candidates = []
        for rule in self.all_rules:
            if rule.property == property_name:
                if selector_contains(rule.selector, element_selector):
                    # Check theme context
                    if theme_selectors_matched(rule, ctx):
                        candidates.append(rule)
                    # Even if not theme-matched, still consider for overridden list

        # Also check resolved rules (variable-resolved values)
        resolved_candidates = []
        for rule in self.resolved_rules:
            if rule.property == property_name:
                if selector_contains(rule.selector, element_selector):
                    resolved_candidates.append(rule)

        trace.matched_rules = len(candidates)

        if not candidates:
            return trace

        # Sort by cascade key: !important(desc) > specificity(desc) > source_order(asc)
        winners = sorted(candidates, key=CSSRule.cascade_key)

        # The first in sorted order is the winner
        winner_rule = winners[0]

        # Build variable chain
        var_chain = []
        resolved_val = winner_rule.value
        current_val = winner_rule.value
        var_refs = re.findall(r'var\((--[\w-]+)', current_val)
        if var_refs:
            for var_name in var_refs:
                var_chain.append(var_name)
                # Trace through scope
                if self.var_scope:
                    res = self.var_scope.resolve(var_name)
                    if res:
                        var_chain.append(res)
                        resolved_val = res
                        # Check if resolved value itself contains var()
                        nested_vars = re.findall(r'var\((--[\w-]+)', res)
                        if nested_vars and len(var_chain) < 10:
                            for nv in nested_vars:
                                if nv not in var_chain:
                                    nr = self.var_scope.resolve(nv)
                                    if nr:
                                        var_chain.append(nv)
                                        var_chain.append(nr)
                                        resolved_val = nr

        # Build winner
        cw = CascadeWinner(
            selector=winner_rule.selector,
            property=winner_rule.property,
            value=winner_rule.value,
            important=winner_rule.important,
            specificity=winner_rule.specificity_tuple,
            source_file=winner_rule.source_file,
            source_line=winner_rule.line,
            source_order=winner_rule.source_order,
            media_context=winner_rule.media_context,
            variable_chain=var_chain,
            resolved_value=var_chain[-1] if var_chain else winner_rule.value,
        )

        # Confidence
        if var_chain:
            cw.confidence = "HIGH"
        elif winner_rule.source_order > 0 or winner_rule.specificity_tuple != (0, 0, 0):
            cw.confidence = "MEDIUM"
        else:
            cw.confidence = "LOW"

        trace.winner = cw

        # Collect overridden rules (everything that lost)
        for rule in winners[1:]:
            trace.overridden.append(CascadeWinner(
                selector=rule.selector,
                property=rule.property,
                value=rule.value,
                important=rule.important,
                specificity=rule.specificity_tuple,
                source_file=rule.source_file,
                source_line=rule.line,
                source_order=rule.source_order,
            ))

        return trace

    def batch_resolve(self, issues: List[Issue],
                      ctx: Optional[ThemeContext] = None) -> 'CascadeReport':
        """Resolve all visual issues and produce a CascadeReport."""
        report = CascadeReport()
        report.total_issues = len(issues)

        for issue in issues:
            if issue.rule != "visual/contrast":
                continue
            data = issue.data or {}
            element_selector = data.get("selector", "")
            computed_color = normalize_color(data.get("fg", ""))
            if not element_selector:
                report.unmatched.append(issue)
                continue

            trace = self.resolve(element_selector, "color", computed_color or "", ctx)
            if trace.winner:
                report.mapped += 1
                report.confidence_counts[trace.winner.confidence] += 1
                report.traces.append(trace)
            else:
                report.unmatched.append(issue)

        return report


@dataclass
class CascadeReport:
    total_issues: int = 0
    mapped: int = 0
    confidence_counts: Dict[str, int] = field(default_factory=lambda:
                                               {"HIGH": 0, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0})
    traces: List[CascadeTrace] = field(default_factory=list)
    unmatched: List[Issue] = field(default_factory=list)

    @property
    def mapped_accuracy(self) -> float:
        if self.total_issues == 0:
            return 1.0
        return self.mapped / self.total_issues

    def to_dict(self) -> dict:
        return {
            "total_issues": self.total_issues,
            "mapped": self.mapped,
            "accuracy": f"{self.mapped_accuracy*100:.1f}%",
            "confidence": self.confidence_counts,
        }