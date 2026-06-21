# angelife 项目术语修正记录

本文档记录已确认的术语修正，供后续维护参考。

## 修正 1：总控表述

**规则**：总控永远是"人类用户 + ChatGPT / 剑妈"，不是 Hermes。

### 错误表述（应修正为）

| 错误表述 | 正确表述 |
|---------|---------|
| `配合 Hermes 总控完成发布流程` | `配合总控（人类+剑妈）完成发布流程` |
| `Hermes（手机远程总控和 Telegram 入口）` | `Hermes（手机远控和 Telegram 入口）` |
| `总控+远控+Telegram入口` | `远控+Telegram入口（执行代理）` |
| `手机 Telegram → Hermes 总控 → terminal` | `手机 Telegram → Hermes（远控+Telegram入口）→ 总控（人类+剑妈）→ terminal` |
| `Hermes 为总控和 terminal 手臂` | `人类用户+剑妈负责总控。Reasonix 为执行工，Hermes 为远控+Telegram入口（执行代理）和 terminal 手臂。` |
| `Hermes 是手机远程总控和 Telegram 入口` | `人类用户 + ChatGPT / 剑妈负责总控、定稿、边界和验收。Hermes / Docker Hermes / 龙虾 / Reasonix / Codex / Claude Code 都是 AI 执行代理。` |

### 涉及文件

- `AI_EXECUTION_AGENTS.md`（分工表、`配合 Hermes 总控`行）
- `AI_WORK_RULES.md`（开篇分工说明、远控链路描述、硬性禁止段）
- `BUILD_HANDOFF.md`（手机远控操作指南段）
- `hugo-site/content/about.md`（关于页，需同步更新）
- `DAILY_WORK_LOG.md`（日志历史，不修改，仅作参考）
- `SITE_CHANGELOG.md`（变更历史，不修改，仅作参考）
- `hugo-site/data/changelog.yaml`（历史 changelog，不修改，仅作参考）

> 注意：`DAILY_WORK_LOG.md`、`SITE_CHANGELOG.md`、`hugo-site/data/changelog.yaml`、`hugo-site/content/about.md` 是历史记录或已上线页面，修正时通常不修改这些文件中的历史记录。只需修改"活"的治理文件（`AI_EXECUTION_AGENTS.md` 等）。如果涉及已上线的 `about.md`，需要另行处理（修改 + Hugo 构建 + 发布）。

---

## 修正 2：Docker Hermes 技术栈表述

**规则**：Docker Hermes 使用 NVIDIA API / NIM，不是"GPU"。

| 错误表述 | 正确表述 |
|---------|---------|
| `NVIDIA GPU + Minimax 免费或低成本模型` | `NVIDIA API / NIM + Minimax 免费练功房` |
| `Docker 独立 Hermes + NVIDIA GPU + Minimax 免费/低成本模型` | `NVIDIA API / NIM + Minimax 免费练功房` |

### 涉及文件

- `AI_EXECUTION_AGENTS.md`（Docker Hermes 章节）
- `AI_WORK_RULES.md`（开篇分工说明）
- `HERMES_COST_RULES.md`（练功房隔离要求）
- `BUILD_HANDOFF.md`（文件开篇说明）

---

## 修正 3：代理分工总原则

**规则**：所有 AI 执行代理同级，无阶级差异。只有工具特长不同。

每句话都要体现：

```
人类用户 + ChatGPT / 剑妈 负责总控、定稿、边界和验收。
Hermes / Docker Hermes / 龙虾 / Reasonix / Codex / Claude Code 都是 AI 执行代理。
```

典型场景：
- 新增代理定位章节 → 包含上述总原则
- 修改分工表 → 包含"总控是人和剑妈"说明
- 远控链路描述 → 体现 Hermes 只是入口，不是总控

---

## 修正 4：Docker Hermes 独立实例正式命名为 NVIDIA

**规则**：Docker Hermes 独立实例在所有治理文件中统一称为"NVIDIA"，是 NVIDIA API / NIM + Minimax 免费练功房，是高 token 累活执行代理。

| 错误表述 | 正确表述 |
|---------|---------|
| `Docker Hermes`（作为代理名称） | `NVIDIA（Docker Hermes）` |
| `### Docker Hermes` 章节标题 | `### NVIDIA（Docker Hermes 独立实例）` |
| `NVIDIA GPU + Minimax` | `NVIDIA API / NIM + Minimax 免费练功房` |
| `Docker Hermes 练功房` | `NVIDIA 练功房` |
| `Docker Hermes 做总控` | `NVIDIA 不是总控代理（总控：人类用户 + ChatGPT / 剑妈）` |
| `Docker Hermes 可做/禁止` | `NVIDIA 可做/禁止` |

### NVIDIA 的准确描述

```
NVIDIA（Docker Hermes 独立实例）
- 定位：NVIDIA API / NIM + Minimax 免费练功房，高 token 累活执行代理
- 适合：长文档处理、规则整理、日志补账、跨文件一致性检查、低风险治理施工
- 禁止：git add/commit/tag/push/rsync/Hugo 构建/删除文件/触碰密钥
- 一句话：NVIDIA 适合高 token 累活，不适合高破坏冒险
- 原则：可以大胆学，不可以大胆破坏
```

### 涉及文件

- `AI_EXECUTION_AGENTS.md`（§14 代理描述、表格式、核心原则）
- `AI_WORK_RULES.md`（分工列表）
- `HERMES_COST_RULES.md`（抬头引用、§9 标题和正文、§10 执行代理同级原则）
- `BUILD_HANDOFF.md`（版本号更新）
- 5 个 changelog 文件（见 SKILL.md 场景 D）

---

## 下次需要修正时的快速检查清单

1. `rg "总控.*Hermes|Hermes.*总控"` → 确认无遗漏
2. `rg "NVIDIA GPU"` → 确认无遗漏
3. `rg "悍马"` → 确认无遗漏（中文音译）
4. `rg "Docker Hermes 做总控|Docker Hermes 是总控"` → 确认无遗漏
5. 同一术语在 4 个核心治理文件中是否一致
6. changelog 5 文件是否同步更新（SITE_CHANGELOG + DAILY_WORK_LOG + PROJECT_STATUS + BUILD_HANDOFF + changelog.yaml）
7. 输出是否为三段式（文件、表述、是否发布）