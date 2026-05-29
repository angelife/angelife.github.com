# angelife / 安知生

> 让不同 AI 都能接手、又不至于失控的共同工地规则。

## 这是什么项目

angelife（安知生）是一个公开知识网站，托管于 GitHub Pages。
当前版本 **v0.6.36**。

本项目不是谁的独门工作流，而是一套让不同 AI 都能接手的协作制度。
所有规则都写在文档里，不在任何人脑子里。

---

## AI 接手第一步

**必须先读 README.md，然后按顺序读以下文件。**

不读这些文件，不算正式接手。

### 必读清单

1. `README.md`（本文件）← 你在这里
2. `AI_BOOTSTRAP.md` — 完整项目记忆恢复入口
3. `PROJECT_STATUS.md` — 当前版本、发布状态、项目阶段
4. `BUILD_HANDOFF.md` — 构建与发布的标准交接流程
5. `AI_WORK_RULES.md` — AI 施工规则与安全红线
6. `AI_EXECUTION_AGENTS.md` — 执行代理分工与备用列表
7. `DAILY_WORK_LOG.md` — 日常执行日志
8. `SITE_CHANGELOG.md` — 版本变更记录
9. `hugo-site/data/changelog.yaml` — 结构化 changelog

按顺序读。读完全部，再动手。

---

## AI_BOOTSTRAP.md 是完整记忆恢复入口

`AI_BOOTSTRAP.md` 包含：

- 项目定位与目标
- 核心协作原则
- 版本演进脉络
- 当前施工阶段
- 关键配置文件位置
- 发布链路说明

它是新 AI 入场的起点文档。读完它之后，再去读上面必读清单里的其他文件。

---

## 当前真实分工

本项目不存在"总控 AI"，只有**总控层**和**执行层**。

### 总控层

| 角色 | 职责 |
|------|------|
| 人类用户 | 最终拍板、授权发布、验收结果 |
| 剑妈 / ChatGPT | 方向、架构、规则、口径、任务拆解、验收标准 |

### 执行层（同级，无阶级差异）

| 角色 | 定位 |
|------|------|
| NVIDIA（Docker Hermes） | 具体做事者：高 token 累活代理，负责生成、整理、检查、落文件、日志草案 |
| 蝉师傅 / 本机 Hermes | 本机执行代理，适合直接联动本地环境 |
| 龙虾 / OpenClaw | 主力施工位，适合仓库内持续修改与正式施工 |
| Reasonix / Codex / Claude Code | 按需求作为可替换执行代理 |

**Obsidian 内容由剑妈 + NVIDIA 生成。本地 Mac 只负责写入，不生成内容。**

---

## 发布方式

```
本地 Hugo 构建 → tools/angelife-release → 精确 git add → commit → tag → push → 线上验证
```

- Hugo 源站：`hugo-site/`
- 实际读取：仓库根目录静态产物（GitHub Pages）
- 只修改 `hugo-site/content/` 不等于上线

**禁止裸 rsync。** 必须通过 `tools/angelife-release`。

---

## 安全红线（禁止事项）

以下行为无论谁授权，一律禁止：

- ❌ `git add .`（必须精确指定文件）
- ❌ 提交 `_incoming/` 或 `.reasonix/` 目录
- ❌ 裸 `rsync --delete`
- ❌ 删除 `tools/` 或 `publish.sh`
- ❌ 删除 `.gitignore` 或 `.gitmodules`
- ❌ 删除微信认证文件（`0847745cb78663855a3a1732c9c6a130.txt`）
- ❌ 未授权发布
- ❌ 匿名施工（不署名）

**谁干活，谁署名。谁操作，谁负责。谁出问题，能回溯。**

---

## 版本演进

| 版本 | 内容 |
|------|------|
| v0.6.33 | 公开 /site-workflow/ 协作制度 |
| v0.6.34 | 热修流程图静态资源 |
| v0.6.35 | 新增 AI_BOOTSTRAP.md，固化 AI 接手记忆 |
| **v0.6.36** | **更新 README 为 AI 接手入口** |

---

## 下一阶段

**v0.7.0：旧 Blogger 内容回流工程**

来源：https://angelifex.blogspot.com/

目标：剑妈 + NVIDIA 自动抓取、整理、分类、去重、再加工旧 Blogger 内容，迁移回 Hugo 新站。

原则：不无脑搬运，能合并就合并，有独立价值才新建文章，过时内容归档，长期目标 0 参与自动化。

---

## 链接

- 公开站点：https://angelife.github.io/
- 建站模式日志：https://angelife.github.io/site-workflow/
- 项目 GitHub：https://github.com/angelife/angelife.github.com# README.md 追加内容

> 以下内容追加到 README.md 末尾，不要重写全文。

---

## NVIDIA / Hermes 故障恢复

Telegram 中 NVIDIA 不回复时，先读 `NVIDIA_GATEWAY_RECOVERY.md`。
禁止直接 docker restart 或挂载主库。

---

## changelog.yaml 写入规则

changelog.yaml 修改必须遵守 `CHANGELOG_YAML_RULES.md`。
NVIDIA 只生成 YAML 块草案，本地 Mac 构建验证通过后才能 release。

---

## 主库挂载规划

当前 NVIDIA 无主库访问权限。详见 `NVIDIA_MAIN_REPO_MOUNT_PLAN.md`。
三阶段规划：只写文件 → 可 commit/tag → 完整 release。