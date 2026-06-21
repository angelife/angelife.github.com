# INC-20260620-001: Docker 端 git push 覆盖远程导致网站回滚

## 概要

2026-06-20，木同学（NVIDIA Docker Hermes 实例）在 Docker 端 `angelife-clone/` 执行 git push 时，基于落后的本地 master（`1070b73`，Revert commit）覆盖了远程 master（`c79dd48`，6月19日正确版），导致 GitHub Pages 部署旧版，线上站点回滚。

## 时间线

| 时间 | 事件 |
|------|------|
| 6月19日 | /repo/ 中累计 ~14 个 commit（木工作报告、金工作日志、土工作总结、AI底层修仙 等） |
| 6月19日晚 | 可能通过 Docker 端执行了 git push 测试文章（`test: 验证文章发布完整链路`, `55d2f40`） |
| 6月19日晚 | 测试后被 revert（`Revert "test: 验证文章发布完整链路"`, `1070b73`），远程在此 |
| 6月20日 | 用户发现网站回滚到旧版本，只有 6月3日文章 |
| 6月20日 | 根因排查发现：Docker 端 angelife-clone/ HEAD = `1070b73`，/repo/ HEAD = `c79dd48` |
| 6月20日 | 有人（Mac 端或用户）force-push `c79dd48` 到远程，覆盖 `1070b73` |
| 6月20日 | GitHub Actions #167 部署正确版本，网站恢复 |

## 根因

- **直接原因**：Docker 端 `angelife-clone/` 仓库处于陈旧状态（落后 ~14 commits），git push 覆盖了远程 master
- **根本原因**：Docker 内有多个 git 仓库副本（`/repo/` Mac 绑定挂载 + `angelife-clone/` 独立 clone），无统一规范规定必须从哪个 push
- **次生原因**：SSH key 加载容器重启后丢失，Docker 端可能使用了未认证状态

## 关键证据

```bash
# 远程 master 被覆盖时的 SHA
1070b73a2b5aaab21b372b013b9b2049dedd491b  (Revert "test: 验证文章发布完整链路")

# 正确的远程 HEAD（6月19日版）
c79dd4885349de1c7d9963ae84ce70c0b77bee21  (fix: 2026-06-19 木同学工作报告)

# git fetch 确认 force-push 恢复记录
+ 1070b73...c79dd48 master -> origin/master (forced update)
```

## 修复操作

1. 查远程 HEAD → 发现被 revert commit 覆盖
2. 查 `/repo/` 本地 HEAD → `c79dd48` 正确版本仍在
3. 确认本地正确后 force-push `/repo/` 的 master 到远程
4. 等待 GitHub Actions 重新部署
5. 验证线上所有文章可访问

## 预防措施

1. **禁止 Docker 端 push**（已在 SKILL.md 中写入核心规则）
2. **push 前同步检查**（`git fetch origin master` + 比较本地/远程）
3. **权威路径声明**：`/repo/` 是唯一授权 push 来源
4. **root cause 快速诊断流程**（已在 SKILL.md 中写入）

## 相关 SHA

| SHA | 描述 |
|-----|------|
| `c79dd48` | 正确的远程 HEAD（6月19日完整版） |
| `1070b73` | 被覆盖时的远程 HEAD（Revert 旧版） |
| `55d2f40` | 测试文章 commit（被 revert 的目标） |
| `1dcf332` | 6月3日版（修复 checkout 残留） |
| `70a2632` | vault 自动同步 6月20日 |
| `f596312` | 木同学工作报告 6月19日 |
| `62a7959` | 金·工作日志 6月19日 |
| `8ed8665` | 土·工作总结 6月19日 |
