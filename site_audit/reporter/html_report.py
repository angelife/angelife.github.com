"""HTML report generation."""

from pathlib import Path
from typing import List
from datetime import datetime

from ..models.issue import Issue, Severity, AuditSummary
from ..scoring.score import severity_counts


def generate_html(summary: AuditSummary, output_path: str) -> Path:
    """Write the audit report as a human-readable HTML file."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    counts = severity_counts(summary.source_layer_issues + summary.visual_layer_issues)

    source_rows = _render_issue_rows(summary.source_layer_issues)
    visual_rows = _render_issue_rows(summary.visual_layer_issues)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>site-audit Report - {summary.target}</title>
<style>
:root {{ --bg: #fafafa; --card: #fff; --text: #1a1a2e; --border: #e2e8f0; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 20px; line-height: 1.6; }}
.wrap {{ max-width: 1200px; margin: 0 auto; }}
h1 {{ font-size: 1.5rem; margin: 0 0 4px 0; }}
.meta {{ color: #666; font-size: 0.85rem; margin-bottom: 20px; }}
.score-card {{ background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 24px; margin-bottom: 20px; }}
.score-number {{ font-size: 3rem; font-weight: 700; }}
.score-bar {{ height: 8px; background: #e2e8f0; border-radius: 4px; margin: 12px 0; overflow: hidden; }}
.score-fill {{ height: 100%; border-radius: 4px; transition: width 0.6s; }}
.badges {{ display: flex; gap: 12px; flex-wrap: wrap; }}
.badge {{ padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }}
.badge-critical {{ background: #fee2e2; color: #dc2626; }}
.badge-major {{ background: #fed7aa; color: #ea580c; }}
.badge-minor {{ background: #e0e7ff; color: #4f46e5; }}
section {{ background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 20px; margin-bottom: 16px; }}
h2 {{ font-size: 1.1rem; margin: 0 0 12px 0; }}
.issue {{ padding: 8px 0; border-bottom: 1px solid #f1f5f9; }}
.issue:last-child {{ border-bottom: none; }}
.issue-header {{ display: flex; gap: 8px; align-items: baseline; font-weight: 600; }}
.issue-file {{ color: #6366f1; font-size: 0.8rem; font-family: monospace; }}
.issue-line {{ color: #94a3b8; font-size: 0.75rem; }}
.issue-msg {{ margin: 4px 0; }}
.issue-ctx {{ font-size: 0.8rem; color: #64748b; background: #f8fafc; padding: 4px 8px; border-radius: 4px; font-family: monospace; }}
.issue-sug {{ font-size: 0.8rem; color: #16a34a; margin: 4px 0; }}
.sev-critical {{ border-left: 3px solid #dc2626; padding-left: 8px; }}
.sev-major {{ border-left: 3px solid #ea580c; padding-left: 8px; }}
.sev-minor {{ border-left: 3px solid #4f46e5; padding-left: 8px; }}
.no-issues {{ color: #16a34a; font-weight: 600; }}
</style>
</head>
<body>
<div class="wrap">
<h1>🔍 site-audit Report</h1>
<div class="meta">{summary.target} · {summary.timestamp} · {summary.files_scanned} files · {summary.pages_scanned} pages</div>

<div class="score-card">
<div class="score-number" style="color: {'#16a34a' if summary.score >= 90 else '#ea580c' if summary.score >= 70 else '#dc2626'}">{summary.score}/100</div>
<div class="score-bar"><div class="score-fill" style="width:{summary.score}%;background:{'#16a34a' if summary.score >= 90 else '#ea580c' if summary.score >= 70 else '#dc2626'}"></div></div>
<div class="badges">
<span class="badge badge-critical">🔴 {counts['critical']} critical</span>
<span class="badge badge-major">🟠 {counts['major']} major</span>
<span class="badge badge-minor">🔵 {counts['minor']} minor</span>
</div>
</div>

<section>
<h2>📄 Source Layer ({len(summary.source_layer_issues)} issues)</h2>
{source_rows if source_rows else '<p class="no-issues">✅ No source layer issues found.</p>'}
</section>

<section>
<h2>🖥️ Render Layer ({len(summary.visual_layer_issues)} issues)</h2>
{visual_rows if visual_rows else '<p class="no-issues">✅ No render layer issues found.</p>'}
</section>
</div>
</body>
</html>"""

    path.write_text(html, encoding="utf-8")
    return path


def _render_issue_rows(issues: List[Issue]) -> str:
    if not issues:
        return ""
    rows = []
    for i in issues:
        file_part = f'<span class="issue-file">{i.file}</span>' if i.file else ""
        line_part = f'<span class="issue-line">L{i.line}</span>' if i.line else ""
        ctx_part = f'<div class="issue-ctx">{i.context}</div>' if i.context else ""
        sug_part = f'<div class="issue-sug">💡 {i.suggestion}</div>' if i.suggestion else ""

        rows.append(
            f'<div class="issue sev-{i.severity.value}">'
            f'<div class="issue-header"><span class="badge badge-{i.severity.value}">{i.rule}</span>{file_part}{line_part}</div>'
            f'<div class="issue-msg">{i.message}</div>'
            f'{ctx_part}{sug_part}'
            f'</div>'
        )
    return "\n".join(rows)
