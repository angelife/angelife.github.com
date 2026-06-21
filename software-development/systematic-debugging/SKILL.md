---
name: systematic-debugging
description: "4-phase root cause debugging: understand bugs before fixing."
version: 1.3.0
author: Hermes Agent (adapted from obra/superpowers)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [debugging, troubleshooting, problem-solving, root-cause, investigation]
    related_skills: [test-driven-development, writing-plans, subagent-driven-development]
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**
- Issue seems simple (simple bugs have root causes too)
- You're in a hurry (rushing guarantees rework)
- Someone wants it fixed NOW (systematic is faster than thrashing)

## The Four Phases

You MUST complete each phase before proceeding to the next.

---

## Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

### 1. Read Error Messages Carefully

- Don't skip past errors or warnings
- They often contain the exact solution
- Read stack traces completely
- Note line numbers, file paths, error codes

**Action:** Use `read_file` on the relevant source files. Use `search_files` to find the error string in the codebase.

### 2. Reproduce Consistently

- Can you trigger it reliably?
- What are the exact steps?
- Does it happen every time?
- If not reproducible → gather more data, don't guess

**Action:** Use the `terminal` tool to run the failing test or trigger the bug:

```bash
# Run specific failing test
pytest tests/test_module.py::test_name -v

# Run with verbose output
pytest tests/test_module.py -v --tb=long
```

### 3. Check Recent Changes

- What changed that could cause this?
- Git diff, recent commits
- New dependencies, config changes

**Action:**

```bash
# Recent commits
git log --oneline -10

# Uncommitted changes
git diff

# Changes in specific file
git log -p --follow src/problematic_file.py | head -100
```

### 4. Gather Evidence in Multi-Component Systems

**WHEN system has multiple components (API → service → database, CI → build → deploy):**

**BEFORE proposing fixes, add diagnostic instrumentation:**

For EACH component boundary:
- Log what data enters the component
- Log what data exits the component
- Verify environment/config propagation
- Check state at each layer

Run once to gather evidence showing WHERE it breaks.
THEN analyze evidence to identify the failing component.
THEN investigate that specific component.

### 5. Trace Data Flow

**WHEN error is deep in the call stack:**

- Where does the bad value originate?
- What called this function with the bad value?
- Keep tracing upstream until you find the source
- Fix at the source, not at the symptom

**Action:** Use `search_files` to trace references:

```python
# Find where the function is called
search_files("function_name(", path="src/", file_glob="*.py")

# Find where the variable is set
search_files("variable_name\\s*=", path="src/", file_glob="*.py")
```

### Phase 1 Completion Checklist

- [ ] Error messages fully read and understood
- [ ] Issue reproduced consistently
- [ ] Recent changes identified and reviewed
- [ ] Evidence gathered (logs, state, data flow)
- [ ] Problem isolated to specific component/code
- [ ] Root cause hypothesis formed

**STOP:** Do not proceed to Phase 2 until you understand WHY it's happening.

---

## Phase 2: Pattern Analysis

**Find the pattern before fixing:**

### 1. Find Working Examples

- Locate similar working code in the same codebase
- What works that's similar to what's broken?

**Action:** Use `search_files` to find comparable patterns:

```python
search_files("similar_pattern", path="src/", file_glob="*.py")
```

### 2. Compare Against References

- If implementing a pattern, read the reference implementation COMPLETELY
- Don't skim — read every line
- Understand the pattern fully before applying

### 3. Identify Differences

- What's different between working and broken?
- List every difference, however small
- Don't assume "that can't matter"

### 4. Understand Dependencies

- What other components does this need?
- What settings, config, environment?
- What assumptions does it make?

---

## Phase 3: Hypothesis and Testing

**Scientific method:**

### 1. Form a Single Hypothesis

- State clearly: "I think X is the root cause because Y"
- Write it down
- Be specific, not vague

### 2. Test Minimally

- Make the SMALLEST possible change to test the hypothesis
- One variable at a time
- Don't fix multiple things at once

### 3. Verify Before Continuing

- Did it work? → Phase 4
- Didn't work? → Form NEW hypothesis
- DON'T add more fixes on top

### 4. When You Don't Know

- Say "I don't understand X"
- Don't pretend to know
- Ask the user for help
- Research more

---

## Phase 4: Implementation

**Fix the root cause, not the symptom:**

### 1. Create Failing Test Case

- Simplest possible reproduction
- Automated test if possible
- MUST have before fixing
- Use the `test-driven-development` skill

### 2. Implement Single Fix

- Address the root cause identified
- ONE change at a time
- No "while I'm here" improvements
- No bundled refactoring

### 3. Verify Fix

```bash
# Run the specific regression test
pytest tests/test_module.py::test_regression -v

# Run full suite — no regressions
pytest tests/ -q
```

