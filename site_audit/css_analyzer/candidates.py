"""Three-tier color candidates: light, balanced, strong."""

from typing import Dict, List, Optional
from .report import suggest_color
from .parser import normalize_color, hex_to_rgb
from .colors import compute_contrast_for_token, ColorToken


def generate_candidates(token: ColorToken, bg_hex: str = "#ffffff",
                         color_value: Optional[str] = None) -> List[Dict]:
    """Generate three recommendation tiers for a color token.

    Returns list of candidate dicts sorted by strength:
    [
        {
            "level": "light",
            "color": "#777777",
            "ratio": 4.5,
            "delta": 17,
            "description": "minimal change, barely meets AA"
        },
        ...
    ]
    """
    current_hex = token.value
    fg_rgb = hex_to_rgb(current_hex)
    bg_rgb = hex_to_rgb(bg_hex)
    if not fg_rgb or not bg_rgb:
        return []

    candidates = []

    # Light: just above AA threshold (4.5:1 with small margin)
    light = suggest_color(current_hex, bg_hex, target_ratio=4.6)
    if light and light != current_hex:
        candidates.append(_make_candidate("light", "minimal change, barely meets WCAG AA", light, current_hex, bg_hex))

    # Balanced: comfortable AA (5.5:1)
    balanced = suggest_color(current_hex, bg_hex, target_ratio=5.5)
    if balanced and balanced != current_hex and balanced not in [c["color"] for c in candidates]:
        candidates.append(_make_candidate("balanced", "safe default with comfortable margin", balanced, current_hex, bg_hex))

    # Strong: high readability (~7.0:1)
    strong = suggest_color(current_hex, bg_hex, target_ratio=7.0)
    if strong and strong != current_hex and strong not in [c["color"] for c in candidates]:
        candidates.append(_make_candidate("strong", "high readability, AAA-compatible", strong, current_hex, bg_hex))

    return candidates


def _make_candidate(level: str, description: str, hex_color: str,
                    original_hex: str, bg_hex: str) -> dict:
    """Build candidate dict with computed metrics."""
    ratio = compute_contrast_for_token(ColorToken(value=hex_color), bg_hex)

    # Color delta (Euclidean in RGB)
    orig_rgb = hex_to_rgb(original_hex)
    cand_rgb = hex_to_rgb(hex_color)
    delta = 0
    if orig_rgb and cand_rgb:
        delta = int(round(
            ((orig_rgb[0] - cand_rgb[0]) ** 2 +
             (orig_rgb[1] - cand_rgb[1]) ** 2 +
             (orig_rgb[2] - cand_rgb[2]) ** 2) ** 0.5
        ))

    return {
        "level": level,
        "color": hex_color,
        "ratio": round(ratio, 2),
        "delta": delta,
        "description": description,
    }