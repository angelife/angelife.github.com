#!/usr/bin/env python3
"""site-audit CLI — Hugo静态站点排版体检工具."""

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

from .models.issue import Issue, Severity, AuditSummary
from .scanner.scanner import scan_source
from .scoring.score import compute_score
from .reporter.json_report import generate_json
from .reporter.html_report import generate_html


def main():
    parser = argparse.ArgumentParser(
        description="site-audit — Hugo静态站点排版体检系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  site-audit /path/to/hugo/project
  site-audit . --max-pages 50 --browser-path /usr/bin/chromium
  site-audit . --url https://example.com --output ./reports/
        """,
    )
    parser.add_argument("path", nargs="?", default=".", help="Project directory")
    parser.add_argument("--url", help="Live URL (skip Hugo server startup)")
    parser.add_argument("--evidence-export", action="store_true",
                        help="Export structured DOM evidence JSON (Phase 8A) to evidence/ directory")
    parser.add_argument("--mobile-only", action="store_true", help="Only check mobile viewport")
    parser.add_argument("--max-pages", type=int, default=100, help="Max pages to scan (default: 100)")
    parser.add_argument("--output", default="./", help="Output directory for reports")
    parser.add_argument("--skip-render", action="store_true", help="Skip render-layer audit (source only)")
    parser.add_argument("--baseline", help="Baseline JSON file to diff against (only report new issues)")
    parser.add_argument("--save-baseline", help="Save current issues as baseline to FILE")
    parser.add_argument("--severity-threshold", choices=["critical", "major", "minor"], default="minor",
                        help="Minimum severity to report (default: minor = all)")
    parser.add_argument("--browser-path", help="Path to Chrome/Chromium binary (unused with Playwright)")
    parser.add_argument("--ci", action="store_true", help="CI mode: exit 2=new critical, 1=new major, 0=pass")
    parser.add_argument("--contrast-screenshot", action="store_true",
                        help="Take screenshot evidence for contrast issues (1 per selector)")
    parser.add_argument("--css-audit", default=True, action=argparse.BooleanOptionalAction,
                        help="Run CSS Design Token Audit after render layer (default: on)")
    parser.add_argument("--patch-preview", action="store_true",
                        help="Generate site_audit_patch.md (preview only, no files modified)")
    parser.add_argument("--css-snapshot", help="Save CSS token snapshot to FILE (e.g. css_snapshot.json)")
    parser.add_argument("--css-baseline", help="CSS snapshot baseline file for regression detection")
    parser.add_argument("--css-regression", action="store_true",
                        help="Detect CSS token drift against baseline (requires --css-baseline)")

    args = parser.parse_args()
    start = time.time()

    # Prepare output dirs
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir = output_dir / "evidence"
    evidence_dir.mkdir(exist_ok=True)

    print(f"\U0001f50d site-audit: {args.path}")
    print(f"   Output: {output_dir}")

    # ========== SOURCE LAYER ==========
    print("\n\U0001f4c4 Source Layer Audit...")
    source_issues = scan_source(args.path)
    print(f"   Found {len(source_issues)} source issues")

    # ========== SEVERITY FILTER ==========
    sev_map = {"critical": Severity.CRITICAL, "major": Severity.MAJOR, "minor": Severity.MINOR}
    threshold = sev_map[args.severity_threshold]
    active_scores = [Severity.CRITICAL, Severity.MAJOR, Severity.MINOR]
    source_issues = [i for i in source_issues if active_scores.index(i.severity) <= active_scores.index(threshold)]

    # ========== BASELINE DIFF (source layer) ==========
    if args.baseline:
        from .reporter.baseline import load_baseline, filter_new_issues
        print(f"   Loading baseline: {args.baseline}")
        baseline = load_baseline(args.baseline)
        source_issues, matched = filter_new_issues(source_issues, baseline)
        print(f"   {matched} existing issues suppressed, {len(source_issues)} new")

    # ========== RENDER LAYER ==========
    visual_issues: list[Issue] = []
    pages_scanned = 0
    browser_path = None

    if not args.skip_render:
        print("\n\U0001f5a5\ufe0f  Render Layer Audit...")
        try:
            from .renderer.server import start_hugo_server, stop_hugo_server, build_hugo
            from .renderer.browser import launch_browser, close_browser, get_page_urls
            from .renderer.contrast import check_contrast, check_font_size
            from .renderer.overflow import check_overflow

            port = 0
            server = None
            page = None

            if args.url:
                base_url = args.url.rstrip("/")
            else:
                print("   Building Hugo site...")
                try:
                    build_hugo(args.path)
                except Exception as e:
                    print(f"   \u26a0\ufe0f Hugo build: {e}")

                print("   Starting Hugo server...")
                server, port = start_hugo_server(args.path, port=0)
                base_url = f"http://127.0.0.1:{port}"

            print("   Launching Playwright Chromium...")
            p_obj, browser, page = launch_browser(headless=True)
            print("   Playwright ready")

            print(f"   Discovering pages (max: {args.max_pages})...")
            urls = get_page_urls(page, base_url, max_pages=args.max_pages)
            pages_scanned = len(urls)
            print(f"   Found {pages_scanned} pages")

            for i, url in enumerate(urls, 1):
                print(f"   [{i}/{pages_scanned}] {url}")
                try:
                    evidence_export_dir = evidence_dir if args.evidence_export else None
                    visual_issues.extend(check_contrast(page, url, evidence_dir, args.contrast_screenshot, evidence_export_dir))
                    visual_issues.extend(check_font_size(page, url))
                    visual_issues.extend(check_overflow(page, url, evidence_dir))
                except Exception as e:
                    print(f"      \u26a0\ufe0f error: {e}")

            close_browser(browser, p_obj)
            if server:
                stop_hugo_server(server)

            print(f"   Found {len(visual_issues)} visual issues")

        except ImportError as e:
            print(f"   \u26a0\ufe0f Render layer unavailable: {e}")
        except SystemExit:
            pass
        except Exception as e:
            print(f"   \u26a0\ufe0f Render layer error: {e}")

    # ========== BASELINE DIFF (visual layer) ==========
    baseline_matched = 0
    if args.baseline and visual_issues:
        from .reporter.baseline import load_baseline, filter_new_issues
        bl_fps = load_baseline(args.baseline)
        visual_issues, matched = filter_new_issues(visual_issues, bl_fps)
        baseline_matched = matched
        print(f"   Baseline: {matched} visual issues suppressed, {len(visual_issues)} new")

    # ========== AGGREGATION ==========
    from .reporter.baseline import aggregate_by_selector
    sel_summary = aggregate_by_selector(visual_issues)

    # ========== SCORING ==========
    all_issues = source_issues + visual_issues
    score = compute_score(all_issues)
    elapsed = time.time() - start

    summary = AuditSummary(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        target=str(Path(args.path).resolve()),
        files_scanned=len(set(i.file for i in source_issues if i.file)),
        pages_scanned=pages_scanned,
        score=score,
        issue_count=len(all_issues),
        source_layer_issues=source_issues,
        visual_layer_issues=visual_issues,
        summary_by_selector=sel_summary,
    )

    # ========== PRINT AGGREGATION ==========
    if sel_summary:
        top_selectors = sorted(sel_summary.items(), key=lambda x: -x[1])[:5]
        print(f"\n  Top CSS selectors by issue count:")
        for sel, cnt in top_selectors:
            print(f"    {sel}: {cnt}")

    # ========== SAVE BASELINE ==========
    if args.save_baseline:
        from .reporter.baseline import save_baseline
        save_baseline(source_issues + visual_issues, args.save_baseline)
        print(f"   Baseline saved: {args.save_baseline}")

    # ========== CSS DESIGN TOKEN AUDIT ==========
    css_token_issues = None
    if args.css_audit and visual_issues:
        try:
            print("\n\U0001f3a8  CSS Design Token Audit...")
            from .css_analyzer.parser import parse_all_css
            from .css_analyzer.variables import build_variable_graph, resolve_all_variables, filter_color_rules
            from .css_analyzer.colors import build_color_tokens, rank_tokens
            from .css_analyzer.matcher import match_issues_to_rules, enrich_issues
            from .css_analyzer.report import generate_css_token_issues

            # Determine CSS location (Hugo public/ output)
            hugo_public = Path(args.path) / "public"
            if not hugo_public.is_dir():
                # Try subdirectory hugo-site/public
                hugo_public = Path(args.path) / "hugo-site" / "public"

            if hugo_public.is_dir():
                css_dir = str(hugo_public)
                print(f"   Scanning: {css_dir}/*.css")

                all_rules = parse_all_css(css_dir)
                print(f"   Found {len(all_rules)} CSS rules")

                if all_rules:
                    var_map = build_variable_graph(all_rules)
                    if var_map:
                        print(f"   CSS variables: {len(var_map)}")

                    resolved = resolve_all_variables(all_rules, var_map)
                    color_rules = filter_color_rules(all_rules + resolved)
                    tokens = build_color_tokens(color_rules)
                    ranked = rank_tokens(tokens)
                    print(f"   Color tokens: {len(ranked)}")

                    # Connect visual issues to CSS rules (enrich in place)
                    enriched = enrich_issues(visual_issues, color_rules)

                    css_token_issues = generate_css_token_issues(tokens, enriched)
                    if css_token_issues:
                        print(f"   Token-level issues: {len(css_token_issues)}")
                        for ti in css_token_issues[:3]:
                            print(f"     {ti['color']} ({ti.get('variable','?')}): "
                                  f"{ti['issue_count']} instances, ratio {ti['contrast_min']}:1")
                            if ti.get('suggestion'):
                                print(f"       → {ti['suggestion']}")
                    else:
                        print("   No token-level issues (all contrast passes WCAG AA)")
            else:
                print(f"   \u26a0 Hugo public/ not found at {hugo_public} — run `hugo` first")

        except ImportError as e:
            print(f"   \u26a0 CSS audit unavailable: {e}")
        except Exception as e:
            print(f"   \u26a0 CSS audit error: {e}")

    # ========== PATCH PREVIEW (Phase 6) ==========
    if args.patch_preview and css_token_issues:
        try:
            print("\n\u2702\ufe0f  Patch Preview (read-only)...")
            from .css_analyzer.candidates import generate_candidates
            from .css_analyzer.patch import generate_patches
            from .css_analyzer.patch.preview import generate_markdown_preview
            from .css_analyzer.simulation import simulate_bulk
            from .css_analyzer.colors import ColorToken

            # Generate 3-tier candidates and attach to token issues
            token_list = list(tokens.values()) if 'tokens' in dir() else []
            if token_list:
                for ti in css_token_issues:
                    tok = next((t for t in token_list if t.value == ti["color"]), None)
                    if tok:
                        cands = generate_candidates(tok)
                        ti["candidates"] = cands
                        # Use balanced as recommendation
                        bal = next((c for c in cands if c["level"] == "balanced"), None)
                        if bal:
                            ti["recommended"] = bal["color"]

            # Generate patches
            token_list = list(tokens.values()) if 'tokens' in dir() else []
            patches = generate_patches(token_list, css_token_issues)
            if patches:
                print(f"   Patches generated: {len(patches)}")
                for p in patches:
                    print(f"     {p.variable}: {p.old_value} → {p.new_value} ({p.source_file}:{p.line})")

                # Generate simulation
                sim_results = simulate_bulk(token_list, css_token_issues)
                if sim_results:
                    print(f"   Simulations: {len(sim_results)}")
                    for s in sim_results:
                        print(f"     {s.variable}: {s.before_failures} issues → {s.after_failures} issues ({s.before_ratio}:1 → {s.after_ratio}:1)")

                # Write patch preview
                preview_path = str(output_dir / "site_audit_patch.md")
                generate_markdown_preview(patches, preview_path, [s.to_dict() for s in sim_results])
                print(f"   Preview: {preview_path}")
                print("   \u26a0 Preview only. No files modified.")
            else:
                print("   No patches generated (no variable-bound tokens)")

        except Exception as e:
            print(f"   \u26a0 Patch preview error: {e}")

    # ========== CSS SNAPSHOT (Phase 6) ==========
    if args.css_snapshot and 'tokens' in dir() and tokens:
        try:
            from .css_analyzer.snapshot import save_snapshot
            sp = save_snapshot(tokens, args.css_snapshot)
            print(f"\U0001f4f8  CSS snapshot saved: {sp}")
        except Exception as e:
            print(f"   \u26a0 CSS snapshot error: {e}")

    # ========== CSS REGRESSION (Phase 6) ==========
    if args.css_regression:
        try:
            from .css_analyzer.snapshot import load_snapshot, save_snapshot, diff_snapshots, generate_regression_report
            current_snap = save_snapshot(tokens, str(output_dir / ".css_snapshot_current.json")) if 'tokens' in dir() and tokens else None

            baseline_path = args.css_baseline
            if not baseline_path:
                print("   \u26a0 --css-baseline required with --css-regression")
            elif not Path(baseline_path).is_file():
                print(f"   \u26a0 Baseline not found: {baseline_path}")
            elif 'tokens' not in dir() or not tokens:
                print("   \u26a0 No tokens to compare")
            else:
                baseline = load_snapshot(baseline_path)
                diff = diff_snapshots(load_snapshot(current_snap), baseline) if current_snap else {"changed": [], "added": [], "removed": []}
                report = generate_regression_report(diff)

                reg_path = str(output_dir / "css_regression_report.json")
                import json
                Path(reg_path).write_text(json.dumps({
                    "timestamp": {"current": diff.get("timestamp", {}).get("current", ""),
                                  "baseline": diff.get("timestamp", {}).get("baseline", "")},
                    "regression": report,
                }, ensure_ascii=False, indent=2), encoding="utf-8")

                print(f"\U0001f504  CSS Regression Report: {reg_path}")
                if report:
                    changed = [r for r in report if r["type"] == "changed"]
                    added = [r for r in report if r["type"] == "added"]
                    removed = [r for r in report if r["type"] == "removed"]
                    if changed:
                        print(f"   Changed: {len(changed)}")
                        for r in changed:
                            print(f"     {r.get('variable','?')}: {r.get('before','')} → {r.get('after','')}")
                    if added:
                        print(f"   Added: {len(added)}")
                    if removed:
                        print(f"   Removed: {len(removed)}")
                    if args.ci and changed:
                        print("   \u26a0 CSS regression detected changes — review required")
                else:
                    print("   No regressions detected. \u2705")

        except Exception as e:
            print(f"   \u26a0 CSS regression error: {e}")

    # ========== REPORTS ==========
    json_path = generate_json(summary, str(output_dir / "site_audit_report.json"),
                              css_token_issues=css_token_issues)
    # v1.0 unified report
    from .reporter.json_report import generate_report
    from .models.evidence import Report as UnifiedReport, ReportMetadata, Metrics, issue_to_evidence
    unified = UnifiedReport(
        metadata=ReportMetadata(
            version="1.0",
            timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            target=str(Path(args.path).resolve()),
            duration_seconds=round(elapsed, 1),
            pages_scanned=pages_scanned,
        ),
        evidence=[issue_to_evidence(i) for i in all_issues],
        metrics=Metrics(
            score=score,
            total_issues=len(all_issues),
            by_severity={"critical": sum(1 for i in all_issues if i.severity == Severity.CRITICAL),
                         "major": sum(1 for i in all_issues if i.severity == Severity.MAJOR),
                         "minor": sum(1 for i in all_issues if i.severity == Severity.MINOR)},
        ),
    )
    unified_path = generate_report(unified, str(output_dir / "site_audit_report.v1.json"))
    html_path = generate_html(summary, str(output_dir / "site_audit_report.html"))

    print(f"\n\u2554\u2550\u2550\u2550 Results \u2550\u2550\u2550\u2550")
    print(f"  Score:   {score}/100")
    print(f"  Issues:  {len(all_issues)} total")
    if baseline_matched:
        print(f"  Matched: {baseline_matched} (suppressed from baseline)")
    print(f"  Time:    {elapsed:.1f}s")
    print(f"  JSON:    {json_path}")
    print(f"  HTML:    {html_path}")

    if browser_path:
        print(f"  Browser: {browser_path}")

    evidence_files = list(evidence_dir.glob("*.png"))
    if evidence_files:
        print(f"  Evidence: {len(evidence_files)} screenshot(s) at {evidence_dir}")

    # ========== CI MODE ==========
    if args.ci:
        new_critical = sum(1 for i in all_issues if i.severity == Severity.CRITICAL)
        new_major = sum(1 for i in all_issues if i.severity == Severity.MAJOR)

        if new_critical > 0:
            print(f"\n  \U0001f6a8 CI FAIL: {new_critical} new critical issues")
            return 2
        elif new_major > 0:
            print(f"\n  \U0001f6a8 CI FAIL: {new_major} new major issues")
            return 1
        else:
            print(f"\n  \u2705 CI PASS: no new critical/major issues")
            return 0

    return 0 if score >= 70 else 1


if __name__ == "__main__":
    sys.exit(main())