### 4. If Fix Doesn't Work — The Rule of Three

- **STOP.**
- Count: How many fixes have you tried?
- If < 3: Return to Phase 1, re-analyze with new information
- **If ≥ 3: STOP and question the architecture (step 5 below)**
- DON'T attempt Fix #4 without architectural discussion

### 5. If 3+ Fixes Failed: Question Architecture

**Pattern indicating an architectural problem:**
- Each fix reveals new shared state/coupling in a different place
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere

**STOP and question fundamentals:**
- Is this pattern fundamentally sound?
- Are we "sticking with it through sheer inertia"?
- Should we refactor the architecture vs. continue fixing symptoms?

**Discuss with the user before attempting more fixes.**

This is NOT a failed hypothesis — this is a wrong architecture.

---

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals a new problem in a different place**

**ALL of these mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the architecture (Phase 4 step 5).

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question the pattern, don't fix again. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence, trace data flow | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare, identify differences | Know what's different |
| **3. Hypothesis** | Form theory, test minimally, one variable at a time | Confirmed or new hypothesis |
| **4. Implementation** | Create regression test, fix root cause, verify | Bug resolved, all tests pass |

## Terminal Output Masking — Critical Pitfall

**The terminal tool masks secrets in output.** This is NOT a filesystem issue — the file on disk has the full value, but what you see in the terminal output is censored.

### The Masking Problem

When you read a file containing an API key or credential:

```
# What terminal output shows:
    api_key: sk-7iw...H6rl         # ← only 13 visible chars, has ...

# What the actual file contains:
    api_key: sk-7iwhS4S4BtyTd5...  # ← 50 chars, no literal dots
```

Three things happen:
- Keys are replaced with `***` or truncated with `...` in displayed output
- Length can be different (13 visible vs 50 actual)
- The `...` is display-only — **not in the file**

### How This Bites You

- You read a config file via `terminal` with `cat`/`grep`/`head` → see truncated key
- You diagnose "key is truncated/corrupted in file" → wrong conclusion
- You try to verify your fix by grepping again → still see truncated version → think fix didn't work
- The file was correct all along; the display was lying

### Correct Verification Methods

**DO NOT** trust the displayed value of any field that looks like `sk-`, `ak-`, `key`, `secret`, `token`, `auth`, `password`, or `<any>...<any>`.

**DO use one of these:**

```python
# Method 1: Python len() + first/last chars
import re
with open('config.yaml') as f:
    content = f.read()
m = re.search(r'api_key:\s*(\S+)', content)
k = m.group(1)
print(f'Key length: {len(k)} — if < 40, investigate')
print(f'Starts: {k[:7]}, Ends: {k[-4:]}')

# Method 2: Hex dump (definitive proof)
# bash: xxd /path/to/file | grep -A2 'api_key'
# python: ' '.join(f'{b:02x}' for b in k.encode())
hex_bytes = ' '.join(f'{b:02x}' for b in k.encode())
print(f'Hex: {hex_bytes}')
# If no 2e2e2e (... in hex) appears, the dots are display-only

# Method 3: Direct comparison with env var
import os
real = os.environ.get('SOME_API_KEY', '')
match = k == real
print(f'Keys match: {match}')
```

### Examples of Deceptive Display

| You see in terminal | Likely reality |
|--------------------|---------------|
| `key = sk-7iw...H6rl` (13 chars) | 50-char real key, masking activated |
| `API_KEY=***` | Valid key exists, masked |
| `PASSWORD=s3cret...` | Not truncated — display artifact |

### When to Suspect Masking

- Any string containing `...` in the middle (check hex for `2e2e2e`)
- Any value shown as `***`
- A credential/key that looks too short to be real
- `len()` in Python shows much longer than visible output

### Public Endpoint Trap

Some API endpoints return 200 without auth. `/v1/models` is a common example — it's a **public discovery endpoint**. Getting 200 from it proves nothing about key validity.

**Always test against an authenticated endpoint** (e.g. `/v1/images/generations`, `/v1/chat/completions`) to verify a key actually works. A 401 on the real endpoint with 200 on the models endpoint means the key is invalid — the models endpoint just doesn't check auth.

```python
# WRONG — models endpoint may be public
import urllib.request
req = urllib.request.Request('https://api.example.com/v1/models',
    headers={'Authorization': 'Bearer ' + key})
resp = urllib.request.urlopen(req, timeout=10)  # may succeed even with bad key

# RIGHT — test against an authenticated endpoint
payload = json.dumps({"model": "some-model", "prompt": "test"}).encode()
req = urllib.request.Request('https://api.example.com/v1/images/generations',
    data=payload,
    headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
# 401 on this endpoint = key is genuinely invalid
```

