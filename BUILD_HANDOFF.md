# angelife 建站交接手册

本文件是任何 AI 接手 angelife 网站前必须阅读的建站交接手册。

所有 AI 执行代理（OpenClaw/龙虾、Hermes/Hermers、Docker Hermes、Reasonix、Codex、Claude Code 等）统一工作在同一个本地仓库。

Docker Hermes（NVIDIA API / NIM + Minimax 免费练功房）是 angelife 项目的专用练功房，与本机 Hermes 配置、Telegram bot token、DeepSeek 旧配置严格隔离。

所有执行代理同级，没有阶级差异，只有工具特长不同。详见 `AI_EXECUTION_AGENTS.md` 第 14 节。

- macOS 主機：`/Users/macos/angelife.github.com`
- OpenClaw 容器內：`/home/node/.openclaw/workspace/angelife.github.com`

不得各自创建独立流程、独立目录、独立发布方式。

## 当前固定发布方式

固定流程：

1. 在 `hugo-site/` 本地运行 Hugo 构建。
2. **安全 rsync** 到仓库根目录（禁止使用裸 rsync，必须保护治理文档和微信文件）。
3. 提交源文件和根目录静态产物。
4. `git push origin master`。
5. 创建并推送 Git tag，作为可回退备份点。

当前最新版本：`v0.6.33 待发布`。本地有待发布改动，包含 site-workflow 页面更新、流程图接入、日志补全等。

## 接手前必读文件

所有 AI 执行代理接手前必须读取：

- `PROJECT_STATUS.md` — 项目总控进度
- `BUILD_HANDOFF.md` — 建站交接手册（本文件）
- `AI_WORK_RULES.md` — AI 工作规则
- `AI_EXECUTION_AGENTS.md` — AI 执行代理统一身份、权限、边界和协作规则
- `HERMES_COST_RULES.md` — 省 Token 执行规则（适用于所有执行代理）
- `SITE_STYLE_GUIDE.md` — 网站风格规范
- `SITE_CHANGELOG.md` — 内部版本日志
- `DAILY_WORK_LOG.md` — 每日工作日志
- `hugo-site/data/changelog.yaml` — 公开 changelog

## 受控脚本套件（v0.6.20+）

从 v0.6.20 起，项目工具套件包含 4 个脚本：

| 脚本 | 用途 |
|------|------|
| `tools/angelife-status` | 快速查看项目状态（版本、分支、clean 状态、远程对比） |
| `tools/angelife-check` | 发布前置检查（目录/分支/Hugo 构建/Kindle 验收/git 状态） |
| `tools/angelife-cost-log` | AI 成本记录模板（手动填写后粘贴到 DAILY_WORK_LOG.md） |
| `tools/angelife-release` | 受控发布（含前置检查集成 + 成本记录占位符） |

## 受控发布脚本（v0.6.18+）

从 v0.6.18 起，正式发布必须使用受控发布脚本：

```bash
cd /Users/macos/angelife.github.com
./tools/angelife-release v0.6.18 'chore: add controlled release workflow'
./tools/angelife-release --yes v0.6.21 'chore: update release'
```

脚本内部自动执行：目录检查 → 分支检查 → Hugo 清洁构建 → rsync → 精准 git add → commit → tag → push。

以后 Hermes 或 Reasonix 不应自由发挥发布命令，而应在用户授权后调用这个脚本。

> **远程 / 非交互调用**：使用 `--yes` 参数跳过所有确认提示：
> ```bash
> cd /Users/macos/angelife.github.com
> ./tools/angelife-release --yes v0.6.21 'chore: update release'
> ```
> 用于 Hermes Gateway 通过 Telegram 管道调用，避免卡在 `read` 等待输入。

### 标准命令（手工备选）

仅在无法使用脚本时手工执行：

