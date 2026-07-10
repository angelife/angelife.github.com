---
title: "Claude Desktop MCP Debug 2：29 个工具为什么曾看起来只剩 1 个"
date: 2026-07-06
draft: false
summary: "服务端返回 29 个工具，但 Desktop 里一度只像暴露了 get_bank；真实原因是调用范围有限，不是系统裁剪。"
tags: ["Claude Desktop", "MCP", "runtime", "tool shaping"]
series: ["claude-desktop-mcp-debug"]
slug: "claude-desktop-mcp-debug-02-tool-count-misreading"
---

## 结论

不是 29 个工具被裁剪成了 1 个。是第一次只看到 `get_bank`，后来才发现 `retain`、`recall`、`reflect`、`list_memories` 等都已暴露。

## 背景

entry 修复后，Desktop 日志明确出现：

```
[custom3p-mcp] connected { name: 'hindsight', toolCount: 29, auth: 'stdio' }
```

但对话里一开始只见过 `mcp__hindsight__get_bank`。
于是有了几个推测方向：

- 3P policy 裁剪
- toolPolicy blocked 隐藏
- CC Switch 覆写
- Desktop runtime bug

## 核心判断

先把已知事实钉死：

- [KNOWN] Hindsight `tools/list` 返回 29 个工具。
- [KNOWN] Desktop 连接日志记录 `toolCount: 29`。
- [KNOWN] Desktop runtime 中 `mcp__hindsight__get_bank` 可用。
- [KNOWN] 后续完整工具列表可用，包括 `retain`、`recall`、`reflect` 等。

其余解释，如 policy pruning、blocked 隐藏、CC Switch 截断，都属于 **[INFERRED]**。
它们都不能直接解释 29→1。

## 依据

- 直接访问 Hindsight 服务端 `tools/list`，得到完整 29 个工具清单。
- Desktop 日志是连接成功的证据，不是裁剪证据。
- 实际询问 Desktop 后，完整工具集合可被调用。

## 常见误区

- 把“没看到全部工具”当成“工具被隐藏”。
- 把 UI 显示不全当成 runtime 真裁剪。
- 把单一路径观测当成全局状态。

## 方法论

已知 service 层完整时，先问：是“服务端没给”，还是“客户端没展示”？
切分标准模式实验、toolPolicy 实验、日志取证。
逻辑上最有信息增益的是：标准模式是否能复现 29 工具。

最难的是区分“ observed limitation”和“ actual limitation”。
这一章结束时，Hindsight 的真实状态已经是：**29 个工具，3P managed 模式可用，已恢复 clean baseline**。下一章写最终验证结果和可恢复过程。