## Hermes Agent Integration

### Investigation Tools

Use these Hermes tools during Phase 1:

- **`search_files`** — Find error strings, trace function calls, locate patterns
- **`read_file`** — Read source code with line numbers for precise analysis
- **`terminal`** — Run tests, check git history, reproduce bugs
- **`web_search`/`web_extract`** — Research error messages, library docs

### With delegate_task

For complex multi-component debugging, dispatch investigation subagents:

```python
delegate_task(
    goal="Investigate why [specific test/behavior] fails",
    context="""
    Follow systematic-debugging skill:
    1. Read the error message carefully
    2. Reproduce the issue
    3. Trace the data flow to find root cause
    4. Report findings — do NOT fix yet

    Error: [paste full error]
    File: [path to failing code]
    Test command: [exact command]
    """,
    toolsets=['terminal', 'file']
)
```

### With test-driven-development

When fixing bugs:
1. Write a test that reproduces the bug (RED)
2. Debug systematically to find root cause
3. Fix the root cause (GREEN)
4. The test proves the fix and prevents regression

---

## Containerized Environment Debugging

When debugging targets that are **physically connected to the host machine**, the containerized Hermes environment has specific access constraints that must be detected early.

### Environment Detection Checklist (Phase 1, Step 0)

**Run this BEFORE attempting any device-level operation:**

```bash
# USB access (Android devices, Kindles, etc.)
ls /dev/bus/usb/ 2>/dev/null && echo "USB_AVAILABLE" || echo "USB_NOT_ACCESSIBLE"

# ADB binary presence
which adb 2>/dev/null || echo "ADB_NOT_IN_CONTAINER"

# Docker environment
grep -q docker /proc/1/cgroup 2>/dev/null && echo "IN_DOCKER" || echo "NOT_DOCKER"
ls /dev/bus/usb/ 2>/dev/null | head -3 || echo "NO_USB_BUS"

# Host directory mounts
ls /opt/data/home/Library/Android/sdk/platform-tools/adb 2>/dev/null && echo "SDK_MOUNTED" || echo "SDK_NOT_MOUNTED"
```

**STOP if target device is USB-connected and no USB bus is visible.** Do not attempt ADB/shell operations from inside the container — they will fail silently or with "device not found". Instead:

### When USB is Host-Only (BLOCKED state)

**Rule:** If the device is USB-tethered to the Mac and the container has no USB bus access, **you cannot run diagnostic commands directly.**

**Required action:** Ask the user to run diagnostic commands in Mac Terminal and paste the output.

**Standard pattern for Android/Kindle diagnostics:**

```bash
# Step 1: User runs in Mac Terminal
brew install android-platform-tools  # if adb not present
adb devices
adb shell getprop ro.product.model
adb shell getprop ro.build.version.release
adb shell dumpsys usb
adb logcat -d -v time -t 200 | grep -E "ERROR|WARN|Exception|ANR|Crash|FATAL"
adb shell dumpsys battery

# Step 2: Paste output here for analysis
```

**For Kindle specifically:**
```bash
system_profiler SPUSBDataType | grep -i kindle
diskutil list | grep -i kindle
```

### When WiFi ADB is Available

If the device is on the same network and has ADB over WiFi enabled, you CAN connect from the container:

```bash
# From inside container
adb connect <device-ip>:5555
adb devices
```

This requires the device to have been set up for wireless debugging first (one-time USB pairing + `adb tcpip 5555`).

### Docker Run Parameters for USB Passthrough (Host Action Required)

If USB passthrough is needed and the user agrees to modify Docker startup:

```bash
# Mac Terminal — stop current container
docker stop <container_name>

# Restart with USB access
docker run --device=/dev/bus/usb:/dev/bus/usb \
  --privileged \
  -v /opt/data:/opt/data \
  -v ~/.hermes:/root/.hermes \
  <other-args> \
  <image-name>
```

**You cannot change Docker run parameters from inside the container.** This requires the user to restart the container from Mac Terminal.

## Real-World Impact

From debugging sessions:
- Systematic approach: 15-30 minutes to fix
- Random fixes approach: 2-3 hours of thrashing
- First-time fix rate: 95% vs 40%
- New bugs introduced: Near zero vs common

**No shortcuts. No guessing. Systematic always wins.**

---

## CI/CD Multi-Environment Debugging

When local build succeeds but live/deployed site fails, standard debugging process still applies — but the **investigation order shifts** to prioritize environment differences.

### The Core Problem Pattern

Local build: correct output.
CI/deployed site: incorrect output (fewer items, wrong content, stale pages).

**Critical assumption to discard immediately:** "If Hugo version matches and source files match, CI must produce the same output." CI has additional constraints that can silently corrupt output.

