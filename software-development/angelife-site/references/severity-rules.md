# Severity Rules — angelife Incident Classification

> Complete version at `/repo/_private/INCIDENT_REPORTS/SEVERITY_RULES.md`

## Severity Levels

| Level | Name | Definition | Response |
|-------|------|------------|----------|
| P0 | Fatal | Permanent data loss, site fully down, critical security | Immediate |
| P1 | Severe | Major feature broken, process blocked, data at risk | Within 4 hours |
| P2 | General | Minor issue, no mainline impact, can fix later | Within 24 hours |

## ID Format

`INC-YYYYMMDD-XXX` — e.g., `INC-20260529-001`

- `YYYYMMDD`: date discovered
- `XXX`: sequence number 001–999

## Public vs Internal Boundary

| Content | Internal Report | Public Summary |
|---------|----------------|----------------|
| Full timeline | ✅ | ❌ |
| Exact commands/paths | ✅ | ❌ |
| Tokens/keys/env | ❌ | ❌ |
| Docker internals | ✅ | ❌ |
| Root cause (principles only) | ✅ | ✅ |
| New rules (principle level) | ✅ | ✅ |
| Post-mortem conclusions | ✅ | ✅ |
| Individual blame | ✅ | ❌ |

Rule: `INCIDENT_REPORTS_PUBLIC/` = sanitized summaries that CAN go into version history. `_private/INCIDENT_REPORTS/` = internal only, must be in `.gitignore`.

## Response Timelines

**P0**: Stop all publishing → 5 min confirm scope → 30 min plan → restore → ≤24h post-mortem归档
**P1**: ≤4h scope confirm → ≤24h restore → ≤72h archive
**P2**: Log it → fix in next release

## Archive Checklist

Every P0/P1 archive must include:
- [ ] Incident ID (INC-YYYYMMDD-NNN)
- [ ] Full timeline (minute-by-minute)
- [ ] Direct cause + root cause
- [ ] Recovery steps
- [ ] Loss assessment
- [ ] New rules (each maps to one exposed problem)
- [ ] Follow-up tasks (owner + status)
- [ ] Three lessons learned
- [ ] Report author + approver

## Keyword Index

| Keyword | Related Incident |
|---------|----------------|
| release | INC-20260529-001 |
| rsync | INC-20260529-001 |
| Docker bind mount | INC-20260529-001 |
| git add (Chinese path) | INC-20260529-001 |
| repo wipe | INC-20260529-001 |
| Telegram gateway | INC-20260529-001 |