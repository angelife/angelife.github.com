# angelife 每日工作日志

## 2026-05-29｜v0.6.33｜NVIDIA 更新建站模式日志并补入项目总控流程图

### 执行链

- 总控 / 验收：人类用户 + ChatGPT / 剑妈
- 执行代理：NVIDIA（Docker Hermes 独立实例）
- 执行环境：Docker 容器（NVIDIA 独立实例）
- 模型后端：NVIDIA API / NIM + Minimax（免费练功房）
- 修改文件：hugo-site/content/site-workflow/index.md、hugo-site/static/images/workflow/site-control-map.png、SITE_CHANGELOG.md、DAILY_WORK_LOG.md、PROJECT_STATUS.md、BUILD_HANDOFF.md、hugo-site/data/changelog.yaml
- 是否构建：待 Hugo 构建（NVIDIA 容器无 Hugo 需 macOS 本机）
- 是否 rsync：待安全 rsync（macOS 本机执行）
- 是否提交：待 commit
- 是否发布：待 tag v0.6.33 + push

### 今天做了什么（NVIDIA 接手）

**接手来源**：用户通过 Telegram DM 发送 site-workflow-update-package.zip，指定 NVIDIA 执行。

**本包内容**：
1. `hugo-site/content/site-workflow/index.md` — 最新版《建站模式日志》正文
2. `hugo-site/static/images/workflow/site-control-map.png` — 项目总控流程图（2MB）

**操作内容**：
- 将包内两个文件复制到仓库对应路径
- 更新 SITE_CHANGELOG.md、DAILY_WORK_LOG.md、PROJECT_STATUS.md、BUILD_HANDOFF.md、hugo-site/data/changelog.yaml

**遵守规则**：
- 安全 rsync 排除清单（.gitignore、.gitmodules、publish.sh、tools/ 等已保护）
- 禁止裸 rsync、禁止 git add .、必须精确指定文件
- 微信认证文件 0847745cb78663855a3a1732c9c6a130.txt 已保护
- 署名追责：NVIDIA、NVIDIA 容器、minimaxai/minimax-m2.7

**版本号**：v0.6.33（待发布）

**下一步**：Hugo 构建 + 安全 rsync + commit + tag + push（macOS 本机执行）

## 2026-05-29｜v0.6.32｜NVIDIA 补全日志与规则一致性整理

### 执行链

- 总控 / 验收：人类用户 + ChatGPT / 剑妈
- 累活整理与规则补账：NVIDIA（Docker Hermes 独立实例）
- 执行环境：Docker 容器（NVIDIA 独立实例）
- 模型后端：NVIDIA API / NIM + Minimax（免费练功房）
- 修改文件：AI_EXECUTION_AGENTS.md、AI_WORK_RULES.md、HERMES_COST_RULES.md、BUILD_HANDOFF.md、SITE_CHANGELOG.md、DAILY_WORK_LOG.md、PROJECT_STATUS.md、hugo-site/data/changelog.yaml
- 是否构建：否
- 是否 rsync：否
- 是否提交：否（待本轮规则补全后统一发布）
- 是否发布：否
- 异常与风险：无

### 今天做了什么（NVIDIA 接手）

本轮 NVIDIA 正式接手 angelife 仓库，执行规则一致性整理与 v0.6.32 日志补全。

**修正错误表述：**
- 将所有治理文件中的"Docker Hermes"独立实例正式命名为"NVIDIA"
- 明确 NVIDIA 是 NVIDIA API / NIM + Minimax 免费练功房，是高 token 累活执行代理
- 明确 NVIDIA 不是总控代理（总控：人类用户 + ChatGPT / 剑妈）
- 明确所有 AI 执行代理同级，无阶级差异，只有工具特长不同
- 明确 NVIDIA 适合：长文档处理、规则整理、日志补账、跨文件一致性检查、低风险治理施工
- 明确 NVIDIA 禁止：git add / commit / tag / push / rsync / Hugo 构建 / 删除文件 / 触碰密钥
- 明确 NVIDIA 是免费练功房，可以大胆学，不可以大胆破坏

**修改文件：**
- `AI_EXECUTION_AGENTS.md` — NVIDIA 完整描述 + 表格式更新 + 核心原则更新
- `AI_WORK_RULES.md` — Docker Hermes → NVIDIA（Docker Hermes）
- `HERMES_COST_RULES.md` — 抬头引用 + §9 NVIDIA 练功房隔离要求 + §10 执行代理同级原则
- `BUILD_HANDOFF.md` — 版本号更新为 v0.6.32 待发布
- `SITE_CHANGELOG.md` — 新增 v0.6.32 版本日志
- `DAILY_WORK_LOG.md` — 新增本条
- `PROJECT_STATUS.md` — 版本更新为 v0.6.32 待发布
- `hugo-site/data/changelog.yaml` — 新增 v0.6.32 公开 changelog 条目

**当前 git status 待发布文件清单（未 commit、待发布）：**
- AI_EXECUTION_AGENTS.md（M）
- AI_WORK_RULES.md（M）
- HERMES_COST_RULES.md（M）
- BUILD_HANDOFF.md（M）
- SITE_CHANGELOG.md（M）
- DAILY_WORK_LOG.md（M）
- PROJECT_STATUS.md（M）
- hugo-site/data/changelog.yaml（M）
- hugo-site/content/about/index.md（M，上轮遗留）
- hugo-site/content/posts/ai-self-distillation-electronic-donkey/index.md（M，上轮遗留）
- hugo-site/content/posts/highway-and-muddy-road-ai-localization/index.md（M，上轮遗留）

**本轮不进行 Hugo 构建，不发布，不 commit，不 tag，不 push。**

**下一步：**
- 等待用户授权后，由指定执行代理使用 `./tools/angelife-release v0.6.32 '<commit message>'` 统一发布本轮所有改动
- 发布前先运行 `git status --short` 确认待发布文件清单

**版本号：**

v0.6.32（待发布）

**当日 AI 成本**

- 模型：NVIDIA API / NIM + Minimax 免费练功房（免费 token）
- 估算 token：高 token 消耗（跨文件规则一致性检查、长文档处理）
- 费用：免费

### v0.6.32 发布前安全规则补全（第二阶段）

**执行链：**
- 总控 / 验收：人类用户 + ChatGPT / 剑妈
- 安全规则补账：NVIDIA（Docker Hermes 独立实例）
- 本机构建与 rsync：macOS 终端手工执行，剑妈实时指挥
- 上轮文章互链：龙虾遗留改动
- 执行环境：Docker 容器（NVIDIA） + macOS 终端（手工）
- 模型后端：NVIDIA API / NIM + Minimax（免费） + DeepSeek（手工终端）

