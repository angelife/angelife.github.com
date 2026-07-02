---
title: "Hermes Agent 速查"
slug: "hermes-quick-reference"
date: 2026-07-03T02:00:00+08:00
draft: false
description: "Hermes Agent（Nous Research）的核心架构速查——面向自部署用户的骨架级理解，不废话。"
categories:
  - "火·AI"
  - "工具"
series: ["ai-bu-yin"]
tags:
  - "Hermes"
  - "AI智能体"
  - "自部署"
  - "工具系统"
  - "配置"
---

## 一句话

Hermes 是一个**以 AIAgent 为窄腰的智能体操作系统**。所有前端（CLI、Telegram、Discord、API）共享同一个核心循环，能力通过工具、Provider、记忆在边缘扩展。

```
CLI     Telegram     Discord     API
 │          │           │          │
 └──────────┼───────────┼──────────┘
            │
     ┌──────▼──────┐
     │  AIAgent    │  ← 窄腰（核心会话循环，最小接口）
     └──────┬──────┘
            │
  ┌─────────┼─────────┐
  │         │         │
  ▼         ▼         ▼
工具      Provider   记忆
(70+)     (30+)      (5+ 类型)
```

---

## 入口点

| 命令 | 用途 | 进程模型 |
|------|------|---------|
| `hermes` / `hermes chat` | 终端交互对话 | 前台单进程 |
| `hermes gateway start` | 消息平台网关 | 后台 asyncio 守护 |
| `hermes setup` | 初始设置向导 | 临时进程 |
| `hermes mcp serve` | 暴露为 MCP 服务器 | stdio MCP 协议 |
| `hermes acp` | ACP 服务器（编辑器集成） | stdio 协议 |

---

## 配置系统

三层合并（高→低优先级）：CLI 参数 > `~/.hermes/config.yaml` > 内建默认值。

密钥走 `~/.hermes/.env`，不写在 yaml 里。

### 核心字段

```yaml
model:
  default: "模型名"
  provider: "auto"          # auto / anthropic / openrouter / custom
  base_url: "https://..."
  api_key: "sk-..."         # 推荐放 .env

providers:
  <名称>:
    base_url: "https://..."
    key_env: "环境变量名"
    extra_headers: {}       # 自定义 HTTP 头
    request_timeout_seconds: 300
    models:
      <模型名>:             # 按模型覆盖
        timeout_seconds: 600

custom_providers:           # 完整自定义提供者
  - name:
    provider_key:
    base_url:
    model:
    extra_body:

gateway:
  platforms:
    telegram:
      bot_token: "..."

mcp_servers:
  <名称>:
    command: "..."          # stdio 模式
    url: "..."              # HTTP 模式
    transport: stdio        # stdio / http / sse
```

### Provider 路由机制

```
model.provider="auto"
  → PROVIDER_REGISTRY 扫描所有环境变量
  → 按优先级匹配（anthropic > openai > openrouter > …）
  → runtime_provider.py 解析 api_mode
     ├── chat_completions（OpenAI 兼容）
     ├── codex_responses（Codex 专用）
     └── anthropic（原生 API）
```

> **排查要点**：非标准 Provider 的 tool_calls 格式可能与 OpenAI 标准不一致，导致工具调用失效（模型返回文本而非函数调用）。

---

## 工具系统

### 注册机制

每个工具文件在 import 时自注册到中心注册表：

```python
# tools/terminal_tool.py
registry.register(
    name="terminal",
    toolset="terminal",
    schema={...},          # OpenAI 函数 schema
    handler=handler_fn,
    check_fn=_check,       # 运行时可用性检测
    requires_env=[],
)
```

### 调用链路

```
用户提问
  → API 请求（带上所有可用工具 schema）
  → 模型返回 tool_call
  → model_tools.handle_function_call(name, args)
    → registry.dispatch(name, args)
      → 调用 handler
  → 结果注入消息历史
  → 再次 API 调用
  → 循环直到模型返回纯文本（上限 90 次迭代）
```

### 28 个工具集

通过 `toolsets.py` 分组，可自由启用/禁用：

- `web` — web_search, web_extract
- `terminal` — terminal, process
- `code` — execute_code
- `file` — read_file, write_file, patch, search_files
- `browser` — browser_navigate, browser_click 等
- `memory` — memory CRUD
- `skills` — skills_list, skill_view, skill_manage
- `messaging` — send_message
- `vision` — vision_analyze
- `image_gen` — image_generate
- `delegation` — delegate_task
- `mcp` — MCP 客户端调用

---

## 技能系统（Skills）

**技能不是 prompt 注入，是渐进式披露的知识文档。**

### 三层加载

