# AI 执行代理低成本练功规则（Docker Hermes / NVIDIA Minimax 练功房）

> 本文件原名"Hermes 省 Token 执行规则"，但其原则同样适用于所有 AI 执行代理。
> **现在升级定位**：本文件不仅是省 token 文件，也记录 NVIDIA / 执行代理的低成本练功原则。
> NVIDIA（NVIDIA API / NIM + Minimax 免费练功房）是 angelife 项目的正式 AI 执行代理之一，适合高 token 长文档处理和免费累活练功。

## 0. 练功原则：免费可以大胆练，但不能大胆破坏

- 免费 token 可以大胆探索、大胆复盘、大胆总结、大胆整理规则。
- 但禁止借"练功"名义执行任何有破坏性的操作。
- 练功房边界清晰：本机蝉师傅 Hermes 配置、Telegram bot token、DeepSeek 旧配置均不可污染。

## 1. Docker Hermes 练功房定位

> ChatGPT / 剑妈负责思考、写作、策略、文章定稿和任务拆解。
> 所有 AI 执行代理负责本地文件操作、Hugo 构建、rsync、精确 git add、commit、tag、push。
> 执行代理是执行工具，不是写作代理，不是策略代理，不是排障研究员。

---

## 1. 默认省 Token 模式

Hermes 每次任务默认进入省 Token 模式。

必须遵守：

- 不重写文章；
- 不改写正文；
- 不总结观点；
- 不输出长篇解释；
- 不全文 cat 长文件；
- 不扫描无关目录；
- 不自行扩展任务；
- 不主动研究项目历史；
- 不输出大段命令日志；
- 不把正常过程写成分析报告。

每一步只返回最短状态，例如：

```text
✅ 检查完成
✅ Hugo 构建通过
✅ rsync 已同步
✅ commit/tag 已完成
✅ push 完成
```

---

## 2. 固定执行顺序

```text
1. pwd + git status -sb → 确认仓库状态
2. Hugo 构建
3. rsync 到仓库根
4. 更新日志文件（如果需要）
5. 精确 git add
6. git commit
7. git tag（版本号顺延）
8. git push origin master && git push origin <tag>
```

每个步骤成功后，输出一行状态。

---

## 3. 省 Token 检查

- 检查任何文件时，只用 `test -f` 或 `ls -lh`（一行）；
- 读取文件只用 `head -5` 或 `grep -c`；
- 不全文 cat，除非该文件 < 500 字节且必需；
- 不 grep 全仓库；
- 不看 themes/ 内部；
- 不看 node_modules/；
- 不看 .git/objects/。

---

## 4. 版本号顺延规则

- 每次发布新版本号从当前 `vMAJOR.MINOR.PATCH` 的 `PATCH+1` 开始；
- 例如：v0.6.26 → 下一版本 v0.6.27；
- 不跳号，不改 MAJOR/MINOR，除非用户明确要求。

---

## 5. 禁止操作

- 禁止 `git add .`
- 禁止 `git init`
- 禁止 `git pull`
- 禁止 `git merge`
- 禁止 `git rebase`
- 禁止 `git reset --hard`
- 禁止 `rm -rf`
- 禁止提交 `_incoming/`
- 禁止启用 GitHub Actions 在线 Hugo 构建
- 禁止新增 `.github/workflows/` 文件

---

## 6. 遇到异常时

- 立刻停止；
- 不自行修复；
- 报告原因和最后一步状态；
- 等待用户指令。

---

## 7. 日志更新要求

- 更新 `DAILY_WORK_LOG.md`：每天最新一次日志之前插入新条目；
- 更新 `SITE_CHANGELOG.md`：最新版本之前插入；
- 更新 `PROJECT_STATUS.md`：仅更新当前版本号和 tag 行；
- 更新 `BUILD_HANDOFF.md`：仅更新当前版本号行；
- 更新 `hugo-site/data/changelog.yaml`：文件顶部插入新条目。

---

## 8. 补充规则

以下规则来自 `AI_EXECUTION_AGENTS.md`，在此重申：

### 同一时间只能一个代理操作仓库
不得多个 AI 执行代理同时操作 angelife 仓库。

### 小改不单独发布
互链修正、标签调整、轻量补充等，保留为本地改动，等成熟後统一发布。

### 微信认证文件保护
`hugo-site/static/0847745cb78663855a3a1732c9c6a130.txt` 和根目錄同名文件，内容 `01413348ab0d5b381a2e7099ba2600ed57ad50d3`，永久保护不得删除或覆蓋。

### 安全 rsync
禁止裸 `rsync -av hugo-site/public/ ./`。必须排除治理文档、微信文件、`.git/`、`_incoming/` 等。完整排除清单見 `AI_EXECUTION_AGENTS.md` 第 11 節。

---

## 9. NVIDIA 练功房隔离要求

NVIDIA（Docker Hermes 独立实例）与本机 Hermes 必须严格隔离，具体要求：

1. **配置隔离**：不得共用 `~/.hermes/` 配置目录。NVIDIA 使用独立 profile。
2. **数据隔离**：不得共用数据库、会话文件、memory 文件。
3. **机器人隔离**：不得共用 Telegram bot token。NVIDIA 使用独立的 Telegram bot。
4. **环境隔离**：Docker 容器内运行，不污染本机蝉师傅 Hermes 的进程和环境。
5. **token 来源隔离**：NVIDIA 使用 NVIDIA API / NIM + Minimax 免费练功房；本机蝉师傅使用 DeepSeek 旧配置。二者不得混用 API key。

**NVIDIA 可做**：
- 大胆探索、复盘、总结、规则整理
- 高 token 长文档处理（跨文件规则一致性检查、日志补账）
- 读取项目规则、检查一致性
- 低风险治理施工（修改规则文档、补全日志）
- 用实践掌握项目工具特点

**NVIDIA 禁止**：
- git add（精确 add 除外，但本练功房不进行任何发布操作）
- git commit
- git tag
- git push
- rsync
- Hugo 构建（除非用户明确授权做验收检查）
- 删除文件
- 修改 .git 或 .github
- 触碰密钥、Telegram token、NVIDIA key
- 任何有破坏性或有发布意图的操作

**一句话**：NVIDIA 适合高 token 累活，不适合高破坏冒险。练功房里可以大胆学，不可以大胆破坏。

---

## 10. 执行代理同级原则

龙虾、Hermes、NVIDIA、Reasonix、Codex、Claude Code 都是同级 AI 执行代理。
没有阶级差异，只有工具特长、成本、稳定性、界面和模型后端的差异。

- 龙虾目标逐步接 Codex 的主力施工位。
- NVIDIA 适合高 token 长文档处理、规则整理、日志补账和免费累活练功。使用 NVIDIA API / NIM + Minimax 免费或极低成本模型，不污染本机配置。
- 但所有代理必须遵守同一仓库、同一流程、同一时间单代理操作原则。

---

> 本文件升级为"NVIDIA 练功房"定位后，核心禁止规则（如禁止裸 rsync、禁止 git add .、禁止删除文件等）保持不变。
> NVIDIA 适合高 token 累活，不适合高破坏冒险。所有练功活动必须在不破坏项目安全边界的前提下进行。
> **即使是免费 token / 高 token 练功任务，也必须署名留痕。免费可以多练，但不能匿名操作。**
> NVIDIA、Hermes、龙虾、Reasonix、Codex、Claude Code 等所有执行代理都必须写清楚自己是谁、做了什么、是否影响仓库、是否发布。