**发现并修复安全 rsync 排除项漏洞：**
- v0.6.32 构建 + rsync 过程中发现原安全 rsync 排除项缺少 .gitignore、.gitmodules、publish.sh、tools/
- rsync 曾将上述文件标记为删除（--delete 模式误删）
- 已由用户执行 git restore 恢复
- 本轮补齐规则：新增 .gitignore、.gitmodules、publish.sh、tools/ 到排除清单

**新增操作署名与追责规则：**
- AI_EXECUTION_AGENTS.md：新增 §13 操作署名与追责规则（执行代理名称、执行环境、模型后端、操作范围、总控与验收、异常追责）
- AI_WORK_RULES.md：新增署名追责规则节
- BUILD_HANDOFF.md：新增接手报告与交接报告执行链格式
- HERMES_COST_RULES.md：明确免费 token 也必须署名留痕

**当前 git status 待发布文件清单（补全后）：**
- AI_EXECUTION_AGENTS.md（M，安全 rsync 排除项 + §13 署名追责）
- AI_WORK_RULES.md（M，署名追责规则节）
- BUILD_HANDOFF.md（M，执行链格式 + 本轮工作说明）
- HERMES_COST_RULES.md（M，免费 token 署名要求）
- SITE_CHANGELOG.md（M，本轮安全规则补全记录）
- DAILY_WORK_LOG.md（M，执行链 + 事故记录）
- PROJECT_STATUS.md（M，安全 rsync 漏洞修复说明）
- hugo-site/data/changelog.yaml（M，新增安全规则补全描述）

**版本号：**

v0.6.32（待发布，已完成构建和 rsync，尚未 commit / tag / push）

## 2026-05-29｜v0.6.31｜增强自费蒸馏文章：新增学徒期小节

### 今天做了什么
- 在「程序员只是第一个样本」后新增「没有学徒期，就没有高级工」完整小节
- 结尾增加插入句
- tags 新增「学徒期」
- 版本从 v0.6.30 顺延至 v0.6.31

## 2026-05-29｜v0.6.29｜更新 about 页面工作流

### 今天做了什么
- 更新 `hugo-site/content/about/index.md` — 由剑妈提供
- 明确文章和图片由 ChatGPT / 剑妈生成
- 明确 Hermes 只负责落盘、接图、构建、rsync、精确 git add、commit/tag/push
- 明确 DeepSeek 只是低成本模型能力
- 明确固定发布流程
- 明确微信认证文件保护
- 版本从 v0.6.28 顺延至 v0.6.29

## 2026-05-29｜v0.6.27｜新增 Hermes 省 Token 执行规则

### 今天做了什么
- 新增 `HERMES_COST_RULES.md`
- 在 `AI_WORK_RULES.md` 接手必读列表中添加引用
- 版本从 v0.6.26 顺延至 v0.6.27

## 2026-05-29｜v0.6.25｜恢复本地静态发布 + 禁用 GitHub Actions 在线构建

### 今天做了什么
- **禁用 GitHub Actions 在线 Hugo 构建**：将 `.github/workflows/hugo.yml` 移至 `docs/disabled-workflows/hugo.yml.disabled`
- 本地 Hugo 构建 → rsync 到仓库根 → commit → push
- 更新版本治理文档
- 版本从 v0.6.24 顺延至 v0.6.25

### 核心规则更新
- 禁止新增 `.github/workflows/hugo.yml` 类在线构建 workflow
- GitHub Pages 必须设置为 "Deploy from a branch" → Branch: master, Folder: / (root)

## 2026-05-29｜v0.6.24｜添加微信域名验证

### 今天做了什么
- 在 `hugo-site/static/` 添加微信域名验证文件 `0847745cb78663855a3a1732c9c6a130.txt`
- 构建 Hugo 并 rsync 到仓库根目录
- 更新版本日志
- 版本从 v0.6.23 顺延至 v0.6.24

## 2026-05-29｜v0.6.23｜发布新文章：自费蒸馏

### 今天做了什么

- 新增文章《自费蒸馏：我们正在花钱训练替代自己的人》
- slug: `ai-self-distillation-electronic-donkey`
- 分类：AI时代
- 标签：AI写作、自我蒸馏、电子驴、失业、判断力、自动化、不失正见
- 封面图已接入：`/images/posts/ai-self-distillation-electronic-donkey/cover.png`
- Hugo 222→223 pages，静态文件 360→361（新增封面图）
- 已通过受控发布脚本发布 v0.6.23

### 修改文件

- `hugo-site/content/posts/ai-self-distillation-electronic-donkey/index.md`（新增）
- `hugo-site/static/images/posts/ai-self-distillation-electronic-donkey/cover.png`（新增）
- `PROJECT_STATUS.md`
- `BUILD_HANDOFF.md`
- `DAILY_WORK_LOG.md`
- `SITE_CHANGELOG.md`
- `hugo-site/data/changelog.yaml`

### 版本号

v0.6.23

### 当日 AI 成本

- 模型：deepseek-v4-flash（Hermes 直接执行）
- 精确 token：未获取
- 费用估算：flash 档位，中等规模

## 2026-05-29｜v0.6.23｜发布新文章：自费蒸馏

### 今天做了什么

- 发布文章《自费蒸馏：我们正在花钱训练替代自己的人》
- slug: `ai-self-distillation-electronic-donkey`，分类：AI时代
- 封面图已接入：`cover.png`（image_ready）
- Hugo 223 pages，361 static files，0 errors
- 已通过受控流程发布 v0.6.23

### 修改文件

- 文章 + 封面图 + 治理文档 + changelog.yaml

### 版本号

v0.6.23

## 2026-05-29｜v0.6.22｜发布新文章：能干的驴

### 今天做了什么

- 新增文章《能干的驴：AI放大能力，但不改变物种》
- slug: `capable-donkey-ai-amplifies-but-does-not-transform`
- 分类：AI时代
- 标签：AI写作、自动化、判断力、技术与规则、不失正见
- 封面状态：cover_status: prompt_ready（未接入封面图）
- 更新 DAILY_WORK_LOG.md、SITE_CHANGELOG.md、hugo-site/data/changelog.yaml、PROJECT_STATUS.md、BUILD_HANDOFF.md
- Hugo 构建验证通过后发布

### 修改文件

- `hugo-site/content/posts/capable-donkey-ai-amplifies-but-does-not-transform/index.md`（新增）
- `PROJECT_STATUS.md`
- `BUILD_HANDOFF.md`
- `DAILY_WORK_LOG.md`
- `SITE_CHANGELOG.md`
- `hugo-site/data/changelog.yaml`

### 构建状态

待 Hugo 构建

### 版本号

v0.6.22

### 当日 AI 成本

- 模型：deepseek-v4-flash（Hermes 直接执行）
- 精确 token：未获取
- 费用估算：flash 档位，规模小