```bash
cd /Users/macos/angelife.github.com/hugo-site
hugo --cleanDestinationDir --minify

cd /Users/macos/angelife.github.com
# ⚠️ 禁止使用裸 rsync -av hugo-site/public/ ./
# 必须使用安全排除规则，至少排除治理文档、微信文件、_incoming/ 等
# 完整排除清单见 AI_EXECUTION_AGENTS.md 第 11 节
touch .nojekyll

git status --short
git commit -m "..."
git push origin master
git tag -a VERSION -m "VERSION: ..."
git push origin VERSION
```

## 当前不优先使用 GitHub Actions 在线构建

当前不默认切换到 GitHub Actions 在线构建。原因：

- 线上实际读取的是仓库根目录静态产物。
- 本地 Hugo `v0.147.4` 构建稳定。
- GitHub Actions 曾因 `Hugo latest` / PaperMod `rss.xml` 兼容问题失败。

除非用户明确授权，不要临时切换部署模式，不要修改 workflow。

## 目录职责

- `hugo-site/`：Hugo 源站目录。
- 仓库根目录：GitHub Pages 实际发布目录。
- `hugo-site/public/`：本地构建产物，构建后通过 `rsync` 同步到仓库根目录。
- `_incoming/`：临时素材区，不提交、不发布。
- `old-site/`：旧站历史版本，保留用于追溯，不随意删除。

## 每轮修改要求

每次修改必须：

- 更新版本号。
- 更新 `SITE_CHANGELOG.md`。
- 更新 `DAILY_WORK_LOG.md`（含「当日 AI 成本」小节）。
- 记录本轮 AI 消耗（模型、估算 token、费用或说明无法获取）。
- 更新 `PROJECT_STATUS.md` 中的当前状态。
- 如影响公开站点，更新 `hugo-site/data/changelog.yaml`。
- 运行 `hugo --cleanDestinationDir --minify`，必须 0 errors。
- **安全 rsync**（禁止裸 `rsync -av hugo-site/public/ ./`；必须排除治理文档、微信认证文件、`_incoming/`、Git 元数据等；完整排除清单见 `AI_EXECUTION_AGENTS.md` 第 11 节）。
- 提交后创建 Git tag。

注意：推荐使用 `publish.sh` 或 `tools/angelife-release`。这些脚本已内置治理文档和微信文件保护。

## 版本号规则

`v2026.05.27-05` 及以前为日期流水版本；自 `v0.6.0` 起，angelife 网站改用 SemVer：`vMAJOR.MINOR.PATCH`。

- `MAJOR`：网站架构、发布方式、主题结构发生破坏性变化，例如 `v1.0.0`、`v2.0.0`。
- `MINOR`：新增功能、栏目、搜索、评论、日志系统、内容体系，例如 `v0.6.0`。
- `PATCH`：修复样式、错字、链接、图片、分类、小 bug，例如 `v0.6.1`。

每次发布必须创建同名 Git tag，tag 是可回退备份点。

## 文章双版本维护（v0.6.11+）

以后每篇文章不写两份正文。

一份 Markdown 源文件 → Hugo 自动生成两个版本：
- 普通图文版 `/posts/<slug>/`
- Kindle 阅读版 `/kindle/posts/<slug>/`

封面图只服务普通版。发布验收必须同时检查两个版本。

## Kindle 接手交接确认（v0.6.14+）

Kindle 阅读模式规则已固化到 `AI_WORK_RULES.md` 和 `SITE_STYLE_GUIDE.md`。

- 修改 layout/header/footer/baseof/single/list/outputFormats 前必须先读 `AI_WORK_RULES.md` 中的 Kindle 不可破坏规则和验收要求。
- 每次发布文章后必须验收普通版和 Kindle 版。
- Kindle 版是独立输出（Hugo outputFormat），不是 CSS 隐藏变体。
- 不得提交 `_incoming/`。
- 不得提交 `.reasonix/`。
- 不得 `git add .`。

## 搜索与评论维护

- 站内搜索依赖首页 JSON 输出与 `/search/` 页面，搜索索引必须包含标题、摘要、正文、分类、标签和链接。
- 搜索增强应保持轻量，不要引入复杂后端。
- 评论系统优先预留 giscus，基于 GitHub Discussions。
- giscus 未配置 `repoId` / `categoryId` 前必须隐藏评论区，不得显示空白报错区。
- 正式启用评论前，需要用户在 GitHub 仓库开启 Discussions，安装/授权 giscus，并提供 `repoId` / `categoryId`。

