# AI 执行代理统一规则

本文件适用于 angelife Hugo 网站项目中所有 AI 执行代理，包括但不限于：

- OpenClaw / 龙虾
- Hermes / Hermers
- Reasonix
- Codex
- Claude Code
- 其他未来接入的 AI 工具

## 1. 身份定位

所有 AI 执行代理都是同一类工具：AI execution agents。

它们没有阶级高低，没有"谁更高级、谁更低级"的固定身份。

区别只在于：

- 界面不同；
- 模型后端不同；
- 成本不同；
- 稳定性不同；
- 手机端/远程控制便利性不同；
- 长会话、代码修改、文件操作、可视化观察等特长不同。

选择哪个代理上场，取决于当前任务最适合谁，而不是工具阶级。

## 2. 统一工地

所有执行代理默认工作在同一个本地仓库：

/Users/macos/angelife.github.com

在 Docker / OpenClaw 容器内，对应路径可能是：

/home/node/.openclaw/workspace/angelife.github.com

不得各自创建一套独立流程、独立目录、独立发布方式。

## 3. 统一法度

所有执行代理接手前必须先读取：

- PROJECT_STATUS.md
- BUILD_HANDOFF.md
- AI_WORK_RULES.md
- HERMES_COST_RULES.md
- AI_EXECUTION_AGENTS.md
- SITE_STYLE_GUIDE.md
- SITE_CHANGELOG.md
- DAILY_WORK_LOG.md

如果这些文件之间有冲突，以用户和 ChatGPT / 剑妈的最新明确指令为准，并停止等待确认。

## 4. 总控关系（v0.7.14 更新）

**NVIDIA（Docker Hermes）是总控，独立维护 angelife 网站。**

人类用户负责：
- 最终验收（所有 push 必须用户确认）
- 方向否决权

AI 执行代理（龙虾 / Hermes / Reasonix / Codex / Claude Code）负责：
- 文件操作
- 内容整理
- Hugo 源文件修改
- 本地构建；
- rsync；
- 精确 git add；
- commit；
- tag；
- push。

但发布动作必须在用户明确授权后执行。

## 5. 同一时间只能一个代理操作仓库

不得多个 AI 执行代理同时操作同一个仓库。

正确流程：

当前代理接手
→ 读取规则
→ 执行任务
→ 输出改动报告
→ 停止等待确认
→ 下一个代理再接手

禁止多个代理并发修改同一批文件。

## 6. 固定发布流程

angelife 网站固定发布方式是：

本地 Hugo 构建
→ 安全 rsync 到仓库根目录
→ 更新日志和版本文件
→ 精确 git add
→ commit
→ tag
→ push commit + tag

GitHub Pages 必须保持：

Deploy from branch / master / root

禁止恢复 GitHub Actions 在线 Hugo 构建。

## 7. 内容流程

本地文本库 / Emacs 是草稿炉。

angelife Hugo 网站是成品库。

网站只发定稿。

日常碎片、半成品、小补充、相似观点，应先在本地文本库 / Emacs 或本地文件中整理、合并、打磨。

观念雷同，只合并，不另开。

只有具备独立主论点、独立结构、独立读者价值时，才新开文章。

## 8. 执行代理可做事项

执行代理可以：

- 读取项目规则；
- 读取 Hugo 正式文章；
- 读取本地文本库 / Emacs 草稿；
- 判断相似观点应并入哪篇旧文；
- 修改 Hugo 源文件；
- 修正 front matter、标签、分类；
- 增强旧文；
- 更新本地说明文档；
- 执行本地 Hugo 构建；
- 在用户明确授权发布时执行 rsync、commit、tag、push。

## 9. 永久禁止事项

禁止：

- git add .
- git init
- git pull
- git merge
- git rebase
- git reset --hard
- rm -rf
- 删除文件
- 提交 _incoming/
- 删除或破坏 .git/
- 删除或破坏 .github/
- 删除或破坏 hugo-site/
- 恢复 .github/workflows/hugo.yml
- 启用 GitHub Actions 在线 Hugo 构建
- 未经确认重写整篇文章
- 未经确认发布网站
- 多个执行代理同时操作仓库

## 10. 微信认证文件保护

微信认证文件必须永久保护。

源文件：

hugo-site/static/0847745cb78663855a3a1732c9c6a130.txt

仓库根目录文件：