## 2026-05-29｜v0.6.21｜第二阶段：angelife-release --yes 非交互参数

### 今天做了什么（第二阶段，未发布）

- tools/angelife-release：新增 `--yes` 参数，跳过两次确认提示
- 非交互用法：`./tools/angelife-release --yes v0.6.21 "chore: message"`
- 适用于 Hermes Gateway 通过 Telegram 管道调用（避免卡 read）
- 更新 AI_WORK_RULES.md：白名单 + 用法说明
- 更新 BUILD_HANDOFF.md：用法 + --yes 说明
- 更新 PROJECT_STATUS.md：版本号 + 已完成列表
- 更新 DAILY_WORK_LOG.md、SITE_CHANGELOG.md、hugo-site/data/changelog.yaml
- 脚本已 chmod +x（执行位保留）

### 当日 AI 成本

- 模型：deepseek-v4-flash（Hermes 直接执行）
- 估算 token：未获取精确值
- 费用估算：flash 档位，规模小

### 本阶段不发布、不 commit、不 push

## 2026-05-29｜v0.6.20｜第一阶段：新增工具脚本套件

### 今天做了什么（第一阶段，未发布）

- 新增 3 个工具脚本：
  - `tools/angelife-status` — 项目状态概览
  - `tools/angelife-check` — 发布前置检查（含 Kindle 验收）
  - `tools/angelife-cost-log` — AI 成本记录模板
- 更新 `tools/angelife-release` — 集成前置检查调用 + 成本记录占位符优化
- 更新 Hermes 代跑白名单，加入 3 个新脚本
- 更新 BUILD_HANDOFF.md — 版本号 v0.6.20 + 新增脚本套件说明
- 更新 PROJECT_STATUS.md — 版本号 + 已完成列表
- 更新 DAILY_WORK_LOG.md — 新增日志
- 更新 SITE_CHANGELOG.md — 新增 v0.6.20 版本日志
- 更新 hugo-site/data/changelog.yaml — 新增 v0.6.20 公开 changelog
- 所有脚本已 chmod +x

### 当日 AI 成本

- 模型：deepseek-v4-flash（Hermes 直接执行）
- 估算 token：未获取精确值
- 费用估算：flash 档位，规模较小

### 本阶段不发布、不 commit、不 push

## 2026-05-29｜v0.6.19｜加入 AI token 与费用记录制度

### 今天做了什么

- 新增 AI 消耗记录规则到项目治理体系。
- AI_WORK_RULES.md：新增「AI 消耗记录规则」章节，包含记录原则（6 条）、成本优化原则（4 条）、安全红线（2 条）。
- 每轮收工要求新增「AI 消耗记录」条目。
- BUILD_HANDOFF.md：每轮修改要求新增 AI 消耗记录 + DAILY_WORK_LOG 含 AI 成本小节。
- DAILY_WORK_LOG.md：新增「当日 AI 成本」小节。
- PROJECT_STATUS.md：版本号更新至 v0.6.19。
- SITE_CHANGELOG.md、hugo-site/data/changelog.yaml：新增 v0.6.19 日志。
- tools/angelife-release：输出部分新增 AI 消耗记录占位符提示。

### 当日 AI 成本

- 模型：deepseek-v4-flash（当前轮次）
- 估算 token：暂无法获取精确值（DeepSeek 未开放单次会话 token 明细 API）
- 估算费用：使用 flash 模型，成本较低
- 余额差值法：未记录（本轮为治理文档编写，规模较小）

### 修改文件

- `AI_WORK_RULES.md` — 新增 AI 消耗记录规则章节 + 收工报告新增条目
- `BUILD_HANDOFF.md` — 版本号 v0.6.19 + 新增 AI 消耗记录要求
- `DAILY_WORK_LOG.md` — 新增今日日志 + 当日 AI 成本小节
- `PROJECT_STATUS.md` — 版本号更新至 v0.6.19
- `SITE_CHANGELOG.md` — 新增 v0.6.19 版本日志
- `hugo-site/data/changelog.yaml` — 新增 v0.6.19 公开日志
- `tools/angelife-release` — 输出部分新增 AI 消耗占位符

### 核心规则变更

- 每轮 AI 任务必须记录 token 消耗与费用。
- shell 命令不计 token。
- 收工报告新增「AI 消耗记录」条目。
- 不可编造精确 token，无法获取则如实说明。
- Daily 日志增加「当日 AI 成本」小节。
- 建议大任务前后记录 DeepSeek 控制台余额做差值。
- 默认 flash，复杂才用 pro。
- 严禁日志中出现 API key / token 等敏感信息。

### AI 消耗记录

- 模型：deepseek-v4-flash
- 估算 token：未获取精确值（本平台未提供单会话 token 明细）
- 费用估算：flash 档位，治理文档编写规模小

### 构建状态

待执行 Hugo 构建并通过脚本发布。纯治理文档变更，不影响站点内容。

### 版本号

v0.6.19

## 2026-05-29｜v0.6.18｜新增受控发布脚本 tools/angelife-release

### 今天做了什么

- 创建 `tools/angelife-release` 受控发布脚本。
- 脚本内部自动执行：目录检查 → 分支检查 → Hugo 清洁构建 → rsync → 精准 git add → commit → tag → push。
- 明确禁止 `git add .`、禁止提交 `_incoming/` 和 `.reasonix/`。
- 写入 AI_WORK_RULES.md：受控发布脚本规则 + Reasonix/Hermes 发布约束。
- 更新 BUILD_HANDOFF.md：新增受控发布脚本节，标注版本号 v0.6.18。
- 更新 PROJECT_STATUS.md：版本号、已完成项、进行中项、注意事项。
- 更新 SITE_CHANGELOG.md、DAILY_WORK_LOG.md、hugo-site/data/changelog.yaml。
- `chmod +x tools/angelife-release` 已执行。

### 修改文件

- 新增：`tools/angelife-release` — 受控发布脚本
- `AI_WORK_RULES.md` — 新增受控发布脚本规则 + 硬性禁止新增
- `BUILD_HANDOFF.md` — 版本号 v0.6.18 + 新增受控发布脚本说明
- `PROJECT_STATUS.md` — 版本号更新 + 新增受控脚本相关条目
- `SITE_CHANGELOG.md` — 新增 v0.6.18 版本日志
- `DAILY_WORK_LOG.md` — 新增今日日志
- `hugo-site/data/changelog.yaml` — 新增 v0.6.18 公开日志

### 核心规则变更

以后正式发布优先使用 `tools/angelife-release`：
- Reasonix 不直接裸跑 git push/tag。
- Hermes 不自行拼接发布流程。
- 发布权交给用户授权 + 固定脚本。
- Hermes 只负责代跑脚本，不得自行 patch 或修复 Reasonix 输出。

