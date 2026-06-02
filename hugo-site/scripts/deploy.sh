#!/usr/bin/env bash
# deploy.sh — 雲端觸發腳本（由 GitHub Actions 調用，禁止本地執行）
# 用法：在本地 commit 並 git push，CI 自動觸發
set -euo pipefail

echo "=== Angelife 網站雲端構建觸發 ==="
echo "觸發時間: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "觸發分支: $(git rev-parse --abbrev-ref HEAD)"
echo "觸發 SHA: $(git rev-parse HEAD)"

# Hugo 版本
echo "Hugo 版本: $(hugo version)"

# 清理
rm -rf public resources .hugo_build_lock

# 構建
echo "=== 開始 Hugo 構建 ==="
hugo --gc --minify --cleanDestinationDir

# 驗收
echo "=== 構建驗收 ==="
echo "總 HTML 檔案: $(find public -name '*.html' | wc -l)"
echo "Series taxonomy 頁面:"
for tax in information-judgment chan-shi-lu confucian-framework ai-bu-yin yi-notes; do
  if [ -f "public/series/$tax/index.html" ]; then
    size=$(wc -c < "public/series/$tax/index.html")
    posts=$(grep -c 'post-entry' "public/series/$tax/index.html" || echo 0)
    echo "  $tax: ${size}B, post-entry=$posts"
  else
    echo "  $tax: MISSING"
  fi
done

echo "Categories:"
if [ -d "public/categories" ]; then
  echo "  日课: $([ -f 'public/categories/日课/index.html' ] && wc -c < 'public/categories/日课/index.html' || echo 'MISSING')B"
fi

echo "=== 觸發 artifact 上傳 ==="