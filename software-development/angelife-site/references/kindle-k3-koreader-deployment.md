# Kindle K3 KOReader Deployment — Key Lessons

> 2026-06-11, multi-session recovery operation for Kindle Keyboard 3 (B008, FW 3.3)

## Problem

K3 KOReader deployment stalled due to:
1. KUAL "This device is not registered as a Test Kindle" error
2. DevCerts expired in 2025-04-17
3. KUAL v2.7.37 requires FW >= 3.4 (K3 was on FW 3.3)
4. Root cause: Kindle may not be jailbroken at all

## Architecture

```
Docker Hermes --SSH--> Mac (macos@host.docker.internal) --USB--> Kindle (/Volumes/Kindle/)
```

## Key Findings

### File Deployment Chain
1. KOReader zip (koreader-kindle-legacy-v2026.03.zip, ~39MB) → 1021 files extracted
2. Missing 6 files on first deployment: launchpad/*, extensions/koreader/* (KUAL menu extensions)
3. File-level verification essential: compare zip contents vs deployed files

### MKK + DevCerts
- `kindle-mkk-20141129-r18833.tar.xz` → `Update_mkk-20141129-k3w-B008_install.bin` (90KB)
- `DevCerts-20250419-KeyStore.zip` → `Update-mkk-20250419-k3w-B008_keystore-install.bin` (10KB)
- MKK must be installed FIRST (establishes OTA trust), then keystore
- WiFi MUST be off during MKK install

### Source Finding Notes
- NiLuJe's snapshot thread on MobileRead (t=225030) is the primary source
- DevCerts-20250419 was found at attachmentid=215127 (postcount~1295, page 87)
- OVH public cloud mirror has the old MKK 2014 tar.xz
- GitHub API rate limits (unauthenticated) are restrictive; use `?per_page=10`

### File Verification
```bash
# Compare zip vs deployed
python3 -c "
import zipfile, subprocess
z = zipfile.ZipFile('koreader-kindl-legacy-...zip')
zip_files = set(z.namelist())
result = subprocess.run(['ssh', ..., 'find /Volumes/Kindle/koreader -type f'], ...)
# ... parse and diff
"
```