### 构建状态

待执行 Hugo 构建并通过脚本发布。

### 版本号

v0.6.18

## 2026-05-29｜v0.6.17｜更新 about 页以反映当前真实建站工作流

### 今天做了什么

- 完全重写 /about/ 页面，反映当前真实建站工作流。
- Obsidian 不再被表述为深度接入自动化流程（当前不是主流程）。
- Codex 不再被表述为当前主施工流。
- 新增当前真实链路展示：剑妈总编 → 蝉师傅 → Hermes → Reasonix → Hugo → rsync → Git → GitHub Pages。
- 新增角色分工描述：剑妈（总编）、蝉师傅（Telegram 入口）、Hermes（远程总控）、Reasonix（执行工）、DeepSeek（背后模型）、用户（最终决策）。
- 更新 Mermaid 流程图，反映当前真实链路。
- 注明 Obsidian 为未来方向，当前未深度接入。
- 同步更新 PROJECT_STATUS.md、BUILD_HANDOFF.md、SITE_CHANGELOG.md、DAILY_WORK_LOG.md、hugo-site/data/changelog.yaml。
- 确认 .gitignore 已包含 .reasonix/。

### 修改文件

- `hugo-site/content/about.md` — 完全重写 about 页正文
- `PROJECT_STATUS.md` — 版本号更新，已完成列表增加
- `BUILD_HANDOFF.md` — 版本号更新
- `SITE_CHANGELOG.md` — 新增 v0.6.17 版本日志
- `DAILY_WORK_LOG.md` — 新增今日日志
- `hugo-site/data/changelog.yaml` — 新增 v0.6.17 公开日志

### 构建状态

待执行 Hugo 构建。

### 版本号

v0.6.17

### 验收

- about.md 正文已准确反映当前工作流，无误导性描述。

## 2026-05-28 - Hermes / Reasonix 手机远控链路打通与权限边界调整

今日完成：
1. 修复 Telegram bot「蝉师傅」无响应问题。
2. 排查 Hermes gateway 日志，确认早期问题为 Telegram API 连接失败及 Hermes 残留进程干扰。
3. 清理 Hermes 残留进程，重设 Telegram bot token、allowed user ID、home channel ID。
4. 验证 Hermes Gateway 与 Telegram 重新连通。
5. 验证 DeepSeek v4 Flash provider 正常。
6. 发现 launchd 后台启动时 terminal 默认目录仍在 /Users/macos/.hermes/hermes-agent。
7. 改用在 /Users/macos/angelife.github.com 项目目录下前台运行 hermes gateway run --replace。
8. 验证 Telegram 远程 terminal pwd 正确返回 /Users/macos/angelife.github.com。
9. 通过 Hermes 调用 Reasonix 执行 v0.6.14 Kindle 治理固化。
10. 完成 v0.6.15 静态产物收尾同步。
11. 发现 Hermes 在 Reasonix 表示 shell 能力有限后直接接管 shell、git、Hugo、commit、tag、push，形成「总控夺权」风险。
12. 确认最终结果未损坏项目，但需要正式固化 Hermes / Reasonix 分权边界。

经验结论：
Hermes 适合做手机入口、Telegram 网关、远程总控和 terminal 手臂。
Reasonix 适合做项目理解、文件修改、方案判断和代码执行工。
Reasonix 在 headless run / MCP 限制下可能不适合单独完成 shell 收尾。
Hermes 可以代跑 shell，但必须受控，不得夺权。
以后标准分工是：Reasonix 负责「脑」，Hermes 负责「手」，用户负责「授权」。

风险：
Hermes 若不受限制，可能自行 patch、git add、commit、tag、push。
Reasonix 若单独负责全链路，可能在 shell/git/Hugo 阶段卡住。
launchd 后台启动 Hermes 可能不在项目目录，导致找不到项目文件。
Telegram gateway 断连时应优先查 ~/.hermes/logs/gateway.error.log 和 gateway.log。

固化规则：
以后 angelife 项目手机远控任务必须明确：
Hermes 是总控，不得夺权。
主要执行方式：cd /Users/macos/angelife.github.com && reasonix run "任务内容"
如 Reasonix 要求代跑 shell，Hermes 只能执行 Reasonix 明确给出的命令。
禁止 git add .
禁止提交 _incoming/
禁止提交 .reasonix/
禁止覆盖 tag 或强推。

## 2026-05-28｜v0.6.15｜收尾提交：Kindle 治理固化后静态产物同步

### 今天做了什么

- v0.6.14 治理文件变更（AI_WORK_RULES.md、SITE_STYLE_GUIDE.md 等）导致 Hugo 重新生成所有页面。
- 执行 Hugo 清洁构建（223 pages, 0 errors）。
- rsync 全量同步静态产物到仓库根目录。
- 创建 v0.6.15 收尾提交，包含全部静态产物 + 治理文件版本日志更新。
- 推送 master 和 tag v0.6.15。

## 2026-05-28｜v0.6.14｜固化 Kindle 阅读模式治理规则

### 今天做了什么

- 治理固化轮，无模板/CSS/内容变更。
- AI_WORK_RULES.md：新增 Kindle 不可破坏规则 + 验收强制要求。
- SITE_STYLE_GUIDE.md：新增 Kindle 阅读模式独立小节（5 条核心原则）。
- BUILD_HANDOFF.md：新增 Kindle 接手交接确认。
- PROJECT_STATUS.md、SITE_CHANGELOG.md、DAILY_WORK_LOG.md、changelog.yaml 同步更新。

### 修改文件

- `AI_WORK_RULES.md`
- `SITE_STYLE_GUIDE.md`
- `BUILD_HANDOFF.md`
- `PROJECT_STATUS.md`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `hugo-site/data/changelog.yaml`

### 构建状态

Hugo `v0.147.4` 构建通过，223 pages，0 errors。

### 版本号

v0.6.14，tag v0.6.14

### 验收

- Kindle 目录页：无导航词 ✓（此前已固化）
- Kindle 文章页：无导航词和 footer ✓（此前已固化）
- 普通首页：导航完整保留 ✓

## 2026-05-28｜v0.6.13｜修复 Kindle 文章页外层 PaperMod 壳

### 今天做了什么

- 根因：baseof.html 用 `hasPrefix .RelPermalink "/kindle/"` 判断 Kindle 页面，单条件在 KindlePage outputFormat 下偶发不匹配。
- 修复：改为 `$isKindle` 变量，三重判断（RelPermalink / Section / Layout），统一控制 body class、header、footer 渲染。
- 验证：Kindle 文章页和目录页均无导航词和 Powered by。

### 修改文件

