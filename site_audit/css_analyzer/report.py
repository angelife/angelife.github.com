"""CSS token report — generate color system issues and fix suggestions."""

import math
from typing import Dict, List, Optional

from .parser import ColorToken, hex_to_rgb, normalize_color
from .colors import build_color_tokens, rank_tokens, compute_contrast_for_token
from ..models.issue import Issue, Severity


def _relative_luminance(r: int, g: int, b: int) -> float:
    def _lin(c: float) -> float:
        ci = c / 255.0
        return ci / 12.92 if ci <= 0.04045 else ((ci + 0.055) / 1.055) ** 2.4
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def _contrast_ratio(fg: tuple, bg: tuple) -> float:
    fg_lum = _relative_luminance(*fg)
    bg_lum = _relative_luminance(*bg)
    return (max(fg_lum, bg_lum) + 0.05) / (min(fg_lum, bg_lum) + 0.05)


def suggest_color(current_hex: str, bg_hex: str = "#ffffff",
                  target_ratio: float = 4.5, large_text: bool = False) -> Optional[str]:
    if large_text:
        target_ratio = max(target_ratio, 3.0)

    fg_rgb = hex_to_rgb(current_hex)
    bg_rgb = hex_to_rgb(bg_hex)
    if not fg_rgb or not bg_rgb:
        return None

    current_ratio = _contrast_ratio(fg_rgb, bg_rgb)
    if current_ratio >= target_ratio:
        return current_hex

    fg_lum = _relative_luminance(*fg_rgb)
    bg_lum = _relative_luminance(*bg_rgb)

    # Use a safety margin (10%) to ensure we actually meet the threshold
    adjusted_target = target_ratio * 1.1

    if fg_lum < bg_lum:
        target_lum = max(0.0, (bg_lum + 0.05) / adjusted_target - 0.05)
    else:
        target_lum = min(1.0, (bg_lum + 0.05) * adjusted_target - 0.05)

    return _luminance_to_hex(fg_rgb, target_lum)


def _luminance_to_hex(rgb: tuple, target_lum: float) -> Optional[str]:
    """Find the closest color with target luminance via channel scaling."""
    r, g, b = rgb
    current_lum = _relative_luminance(r, g, b)

    if current_lum <= 0.0001 or abs(current_lum - target_lum) < 0.001:
        return f"#{r:02x}{g:02x}{b:02x}"

    scale = math.sqrt(max(target_lum / current_lum, 0.001))

    def _clip(v: int) -> int:
        return max(0, min(255, round(v)))

    new_r = _clip(r * scale)
    new_g = _clip(g * scale)
    new_b = _clip(b * scale)

    # Verify the result meets the target
    result_lum = _relative_luminance(new_r, new_g, new_b)
    if abs(result_lum - target_lum) > 0.02 and scale < 1.0:
        # Further darken if needed
        scale2 = math.sqrt(max(target_lum / max(result_lum, 0.001), 0.001))
        new_r = _clip(r * scale * scale2)
        new_g = _clip(g * scale * scale2)
        new_b = _clip(b * scale * scale2)

    return f"#{new_r:02x}{new_g:02x}{new_b:02x}"


def generate_css_token_issues(tokens: Dict[str, ColorToken],
                               visual_issues: List[Issue]) -> List[dict]:
    """Generate css_token_issues list for JSON report.

    Each entry:
    {
        "color": "#888888",
        "variable": "--secondary",
        "contrast_min": 2.1,
        "affected_selectors": [".post-title", ".post-meta"],
        "issue_count": 85,
        "suggestion": "change #888888 → #595959 (WCAG AA 4.5:1)"
    }
    """
    color_issue_count: Dict[str, int] = {}
    for issue in visual_issues:
        if issue.rule != "visual/contrast":
            continue
        data = issue.data or {}
        fg_hex = normalize_color(data.get("fg", ""))
        if fg_hex:
            color_issue_count[fg_hex] = color_issue_count.get(fg_hex, 0) + 1

    result = []
    for hex_val, token in tokens.items():
        cnt = color_issue_count.get(hex_val, 0)
        if cnt == 0:
            continue

        contrast_min = compute_contrast_for_token(token)
        if contrast_min >= 4.5:
            continue  # passes WCAG AA, not a token issue

        suggestion = _build_suggestion(hex_val, contrast_min, cnt)

        entry = {
            "color": hex_val,
            "variable": token.variable,
            "contrast_min": round(contrast_min, 2),
            "affected_selectors": token.selectors[:20],
            "issue_count": cnt,
            "suggestion": suggestion,
        }
        result.append(entry)

    return sorted(result, key=lambda x: -x["issue_count"])


def _build_suggestion(hex_val: str, current_ratio: float, count: int) -> str:
    """Build a human-readable fix suggestion."""
    if current_ratio >= 4.5:
        return ""

    suggested = suggest_color(hex_val, target_ratio=4.5)
    if suggested and suggested != hex_val:
        new_ratio = _ratio_against_white(suggested)
        return (f"Change {hex_val} → {suggested} "
                f"(WCAG AA from {current_ratio:.1f}:1 to {new_ratio:.1f}:1)")
    return ""


def _ratio_against_white(hex_color: str) -> float:
    """Quick contrast ratio against white background."""
    rgb = hex_to_rgb(hex_color)
    if not rgb:
        return 0.0
    return _contrast_ratio(rgb, (255, 255, 255))