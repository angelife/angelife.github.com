#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SITE_DIR="$ROOT_DIR/hugo-site"
PUBLIC_DIR="$SITE_DIR/public"
HUGO_BIN="${HUGO_BIN:-/usr/local/bin/hugo}"

"$HUGO_BIN" --source "$SITE_DIR" --destination "$PUBLIC_DIR" --cleanDestinationDir --minify

rsync -a --delete \
  --exclude='.git/' \
  --exclude='.github/' \
  --exclude='hugo-site/' \
  --exclude='.gitignore' \
  --exclude='.gitmodules' \
  --exclude='README.md' \
  --exclude='publish.sh' \
  "$PUBLIC_DIR/" "$ROOT_DIR/"

echo "Published Hugo output to repository root."