- `hugo-site/layouts/_default/baseof.html`
- `SITE_CHANGELOG.md`、`DAILY_WORK_LOG.md`、`PROJECT_STATUS.md`、`BUILD_HANDOFF.md`、`hugo-site/data/changelog.yaml`

### 构建状态

Hugo `v0.147.4` 构建通过，223 pages，0 errors。

### commit / tag / 版本号

- 版本号：v0.6.13
- tag：v0.6.13

## 2026-05-28｜v0.6.12｜重新同步 Kindle 线上静态产物

### 今天做了什么

- 本地 Kindle 模板已正确，但线上 GitHub Pages 有导航残留。
- 执行 `hugo --gc --cleanDestinationDir --minify` 强制清洁构建。
- 全量 rsync 覆盖根目录静态产物。
- 排除 `.reasonix/` 避免 rsync 警告。
- 重新 push 确保线上部署的是完全清洁的 Kindle 产物。

### 验收结果

- Kindle 目录/文章页：无导航词、无 Powered by、无 id=menu ✓
- 普通页面：导航完整保留 ✓

### 修改文件

- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `PROJECT_STATUS.md`
- `BUILD_HANDOFF.md`
- `hugo-site/data/changelog.yaml`

### 构建状态

Hugo `v0.147.4` 构建通过，223 pages，0 errors。

### commit / tag / 版本号

- 版本号：v0.6.12
- tag：v0.6.12

## 2026-05-28｜v0.6.11｜Kindle/手机自动跳转 + 双版本规则固化

### 今天做了什么

- 创建 `reader-redirect.js`：Kindle 设备/手机用户自动跳转 Kindle 阅读版。
- 条件加载脚本：仅非 Kindle 页面加载，Kindle 页面不重复加载。
- `?normal=1` 出口：Kindle 页面可返回图文版，记录偏好后不再自动跳走。
- `?reader=1`/`?kindle=1` 入口：可强制进入阅读模式。
- 更新 Kindle 模板页脚：文章页增加「本文图文版」链接，目录页增加「返回首页图文版」。
- 固化双版本发布规则到 `AI_WORK_RULES.md`、`SITE_STYLE_GUIDE.md`、`BUILD_HANDOFF.md`。
- 更新公开 changelog、内部详细日志、项目状态。

### 验收结果

- Kindle 页面无普通导航 ✓
- 普通页面保留完整导航 ✓
- JS 已部署到 /js/reader-redirect.js ✓
- 正常页面已加载脚本 ✓
- /kindle/ 和 /kindle/posts/<slug>/ 均可打开 ✓

### 修改文件

- 新增：`hugo-site/static/js/reader-redirect.js`
- 修改：`hugo-site/layouts/partials/extend_head.html`
- 修改：`hugo-site/layouts/_default/single.kindle.html`
- 修改：`hugo-site/layouts/kindle/list.html`
- 修改：`AI_WORK_RULES.md`、`SITE_STYLE_GUIDE.md`、`BUILD_HANDOFF.md`、`PROJECT_STATUS.md`
- 修改：`SITE_CHANGELOG.md`、`DAILY_WORK_LOG.md`、`hugo-site/data/changelog.yaml`

### 构建状态

Hugo `v0.147.4` 构建通过，223 pages，0 errors。

### commit / tag / 版本号

- 版本号：v0.6.11
- tag：v0.6.11

## 2026-05-28｜v0.6.10｜Kindle 阅读模式细化：模板层移除导航

### 今天做了什么

- 修改 `baseof.html`：Kindle 页面跳过 PaperMod 完整导航和页脚渲染。
- Kindle 文章页模板和目录页模板加入简约顶栏：`安知生 angelife ／ Kindle 阅读版`。
- 页脚改为纯文字极简版权 + 返回链接。
- 清理 `kindle.css`：删除不再使用的 `.footer` 和重复的 `.kindle-footer` 样式。

### 验收结果

- Kindle 目录页和文章页源代码中无 `id=menu`、无 `nav`、无导航词。
- 普通页面导航完整保留。

### 修改文件

- `hugo-site/layouts/_default/baseof.html`
- `hugo-site/layouts/_default/single.kindle.html`
- `hugo-site/layouts/kindle/list.html`
- `hugo-site/static/css/kindle.css`
- 日志/治理文件

### 构建状态

Hugo `v0.147.4` 构建通过，223 pages，0 errors。

### commit / tag / 版本号

- 版本号：v0.6.10
- tag：v0.6.10

## 2026-05-28｜v0.6.9｜重构为独立 Kindle 电子书阅读模式

### 今天做了什么

- 将 Kindle 模式从"网页兼容"重构为"独立电子书阅读模式"。
- 使用 Hugo output format 为每篇文章自动生成独立 Kindle 文章页 `/kindle/posts/<slug>/`。
- 创建 `layouts/_default/single.kindle.html`：纯文字、无封面、无标签、无分享、无评论，只有标题+日期+正文+上一篇/下一篇。
- 创建 `layouts/kindle/list.html`：纯文字文章目录，链接到 Kindle 独立文章页。
- 创建 `layouts/_default/baseof.html`：通过 `hasPrefix .RelPermalink "/kindle/"` 自动注入 `body.kindle-mode`。
- 完全重写 `static/css/kindle.css`：使用 `body.kindle-mode` 选择器，serif 字体，强制去掉所有装饰。
- 更新 `hugo.toml`、`content/posts/_index.md` cascade 配置。

### 做到什么程度

Kindle 阅读模式从"微调兼容"变成了"独立电子书入口"：
- 目录页像 Kindle 书架
- 文章页像纯电子书正文
- 所有 Kindle 页面自动带 `kindle-mode` class

### 遇到什么问题

- `.OutputFormat.Name` 在 Hugo v0.147 的某些 page 类型中不可用，改用 `.RelPermalink` 前缀判断。
- `layouts/section/kindle.html` 未被 Hugo 识别，移至 `layouts/kindle/list.html` 后正常。

### 已解决什么

- 独立 Kindle 文章页正常渲染，目录链接指向 Kindle 文章页。

### 未完成什么

- 无。

### 修改文件

- 新增：`hugo-site/layouts/_default/single.kindle.html`
- 新增：`hugo-site/layouts/kindle/list.html`
- 新增：`hugo-site/layouts/_default/baseof.html`
- 修改：`hugo-site/static/css/kindle.css`
- 修改：`hugo-site/content/kindle/_index.md`
- 修改：`hugo-site/content/posts/_index.md`
- 修改：`hugo-site/hugo.toml`
- 修改：`SITE_CHANGELOG.md`、`DAILY_WORK_LOG.md`、`PROJECT_STATUS.md`、`BUILD_HANDOFF.md`、`hugo-site/data/changelog.yaml`

### 构建状态

