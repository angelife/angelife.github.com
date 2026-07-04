#!/bin/bash
# Memory audit — observation mode
# Reads current memory entries, applies three rules, writes audit log.
# Run daily. In observation mode (default), only reports — does NOT delete.

MEMORY_LOG="${HOME}/.hermes/memory/audit-$(date +%Y%m%d).log"
exec > "$MEMORY_LOG" 2>&1

echo "=== Memory Audit $(date -u '+%Y-%m-%dT%H:%M:%SZ') ==="
echo

# ------------------------------------------------------------------
# Rule 1: entries > 4 days without being referenced in session_search
# Rule 2: contradictory entries (hard to automate, note for manual)
# Rule 3: capacity > 70% → flag for manual compression
# ------------------------------------------------------------------

echo "=== Current capacity estimate ==="
hermes --dump-memory 2>/dev/null || echo "no memory dump tool available"

echo
echo "=== Entries flagged for review (observation mode — no deletions) ==="
echo "(placeholder: needs access to memory metadata via hermes cli or python)"

echo
echo "=== Next step ==="
echo "Review manual: cat $MEMORY_LOG"
