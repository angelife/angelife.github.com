"""Tests for CSS regression snapshot and diff."""

import json
import tempfile
from pathlib import Path

from site_audit.css_analyzer.parser import ColorToken
from site_audit.css_analyzer.snapshot import save_snapshot, load_snapshot, diff_snapshots


def _make_token(value, var, selectors, count=1):
    return ColorToken(value=value, variable=var, selectors=selectors, usage_count=count)


def test_save_and_load_snapshot():
    """Round-trip save/load should preserve data."""
    tokens = {
        "#888888": _make_token("#888888", "--secondary", [".post-meta", ".post-title"], 68),
    }
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
        save_snapshot(tokens, f.name)
        loaded = load_snapshot(f.name)
    assert loaded["variables"]["--secondary"] == "#888888"
    assert loaded["colors"]["#888888"]["count"] == 68


def test_snapshot_structure():
    """Snapshot should have timestamp, variables, colors."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
        save_snapshot({}, f.name)
        loaded = load_snapshot(f.name)
    assert "timestamp" in loaded
    assert "variables" in loaded
    assert "colors" in loaded


def test_diff_no_changes():
    """Identical snapshots should show no changes."""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
        save_snapshot({}, f.name)
        base = load_snapshot(f.name)
    diff = diff_snapshots(base, base)
    assert len(diff["changed"]) == 0
    assert len(diff["added"]) == 0
    assert len(diff["removed"]) == 0


def test_diff_changed_variable():
    """Changed variable should be detected."""
    base_tokens = {
        "#888888": _make_token("#888888", "--secondary", [".post-meta"], 68),
    }
    cur_tokens = {
        "#666666": _make_token("#666666", "--secondary", [".post-meta"], 68),
    }
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f1:
        save_snapshot(base_tokens, f1.name)
        base = load_snapshot(f1.name)
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f2:
        save_snapshot(cur_tokens, f2.name)
        cur = load_snapshot(f2.name)

    diff = diff_snapshots(cur, base)
    assert len(diff["changed"]) == 1
    assert diff["changed"][0]["variable"] == "--secondary"
    assert diff["changed"][0]["before"] == "#888888"
    assert diff["changed"][0]["after"] == "#666666"


def test_diff_added_token():
    """Newly added token should be detected."""
    cur_tokens = {"#666666": _make_token("#666666", "--new", [".x"], 1)}
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f1:
        save_snapshot({}, f1.name)
        base = load_snapshot(f1.name)
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f2:
        save_snapshot(cur_tokens, f2.name)
        cur = load_snapshot(f2.name)

    diff = diff_snapshots(cur, base)
    assert len(diff["added"]) >= 1


def test_diff_removed_token():
    """Removed token should be detected."""
    base_tokens = {"#888888": _make_token("#888888", "--old", [".x"], 1)}
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f1:
        save_snapshot(base_tokens, f1.name)
        base = load_snapshot(f1.name)
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f2:
        save_snapshot({}, f2.name)
        cur = load_snapshot(f2.name)

    diff = diff_snapshots(cur, base)
    assert len(diff["removed"]) >= 1