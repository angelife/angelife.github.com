"""CSS Selector Matcher - parse element selectors and match against CSS rules."""

import re
from typing import Dict, List, Optional, Tuple

from .parser import CSSRule, parse_all_css
from .source_index import SourceIndex, build_source_index, SelectorEntry


def specificity(selector: str) -> int:
    """Calculate CSS specificity: id=100, class=10, tag=1.

    Correctly strips IDs and classes before counting tags,
    and ignores pseudo-classes/elements.
    """
    # Remove ID and class parts first so they don't leak into tag count
    clean = selector.split("{")[0].split(":")[0]
    clean = re.sub(r'#[\w-]+', '', clean)
    clean = re.sub(r'\.[\w-]+', '', clean)
    clean = re.sub(r'\*+', '', clean)  # universal selector
    ids = len(re.findall(r'#[\w-]+', selector))
    classes = len(re.findall(r'\.[\w-]+', selector))
    # Tags are word-like tokens remaining after stripping
    tags = len(re.findall(r'[a-zA-Z][\w-]*', clean))
    return ids * 100 + classes * 10 + tags


def parse_element_selector(selector: str) -> Dict:
    """Parse a DOM element selector into its parts."""
    tag_match = re.match(r'^([a-zA-Z][\w]*)', selector)
    tag = tag_match.group(1) if tag_match else ""
    classes = re.findall(r'\.([\w-]+)', selector)
    ids = re.findall(r'#([\w-]+)', selector)
    return {"tag": tag, "classes": classes, "id": ids[0] if ids else ""}


def selector_contains(css_sel: str, element_sel: str) -> bool:
    """Check if a CSS selector matches an element selector."""
    for part in re.split(r'\s*,\s*', css_sel):
        if _selector_part_matches(part.strip(), element_sel):
            return True
    return False


def _selector_part_matches(css_part: str, element_sel: str) -> bool:
    """Match a single (non-group) CSS selector part against an element."""
    parts = [p.strip() for p in re.split(r'\s+', css_part) if p.strip() and p.strip() != '>']
    if not parts:
        return False

    last_part = parts[-1]
    elem = parse_element_selector(element_sel)

    if not _simple_selector_matches(last_part, elem):
        return False

    if len(parts) == 1:
        return True

    # For descendants, check ancestor class overlap with element classes
    for ancestor in parts[:-1]:
        anc_classes = set(re.findall(r'\.([\w-]+)', ancestor))
        anc_ids = set(re.findall(r'#([\w-]+)', ancestor))
        elem_classes = set(elem['classes'])

        if anc_ids and not anc_ids & (set([elem['id']]) if elem['id'] else set()):
            return False

        if anc_classes:
            if anc_classes & elem_classes:
                continue
            substr_overlap = any(ac in ec or ec in ac for ac in anc_classes for ec in elem_classes)
            if substr_overlap:
                continue
            # No ancestor class overlap — accept heuristically (no DOM ancestry available)
            # Phase 8A will provide real ancestors; Phase 8B will use them for proper matching
            pass

    return True


def _simple_selector_matches(simple: str, elem: Dict) -> bool:
    """Match a simple selector (no combinators) against an element dict."""
    tag = re.match(r'^([a-zA-Z][\w]*)', simple)
    has_tag = tag is not None
    tag_name = tag.group(1) if has_tag else ""

    classes = set(re.findall(r'\.([\w-]+)', simple))
    elem_classes = set(elem['classes'])
    ids = re.findall(r'#([\w-]+)', simple)
    elem_id = elem.get('id', '')

    if simple == '*':
        return True

    if tag_name == '*':
        remaining = simple.replace('*', '').strip()
        if not remaining:
            return True
        rem_classes = set(re.findall(r'\.([\w-]+)', remaining))
        rem_ids = re.findall(r'#([\w-]+)', remaining)
        if rem_classes and not rem_classes.issubset(elem_classes):
            return False
        if rem_ids and rem_ids[0] != elem_id:
            return False
        return True

    if not classes and not ids and tag_name and tag_name != '*':
        if elem['tag'] and tag_name != elem['tag']:
            return False
        return True

    if has_tag and tag_name and tag_name != '*' and elem['tag']:
        if tag_name != elem['tag']:
            return False

    if classes and not classes.issubset(elem_classes):
        return False

    if ids and ids[0] != elem_id:
        return False

    return True


def match_selector(css_sel: str, element_sel: str) -> Tuple[bool, int]:
    """Match a CSS selector against an element selector."""
    if selector_contains(css_sel, element_sel):
        sp = specificity(css_sel)
        if css_sel == element_sel:
            sp += 500
        elif _loose_match(css_sel, element_sel):
            sp += 200
        return True, sp
    return False, 0


def _loose_match(css_sel: str, element_sel: str) -> bool:
    """Check if they share enough characteristics for a loose match."""
    css_classes = set(re.findall(r'\.([\w-]+)', css_sel))
    elem_classes = set(re.findall(r'\.([\w-]+)', element_sel))
    shared = css_classes & elem_classes
    return len(shared) > 0


def find_best_match(element_selector: str, source_index: SourceIndex,
                    property_name: str = "color") -> List[Tuple[SelectorEntry, int, int]]:
    """Find the best matching CSS rule(s) for an element selector."""
    elem = parse_element_selector(element_selector)
    candidates = {}

    for entry in source_index.get_all():
        matched, spec = match_selector(entry.selector, element_selector)
        if matched:
            confidence = 0
            if property_name in entry.properties:
                confidence = 50
            old_score = candidates.get(entry.selector, (None, -1, 0))[1]
            if spec > old_score:
                candidates[entry.selector] = (entry, spec, confidence)

    results = sorted(candidates.values(), key=lambda x: -x[1])
    return results