Hugo `v0.147.4` 构建通过，223 pages，0 errors。

### 发布状态

已按固定方式执行 rsync，根目录静态产物已更新。

### commit / tag / 版本号

- 版本号：v0.6.9
- commit：提交后以 tag `v0.6.9` 指向的 release commit 为准
- tag：v0.6.9

## 2026-05-28｜v0.6.8｜新增 Kindle Paperwhite 阅读模式

### 今天做了什么

- 为 angelife 网站增加 Kindle KPW5 / 电子墨水屏阅读优化模式。
- 新增 `/kindle/` 入口：文章列表按日期倒序，无封面大图，黑白高对比。
- 创建 `hugo-site/static/css/kindle.css`，通过 `@media (monochrome)` 条件激活全站 Kindle 优化。
- 创建 `hugo-site/layouts/section/kindle.html` 作为 `/kindle/` 页面模板。
- 创建 `hugo-site/content/kindle/_index.md` 内容页。
- 在 `hugo.toml` 主导航增加「Kindle版」条目。
- 在 `extend_head.html` 中加载 `kindle.css`。

### 做到什么程度

Kindle 阅读模式已创建并发布。普通桌面端、手机端不受影响。

### 遇到什么问题

- 最初将模板放在 `layouts/page/` 目录，但 `content/kindle/_index.md` 是 section 类型。将模板移到 `layouts/section/` 后正常渲染。

### 已解决什么

- Kindle 页面已正常生成，包含 9 篇文章列表。

### 未完成什么

- 无。

### 修改文件

- 新增：`hugo-site/content/kindle/_index.md`
- 新增：`hugo-site/layouts/section/kindle.html`
- 新增：`hugo-site/static/css/kindle.css`
- 修改：`hugo-site/hugo.toml`
- 修改：`hugo-site/layouts/partials/extend_head.html`
- 修改：`SITE_CHANGELOG.md`
- 修改：`DAILY_WORK_LOG.md`
- 修改：`PROJECT_STATUS.md`
- 修改：`BUILD_HANDOFF.md`
- 修改：`hugo-site/data/changelog.yaml`

### 构建状态

Hugo `v0.147.4` 构建通过，215 pages，0 errors。

### 发布状态

已按固定方式执行 rsync，根目录静态产物已更新。

### commit / tag / 版本号

- 版本号：v0.6.8
- commit：提交后以 tag `v0.6.8` 指向的 release commit 为准
- tag：v0.6.8

## 2026-05-28｜v0.6.7｜发布机器执行文章并修复 404

### 今天做了什么

- 将长期滞留于 untracked 状态的文章《机器执行，经验指挥：AI 时代真正昂贵的东西》正式纳入 git 跟踪并发布上线。
- 修复线上 `/posts/ai-machine-executes-experience-commands/` 404 问题。
- 文章源文件 front matter 已确认：draft: false，slug、title、categories、tags 均正常。
- 封面状态记录为 `cover_status: prompt_ready`，未写入 front matter cover 字段。
- 更新公开 changelog、内部详细日志、每日工作日志、交接日志和项目状态文件。

### 做到什么程度

文章已正式发布，线上 404 已修复。

### 遇到什么问题

- 文章源文件长期存在于 content 目录中，但从未 `git add` 和 `git commit`，导致 Hugo 构建时包含该页，但 GitHub Pages 部署的 git 仓库中不存在该文件。

### 已解决什么

- 已将该文章纳入 git 跟踪，按既定流程完成构建、rsync、commit、tag、push。

### 未完成什么

- 封面图待 ChatGPT 生成后接入。

### 下一个 AI 应该从哪里接手

先读 `PROJECT_STATUS.md` 和 `AI_WORK_RULES.md`。本轮文章已正式发布，`_incoming/` 不纳入提交范围。

### 修改文件

- `hugo-site/content/posts/ai-machine-executes-experience-commands/index.md`
- `posts/ai-machine-executes-experience-commands/index.html`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `PROJECT_STATUS.md`
- `BUILD_HANDOFF.md`
- `hugo-site/data/changelog.yaml`

### 构建状态

Hugo `v0.147.4` 构建通过，213 pages，0 errors。

### 发布状态

已按固定方式执行 rsync，根目录静态产物已更新。`_incoming/` 不纳入提交范围。

### commit / tag / 版本号

- 版本号：v0.6.7
- commit：提交后以 tag `v0.6.7` 指向的 release commit 为准
- tag：v0.6.7

## 2026-05-28｜v0.6.6｜接入高速公路与泥巴地文章封面图

### 今天做了什么

- 将 ChatGPT 生成的封面图接入已发布的《高速公路与泥巴地：AI时代的本土化生存》。
- 拷贝封面图到 `hugo-site/static/images/posts/highway-and-muddy-road-ai-localization/cover.png`。
- 更新 front matter 接入 `cover` 字段：图片路径、alt 文本、caption。
- 更新视觉资产记录为 `cover_status: image_ready`。
- 更新公开 changelog、内部详细日志、每日工作日志、交接日志和项目状态文件。

### 做到什么程度

文章封面图已正式接入，作为 `v0.6.6` 发布。

### 遇到什么问题

- 无。

### 已解决什么

- 封面图已成功部署，Hugo 构建 213 pages, 0 errors。

### 未完成什么

- commit、push、tag 和线上验证在后续步骤完成后补入最终收工报告。

### 下一个 AI 应该从哪里接手

先读 `PROJECT_STATUS.md` 和 `AI_WORK_RULES.md`。本轮封面图已接入发布，`_incoming/` 不纳入提交范围。

### 修改文件

- `hugo-site/static/images/posts/highway-and-muddy-road-ai-localization/cover.png`
- `hugo-site/content/posts/highway-and-muddy-road-ai-localization/index.md`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `PROJECT_STATUS.md`
- `BUILD_HANDOFF.md`
- `hugo-site/data/changelog.yaml`

### 构建状态

Hugo `v0.147.4` 构建通过，213 pages，0 errors。静态文件 358。

### 发布状态

已按固定方式执行 rsync，根目录静态产物已更新。

### commit / tag / 版本号

- 版本号：v0.6.6
- commit：提交后以 tag `v0.6.6` 指向的 release commit 为准
- tag：v0.6.6

## 2026-05-28｜v0.6.5｜发布高速公路与泥巴地文章

## 2026-05-28｜v0.6.4｜接入付费墙与迷雾墙文章封面图

### 今天做了什么

- 将 ChatGPT 生成的封面图接入已发布的《付费墙与迷雾墙：AI时代真正昂贵的是判断》。
- 拷贝封面图到 `hugo-site/static/images/posts/paywall-and-mist-wall/cover.png`。
- 更新 front matter 接入 `cover` 字段：图片路径、alt 文本、caption。
- 更新视觉资产记录为 `cover_status: image_ready`。
- 更新公开 changelog、内部详细日志、每日工作日志、交接日志和项目状态文件。

