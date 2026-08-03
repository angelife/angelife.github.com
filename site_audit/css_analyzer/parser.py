"""CSS parser — extract rules, selectors, colors, variables from raw CSS."""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class CSSRule:
    selector: str
    property: str
    value: str
    source_file: str = ""
    line: int = 0
    resolved_value: str = ""
    variables: List[str] = field(default_factory=list)
    important: bool = False
    specificity_a: int = 0
    specificity_b: int = 0
    specificity_c: int = 0
    source_order: int = 0
    media_context: str = ""
    layer: str = ""

    @property
    def specificity_tuple(self):
        return (self.specificity_a, self.specificity_b, self.specificity_c)

    def cascade_key(self, theme: str = "", viewport: tuple = (0, 0)) -> tuple:
        """Key for cascade ordering: important(desc) > specificity(desc) > source_order(asc)."""
        return (-self.important, -self.specificity_a, -self.specificity_b, -self.specificity_c, self.source_order)


@dataclass
class ColorToken:
    value: str           # normalized hex #888888
    variable: str = ""   # originating variable name
    selectors: List[str] = field(default_factory=list)
    source_files: List[str] = field(default_factory=list)
    usage_count: int = 0


_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
_RULE_BLOCK_RE = re.compile(r"([^{]+)\{([^}]+)\}")
_DECL_RE = re.compile(r"([\w-]+)\s*:\s*(.*?)\s*;")
_VAR_REF_RE = re.compile(r"var\((--[\w-]+)\s*(?:,\s*([^)]+))?\)")

# Color formats
_HEX_RE = re.compile(r"#([0-9a-fA-F]{3,8})\b")
_RGB_RE = re.compile(r"rgba?\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?:\s*,\s*[\d.]+)?\s*\)")
_HSL_RE = re.compile(r"hsla?\s*\(\s*([\d.]+)\s*,\s*([\d.]+%)\s*,\s*([\d.]+%)")

_COLOR_PROPERTIES = {"color", "background", "background-color", "border-color",
                     "background-image", "outline-color", "text-decoration-color"}


def find_css_files(public_dir: str) -> List[str]:
    """Find all CSS files under public/ recursively."""
    p = Path(public_dir)
    if not p.is_dir():
        return []
    return sorted(str(f) for f in p.rglob("*.css") if f.is_file())


def parse_css_file(filepath: str, source_order_start: int = 0) -> List[CSSRule]:
    """Parse a single CSS file and return all color-related rules."""
    text = Path(filepath).read_text(encoding="utf-8")
    text = _COMMENT_RE.sub("", text)
    rules: List[CSSRule] = []
    global_counter = source_order_start

    for match in _RULE_BLOCK_RE.finditer(text):
        raw_selector = match.group(1).strip()
        body = match.group(2)
        line_no = text[: match.start()].count("\n") + 1

        for decl in _DECL_RE.finditer(body):
            prop = decl.group(1).strip()
            value = decl.group(2).strip()
            if prop not in _COLOR_PROPERTIES and not prop.startswith("--"):
                continue

            # Detect !important
            important = "!important" in value
            clean_value = value.replace("!important", "").strip()

            variables = [m.group(1) for m in _VAR_REF_RE.finditer(clean_value)]

            # Compute specificity
            from .specificity import specificity
            a, b, c = specificity(raw_selector)

            rules.append(CSSRule(
                selector=raw_selector,
                property=prop,
                value=clean_value,
                source_file=filepath,
                line=line_no,
                resolved_value=clean_value,
                variables=variables,
                important=important,
                specificity_a=a,
                specificity_b=b,
                specificity_c=c,
                source_order=global_counter,
            ))
            global_counter += 1

    return rules


def parse_all_css(public_dir: str) -> List[CSSRule]:
    """Parse all CSS files in the public directory."""
    files = find_css_files(public_dir)
    all_rules: List[CSSRule] = []
    for fp in files:
        all_rules.extend(parse_css_file(fp))
    return all_rules


def normalize_color(value: str) -> Optional[str]:
    """Normalize any CSS color to #rrggbb hex, or None if unrecognised."""
    value = value.strip()

    # Hex
    m = _HEX_RE.search(value)
    if m:
        h = m.group(1)
        if len(h) == 3:
            return "#" + "".join(c * 2 for c in h)
        elif len(h) in (6, 8):
            return "#" + h[:6].lower()
        return None

    # rgb/rgba
    m = _RGB_RE.search(value)
    if m:
        r, g, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return f"#{r:02x}{g:02x}{b:02x}"

    # hsl
    m = _HSL_RE.search(value)
    if m:
        h = float(m.group(1))
        s = float(m.group(2).rstrip("%")) / 100
        l = float(m.group(3).rstrip("%")) / 100
        r, g, b = _hsl_to_rgb(h, s, l)
        return f"#{r:02x}{g:02x}{b:02x}"

    # Named colors
    named = {
        "white": "#ffffff", "black": "#000000", "red": "#ff0000",
        "green": "#008000", "blue": "#0000ff", "gray": "#808080",
        "grey": "#808080", "silver": "#c0c0c0", "transparent": None,
    }
    if value.lower() in named:
        return named[value.lower()]

    return None


def _hsl_to_rgb(h: float, s: float, l: float):
    """HSL to RGB conversion."""
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2

    if h < 60: r1, g1, b1 = c, x, 0
    elif h < 120: r1, g1, b1 = x, c, 0
    elif h < 180: r1, g1, b1 = 0, c, x
    elif h < 240: r1, g1, b1 = 0, x, c
    elif h < 300: r1, g1, b1 = x, 0, c
    else: r1, g1, b1 = c, 0, x

    return int((r1 + m) * 255), int((g1 + m) * 255), int((b1 + m) * 255)


def hex_to_rgb(hex_color: str) -> Optional[tuple]:
    """Convert #rrggbb to (r, g, b) ints."""
    h = hex_color.lstrip("#")
    if len(h) != 6:
        return None
    try:
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    except ValueError:
        return None