0847745cb78663855a3a1732c9c6a130.txt

内容必须保持：

01413348ab0d5b381a2e7099ba2600ed57ad50d3

线上必须保持可访问：

https://angelife.github.io/0847745cb78663855a3a1732c9c6a130.txt

任何构建、rsync、清理、发布，都不得删除或覆盖该文件。

## 11. 安全 rsync

禁止使用裸 rsync：

rsync -av hugo-site/public/ ./

正式发布必须使用安全排除规则，必须同时排除：

- .git/（Git 元数据目录）
- .github/（GitHub Actions 等配置文件）
- hugo-site/（Hugo 源目录，不应同步到根目录）
- _incoming/（临时素材区，禁止发布）
- docs/（文档目录）
- tools/（发布脚本目录，禁止同步产物）
- PROJECT_STATUS.md
- BUILD_HANDOFF.md
- AI_WORK_RULES.md
- HERMES_COST_RULES.md
- AI_EXECUTION_AGENTS.md
- SITE_STYLE_GUIDE.md
- SITE_CHANGELOG.md
- DAILY_WORK_LOG.md
- README.md
- LICENSE
- .gitignore（项目 Git 忽略规则）
- .gitmodules（Git 子模块配置）
- publish.sh（发布脚本）
- 0847745cb78663855a3a1732c9c6a130.txt
- .DS_Store

**必须保护：**
- Git 元数据（.git/、.gitignore、.gitmodules）
- 发布脚本（tools/、publish.sh）
- 微信认证文件（0847745cb78663855a3a1732c9c6a130.txt）
- Hugo 源目录（hugo-site/）

**禁止：**
- 裸 rsync：`rsync -av hugo-site/public/ ./`
- 未带完整排除项的 rsync --delete

## 12. 小改不单独发布

小改、互链、标签修正、轻量补充，不单独发布。

应保留为本地待发布改动，等形成一批成熟改动后，再统一构建、rsync、commit、tag、push。

## 13. 操作署名与追责规则

每一轮 AI 执行代理接手 angelife 仓库，必须在工作报告、发布报告或 DAILY_WORK_LOG 中明确记录以下信息：

**1. 执行代理名称**
必须写清楚具体是哪个 AI 在操作，不接受匿名施工：
- 龙虾 / OpenClaw
- 蝉师傅 / 本机 Hermes
- NVIDIA（Docker Hermes 独立实例）
- Reasonix
- Codex
- Claude Code
- 或其他实际工具名称

**2. 执行环境**
- macOS 本机
- Docker 容器
- OpenClaw 容器
- Telegram 远控
- 手工终端
- 其他实际环境

**3. 模型或后端**
- DeepSeek
- NVIDIA API / NIM + Minimax
- OpenAI
- Claude
- 或其他实际模型后端

**4. 操作范围**
必须记录：
- 修改了哪些文件（精确到文件名）
- 是否 Hugo 构建
- 是否 rsync
- 是否 git add
- 是否 commit
- 是否 tag
- 是否 push
- 是否发布线上

**5. 总控与验收**
- 总控：人类用户 + ChatGPT / 剑妈
- 执行代理只负责施工，不得自行发布
- 最终是否发布由人确认

**6. 异常追责**
如果发生误删、错改、漏记、误发布、路径污染、密钥泄露、bot 冲突、rsync 误删等问题，必须能从 DAILY_WORK_LOG、SITE_CHANGELOG、BUILD_HANDOFF 或发布报告中追溯到当轮执行代理和具体动作。

**禁止：**
- 匿名施工（只写"已完成"而不写执行者）
- 多个代理共同操作但不区分责任
- 事后补日志（当天不记录，事后补录）

## 14. 工具特长与当前推荐用法

以下描述各 AI 执行代理的工具特长和当前推荐任务场景。
所有代理无阶级差异，只有工具特长、成本、稳定性、界面和模型后端差异。
谁适合当前任务，谁上场。实践出真知，边用边学，边用边掌握工具特点。

### OpenClaw / 龙虾

**当前定位**：逐步承担 Codex 过去在 angelife 项目中的主力成熟执行代理位置。

**推荐场景**：
- 网页可视化项目改造（CSS/HTML/JS）
- 长会话复杂任务拆解与执行
- 真实仓库施工、项目建设干中学
- 需要较强模型推理能力的复杂架构修改

### Hermes