## 回退方式

统一使用非破坏式回退：

```bash
git checkout VERSION -- .
git commit -m "Rollback site to VERSION"
git push origin master
```

不要使用 force push 回退，除非用户明确要求。

## 手机远控操作指南（v0.6.16+）

推荐启动方式（前台，项目目录运行）：

```bash
cd /Users/macos/angelife.github.com
hermes gateway run --replace
```

不要在后台 launchd 启动，因为默认目录不是项目目录。
Telegram 中执行任务时，Hermes 必须先确认 pwd 为 `/Users/macos/angelife.github.com`。
人类用户 + ChatGPT / 剑妈负责总控、定稿、边界和验收。Reasonix 为执行工，Hermes 为远控+Telegram入口（执行代理）和 terminal 手臂。
如果 Reasonix 无法直接执行 git/Hugo/shell，Hermes 只可按 Reasonix 明确命令代跑。

## 同一时间只能一个代理操作仓库

不得多个 AI 执行代理同时操作 angelife 仓库。当前代理完成并输出报告后，下一个代理才能接手。

## 小改不单独发布

互链修正、标签调整、轻量补充等小改动，保留为本地改动，等形成一批成熟改动后再统一构建发布。

## 本轮 v0.6.33 工作说明

本轮由 NVIDIA（Docker Hermes 独立实例）执行 site-workflow 页面更新与日志补全。

**执行链：**
- 总控 / 验收：人类用户 + ChatGPT / 剑妈
- 执行代理：NVIDIA
- 执行环境：Docker 容器（NVIDIA 独立实例）
- 模型后端：NVIDIA API / NIM + Minimax（免费练功房）
- 修改文件：hugo-site/content/site-workflow/index.md、hugo-site/static/images/workflow/site-control-map.png、SITE_CHANGELOG.md、DAILY_WORK_LOG.md、PROJECT_STATUS.md、BUILD_HANDOFF.md、hugo-site/data/changelog.yaml
- 是否构建：待 Hugo 构建（NVIDIA 容器无 Hugo 需 macOS 本机）
- 是否 rsync：待安全 rsync（macOS 本机执行）
- 是否提交：待 commit
- 是否发布：待 tag v0.6.33 + push

**本轮更新内容：**
- site-workflow 页面更新为最新版《建站模式日志》
- 补入项目总控流程图 `/images/workflow/site-control-map.png`（2MB）
- 更新所有日志文件

**遵守规则：**
- 安全 rsync 排除清单已完整（.gitignore、.gitmodules、publish.sh、tools/ 等已保护）
- 禁止裸 rsync、禁止 git add .、必须精确指定文件
- 微信认证文件 0847745cb78663855a3a1732c9c6a130.txt 已保护
- 署名追责：NVIDIA、NVIDIA 容器、minimaxai/minimax-m2.7

**当前状态：尚未 Hugo 构建、尚未 rsync、尚未 commit、尚未 tag、尚未发布。**

## 本轮 v0.6.32 工作说明

本轮由 NVIDIA（Docker Hermes 独立实例）执行规则一致性整理与日志补全。

**本轮修正内容：**
- Docker Hermes 独立实例正式命名为"NVIDIA"
- 明确 NVIDIA 是 NVIDIA API / NIM + Minimax 免费练功房，高 token 累活执行代理
- 明确 NVIDIA 不是总控代理（总控：人类用户 + ChatGPT / 剑妈）
- 明确所有 AI 执行代理同级，无阶级差异，只有工具特长不同

**本轮修改文件：**
`AI_EXECUTION_AGENTS.md`、`AI_WORK_RULES.md`、`HERMES_COST_RULES.md`、`BUILD_HANDOFF.md`、`SITE_CHANGELOG.md`、`DAILY_WORK_LOG.md`、`PROJECT_STATUS.md`、`hugo-site/data/changelog.yaml`

