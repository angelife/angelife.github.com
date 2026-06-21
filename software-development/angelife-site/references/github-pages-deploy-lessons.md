# GitHub Pages Deployment — 事故归档

## 事故 1（v0.7.4）：favicon 全部 404

**日期**：2026-05-30
**版本**：v0.7.3 → v0.7.4
**严重性**：P1（影响浏览器标签图标显示，不影响内容访问）
**执行者**：NVIDIA (Docker Hermes)

### 症状

Hugo build 生成了 5 个 favicon 文件，全部 404：
- `favicon.ico`
- `favicon-16x16.png`
- `favicon-32x32.png`
- `apple-touch-icon.png`
- `safari-pinned-tab.svg`

文章页面 HTML 中引用的 favicon 路径全部正确，但 GitHub Pages 返回 404。

### 根因

```
hugo build → hugo-site/public/   ← Hugo 生成，非 git 追踪
                 ↓
    cp -a hugo-site/public/. ./  ← 仅本地同步，不进 git
                 ↓
    git commit (source files only)
                 ↓
    GitHub Pages → 不知道这些文件存在（public/ 未进 git）
```

**关键误解**：`cp -a hugo-site/public/. ./` 在本地可以跑 `hugo server` 预览，是因为 Hugo 直接读取 `public/`。但 GitHub Pages 不运行 Hugo，它直接从 git 仓库根目录服务文件。`public/` 从未 commit 到 git，所以 GitHub Pages 看不到任何 favicon 文件。

### 修复

v0.7.4：把 `hugo-site/static/` 中的 favicon 文件直接 commit 到 repo 根目录（绕过 Hugo build），确保 GitHub Pages 能直接服务这些文件。

### 教训

1. **GitHub Pages 不运行 Hugo** — 它是静态文件服务器，只服务 git 仓库里的文件
2. **`public/` 目录不在 git** — Hugo 每次 build 重新生成，不是源码
3. **Hugo build 的产物需要手动同步到 git** — `cp` 只在本地生效
4. **根目录静态资源要单独 commit** — Hugo 不会自动把 `static/` 的文件放进 git

## 事故 2（v0.7.20）：deploy-pages 报告 success 但 Pages 不更新

**日期**：2026-06-02
**版本**：v0.7.18 → v0.7.20
**严重性**：P0
**执行者**：NVIDIA (Docker Hermes)
**现象**：CI workflow 所有 jobs 报告 `conclusion: success`，但 live 站持续显示旧内容（栏目页只有 2 篇文章）。

### 根因

`actions/deploy-pages@v4` 成功的前提是 **GitHub Pages source 必须设置为"GitHub Actions"**。

路径：Settings → Pages → Source → 选择 **"GitHub Actions"**（不是"Deploy from a branch"）。

如果 Pages source 设为"Deploy from a branch"，则 deploy-pages action 会上传 artifact 到 Pages infrastructure，但 Pages 服务端不会切换到新 artifact（因为它不知道要听 Actions 的指挥）。此时 deploy job 仍报告 success，但 Pages 实际服务的是旧 artifact。

### 诊断命令

```bash
# 验证 live site 的 last-modified 时间（与 CI artifact 创建时间对比）
curl -sI "https://angelife.github.io/series/information-judgment/" | grep last-modified

# 对比 CI artifact 创建时间
curl -s "https://api.github.com/repos/angelife/angelife.github.com/actions/artifacts?per_page=5" \
  -H "Accept: application/vnd.github+json" | \
  python3 -c "import sys,json; [print(a['id'], a['created_at'][5:16]) for a in json.load(sys.stdin).get('artifacts',[])]"

# 确认 workflow run 的 deploy job 是否实际执行（不是 skipped）
curl -s "https://api.github.com/repos/angelife/angelife.github.com/actions/runs/{run_id}/jobs" \
  -H "Accept: application/vnd.github+json" | \
  python3 -c "import sys,json; [print(j['name'], j['status'], j.get('conclusion')) for j in json.load(sys.stdin).get('jobs',[])]"
```

## 事故 3（v0.7.20）：debug step 的 `set -e` 导致 build job 失败，deploy 被跳过

**日期**：2026-06-02
**严重性**：P1

### 根因

`set -e`（shell 默认行为）导致 `grep -c 'post-entry\|entry-hint'` 返回 0 时 exit code = 1，job 立即失败。后续 deploy job 被标记为 `skipped`。

### 最小修复

