"""Markdown source file scanner — reads .md files and returns tokens."""

from pathlib import Path
from typing import List, Tuple
import markdown_it
from markdown_it.token import Token


def scan(path: str) -> List[Tuple[Path, List[Token]]]:
    """Scan content/**/*.md files and return (path, tokens) pairs."""
    base = Path(path)
    if not base.exists():
        raise FileNotFoundError(f"Path not found: {path}")

    content_dirs = [
        base / "content",
        base / "hugo-site" / "content",
        base / "hugo-site" / "content" / "posts",
    ]

    md_files: List[Path] = []

    for cd in content_dirs:
        if cd.exists():
            md_files.extend(sorted(cd.rglob("*.md")))

    # Fallback: if none of the expected paths work, try recursive
    if not md_files:
        md_files = sorted(base.rglob("*.md"))
        # exclude hidden, vendor, node_modules
        md_files = [
            f
            for f in md_files
            if not any(p.startswith(".") for p in f.parts)
            and "node_modules" not in f.parts
            and "venv" not in f.parts
        ]

    md = markdown_it.MarkdownIt()

    results = []
    for f in md_files[:500]:  # safety cap
        try:
            tokens = md.parse(f.read_text(encoding="utf-8"))
            results.append((f, tokens))
        except Exception as e:
            print(f"  [WARN] Failed to parse {f}: {e}")

    return results


def _is_frontmatter(token: Token) -> bool:
    """Check if token is YAML frontmatter fence."""
    return token.type == "fence" and getattr(token, "info", "").strip() in ("yaml", "yml", "")
