# Bridge Hardening Session — 2026-06-10

## Tasks Completed

1. **SSH PATH fix** — `ssh_run()` wraps every command chain with `export PATH=/usr/local/bin:/opt/homebrew/bin:$PATH &&`. Verified: `which hugo` → `/usr/local/bin/hugo`, `which rsync` → `/usr/bin/rsync`.

2. **file_copy root cause validated** — Previous "file_copy broken" was a **test file not existing** issue, not code. The `execute_file_copy()` handler reads `params["source"]` and `params["dest"]` correctly. scp runs Docker→Mac; if the file doesn't exist in Docker, scp → exit 255. Always `ls -la` first before file_copy.

3. **bridge_send.py --wait added** — New flag that polls outbox at 1s intervals, returns result JSON directly, default timeout 30s. Exit codes: 0=ok, 2=timeout, 3=bridge error. Compatible with all existing call patterns.

4. **kindle_cp mount check fixed** — The OLD pattern `test -d || echo NOT_MOUNTED && mkdir && mv` was BROKEN: shell `||`/`&&` precedence means `echo NOT_MOUNTED` appeared but `mv` still ran. Fixed to use TWO independent SSH calls: first a strict `if [ ! -d /Volumes/Kindle ]; then echo NOT_MOUNTED && exit 1; fi` check, then only proceed if exit 0.

5. **Pressure test** — 10/10 consecutive shell tasks: 100% success, avg 6.42s, max 6.52s, no loss, no duplicates.

## Files Changed

- `/opt/data/bridge/bridge_client.py` — PATH export in ssh_run(), independent kindle_cp mount check
- `/opt/data/bridge/bridge_send.py` — --wait flag added, complete rewrite (was 40 lines, now ~70)
- No changes to bridge_check.py

## Bridge Client State

- PID: verified running after restart
- Log: `/opt/data/bridge/bridge_client.log`
- Poll: 2s (hardcoded POLL_INTERVAL)
- All handlers: shell, file_copy, kindle_cp, hugo_build, rsync, token_inject — working

## Kindles at Last Known State

- K3 B008 WiFi
- `/Volumes/Kindle` mounted, 3.0 GiB free
- KUAL-KDK-1.0.azw2 in documents/
- koreader/ directory is **EMPTY** (1 node, dir only)
- No MKK installed, no developer.keystore
- Kindle FW version unknown (not visible via USB)
- `one_person_company.epub` (600KB) verified on Kindle via Mac `cp`