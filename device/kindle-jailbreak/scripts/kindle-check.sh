#!/bin/bash
# kindle-check.sh
# Kindle K3 status diagnostic script
# Usage: scp to Mac, then: bash /tmp/kindle_check.sh
# Output: 9-point Kindle status check for bridge diagnostics

echo "=== KINDLE USB ROOT ==="
ls -la /Volumes/Kindle/

echo "=== CHECK KOReader PACKAGES ==="
find /Volumes/Kindle -maxdepth 2 -type f \( -iname "*koreader*" -o -iname "*.zip" \) 2>/dev/null

echo "=== CHECK KOReader DIR ==="
ls -la /Volumes/Kindle/koreader 2>/dev/null || echo "NO KOREADER DIR"

echo "=== DEVELOPER / KUAL ==="
ls -la /Volumes/Kindle/developer/ 2>/dev/null
ls -la /Volumes/Kindle/developer/KUAL/ 2>/dev/null || echo "NO KUAL DIR"
ls -la /Volumes/Kindle/documents/KUAL-KDK-*.azw2 2>/dev/null || echo "NO KUAL BOOKLET"

echo "=== MKK / KEYSTORE ==="
find /Volumes/Kindle -maxdepth 3 -type f \( -iname "*mkk*" -o -iname "*keystore*" -o -iname "*cert*" \) 2>/dev/null || echo "NO MKK OR KEYSTORE"

echo "=== UPDATE MENU CHECK ==="
ls /Volumes/Kindle/update_*.bin 2>/dev/null && echo "UPDATE_MENU_AVAILABLE=YES" || echo "UPDATE_MENU_AVAILABLE=NO"

echo "=== DISK USAGE ==="
df -h /Volumes/Kindle/ 2>/dev/null

echo "=== SYSTEM DIR ==="
ls -la /Volumes/Kindle/system/ 2>/dev/null | head -10

echo "=== DOCUMENTS ==="
ls -la /Volumes/Kindle/documents/ 2>/dev/null

echo "CHECK_DONE"