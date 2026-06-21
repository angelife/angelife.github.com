# NVIDIA 命名更新记录（v0.6.32）

本文档记录 v0.6.32 期间将"Docker Hermes 独立实例"正式命名为"NVIDIA"的具体修正内容。

## 背景

Docker Hermes 独立实例是 angelife 项目的正式 AI 执行代理之一，使用 NVIDIA API / NIM + Minimax 免费模型。本机 Hermes 使用 DeepSeek 旧配置。两者严格隔离，不得混用。

命名更新原因：统一所有治理文件中的代理称呼，明确 NVIDIA 是高 token 累活执行代理而非总控代理。

## 具体修正清单

### 1. AI_EXECUTION_AGENTS.md

**§14 代理描述段落（原 Docker Hermes 部分）**：

- 标题：`### Docker Hermes` → `### NVIDIA（Docker Hermes 独立实例）`
- 描述更新：明确 NVIDIA 是 NVIDIA API / NIM + Minimax 免费练功房，高 token 累活执行代理，适合长文档处理、规则整理、日志补账
- 新增明确说明：NVIDIA 不是总控代理（总控：人类用户 + ChatGPT / 剑妈）
- 新增"NVIDIA 可做/禁止"列表（8 项禁止：git add/commit/tag/push/rsync/Hugo构建/删除文件/触碰密钥）
- 新增一句话：NVIDIA 适合高 token 累活，不适合高破坏冒险

**表格式**：
- `Docker Hermes` → `NVIDIA（Docker Hermes）`
- 表中主力任务描述更新为"高token累活执行代理：长文档处理、规则整理、日志补账"

**核心原则 4 条**：
- 第 1 条：加入"NVIDIA"
- 第 2 条：Docker Hermes 特殊性 → NVIDIA 特殊性，描述更新为高 token 累活
- 第 3 条：Docker Hermes → NVIDIA，本机 Hermes 保护增加"DeepSeek 旧配置"

### 2. AI_WORK_RULES.md

- `Docker Hermes` 行 → `NVIDIA（Docker Hermes）`
- 描述增强为"高 token 累活执行代理，适合长文档处理、规则整理、日志补账"

### 3. HERMES_COST_RULES.md

- 标题保持（文件本身以"Docker Hermes / NVIDIA Minimax 练功房"为副标题）
- 抬头引用：Docker Hermes（NVIDIA + Minimax...）→ NVIDIA（NVIDIA API / NIM + Minimax 免费练功房）
- §9 标题：`Docker Hermes 练功房隔离要求` → `NVIDIA 练功房隔离要求`
- §9 正文：所有"Docker Hermes"改为"NVIDIA"，5 项隔离更新（独立 profile、独立 Telegram bot 等）
- §9 可做：增加"高 token 长文档处理（跨文件规则一致性检查、日志补账）"
- §9 禁止：Docker Hermes 禁止 → NVIDIA 禁止
- §9 一句话：增加"NVIDIA 适合高 token 累活，不适合高破坏冒险"
- §10 执行代理同级：列表中加入"NVIDIA"
- §10 NVIDIA 描述：适合高 token 长文档处理、规则整理、日志补账和免费累活练功
- 结尾备注：更新为"NVIDIA 练功房定位"

### 4. BUILD_HANDOFF.md

- 版本号：`v0.6.31` → `v0.6.32 待发布`
- 新增"本轮 v0.6.32 工作说明"节（修正内容、修改文件、当前状态）

### 5. changelog 5 文件同步更新

见 SKILL.md 场景 D 的 5 文件更新表。

## 修正原则

1. **NVIDIA 不是总控**：所有文件中明确 NVIDIA 是累活执行代理，不是总控
2. **同级协作**：NVIDIA 与龙虾、Hermes、Reasonix、Codex、Claude Code 同级，无阶级差异
3. **免费练功原则**：NVIDIA 是免费练功房，可以大胆学，不可以大胆破坏
4. **本机保护**：NVIDIA 不得污染本机 Hermes/蝉师傅的 DeepSeek 旧配置

## 剩余历史记录（不修正）

以下文件中的历史记录不需要修正：
- `DAILY_WORK_LOG.md` 第 394 行："Hermes 是总控，不得夺权。"（历史日志）
- `SITE_CHANGELOG.md` 第 313 行：历史变更记录
- `hugo-site/content/about.md`：legacy 文件，用户明确禁止修改正文

## 搜索验证命令

修正完成后，用以下命令验证无遗漏：

```bash
rg "Docker Hermes 做总控|Hermes 做总控|Hermes 是总控|NVIDIA GPU"
```

预期：0 个匹配（或仅限历史记录文件）