**当前状态：尚未 commit、尚未 tag、尚未发布。下一步由指定执行代理统一构建发布。**

## 微信认证文件保护

微信认证文件（`hugo-site/static/...` 和根目录 `0847745cb78663855a3a1732c9c6a130.txt`，内容 `01413348ab0d5b381a2e7099ba2600ed57ad50d3`）永久受保护。任何构建、rsync、清理、发布不得删除或覆盖。

## 接手报告与交接报告执行链格式

每轮交接必须包含以下执行链信息：

```
- 总控 / 验收：人类用户 + ChatGPT / 剑妈
- 执行代理：（龙虾 / 蝉师傅 / NVIDIA / Reasonix / Codex / Claude Code）
- 执行环境：（macOS 本机 / Docker 容器 / OpenClaw 容器 / Telegram 远控 / 手工终端）
- 模型后端：（DeepSeek / NVIDIA API / NIM + Minimax / OpenAI / Claude）
- 修改文件：（精确列出文件名）
- 是否构建：（Hugo 构建结果或"未构建"）
- 是否 rsync：（是/否，如是说明排除项是否完整）
- 是否提交：（commit hash 或"未提交"）
- 是否发布：（是/否，如否则说明原因）
- 异常与风险：（无 / 有问题需说明）
```

禁止匿名交接。禁止只写"已完成"不附执行链。

## v0.6.35 交接记录

新增 `AI_BOOTSTRAP.md`。

以后任何 AI 接手 angelife 项目前，必须先读：

1. `AI_BOOTSTRAP.md`
2. `PROJECT_STATUS.md`
3. `BUILD_HANDOFF.md`
4. `AI_WORK_RULES.md`
5. `AI_EXECUTION_AGENTS.md`
6. `DAILY_WORK_LOG.md`
7. `SITE_CHANGELOG.md`
8. `hugo-site/data/changelog.yaml`

本文件用于防止新聊天、新机器人、新执行环境遗忘项目规则。

### 三者分工

- 剑妈：设计师 + 总控
- NVIDIA：具体做事者
- 本地 Mac：补完 NVIDIA 因 Docker 限制无法完成的本机动作

### 责任规则

谁干活，谁署名。  
谁操作，谁负责。  
谁出问题，能回溯。

## v0.6.36 构建交接 — 2026-05-29

**版本**：v0.6.36
**目标**：更新 README.md 为 GitHub 项目 AI 接手入口

**上游交付物**：
- README.md（已生成，重写为 AI 接手入口）
- DAILY_WORK_LOG.md 草案（已生成）
- SITE_CHANGELOG.md 追加（已生成）
- PROJECT_STATUS.md 追加（已生成）
- BUILD_HANDOFF.md 追加（已生成）
- hugo-site/data/changelog.yaml 追加（已生成）

**本地 Mac 接收检查清单**：
□ 确认仓库根目录的 README.md 被覆盖替换为新版本
□ 确认 DAILY_WORK_LOG.md 追加了 v0.6.36 记录
□ 确认 SITE_CHANGELOG.md 追加了 v0.6.36 记录
□ 确认 PROJECT_STATUS.md 当前版本更新为 v0.6.36
□ 确认 BUILD_HANDOFF.md 追加了 v0.6.36 构建交接记录
□ 确认 hugo-site/data/changelog.yaml 追加了 v0.6.36 条目
□ Hugo 构建无报错
□ tools/angelife-release v0.6.36（待授权）
□ git add 精确指定文件（不用 git add .）
□ git commit -m 含版本号 v0.6.36
□ git tag v0.6.33 已推送
□ 线上验证 README.md 返回 200
□ 微信认证文件仍存在

**发布前必须停下的条件**：
- tools/angelife-release 不可用
- Hugo 构建报错
- 微信认证文件缺失

**交接方**：NVIDIA
**接收方**：本地 Mac
**验收方**：人类用户 + ChatGPT / 剑妈## v0.6.37 构建交接 — 2026-05-29

**版本**：v0.6.37
**目标**：固化 NVIDIA Gateway 恢复 SOP 与 YAML 写入规则

