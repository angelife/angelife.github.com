# NVIDIA 主库挂载规划

> 本文档记录未来"主库挂载版 NVIDIA"的规划。
> **本轮不执行任何挂载操作。**

---

## 当前状态

| 项目 | 状态 |
|------|------|
| NVIDIA / Hermes 可用 | ✅ |
| Telegram gateway 已恢复 | ✅ |
| 主库未挂载 | ❌ |
| 容器内无 `/repo` | ❌ |
| 容器内无 `/Users/macos/angelife.github.com` | ❌ |
| git push / release 权限 | ❌ |

---

## 目标状态

- 宿主机 `/Users/macos/angelife.github.com` 挂载到容器 `/repo`
- NVIDIA 可直接修改 `/repo` 中的项目文件
- 初期 **不授予** git push / release 权限
- 稳定后分阶段考虑 Git 权和发布权

---

## 风险识别

| 风险 | 后果 | 应对 |
|------|------|------|
| 误删主库文件 | 数据丢失，不可逆 | 初期只写文件，不删除 |
| `git add .` | 提交不该提交的文件 | 明确禁止，禁止 AI 执行 git add . |
| 提交 `_incoming/` 或 `.reasonix/` | 污染仓库历史 | 明确禁止 |
| 改坏 changelog.yaml | 构建失败，网站不可用 | 先 git restore 再修改 |
| 删除微信认证文件 | 微信公众号验证失效 | 写入安全红线 |
| 多代理同时操作仓库 | 文件冲突，覆盖丢失 | 单代理施工规则 |
| 凭据暴露 | GitHub Token 泄露 | 容器内不存明文 token |
| 凭据暴露 | Docker socket 泄露 | 不暴露宿主 Docker socket |

---

## 分阶段规划

### 阶段一：只写文件（初期）

**NVIDIA 权限**：
- 读取 `/repo` 中所有文件
- 写入 `/repo` 中指定文件
- 生成 `/opt/data/vXXXX-pickup/` 交接包

**NVIDIA 禁止**：
- 删除 `/repo` 中任何文件
- 执行 git 命令（add / commit / tag / push / pull / fetch）
- 执行 `./tools/angelife-release`
- 修改 `.git/` 目录
- 修改 `.gitignore`

**本地 Mac 职责**：
- docker cp 将交接包复制到仓库
- commit / tag / push
- Hugo 构建
- release

---

### 阶段二：可 commit / tag，不可 push

**NVIDIA 新增权限**：
- 执行 `git add`（精确指定文件，不使用 `.`）
- 执行 `git commit`
- 执行 `git tag`

**NVIDIA 禁止**：
- 执行 `git push`
- 执行 `git push --tags`
- 执行 `git push -u`

**本地 Mac 职责**：
- 审查 NVIDIA 的 commit 内容
- 执行 `git push` 和 `git push --tags`
- 保留撤回权

---

### 阶段三：完整 release（稳定后）

**NVIDIA 新增权限**：
- 执行 `./tools/angelife-release`
- 执行 `git push` 和 `git push --tags`

**前提条件**：
- 阶段二稳定运行 ≥ 5 次无事故
- 本地 Mac 已建立 commit 审查习惯
- 安全红线已全部写入 AI_BOOTSTRAP.md
- 凭据管理方案已确定

---

## 本轮执行限制

**本轮（v0.6.37）明确不执行**：
- 不挂载主库
- 不重启容器
- 不修改 docker run 参数
- 不授予任何新的写仓库权限

---

## 相关文档

- `NVIDIA_GATEWAY_RECOVERY.md` — 故障恢复 SOP
- `CHANGELOG_YAML_RULES.md` — YAML 写入规则
- `AI_BOOTSTRAP.md` — 项目记忆恢复入口（将追加本规划引用）

---

## 责任链

- 规划制定：剑妈 + NVIDIA
- 分阶段决策：人类用户 + 剑妈
- 阶段一执行：本地 Mac
- 风险最终承担：人类用户