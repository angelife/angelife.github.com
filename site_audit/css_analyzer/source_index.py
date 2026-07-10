"""CSS Source Index — selector → file/line/properties lookup."""

from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .parser import CSSRule, _RULE_BLOCK_RE, _COMMENT_RE, _DECL_RE, _COLOR_PROPERTIES


class SelectorEntry:
    """Information about a CSS selector: where it's defined and what properties it sets."""

    def __init__(self, selector: str, source_file: str, line: int, properties: Dict[str, str]):
        self.selector = selector
        self.source_file = source_file
        self.line = line
        self.properties = properties

    def to_dict(self) -> dict:
        return {
            "selector": self.selector,
            "source_file": self.source_file,
            "line": self.line,
            "properties": self.properties,
        }


class SourceIndex:
    """Index of all CSS selectors with their source locations and properties."""

    def __init__(self):
        # raw_selector → SelectorEntry
        self._exact: Dict[str, SelectorEntry] = {}
        # class name → list of entries
        self._by_class: Dict[str, List[SelectorEntry]] = defaultdict(list)
        # tag name → list of entries
        self._by_tag: Dict[str, List[SelectorEntry]] = defaultdict(list)
        # id → list of entries
        self._by_id: Dict[str, List[SelectorEntry]] = defaultdict(list)

        # Theme context: selector → is_dark_theme
        self._theme_context: Dict[str, bool] = {}

        # Media query context per file
        self._media_contexts: Dict[str, List[str]] = defaultdict(list)

    def add_rule(self, rule: CSSRule):
        """Register a CSS rule in the index."""
        from .parser import normalize_color
        nv = rule.resolved_value or rule.value
        norm_val = normalize_color(nv) or nv
        sel = rule.selector
        if sel not in self._exact:
            self._exact[sel] = SelectorEntry(sel, rule.source_file, rule.line, {})
        self._exact[sel].properties[rule.property] = norm_val

        # Index by class
        classes = re.findall(r'\.([\w-]+)', sel)
        for cls in classes:
            self._by_class[cls].append(self._exact[sel])

        # Index by tag
        tags = re.findall(r'(?<![.\#])([a-zA-Z][\w-]*)', sel.split(":")[0])
        for tag in tags:
            if tag not in ("hover", "focus", "active", "visited", "nth", "first",
                           "last", "not", "where", "has", "is"):
                self._by_tag[tag].append(self._exact[sel])

        # Index by id
        ids = re.findall(r'#([\w-]+)', sel)
        for id_ in ids:
            self._by_id[id_].append(self._exact[sel])

        # Theme detection
        if ".dark" in sel or "[data-theme" in sel:
            self._theme_context[sel] = True
        elif ":root" in sel or ":where(:root)" in sel:
            # Assume light by default
            pass

    def find_matches(self, element_selector: str,
                     property_name: str = "color") -> List[Tuple[SelectorEntry, int]]:
        """Find the best matching CSS source rule for an element selector.

        Returns list of (SelectorEntry, score) sorted by score descending.
        """
        candidates: Dict[str, Tuple[SelectorEntry, int]] = {}
        elem_classes = re.findall(r'\.([\w-]+)', element_selector)
        elem_tags = re.findall(r'(?<![.\#])([a-zA-Z][\w-]+)', element_selector)
        elem_ids = re.findall(r'#([\w-]+)', element_selector)

        # Score by class match
        for cls in elem_classes:
            for entry in self._by_class.get(cls, []):
                score = self._score_match(entry.selector, element_selector, 50)
                if entry.selector not in candidates or score > candidates[entry.selector][1]:
                    candidates[entry.selector] = (entry, score)

        # Score by tag match
        for tag in elem_tags:
            for entry in self._by_tag.get(tag, []):
                score = self._score_match(entry.selector, element_selector, 20)
                if entry.selector not in candidates or score > candidates[entry.selector][1]:
                    candidates[entry.selector] = (entry, score)

        # Score by id match (highest weight)
        for id_ in elem_ids:
            for entry in self._by_id.get(id_, []):
                score = self._score_match(entry.selector, element_selector, 80)
                if entry.selector not in candidates or score > candidates[entry.selector][1]:
                    candidates[entry.selector] = (entry, score)

        # Filter to entries that define the requested property
        filtered = [(e, s) for e, s in candidates.values()
                    if property_name in e.properties]

        # Also include entries that don't define the property but inherit (lower score)
        if not filtered:
            filtered = [(e, s * 0.5) for e, s in candidates.values()]

        return sorted(filtered, key=lambda x: -x[1])

    def _score_match(self, css_sel: str, element_sel: str, base_score: int) -> int:
        """Score how well a CSS selector matches an element selector."""
        score = base_score

        # Exact match boost
        if css_sel == element_sel:
            score += 100
        elif css_sel.replace(" ", "") == element_sel:
            score += 80

        # All classes match
        css_classes = set(re.findall(r'\.([\w-]+)', css_sel))
        elem_classes = set(re.findall(r'\.([\w-]+)', element_sel))
        if css_classes and css_classes.issubset(elem_classes):
            score += 30 * len(css_classes)

        # Descendant match
        css_parts = css_sel.split()
        if len(css_parts) > 1:
            last_part = css_parts[-1].strip()
            if last_part == element_sel:
                score += 60
            elif set(re.findall(r'\.([\w-]+)', last_part)).issubset(elem_classes):
                score += 40

        return score

    def get_all(self) -> List[SelectorEntry]:
        return list(self._exact.values())


import re


def build_source_index(rules: List[CSSRule]) -> SourceIndex:
    """Build a SourceIndex from a list of CSS rules."""
    idx = SourceIndex()
    for rule in rules:
        idx.add_rule(rule)
    return idx


def extract_selectors_from_file(filepath: str) -> List[str]:
    """Quickly extract all selectors from a CSS file (for indexing)."""
    text = Path(filepath).read_text(encoding="utf-8")
    text = _COMMENT_RE.sub("", text)
    selectors = []
    for match in _RULE_BLOCK_RE.finditer(text):
        sel = match.group(1).strip()
        selectors.append(sel)
    return selectors