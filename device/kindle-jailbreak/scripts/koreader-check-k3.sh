#!/bin/bash
# koreader-check-k3.sh — Run on Mac to check K3 KOReader readiness
# Copy to Mac via: bridge_send.py --wait file_copy '{"source":"<path>","dest":"/tmp/koreader-check-k3.sh"}'
# Usage: bash /tmp/koreader-check-k3.sh

echo "=== MODEL CHECK ==="
ls -la /Volumes/Kindle/ 2>/dev/null || { echo "KINDLE_NOT_MOUNTED"; exit 1; }

echo "=== KOREADER ZIP CHECK ==="
find /opt/data/kindle/koreader -name "*koreader*legacy*" -type f 2>/dev/null | head -3
if [ -f /opt/data/kindle/koreader/koreader-kindle-legacy-v2026.03.zip ]; then
  echo "SHA256: $(sha256sum /opt/data/kindle/koreader/koreader-kindle-legacy-v2026.03.zip | cut -d' ' -f1)"
fi

echo "=== KUAL STATUS ==="
if [ -f "/Volumes/Kindle/documents/KUAL-KDK-1.0.azw2" ]; then
  echo "KUAL: PRESENT"
  # Check if KUAL might work: keystore and MKK check
  if [ -d "/Volumes/Kindle/developer/KUAL" ]; then
    echo "KUAL_BOOKLET: present"
  fi
  # Check if there's a .bin pending in root (means Update menu is active)
  BIN_COUNT=$(ls /Volumes/Kindle/*.bin 2>/dev/null | wc -l)
  if [ "$BIN_COUNT" -gt 0 ]; then
    echo "UPDATE_PENDING: yes ($BIN_COUNT bin files)"
  else
    echo "UPDATE_PENDING: no (root clean)"
  fi
  # Check disabled-updates
  if [ -d "/Volumes/Kindle/disabled-updates" ]; then
    echo "DISABLED_UPDATES: exists"
    ls /Volumes/Kindle/disabled-updates/*.bin* 2>/dev/null | head -5
  else
    echo "DISABLED_UPDATES: does not exist"
  fi
else
  echo "KUAL: MISSING from documents/"
fi

echo "=== K3 DEST PATH CHECK ==="
echo "Kindle documents/:"
ls -la /Volumes/Kindle/documents/ | head -10

echo "=== CHECK_K3_DONE ==="