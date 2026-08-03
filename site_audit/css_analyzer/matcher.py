"""Match visual issues to CSS rules by selector and color."""

from collections import defaultdict
from typing import Dict, List
from ..models.issue import Issue
from .parser import CSSRule, normalize_color


def _selector_matches(css_selector: str, element_selector: str) -> bool:
    """Check if a CSS selector covers the given element selector."""
    sel = css_selector.strip()
    elem = element_selector.strip()
    if sel == elem:
        return True
    parts = sel.split()
    for part in parts:
        p_clean = part.strip().lstrip(">+~").strip()
        if p_clean == elem:
            return True
    if "." in elem:
        elem_classes = elem.split(".")[1:]
        for cls in elem_classes:
            if cls and f".{cls}" in sel:
                return True
    return False


def match_issues_to_rules(issues: List[Issue], rules: List[CSSRule]) -> Dict[str, List[CSSRule]]:
    """Group visual issues by their color hex → matching CSS rules."""
    matches: Dict[str, List[CSSRule]] = defaultdict(list)
    for issue in issues:
        if issue.rule != "visual/contrast":
            continue
        data = issue.data or {}
        selector = data.get("selector", "")
        fg_hex = normalize_color(data.get("fg", ""))
        if not fg_hex:
            continue
        for rule in rules:
            resolved = rule.resolved_value or rule.value
            rule_color = normalize_color(resolved)
            if rule_color and rule_color == fg_hex and _selector_matches(rule.selector, selector):
                matches[fg_hex].append(rule)
    return dict(matches)


def enrich_issues(issues: List[Issue], rules: List[CSSRule]) -> List[Issue]:
    """Add css_token, css_rule, source_file to issues that can be matched."""
    rule_index: Dict[str, List[CSSRule]] = defaultdict(list)
    for rule in rules:
        c = normalize_color(rule.resolved_value or rule.value)
        if c:
            rule_index[c].append(rule)

    enriched: List[Issue] = []
    for issue in issues:
        if issue.rule == "visual/contrast":
            data = dict(issue.data or {})
            fg_hex = normalize_color(data.get("fg", ""))
            sel = data.get("selector", "")
            if fg_hex and fg_hex in rule_index:
                for r in rule_index[fg_hex]:
                    if _selector_matches(r.selector, sel):
                        data["css_token"] = fg_hex
                        data["css_rule"] = r.selector
                        data["source_file"] = r.source_file
                        break
            # Replace issue data (immutable dataclass — recreate)
            enriched.append(Issue(
                rule=issue.rule, severity=issue.severity,
                message=issue.message, file=issue.file,
                line=issue.line, context=issue.context,
                suggestion=issue.suggestion,
                evidence_path=issue.evidence_path, data=data,
            ))
        else:
            enriched.append(issue)
    return enriched