**上游交付物**：
- `NVIDIA_GATEWAY_RECOVERY.md`（新增，SOP 全文）
- `CHANGELOG_YAML_RULES.md`（新增，规则全文）
- `NVIDIA_MAIN_REPO_MOUNT_PLAN.md`（新增，规划全文）
- `AI_BOOTSTRAP_APPEND.md`（追加块）
- `README_APPEND.md`（追加块）
- `DAILY_WORK_LOG_APPEND.md`（日志追加块）
- `SITE_CHANGELOG_APPEND.md`（changelog 追加块）
- `PROJECT_STATUS_APPEND.md`（状态追加块）
- `BUILD_HANDOFF_APPEND.md`（本文件）
- `changelog_yaml_block.yaml`（标准 YAML 块）

**本地 Mac 接收检查清单**：

□ 追加 AI_BOOTSTRAP.md（将 AI_BOOTSTRAP_APPEND.md 内容追加到文件末尾）
□ 追加 README.md（将 README_APPEND.md 内容追加到文件末尾）
□ 追加 DAILY_WORK_LOG.md（追加 v0.6.37 记录）
□ 追加 SITE_CHANGELOG.md（追加 v0.6.37 记录）
□ 追加 PROJECT_STATUS.md（追加 v0.6.37 记录）
□ 追加 BUILD_HANDOFF.md（追加本记录）
□ **插入** changelog_yaml_block.yaml 内容到 hugo-site/data/changelog.yaml（注意是插入，非追加）
□ Hugo 构建验证：`hugo --gc --cleanDestinationDir --minify -s hugo-site`
□ tools/angelife-release v0.6.37（待授权）
□ git add 精确指定文件（不用 git add .）
□ git commit -m 含版本号 v0.6.37
□ git tag v0.6.37 已推送
□ 线上验证 /site-workflow/ 返回 200
□ 微信认证文件仍存在

**changelog_yaml_block.yaml 插入注意**：
- 该文件为标准 YAML 块，不能直接 cat >> 拼接
- 必须按 CHANGELOG_YAML_RULES.md 模板插入
- 插入后必须 Hugo 构建验证

**发布前必须停下的条件**：
- Hugo 构建报错（尤其是 YAML 格式）
- tools/angelife-release 不可用
- 微信认证文件缺失

**交接方**：NVIDIA
**接收方**：本地 Mac
**验收方**：人类用户 + ChatGPT / 剑妈## v0.6.38 构建交接 — 2026-05-29

**版本**：v0.6.38
**目标**：主库挂载预检完成，安全启动方案就绪

**关键发现（请本地 Mac 确认）**：
- 主库已挂载到 `/workspace/angelife.github.com`
- `/repo` 路径在容器内不存在
- Telegram gateway 正常运行

**上游交付物**：
- `NVIDIA_REPO_MOUNT_RUNBOOK.md`（完整 RUNBOOK）
- `DAILY_WORK_LOG_APPEND.md`（日志追加块）
- `SITE_CHANGELOG_APPEND.md`（changelog 追加块）
- `PROJECT_STATUS_APPEND.md`（状态追加块）
- `BUILD_HANDOFF_APPEND.md`（本文件）
- `changelog_yaml_block.yaml`（标准 YAML 块）

**本地 Mac /repo 路径方案选择**：

方案一（立即可用，临时，重启丢失）：
```bash
docker exec hermes-minimaxlab ln -sf /workspace/angelife.github.com /repo
docker exec hermes-minimaxlab ls /repo/README.md
```

方案二（推荐，等授权后执行，新建容器）：
- 按 `NVIDIA_REPO_MOUNT_RUNBOOK.md` 中的完整 docker run 命令
- 同时保留 `/repo` 和 `/workspace/angelife.github.com` 两种挂载
- 验证 Telegram gateway 在新容器中正常

**本地 Mac 接收检查清单**：

