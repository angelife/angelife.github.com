# Version Audit Snapshot — v0.7.12（2026-05-30）

## 版本状态

| 追踪对象 | 版本 | 差距 |
|----------|------|------|
| Git HEAD | v0.7.12 | — |
| SITE_CHANGELOG.md | v0.6.33 | -26 minor |
| DAILY_WORK_LOG.md | v0.6.33 | -26 minor |
| changelog.yaml | v0.6.42 | -13 minor |
| PROJECT_STATUS.md | v0.6.33 待发布 | 完全过时 |

## 缺失版本明细

| 版本 | Commit | 变更 |
|------|--------|------|
| v0.6.34 | 966b9c9 | Fix workflow control map asset |
| v0.6.35 | a60e7d4 | Add AI bootstrap memory and project rules |
| v0.6.36 | 098182e | Update README as AI onboarding entry |
| v0.6.37 | c8ac7f8 | Add NVIDIA recovery SOP and YAML rules |
| v0.6.38 | 20fbe0e | Add NVIDIA repo mount runbook |
| v0.6.39 | ee56c4d | Test NVIDIA direct repo write |
| v0.6.40 | 986c697 | Publish zhen to sui article |
| v0.6.41 | 9cb4aca | vault: 2026-05-30 01:56:48 |
| v0.7.0 | f35e01f | Blogger 迁移 71 篇文章 |
| v0.7.1 | b4b20d4 | Hugo build 重建，修复 posts/ 404 |
| v0.7.2 | 111b3d7 | 正确 Hugo build，posts 同步 |
| v0.7.3 | 24881ef | 添加全部 5 个 favicon 文件 |
| v0.7.4–v0.7.11 | (无单独 commit msg) | Hugo build 产物同步 |

## 根因

v0.6.34 起 changelog 写入流程断裂，此后每个版本 tag 打完后都没有同步更新 4 个 changelog 文件。

## 关键 git 命令（用于重建）

```bash
# 快速查版本差距
git -C /repo log --oneline | head -30
git -C /repo tag -l | grep "^v0\." | sort -V | tail -20

# 查特定 tag 指向的 commit
git -C /repo rev-parse v0.7.12^{commit}

# 查 changelog 最新版（配合 git log 交叉验证）
grep -n "^## v0\." /repo/SITE_CHANGELOG.md | head -3
grep "version:" /repo/hugo-site/data/changelog.yaml | head -3
```

## 修复策略

5 文件同步更新（见 SKILL.md 场景 D），从 v0.6.34 补到 v0.7.12，共 13 个版本。commit message 统一写"changelog 补全"。