### Investigation Sequence for CI Divergence

**Step 1: Verify workflow file filesystem presence.**

```bash
# Check if workflow file is visible in working directory (not just git tree)
ls -la .github/workflows/hugo.yml

# A file that exists in git tree but NOT in filesystem:
# git show HEAD:.github/workflows/hugo.yml  # works (git tree)
# ls .github/workflows/                      # empty (filesystem missing)
# → CI may use cached/fallback workflow or fail silently
```

**Step 2: Trace CI execution timestamp vs commit timestamp.**

```bash
# Get commit timestamp
git log -1 --format='%ct' HEAD

# Check live site Last-Modified header (approximate CI completion)
curl -sI https://example.com/ | grep last-modified
```

If CI "rebuild" timestamp is newer than commit push time → CI did run.
If content still wrong → CI output is wrong, check artifact.

**Step 3: Add CI debug instrumentation BEFORE assuming version mismatch.**

For Hugo specifically:
- Add `hugo --verbose` output to CI steps
- Log post counts at CI build time: `find public/posts -name 'index.html' | wc -l`
- Log taxonomy page content: `grep -c 'class="post-entry"' public/series/*/index.html`
- Commit debug step first, push, observe CI output, THEN analyze.

**Step 4: Check CI artifact path correctness.**

Many CI/deploy misconfigs cause the **old artifact** to be served:
- GitHub Pages source branch set to `gh-pages` but artifact uploaded to wrong path
- Pages CDN has long TTL cache on taxonomy pages
- `actions/upload-pages-artifact` path doesn't match `actions/deploy-pages` expectation

### Common CI Traps

**`grep -c` + `set -e` = silent deploy skip:**
```bash
set -e
count=$(grep -c "pattern" file)
# If count=0, exit code 1 (grep returns 1 when no matches)
# set -e → job exits before deploy step
```
Fix: Use `grep -c` with `|| true` or check `set -e` placement carefully.

**`.github/workflows/` in git tree but not filesystem:**
```bash
# This creates a file only in git tree:
git show HEAD:.github/workflows/hugo.yml > .github/workflows/hugo.yml
# But if the directory .github/ itself was never created by checkout,
# ls .github/workflows/ shows nothing even though git knows about the file
```
Fix: Always `mkdir -p .github/workflows` before writing workflow files to ensure filesystem and git tree stay in sync.

---

## Hugo-Specific Debugging

### Taxonomy / Section Disappearing in CI

**Symptom:** Local build shows 42 posts in taxonomy; live site shows 2 (or 0).

**Common causes (check in order):**

1. **`mainSections` missing the target section.**
   ```toml
   # hugo.toml
   mainSections = ["columns", "posts"]  # missing "series"
   ```
   PaperMod theme filters posts to only sections listed in `mainSections`. Taxonomy pages for unlisted sections appear empty even though content exists.

2. **Chinese vs English taxonomy values in frontmatter.**
   ```yaml
   # Posts have:
   series: ["信息判断"]
   # Taxonomy page generates: /information-judgment/
   # → sitemap, metadata, and taxonomy links all point to English slug
   # → Chinese value doesn't match → zero results
   ```
   Fix: Normalize all taxonomy values to English slugs (same as URL) in frontmatter.

3. **Duplicate content files with conflicting frontmatter.**
   An `organize` script may have created `.md.md` duplicates (filename like `2024-01-01-title.md.md`) or placed flat files in `content/series/` alongside `content/posts/` subdirectories. The duplicates have different frontmatter (English vs Chinese taxonomy values), causing Hugo to index both but with conflicting taxonomy associations.
   - `.md.md` files: Delete — these are organize script artifacts with same content as clean-named files.
   - Flat file duplicates: Determine canonical source; delete the other.

### Verifying Hugo Build Locally

```bash
# Full clean build
hugo --cleanDestinationDir --minify

# Count generated taxonomy pages
find public/series -name 'index.html' -not -path '*/page/*' | wc -l

# Check specific taxonomy section
grep -c 'class="post-entry"' public/series/information-judgment/index.html
find public/series/information-judgment -name 'index.html' | wc -l

# Count paginator pages
find public/series/information-judgment/page -name 'index.html' | wc -l
```

Run local build **after every frontmatter/config change** before pushing. A local build that passes with `hugo --verbose` gives you a known-good baseline to compare against CI output.

### Hugo Version Pinning in CI

Specify exact version in workflow file:
```yaml
- name: Setup Hugo
  uses: peaceiris/actions-hugo@v3
  with:
    hugo-version: '0.147.4'
    hugo-extended: true
```
Mismatches between local `hugo version` and CI `hugo version` can cause subtle output differences.
