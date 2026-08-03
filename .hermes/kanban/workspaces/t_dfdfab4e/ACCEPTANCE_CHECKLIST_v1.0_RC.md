# site_audit v1.0 RC — Acceptance Checklist

**Date:** 2026-07-11
**Version:** v0.7.20
**Status:** ✅ PASS (RC Ready)

---

## 1. Evidence Model (v1.0 Architecture)

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1.1 | Unified Evidence model replaces v0.x per-analyzer Issue structs | ✅ PASS | `models/evidence.py` — `Evidence`, `ElementInfo`, `ComputedInfo`, `SourceInfo`, `Finding`, `Recommendation` dataclasses |
| 1.2 | All analyzers produce Evidence (source, visual, CSS) | ✅ PASS | `issue_to_evidence()` backward compat in `models/evidence.py` |
| 1.3 | All consumers read Evidence (report, patch, HTML inspector) | ✅ PASS | `Report` dataclass with `evidence: List[Evidence]` |
| 1.4 | Evidence JSON serialization roundtrip | ✅ PASS | `test_evidence.py::TestReport::test_report_json_roundtrip` |
| 1.5 | Backward compat: v0.x Issue → v1.0 Evidence conversion | ✅ PASS | `issue_to_evidence()` + `test_issue_to_evidence_basic` |
| 1.6 | Evidence schema: url + elements top-level structure | ✅ PASS | 50 evidence JSON files validated (2,689 elements) |

## 2. Scoring System

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 2.1 | Perfect score (no issues) = 100 | ✅ PASS | `test_scoring.py::test_perfect_score` |
| 2.2 | Critical: -10 each, capped at -50 | ✅ PASS | `test_scoring.py::test_critical_penalty`, `test_critical_capped` |
| 2.3 | Major: -3 each, capped at -30 | ✅ PASS | `test_scoring.py::test_major_capped` |
| 2.4 | Minor: -1 per 100 issues, capped at -20 | ✅ PASS | `test_scoring.py::test_minor_graded` |
| 2.5 | Mixed scenario scoring correct | ✅ PASS | `test_scoring.py::test_mixed_scenario` |
| 2.6 | Grade thresholds (A/B/C/D) | ✅ PASS | `test_scoring.py::test_grade_thresholds` |
| 2.7 | Severity counts aggregation | ✅ PASS | `test_scoring.py::test_severity_counts` |

## 3. Source Layer Scanner

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 3.1 | Markdown heading level skip detection (H1→H3) | ✅ PASS | `test_headings.py::test_heading_skip_level` |
| 3.2 | HR separator resets heading continuity | ✅ PASS | `test_headings.py::test_heading_no_skip_with_hr` |
| 3.3 | Missing blank line before heading detection | ✅ PASS | `test_headings.py::test_heading_spacing_blank_before` |
| 3.4 | CJK-ASCII missing space detection | ✅ PASS | `test_spacing.py::test_cjk_ascii_missing_space` |
| 3.5 | ASCII-CJK missing space detection | ✅ PASS | `test_spacing.py::test_ascii_cjk_missing_space` |
| 3.6 | IPv4 addresses ignored (no false positive) | ✅ PASS | `test_spacing.py::test_ipv4_ignored` |
| 3.7 | Acronyms (CSS, HTML, AI) handled correctly | ✅ PASS | `test_spacing.py::test_acronyms_ignored` |
| 3.8 | Properly spaced CN/EN text — no false positive | ✅ PASS | `test_spacing.py::test_no_false_positive_with_spaces` |

## 4. Render Layer (Browser)

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 4.1 | Contrast ratio calculation (WCAG) | ✅ PASS | `test_contrast.py` — luminance, ratio, RGB/RGBA parsing |
| 4.2 | Hugo server control (start/stop) | ✅ PASS | `renderer/server.py` — integrated in full audit pipeline |
| 4.3 | Chromium browser control | ✅ PASS | `renderer/browser.py` — integrated in full audit pipeline |
| 4.4 | Mobile viewport overflow detection | ✅ PASS | 5 overflow screenshots captured during evidence export |
| 4.5 | Font size < 12px detection | ✅ PASS | `renderer/overflow.py` — integrated in full audit |