**当前定位**：适合利用免费或低成本 token，做真实项目中的长期练功、自我学习、流程试错、规则复盘、技能沉淀、低风险治理施工。

**推荐场景**：
- 规则文档的整理、修正、一致性检查
- 多文件联动检查（跨文件一致性审查）
- 低成本探索式学习（新工具试用、新流程验证）
- 规则复盘与流程优化建议
- 小批量规则文件的本地修改（不触发 rsync/push）

### NVIDIA（Docker Hermes 独立实例）

**当前定位**：Docker Hermes 正式命名为 NVIDIA。作为 angelife 项目的正式 AI 执行代理之一，NVIDIA 是 NVIDIA API / NIM + Minimax 免费练功房，使用高 token 长文档处理能力，适合做高 token 消耗、长文档、重复检查、日志补账、规则一致性整理等累活。

NVIDIA 不是总控，不是军师，不是写作代理。人类用户 + ChatGPT / 剑妈是总控。NVIDIA 是高 token / 免费 token 累活执行代理，适合长文档复盘、跨文件一致性检查、治理整理和低风险施工。

本机 Hermes / 蝉师傅的旧配置（DeepSeek / Telegram 蝉师傅）不得被 NVIDIA 污染。

**推荐场景**：
- 高 token 消耗的长文档处理（跨文件规则一致性检查、日志补账）
- 重复检查类累活（对照多个文件找不一致）
- 规则整理（修法度、补日志、写 changelog）
- 练功和自我学习（NVIDIA 使用免费或极低成本模型）
- 规则施工后的隔离验证

**NVIDIA 可做**：
- 大胆探索、复盘、总结、规则整理
- 读取项目规则、检查一致性
- 低风险治理施工（修改规则文档、补全日志）
- 高 token 长文档处理

**NVIDIA 禁止**：
- git add / git commit / git tag / git push
- rsync / Hugo 构建（除非用户明确授权做验收检查）
- 删除文件
- 修改 .git 或 .github
- 触碰密钥、Telegram token、NVIDIA key
- 任何有破坏性或有发布意图的操作

**一句话**：NVIDIA 适合高 token 累活，不适合高破坏冒险。

### Reasonix / Codex / Claude Code

**当前定位**：同属 AI 执行代理，按任务适配选择，通常用于主力项目执行和复杂代码修改。

**推荐场景**：
- Codex：主力施工代理（目标由 OpenClaw/龙虾逐步接替）
- Claude Code：复杂推理与代码修改
- **Reasonix**：项目执行工，配合总控（人类+剑妈）完成发布流程

### 执行代理分工总结

| 代理 | 主力任务 | 模型成本 | 隔离性 |
|------|---------|---------|-------|
| OpenClaw/龙虾 | 主力成熟施工 | 付费 | 容器隔离 |
| Hermes (本机) | 远控+Telegram入口（执行代理） | 低成本 | 与 Docker 隔离 |
| NVIDIA（Docker Hermes） | 高token累活执行代理：长文档处理、规则整理、日志补账 | 免费/极低 | Docker 隔离 |
| Reasonix | 执行工+shell代跑 | 付费 | 容器内 |
| Codex | 主力施工（过渡期） | 付费 | 容器内 |
| Claude Code | 复杂推理 | 付费 | 容器内 |

**核心原则**：

1. **同级协作**：龙虾、Hermes、NVIDIA、Reasonix、Codex、Claude Code 都是同级 AI 执行代理，没有谁比谁高贵，只有工具特长不同。
2. **NVIDIA 特殊性**：适合高 token 长文档处理、跨文件规则一致性检查、日志补账、规则整理、低风险治理施工。使用免费或极低成本模型，不污染本机配置。作为免费练功房，可以多做探索、复盘、总结、规则整理、低风险修改。但禁止借"练功"名义执行 git add、commit、tag、push、rsync、删除文件、发布网站。
3. **本机 Hermes 保护**：NVIDIA 与本机 Hermes 必须配置隔离、数据隔离、机器人隔离，不得共用 Telegram bot token，不得污染本机蝉师傅 Hermes 和 DeepSeek 旧配置。
4. **单代理操作**：同一时间只能一个代理操作仓库，其他代理等待交接。

---

## 15. 一句话总结

剑妈定法度，执行代理轮值干活。
本地为主场，AI 为外援。
网站只发定稿。
观念雷同，只合并，不另开。
