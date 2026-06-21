# vault 自动提交行为与 Git 工作流

## 观察记录（v0.7.14 实测）

### vault 行为模式
- vault（Mac）是定时 cron，约每 10 分钟自动跑 `hugo build` 并 commit Hugo 产物
- commit 消息格式示例：`bfb3b60`, `5ab4c9d`, `ab53815`, `7691c09`（无描述性消息）
- 每次 vault commit 后，`public/` 构建产物进入 Git 历史，但 GitHub Pages 仍需 push 才部署

### 实战场景
NVIDIA 在 Docker 内做 posts 清理 + changelog 更新，vault 在间隔内自动 commit 了 Hugo 产物：
```
7691c09 vault: hugo build
8487205 NVIDIA: posts cleanup + changelog
```
此时本地 `/repo` 领先 `origin/master` 1 个 commit，必须及时 `git push` 否则：
1. vault 下次 commit 时会产生 merge conflict
2. 本地改动被 vault 的 auto-merge 覆盖

### 识别 vault 活跃状态
```bash
git -C /repo log --oneline -3
# 如果最新 commit 无描述性消息且 hash 看起来随机 → vault

git -C /repo status --short
# 如果 clean 且 vault 最近有 commit → vault 已接管，不需要再 add/commit public/
```

### 正确的 Git 工作流（在 vault 活跃环境中）
1. 开始工作前：`git -C /repo status` 确认工作区干净
2. 做改动（Hugo 清理、changelog 更新、frontmatter 修改等）
3. `git -C /repo status --short` 确认有 dirty 文件
4. `git -C /repo add hugo-site/content/about/index.md about/` 等（精确指定）
5. `git -C /repo commit -m "description"`
6. **立即** `git -C /repo push origin master`
7. 若 vault 在 10min 内又 commit 了，先 `git -C /repo pull --rebase` 再 push

### 预防原则
- vault 自动 commit 无法关闭（用户配置）
- NVIDIA 的改动必须及时 push，不要积压
- 避免在 vault commit 间隔内做大量文件操作（会被 vault 的 auto-commit 打断）
- vault commit 后 `public/` 已在 git，不需要再 add Hugo 产物

## 多文件版本同步模式（治理规则修正标准流程）

### 触发场景
版本 state 变化（如 v0.7.14）需要在多个治理文件中同步更新。

### 5 文件同步清单
| 文件 | 更新内容 |
|------|---------|
| `README.md` | 版本演进表加入新条目 + 当前版本号 |
| `PROJECT_STATUS.md` | 当前版本状态章节（版本号、commit hash、tag、线上状态）|
| `AI_EXECUTION_AGENTS.md` | 标题版本号（第 N 节标题 `vX.Y`）|
| `AI_WORK_RULES.md` | 顶部注释版本号 |
| `AI_BOOTSTRAP.md` | 当前版本状态重写（版本号 + 已完成 + 后续任务）|

### 执行顺序
1. `git -C /repo log --oneline -3` + `git -C /repo describe --tags` 确认当前 HEAD
2. 更新 5 个文件（`patch` 精准修改，不重写整文件）
3. `hugo build` 验证（若涉及 Hugo 改动）
4. `git add` 精确指定变更文件
5. commit + tag
6. `git push origin master && git push origin vX.Y.Z`

### 本次 v0.7.13→v0.7.14 示例
- README: 全面重写执行层描述（去掉龙虾/蝉师傅/Reasonix）+ 版本演进表 + 发布方式改为 git push + GitHub Actions
- PROJECT_STATUS: 当前版本状态重写 + 已完成内容列表
- AI_EXECUTION_AGENTS: `v0.6.42` → `v0.7.14`（标题）
- AI_WORK_RULES: 顶部注释 `v0.6.42` → `v0.7.14`
- AI_BOOTSTRAP: 当前版本状态重写（五行体系稳定运行 + 下一步任务：giscus评论系统/旧文迁移/配图升级）

### README 全面重写 vs 只改版本号
当版本演进涉及执行层变化（换AI/换工具/换分工），不只是版本号变化时，应全面重写 README 相关章节，不只改版本号。新增版本条目时同步更新执行层描述。