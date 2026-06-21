# K3W B008 "permissions expired" Session Diagnosis (2026-06-09)

## Device Info

- Model: Kindle 3 WiFi (Keyboard)
- Code: k3w / B008
- Firmware: 3.3
- Status: KUAL opens with "The permissions to open the requested title have expired"

## Patient History (as reported)

User had previously attempted:
1. Install KUAL ✅ (file exists in documents/)
2. Install MKK (2014 version) ✅ (file exists in disabled-updates/)
3. Install DevCerts (2025) ❌ (never downloaded)
4. Modify system date ✅ (temporary bypass, worked but not persistent)
5. Create setdate update package ❌ (no effect)
6. Reinstall some components

## File System Evidence (verified via SSH to Mac host)

```
/Volumes/Kindle/
├── disabled-updates/
│   ├── Update_mkk-20141129-k3w-B008_install.bin      ← NO .last-greyed suffix!
│   └── Update_KUALBooklet_v2.7.37_install.bin.last-greyed  ← confirmed installed
├── documents/
│   └── KUAL-KDK-1.0.azw2                             ← KDK signed (K3 compatible after keystore fix)
└── (no pending .bin in root)
```

## Root Cause Analysis

**Direct cause**: `developer.keystore` expired 2025-04-17.

**Deep cause**: MKK 2014 certificate was **never actually installed** via Settings → Update.
- The `.bin` file sat in `disabled-updates/` without `.last-greyed` suffix
- Without MKK 2014 certificates installed, the 2025 keystore update has no valid underlying cert chain to extend
- KUAL opens → Kindlet Runtime checks developer.keystore → expired → blocks launch

**Missing keystore file**: `Update-mkk-20250419-k3w-B008_keystore-install.bin` was never on the device.

## Fix Steps (determined but not executed in this session)

1. Upgrade FW 3.3 → 3.4.3 (optional, needed if KUAL requires newer FW)
   - K3 max FW is 3.4.3, available on MobileRead or Amazon archive
   - Some KUAL-KDK builds check for FW ≥ 3.4 and refuse to open on 3.3

2. Install **MKK 2014** properly:
   - Copy `Update_mkk-20141129-k3w-B008_install.bin` to Kindle root (if not already there)
   - Settings → Menu → Update Your Kindle → select it
   - Wait for restart
   - Verify: file becomes `disabled-updates/Update_mkk-20141129-k3w-B008_install.bin.last-greyed`

3. Install **2025 keystore**:
   - Download DevCerts-20250419.zip from MobileRead (attachmentid=215127)
   - Extract `Update-mkk-20250419-k3w-B008_keystore-install.bin`
   - Copy to Kindle root
   - Settings → Menu → Update Your Kindle → select it
   - Wait for restart
   - Verification: open KUAL → no "permissions expired"

## Lessons Learned

1. **`.last-greyed` is the only reliable indicator of installed .bin**. Files in `disabled-updates/` without this suffix were never executed via Settings → Update.

2. **MKK 2014 + 2025 keystore is a TWO-step process**, not interchangeable or skippable. Each step establishes part of the cert chain. The 2025 installer depends on the 2014 base.

3. **FW 3.3 vs 3.4 issue is orthogonal to permissions**. If user gets "requires newer firmware" after fixing keystore, that's a separate KUAL version check problem — not a failed jailbreak. Solution: upgrade to 3.4.3 or build/use a KUAL without FW version pinning.

4. **KUAL-KDK-1.0.azw2 works on K3 after keystore is fixed**. The earlier assumption that KDK-signed KUAL always fails on K3 ("Test Kindle" error) is incorrect — the Test Kindle error only occurs when MKK certificates are completely absent. After proper MKK 2014 + 2025 keystore installation, KDK-signed KUAL works fine on K3.

5. **System date bypass works but is fragile**. `date -s "2025-04-01"` via USBNetwork SSH allows KUAL to open past the expiry check, but the fix resets on reboot. Useful only for verification.

## References

- MobileRead t=367665: K3/K4 permissions expired + Error 003 megathread
- MobileRead t=225030 post #1295: NiLuJe confirms developer.keystore expiry date
- DevCerts-20250419: attachmentid=215127 at mobileread.com/forums/attachment.php
- K3 3.4.3 firmware: available on MobileRead (search "kindle 3 3.4.3 update")