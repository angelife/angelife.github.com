#!/usr/bin/env bash
# angelife 木同学发稿通道 (土·发布助手)
# 用法: ./tools/publish-mu.sh "<commit-message>"
#
# 木同学在容器内写好的 .md 经 bind mount 已同步到 Mac
# 土在 Mac 上运行此脚本完成构建+发布
set -euo pipefail

cd "$(dirname "$0")/.."
REPO_ROOT=$(pwd)

echo "=== 检查木同学是否有新文章 ==="
# 查找木同学的最新文章 (content/posts 中最近修改的 .md)
LATEST_POST=$(find "$REPO_ROOT/hugo-site/content/posts" -name "*.md" -newer "$REPO_ROOT/.git/HEAD" -type f 2>/dev/null | head -5)
if [ -n "$LATEST_POST" ]; then
    echo "检测到新文章:"
    for f in $LATEST_POST; do
        echo "  $(basename $(dirname $f))/$(basename $f)"
    done
fi

echo ""
echo "=== Hugo 清洁构建 ==="
hugo --gc --minify --cleanDestinationDir -s hugo-site

echo ""
echo "=== git 状态 ==="
git status --short | grep -v '^?? _incoming/' | grep -v '^?? .reasonix/' || echo "  (无修改)"

echo ""
echo "=== git commit ==="
COMMIT_MSG="${1:-"posts: 木同学文章发布 - $(date +%Y-%m-%d)"}"
git add -A
git commit -m "$COMMIT_MSG"
COMMIT_HASH=$(git rev-parse HEAD)
echo "  commit: $COMMIT_HASH"

echo ""
echo "=== git push ==="
git push origin master
echo "  ✅ push 完成"

echo ""
echo "=== 部署中... GitHub Actions 将自动部署 ==="
echo "  预计 1-2 分钟后访问 https://angelife.github.io 可见"
