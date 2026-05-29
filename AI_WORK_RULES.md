# angelife AI 工作规则

本文件适用于所有接手 angelife 网站的 AI 执行代理，包括 OpenClaw/龙虾、Hermes/Hermers、Docker Hermes、Reasonix、Codex、Claude Code 或其他 AI 执行代理。

ChatGPT / 剑妈是总控，不属于 AI 执行代理；DeepSeek 是模型后端，不属于 AI 执行代理。

## 执行代理同级原则

龙虾、Hermes、Docker Hermes、Reasonix、Codex、Claude Code 都是同级 AI 执行代理。
没有阶级差异，只有工具特长、成本、稳定性、界面和模型后端的差异。

- **OpenClaw / 龙虾**：目标逐步接 Codex 的主力施工位，适合网页可视化、长会话、真实仓库施工。
- **Hermes（本机）**：手机远控和 Telegram 入口（执行代理）
- **NVIDIA（Docker Hermes）**：NVIDIA API / NIM + Minimax 免费练功房，高 token 累活执行代理，适合长文档处理、规则整理、日志补账。不污染本机蝉师傅 Hermes 和 DeepSeek 旧配置。
- **Reasonix**：项目执行工，配合总控（人类+剑妈）完成发布流程。
- **Codex**：主力施工代理（过渡期，目标由 OpenClaw/龙虾逐步接替）。
- **Claude Code**：复杂推理与代码修改。

所有代理必须遵守同一仓库、同一流程、同一时间单代理操作原则。

## 统一工地

所有 AI 执行代理默认操作同一个本地仓库：

- macOS 主机：`/Users/macos/angelife.github.com`
- OpenClaw 容器内：`/home/node/.openclaw/workspace/angelife.github.com`

不得各自创建独立流程、独立目录、独立发布方式。

## 接手前必读

任何 AI 接手前必须先读：

- `PROJECT_STATUS.md`
- `BUILD_HANDOFF.md`
- `AI_WORK_RULES.md`
- `AI_EXECUTION_AGENTS.md`
- `HERMES_COST_RULES.md`
- `SITE_STYLE_GUIDE.md`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `hugo-site/data/changelog.yaml`

> 所有 AI 执行代理接手前必须读取并遵守 `AI_EXECUTION_AGENTS.md`。OpenClaw/龙虾、Hermes/Hermers、Reasonix、Codex、Claude Code 等工具同属 AI 执行代理，只有特长差异，没有阶级高低；它们统一使用同一个本地仓库和同一套发布流程。

## 硬性禁止

- 不准修改 `.github/workflows/` 或新增任何 GitHub Actions 构建 workflow。
- 不准切换 GitHub Actions 在线构建。
- 不准 `git add .`。
- 不准提交 `_incoming/`。
- 不准发布 `_incoming/`。
- 不准改完不写日志。
- 不准破坏首页宽屏布局。
- 不准破坏文章页窄栏书页风格。
- 不准只提交 Hugo 源文件而忘记 `rsync` 根目录静态产物。
- 不准大范围重写文章正文，除非用户明确要求。
- 不准删除 `old-site/`、`themes/`、`public/` 历史内容，除非用户明确要求。
- 不准破坏 Kindle 阅读模式的独立输出。Kindle 版是独立阅读输出，不是普通页面的 CSS 隐藏变体。修改 header、footer、baseof、single、list、outputFormats 或导航模板时，必须同时验收普通版和 Kindle 版。不得让 `/kindle/` 或 `/kindle/posts/<slug>/` 输出 PaperMod 普通导航、普通 footer 或桌面站点 chrome。

- 人类用户 + ChatGPT / 剑妈负责总控、定稿、边界和验收。Hermes / Docker Hermes / 龙虾 / Reasonix / Codex / Claude Code 都是 AI 执行代理。
- Hermes 是手机远控和 Telegram 入口（执行代理）。Reasonix 是项目执行工。Hermes 默认不得直接修改项目文件，不得自行 patch，不得自行扩大 git add，不得擅自 commit/tag/push。当 Reasonix 在 headless/MCP 场景下无法执行 shell 命令时，Hermes 可以作为 terminal 手臂代跑 shell，但必须严格执行 Reasonix 明确列出的命令，不得自由发挥。
- 正式发布必须使用 `tools/angelife-release` 脚本，Reasonix 不直接裸跑 git push/tag，Hermes 不自行拼接发布流程。

## 固定发布流程

继续使用受控发布脚本：

```bash
./tools/angelife-release [--yes] <version> '<commit message>'
```

等价于以下标准流程：

```text
本地 Hugo 生成 -> rsync 到仓库根目录 -> commit -> push -> git tag
```

使用 `--yes` 可跳过两次确认提示，用于 Hermes 远程非交互发布（如 Telegram 管道调用）。

## 受控发布脚本规则（v0.6.18+）

