"""Tests for baseline diff functionality."""

from pathlib import Path
import json
import tempfile

from site_audit.models.issue import Issue, Severity
from site_audit.reporter.baseline import load_baseline, filter_new_issues, save_baseline


def test_fingerprint_uniqueness():
    """Different issues should have different fingerprints."""
    i1 = Issue(rule="test/a", severity=Severity.MINOR, message="msg", file="f.md", line=1)
    i2 = Issue(rule="test/b", severity=Severity.MINOR, message="msg", file="f.md", line=1)
    assert i1.fingerprint() != i2.fingerprint()


def test_filter_new_issues():
    """Baseline should suppress known issues."""
    old = [
        Issue(rule="test/a", severity=Severity.MINOR, message="old", file="f.md", line=1),
    ]
    new = [
        Issue(rule="test/a", severity=Severity.MINOR, message="old", file="f.md", line=1),
        Issue(rule="test/b", severity=Severity.MINOR, message="new", file="f.md", line=5),
    ]

    baseline = [i.fingerprint() for i in old]
    filtered, matched = filter_new_issues(new, baseline)
    assert matched == 1
    assert len(filtered) == 1
    assert filtered[0].message == "new"


def test_save_and_load_baseline():
    """Round-trip save/load baseline."""
    issues = [
        Issue(rule="test/a", severity=Severity.MINOR, message="x", file="f.md", line=1),
    ]
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        save_baseline(issues, f.name)
        loaded = load_baseline(f.name)
    assert len(loaded) == 1
    assert "test/a:f.md:1" in loaded


def test_visual_baseline_fingerprint():
    """Visual issues should fingerprint by selector+fg+bg+ratio."""
    v = Issue(
        rule="visual/contrast", severity=Severity.MAJOR,
        message="Low contrast", file="/page/",
        data={"selector": ".post-meta", "fg": "rgba(136,136,136,1)", "bg": "rgba(255,255,255,1)", "ratio": 2.8}
    )
    fp = v.fingerprint()
    assert fp.startswith("contrast:")
    assert ".post-meta" in fp


def test_baseline_suppresses_visual():
    """Visual baseline should work same way."""
    old_v = Issue(
        rule="visual/contrast", severity=Severity.MAJOR,
        message="Low contrast", file="/p/",
        data={"selector": ".meta", "fg": "#888", "bg": "#fff", "ratio": 3.0}
    )
    new_v = [
        Issue(
            rule="visual/contrast", severity=Severity.MAJOR,
            message="Low contrast", file="/p/",
            data={"selector": ".meta", "fg": "#888", "bg": "#fff", "ratio": 3.0}
        ),
        Issue(
            rule="visual/contrast", severity=Severity.MAJOR,
            message="New contrast", file="/p/",
            data={"selector": ".footer", "fg": "#999", "bg": "#fff", "ratio": 4.0}
        ),
    ]
    bl = [old_v.fingerprint()]
    filtered, matched = filter_new_issues(new_v, bl)
    assert matched == 1
    assert len(filtered) == 1
    assert ".footer" in filtered[0].data.get("selector", "")
