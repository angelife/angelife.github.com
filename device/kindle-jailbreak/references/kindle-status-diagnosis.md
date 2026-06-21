# Kindle Status Diagnosis

## 9-Point Status Check

Check these via the Mac Execution Bridge (`kindle_cp` + `shell`):

```
1. Model identification
   → USB Product ID 0x0004  = Kindle 3 Keyboard (K3)
   → USB Vendor ID 0x1949   = Lab126 (Amazon)
   → Serial prefix B008     = K3 WiFi

2. Firmware version
   → NOT readable via USB storage (Amazon hides it)
   → Must read on device: Home → Menu → Settings → Menu → Device Info

3. Jailbreak status
   → Check /Volumes/Kindle/koreader/ exists
   → Check /Volumes/Kindle/developer/KUAL/ exists

4. KUAL (Kindle Unified Application Launcher)
   → /Volumes/Kindle/developer/KUAL/ (directory with metadata/temp/work)
   → /Volumes/Kindle/documents/KUAL-KDK-*.azw2 (booklet registration file)

5. MKK (Mobileread Kindlet Kit)
   → find /Volumes/Kindle -maxdepth 3 -type f ( -iname *mkk* -o -iname *keystore* )
   → No .jar files or extensions/ directory → MKK not installed

6. developer.keystore
   → /Volumes/Kindle/developer/keystore/developer.keystore
   → If only developer/KUAL/ exists (no keystore dir) → MKK route unavailable

7. Update Your Kindle menu
   → Visible ONLY if update_*.bin exists in Kindle root (/Volumes/Kindle/)
   → Not visible by default → need to copy update bin first before menu appears

8. Root file list
   → ls -la /Volumes/Kindle/
   → Key dirs: system/, documents/, developer/, koreader/, audible/, music/

9. Documents list
   → ls -la /Volumes/Kindle/documents/
   → Existing files + kindle_cp targets

## K3 Specifics

- Architecture: ARM (Freescale i.MX3x)
- Storage: 3.28 GB FAT32 via USB
- FW versions: 3.0.x → 3.4.x (3.4.1, 3.4.3 are common upgrade targets)
- KOReader: works on K3, separate build per FW version
- KUAL: KDK-1.0 required for K3
- MKK: needed for 3.4.x jailbreak, requires developer.keystore
- "Update Your Kindle" in Settings menu appears only when update_*.bin is in root

## Upgrade Decision Framework

**Upgrade only when:**
1. Current FW has a known bug affecting reading
2. KOReader version is too old for needed features
3. User explicitly wants 3.4.x features
4. AND user accepts re-jailbreak + re-KOReader cost

**Upgrade prerequisites:**
1. Know current FW version (on-device check)
2. Download matching jailbreak tool (3.4.x requires MKK route)
3. Prepare developer.keystore
4. Backup KOReader config
5. Have re-jailbreak process ready before upgrading

**When NOT to upgrade:**
- KOReader already works fine
- No developer.keystore (MKK route blocked)
- No pressing need for newer FW features
- Risk of bricking (K3 upgrades are notoriously fragile)