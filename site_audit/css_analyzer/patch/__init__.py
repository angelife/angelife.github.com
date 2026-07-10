"""CSS Patch Generator — read-only diff generation for color token fixes."""

from pathlib import Path
from typing import Optional, Dict, Any
from ..parser import normalize_color
from ..colors import ColorToken


class Patch:
    """Represents a single CSS patch (for preview only — never writes)."""

    def __init__(self, variable: str, source_file: str, line: int,
                 old_value: str, new_value: str,
                 selectors: list, issue_count: int,
                 risk: str = "low", patch_type: str = "variable"):
        self.variable = variable
        self.source_file = source_file
        self.line = line
        self.old_value = old_value.strip()
        self.new_value = new_value.strip()
        self.selectors = list(selectors)
        self.issue_count = issue_count
        self.risk = risk
        self.patch_type = patch_type  # "variable" or "direct"

    def to_dict(self) -> dict:
        return {
            "variable": self.variable,
            "source_file": self.source_file,
            "line": self.line,
            "old_value": self.old_value,
            "new_value": self.new_value,
            "selectors": self.selectors,
            "issue_count": self.issue_count,
            "risk": self.risk,
            "patch_type": self.patch_type,
        }


def generate_patch(token: ColorToken, new_value: str) -> Optional[Patch]:
    """Generate a patch for a color token's variable definition.

    Reads the actual CSS file to find the variable definition line.
    Returns None if the variable isn't found in any known source file.
    """
    if not token.variable or not token.source_files:
        return None

    for src in token.source_files:
        sf = Path(src)
        if not sf.is_file():
            continue

        content = sf.read_text(encoding="utf-8")
        lines = content.split("\n")

        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith(token.variable) and ":" in stripped:
                old_val = stripped.split(":", 1)[1].strip().rstrip(";").strip()
                return Patch(
                    variable=token.variable,
                    source_file=src,
                    line=i + 1,
                    old_value=old_val,
                    new_value=new_value,
                    selectors=token.selectors,
                    issue_count=token.usage_count,
                )

    return None


def generate_patches(tokens: list, suggestions: list) -> list[Patch]:
    """Generate patches from token issues and their suggestions.

    Args:
        tokens: List of ColorToken objects
        suggestions: List of css_token_issue dicts (from report)

    Returns:
        List of Patch objects
    """
    patches = []
    # Build a lookup: hex → ColorToken
    token_by_val = {t.value: t for t in tokens}

    for sug in suggestions:
        color = sug["color"]
        recommendation = sug.get("balanced", sug.get("suggestion", ""))
        # Extract hex from recommendation like "Change #888888 → #6b6b6b ..."
        new_val = _extract_new_value(recommendation)
        if not new_val:
            continue

        token = token_by_val.get(color)
        if not token:
            continue

        patch = generate_patch(token, new_val)
        if patch:
            patches.append(patch)

    return patches


def _extract_new_value(text: str) -> Optional[str]:
    """Extract target hex from a suggestion string.

    e.g. "Change #888888 → #6b6b6b ..." → "#6b6b6b"
    """
    if "→" not in text:
        return None
    parts = text.split("→")
    if len(parts) < 2:
        return None
    candidate = parts[1].strip().split()[0].strip()
    if candidate.startswith("#") and len(candidate) == 7:
        return candidate
    return None