### 做到什么程度

文章封面图已正式接入，作为 `v0.6.4` 发布。

### 遇到什么问题

- `~` 在 run_command 中未展开为 home 目录，改用完整路径 `/Users/macos/Downloads/` 后正常。

### 已解决什么

- 封面图已成功部署，Hugo 构建 206 pages, 0 errors。

### 未完成什么

- commit、push、tag 和线上验证在后续步骤完成后补入最终收工报告。

### 下一个 AI 应该从哪里接手

先读 `PROJECT_STATUS.md` 和 `AI_WORK_RULES.md`。本轮封面图已接入发布，`_incoming/` 不纳入提交范围。

### 修改文件

- `hugo-site/static/images/posts/paywall-and-mist-wall/cover.png`
- `hugo-site/content/posts/paywall-and-mist-wall/index.md`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `PROJECT_STATUS.md`
- `BUILD_HANDOFF.md`
- `hugo-site/data/changelog.yaml`

### 构建状态

Hugo `v0.147.4` 构建通过，206 pages，0 errors。静态文件 357。

### 发布状态

已按固定方式执行 rsync，根目录静态产物已更新。

### commit / tag / 版本号

- 版本号：v0.6.4
- commit：提交后以 tag `v0.6.4` 指向的 release commit 为准
- tag：v0.6.4

## 2026-05-28｜v0.6.3｜发布付费墙与迷雾墙文章

### 今天做了什么

- 将用户提供的《付费墙与迷雾墙：AI时代真正昂贵的是判断》整理为 Hugo 正式文章。
- 按 slug `paywall-and-mist-wall` 创建文章 bundle。
- 归入 `AI时代`。
- 添加 `AI写作`、`判断力`、`规则意识`、`现实规则`、`不失正见` 标签。
- 更新公开 changelog、内部详细日志、每日工作日志、交接日志和项目状态文件。

### 做到什么程度

文章已进入正式发布流，作为公开长文发布，不放入 `_incoming/`。

### 遇到什么问题

- 无。

### 已解决什么

- 按既定流程完成构建、rsync、日志更新。

### 未完成什么

- commit、push、tag 和线上验证在后续步骤完成后补入最终收工报告。

### 下一个 AI 应该从哪里接手

先读 `PROJECT_STATUS.md` 和 `AI_WORK_RULES.md`。本轮文章已经正式发布，不需要再从 `_incoming/` 处理。

### 修改文件

- `hugo-site/content/posts/paywall-and-mist-wall/index.md`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `PROJECT_STATUS.md`
- `BUILD_HANDOFF.md`
- `hugo-site/CODEX_HANDOFF.md`
- `hugo-site/data/changelog.yaml`

### 构建状态

Hugo `v0.147.4` 构建通过，206 pages，0 errors。

### 发布状态

已按固定方式执行 rsync，根目录静态产物已更新。`_incoming/` 不纳入提交范围。

### commit / tag / 版本号

- 版本号：v0.6.3
- commit：提交后以 tag `v0.6.3` 指向的 release commit 为准
- tag：v0.6.3

## 2026-05-28｜v0.6.2｜发布 AI 时代经验瓶颈文章

### 今天做了什么

- 将用户提供的《AI时代，经验才是最大的瓶颈》整理为 Hugo 正式文章。
- 按建议 slug 创建文章 bundle：`ai-era-experience-is-the-bottleneck`。
- 归入 `火·AI`、`AI时代`。
- 添加 `AI`、`经验`、`判断力`、`信息筛选`、`方法论`、`个人知识系统` 标签。
- 使用 imagegen 生成并接入文章封面图。
- 更新公开 changelog、内部详细日志、每日工作日志、交接日志和项目状态文件。

### 做到什么程度

文章已进入正式发布流，作为公开长文发布，不放入 `_incoming/`，也不作为未发布储备稿处理。

### 遇到什么问题

- 默认 Codex 工作目录为空且不是 Git 仓库，需要重新定位到 `/Users/macos/angelife.github.com`。
- 实际仓库不在当前 writable sandbox root 内，写入时需要按权限流程执行。
- 文章初始发布时间写在本机当前时间之后，Hugo 未将其输出；已改为 `2026-05-28T12:40:00+08:00`。

### 已解决什么

- 已确认 angelife 仓库、Hugo 源站、发布脚本、版本规则和日志要求。
- 已按 SemVer 规则生成本轮版本号 `v0.6.2`。
- 已按当前文章格式保留 front matter 标题，正文不重复插入一级标题。

### 未完成什么

- commit、push、tag 和线上验证在后续步骤完成后补入最终收工报告。

### 下一个 AI 应该从哪里接手

先读 `PROJECT_STATUS.md` 和 `AI_WORK_RULES.md`。本轮文章已经正式发布，不需要再从 `_incoming/` 处理。

### 修改文件

- `BUILD_HANDOFF.md`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `PROJECT_STATUS.md`
- `hugo-site/CODEX_HANDOFF.md`
- `hugo-site/data/changelog.yaml`
- `hugo-site/content/posts/ai-era-experience-is-the-bottleneck/index.md`
- `hugo-site/content/posts/ai-era-experience-is-the-bottleneck/cover.png`

### 构建状态

Hugo `v0.147.4` 构建通过，192 pages，0 errors。

### 发布状态

已按固定方式执行 `./publish.sh`，根目录静态产物已更新。`_incoming/` 不纳入提交范围。

### commit / tag / 版本号

- 版本号：v0.6.2
- commit：提交后以 tag `v0.6.2` 指向的 release commit 为准
- tag：v0.6.2

## 2026-05-28｜v0.6.1｜发布 ChatGPT 高反馈系统文章

### 今天做了什么

- 将用户提供的《和 ChatGPT 在一起，我重新找回了天天进步的感觉》整理为 Hugo 正式文章。
- 按建议 slug 创建文章 bundle：`chatgpt-daily-progress-feedback-system`。
- 归入 `火·AI`、`日课`、`AI时代`、`个人知识资产`。
- 添加 `ChatGPT`、`AI陪练`、`个人成长`、`高反馈环境`、`知识系统` 标签。
- 使用 imagegen 生成并接入文章封面图。
- 修正 `publish.sh` 排除清单，防止发布时误删根目录治理文档和站点校验 txt 文件。
- 更新公开 changelog、内部详细日志、每日工作日志、交接日志和项目状态文件。

### 做到什么程度

文章已进入正式发布流，作为公开长文发布，不放入 `_incoming/`，也不作为未发布储备稿处理。

### 遇到什么问题

