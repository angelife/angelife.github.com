"""Tests for unified Evidence model (v1.0 Architecture)."""

import json
import pytest

from models.evidence import (
    Evidence, ElementInfo, ComputedInfo, SourceInfo,
    Finding, Recommendation, Report, ReportMetadata, Metrics,
    EvidenceKind, Severity, Confidence,
    issue_to_evidence,
)


class TestBasicCreation:
    def test_minimal_evidence(self):
        ev = Evidence(kind="source", analyzer="markdown")
        assert ev.kind == "source"
        assert ev.analyzer == "markdown"

    def test_full_evidence(self):
        ev = Evidence(
            kind="visual",
            analyzer="contrast",
            page="/posts/test/",
            viewport="375x812",
            theme="light",
            element=ElementInfo(
                tag="h1",
                classes=["post-title"],
                css_path="body > main > article.post-single > h1.post-title",
            ),
            computed=ComputedInfo(
                color="rgb(51, 51, 51)",
                background_color="rgba(0, 0, 0, 0)",
                font_size="24px",
            ),
            source=SourceInfo(
                css_file="style.css",
                selector=".post-title",
                property="color",
                value="var(--primary)",
                variable_chain=["--primary", "--text", "#333333"],
            ),
            finding=Finding(
                rule="visual/contrast",
                severity="major",
                confidence="medium",
                message="Low contrast ratio 3.2:1",
                suggestion="Increase to at least 4.5:1",
            ),
            recommendation=Recommendation(
                patch=".post-title { color: #222; }",
                file="style.css",
                line=42,
            ),
        )
        d = ev.to_dict()
        assert d["kind"] == "visual"
        assert d["element"]["tag"] == "h1"
        assert d["computed"]["color"] == "rgb(51, 51, 51)"
        assert d["source"]["variable_chain"] == ["--primary", "--text", "#333333"]
        assert d["finding"]["rule"] == "visual/contrast"
        assert d["recommendation"]["file"] == "style.css"

    def test_missing_optional_fields(self):
        """Evidence with only required fields should serialize."""
        ev = Evidence(kind="source", analyzer="markdown")
        d = ev.to_dict()
        # Default sub-models have empty default values, not missing
        assert d["element"]["tag"] == ""
        assert d["element"]["classes"] == []
        assert d["finding"]["rule"] == ""
        assert d["finding"]["severity"] == "info"
        assert d["source"]["css_file"] == ""

    def test_metadata_freeform(self):
        ev = Evidence(kind="visual", analyzer="contrast", metadata={"ratio": 3.2})
        assert ev.metadata["ratio"] == 3.2


class TestReport:
    def test_empty_report(self):
        rpt = Report()
        d = rpt.to_dict()
        assert d["evidence"] == []
        assert d["metrics"]["score"] == 100
        assert d["metrics"]["total_issues"] == 0

    def test_report_with_evidence(self):
        rpt = Report()
        rpt.metadata.target = "~/mysite"
        rpt.evidence = [
            Evidence(kind="source", analyzer="markdown"),
            Evidence(kind="visual", analyzer="contrast"),
        ]
        rpt.metrics.total_issues = 2
        rpt.metrics.by_severity = {"major": 1, "info": 1}
        d = rpt.to_dict()
        assert len(d["evidence"]) == 2
        assert d["metrics"]["total_issues"] == 2

    def test_report_json_roundtrip(self):
        rpt = Report()
        rpt.metadata.target = "~/test"
        rpt.metadata.version = "1.0"
        rpt.evidence.append(
            Evidence(kind="visual", analyzer="contrast", page="/test/")
        )
        j = json.dumps(rpt.to_dict(), ensure_ascii=False)
        loaded = json.loads(j)
        assert loaded["metadata"]["version"] == "1.0"
        assert len(loaded["evidence"]) == 1


class TestBackwardCompat:
    def test_issue_to_evidence_basic(self):
        """Test conversion from v0.x Issue-like object."""

        class MockIssue:
            def __init__(self):
                self.rule = "visual/contrast"
                self.severity = Severity.MAJOR
                self.message = "Low contrast 3.2:1"
                self.suggestion = "Increase to 4.5:1"
                self.file = "/posts/test/"
                self.line = 0
                self.data = {
                    "selector": "h1.post-title",
                    "fg": "rgb(51, 51, 51)",
                    "bg": "rgb(255, 255, 255)",
                    "fontSize": "24px",
                    "ratio": 3.2,
                }

            def fingerprint(self):
                return "contrast:h1.post-title:rgb(51,51,51):rgb(255,255,255):3.2"

        mock = MockIssue()
        ev = issue_to_evidence(mock)
        assert ev.kind == "visual"
        assert ev.finding.rule == "visual/contrast"
        assert ev.finding.message == "Low contrast 3.2:1"
        assert ev.element.css_path == "h1.post-title"
        assert ev.computed.color == "rgb(51, 51, 51)"

    def test_infer_kind(self):
        from models.evidence import _infer_kind
        assert _infer_kind("visual/contrast") == "visual"
        assert _infer_kind("visual/overflow") == "visual"
        assert _infer_kind("css/token") == "css_token"
        assert _infer_kind("source/heading-order") == "source"
        assert _infer_kind("spacing") == "source"


class TestElementInfo:
    def test_minimal(self):
        e = ElementInfo(tag="p")
        d = e.to_dict()
        assert d["tag"] == "p"
        assert d["classes"] == []

    def test_with_id_and_ancestors(self):
        e = ElementInfo(
            tag="div",
            id="header",
            classes=["main-header", "sticky"],
            css_path="body > div#header.main-header",
            ancestor_chain=[
                {"tag": "body", "id": "", "classes": []},
                {"tag": "div", "id": "header", "classes": ["main-header"]},
            ],
        )
        d = e.to_dict()
        assert d["id"] == "header"
        assert d["classes"] == ["main-header", "sticky"]
        assert len(d["ancestor_chain"]) == 2


class TestMetrics:
    def test_by_severity(self):
        m = Metrics(score=85, total_issues=5, by_severity={"major": 3, "minor": 2})
        d = m.to_dict()
        assert d["score"] == 85
        assert d["by_severity"]["major"] == 3