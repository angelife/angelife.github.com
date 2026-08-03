"""Chinese/English spacing detection (pangu-like)."""

import re
from pathlib import Path
from typing import List

from ..models.issue import Issue, Severity


# Patterns that should NOT trigger spacing warnings
_IGNORE_PATTERNS = [
    re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"),  # IPv4
    re.compile(r"[0-9a-fA-F:]+:[0-9a-fA-F:]+"),  # IPv6 (partial)
    re.compile(r"HTTP\d+", re.IGNORECASE),  # HTTP2, HTTP3
    re.compile(r"HTTPS?", re.IGNORECASE),
    re.compile(r"[A-Za-z]+[0-9]+"),  # Version strings like Hugo60
    re.compile(r"\d+x\d+"),  # Resolutions: 1920x1080
    re.compile(r"[A-Za-z]'[A-Za-z]"),  # Contractions: don't, it's
    re.compile(r"_\w+"),  # Underscore prefixes: _config
    re.compile(r"\w+_\w+"),  # Snake case: my_var
]

# Chinese char range
CJK_RE = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]")

# Pattern: Chinese followed by ASCII letter/digit without space
CN_EN_RE = re.compile(r"([\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff])([A-Za-z0-9])")
# Pattern: ASCII letter/digit followed by Chinese without space
EN_CN_RE = re.compile(r"([A-Za-z0-9])([\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff])")


def _is_ignored(line: str, start: int, end: int) -> bool:
    """Check if a range [start, end) overlaps any ignored pattern."""
    for pat in _IGNORE_PATTERNS:
        for m in pat.finditer(line):
            if m.start() < end and m.end() > start:
                return True
    return False


def check_spacing(path: Path, content: str) -> List[Issue]:
    """Detect missing spaces between Chinese and ASCII characters."""
    issues: List[Issue] = []
    lines = content.splitlines()

    for lineno, line in enumerate(lines, 1):
        # Check CN→EN missing space
        for m in CN_EN_RE.finditer(line):
            if _is_ignored(line, m.start(), m.end()):
                continue
            matched = m.group(0)
            suggestion = m.group(1) + " " + m.group(2)
            issues.append(
                Issue(
                    rule="markdown/cjk-spacing",
                    severity=Severity.MINOR,
                    message=f"Missing space between Chinese and ASCII: '{matched}'",
                    file=str(path),
                    line=lineno,
                    context=f"... {line[max(0, m.start()-10):m.end()+10].strip()} ...",
                    suggestion=f"Replace '{matched}' with '{suggestion}'."
                )
            )

        # Check EN→CN missing space
        for m in EN_CN_RE.finditer(line):
            if _is_ignored(line, m.start(), m.end()):
                continue
            matched = m.group(0)
            suggestion = m.group(1) + " " + m.group(2)
            issues.append(
                Issue(
                    rule="markdown/cjk-spacing",
                    severity=Severity.MINOR,
                    message=f"Missing space between ASCII and Chinese: '{matched}'",
                    file=str(path),
                    line=lineno,
                    context=f"... {line[max(0, m.start()-10):m.end()+10].strip()} ...",
                    suggestion=f"Replace '{matched}' with '{suggestion}'."
                )
            )

    return issues
