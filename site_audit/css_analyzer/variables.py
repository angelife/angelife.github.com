"""Enhanced CSS variable resolver — recursive resolution, local scope, depth 5."""

import re
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

from .parser import CSSRule, normalize_color


_VAR_REF_RE = re.compile(r"var\((--[\w-]+)(?:\s*,\s*([^)]+))?\)")
_MAX_DEPTH = 5


class VariableScope:
    """Variable definitions with theme context."""

    def __init__(self):
        # { variable_name: (value, selector, source_file, line) }
        self._all: Dict[str, Tuple[str, str, str, int]] = {}
        # { variable_name: is_dark_theme }
        self._theme: Dict[str, bool] = {}

    def add_definition(self, var_name: str, value: str, selector: str,
                       source_file: str, line: int):
        self._all[var_name] = (value, selector, source_file, line)
        is_dark = ".dark" in selector or "[data-theme" in selector or "dark" in selector
        self._theme[var_name] = is_dark

    def resolve(self, var_name: str, context_selector: str = "") -> Optional[str]:
        if var_name in self._all:
            return self._all[var_name][0]
        return None

    def resolve_with_theme(self, var_name: str, theme: str = "light") -> Optional[Tuple[str, bool]]:
        """Resolve with theme awareness. Returns (value, is_dark) or None."""
        if var_name in self._all:
            is_dark = self._theme.get(var_name, False)
            return (self._all[var_name][0], is_dark)
        return None

    def all_global(self) -> Dict[str, str]:
        return {k: v[0] for k, v in self._all.items() if not self._theme.get(k, False)}

    def all_theme(self, is_dark: bool = True) -> Dict[str, str]:
        return {k: v[0] for k, v in self._all.items() if self._theme.get(k, False) == is_dark}


# Backward-compatible aliases — kept here for call-time resolution (lazy lambda)
build_variable_graph = lambda rules: {k: v[0] for k, v in build_scope(rules)._all.items()}
filter_color_rules = lambda rules: [r for r in rules
                                    if r.property in {"color", "background", "background-color",
                                                      "border-color", "outline-color",
                                                      "text-decoration-color", "fill", "stroke"}]
# resolve_all_variables goes at file end (needs resolve_all_var_references defined first)


def build_scope(rules: List[CSSRule]) -> VariableScope:
    """Build a VariableScope from parsed CSS rules."""
    scope = VariableScope()
    for rule in rules:
        if not rule.property.startswith("--"):
            continue
        scope.add_definition(
            rule.property, rule.value.strip(),
            rule.selector, rule.source_file, rule.line,
        )
    return scope


def resolve_value(value: str, scope: VariableScope,
                  context_selector: str = "", depth: int = 0) -> str:
    """Recursively resolve all var() references in a CSS value.

    Args:
        value: The CSS value potentially containing var() calls
        scope: VariableScope with definitions
        context_selector: The selector context for local variable lookup
        depth: Current recursion depth (internal)

    Returns:
        Resolved value with all var() expanded
    """
    if depth > _MAX_DEPTH:
        return value

    def _replace(m: re.Match) -> str:
        name = m.group(1)
        fallback = m.group(2)
        resolved = scope.resolve(name, context_selector)
        if resolved is not None:
            # Recurse in case the resolved value itself contains var()
            return resolve_value(resolved, scope, context_selector, depth + 1)
        if fallback is not None:
            # Fallback might also contain var()
            return resolve_value(fallback.strip(), scope, context_selector, depth + 1)
        return f"var({name})"

    return _VAR_REF_RE.sub(_replace, value)


def resolve_all_var_references(rules: List[CSSRule]) -> List[CSSRule]:
    """Resolve var() references for all rules using enhanced scope.

    Returns rules with resolved_value set.
    """
    scope = build_scope(rules)

    # Pre-resolve all variable definitions (depth-first)
    for name in list(scope._all.keys()):
        val = scope._all[name][0]
        resolved = resolve_value(val, scope)
        if resolved != val:
            scope._all[name] = (resolved, scope._all[name][1],
                                scope._all[name][2], scope._all[name][3])

    # Resolve all color rules
    resolved_rules = []
    for rule in rules:
        if rule.property.startswith("--"):
            continue
        if rule.property not in {"color", "background", "background-color",
                                  "border-color", "outline-color",
                                  "text-decoration-color", "fill", "stroke"}:
            continue
        if "var(" not in rule.value:
            continue

        resolved_val = resolve_value(rule.value, scope, rule.selector)
        if resolved_val != rule.value:
            resolved_rules.append(CSSRule(
                selector=rule.selector,
                property=rule.property,
                value=rule.value,
                source_file=rule.source_file,
                line=rule.line,
                resolved_value=resolved_val,
            ))

    return resolved_rules


# Backward-compat: old API was resolve_all_variables(rules, var_map)
def resolve_all_variables(rules, var_map=None):
    """Resolve all var() references. Old signature accepted (rules, var_map)."""
    return resolve_all_var_references(rules)