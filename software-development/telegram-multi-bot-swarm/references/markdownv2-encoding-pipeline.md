# Telegram MarkdownV2 Encoding Pipeline

Hermes Gateway converts standard Markdown to Telegram's MarkdownV2 format before sending messages. This reference documents the exact conversion steps, what gets escaped, and known rendering issues.

## Source File

`/opt/hermes/gateway/platforms/telegram.py` — the `format_message()` function (around line 5065-5200) and `_escape_mdv2()` helper (line 172).

## Escape Character Set

```python
# Line 169
_MDV2_ESCAPE_RE = re.compile(r'([_*\[\]()~`>#+\-=|{}.!\\])')
```

All these characters must be backslash-escaped when they appear outside a code span or fenced code block. Notably includes `|` (pipe), `-` (hyphen), `#` (hash), `>` (gt), and `.` (period).

## Conversion Steps (11 steps)

The `format_message()` function processes markdown in this order:

### Step 1: Protect fenced code blocks
- Identifies ```...``` blocks
- Escapes backslash `\\` and backtick `` ` `` inside the code body
- Wraps in placeholder to prevent further processing

### Step 2: Protect inline code
- Identifies `` `...` `` spans
- Escapes backslash `\\` inside (per MarkdownV2 spec)
- Wraps in placeholder

### Step 3: Convert markdown links
- Pattern: `[display](url)`
- Escapes MarkdownV2 chars in display text via `_escape_mdv2()`
- Escapes only `)` and `\\` inside URL
- Wraps in placeholder

### Step 4: Convert headers `## Title` → `*Title*`
- Removes inner `**bold**` markers
- Escapes content, wraps in `*...*` (MarkdownV2 bold-equivalent)

### Step 5: Convert bold `**text**` → `*text*`
- Escapes content, wraps in single `*...*`

### Step 6: Convert italic `*text*` → `_text_`
- Single asterisk only (not `**`)
- Escapes content, wraps in `_..._`
- Won't match across newlines (preserves bullet lists)

### Step 7: Convert strikethrough `~~text~~` → `~text~`
- Escapes content, wraps in `~...~`

### Step 8: Convert spoiler `||text||`
- Escapes text content, preserves `||...||` markers
- Wraps in placeholder

### Step 9: Convert blockquotes `> text`
- Recognizes `>`, `>>`, `>>>` variants and expandable `**>` prefix
- Escapes content, preserves prefix

### Step 10: Escape remaining special characters
- Applies `_escape_mdv2()` to the **entire remaining text**
- This is where `|` in pipe tables gets destroyed: `| col |` → `\| col \|`
- ALL characters matched by `_MDV2_ESCAPE_RE` get backslash-prefixed

### Step 11: Restore placeholders
- Reverses the placeholder substitutions in reverse insertion order

## The Pipe Table Problem

**Input markdown:**
```markdown
| Item | Status |
|------|--------|
| Gateway | ✅ Running |
```

**After Steps 1-9**: pipe table syntax is unrecognized — it passes through as plain text.

**After Step 10**: `_escape_mdv2()` escapes every `|`, `-`, `✅`:
```
\| Item \| Status \|
\|\-\-\-\-\-\|\-\-\-\-\-\|
\| Gateway \| ✅ Running \|
```

**Telegram receives**: `\|` characters, not table syntax. Telegram MarkdownV2 does NOT have native table support, so these escaped pipes render as literal `\|` or cause parse failures.

## Why Web Telegram Differs from Mobile

| Issue | Mobile | Web |
|-------|--------|-----|
| Escaped `\|` chars | Renders as `\|` | May show blank |
| Unclosed `*text` | Tolerates silently | Refuses to render |
| Message >4096 chars | Truncates | Fails silently |
| Multiple `_escape_mdv2` runs | Renders escaped chars | May break all formatting |

## Detection

To detect if a message has pipe tables that will break:

```bash
grep -n '|' /path/to/message.md
# If pipes appear outside code blocks, they will be escaped
```

## Suggested Fix (if modifying gateway code)

Add a pipe-table protector before Step 10, similar to code-block protection:

```python
# Before Step 10, protect pipe tables
def _protect_table(m):
    """Preserve pipe table rows from escaping."""
    row = m.group(0)
    # Escape the row but restore pipes
    escaped = _escape_mdv2(row)
    # Restore pipe characters that were escaped
    escaped = escaped.replace('\\|', '|')
    return _ph(escaped)

text = re.sub(r'^\|.+\|$', _protect_table, text, flags=re.MULTILINE)
```

This preserves the table structure while still escaping other special characters inside cells.
