"""Before/after simulation for color token fixes.

Re-calculates contrast without modifying any issues or files."""

from typing import Dict, List, Optional
from .parser import ColorToken, hex_to_rgb
from .colors import compute_contrast_for_token, build_color_tokens


class SimulationResult:
    """Result of simulating a color token change."""

    def __init__(self, variable: str, before_color: str, after_color: str,
                 before_ratio: float, after_ratio: float,
                 before_failures: int, after_failures: int,
                 bg_color: str = "#ffffff"):
        self.variable = variable
        self.before_color = before_color
        self.after_color = after_color
        self.before_ratio = round(before_ratio, 2)
        self.after_ratio = round(after_ratio, 2)
        self.before_failures = before_failures
        self.after_failures = after_failures
        self.bg_color = bg_color

    def to_dict(self) -> dict:
        return {
            "variable": self.variable,
            "before_color": self.before_color,
            "after_color": self.after_color,
            "before_ratio": self.before_ratio,
            "after_ratio": self.after_ratio,
            "before_failures": self.before_failures,
            "after_failures": self.after_failures,
            "bg_color": self.bg_color,
        }


def simulate_fix(token: ColorToken, new_hex: str,
                  original_issue_count: int,
                  bg_hex: str = "#ffffff") -> SimulationResult:
    """Simulate changing a token's color.

    Returns before/after contrast comparison.
    """
    old_ratio = compute_contrast_for_token(token, bg_hex)
    new_token = ColorToken(value=new_hex, variable=token.variable)
    new_ratio = compute_contrast_for_token(new_token, bg_hex)

    # Calculate failures: count of issues that would be fixed
    after_failures = 0
    threshold = 4.5
    if old_ratio < threshold and new_ratio >= threshold:
        after_failures = 0
    elif old_ratio < threshold:
        # Still failing but maybe improved
        if new_ratio < threshold:
            after_failures = original_issue_count  # still failing
        else:
            after_failures = 0  # passed
    else:
        after_failures = 0  # already passed

    return SimulationResult(
        variable=token.variable,
        before_color=token.value,
        after_color=new_hex,
        before_ratio=old_ratio,
        after_ratio=new_ratio,
        before_failures=original_issue_count,
        after_failures=0 if new_ratio >= threshold else original_issue_count,
        bg_color=bg_hex,
    )


def simulate_bulk(tokens: list, suggestions: list) -> list[SimulationResult]:
    """Run simulation on all suggested fixes.

    Args:
        tokens: List of ColorToken
        suggestions: List of css_token_issue dicts from report

    Returns:
        List of SimulationResult
    """
    results = []
    token_by_val = {t.value: t for t in tokens}

    for sug in suggestions:
        color = sug["color"]
        count = sug["issue_count"]
        token = token_by_val.get(color)
        if not token:
            continue

        # Extract recommended color from suggestion
        rec = _extract_rec_color(sug)
        if not rec:
            continue

        sim = simulate_fix(token, rec, count)
        results.append(sim)

    return results


def _extract_rec_color(suggestion: dict) -> Optional[str]:
    """Extract recommended hex from a css_token_issue dict."""
    text = suggestion.get("suggestion", "")
    if "→" not in text:
        return None
    parts = text.split("→")
    if len(parts) < 2:
        return None
    candidate = parts[1].strip().split()[0]
    if candidate.startswith("#") and len(candidate) == 7:
        return candidate
    return None