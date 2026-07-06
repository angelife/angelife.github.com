---
title: "Claude Desktop MCP Debug 3：最终验证与恢复"
date: 2026-07-06
draft: false
summary: "经过误判、重启、实验和恢复后，这条 managed MCP 的可交付状态是什么。"
tags: ["Claude Desktop", "MCP", "Hindsight", "恢复验证"]
series: ["claude-desktop-mcp-debug"]
slug: "claude-desktop-mcp-debug-03-final-verification-and-rollback"
---

## 结论

这个事情最终是可用状态，不是部分成功状态。
根因已收敛为：managed schema 字段名和结构一开始写错。
之后出现的“只剩 1 个工具”不是真裁剪，已被验证为误判。

## 核心判断

当前可交付状态：
- managed config 路径正确：`Claude-3p/configLibrary/00000000-0000-4000-8000-000000157210.json`
- 正确字段：`managedMcpServers`
- 正确结构：array-of-entries
- Hindsight 已连接，日志记录 `toolCount: 29`
- Desktop runtime 可调用完整 hindsight 工具集
- config 已恢复 clean baseline

## 依据

- managed config 内容可读，`mcpServers` 误写已被删除。
- Desktop 日志显示：

  ```
  [custom3p-mcp] connected { name: 'hindsight', toolCount: 29, auth: 'stdio' }
  ```

- 直接询问 Desktop 可见工具列表，确认可见完整集合。
- 备份存在：`/Users/macos/Desktop/managed-config-toolpolicy-backup-20260706.json`

## 常见误区

- 已经有可用连接后，还继续加 `toolPolicy: blocked` 实验。
- 看到“UI 没显示全部”就继续怀疑 runtime 裁剪。
- 在多 AI 分析之间来回追问，却忘了做本地对照实验。

## 可恢复性

关键操作都有备份：
- managed config 写入前备份
- 实验前后有 restore
- baseline 已回到干净状态

## 遗留问题

- `managedMcpServers` 的 validator 是否还有未文档化行为
- `allowedMcpServers: []` 在 3P 模式下的完整语义
- UI 展示层与 runtime registry 的状态同步机制

这些不再影响当前可用性，如果后续需要，可单独作为新题目追踪。

## 结语

最难的阶段不是写配置，而是区分“ observed limitation”和“ actual limitation”。
当服务端、连接层、调用层都给出正向证据时，先相信系统已经工作，再设计实验验证，是更稳的做法。