- 默认 Codex 工作目录为空且不是 Git 仓库，需要重新定位到 `/Users/macos/angelife.github.com`。
- 首次运行发布脚本后发现 `rsync --delete` 会删除根目录治理文档，需要补充排除项。
- 文章初始发布时间写在本机当前时间之后，Hugo 未将其输出；已改为 `2026-05-28T12:20:00+08:00`。

### 已解决什么

- 已确认 angelife 仓库、Hugo 源站、发布脚本、版本规则和日志要求。
- 已按 SemVer 规则生成本轮版本号 `v0.6.1`。
- 已恢复根目录治理文档，并更新 `publish.sh` 防止后续重复误删。

### 未完成什么

- commit、push、tag 和线上验证在后续步骤完成后补入最终收工报告。

### 下一个 AI 应该从哪里接手

先读 `PROJECT_STATUS.md` 和 `AI_WORK_RULES.md`。本轮文章已经正式发布，不需要再从 `_incoming/` 处理。

### 修改文件

- `BUILD_HANDOFF.md`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `PROJECT_STATUS.md`
- `publish.sh`
- `hugo-site/CODEX_HANDOFF.md`
- `hugo-site/data/changelog.yaml`
- `hugo-site/content/posts/chatgpt-daily-progress-feedback-system/index.md`
- `hugo-site/content/posts/chatgpt-daily-progress-feedback-system/cover.png`

### 构建状态

Hugo `v0.147.4` 构建通过，183 pages，0 errors。

### 发布状态

已按固定方式执行 `./publish.sh`，根目录静态产物已更新。`_incoming/` 已加入脚本排除项，未纳入提交范围。

### commit / tag / 版本号

- 版本号：v0.6.1
- commit：提交后以 tag `v0.6.1` 指向的 release commit 为准
- tag：v0.6.1

## 2026-05-27｜v0.6.0｜改用 SemVer、增强搜索并预留 GitHub 评论

### 今天做了什么

- 将版本号规则从日期流水切换为 SemVer。
- 增强 `/search/`：命中词高亮、上下文摘要、无结果提示、排序优化。
- 搜索索引增加 `description`，继续覆盖标题、摘要、正文、分类、标签和链接。
- 预留 giscus 评论系统，默认隐藏，等待 GitHub Discussions 和 giscus 参数。
- 检查流程图候选路径，未找到图片，`/site-workflow/` 保留 TODO。
- 同步更新公开 changelog、内部日志、每日工作日志和项目总控进度。

### 做到什么程度

功能增强层完成。搜索可作为知识库入口使用，评论系统已具备安全预留结构，SemVer 规则已进入治理文档。

### 遇到什么问题

- 未找到项目总控流程图素材。
- giscus 缺少 `repoId` / `categoryId`，不能正式显示评论区。

### 已解决什么

- 以 `v0.6.0` 作为 SemVer 起点。
- giscus 默认 `enabled = false`，缺少必要参数时不会显示空白评论区。
- 搜索可显示高亮和上下文。

### 未完成什么

- 接入 `hugo-site/static/images/workflow/site-control-map.png`。
- 用户开启 GitHub Discussions、安装/授权 giscus 后，填写 `repoId` / `categoryId` 并按文章开启 `comments: true`。

### 下一个 AI 应该从哪里接手

先读 `PROJECT_STATUS.md`，再按 `AI_WORK_RULES.md` 的必读清单阅读全部交接文件。评论正式启用前，先确认 GitHub Discussions 和 giscus 参数。

### 修改文件

- `BUILD_HANDOFF.md`
- `AI_WORK_RULES.md`
- `SITE_STYLE_GUIDE.md`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `PROJECT_STATUS.md`
- `hugo-site/data/changelog.yaml`
- `hugo-site/content/site-workflow.md`
- `hugo-site/layouts/_default/index.json`
- `hugo-site/layouts/_default/search.html`
- `hugo-site/layouts/partials/comments.html`
- `hugo-site/static/css/angelife-brand.css`
- `hugo-site/hugo.toml`

### 构建状态

Hugo `v0.147.4` 构建通过，174 pages，0 errors。

### 发布状态

已按固定方式执行 `rsync -av hugo-site/public/ ./`，根目录静态产物已更新。

### commit / tag / 版本号

- 版本号：v0.6.0
- commit：提交后以 tag `v0.6.0` 指向的 release commit 为准
- tag：v0.6.0

## 2026-05-27｜v2026.05.27-05｜建立统一 AI 接手规范与项目进度体系

### 今天做了什么

- 建立建站交接手册 `BUILD_HANDOFF.md`。
- 建立统一 AI 工作规则 `AI_WORK_RULES.md`。
- 建立网站风格规范 `SITE_STYLE_GUIDE.md`。
- 建立内部详细版本日志 `SITE_CHANGELOG.md`。
- 建立每日/每轮工作日志 `DAILY_WORK_LOG.md`。
- 建立项目总控进度视图 `PROJECT_STATUS.md`。
- 建立公开更新日志数据 `hugo-site/data/changelog.yaml`。
- 建立公开 `/changelog/` 页面。
- 建立公开 `/site-workflow/` 建站模式日志页面。
- 顶部导航增加“更新”入口。

### 做到什么程度

治理层第一版完成，可供下一个 AI 接手时快速理解发布方式、禁止事项、风格边界、当前进度和回退方法。

### 遇到什么问题

- Git commit hash 无法预先写入被提交文件。
- 尚未找到用户提到的“网站项目总控流程可视化图.png”。

### 已解决什么

- 以 Git tag 作为文档内稳定可回退锚点。
- `/site-workflow/` 先保留流程图 TODO，不阻塞构建和发布。

### 未完成什么

- 补充并接入 `hugo-site/static/images/workflow/site-control-map.png`。
- 后续版本继续细化公开 changelog 展示。

### 下一个 AI 应该从哪里接手

先读 `PROJECT_STATUS.md`，再按 `AI_WORK_RULES.md` 的必读清单阅读全部交接文件。

### 修改文件

- `BUILD_HANDOFF.md`
- `AI_WORK_RULES.md`
- `SITE_STYLE_GUIDE.md`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `PROJECT_STATUS.md`
- `hugo-site/data/changelog.yaml`
- `hugo-site/content/changelog.md`
- `hugo-site/content/site-workflow.md`
- `hugo-site/layouts/_default/changelog.html`
- `hugo-site/hugo.toml`

### 构建状态

Hugo `v0.147.4` 构建通过，174 pages，0 errors。

### 发布状态

已按固定方式执行 `rsync -av hugo-site/public/ ./`，根目录静态产物已更新。

### commit / tag / 版本号

- 版本号：v2026.05.27-05
- commit：提交后以 tag `v2026.05.27-05` 指向的 release commit 为准
- tag：v2026.05.27-05