- 以后正式发布优先使用 `tools/angelife-release`。
- Reasonix 不直接裸跑 `git push` / `git tag`。
- Hermes 不自行拼接发布流程。
- 发布权交给用户授权 + 固定脚本。
- Hermes 只负责代跑脚本，不得自行 patch 或修复 Reasonix 输出。
- Reasonix 输出修改后如需代跑，应直接输出 `./tools/angelife-release <version> '<commit message>'` 命令。

调用方式：

```bash
cd /Users/macos/angelife.github.com
./tools/angelife-release v0.6.18 'chore: add controlled release workflow'
```

脚本内部已实现：
1. 检查当前目录必须是 `/Users/macos/angelife.github.com`。
2. 检查当前分支必须是 master。
3. 检查 version 参数不能为空。
4. 检查 commit message 参数不能为空。
5. 禁止 `git add .`（通过精准逐个添加替代）。
6. 禁止提交 `_incoming/`。
7. 禁止提交 `.reasonix/`。
8. 执行 Hugo 清洁构建：`hugo --gc --cleanDestinationDir --minify -s hugo-site`。
9. rsync Hugo 产物到仓库根目录。
10. 精准 git add 本轮修改内容，显式排除 `_incoming/` 和 `.reasonix/`。
11. git commit 使用传入 commit message。
12. git tag 使用传入 version。
13. git push origin master。
14. git push origin <version>。
15. 输出收工确认信息。

## AI 消耗记录规则（v0.6.19+）

每轮 AI 任务必须记录 AI token 消耗与费用。

### 记录原则

1. **每轮必记** — 每轮 AI 任务（Reasonix 每次 run）必须记录 token 消耗与费用。
2. **shell 不计** — shell 命令本身的 token 消耗不单独记录。
3. **收工必报** — 收工报告必须新增「AI 消耗记录」条目。
4. **不编造精确值** — 如果无法获取精确 token 数，如实说明原因（如：DeepSeek 控制台未开放 token 明细 API）。
5. **每日汇总** — Daily 工作日志增加「当日 AI 成本」小节。
6. **余额差值法** — 建议大任务前后记录 DeepSeek 控制台余额，用差值估算成本。

### 成本优化原则

- 默认使用 flash 模型（低成本）。
- 仅复杂任务（跨文件架构重构、并发安全分析等）使用 pro 模型。
- 避免重复全量读仓库；优先精确读取目标文件或搜索定位。
- 长任务拆段执行，避免单轮上下文过长导致重复计费。

### 安全红线

- 日志中严禁出现 API key、token（认证令牌）、密钥等敏感信息。
- 不得在日志、commit message、公开 changelog 中泄露任何凭证。
- 模型名称（如 DeepSeek Chat / deepseek-v4-flash）可以记录。

## 版本号规则

`v2026.05.27-05` 及以前为日期流水版本；自 `v0.6.0` 起，angelife 网站改用 SemVer：`vMAJOR.MINOR.PATCH`。

- `MAJOR`：网站架构、发布方式、主题结构发生破坏性变化。
- `MINOR`：新增功能、栏目、搜索、评论、日志系统、内容体系。
- `PATCH`：修复样式、错字、链接、图片、分类、小 bug。

每次提交后必须创建对应 Git tag。

## 搜索与评论规则

- 维护搜索时必须确认 `/search/` 可打开，关键词能命中文章，并有上下文摘要。
- 搜索索引应覆盖 `title`、`summary` / `description`、`content`、`categories`、`tags`、`permalink`。
- 评论系统优先 giscus，不准引入 Disqus。
- giscus 未配置 `repoId` / `categoryId` 时，评论区必须默认隐藏。
- `comments: true` / `comments: false` 应由文章 front matter 控制；旧日志、资料归档、短日课默认不开。

## 文章双版本发布规则（v0.6.11 起固化）

每篇文章只维护一份 Markdown 源文件，Hugo 自动输出两个版本：

- 普通图文版：`/posts/<slug>/`
- Kindle 阅读版：`/kindle/posts/<slug>/`

由 `content/posts/_index.md` 的 `cascade` 配置自动控制：

[cascade]
  outputs = ["HTML", "Kindle"]

发布验收必须同时检查两个版本：

| 检查项 | 普通图文版 | Kindle 阅读版 |
|--------|-----------|--------------|
| 封面图 | 正常显示 | 不显示 |
| 导航 | 完整导航 | 无主导航/搜索/分类导航 |
| 标签/评论/分享 | 正常 | 不显示 |

封面图只服务普通图文版；不为 Kindle 版单独维护图片或第二份正文。

### Kindle 验收强制要求

每次修改后必须执行以下验收：

1. `/kindle/` 目录页无普通导航（grep 金·判断/木·蝉识/搜索/id="menu" /kindle/index.html 应为 0）
2. `/kindle/posts/<slug>/` 文章页无普通导航和 footer（grep Powered by/PaperMod/id="menu" 应为 0）
3. `/posts/<slug>/` 普通文章页必须保留正常导航
4. 首页普通导航必须保留
5. 不得通过 `display:none` 临时遮挡来伪造 Kindle 模式——模板层必须已剥离