```yaml
# ❌ 错误：grep -c 返回 0 时 exit code 1，set -e 触发，job 失败
- name: Debug - verify build output
  run: |
    for d in public/series/*/; do
      count=$(grep -c 'post-entry\|entry-hint' "${d}index.html")
      echo "$(basename $d): $count"
    done

# ✅ 正确：|| true 防止非零退出码中断 job
- name: Debug - verify build output
  run: |
    for d in public/series/*/; do
      count=$(grep -c 'post-entry\|entry-hint' "${d}index.html" 2>/dev/null || true)
      echo "$(basename $d): $count"
    done
```

## 事故 4（v0.7.20）：中文文件名在 GitHub raw 返回 404（但文件在 git tree 中存在）

**日期**：2026-06-02
**严重性**：P2

### 现象

`git push` 报告成功，GitHub API 显示文件数量正确（46 个文件），但 `raw.githubusercontent.com/.../中文名.md` 返回 HTTP 404。ASCII 文件名（如 `test-marker.md`）工作正常。

### Workaround

commit 前把中文文件名转为 ASCII pinyin slug。

### 验证

```bash
# 检查 raw 是否可访问
curl -sI "https://raw.githubusercontent.com/angelife/angelife.github.com/{SHA}/path/中文名.md" | grep HTTP
# HTTP/2 404 → 切换为 ASCII 文件名
```

## 事故 5（v0.7.20）：`git add -A` 部分失败，commit 缺少 80 个文件

**日期**：2026-06-02
**严重性**：P1
**现象**：organize script 创建了 80 个新文件，`git add -A` 后 `git commit` 成功，但 `git ls-tree HEAD` 只有 6 个文件。本地 `ls` 显示 86 个文件。

### 根因

`git add -A` 遇到中文/空格文件名时可能在内部 pipe 处理中部分失败，但 commit 仍完成（只 commit 了成功 add 的文件）。没有错误提示，`git status` 显示 clean。

### 诊断

```bash
# 对比 git tree vs 本地文件数
git ls-tree -r HEAD -- hugo-site/content/series/information-judgment | grep "\.md$" | wc -l
ls hugo-site/content/series/information-judgment/*.md | wc -l
# 如果本地 > git tree → 有文件未进 commit

# 检查 untracked 文件
git status --short -uall | grep "series" | wc -l
```

### 教训

**`git add .` 或 `git add -A` 成功不等于所有文件都进了 commit。commit 后必须用 `git ls-tree -r HEAD -- {path} | wc -l` 验证文件数。**

## 事故 6（v0.7.20）：organize script 生成 `.md.md` 双重扩展名文件

**日期**：2026-06-02
**严重性**：P2

当 entry 名称本身以 `.md` 结尾时，拼接 `.md` 后缀产生 `xxx.md.md`。这些文件能 commit 但 Hugo 解析行为不确定。

### 修复

```bash
find hugo-site/content/series -name "*.md.md" -delete
find hugo-site/content/series -name "2012-02-09-2012-02-09*" -delete
```

## 正确的 Hugo + GitHub Pages 部署方式

### 方式 A（当前）：手动同步 public/ 到 repo 根目录

```bash
cd /repo/hugo-site && /opt/data/hugo        # build
cp -a hugo-site/public/. /repo/             # sync to repo root
# ⚠️ 然后必须 git add 那些不在 hugo-site/static/ 但 Hugo 生成的根目录文件
```

### 方式 B（推荐）：GitHub Actions + deploy-pages

1. 在 `.github/workflows/hugo.yml` 配置 Hugo Action
2. Settings → Pages → Source → 选择 **"GitHub Actions"**
3. `actions/deploy-pages@v4` 才能控制 Pages artifact 切换

## 诊断命令汇总

```bash
# 1. 检查文件是否在 git
git ls-files /path/to/file

# 2. 检查 Hugo 是否生成了该文件
ls hugo-site/public/path/to/file

# 3. 验证 commit 后 git tree 文件数
git ls-tree -r HEAD -- {path} | grep "\.md$" | wc -l

# 4. 验证 untracked 文件
git status --short -uall | grep "series"

# 5. 验证 live site 的 last-modified
curl -sI "https://angelife.github.io/series/information-judgment/" | grep last-modified

# 6. 验证 CI artifact
curl -s "https://api.github.com/repos/angelife/angelife.github.com/actions/artifacts?per_page=5" \
  -H "Accept: application/vnd.github+json" | \
  python3 -c "import sys,json; [print(a['id'], a['created_at'][5:16]) for a in json.load(sys.stdin).get('artifacts',[])]"
```

## 相关文件

- `hugo-site/static/favicon.ico` — 源文件（进了 git）
- `hugo-site/public/favicon.ico` — Hugo 生成（未进 git）
- `/repo/favicon.ico` — v0.7.4 手动同步版本（直接服务）