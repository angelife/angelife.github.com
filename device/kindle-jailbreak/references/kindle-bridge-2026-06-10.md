# Kindle Bridge — 2026-06-10

## Mount Verification

- `/Volumes/Kindle` exists ✅
- 3.0 GiB free (3.1 GiB total, 4.1 MiB used)
- Filesystem: FAT32
- Writable: ✅ (touch + rm succeeded)
- KOReader installed (`koreader/` directory)
- `system/version` not found (cannot auto-detect model, but K3 MKK 2014 confirmed from prior session)

## kindle_cp Implementation

Two-step delivery:
1. `scp` from Docker to Mac temp: `/tmp/kindle_bridge_<basename>_<timestamp>`
2. SSH: `mkdir -p $(dirname '/Volumes/Kindle/<dest>')` → `mv` from temp → `ls -la` verify

## Test Results

```bash
# Create test file
echo "KINDLE_BRIDGE_OK" > /tmp/kindle_bridge_test.txt

# Send via bridge
python3 /opt/data/bridge/bridge_send.py --wait kindle_cp \
  '{"source":"/tmp/kindle_bridge_test.txt","dest":"documents/kindle_bridge_test.txt"}'

# Result: mv succeeded, content verified by cat
```

## Known FAT32 Quirk

`mv: /Volumes/Kindle/documents/kindle_bridge_test.txt: set owner/group (was: 501/0): Operation not permitted`

This is a FAT32 characteristic — the filesystem doesn't support POSIX ownership. The file is written correctly; stderr is advisory only. bridge_client.py still reports `status: "ok"` and `exit_code: 0` because `mv` itself succeeds.

## Documents Already Present

```
/Volumes/Kindle/documents/  (not empty — has pre-existing ebooks)
```

## Safety Features Verified

- ✅ Missing source → `{"error": "missing source path"}`
- ✅ Kindle not mounted → `{"error": "Kindle not mounted at /Volumes/Kindle"}`
- ✅ scp timeout → `{"error": "scp timeout"}`
- ✅ scp failure → `{"error": "scp failed: ..."}`
- ✅ Temp file cleanup on all failure paths