## 每轮收工必须输出

- 版本号。
- 修改目标。
- 修改文件。
- 具体改动。
- 影响页面。
- Hugo 构建结果。
- `rsync` 是否完成。
- commit hash。
- git tag。
- 是否未提交 `_incoming`。
- 线上验证结果。
- AI 消耗记录（模型、估算 token、费用或说明无法获取）。
- 下轮接手提示。

## Hermes / Reasonix 手机远控工作流

固定链路：

手机 Telegram → Hermes（远控+Telegram入口）→ 总控（人类+剑妈） → terminal → reasonix run → Reasonix 执行 → Hermes 按 Reasonix 明确命令代跑 shell → Hugo 构建 → rsync → 精准 git add → commit → tag → push



Hermes 代跑 shell 白名单：

pwd、ls、cat、grep、rg、git status、git diff、git log、hugo --gc --cleanDestinationDir --minify -s hugo-site、安全 rsync（见下方安全排除规则）、精准 git add <文件列表>、git commit、git tag、git push、./tools/angelife-status、./tools/angelife-check、./tools/angelife-cost-log

**安全 rsync 规则：** 禁止使用裸 `rsync -av hugo-site/public/ ./`。正式 rsync 必须至少排除治理文档、微信认证文件、Git 元数据和 `_incoming/`。具体排除清单见 `AI_EXECUTION_AGENTS.md` 第 11 节。

任何超出白名单的命令必须先汇报并等待用户确认。

## 署名追责规则

所有 AI 执行代理接手、修改、构建、发布、排障，都必须署名留痕。报告中必须写清：

- 执行代理名称（龙虾 / 蝉师傅 / NVIDIA / Reasonix / Codex / Claude Code）
- 执行环境（macOS 本机 / Docker 容器 / Telegram 远控 / 手工终端）
- 模型后端（DeepSeek / NVIDIA API / NIM + Minimax / OpenAI / Claude）
- 修改文件（精确到文件名）
- 是否构建（Hugo 构建结果）
- 是否 rsync
- 是否 git add / commit / tag / push
- 是否发布线上

禁止匿名施工。禁止只写"已完成"而不写执行者。禁止多个代理共同操作但不区分责任。

## Git 添加规则

不要使用 `git add .`。

按任务范围精确添加源文件和根目录静态产物。每次提交前必须运行：

```bash
git status --short
git diff --cached --stat
git diff --cached --name-only | rg '^_incoming|^\.github/workflows/'
```

如果发现 `_incoming/` 或未授权 workflow 修改，必须取消暂存并重新检查。

## 同一时间只能一个代理操作仓库

不得多个 AI 执行代理同时操作同一个 angelife 仓库。

当前代理接手 → 读取规则 → 执行任务 → 输出改动报告 → 停止等待确认 → 下一个代理再接手。

禁止并发修改同一批文件。

## 小改不单独发布

互链修正、标签调整、轻量补充等小改动，不单独发布。

应保留为本地待发布改动，等形成一批成熟改动后，再统一 Hugo 构建、rsync、commit、tag、push。

## 微信认证文件保护

微信认证文件必须永久保护。

- 源文件：`hugo-site/static/0847745cb78663855a3a1732c9c6a130.txt`
- 根目录文件：`0847745cb78663855a3a1732c9c6a130.txt`
- 内容：`01413348ab0d5b381a2e7099ba2600ed57ad50d3`
- 线上地址：`https://angelife.github.io/0847745cb78663855a3a1732c9c6a130.txt`

任何构建、rsync、清理、发布，都不得删除或覆盖该文件。

## 发布前安全检查规则（RULE-021 至 RULE-025，v0.6.41+）

所有正式发布前必须通过以下检查：

**RULE-021：.git 目录存在检查**
- 发布前必须验证当前目录是 Git 仓库
- 验证命令：`test -d ".git" && echo "OK" || echo "FAIL"`
- 失败处理：`log_error` 并 exit 1

**RULE-022：hugo-site 目录存在检查**
- 发布前必须验证 Hugo 源站存在
- 验证命令：`test -d "hugo-site" && echo "OK" || echo "FAIL"`
- 失败处理：`log_error` 并 exit 1

**RULE-023：bind mount 路径安全检查**
- 当前目录必须在白名单路径内：`/Users/macos/angelife.github.com` 或 `/repo`
- 禁止在非白名单目录执行 rsync 或 release
- 失败处理：`log_error` 并 exit 1

**RULE-024：dry-run 预览**
- 实际执行前必须输出本轮将执行的操作预览
- 包括：Hugo 源站路径、rsync 目标路径、版本号、Commit 信息
- 预览不等于执行，用于操作者确认

**RULE-025：repo 快照提示**
- 发布前提示创建快照：`git bundle create /tmp/angelife-$(date +%Y%m%d).bundle --all`
- 快照为可选操作，但推荐执行
- 快照可以防范 rsync --delete 误删等不可逆操作

完整规则见 `RELEASE_SCRIPT_SAFETY_RULES.md`。
