---
title: "建站模式日志"
date: 2026-05-29
description: "angelife 网站当前建站模式、发布流程、AI 协作规则与项目总控流程图。"
showToc: true
tocOpen: true
---

angelife 当前采用的不是“想到哪改到哪”，而是一套逐渐稳定下来的本地优先建站模式。

这套模式的核心只有一句话：**本地为主场，AI 为外援。**

本地文本库 / Emacs 是草稿炉，Hugo 网站是成品库；人类用户与剑妈负责总控、定稿与验收；龙虾、蝉师傅、NVIDIA、Reasonix、Codex、Claude Code 等都属于 **AI 执行代理**，负责在统一规则下施工、构建、落盘与发布。

## 当前固定发布方式

angelife 网站当前固定采用：

> **本地 Hugo 生成 → 安全 rsync 到仓库根目录 → 精确 git add → commit → push → git tag**

Hugo 源站位于 `hugo-site/`，GitHub Pages 实际读取的是仓库根目录静态产物。也就是说，只修改 `hugo-site/content/` 并不等于网站已经上线；必须本地构建，再把 `hugo-site/public/` 同步到仓库根目录。

## 为什么坚持本地优先

当前不默认切换到 GitHub Actions 在线构建，主要因为：

- 线上实际读取的是仓库根目录静态产物；
- 本地 Hugo `v0.147.4` 构建已经稳定；
- 过去在线构建曾遇到兼容与主题问题；
- 本地优先更利于可控回滚、文件核验与人工验收。

除非用户明确授权，后续 AI 不应临时切换部署方式。

## 版本号规则

自 `v0.6.0` 起，angelife 网站采用 SemVer：`vMAJOR.MINOR.PATCH`。

- `MAJOR`：网站架构、主题、发布方式发生破坏性变化；
- `MINOR`：新增重要栏目、功能或内容体系；
- `PATCH`：样式、文案、标签、链接、图片、日志、流程等小范围优化与修复。

## 人、剑妈与 AI 执行代理的分工

### 总控层

- **人类用户**：最终拍板、授权发布、验收结果；
- **ChatGPT / 剑妈**：负责讨论、定稿、整理文章、生成图片需求、制定交接与发布要求。

### 执行层

以下都属于 **AI 执行代理**，彼此同级，没有阶级差异，只有工具特长不同：

- **龙虾 / OpenClaw**：逐步接替 Codex 的主力施工位，适合仓库内持续修改与正式施工；
- **蝉师傅 / 本机 Hermes**：本机执行代理，适合直接联动本地环境；
- **NVIDIA（Docker Hermes）**：高 token / 免费 token 的累活执行代理，适合长文档处理、规则补账、批量整理与低风险练功；
- **Reasonix / Codex / Claude Code 等**：按当下任务需求与成本情况作为可替换执行代理使用。

**原则：同一时间只允许一个执行代理操作仓库。** 不允许多个执行代理同时在同一工作树里混合施工。

## AI 接手前必读

所有执行代理接手前，必须先读：

- `PROJECT_STATUS.md`
- `BUILD_HANDOFF.md`
- `AI_WORK_RULES.md`
- `AI_EXECUTION_AGENTS.md`
- `SITE_STYLE_GUIDE.md`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `hugo-site/data/changelog.yaml`

如果不先读这些文件，就不算正式接手。

## 安全 rsync 规则

发布时必须使用 **安全 rsync**，不得裸跑 `rsync --delete`。

需要明确排除的内容至少包括：

- `.git/`
- `.github/`
- `hugo-site/`
- `_incoming/`
- `docs/`
- `tools/`
- `PROJECT_STATUS.md`
- `BUILD_HANDOFF.md`
- `AI_WORK_RULES.md`
- `AI_EXECUTION_AGENTS.md`
- `HERMES_COST_RULES.md`
- `SITE_STYLE_GUIDE.md`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `README.md`
- `LICENSE`
- `.gitignore`
- `.gitmodules`
- `publish.sh`
- `0847745cb78663855a3a1732c9c6a130.txt`
- `.DS_Store`

微信域名认证文件必须始终保留，不能被 `rsync --delete` 误删。

## 每次修改后的固定动作

每次正式发布都要完成：

1. 更新公开 changelog；
2. 更新内部日志；
3. 更新项目总控状态；
4. 本地运行 Hugo 构建；
5. 安全 rsync 到仓库根目录；
6. 精确 `git add`；
7. `commit` 并 `push`；
8. 创建 Git tag 作为可回退版本；
9. 验证线上页面和微信认证文件；
10. 记录执行代理名称、环境、模型后端与操作范围，做到可追责。

## 文章与图片如何进入网站

angelife 当前采用 **本地优先、批量发布** 的内容流程：

- 日常碎片、半成品与思路整理，优先留在 Obsidian；
- 观点成熟后，由剑妈整理成可发布文章；
- 封面图、配图、流程图等，优先由 ChatGPT 或专门图像模型生成；
- 执行代理只负责把已经准备好的成品文件接入 Hugo、构建、发布与留痕；
- 如果图片文件还不存在，就不能假装“已接入”，只能记录为 `prompt_ready`。

## 评论系统

评论系统优先采用 giscus，基于 GitHub Discussions。

正式启用前，需要用户在 GitHub 仓库开启 Discussions，并提供 giscus 所需参数。正式长文可按 front matter 决定是否开启评论；日课短文、旧日志和资料归档默认不开。

## 项目总控流程图

下图用于帮助后续 AI 快速理解：谁负责定稿，谁负责执行，文件在哪一层沉淀，以及发布链路如何闭环。

![angelife 项目总控流程图](/images/workflow/site-control-map.png)

*图：angelife 项目总控流程图。总控在人类用户与剑妈，执行层由不同 AI 执行代理接手；本地文本库 / Emacs 是草稿炉，Hugo 网站是成品库，本地 Hugo 构建与安全 rsync 构成固定发布链路。*

## 最后的原则

这个项目不是谁的“独门工作流”，而是一套要让不同 AI 都能接手、又不至于失控的共同工地规则。

所以最后落回三句话：

- **本地为主场，AI 为外援。**
- **所有执行代理同级，只有工具特长不同。**
- **先留痕，再发布；先验收，再上线。**

## 本轮执行链说明

当前 angelife 的实际执行链是：

**剑妈定法，NVIDIA 干活，本地 Mac 补完。**

人类用户 + ChatGPT / 剑妈负责设计、总控、口径、任务拆解和验收标准。

NVIDIA 是当前具体做事者，负责内容生成、整理、检查、日志草案、Obsidian 记录内容、Hugo 源文件内容和交接报告。NVIDIA 当前是运行在 Docker 里的 Hermes 程序，不持有本地仓库写权限，不运行 Hugo，不执行 release，也不直接发布。

Obsidian 内容由剑妈和 NVIDIA 生成。本地 Mac 只负责把已经生成好的内容写入本地 Vault，不生成 Obsidian 内容，不重新决策，不重新改写。

本地 Mac 只补完 NVIDIA 因 Docker 环境限制无法完成的本机动作，包括文件落盘、Hugo 构建、Obsidian 写入、tools/angelife-release、git 操作和线上验证。

本轮不启用蝉师傅、龙虾、Reasonix、Codex、Claude Code。它们作为后备工具保留，不进入 v0.6.33 默认链路。

所有操作遵循署名追责：

谁设计，谁署名。  
谁生成，谁署名。  
谁写入，谁署名。  
谁构建，谁署名。  
谁发布，谁署名。  
谁验证，谁署名。  
谁出问题，能回溯。
