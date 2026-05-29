# Release 脚本安全规则（v0.6.41 事故后固化）

> 本文档记录 v0.6.40 中文路径 git add bug 的根因与修复规则。
> 所有涉及 git / rsync 的脚本修改必须遵守本文档。
> 新增 RULE-021 至 RULE-025。

---

## v0.6.40 事故复盘

**现象**：
- Hugo 构建成功
- rsync 成功
- tools/angelife-release 在"精准 git add"阶段失败
- 报错：`fatal: pathspec ... did not match any files`

**根因**：
- 脚本使用 `git diff --name-only` 获取改动文件列表
- 输出通过 pipe 传递给 `while read` 循环
- 中文路径在 pipe 传递过程中被 shell 转义或截断
- 传递给 `git add` 的是错误路径，导致路径不匹配

**教训**：
- 普通 git 命令输出不适合程序化解析
- 必须使用 NUL-safe 方式处理文件名

---

## 中文路径 git add bug 根因

普通 `git diff --name-only` 或 `git status --short` 输出：

```
file1.txt
中文文件.md
another.txt
```

这些输出通过 pipe 传递时，shell 会按换行符切割。
**如果路径中包含空格、引号、反斜杠等字符，切割会失败。**

更危险的是：某些终端或 Telegram 界面会对输出做转义，
导致 `git add "中文文件.md"` 实际收到的是 `"\344\270\255\346\226\207\345\255\270"` 这类八进制转义序列。

---

## 必须使用的 NUL-safe 方式

### ✅ 正确：git diff --name-only -z + read -d ''

```bash
# 获取已修改文件（已跟踪）
git diff --name-only -z | while IFS= read -r -d '' file; do
    [[ "$file" != "_incoming/"* && "$file" != ".reasonix/"* ]] && git add -- "$file"
done

# 获取 untracked 文件
git ls-files -z --others --exclude-standard | while IFS= read -r -d '' file; do
    [[ "$file" != "_incoming/"* && "$file" != ".reasonix/"* ]] && git add -- "$file"
done
```

### ❌ 错误：禁止使用

```bash
# 错误：普通 git status 输出
git status --short | awk '{print $2}' | while read file; do ... done

# 错误：git diff --name-only（无 NUL）
git diff --name-only | while read file; do ... done

# 错误：git status --porcelain（无 -z）
git status --porcelain | awk '{print $2}' | while read file; do ... done
```

---

## rsync 输出必须静默或限流

### ❌ 错误：rsync -av 刷屏

### ✅ 正确：rsync 静默模式

```bash
RSYNC_LOG="/tmp/angelife-release-rsync-${VERSION}.log"
rsync -a --delete hugo-site/public/ "$TARGET_DIR/" > "$RSYNC_LOG" 2>&1
```

---

## 闪退后恢复 SOP

当 release 脚本在 Telegram 或远控界面中途闪退时：

### 步骤一：状态检查（必须先做）

```bash
# 检查 Hugo 是否构建完成
ls -la hugo-site/public/

# 检查 rsync 是否完成
git status --short

# 检查是否有残留的 staged 文件
git diff --cached --name-only

# 检查上一次 commit 是否成功
git log -1 --oneline
```

### 步骤二：根据状态决定

| 状态 | 操作 |
|------|------|
| Hugo 未构建 | 先运行 Hugo 构建 |
| rsync 未执行 | 先运行 rsync |
| 已有 staged 但未 commit | 检查 staged 文件是否正确，然后 commit |
| 已有 commit 但未 tag | 检查 commit 内容，然后 tag |
| 已有 tag 但未 push | 检查 tag 内容，然后 push |
| Everything up-to-date | 说明上次已发布成功，不需要重跑 |

### 步骤三：禁止盲目重跑

**如果不确定状态，先 `git status` 查清楚，不要直接重跑 release。**

---

## tag already exists 规则

当 `git tag` 遇到已存在的 tag 时：

| 情况 | 处理 |
|------|------|
| 相同版本号，内容一致 | `Everything up-to-date`，不需要重打 tag |
| 相同版本号，内容不同 | 先 `git push` 现有 tag，再决定是否 force tag |
| 不同版本号 | 正常创建，不冲突 |

---

## Everything up-to-date 规则

当 `git push` 返回 "Everything up-to-date" 时：
**含义**：远程已有这个 commit，不需要再 push。不需要重跑任何操作。

---

## 新增安全规则（RULE-021 至 RULE-025）

### RULE-021：发布前必须检查 .git 目录存在

```bash
# 发布前必须验证 .git 目录存在
if [ ! -d ".git" ]; then
    log_error "当前目录不是 Git 仓库：$(pwd)"
    exit 1
fi
```

### RULE-022：发布前必须检查 hugo-site 目录存在

```bash
# 发布前必须验证 Hugo 源站存在
if [ ! -d "hugo-site" ]; then
    log_error "hugo-site 目录不存在：$(pwd)"
    exit 1
fi
```

### RULE-023：发布前必须检查 bind mount 路径安全

```bash
# 检查当前目录是否为仓库根目录（防止 bind mount 指向错误路径）
EXPECTED_DIRS=(
    "/Users/macos/angelife.github.com"
    "/repo"
)
CURRENT_DIR="$(pwd)"
IS_VALID=false
for d in "${EXPECTED_DIRS[@]}"; do
    if [ "$CURRENT_DIR" = "$d" ]; then
        IS_VALID=true
        break
    fi
done
if [ "$IS_VALID" = false ]; then
    log_error "当前目录不是预期仓库路径：$CURRENT_DIR"
    exit 1
fi
```

### RULE-024：发布前显示 dry-run 提示

```bash
# 显示本轮将执行的操作（不实际执行）
log_info "=== DRY-RUN 预览 ==="
log_info "Hugo 源站: $PWD/hugo-site"
log_info "rsync 目标: $PWD/"
log_info "版本号: $VERSION"
log_info "Commit: $COMMIT_MESSAGE"
log_info "===================="
```

### RULE-025：发布前提示创建 repo 快照

```bash
# 发布前提示创建快照（可选但推荐）
if [ -d ".git" ]; then
    SNAPSHOT_MSG="建议发布前创建快照：git bundle create /tmp/angelife-$(date +%Y%m%d).bundle --all"
    log_warn "$SNAPSHOT_MSG"
fi
```

---

## 禁止事项

- ❌ 不得使用 `git add .`
- ❌ 不得 `cat git status 输出 | while read` 解析路径
- ❌ 不得 `git diff --name-only | while read` 解析路径
- ❌ 不得 `rsync -av`（刷屏）
- ❌ 闪退后不得盲目重跑 release
- ❌ 不得忽略 "Everything up-to-date" 继续 push
- ❌ 禁止在非仓库目录执行发布

---

## 责任链

- 事故发现：v0.6.40 发布过程
- 根因分析：NVIDIA
- 规则制定：剑妈 + NVIDIA
- 脚本修复：NVIDIA
- bash -n 检查：本地 Mac
- 规则验证：人类用户 + 剑妈

---

*本文件由 NVIDIA 于 2026-05-29 生成，对应 v0.6.41。*