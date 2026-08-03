"""Full CSS specificity calculator — (a,b,c) tuple.

Supports: ID, class, attribute, pseudo-class, element/tag, pseudo-element.
CSS Selector Level 4 spec: https://www.w3.org/TR/selectors-4/#specificity-rules

Algorithm:
  1. Split on combinators (>, +, ~, space) into compound selectors
  2. For each compound selector:
     - Count IDs (#id) → column a
     - Count classes (.class), attributes ([attr]), pseudo-classes (:hover) → column b
     - Count elements (div, span) and pseudo-elements (::before) → column c
  3. Sum across all compound selectors
"""

import re
from typing import Tuple


def specificity(selector: str) -> Tuple[int, int, int]:
    """Calculate full CSS specificity as (a, b, c).

    a = number of ID selectors
    b = number of class selectors, attribute selectors, pseudo-classes
    c = number of type selectors and pseudo-elements
    """
    a = 0
    b = 0
    c = 0

    # Step 1: Split on combinators to get compound selectors
    # Combinators: >, +, ~, and descendant (space)
    # We need to handle quoted strings inside selectors
    compound_selectors = _split_on_combinators(selector)

    for compound in compound_selectors:
        compound = compound.strip()
        if not compound or compound == '*':
            continue

        # Step 2: Remove pseudo-elements (::before, ::after) — count as c
        pseudo_elems = re.findall(r'::[a-zA-Z][\w-]*', compound)
        c += len(pseudo_elems)
        compound = re.sub(r'::[a-zA-Z][\w-]*', '', compound)

        # Step 3: Handle :not(), :is(), :has() — their arguments contribute specificity
        special_pseudo = re.findall(r':(not|is|has)\(([^)]+)\)', compound)
        for _, args in special_pseudo:
            inner_a, inner_b, inner_c = specificity(args)
            a += inner_a
            b += inner_b
            c += inner_c
        compound = re.sub(r':(not|is|has)\([^)]*\)', '', compound)

        # Step 4: Handle :where() — adds 0 specificity, strip entirely
        compound = re.sub(r':where\([^)]*\)', '', compound)

        # Step 5: Count attribute selectors [attr]
        attr_matches = re.findall(r'\[[^\]]+\]', compound)
        b += len(attr_matches)
        compound = re.sub(r'\[[^\]]+\]', '', compound)

        # Step 6: Count pseudo-classes (:hover, :focus, etc.)
        pseudo_classes = re.findall(r':[a-zA-Z][\w-]*(?:\([^)]*\))?', compound)
        for pc in pseudo_classes:
            name = pc.split('(')[0]
            if name == ':where':
                continue
            if name in (':not', ':is', ':has'):
                continue  # Already handled above
            b += 1
        compound = re.sub(r':[a-zA-Z][\w-]*(?:\([^)]*\))?', '', compound)

        # Step 7: Count ID selectors (#id)
        id_matches = re.findall(r'#([a-zA-Z_][\w-]*)', compound)
        a += len(id_matches)
        compound = re.sub(r'#[a-zA-Z_][\w-]*', '', compound)

        # Step 8: Count class selectors (.class) — include adjacent pseudo-classes
        class_matches = re.findall(r'\.[a-zA-Z_][\w-]*', compound)
        b += len(class_matches)
        compound = re.sub(r'\.[a-zA-Z_][\w-]*(?::[a-zA-Z][\w-]*)?', '', compound)

        # Step 9: Count element/type selectors
        # Remaining should be tag names separated by spaces
        tags = re.findall(r'[a-zA-Z][\w-]*', compound)
        for tag in tags:
            if tag.lower() not in ('and', 'or', 'not', 'only', 'of', 'where',
                                   'has', 'is', 'from', 'to', 'dark', 'light',
                                   'screen', 'print', 'all', 'and', 'min', 'max',
                                   'width', 'height', 'resolution', 'prefers'):
                c += 1

    return (a, b, c)


def _split_on_combinators(selector: str) -> list:
    """Split a selector string on CSS combinators (> + ~ and space).

    Returns list of compound selectors.
    Handles quoted strings and complex selectors.
    """
    parts = []
    current = ""
    i = 0
    in_bracket = False
    in_paren = False

    while i < len(selector):
        ch = selector[i]

        if ch == '[':
            in_bracket = True
            current += ch
            i += 1
            continue
        if ch == ']':
            in_bracket = False
            current += ch
            i += 1
            continue
        if ch == '(':
            in_paren = True
            current += ch
            i += 1
            continue
        if ch == ')':
            in_paren = False
            current += ch
            i += 1
            continue

        if not in_bracket and not in_paren:
            if ch in ('>', '+', '~') and (i == 0 or selector[i-1] != ' '):
                if current.strip():
                    parts.append(current.strip())
                current = ""
                i += 1
                continue
            if ch == ' ' and i > 0 and i < len(selector) - 1:
                # Check if this space is a descendant combinator
                # (not inside quotes or other context)
                prev_non_space = ''
                j = i - 1
                while j >= 0 and selector[j] == ' ':
                    j -= 1
                if j >= 0:
                    prev_non_space = selector[j]
                next_char = selector[i + 1] if i + 1 < len(selector) else ''

                # Skip if it looks like part of a class name or attribute
                if prev_non_space not in ('>', '+', '~', ' ', '') and \
                   next_char not in ('>', '+', '~', ' '):
                    current += ch
                    i += 1
                    continue
                elif prev_non_space in ('>', '+', '~'):
                    # Space after combinator is just whitespace
                    current += ch
                    i += 1
                    continue

                if current.strip():
                    parts.append(current.strip())
                current = ""
                i += 1
                continue

        current += ch
        i += 1

    if current.strip():
        parts.append(current.strip())

    return parts