| 层级 | 触发操作 | Token 消耗 |
|------|---------|-----------|
| L0 | 启动时自动注入技能索引（名称+描述） | ~3K |
| L1 | `skill_view("名称")` 加载全文 | 按需 |
| L2 | `skill_view("名称", file_path)` 加载引用文件 | 按需 |

### SKILL.md 格式

```yaml
---
name: my-skill
description: 简短描述
version: 1.0.0
platforms: [macos, linux]
metadata:
  hermes:
    tags: [python, automation]
    category: devops
    fallback_for_toolsets: [web]
    requires_toolsets: [terminal]
config:
  - key: my.setting
    description: ""
    default: "value"
---
```

### 条件激活

技能描述越精确，触发概率越高。模糊的描述（如"用于 Python"）会被 L0 索引算法跳过。

---

## 网关系统

### 支持平台（20+）

Telegram、Discord、Slack、WhatsApp、Signal、Matrix、Email（IMAP+SMTP）、微信、企微、飞书、钉钉、QQ Bot、Mattermost、Webhook、API Server、TUI、CLI、Teams、Google Chat、BlueBubbles、Home Assistant。

### 消息流

```
平台接收事件 → GatewayRunner._handle_message()
  → 授权验证
  → 构建 session_key（platform:chat_id:user_id）
  → 获取/创建会话（SQLite 持久化）
  → 获取/创建 AIAgent（LRU 缓存，128 个，1h TTL）
  → AIAgent.run_conversation()
  → 平台适配器.send_message()
```

### Agent 缓存

128 个 agent LRU，1 小时空闲 TTL。大量活跃会话时注意内存压力。

---

## 记忆系统

### 层次

| 层级 | 容量 | 持久性 |
|------|------|--------|
| MEMORY.md | 2,200 字 | 注入每轮系统提示 |
| USER.md | 1,375 字 | 同上 |
| Hindsight | 无上限（语义检索） | 跨会话，按查询命中 |
| SQLite FTS5 | 全部会话历史 | 全文搜索 |

### memory 工具操作

- `add` — 添加新条目
- `replace` — 替换（需子串匹配旧内容）
- `remove` — 删除（需子串匹配）

### 跨会话连贯性

内置记忆（MEMORY.md+USER.md）在每轮系统提示中注入。2,200 字上限满了会挤掉旧条目。Hindsight 作为外部 Memory Provider 补充语义检索，但依赖检索命中率。**两条合起来约能覆盖 80% 的跨会话连贯性。**

---

## 会话管理

- SQLite WAL 模式 + FTS5 全文搜索
- 会话键格式：`agent:profile:platform:chat_id:user_id`
- 自动压缩：上下文使用率 > 75% 时触发，旧消息摘要化
- 分支：`/branch` 或 `/fork` 创建独立子会话
- 恢复：`/resume` 重新加载历史

---

## 自部署常见陷阱

| 现象 | 根因 |
|------|------|
| 工具调用不执行（返回文本） | Provider 返回格式不兼容 OpenAI tool_calls 格式 |
| web_search 不可用 | 检查 enabled_toolsets + check_fn + Provider 是否支持 tools 参数 |
| Termux 安装失败 | pydantic-core / PyNaCl / cryptography 等 C 扩展 wheel 缺失 |
| 跨会话"失忆" | MEMORY.md 超 2,200 字被挤 / Hindsight 检索未命中 |
| hermes update 后行为异常 | 中途中断导致模块状态不一致，重跑完成 |
| 技能不自动使用 | 技能描述不够精确，L0 索引未命中触发条件 |

---

## CLI 命令速查

| 命令 | 作用 |
|------|------|
| `hermes` | 启动交互式终端 |
| `hermes chat` | 同上 |
| `hermes gateway start` | 启动消息网关 |
| `hermes gateway stop` | 停止网关 |
| `hermes gateway status` | 查看网关状态 |
| `hermes doctor` | 环境检测（排障入口） |
| `hermes setup` | 交互式配置向导 |
| `hermes config set <key> <value>` | 修改配置 |
| `hermes config show` | 查看当前配置 |
| `hermes update` | 从 Git 拉取并更新 |
| `hermes skills` | 技能管理（opt-in/opt-out） |
| `hermes cron` | 定时任务管理 |
| `hermes mcp serve` | 启动 MCP 服务器 |
| `hermes --version` | 版本号 |
| `hermes -z <prompt>` | 单次对话（非交互） |
| `/model` | 会话中切换模型 |
| `/reset` | 重置会话 |
| `/branch` | 分支会话 |
| `/learn` | 从当前对话创建技能 |
| `/compress` | 手动触发上下文压缩 |

---

*本文基于 NousResearch/hermes-agent v0.18.0 源码分析。*
