"""Phase 7.1 validation: selector-first cascade mapping accuracy."""

import json
import sys
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path.cwd()))

from site_audit.css_analyzer.cascade import CascadeResolver, CascadeReport
from site_audit.models.issue import Issue


def dict_to_issue(d: dict) -> Issue:
    return Issue(
        rule=d.get("rule", "visual/contrast"),
        severity=d.get("severity", "major"),
        message=d.get("message", ""),
        file=d.get("file", ""),
        line=d.get("line", 0),
        context=d.get("context", ""),
        suggestion=d.get("suggestion", ""),
        evidence_path=d.get("evidence_path", ""),
        data=d.get("data", {}),
    )


def main():
    report_path = Path("/tmp/site_audit_p7/site_audit_report.json")
    report = json.loads(report_path.read_text())
    raw_issues = [i for i in report.get("visual_layer_issues", []) if isinstance(i, dict)]
    issues = [dict_to_issue(i) for i in raw_issues]
    print(f"📊 Visual issues: {len(issues)}")

    resolver = CascadeResolver(str(Path("hugo-site/public")))
    resolver.load()
    si = resolver.source_index
    print(f"📦 {len(resolver.all_rules)} rules, {len(resolver.resolved_rules)} resolved, {len(si._exact) if si else 0} selectors")
    print()

    cr: CascadeReport = resolver.batch_resolve(issues)

    print(f"{'='*55}")
    print(f"  CASCADE MAPPING REPORT (Selector-First)")
    print(f"{'='*55}")
    print(f"  Total issues:     {cr.total_issues}")
    print(f"  Mapped:            {cr.mapped} ({cr.mapped_accuracy*100:.1f}%)")
    print(f"  Unmapped:          {len(cr.unmatched)}")
    print()
    print(f"  Confidence distribution:")
    print(f"    HIGH:    {cr.confidence_counts['HIGH']}")
    print(f"    MEDIUM:  {cr.confidence_counts['MEDIUM']}")
    print(f"    LOW:     {cr.confidence_counts['LOW']}")
    print(f"    UNKNOWN: {cr.confidence_counts['UNKNOWN']}")

    # Top causes by variable/token
    vars_count = Counter()
    selectors_count = Counter()
    files_count = Counter()
    for r in cr.matched_details:
        var = r.variable or "(direct)"
        vars_count[var] += 1
        selectors_count[r.css_selector] += 1
        files_count[r.css_source_file] += 1

    print()
    print(f"  🏆 Top variables:")
    for v, c in vars_count.most_common(5):
        print(f"    {v}: {c} issues")

    print()
    print(f"  🏆 Top source files:")
    for f, c in files_count.most_common(5):
        print(f"    {f}: {c} issues")

    print()
    print(f"  🏆 Top selectors:")
    for s, c in selectors_count.most_common(5):
        print(f"    {s}: {c} issues")

    # Unmatched details
    print()
    print(f"  ❌ Sample unmatched ({min(8, len(cr.unmatched))} shown):")
    color_styles = Counter()
    for u in cr.unmatched[:8]:
        d = u.data or {}
        sel = d.get("selector", "?")
        fg = d.get("fg", "")
        color_styles[fg] += 1
        print(f"    {sel:30s}  fg={fg:20s}  ratio={d.get('ratio','?'):>6s}")

    print()
    print(f"  📊 Unmatched color frequencies:")
    for fg, c in color_styles.most_common(5):
        print(f"    {fg}: {c} unmatched")

    # Save reports
    output = {
        "accuracy": {
            "total_issues": cr.total_issues,
            "mapped": cr.mapped,
            "unmatched": len(cr.unmatched),
            "accuracy": f"{cr.mapped_accuracy*100:.1f}%",
            "confidence": cr.confidence_counts,
        },
        "match_details": [
            {
                "issue_selector": r.issue_selector,
                "computed_color": r.computed_color,
                "css_source_file": r.css_source_file,
                "css_selector": r.css_selector,
                "css_line": r.css_line,
                "variable": r.variable,
                "variable_resolved": r.variable_resolved,
                "source_color": r.source_color,
                "specificity": r.specificity,
                "confidence": r.confidence,
                "color_delta": r.color_delta,
                "theme": r.theme,
            }
            for r in cr.matched_details
        ],
        "unmatched": [
            {"selector": (u.data or {}).get("selector", ""),
             "fg": (u.data or {}).get("fg", ""),
             "ratio": (u.data or {}).get("ratio", "")}
            for u in cr.unmatched[:20]
        ],
    }
    Path("/tmp/site_audit_p7/cascade_mapping.json").write_text(
        json.dumps(output, indent=2, ensure_ascii=False)
    )
    print(f"\n  ✅ Saved /tmp/site_audit_p7/cascade_mapping.json")

    # Markdown report
    md = [
        "# Phase 7.1: Cascade Mapping Report (Selector-First)",
        "",
        f"**Mapping Accuracy: {cr.mapped_accuracy*100:.1f}%**",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Total Visual Issues | {cr.total_issues} |",
        f"| Mapped | {cr.mapped} |",
        f"| Unmapped | {len(cr.unmatched)} |",
        "",
        "### Confidence Distribution",
        "",
        f"- **HIGH:** {cr.confidence_counts['HIGH']}",
        f"- **MEDIUM:** {cr.confidence_counts['MEDIUM']}",
        f"- **LOW:** {cr.confidence_counts['LOW']}",
        f"- **UNKNOWN:** {cr.confidence_counts['UNKNOWN']}",
        "",
        "### Top CSS Variables/Colors",
        "",
    ]
    for v, c in vars_count.most_common(10):
        md.append(f"- `{v}`: {c} issues")
    md += [
        "",
        "### Before/After Mapping",
        "",
        "| Selector | Computed | Source | Variable | Delta | Confidence |",
        "|----------|----------|--------|----------|-------|------------|",
    ]
    for r in cr.matched_details[:15]:
        md.append(
            f"| {r.issue_selector} | {r.computed_color} | {r.source_color} | "
            f"{r.variable or '-'} | {r.color_delta} | {r.confidence} |"
        )
    md += [
        "",
        "### Unmatched Analysis",
        "",
    ]
    for fg, c in color_styles.most_common(5):
        md.append(f"- `{fg}`: {c} unmapped issues")

    Path("/tmp/site_audit_p7/cascade_resolution_report.md").write_text("\n".join(md))
    print(f"  ✅ Saved /tmp/site_audit_p7/cascade_resolution_report.md")

    return cr.mapped_accuracy


if __name__ == "__main__":
    acc = main()
    print(f"\n{'='*55}")
    status = "✅ PASS" if acc >= 0.80 else f"⚠️  Below 80% threshold ({acc*100:.1f}%)"
    print(f"  PHASE 7.1 VALIDATION: {status}")