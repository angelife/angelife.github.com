"""CSS Regression Snapshot — save/load/diff color tokens across sessions."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from .parser import ColorToken


def save_snapshot(tokens: Dict[str, ColorToken], output_path: str) -> str:
    """Save current token state as a snapshot JSON file.

    Structure:
    {
        "timestamp": "2026-07-09T...",
        "variables": { "--secondary": "#888888", ... },
        "colors": {
            "#888888": {
                "selectors": [".post-meta", ".post-title"],
                "count": 68
            },
            ...
        }
    }
    """
    variables = {}
    colors = {}

    for hex_val, token in tokens.items():
        # Variable mapping
        if token.variable:
            variables[token.variable] = hex_val

        # Color → selectors
        colors[hex_val] = {
            "selectors": sorted(token.selectors),
            "count": token.usage_count,
        }

    data = {
        "timestamp": datetime.now().isoformat(),
        "variables": variables,
        "colors": colors,
    }

    Path(output_path).write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return output_path


def load_snapshot(path: str) -> dict:
    """Load a snapshot JSON file."""
    return json.loads(Path(path).read_text(encoding="utf-8"))


def diff_snapshots(current: dict, baseline: dict) -> dict:
    """Compare two snapshots and detect changes.

    Returns:
    {
        "added": [...],
        "removed": [...],
        "changed": [...]
    }
    """
    cur_vars = current.get("variables", {})
    base_vars = baseline.get("variables", {})

    cur_colors = current.get("colors", {})
    base_colors = baseline.get("colors", {})

    added = []
    removed = []
    changed = []

    # Detect added variables
    for var, val in cur_vars.items():
        if var not in base_vars:
            added.append({"variable": var, "value": val})
        elif base_vars[var] != val:
            changed.append({
                "variable": var,
                "before": base_vars[var],
                "after": val,
            })

    # Detect removed variables
    for var, val in base_vars.items():
        if var not in cur_vars:
            removed.append({"variable": var, "value": val})

    # Detect color changes (new/removed tokens)
    for hex_val, info in cur_colors.items():
        if hex_val not in base_colors:
            added.append({"color": hex_val, "count": info["count"]})

    for hex_val, info in base_colors.items():
        if hex_val not in cur_colors:
            removed.append({"color": hex_val, "count": info["count"]})

    return {
        "changed": changed,
        "added": added,
        "removed": removed,
        "timestamp": {
            "current": current.get("timestamp", ""),
            "baseline": baseline.get("timestamp", ""),
        },
    }


def generate_regression_report(diff_result: dict) -> list:
    """Convert diff result into a structured regression report."""
    items = []

    for item in diff_result.get("changed", []):
        items.append({
            "type": "changed",
            "variable": item.get("variable", ""),
            "before": item.get("before", ""),
            "after": item.get("after", ""),
        })

    for item in diff_result.get("added", []):
        if "variable" in item:
            items.append({
                "type": "added",
                "variable": item.get("variable", ""),
                "value": item.get("value", ""),
            })
        else:
            items.append({
                "type": "added",
                "color": item.get("color", ""),
                "count": item.get("count", 0),
            })

    for item in diff_result.get("removed", []):
        if "variable" in item:
            items.append({
                "type": "removed",
                "variable": item.get("variable", ""),
            })
        else:
            items.append({
                "type": "removed",
                "color": item.get("color", ""),
            })

    return items