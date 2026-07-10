"""Phase 8 validation: cascade engine selector-first mapping accuracy."""

import json
import sys
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path.cwd()))

from site_audit.css_analyzer.cascade_engine import (
    CascadeEngine, CascadeReport, ThemeContext
)
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
    if not report_path.exists():
        print("No audit report found at /tmp/site_audit_p7/")
        sys.exit(1)

    report = json.loads(report_path.read_text())
    raw_issues = [i for i in report.get("visual_layer_issues", []) if isinstance(i, dict)]
    issues = [dict_to_issue(i) for i in raw_issues]
    print(f"📊 Visual issues: {len(issues)}")

    # Load cascade engine
    public_dir = str(Path("hugo-site/public"))
    engine = CascadeEngine(public_dir)
    engine.load()
    si = engine.source_index
    print(f"📦 {len(engine.all_rules)} rules, {len(engine.resolved_rules)} resolved")
    print(f"   Specificity computed for all rules")
    print(f"   Source index: {len(si._exact) if si else 0} selectors")
    print()

    # Resolve all visual issues through cascade engine
    ctx = ThemeContext(theme="light", viewport=(375, 812))
    cr: CascadeReport = engine.batch_resolve(issues, ctx)

    print(f"{'='*60}")
    print(f"  CASCADE ENGINE REPORT (Phase 8)")
    print(f"{'='*60}")
    print(f"  Total issues:     {cr.total_issues}")
    print(f"  Mapped:            {cr.mapped} ({cr.mapped_accuracy*100:.1f}%)")
    print(f"  Unmapped:          {len(cr.unmatched)}")
    print()
    print(f"  Confidence distribution:")
    print(f"    HIGH:    {cr.confidence_counts['HIGH']}  (cascade winner + variable chain)")
    print(f"    MEDIUM:  {cr.confidence_counts['MEDIUM']}  (cascade winner only)")
    print(f"    LOW:     {cr.confidence_counts['LOW']}  (selector match only)")
    print(f"    UNKNOWN: {cr.confidence_counts['UNKNOWN']}")

    # Top causes by variable/token
    vars_count = Counter()
    selectors_count = Counter()
    files_count = Counter()
    conf_by_var = Counter()
    for trace in cr.traces:
        w = trace.winner
        if not w:
            continue
        var_chain = " → ".join(w.variable_chain) if w.variable_chain else "(direct)"
        vars_count[var_chain] += 1
        conf_by_var[(var_chain, w.confidence)] += 1
        selectors_count[w.selector] += 1
        files_count[w.source_file] += 1

    print()
    print(f"  🏆 Top variables/chains:")
    for v, c in vars_count.most_common(5):
        print(f"    {v}: {c} issues")

    print()
    print(f"  🏆 Top source files:")
    for f, c in files_count.most_common(5):
        print(f"    {Path(f).name}: {c} issues")

    print()
    print(f"  🏆 Top winning selectors:")
    for s, c in selectors_count.most_common(5):
        print(f"    {s}: {c} issues")

    # Unmatched details
    if cr.unmatched:
        print()
        print(f"  ❌ Unmatched ({len(cr.unmatched)} shown):")
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

    # Sample cascade traces
    print()
    print(f"  🔍 Sample cascade traces (first 5):")
    for trace in cr.traces[:5]:
        w = trace.winner
        if not w:
            continue
        var_chain_str = " → ".join(w.variable_chain) if w.variable_chain else "N/A"
        spec_str = f"({w.specificity[0]},{w.specificity[1]},{w.specificity[2]})"
        overridden_str = f"{len(trace.overridden)} overridden" if trace.overridden else "no overrides"
        print(f"    {trace.element_selector:30s} → {w.selector:30s} [{spec_str}]")
        print(f"      var_chain: {var_chain_str}")
        print(f"      confidence: {w.confidence} | {overridden_str}")

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
                "issue_selector": trace.element_selector,
                "computed_color": trace.computed_color,
                "css_source_file": trace.winner.source_file if trace.winner else "",
                "css_selector": trace.winner.selector if trace.winner else "",
                "css_line": trace.winner.source_line if trace.winner else 0,
                "variable_chain": trace.winner.variable_chain if trace.winner else [],
                "specificity": list(trace.winner.specificity) if trace.winner else [0,0,0],
                "confidence": trace.winner.confidence if trace.winner else "UNKNOWN",
                "overridden_count": len(trace.overridden),
            }
            for trace in cr.traces
        ],
        "unmatched": [
            {"selector": (u.data or {}).get("selector", ""),
             "fg": (u.data or {}).get("fg", ""),
             "ratio": (u.data or {}).get("ratio", "")}
            for u in cr.unmatched[:20]
        ],
    }
    Path("/tmp/site_audit_p8/cascade_mapping.json").parent.mkdir(exist_ok=True)
    Path("/tmp/site_audit_p8/cascade_mapping.json").write_text(
        json.dumps(output, indent=2, ensure_ascii=False)
    )
    print(f"\n  ✅ Saved /tmp/site_audit_p8/cascade_mapping.json")

    # Markdown report
    md = [
        "# Phase 8: CSS Cascade Engine — Validation Report",
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
        f"- **HIGH:** {cr.confidence_counts['HIGH']} (cascade winner + variable chain)",
        f"- **MEDIUM:** {cr.confidence_counts['MEDIUM']} (cascade winner only)",
        f"- **LOW:** {cr.confidence_counts['LOW']} (selector match only)",
        f"- **UNKNOWN:** {cr.confidence_counts['UNKNOWN']}",
        "",
        "### Top CSS Variable Chains",
        "",
    ]
    for v, c in vars_count.most_common(10):
        md.append(f"- `{v}`: {c} issues")
    md += [
        "",
        "### Cascade Trace Examples",
        "",
        "| Element | Winning Selector | Specificity | Variable Chain | Confidence | Overridden |",
        "|---------|-----------------|-------------|----------------|------------|------------|",
    ]
    for trace in cr.traces[:15]:
        w = trace.winner
        if not w:
            continue
        var_str = " → ".join(w.variable_chain[:3]) if w.variable_chain else "-"
        spec_str = f"({w.specificity[0]},{w.specificity[1]},{w.specificity[2]})"
        md.append(
            f"| {trace.element_selector} | {w.selector} | {spec_str} | "
            f"`{var_str}` | {w.confidence} | {len(trace.overridden)} |"
        )
    md += [
        "",
        "### Limitations",
        "",
        "- Dynamic JS-generated colors not resolvable",
        "- Inline styles not captured in CSS source index",
        "- Shadow DOM / scoped styles may have lower match rates",
        "- `@media` context matching is heuristic-based (viewport=375x812, light mode)",
    ]

    Path("/tmp/site_audit_p8/cascade_resolution_report.md").parent.mkdir(exist_ok=True)
    Path("/tmp/site_audit_p8/cascade_resolution_report.md").write_text("\n".join(md))
    print(f"  ✅ Saved /tmp/site_audit_p8/cascade_resolution_report.md")

    return cr.mapped_accuracy, cr.confidence_counts


if __name__ == "__main__":
    acc, conf = main()
    print(f"\n{'='*60}")
    status = "✅ PASS" if acc >= 0.80 else f"⚠️  Below 80% threshold ({acc*100:.1f}%)"
    print(f"  PHASE 8 VALIDATION: {status}")
    print(f"  Confidence: {conf}")