□ 读取 NVIDIA_REPO_MOUNT_RUNBOOK.md
□ 选择 /repo 路径方案（symlink 或新容器）
□ 执行方案一（symlink）或方案二（新容器，等授权）
□ 验证 /repo/README.md 可访问
□ 验证 git status -sb 可执行
□ 追加日志文件
□ Hugo 构建验证（后续）
□ tools/angelife-release v0.6.38（待授权）
□ git add / commit / tag / push（待授权）

**发布前必须停下的条件**：
- /repo 路径不可访问
- Telegram gateway 在新容器中异常
- Hugo 构建报错

**交接方**：NVIDIA
**接收方**：本地 Mac
**验收方**：人类用户 + ChatGPT / 剑妈
## v0.6.39 构建交接 — 2026-05-29

**版本**：v0.6.39
**目标**：NVIDIA 直接写主库试运行验证

**NVIDIA 已完成**：
- 通过 /repo 直接写入主库文件
- 新增 NVIDIA_DIRECT_WRITE_TRIAL.md
- 追加 DAILY_WORK_LOG.md / SITE_CHANGELOG.md / PROJECT_STATUS.md / BUILD_HANDOFF.md

**本地 Mac 接收检查清单**：

□ 检查 git diff：确认 NVIDIA 直接写入的文件
□ 确认无意外修改（old-site/ / themes/ / _incoming/ / .reasonix/ 未触碰）
□ 插入 hugo-site/data/changelog.yaml（changelog_yaml_block.yaml 按模板插入）
□ Hugo 构建验证：hugo --gc --cleanDestinationDir --minify -s hugo-site
□ tools/angelife-release v0.6.39（待授权）
□ git add 精确指定文件（不用 git add .）
□ git commit -m "v0.6.39: NVIDIA 直接写主库试运行"
□ git tag -a v0.6.39 -m "v0.6.39"（注意 tag 版本号）
□ git push && git push --tags（待授权）
□ 线上验证 /site-workflow/ 返回 200
□ 微信认证文件仍存在

**NVIDIA 写入的新文件**：
- NVIDIA_DIRECT_WRITE_TRIAL.md（untracked）

**NVIDIA 修改的文件**：
- DAILY_WORK_LOG.md
- SITE_CHANGELOG.md
- PROJECT_STATUS.md
- BUILD_HANDOFF.md

**发布前必须停下的条件**：
- Hugo 构建报错
- tools/angelife-release 不可用
- 微信认证文件缺失

**交接方**：NVIDIA
**接收方**：本地 Mac
**验收方**：人类用户 + ChatGPT / 剑妈

## v0.6.40 构建交接 — 2026-05-29

**版本**：v0.6.40
**目标**：发布文章《震之随六五：在惊动中摸到规律》

**NVIDIA 已完成**：
- 通过 /repo 直接写入 Hugo 文章源文件
- 新增 hugo-site/content/posts/zhen-to-sui-touching-the-pattern/index.md

**本地 Mac 接收检查清单**：

□ 检查 git diff：确认文章源文件已新增
□ 确认无意外修改（old-site/ / themes/ / _incoming/ / .reasonix/ 未触碰）
□ changelog_yaml_block.yaml → 插入 hugo-site/data/changelog.yaml（按模板）
□ Hugo 构建验证：hugo --gc --cleanDestinationDir --minify -s hugo-site
□ tools/angelife-release v0.6.40（待授权）
□ git add 精确指定文件（不用 git add .）
□ git commit -m "v0.6.40: 发布文章《震之随六五：在惊动中摸到规律》"
□ git tag -a v0.6.40 -m "v0.6.40"
□ git push && git push --tags（待授权）
□ 线上验证 /posts/zhen-to-sui-touching-the-pattern/ 返回 200
□ 线上验证 /changelog/ 返回 200
□ 微信认证文件仍存在

**NVIDIA 写入的新文件**：
- hugo-site/content/posts/zhen-to-sui-touching-the-pattern/index.md（untracked）

**发布前必须停下的条件**：
- Hugo 构建报错
- tools/angelife-release 不可用
- 微信认证文件缺失

**交接方**：NVIDIA
**接收方**：本地 Mac
**验收方**：人类用户 + ChatGPT / 剑妈
