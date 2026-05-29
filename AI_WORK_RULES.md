# angelife AI 工作规则

> **v0.6.42 更新**：NVIDIA（Docker Hermes）升级为总控，负责方向决策、内容管理、规则维护。本规则同步更新。
>
> 人类用户 + 剑妈 + NVIDIA 共同决策，NVIDIA 主导日常运行，用户拥有最终否决权。

---

## 角色定义

### 总控层

| 角色 | 职责 |
|------|------|
| **NVIDIA（Docker Hermes）** | 总控：方向决策、内容管理、规则维护、全流程执行（除最终 push 外） |
| **人类用户** | 最终验收：所有 push/rsync 必须经用户确认后执行 |
| **剑妈** | 方向顾问：架构、口径、验收标准 |

### 执行代理

- **OpenClaw / 龙虾**：网页可视化、长会话、真实仓库施工
- **Hermes（本机）**：手机远控和 Telegram 入口
- **Reasonix**：项目执行工，配合总控完成发布
- **Codex / Claude Code**：复杂推理与代码修改

所有执行代理同级，无阶级差异，只有工具特长差异。

---

## 发布授权链

```
NVIDIA（总控）
  → 方向决策、内容生成、规则维护
  → 完成 commit + tag
  → 报用户："准备好了，push 吗？"
  → 用户确认
  → NVIDIA 执行 push
```

**硬性规则：push / rsync / git push 必须等用户说"发"才能执行。未获授权不得自行 push。**

---

## 硬性禁止

- 不准修改 `.github/workflows/` 或新增任何 GitHub Actions 构建 workflow。
- 不准切换 GitHub Actions 在线构建。
- 不准 `git add .`。
- 不准提交 `_incoming/`。
- 不准发布 `_incoming/`。
- 不准改完不写日志。
- 不准破坏首页宽屏布局。
- 不准破坏文章页窄栏书页风格。
- 不准只提交 Hugo 源文件而忘记 rsync 根目录静态产物。
- 不准大范围重写文章正文，除非用户明确要求。
- 不准删除 `old-site/`、`themes/`、`public/` 历史内容。
- 不准破坏 Kindle 阅读模式的独立输出。
- **不准在未获用户授权的情况下执行 git push / rsync / tag push。**

---

## 发布流程

### 标准流程（NVIDIA 主责）

```bash
# 1. 生成 + 构建（NVIDIA 容器内）
cd /repo/hugo-site && /opt/data/hugo

# 2. 同步 public/ → 仓库根目录（无 rsync 时用 cp）
cd /repo && cp -a hugo-site/public/* ./

# 3. 精准 git add（禁止 git add .）
cd /repo
git add <精确文件列表>

# 4. commit + tag
git commit -m "v0.x.x: 内容描述"
git tag -a v0.x.x -m "v0.x.x: ..."

# 5. 报告用户，等确认
#   "v0.6.42 已完成 build + commit + tag，文章：...，改动：...
#    确认发布？"

# 6. 用户确认后，执行 push
git push origin master && git push origin v0.x.x

# 7. 线上验证
curl -s https://angelife.github.io/posts/文章slug/ | grep -c "关键词"
```

### Mac 辅助流程（可选）

Mac 可使用受控脚本发布，跳过步骤 1-4：

```bash
cd /Users/macos/angelife.github.com
./tools/angelife-release [--yes] v0.x.x '<commit message>'
```

### 发布确认格式

报用户的内容必须包含：
- 版本号
- 文章列表（新增 / 修改）
- 改动摘要
- Hugo build 结果
- commit hash
- **"确认发布？"**

---

## 版本号规则

自 v0.6.0 起使用 SemVer：`vMAJOR.MINOR.PATCH`

- `MAJOR`：架构、发布方式、主题结构发生破坏性变化
- `MINOR`：新增功能、栏目、搜索、评论、内容体系
- `PATCH`：修复样式、错字、链接、图片、分类、小 bug

每次提交后必须创建对应 Git tag。

---

## 文章双版本发布规则

每篇文章只维护一份 Markdown 源文件，Hugo 自动输出：

- 普通图文版：`/posts/<slug>/`
- Kindle 阅读版：`/kindle/posts/<slug>/`

发布验收必须同时检查两个版本。

Kindle 验收强制要求：

1. `/kindle/` 目录页无普通导航
2. `/kindle/posts/<slug>/` 文章页无普通导航和 footer
3. `/posts/<slug>/` 普通文章页保留正常导航
4. 不得通过 `display:none` 临时遮挡来伪造 Kindle 模式

---

## 微信认证文件保护

微信认证文件必须永久保护：

- 源文件：`hugo-site/static/0847745cb78663855a3a1732c9c6a130.txt`
- 根目录文件：`0847745cb78663855a3a1732c9c6a130.txt`
- 内容：`01413348ab0d5b381a2e7099ba2600ed57ad50d3`
- 线上地址：`https://angelife.github.io/0847745cb78663855a3a1732c9c6a130.txt`

任何构建、rsync、清理、发布，都不得删除或覆盖该文件。

---

## 署名追责规则

所有操作必须署名留痕：

- 执行者名称
- 执行环境（macOS 本机 / Docker 容器 / Telegram 远控 / 手工终端）
- 模型后端
- 修改文件（精确到文件名）
- Hugo 构建结果
- 是否 rsync
- 是否 git add / commit / tag / push
- 是否发布线上

禁止匿名施工，禁止只写"已完成"而不写执行者。

---

## AI 消耗记录规则

每轮任务必须记录 token 消耗与费用：

- 每轮必记
- shell 不计
- 收工必报
- 不编造精确值
- 模型名称可以记录
- **日志中严禁出现 API key、token（认证令牌）、私钥等敏感信息**

---

## 接手前必读

任何 AI 接手前必须先读：

- `PROJECT_STATUS.md`
- `BUILD_HANDOFF.md`
- `AI_WORK_RULES.md`（本文件）
- `AI_EXECUTION_AGENTS.md`
- `SITE_STYLE_GUIDE.md`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `hugo-site/data/changelog.yaml`

---

## 统一工地

所有 AI 执行代理默认操作同一个本地仓库：

- macOS 主机：`/Users/macos/angelife.github.com`
- Docker 容器：`/repo`（软链接 → `/workspace/angelife.github.com`）
- OpenClaw 容器内：`/home/node/.openclaw/workspace/angelife.github.com`

不得各自创建独立流程、独立目录、独立发布方式。

---

## 发布前安全检查规则（RULE-021 至 RULE-025）

所有正式发布前必须通过：

- **RULE-021**：.git 目录存在检查
- **RULE-022**：hugo-site 目录存在检查
- **RULE-023**：bind mount 路径安全检查（白名单：`/Users/macos/angelife.github.com` 或 `/repo`）
- **RULE-024**：dry-run 预览（操作者确认）
- **RULE-025**：repo 快照提示（推荐）

---

*本文件由 NVIDIA（总控）起草、落盘、署名。*
*生效日期：v0.6.42*