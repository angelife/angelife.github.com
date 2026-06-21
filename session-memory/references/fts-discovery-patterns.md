# FTS Discovery Query Patterns for Session Archiving

## What FTS5 indexes

FTS5 indexes only the `content` field of messages (user + assistant text). Tool call arguments, tool responses, and empty-string messages are **not indexed**. This means:

- A session where 95% of assistant messages are empty-string with tool calls attached will have very few FTS hits
- A session where user only says "继续" or "你好" is barely indexable
- Only substantive text content — code explanations, error descriptions, Chinese/English prose — appears in FTS

## Query patterns that work

| Pattern | Example | Match behavior |
|---------|---------|----------------|
| **Unique phrase from assistant prose** | `"API Rate Limit Error"` | High precision, single hit |
| **Unique user phrase** | `"请指定方向继续"` | Narrow, may match another session referencing this text |
| **Session ID fragment** | `034002` or `8af34e` | Matches if another session's assistant message *wrote* that fragment (rare) |
| **Topic keyword** | `kindle jailbreak SSH` | Broad recall, may return many sessions |
| **Chinese content** | `证书过期 越狱 KUAL` | Works well for Chinese sessions |
| **Command/function name** | `bridge_send.py bridge_client` | Matches if assistant described it in prose |
| **Topic + session-suffix compound** | `"API Rate Limit 087a74"` | **Anti-pollution pattern**: append the target session's hex suffix to the topic keyword. When a clean topic query gets parent-polluted, the suffix adds a unique token that disambiguates. The suffix alone rarely matches FTS, but combined with a topic keyword the target session DOES contain in its metadata/assistant-prose, the combined term can filter out the polluted result. **Discovered 2026-06-12**: rescued session `20260612_113341_087a74` after plain `"API Rate Limit Error"` returned a cron session summary that happened to reference it. |

## Query patterns that FAIL

| Pattern | Why it fails |
|---------|-------------|
| `195533` (session ID numeric fragment) | No content contains bare numeric IDs |
| `7a6a18` (session ID hex suffix) | No content contains hex suffixes |
| `14563` (message ID) | Message IDs are not stored in content |
| Empty query `""` | Falls back to browse mode (no FTS, no message_ids) |

## Detection heuristic for parent-session pollution

A discover result is **polluted** by a parent session if:

```
bookend_start[0].content ≈ "继续"   # short continuation prompt
AND match_message_id belongs to a different session_id
AND first bookend message references session_search() calls for a different session
```

**Fix**: Always verify that the returned session_id matches your target. If not, use the returned session_id (the one that actually has FTS content) and separately scroll the target session by direct session_id.

**Cross-validation trick (most reliable)**: Compare the `bookend_start[0].timestamp` and `preview` from browse mode against the bookend_start returned by discover. If the browse `preview` (e.g. "继续") and `started_at` don't match the discover `bookend_start` (e.g. first message is a session-memory skill load with a different timestamp), the discover result is polluted. Browse metadata is sourced from session rows, not FTS — it's never polluted. Use browse `started_at` as ground truth; if discover's first message timestamp differs by hours or days, discard that discover result.

## Fallback when FTS fails entirely

If all query attempts return no results or only polluted results for a session:

1. Accept browse-level metadata only (session_id, when, source, message_count, preview)
2. Create archive with `bookend_start: []`, `bookend_end: []`
3. Set `snippet` to a human-written description
4. The archiver creates messages.jsonl with 0 messages — still valid for bookkeeping

This is **not a failure** — some sessions are inherently non-indexable (CLI-driven, tool-call-heavy, compaction-heavy chains).