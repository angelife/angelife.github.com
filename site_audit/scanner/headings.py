"""Heading hierarchy and spacing checks."""

from pathlib import Path
from typing import List
from markdown_it.token import Token

from ..models.issue import Issue, Severity


def check_heading_levels(path: Path, tokens: List[Token]) -> List[Issue]:
    """Detect skipped heading levels (e.g. H1 -> H3 without H2)."""
    issues: List[Issue] = []
    prev_level = 0
    prev_line = 0

    for i, token in enumerate(tokens):
        if token.type == "heading_open":
            level = int(token.tag[1])  # h1 -> 1, h2 -> 2, etc.
            line = token.map[0] + 1 if token.map else 0

            if prev_level > 0 and level > prev_level + 1:
                issues.append(
                    Issue(
                        rule="markdown/heading-level",
                        severity=Severity.MAJOR,
                        message=f"Heading level skipped: H{prev_level} → H{level}",
                        file=str(path),
                        line=line,
                        context=f"... H{prev_level} (line ~{prev_line}) → H{level} (line {line}) ...",
                        suggestion=f"Insert an H{prev_level + 1} heading between H{prev_level} and H{level}, or adjust the hierarchy."
                    )
                )

            prev_level = level
            prev_line = line
        elif token.type == "hr":
            # Thematic break resets heading continuity — headings
            # separated by --- are in different sections
            prev_level = 0

    return issues


def check_heading_spacing(path: Path, tokens: List[Token], content: str | None = None) -> List[Issue]:
    """Detect missing blank lines before/after headings.

    Hugo markdown requires blank lines around headings for correct rendering
    in some themes. Works on token maps or raw content lines.
    """
    issues: List[Issue] = []
    lines = content.splitlines() if content else path.read_text(encoding="utf-8").splitlines()

    for i, token in enumerate(tokens):
        if token.type == "heading_open" and token.map:
            heading_line = token.map[0]

            # Check blank line before heading
            if heading_line > 0:
                line_before = lines[heading_line - 1] if heading_line - 1 < len(lines) else ""
                if line_before.strip() and not line_before.startswith("#"):
                    issues.append(
                        Issue(
                            rule="markdown/heading-spacing",
                            severity=Severity.MINOR,
                            message="Missing blank line before heading",
                            file=str(path),
                            line=heading_line + 1,
                            context=f"... {lines[heading_line - 1].strip()[:40]} ...\n{lines[heading_line].strip()[:40]}",
                            suggestion="Add a blank line before the heading for proper markdown rendering."
                        )
                    )

            # Check blank line after heading (look at next block)
            if i + 1 < len(tokens):
                next_token = tokens[i + 1]
                # The content after heading_open is heading_close + inline heading text
                # The real next block is 2 tokens after
                if i + 2 < len(tokens):
                    content_token = tokens[i + 2]
                    if content_token.map and token.map and content_token.map[0] > token.map[1]:
                        gap = content_token.map[0] - token.map[1]
                        if gap == 0:
                            # heading text and next content on consecutive lines
                            issues.append(
                                Issue(
                                    rule="markdown/heading-spacing",
                                    severity=Severity.MINOR,
                                    message="Missing blank line after heading",
                                    file=str(path),
                                    line=token.map[1] + 1,
                                    suggestion="Add a blank line after the heading."
                                )
                            )

    return issues
