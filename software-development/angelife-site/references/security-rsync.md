# 安全 rsync 规则与漏洞记录

本文档记录安全 rsync 的正确操作方式和已发生的漏洞事故，供后续维护参考。

---

## 漏洞事故（v0.6.32）

**时间**：2026-05-28  
**事故**：执行 `rsync -av hugo-site/public/ ./`（裸 rsync，无排除项）后，.gitignore、.gitmodules、publish.sh、tools/ 被删除。  
**原因**：rsync --delete 模式下，源目录不存在的文件会被目标端删除；裸 rsync 未指定排除项，导致治理文件被误删。  
**恢复**：执行 `git restore .gitignore .gitmodules publish.sh tools/` 恢复。

---

## 安全 rsync 必须排除的项

执行 `rsync -av hugo-site/public/ ./`（将 Hugo 构建产物同步到根目录）时，**必须**使用以下排除项：

```
--exclude='.git/' \
--exclude='.gitignore' \
--exclude='.gitmodules' \
--exclude='hugo-site/' \
--exclude='_incoming/' \
--exclude='docs/' \
--exclude='tools/' \
--exclude='publish.sh' \
--exclude='0847745cb78663855a3a1732c9c6a130.txt' \
--exclude='PROJECT_STATUS.md' \
--exclude='BUILD_HANDOFF.md' \
--exclude='AI_WORK_RULES.md' \
--exclude='HERMES_COST_RULES.md' \
--exclude='AI_EXECUTION_AGENTS.md' \
--exclude='SITE_STYLE_GUIDE.md' \
--exclude='SITE_CHANGELOG.md' \
--exclude='DAILY_WORK_LOG.md' \
--exclude='README.md' \
--exclude='LICENSE' \
--exclude='.DS_Store' \
```

**禁止项**：

1. **禁止裸 rsync**：`rsync -av hugo-site/public/ ./` 不带排除项，严格禁止。
2. **禁止未带完整排除项的 rsync --delete**：必须同时使用排除项和 --delete 才安全。
3. **禁止用 rsync 同步治理文件**：治理文件必须由 git 管理，不能由 rsync 管理。

**正确命令**：

```bash
rsync -av --delete \
  --exclude='.git/' \
  --exclude='.gitignore' \
  --exclude='.gitmodules' \
  --exclude='hugo-site/' \
  --exclude='_incoming/' \
  --exclude='docs/' \
  --exclude='tools/' \
  --exclude='publish.sh' \
  --exclude='0847745cb78663855a3a1732c9c6a130.txt' \
  --exclude='PROJECT_STATUS.md' \
  --exclude='BUILD_HANDOFF.md' \
  --exclude='AI_WORK_RULES.md' \
  --exclude='HERMES_COST_RULES.md' \
  --exclude='AI_EXECUTION_AGENTS.md' \
  --exclude='SITE_STYLE_GUIDE.md' \
  --exclude='SITE_CHANGELOG.md' \
  --exclude='DAILY_WORK_LOG.md' \
  --exclude='README.md' \
  --exclude='LICENSE' \
  --exclude='.DS_Store' \
  hugo-site/public/ ./
```

---

## 发布脚本

正式发布必须使用 `tools/angelife-release`，不得裸跑 rsync。  
如 `tools/angelife-release` 不存在，必须手动构造完整的 rsync 命令（见上方正确命令），不得省略任何排除项。

---

## 验证命令

发布后验证治理文件未被误删：

```bash
git status --short | grep -E 'publish.sh|tools/.gitignore|.gitmodules'
```

预期：无输出（文件未被删除，未被 rsync 覆盖）