#!/usr/bin/env bash
set -eu

# ---------- 配置 ----------
VIMWIKI_ROOT="./"
HUGO_SITE="./hugo-site"
THEME_REPO="https://github.com/adityatelange/hugo-PaperMod.git"
STATIC_DIRS=("images")
OBS_BUCKET="obs://angelife-site/"

declare -A CATEGORY_MAP=(
    ["blog"]="blog"
    ["changshi"]="knowledge"
    ["sikao"]="thoughts"
    ["diary"]="diary"
    ["fangfa"]="methods"
    ["fenxi"]="analysis"
    ["jingyan"]="experience"
)

# ---------- 检查依赖 ----------
command -v hugo >/dev/null 2>&1 || { echo "请先安装 hugo"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "请先安装 python3"; exit 1; }
command -v obsutil >/dev/null 2>&1 || echo "未检测到 obsutil，部署到 OBS 需手动上传"

# ---------- 创建 Hugo site ----------
[ ! -d "$HUGO_SITE" ] && hugo new site "$HUGO_SITE"
[ ! -d "$HUGO_SITE/themes/PaperMod" ] && git -C "$HUGO_SITE" submodule add "$THEME_REPO" "themes/PaperMod"

# ---------- 遍历全站 MD + HTML ----------
find "$VIMWIKI_ROOT" -type f \( -name "*.md" -o -name "*.html" \) | while read -r f; do
    dir=$(dirname "$f")
    fname=$(basename "$f")
    slug=$(echo "${fname%.*}" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g')

    # topdir 安全访问 CATEGORY_MAP
    topdir=$(echo "$dir" | cut -d/ -f1)
    if [ "${CATEGORY_MAP[$topdir]+_}" ]; then
        mapped_dir="${CATEGORY_MAP[$topdir]}"
    else
        mapped_dir="$topdir"
    fi

    destdir="$HUGO_SITE/content/$mapped_dir/$slug"
    mkdir -p "$destdir"
    dest="$destdir/index.md"

    ext="${fname##*.}"

    if [ "$ext" = "md" ]; then
        python3 - "$f" "$slug" "$mapped_dir" "$fname" > "$dest" <<'PY'
import sys, re
from datetime import datetime

fpath=sys.argv[1]
slug=sys.argv[2]
category=sys.argv[3]
fname=sys.argv[4]

text=open(fpath,encoding='utf-8').read()

# 日期
m = re.search(r'(\d{4}-\d{2}-\d{2})', fname)
date = m.group(1) if m else datetime.today().strftime('%Y-%m-%d')

# front-matter
fm=f"---\ntitle: {slug}\ndate: {date}\ndraft: false\ncategories: [{category}]\n---\n\n"

# 内部 [[Page]] 或 [[Page#block]]
def repl_link(m):
    parts = m.group(1).split('#')
    page = parts[0].lower().replace(' ','-')
    anchor = f"#{parts[1]}" if len(parts)>1 else ""
    return f"/{category}/{page}/{anchor}"
text = re.sub(r'\[\[(.*?)\]\]', repl_link, text)

# 块引用 ^block-ref
text = re.sub(r'^\^(\S+)', r'<div id="\1"></div>', text, flags=re.MULTILINE)

# 图片 ![[image.png]] 或 [[image.png]]
def repl_img(m):
    name = m.group(1)
    return f"/images/{name}"
text = re.sub(r'!\[\[(.*?)\]\]', repl_img, text)
text = re.sub(r'\[\[(.*?)\.(png|jpg|jpeg|gif)\]\]', repl_img, text)

sys.stdout.write(fm + text)
PY
    else
        title=$(basename "$fname" .html)
        python3 - "$f" "$mapped_dir" "$title" > "$dest" <<'PY'
import sys, re

fpath=sys.argv[1]
category=sys.argv[2]
title=sys.argv[3]

text=open(fpath,encoding='utf-8').read()

# HTML 内部链接 href="xxx.html" -> /category/xxx/
def repl_link(m):
    href=m.group(1)
    if href.startswith("http://") or href.startswith("https://"):
        return f'href="{href}"'
    new_href = href.replace(".html","/")
    return f'href="{new_href}"'
text = re.sub(r'href="([^"]+\.html)"', repl_link, text)

# 块引用 ^block-ref
text = re.sub(r'^\^(\S+)', r'<div id="\1"></div>', text, flags=re.MULTILINE)

fm=f"""---
title: "{title}"
draft: false
categories: [{category}]
---

"""
sys.stdout.write(fm + text)
PY
    fi

    echo "转换: $f -> $dest"
done

# ---------- section _index.md ----------
for top in "${!CATEGORY_MAP[@]}"; do
    mapped_dir="${CATEGORY_MAP[$top]}"
    index="$HUGO_SITE/content/$mapped_dir/_index.md"
    [ ! -f "$index" ] && cat > "$index" <<EOF
---
title: $mapped_dir
---

# $mapped_dir

导航:
{{ range .Pages }}
- [{{ .Title }}]({{ .RelPermalink }})
{{ end }}
EOF
done

# ---------- 首页 _index.md ----------
cat > "$HUGO_SITE/content/_index.md" <<EOF
---
title: Home
---

# 欢迎来到 Angelife Notes

## 导航
{{ range \$key, \$value := .Site.Sections }}
- [{{ \$value.Title }}]({{ \$value.Permalink }})
{{ end }}

## 最新文章
{{ range first 5 .Site.RegularPages }}
- [{{ .Title }}]({{ .RelPermalink }})
{{ end }}
EOF

# ---------- 静态资源 ----------
for d in "${STATIC_DIRS[@]}"; do
    [ -d "$VIMWIKI_ROOT/$d" ] && rsync -a "$VIMWIKI_ROOT/$d/" "$HUGO_SITE/static/$d/"
done

# ---------- config.toml ----------
[ ! -f "$HUGO_SITE/config.toml" ] && cat > "$HUGO_SITE/config.toml" <<'CFG'
baseURL = "https://angelife-site.obs.cn-east-3.myhuaweicloud.com/"
languageCode = "zh-cn"
title = "Angelife Notes"
theme = "PaperMod"
[params]
  defaultTheme = "auto"
CFG

# ---------- 构建 Hugo ----------
cd "$HUGO_SITE"
hugo

# ---------- 上传 OBS（可选） ----------
command -v obsutil >/dev/null 2>&1 && obsutil cp -r ./public "$OBS_BUCKET" --delete || echo "未安装 obsutil，请手动上传 public/"

echo "整站迁移完成！MD + HTML + 内部链接 + 块引用全部处理完毕。"
