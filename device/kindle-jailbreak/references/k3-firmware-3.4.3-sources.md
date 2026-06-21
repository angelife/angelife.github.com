# K3 Firmware 3.4.3 — Download Sources (2026-06-09)

## Status

Amazon **no longer hosts** K3 3.4.3 firmware on their S3/CDN.
All known URLs return 404:
- `https://s3.amazonaws.com/G7G_FirmwareUpdates_WebLinks/update_kindle_343_k3w.bin` → 404
- `https://s3.amazonaws.com/firmware_updates/update_kindle_343_k3w.bin` → 404
- `https://kindle-firmware.s3.amazonaws.com/update_kindle_3.4.3.bin` → 404
- OVH public mirror (`mr-public/Firmware/`) → 404

## Known Still-Working Sources

### 1. MobileRead Forum (requires login)
- Thread: t=233932 ("K3 Firmware 3.4.3" or similar Kindle Keyboard firmware thread)
- Attachments typically require a registered MobileRead account
- User "NiLuJe" may have posted a link

### 2. Internet Archive (Wayback Machine)
Search CDX API:
```bash
curl -s "https://web.archive.org/cdx/search/cdx?url=*update_kindle*343*&output=json&limit=10"
```
Try IA direct download by guessing timestamps:
```bash
# If you find a timestamp from the CDX, use:
curl -L "https://web.archive.org/web/20220101000000/https://s3.amazonaws.com/G7G_FirmwareUpdates_WebLinks/update_kindle_343_k3w.bin" -o update_kindle_3.4.3.bin
```

### 3. kindlemodding.org
The site has a firmware archive at:
`https://kindlemodding.org/firmware/Legacy/` (tested 2026-06-09, no directory listing)
Try direct known filename:
`https://kindlemodding.org/firmware/Legacy/update_kindle_3.4.3.bin`

## Why This Matters

KUAL-KDK-1.0.azw2 (2025-04-19 build from NiLuJe) requires **firmware ≥ 3.4**.
On K3 FW 3.3, it reports:
```
The title you attempted to open requires a new version of Kindle software.
Please update your Kindle to the new software version.
```

This is **not** a jailbreak/certificate issue — it's a bundled minimum firmware check inside the KUAL AZW2.

## Alternative: Build KUAL Without FW Check

If you have kindletool and KUAL source, you can modify the minimum firmware check in the KUAL source and rebuild. This requires:
1. KindleTool (brew install kindletool on Mac)
2. KUAL Booklet source from https://github.com/NiLuJe/KUAL
3. Modify the android:minSdkVersion or equivalent check in the manifest
4. Re-sign with MKK/DevCerts certs

This approach has not been tested by this session (2026-06-09).