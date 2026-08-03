"""Color token analysis — aggregate CSS color usage by value."""

from typing import Dict, List
from .parser import ColorToken, CSSRule, normalize_color, hex_to_rgb


def build_color_tokens(rules: List[CSSRule]) -> Dict[str, ColorToken]:
    """Aggregate CSS rules into color tokens grouped by normalized hex value."""
    token_map: Dict[str, ColorToken] = {}

    for rule in rules:
        resolved = rule.resolved_value or rule.value
        hex_val = normalize_color(resolved)
        if not hex_val:
            continue

        if hex_val not in token_map:
            token_map[hex_val] = ColorToken(value=hex_val)

        token = token_map[hex_val]

        var = next((v for v in rule.variables if v), "")
        if var and not token.variable:
            token.variable = var

        if rule.selector not in token.selectors:
            token.selectors.append(rule.selector)

        if rule.source_file not in token.source_files:
            token.source_files.append(rule.source_file)

        token.usage_count += 1

    return token_map


def rank_tokens(tokens: Dict[str, ColorToken]) -> List[ColorToken]:
    """Return tokens sorted by usage_count descending."""
    return sorted(tokens.values(), key=lambda t: -t.usage_count)


def compute_contrast_for_token(token: ColorToken, bg_hex: str = "#ffffff") -> float:
    """Compute contrast ratio for this token against background."""
    rgb = hex_to_rgb(token.value)
    bg_rgb = hex_to_rgb(bg_hex)
    if not rgb or not bg_rgb:
        return 0.0

    def _lin(c):
        ci = c / 255.0
        return ci / 12.92 if ci <= 0.04045 else ((ci + 0.055) / 1.055) ** 2.4

    fg_lum = 0.2126 * _lin(rgb[0]) + 0.7152 * _lin(rgb[1]) + 0.0722 * _lin(rgb[2])
    bg_lum = 0.2126 * _lin(bg_rgb[0]) + 0.7152 * _lin(bg_rgb[1]) + 0.0722 * _lin(bg_rgb[2])

    lighter = max(fg_lum, bg_lum)
    darker = min(fg_lum, bg_lum)
    return (lighter + 0.05) / (darker + 0.05)