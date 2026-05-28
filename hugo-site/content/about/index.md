---
title: "关于安知生"
date: 2026-05-28
draft: false
description: "安知生是 angelife 的长期知识系统：本地为主场，AI 为外援；Obsidian 养稿，Hugo 发布，Git 保护成果，人和剑妈守住方向。"
cover:
  image: /images/about/cover.png
  alt: 关于安知生：本地为主场，AI 为外援。图中以 Obsidian、ChatGPT / 剑妈、Hermes、Hugo、Git 和人的判断构成一条从草稿到发布的知识工作流。
  caption: 本地为主场，AI 为外援：以 AI 整理材料，以 Obsidian 沉淀知识，以 Hugo 发布作品，以 Git 保护成果，以人的判断守住方向。
---

# 关于安知生

安知生是 angelife 的个人知识网站。

它不是一个临时博客，也不是流量平台的附属品，而是一个长期积累、整理、校正和发布思想的本地知识系统。这里记录 AI 时代的工具实践、信息判断、个人知识管理、阅读方法、技术折腾、传统文化思考，以及人在复杂系统中如何保持清醒的问题。

这个网站的核心不是"更新得快"，而是：

> 把真正想清楚的东西留下来。

## 本地为主场，AI 为外援

angelife 当前的工作流已经调整为：

**Obsidian 是草稿炉，Hugo 网站是成品库。**

日常碎片、微信聊天、临时想法、未成熟判断，先进入本地 Obsidian。相似观点先合并，重复内容先沉淀，半成品不急着发布。只有当一组观点已经想清楚、整理好、形成定稿，才进入 Hugo 网站。

网站只发定稿。

小改不单独发布。碎片不烧 token。观念雷同，只合并，不另开。成熟一批，再统一发布。

这样做是为了避免把网站变成草稿箱，也避免让 AI 执行代理在不成熟内容上反复试错、消耗 token、扰乱项目结构。

## 人、剑妈与 AI 执行代理

angelife 的当前协作结构分为三层。

第一层是人。

人负责提出问题、判断方向、确认边界、决定是否发布，并且守住最重要的一件事：**不失正见**。

第二层是 ChatGPT / 剑妈。

剑妈负责总控、主编、文章定稿、封面图生成、任务拆解、执行代理调度、验收标准和项目法度维护。

文章正文、标题、slug、description、front matter、封面图、alt text、caption，原则上先由剑妈定稿或生成。

第三层是 AI 执行代理。

OpenClaw / 龙虾、Hermes / Hermers、Docker Hermes、Reasonix、Codex、Claude Code，以及未来接入的类似工具，都属于 AI 执行代理。

它们没有阶级高低，只有工具特长不同。

龙虾 / OpenClaw 适合网页界面、长会话、可视化观察和真实仓库施工。它会逐步承担 Codex 过去在 angelife 项目中的主力成熟执行代理位置。

本机 Hermes 保留原有 DeepSeek / Telegram 蝉师傅配置，不随意污染、不随意覆盖。

Docker Hermes 使用 NVIDIA API / NIM + Minimax 免费或低成本模型，作为独立练功房，用于自我学习、规则复盘、流程试错和低风险治理施工。

Reasonix、Codex、Claude Code 等工具继续作为同类执行代理，按任务适配选择。

谁适合当前任务，谁上场。
工具无阶级，任务有适配。
实践出真知，边用边学，边用边掌握工具特点。

## 同一个工地，同一套法度

所有 AI 执行代理默认围绕同一个本地仓库工作：

```text
/Users/macos/angelife.github.com
```

在 Docker / OpenClaw 容器内，对应路径可能是：

```text
/home/node/.openclaw/workspace/angelife.github.com
/workspace/angelife.github.com
```

但无论外壳如何变化，规则必须统一。

所有执行代理接手前都必须读取项目根目录的规则和交接文件，包括：

```text
PROJECT_STATUS.md
BUILD_HANDOFF.md
AI_WORK_RULES.md
HERMES_COST_RULES.md
AI_EXECUTION_AGENTS.md
SITE_STYLE_GUIDE.md
SITE_CHANGELOG.md
DAILY_WORK_LOG.md
```

不得各自创建一套独立流程、独立目录、独立发布方式。
不得随意切换 GitHub Actions 在线构建。
不得 `git add .`。
不得提交 `_incoming/`。
不得删除微信认证文件。
不得多个 AI 执行代理同时操作同一个仓库。

同一时间只能一个执行代理接手。
一个代理完成后，输出报告并停止。
下一个代理再接手。

## 固定发布流程

angelife 网站固定发布流程是：

```text
本地 Hugo 构建
→ 安全 rsync 到仓库根目录
→ 更新日志和版本文件
→ 精确 git add
→ commit
→ tag
→ push
```

GitHub Pages 保持：

```text
Deploy from branch / master / root
```

不使用 GitHub Actions 在线构建 Hugo。

微信认证文件必须永久保护：

```text
hugo-site/static/0847745cb78663855a3a1732c9c6a130.txt
```

以及仓库根目录：

```text
0847745cb78663855a3a1732c9c6a130.txt
```

内容必须保持：

```text
01413348ab0d5b381a2e7099ba2600ed57ad50d3
```

它是网站的一块地契，不能被清洁构建、rsync、重构或发布流程扫掉。

## 文章与图片如何生成

文章不是交给执行代理随便写。

一篇文章通常先从微信聊天、个人思考、Obsidian 草稿或与剑妈的讨论中形成观点。如果观点成熟，剑妈负责整理成可发布定稿。如果需要配图，也由剑妈或专门图像模型生成真实图片文件。

执行代理只负责把已经定稿的文章和图片放到 Hugo 仓库指定位置，接入 front matter，执行构建和发布流程。

如果图片不存在，执行代理不得伪造 `cover.image`。只能记录 `cover_status: prompt_ready`，等真实图片生成后再接入。

这条规则是为了避免内容生产和网站执行混在一起。

文章的判断权、定稿权和审美方向，仍然在人和剑妈这里。执行代理负责施工，不负责替代总控。

## 为什么坚持本地优先

AI 很强，但 AI 不是主场。

如果所有想法都放在聊天窗口，最后会散。如果所有草稿都交给平台，最后会丢。如果每个小改都让执行代理发布，token 会被烧掉，项目也会变乱。

所以 angelife 选择本地优先。

Obsidian 负责养稿。
Hugo 负责公开。
Git 负责版本和回退。
AI 执行代理负责在明确边界内施工。
剑妈负责定法度、定稿和验收。
人负责最终判断。

工具可以越来越多，但主场不能丢。

## 最后的原则

angelife 网站要记录的不是"AI 替人做了多少事"，而是人在 AI 时代如何不被工具吞掉。

工具可以用。
AI 可以用。
自动化可以用。
低成本模型也可以大胆练。

但不能忘记：

本地为主场，AI 为外援。
网站只发定稿。
观念雷同，只合并，不另开。
剑妈定法度，执行代理轮值干活。
实践出真知。
不失正见。