## 5. CSS Analyzer

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 5.1 | CSS parser — rule extraction | ✅ PASS | `test_css_parser.py` (10 tests) |
| 5.2 | Selector matching (specificity, ancestry) | ✅ PASS | `test_selector_match.py` (17 tests) |
| 5.3 | Full specificity calculation | ✅ PASS | `test_specificity_full.py` (20 tests) |
| 5.4 | CSS variable resolution chain | ✅ PASS | `test_variable_resolver.py` (7 tests), `test_variable_chain.py` (6 tests) |
| 5.5 | Cascade resolution (origin, layer, order) | ✅ PASS | `test_cascade.py` (7 tests), `test_cascade_order.py` (5 tests) |
| 5.6 | Media query handling | ✅ PASS | `test_media_query.py` (10 tests) |
| 5.7 | CSS snapshot parsing | ✅ PASS | `test_css_snapshot.py` (6 tests) |
| 5.8 | Color token analysis | ✅ PASS | `test_color_token.py` (6 tests) |
| 5.9 | Color suggestion generation | ✅ PASS | `test_color_suggestion.py` (6 tests) |
| 5.10 | Color candidate generation | ✅ PASS | `test_color_candidates.py` (4 tests) |
| 5.11 | Mapping confidence scoring | ✅ PASS | `test_mapping_confidence.py` (9 tests) |
| 5.12 | Patch preview generation | ✅ PASS | `test_patch_preview.py` (5 tests) |
| 5.13 | Baseline comparison | ✅ PASS | `test_baseline.py` (5 tests) |
| 5.14 | Simulation mode | ✅ PASS | `test_simulation.py` (3 tests) |

## 6. Reporter

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 6.1 | JSON report output | ✅ PASS | `site_audit_report.json` generated with full evidence |
| 6.2 | HTML report output | ✅ PASS | `site_audit_report.html` generated |
| 6.3 | Evidence export (per-page JSON) | ✅ PASS | 50 evidence JSON files (2,689 elements) at `site_audit/evidence/` |
| 6.4 | Overflow screenshot capture | ✅ PASS | 5 overflow screenshot PNGs captured |

## 7. Test Coverage

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 7.1 | All 160 tests pass (100%) | ✅ PASS | `pytest` — 160 passed in 1.67s, 22 test files |
| 7.2 | No test regressions from v0.x | ✅ PASS | All 22 test files pass, no skips or failures |
| 7.3 | Test coverage across all modules | ✅ PASS | Evidence, scoring, headings, spacing, contrast, CSS parser, selector, cascade, variable, media query, snapshot, patch, baseline, simulation, color token, color suggestion, color candidates, mapping confidence |

## 7. Documentation

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 7.1 | README with v1.0 RC status banner | ✅ PASS | `site_audit/README.md` — Status: v1.0 RC, 2026-07-11 |
| 7.2 | Known issues section documented | ✅ PASS | `site_audit/README.md` — 6,763 minor issues listed with breakdown |
| 7.3 | Changelog entry (v0.7.20) | ✅ PASS | `hugo-site/data/changelog.yaml` — v0.7.20 entry with full summary |
| 7.4 | Scoring rules documented | ✅ PASS | `site_audit/README.md` — severity penalty table |
| 7.5 | Project structure documented | ✅ PASS | `site_audit/README.md` — directory tree |
| 7.6 | Limitations documented | ✅ PASS | `site_audit/README.md` — Hugo dependency, contrast, page limits |

## 8. Known Issues (Accepted for RC)

| # | Issue | Count | Impact | Resolution Plan |
|---|-------|-------|--------|-----------------|
| 8.1 | CJK spacing (CN/ASCII missing space) | 5,522 (81.6%) | Cosmetic — format preference only | Batch auto-fix post-RC |
| 8.2 | Heading blank lines (missing blank before heading) | 1,241 (18.4%) | Cosmetic — format preference only | Batch auto-fix post-RC |
| 8.3 | Total minor issues | 6,763 | Score impact: -20 (capped) | All cosmetic, no functional impact |

## 9. Overall Acceptance

| Criterion | Status |
|-----------|--------|
| All 160 tests pass | ✅ |
| 0 critical issues | ✅ |
| 0 major issues | ✅ |
| Evidence model v1.0 validated | ✅ |
| Documentation complete | ✅ |
| Known issues documented | ✅ |
| **Overall RC Acceptance** | **✅ PASS — Ready for v1.0 RC** |

**Score:** 80/100 (Grade B)
**Grade Interpretation:** ⚠️ Needs improvement (minor issues only)
**Recommendation:** Proceed to v1.0 RC. All 6,763 minor issues are cosmetic format preferences (CJK spacing + heading blank lines) with no functional impact. Batch auto-fix can be applied post-RC to raise score to 100.
