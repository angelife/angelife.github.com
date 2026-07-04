# Hermes Agent 架构深度分析

> 分析日期：2026-07-03 | 源码版本：0.18.0 | 仓库：NousResearch/hermes-agent  
> 分析基于本地源码 `/Users/macos/.hermes/hermes-agent/` 及官方文档 https://hermes-agent.nousresearch.com/docs

---

## 目录

1. [项目概览](#1-项目概览)
2. [项目架构与核心模块](#2-项目架构与核心模块)
3. [入口点与进程模型](#3-入口点与进程模型)
4. [配置系统](#4-配置系统)
5. [Provider 与模型路由](#5-provider-与模型路由)
6. [工具系统（Tools）](#6-工具系统tools)
7. [技能系统（Skills）](#7-技能系统skills)
8. [网关系统（Gateway）](#8-网关系统gateway)
9. [记忆系统（Memory）](#9-记忆系统memory)
10. [会话管理](#10-会话管理)
11. [Cron 调度系统](#11-cron-调度系统)
12. [MCP 集成](#12-mcp-集成)
13. [插件系统](#13-插件系统)
14. [子智能体系统](#14-子智能体系统subagent)
15. [Personality 与 SOUL.md](#15-personality-与-soulmd)
16. [部署模型](#16-部署模型)
17. [项目健康度](#17-项目健康度)
18. [已知限制与痛点](#18-已知限制与痛点)
19. [教学指南：如何理解 Hermes](#19-教学指南如何理解-hermes)

---

## 1. 项目概览

**Hermes Agent** 是 Nous Research 开发的开源自主 AI 智能体框架（MIT 协议）。它的核心理念是 **Closed Learning Loop**——智能体在对话中创造技能、在使用中自我改进、跨会话保持记忆，并持续构建用户模型。

### 关键数据

| 指标 | 数值 |
|------|------|
| Python 文件数 | 2,780 |
| 核心文件（5 个最大文件） | `cli.py` (16K 行), `gateway/run.py` (20K 行), `run_agent.py` (6K 行), `hermes_state.py` (5.8K 行), `model_tools.py` (1.2K 行) |
| Git 提交总数 | 14,215 |
| 2026 年 1-7 月提交数 | 14,155（近乎全部） |
| 最近一月主要贡献者 | Teknium (695), Brooklyn Nicholson (488), kshitijk4poor (234) |
| 核心依赖 | `openai`, `httpx`, `pydantic`, `rich`, `prompt_toolkit`, `pyyaml`, `croniter` |

### 一句话总结

> Hermes 是一个运行在 CLI、消息平台（20+）、TUI 和 Electron 桌面应用之上的自主 AI 智能体，核心是窄腰架构（narrow waist），能力通过工具、技能、插件和 MCP 在边缘扩展。

---

## 2. 项目架构与核心模块

### 整体架构（俯视图）

```
                              ┌───────────────────┐
                              │      Entry Points     │
                              │  CLI / Gateway / ACP  │
                              │  Batch / Library      │
                              └─────────┬─────────────┘
                                        │
                              ┌─────────▼─────────────┐
                              │     AIAgent Core       │
                              │    (run_agent.py)      │
                              │                        │
                              │  ┌──────────────────┐  │
                              │  │  Conversation     │  │
                              │  │  Loop (~5K 行)    │  │
                              │  └──────────────────┘  │
                              └─────────┬──────────────┘
                                        │
         ┌──────────────────────────────┼──────────────────────────────┐
         │              │                              │              │
  ┌──────▼──────┐  ┌──────▼──────┐  ┌──────────▼──────────┐  ┌───────▼───────┐
  │   Provider   │  │    Tool     │  │    Session State    │  │   Memory      │
  │   Resolution │  │   Dispatch  │  │   (SQLite + FTS5)   │  │   Manager     │
  │ (runtime_    │  │ (model_     │  │   (hermes_state.py) │  │ (memory_      │
  │ provider.py) │  │ tools.py)   │  │                     │  │ manager.py)   │
  └──────┬───────┘  └──────┬───────┘  └─────────────────────┘  └──────┬────────┘
         │                 │                                          │
         ▼                 ▼                                          ▼
  ┌──────────┐    ┌──────────────────┐                       ┌─────────────────┐
  │ Provider │    │  Tool Registry   │                       │ Memory Providers │
  │ Profiles │    │ (tools/registry) │                       │ MEMORY.md        │
  │ (20+)    │    │  + 28 Toolsets   │                       │ USER.md          │
  │          │    │  + 70+ Tools     │                       │ Honcho / Mem0    │
  └──────────┘    │  + MCP Servers   │                       └─────────────────┘
                  └──────────────────┘
```

### 目录结构

```
hermes-agent/
├── run_agent.py              # AIAgent 核心：会话循环 + 工具调度
├── cli.py                    # HermesCLI 交互式终端 UI（16K 行巨文件）
├── cli-config.yaml.example   # 完整配置模板（1,382 行）
├── model_tools.py            # 工具发现、Schema 生成、调度分发
├── toolsets.py               # 工具集分组定义（28 个 toolsets）
├── hermes_state.py           # SQLite 会话存储 + FTS5 全文搜索
├── hermes_constants.py       # 路径常量（HERMES_HOME 等）
├── hermes_bootstrap.py       # Windows UTF-8 引导 + sys.path 加固
├── hermes_logging.py         # 集中化日志（RotatingFileHandler + RedactingFormatter）
├── hermes_time.py            # 时间工具函数
├── AGENTS.md                 # AI Agent 开发指南（1,356 行）
├── mcp_serve.py              # MCP 服务端（暴露消息平台为 MCP 工具）
├── batch_runner.py           # 批量轨迹生成
│
├── agent/                    # AIAgent 内部模块
│   ├── agent_init.py         # AIAgent.__init__ 逻辑（1,921 行）
│   ├── conversation_loop.py  # 核心会话循环（5,156 行）
│   ├── prompt_builder.py     # 系统提示组装（SOUL.md, skills, context files）
│   ├── context_compressor.py # 上下文压缩（lossy summarization）
│   ├── memory_manager.py     # 记忆编排（MEMORY.md + USER.md + external providers）
│   ├── memory_provider.py    # MemoryProvider ABC
│   ├── skill_utils.py        # SKILL.md 解析、条件匹配
│   ├── skill_preprocessing.py# SKILL.md 预处理（模板变量、内联 shell）
│   ├── skill_commands.py     # 技能相关斜杠命令
│   ├── skill_bundles.py      # 技能包（bundles）管理
│   ├── auxiliary_client.py   # 辅助 LLM 调用（视觉分析、摘要等）
│   ├── model_metadata.py     # 模型上下文长度、token 估算
│   ├── chat_completion_helpers.py # 3 种 API 模式（chat/completions, codex, anthropic）
│   ├── moa_loop.py           # Mixture of Agents
│   ├── anthropic_adapter.py  # Anthropic Messages API 适配
│   ├── display.py            # 终端显示（KawaiiSpinner, 工具日志）
│   ├── iteration_budget.py   # 工具调用迭代预算
│   ├── tool_executor.py      # 工具执行器
│   ├── turn_context.py       # 回合上下文构建
│   ├── retry_utils.py        # 重试 + 退避策略
│   ├── prompt_caching.py     # Anthropic prompt caching 支持
│   └── ...
│
├── hermes_cli/               # CLI 子系统
│   ├── main.py               # 入口点：所有 `hermes` 子命令（13K 行）
│   ├── config.py             # DEFAULT_CONFIG, 配置加载/合并/override
│   ├── commands.py           # COMMAND_REGISTRY：所有斜杠命令定义
│   ├── auth.py               # PROVIDER_REGISTRY + 凭据解析
│   ├── runtime_provider.py   # Provider → api_mode + 凭据
│   ├── setup.py              # 交互式安装向导
│   ├── plugins.py            # PluginManager（4 种来源，生命周期钩子）
│   ├── gateway.py            # `hermes gateway start/stop/status`
│   ├── skills_config.py      # 平台级技能启用/禁用
│   ├── tools_config.py       # 平台级工具启用/禁用
│   ├── moa_config.py         # MoA 预设配置
│   └── ...
│
├── gateway/                  # 消息网关系统
│   ├── run.py                # GatewayRunner（20K 行，主循环 + 事件分发）
│   ├── config.py             # 网关配置（Platform, SessionResetPolicy, HomeChannel）
│   ├── session.py            # 会话管理（SessionSource, 会话键构建）
│   ├── slash_commands.py     # 42 个斜杠命令处理器（4,566 行）
│   ├── platform_registry.py  # 平台适配器注册表
│   └── platforms/            # 各个平台适配器
│       ├── telegram/adapter.py
│       ├── discord/adapter.py
│       ├── slack/adapter.py
│       ├── whatsapp/adapter.py
│       ├── email/adapter.py
│       ├── matrix/adapter.py
│       ├── feishu/adapter.py
│       ├── wecom/adapter.py
│       ├── mattermost/adapter.py
│       ├── raft/adapter.py
│       └── webhook.py + api_server.py
│
├── tools/                    # 工具实现（每个文件一个工具）
│   ├── registry.py           # 中心注册表（ToolEntry, check_fn TTL 缓存）
│   ├── terminal_tool.py      # 终端执行（local/docker/ssh/modal/daytona/singularity）
│   ├── file_tools.py         # 文件操作（read/write/patch/search）
│   ├── browser_tool.py       # 浏览器自动化（Playwright/Chrome/Camofox）
│   ├── web_tools.py          # web_search + web_extract
│   ├── vision_tools.py       # 图像分析
│   ├── memory_tool.py        # 持久记忆操作
│   ├── delegate_tool.py      # 子智能体（Subagent）
│   ├── mcp_tool.py           # MCP 客户端（集成外部 MCP 服务器）
│   ├── send_message_tool.py  # 跨平台消息发送
│   ├── skills_tool.py        # 技能发现（skills_list / skill_view）
│   ├── skill_manager_tool.py # 技能管理（skill_manage 创建/编辑）
│   ├── todo_tool.py          # 待办事项 / 计划
│   ├── kanban_tools.py       # 看板多智能体协调
│   ├── video_generation_tool.py
│   ├── xai_video_tools.py
│   └── ... (70+ 工具)
│
├── cron/                     # Cron 调度系统
│   ├── scheduler.py          # tick() 检查并执行到期任务
│   └── ... (cron job 定义)
│
├── plugins/                  # 内置插件
│   ├── platforms/            # 消息平台适配器插件
│   ├── image_gen/            # 图片生成后端
│   ├── video_gen/            # 视频生成后端
│   ├── memory/               # 外部记忆提供者（Honcho, Mem0, Holographic, Supermemory）
│   ├── model-providers/      # 模型提供者配置（vertex 等）
│   ├── web/                  # 网页搜索后端（ddgs, firecrawl）
│   ├── dashboard_auth/       # 仪表板认证
│   └── disk-cleanup/         # 磁盘清理
│
├── providers/                # Provider 注册表
│   ├── base.py               # ProviderProfile + OMIT_TEMPERATURE
│   └── __init__.py           # 发现 + 注册（bundled plugins + user plugins + legacy）
│
├── tui_gateway/              # TUI 网关（终端 UI 的 WebSocket 后端）
│   ├── server.py             # WebSocket 服务器
│   ├── ws.py                 # WebSocket 协议
│   ├── slash_worker.py       # 斜杠命令工作线程
│   └── entry.py              # TUI 入口
│
├── scripts/                  # 工具脚本
│   ├── release.py            # 发布流程
│   └── ...
│
├── tests/                    # 测试套件（136 个测试文件）
├── docs/                     # 文档
├── web/                      # Web 仪表板
├── website/                  # 项目网站
└── setup-hermes.sh           # 安装脚本（462 行）
```

---

## 3. 入口点与进程模型

### 入口点矩阵

| 入口点 | 文件 | 场景 | 进程模型 |
|--------|------|------|----------|
| `hermes` (CLI 默认) | `cli.py` → `__main__` | 交互式终端对话 | 前台单进程，prompt_toolkit 事件循环 |
| `hermes chat` | `cli.py` | 同上 | 同上 |
| `hermes gateway` | `gateway/run.py` | 消息平台网关 | asyncio 事件循环 + 后台 agent 缓存 |
| `hermes gateway start` | `hermes_cli/gateway.py` | 后台守护进程 | 子进程 + systemd/launchd |
| `hermes setup` | `hermes_cli/setup.py` | 安装向导 | 临时进程 |
| `python -m gateway.run` | `gateway/run.py` | 直接运行网关 | asyncio 事件循环 |
| `hermes acp` | `acp_adapter/` | ACP 服务器（编辑器集成） | stdio 协议 |
| `hermes mcp serve` | `mcp_serve.py` | MCP 服务器 | stdio MCP 协议 |
| `batch_runner.py` | 独立脚本 | 批量轨迹生成 | 批量非交互 |
| Python 库模式 | `from run_agent import AIAgent` | 程序化调用 | 调用方决定 |

### 启动流程

```
任何入口点
    │
    ▼
import hermes_bootstrap         # Windows UTF-8 修复 + sys.path 加固
    │
    ▼
setproctitle("hermes")          # 设置进程名
    │
    ▼
hermes_logging.setup_logging()  # 日志初始化（agent.log, errors.log, gateway.log）
    │
    ▼
hermes_cli.config.load_config() # 加载 ~/.hermes/config.yaml
    │
    ▼
AIAgent.__init__()              # 初始化（~60 个参数，1,400 行）
    ├── Provider 解析（auto-detect from credentials）
    ├── 凭据解析（.env → auth.json → config.yaml）
    ├── Tool 发现（import 所有 tools/*.py）
    ├── 上下文引擎选择（compressor / Anthropic caching）
    ├── 记忆提供者初始化（local MEMORY.md + external providers）
    ├── 技能索引（遍历 ~/.hermes/skills/）
    └── 会话恢复（SQLite state.db）
    │
    ▼
conversation_loop.py            # 核心会话循环
    ├── System Prompt 组装
    │   ├── SOUL.md（基础身份）
    │   ├── AGENTS.md（任务角色）
    │   ├── .cursorrules（项目规则）
    │   ├── Platform 上下文（来自哪个平台）
    │   ├── 记忆注入（MEMORY.md + USER.md）
    │   ├── 技能索引（progressive disclosure）
    │   └── /personality 覆盖
    ├── 工具定义注入（按 enabled/disabled toolsets 过滤）
    ├── Provider API 调用（chat completions / codex / anthropic）
    ├── 工具循环（自动 tool calling → 结果 → 继续 → 直到完成）
    ├── 后处理（记忆同步、技能学习 nudge、轨迹保存）
    └── 会话持久化（SQLite）
```

### 进程模型关键设计

1. **CLI 模式**：同步单进程，使用 `prompt_toolkit` 的事件循环处理键盘输入
2. **Gateway 模式**：异步 asyncio 事件循环，每个平台适配器作为独立 task 运行
3. **Agent 缓存**：`gateway/run.py` 维护 LRU 缓存（128 个 agent），1 小时空闲 TTL
4. **工具异步桥接**：`model_tools.py::_run_async()` 是同步→异步的唯一桥接点，有三种模式：
   - 无运行中事件循环 → 持久化全局事件循环
   - 已在异步上下文 → 新线程 + 独立循环
   - 工作线程 → 线程本地持久化循环

---

## 4. 配置系统

### 配置文件和加载链

```
加载优先级（高→低）：
1. CLI 参数（--model, --provider 等）
2. ~/.hermes/config.yaml（主配置）
3. ~/.hermes/.env（密钥）
4. ~/.hermes/auth.json（OAuth 凭据）
5. 内建默认值（DEFAULT_CONFIG）

环境变量替换：
  config.yaml 支持 ${VAR} 语法
  undefined 变量保持原样
```

### 配置结构（config.yaml 主要字段）

```yaml
model:               # 模型配置
  default:           # 默认模型
  provider:          # 提供者选择 (auto/anthropic/openai-codex/...)
  base_url:          # API 端点
  api_key:           # API 密钥（不推荐，应放 .env）
  context_length:    # 上下文窗口（自动检测）
  max_tokens:        # 输出上限
  default_headers:   # 自定义 HTTP 头
  ollama_num_ctx:    # Ollama 上下文长度

providers:           # 命名提供者覆盖
  <name>:            # 自定义提供者别名
    base_url:
    key_env:         # 环境变量名
    extra_headers:
    request_timeout_seconds:
    stale_timeout_seconds:
    models:
      <model>:       # 按模型覆盖

custom_providers:    # 自定义提供者列表
  - name:
    provider_key:
    base_url:
    model:
    extra_body:

terminal:            # 终端后端
  backend:           # local/docker/ssh/modal/daytona/singularity
  docker_image:
  timeout:
  # ... 大量 docker/ssh/modal 配置

agent:              # 智能体行为
  disabled_toolsets:  # 禁用的工具集
  personalities:      # 自定义人格定义
  system_prompt_extra: # 额外系统提示

tools:              # 工具配置
  <tool_name>:
    enabled:         # 启用/禁用

gateway:            # 消息网关
  platforms:        # 平台配置
    telegram:
      bot_token:
    discord:
      bot_token:
    # ... 20+ 平台

mcp_servers:        # MCP 服务器
  <name>:           # 服务器名
    command:        # stdio 命令
    args:           # 参数
    url:            # HTTP 端点
    transport:      # stdio/http/sse
    timeout:
    env:           # 环境变量

memory:            # 记忆配置
  memory_enabled:
  user_profile_enabled:
  memory_char_limit: 2200
  user_char_limit: 1375
  write_approval:

skills:            # 技能配置
  enabled:         # 启用技能列表
  disabled:        # 禁用技能列表
  external_dirs:   # 额外技能目录

cron:              # 定时任务
  jobs:
    - name:
      schedule:   # cron 表达式或 interval
      prompt:
      platform:  # 交付平台
```

### 配置合并机制

- `hermes_cli/config.py` 中的 `load_config()` 负责加载和合并
- 密钥优先读取 `.env`（dotenv 加载），其次 `config.yaml`
- `hermes config set` 自动路由：密钥 → `.env`，其余 → `config.yaml`
- `fallback_config.py` 实现 fallback chain 提供者配置

---

## 5. Provider 与模型路由

### Provider 架构

```
config.yaml 中 model.provider = "auto"
    │
    ▼
hermes_cli/auth.py → PROVIDER_REGISTRY
    ├── "auto" → 扫描所有可用凭据，选择第一个可用提供者
    ├── "anthropic" → 检查 ANTHROPIC_API_KEY
    ├── "openai-codex" → 检查 codex OAuth
    ├── "openrouter" → 检查 OPENROUTER_API_KEY
    ├── "gemini" → 检查 GOOGLE_API_KEY
    ├── "custom" → 使用 base_url + 用户提供密钥
    └── ... (30+ 内建提供者)
    │
    ▼
hermes_cli/runtime_provider.py → 解析 api_mode
    ├── api_mode = "chat_completions" (OpenAI 兼容)
    ├── api_mode = "codex_responses" (OpenAI Codex Responses API)
    └── api_mode = "anthropic" (Anthropic 原生 API)
    │
    ▼
AIAgent.__init__ → 创建 LLM 客户端
    ├── OpenAI-wire: openai.OpenAI()
    ├── Anthropic: anthropic.Anthropic()
    └── Codex: 专用适配器
```

### Provider 配置文件

Provider profiles 有两种来源：

1. **内建**（`providers/*.py`）：直接硬编码在源码中
2. **插件**（`plugins/model-providers/<name>/`）：通过 `register_provider(profile)` 注册

```
providers/
├── __init__.py     # 注册表 + 发现逻辑
├── base.py         # ProviderProfile 数据类 + OMIT_TEMPERATURE 哨兵

plugins/model-providers/
└── vertex/         # Google Vertex AI 提供者
    ├── __init__.py
    └── plugin.yaml
```

每个 `ProviderProfile` 包含：
- `name`（如 "anthropic"）
- `aliases`（如 "claude"）
- `base_url` 默认值
- `api_mode`（chat_completions / anthropic 等）
- `env_keys`（需要哪些环境变量）
- `models` 白名单/黑名单

### Fallback 链

当主提供者失败时（网络错误、rate limit、token 耗尽等），Hermes 自动尝试 fallback：

```python
# fallback_config.py 中 get_fallback_chain() 实现
# 从 config.yaml 的 agent.fallback_providers 读取
# 每个 fallback 可以有不同的提供者、模型、base_url
# 在 conversation_loop.py 的 retry 逻辑中被调用
```

### Provider 路由覆盖

```yaml
providers:
  my-proxy:
    base_url: "https://llm.internal.example.com/v1"
    key_env: "MY_PROXY_API_KEY"
    extra_headers:
      CF-Access-Client-Id: "xxxx.access"
    request_timeout_seconds: 300
    models:
      claude-opus-4.6:
        timeout_seconds: 600  # 按模型覆盖
```

---

## 6. 工具系统（Tools）

### 架构概览

```
工具发现链路：
tools/terminal_tool.py           # 每个工具文件
  └── registry.register(...)     # 模块级注册
        │
tools/registry.py                # 中心注册表
  ├── ToolEntry(name, schema, handler, check_fn, toolset...)
  ├── discover_builtin_tools()   # 扫描 tools/*.py 并 import
  └── _check_fn_cached()         # check_fn TTL 缓存（30s）+ 故障容错（60s 窗口）
        │
model_tools.py                   # 调度层
  ├── get_tool_definitions()     # 过滤 + 生成 OpenAI 工具 schema
  ├── handle_function_call()     # 分配 + 执行
  └── _run_async()               # sync→async 桥接
        │
toolsets.py                      # 工具集定义
  ├── TOOLSETS = {               # 28 个工具集
  │   "web": [...],
  │   "code": [...],
  │   "full_stack": [...],
  │   "research": [...],
  │   "terminal": [...],
  │   "skills": [...],
  │   "messaging": [...],
  │   ...
  │ }
  ├── resolve_toolset()          # 递归展开工具集包含关系
  └── _HERMES_CORE_TOOLS         # 默认核心工具（50+）
```

### ToolEntry 结构

```python
@dataclass
class ToolEntry:
    name: str                    # 工具名（如 "terminal"）
    toolset: str                 # 所属工具集（如 "terminal"）
    schema: dict                 # OpenAI 函数 schema
    handler: Callable            # 处理函数
    check_fn: Callable           # 可用性检查（返回 bool）
    requires_env: list           # 需要哪些环境变量
    is_async: bool               # 是否异步
    description: str             # 描述
    emoji: str                   # 显示用 emoji
    max_result_size_chars: int   # 结果大小上限
    dynamic_schema_overrides:    # 运行时 schema 覆盖
```

### 工具注册示例

```python
# tools/send_message_tool.py
registry.register(
    name="send_message",
    toolset="messaging",
    schema={...},          # OpenAI 函数定义
    handler=send_message_tool,
    check_fn=_check_capabilities,
    requires_env=[],
    is_async=True,
    description="Send a message to a user or channel",
    emoji="📤",
)
```

### 工具集的调用过滤

```
get_tool_definitions(enabled_toolsets, disabled_toolsets, quiet_mode)
  │
  ├── 按 enabled_toolsets 过滤（只包含允许的工具集）
  ├── 按 disabled_toolsets 移除（显式禁用的工具集）
  ├── 对每个工具调用 check_fn 检查可用性
  │   └── Docker 不可用 → terminal/docker 工具隐藏
  │   └── Playwright 未安装 → browser 工具隐藏
  └── 返回最终工具列表 → 注入 API 请求
```

### 工具调用时序

```
User: "帮我查一下天气"
    │
    ▼
AIAgent.run_conversation()
    │
    ├── 1. API 调用（包含工具定义）
    │    model 返回 tool_call: web_search({"query": "weather today"})
    │
    ├── 2. model_tools.handle_function_call("web_search", args)
    │    ├── registry.dispatch("web_search", args)
    │    │   └── 查找 ToolEntry → 调用 handler
    │    └── 获取结果（工具返回字符串）
    │
    ├── 3. 将结果注入消息历史（tool 角色消息）
    │
    ├── 4. 再次 API 调用（带工具结果）
    │    model 返回: "今天天气晴朗，25°C"
    │
    └── 5. 循环结束或继续工具调用（max_iterations=90）
```

### 工具类型分类

| 类别 | 工具 | 后端/实现 |
|------|------|----------|
| **终端** | terminal, process | local/docker/ssh/modal/daytona/singularity |
| **文件** | read_file, write_file, patch, search_files | 本地文件系统 + 安全过滤 |
| **Web** | web_search, web_extract | duckduckgo/firecrawl/exa/jina |
| **浏览器** | browser_navigate, browser_snapshot, browser_click... | Playwright/Chrome/Camofox |
| **视觉** | vision_analyze | 辅助 LLM（GPT-4o-mini, Gemini, Claude） |
| **图像** | image_generate | OpenAI Codex/xAI/OpenRouter |
| **视频** | video_generate, xai_video_edit, xai_video_extend | xAI |
| **代码** | execute_code | 隔离沙箱 |
| **技能** | skills_list, skill_view, skill_manage | ~/.hermes/skills/ |
| **记忆** | memory | MEMORY.md + USER.md |
| **MCP** | mcp_* | 动态 MCP 服务器注册 |
| **子智能体** | delegate_task | 线程池 + 独立 AIAgent |
| **消息** | send_message | 跨平台消息 |
| **Cron** | cronjob | cron 调度器 |
| **看板** | kanban_* | 多智能体协调 |
| **会话** | session_search | SQLite FTS5 |
| **待办** | todo | 计划/待办事项 |
| **TTS** | text_to_speech | 文本转语音 |
| **智能家居** | ha_* | Home Assistant |
| **计算机操作** | computer_use | macOS CUA |

---

## 7. 技能系统（Skills）

### 核心概念

技能是**按需加载的知识文档**，采用**渐进式披露**（Progressive Disclosure）模式以最小化 token 消耗。

```
发现层级（token 消耗递增）：
Level 0: skills_list() → [{name, description, category}]    (~3K tokens)
Level 1: skill_view(name) → 完整内容 + 元数据               (~时敏加载)
Level 2: skill_view(name, path) → 特定引用文件                (~按需)
```

### SKILL.md 格式

```markdown
---
name: my-skill
description: Brief description
version: 1.0.0
platforms: [macos, linux]        # 可选 — 限制操作系统
metadata:
  hermes:
    tags: [python, automation]
    category: devops
    fallback_for_toolsets: [web]  # 可选 — 条件激活
    requires_toolsets: [terminal] # 可选 — 条件激活
config:
  - key: my.setting
    description: "What this controls"
    default: "value"
    prompt: "Prompt for setup"
required_environment_variables:
  - name: TENOR_API_KEY
    prompt: "Tenor API key"
    help: "Get a key from ..."
---

# Skill Title
## When to Use
## Procedure
## Pitfalls
## Verification
```

### 技能加载链路

```
AIAgent.__init__()
    │
    ▼
agent/prompt_builder.py
    │
    ├── get_all_skills_dirs()       # 获取所有技能目录
    │   ├── ~/.hermes/skills/       # 主技能目录
    │   └── external_dirs            # 外部技能目录（config.yaml）
    │
    ├── iter_skill_index_files()    # 遍历所有 SKILL.md
    │   ├── 解析 YAML 前置元数据
    │   ├── skill_matches_platform() # 检查平台兼容性
    │   └── skill_matches_environment() # 检查环境条件
    │
    ├── extract_skill_description()  # 提取描述（Level 0 索引）
    └── 注入系统提示
        └── "技能索引：name - description /skills_list 查看详情 /skill_view <name> 加载"

运行时：
    model 调用 skills_list() → 返回索引
    model 调用 skill_view("my-skill") → 加载完整内容
    model 调用 skill_manage() → 创建/编辑技能
```

### 技能条件激活

```yaml
metadata:
  hermes:
    fallback_for_toolsets: [web]    # 当 web 工具集可用时隐藏此技能
    requires_toolsets: [terminal]   # 仅当 terminal 工具集存在时显示
```

### 技能管理

- `/learn` 命令：从对话中自动提取知识创建 SKILL.md
- `skill_manage` 工具：AI 自主创建/编辑/删除技能
- `hermes skills` CLI：opt-out/opt-in 控制
- **Skill Bundles**：`hermes bundles create` 将多个技能组合为一个命令

### 模板变量

```markdown
${HERMES_SKILL_DIR}    # 技能目录路径
${HERMES_SESSION_ID}   # 当前会话 ID
!`date +%Y-%m-%d`      # 内联 shell 命令
```

---

## 8. 网关系统（Gateway）

### 架构

```
GatewayRunner (gateway/run.py)
    │
    ├── asyncio 事件循环
    │
    ├── 平台适配器（每个平台一个 asyncio Task）
    │   ├── telegram/adapter.py    → Telegram Bot API (长轮询)
    │   ├── discord/adapter.py     → Discord Gateway API (WebSocket)
    │   ├── slack/adapter.py       → Slack Events API
    │   ├── whatsapp/adapter.py    → WhatsApp Cloud API
    │   ├── email/adapter.py       → IMAP + SMTP
    │   ├── matrix/adapter.py      → Matrix 协议
    │   ├── feishu/adapter.py      → 飞书
    │   ├── wecom/adapter.py       → 企业微信
    │   └── ... (20+ 平台)
    │
    ├── 会话存储（SessionStore）
    │   ├── sessions.json → 会话路由索引
    │   └── state.db → SQLite 消息历史
    │
    ├── Agent 缓存（LRU, 128 个, 1h TTL）
    │
    └── 斜杠命令分发（gateway/slash_commands.py）
        ├── /model, /reset, /new, /branch
        ├── /usage, /compress, /history
        ├── /background, /agents, /stop
        └── ... (42 个命令)
```

### 消息流

```
用户发送消息
    │
    ▼
平台适配器接收事件
    │
    ▼
GatewayRunner._handle_message()
    ├── 验证用户授权（_is_user_authorized）
    ├── 解析 SessionSource（platform, chat_id, user_id...）
    ├── 构建会话键（session_key = build_session_key(source)）
    ├── 获取/创建会话
    ├── 检查重置策略（SessionResetPolicy）
    ├── 获取/创建 AIAgent（从缓存或新建）
    ├── 注入系统提示中的平台上下文
    └── AIAgent.run_conversation(message)
        │
        ▼
    响应返回
        │
        ▼
    GatewayRunner.deliver_response()
        ├── 平台适配器.send_message()
        ├── 支持长消息分块
        ├── 支持富文本格式
        └── 支持消息编辑（更新已有消息）
```

### 平台注册表

`gateway/platform_registry.py` 定义了 `PlatformEntry` 数据类，允许插件动态注册新平台：

```python
platform_registry.register(PlatformEntry(
    name="irc",
    label="IRC",
    adapter_factory=lambda cfg: IRCAdapter(cfg),
    check_fn=check_requirements,
    validate_config=lambda cfg: bool(cfg.extra.get("server")),
    required_env=["IRC_SERVER"],
    install_hint="pip install irc",
))
```

### 支持平台列表

| 平台 | 通信方式 | 适配器类型 |
|------|---------|-----------|
| Telegram | Bot API 长轮询 | 内置 |
| Discord | Gateway WebSocket | 内置 |
| Slack | Events API / Socket Mode | 内置 |
| WhatsApp | Cloud API | 内置 |
| Signal | Signal Messenger API | 内置 |
| Matrix | Matrix 协议 | 内置 |
| Email | IMAP + SMTP | 内置 |
| WeChat (微信) | 微信公众平台 | 内置 |
| WeCom (企业微信) | 企微 API | 内置 |
| Feishu (飞书) | 飞书 API | 内置 |
| DingTalk (钉钉) | 钉钉机器人 | 内置 |
| QQ Bot | QQ 机器人 | 内置 |
| Mattermost | Mattermost API | 内置 |
| Webhook | HTTP | 内置 |
| API Server | REST | 内置 |
| TUI | WebSocket | 内置 |
| CLI | 本地终端 | 内置 |
| Teams | Microsoft Teams | 内置 |
| Google Chat | Google Chat API | 内置 |
| BlueBubbles | iMessage | 内置 |
| Home Assistant | HA API | 内置 |

---

## 9. 记忆系统（Memory）

### 架构

```
MemoryManager (agent/memory_manager.py)
    │
    ├── 内置记忆（local memory provider）
    │   ├── MEMORY.md（智能体个人笔记，2,200 字符上限）
    │   └── USER.md（用户画像，1,375 字符上限）
    │
    ├── 外部记忆提供者（最多一个同时激活）
    │   ├── Honcho（辩证用户建模）
    │   ├── Mem0
    │   ├── Supermemory
    │   └── Holographic（知识图谱）
    │
    ├── 会话搜索（SQLite FTS5）
    │   └── 全文搜索所有历史消息
    │
    └── Background Review（后台审查 nudge）
        └── 辅助 LLM 定期审查并提醒更新记忆
```

### 记忆注入时机

```
会话开始（AIAgent.__init__）
    │
    ├── 1. 读取 MEMORY.md + USER.md
    ├── 2. 构建记忆上下文块
    │   ╔═══════════════════════════════════════╗
    │   ║ MEMORY (your personal notes) [67%]    ║
    │   ║ User's project is Rust web service... ║
    │   ║ User prefers concise responses        ║
    │   ╚═══════════════════════════════════════╝
    ├── 3. 注入系统提示（slot #2，紧接身份其后）
    │
会话中（每个回合）
    │
    ├── prefetch_all(user_message)    # 回合前获取相关记忆
    └── sync_all(user_msg, assistant) # 回合后同步更新
```

### 记忆工具

```yaml
memory:
  memory_enabled: true
  user_profile_enabled: true
  memory_char_limit: 2200
  user_char_limit: 1375
  write_approval: false    # false = AI 自由写入，true = 需人类批准
```

`memory` 工具支持的操作：
- `add` — 添加新条目
- `replace` — 替换现有条目（需子串匹配）
- `remove` — 删除条目（需子串匹配）

### 上下文安全

- `StreamingContextScrubber`：流式输出中实时剥离 `<memory-context>` 标记
- `sanitize_context()`：后处理移除注入的记忆标记
- 跨会话注入保护：`memory-context` fence tag 自动清理

---

## 10. 会话管理

### 会话生命周期

```
创建 (get_or_create_session)
    │  ← 根据 platform + chat_id + user_id 构建 session_key
    │
    ▼
SQLite 存储（SessionDB, hermes_state.py）
    ├── sessions 表：metadata, model_config, started_at, ended_at
    ├── messages 表：role, content, tool_calls, timestamp
    └── FTS5 虚拟表：全文搜索
    │
    ▼
自动压缩（context_compressor.py）
    ├── 当上下文超过阈值时触发
    ├── 创建子会话（parent_session_id 链）
    └── 旧消息摘要化，保留关键信息
    │
    ▼
分支（/branch 或 /fork）
    ├── 创建独立子会话
    ├── 带着完整历史复制
    └── 标记 _branched_from
    │
    ▼
恢复（/resume）
    ├── 通过 session_search 查找
    ├── 重新加载完整消息历史
    └── 重建 AIAgent 状态
    │
    ▼
结束（end_reason: done/compression/branched/interrupted）
```

### SQLite 设计

```python
# 数据库路径：~/.hermes/state.db
# WAL 模式（并发读 + 单写）
# FTS5 全文搜索
# SCHEMA_VERSION = 17

# 关键表
sessions:
  - id (TEXT PRIMARY KEY)
  - parent_session_id (TEXT)    # 压缩/分支父会话
  - started_at (TEXT)
  - ended_at (TEXT)
  - end_reason (TEXT)           # done/compression/branched
  - model_config (JSON)
  - platform (TEXT)
  - chat_id (TEXT)
  - title (TEXT)
  - cwd (TEXT)

messages:
  - id (INTEGER PRIMARY KEY)
  - session_id (TEXT)
  - role (TEXT)                 # system/user/assistant/tool
  - content (TEXT)
  - tool_calls (JSON)
  - timestamp (TEXT)
  - turn_number (INTEGER)
```

### 会话键构建

```python
def build_session_key(source: SessionSource) -> str:
    # "agent:main:telegram:12345:67890"
    # "agent:main:discord:guild_id:channel_id"
    # "agent:main:cli:cwd_hash"
    # 支持 multi-user session（共享聊天）
```

### 会话压缩

```yaml
compression:
  enabled: true
  threshold: 0.75       # 上下文使用率达到 75% 时触发
  summarization: true   # 使用 LLM 摘要旧消息
  model: "auto"         # 可选特定压缩模型
```

---

## 11. Cron 调度系统

### 架构

```
cron/scheduler.py
    │
    ├── tick() — 主调度函数
    │   ├── 文件锁（~/.hermes/cron/.tick.lock）
    │   ├── 扫描 cron/ 目录下的 .yaml 文件
    │   ├── 检查到期任务（croniter 解析 cron 表达式）
    │   └── 执行到期任务
    │
    ├── Cron job 定义（YAML）
    │   ├── name: job 名称
    │   ├── schedule: cron 表达式 或 interval 秒
    │   ├── prompt: 发送给 AI 的提示
    │   ├── platform: 交付平台（telegram/discord/cli...）
    │   └── chat_id: 交付目标
    │
    └── 执行流程
        ├── 构建 AIAgent（非交互模式）
        ├── 禁用 cronjob/messaging/clarify 工具集
        ├── 运行 prompt
        ├── 收集结果
        └── 交付到指定平台
```

### Cron 执行安全

```python
# 自动禁用的工具集（防止递归/交互）
_RESOLVE_CRON_DISABLED_TOOLSETS = ["cronjob", "messaging", "clarify"]
# 再加上用户 config.yaml 中的 agent.disabled_toolsets
```

### 执行频率

- gateway 每 60 秒调用一次 `tick()`
- 文件锁防止多进程重叠执行
- 错误摘要（rate limit / auth / timeout）分级交付

---

## 12. MCP 集成

### Hermes 作为 MCP 客户端

```yaml
# config.yaml
mcp_servers:
  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_TOKEN: "${GITHUB_TOKEN}"
    supports_parallel_tool_calls: true
  remote_api:
    url: "https://my-mcp-server.example.com/mcp"
    headers:
      Authorization: "Bearer sk-..."
```

### MCP 客户端架构

```
tools/mcp_tool.py
    │
    ├── 后台事件循环（_mcp_loop）
    │   ├── 每个 MCP 服务器独立 asyncio Task
    │   ├── 支持 stdio/HTTP/SSE 传输
    │   └── 自动重连（指数退避，最多 5 次）
    │
    ├── 工具注册
    │   ├── MCP 服务器列出工具 → 调用 registry.register()
    │   ├── 工具名前缀 "mcp_<server_name>_<tool_name>"
    │   └── on_shutdown → 优雅关闭所有 Task
    │
    └── 采样支持（MCP Sampling）
        ├── MCP 服务器可以请求 LLM 补全
        ├── rate limiting（max_rpm）
        └── 审计日志
```

### Hermes 作为 MCP 服务器

`mcp_serve.py` 暴露 Hermes 消息平台为 MCP 工具：

```
工具列表：
  conversations_list    — 列出活跃会话
  conversation_get     — 获取会话详情
  messages_read        — 读取消息历史
  messages_send        — 发送消息
  events_poll          — 轮询新事件
  events_wait          — 等待事件
  attachments_fetch    — 获取附件
  permissions_list_open — 列出待批准请求
  permissions_respond  — 响应批准请求
  channels_list        — 列出可用频道
```

---

## 13. 插件系统

### 插件来源（4 种）

```
优先级（低→高）：
1. Bundled plugins  — <repo>/plugins/<name>/    # 随 Hermes 发布
2. User plugins     — ~/.hermes/plugins/<name>/  # 用户安装
3. Project plugins  — ./.hermes/plugins/<name>/  # 项目级
4. Pip plugins      — entry_point group          # pip 安装
```

### 插件结构

```
my-plugin/
├── plugin.yaml      # 名称、版本、种类、依赖
│   name: my-plugin
│   kind: generic    # 或: model-provider / platform / memory / web
│   version: 1.0.0
│   description: ...
│   dependencies: [pip: "some-package>=1.0"]
│
└── __init__.py      # 必须包含 register(ctx) 函数
    def register(ctx: PluginContext):
        # 注册工具
        ctx.register_tool(name, schema, handler)
        # 注册平台适配器
        ctx.register_platform(PlatformEntry(...))
        # 注册生命周期钩子
        ctx.register_hook("pre_tool_call", my_hook)
        # 注册记忆提供者
        ctx.register_memory_provider(MyMemoryProvider())
```

### 生命周期钩子

```python
VALID_HOOKS = {
    "pre_tool_call",           # 工具调用前
    "post_tool_call",          # 工具调用后
    "transform_terminal_output", # 终端输出转换
    "transform_tool_result",   # 工具结果转换
    "transform_llm_output",    # LLM 输出转换
    "pre_llm_call",            # LLM 调用前
    "post_llm_call",           # LLM 调用后
    "verification_gate",       # 验证循环门控
    "on_agent_init",           # 智能体初始化
    "on_session_start",        # 会话开始
    "on_session_end",          # 会话结束
}
```

### 内置插件种类

| 类别 | 插件 | 功能 |
|------|------|------|
| **Platform** | telegram, discord, slack, whatsapp... | 消息平台适配器 |
| **Model Provider** | vertex | 模型提供者配置 |
| **Memory** | honcho, mem0, holographic, supermemory | 外部记忆提供者 |
| **Image Gen** | openai-codex, openrouter, xai | 图片生成后端 |
| **Video Gen** | xai | 视频生成后端 |
| **Web** | firecrawl, ddgs | 网页搜索后端 |
| **Other** | disk-cleanup, dashboard_auth | 工具/服务 |

---

## 14. 子智能体系统（Subagent）

### delegate_task 工具

子智能体是 Hermes 实现并行工作隔离的核心机制。

```python
# tools/delegate_tool.py
registry.register(
    name="delegate_task",
    toolset="code",
    handler=delegate_task_handler,
    ...
)
```

### 生命周期

```
主 Agent 调用 delegate_task({prompt, toolsets, ...})
    │
    ├── ThreadPoolExecutor 创建工作线程
    ├── 创建独立 AIAgent（新实例，新会话）
    │   ├── 继承主 Agent 的配置（provider, model...）
    │   ├── 拥有独立工具集
    │   ├── 拥有独立会话（SQLite state.db）
    │   └── 标记 _delegate_from = <parent_session_id>
    │
    ├── 执行任务（最多 90 轮工具调用）
    │
    ├── 返回结果（文本摘要）
    │
    └── 清理
        ├── 子会话标记为 ephemeral（可级联删除）
        ├── 线程池关闭
        └── 独立事件循环关闭
```

### 配置

```yaml
delegation:
  max_concurrent_children: 5    # 最大并行子智能体数
  max_spawn_depth: 3            # 最大嵌套深度（子智能体再创建子智能体）
  default_model: ""             # 默认子智能体模型（默认同父）
  task_timeout: 300             # 任务超时（秒）
```

### 异步委托

```python
# tools/async_delegation.py
# 支持异步（非阻塞）子智能体调用
# 主 Agent 继续工作，子智能体完成后通知
```

---

## 15. Personality 与 SOUL.md

### 身份堆叠

```
系统提示组装顺序：
1. SOUL.md（基础身份，slot #1）
   └── ~/.hermes/SOUL.md → "$HERMES_HOME/SOUL.md"
   默认："You are Hermes Agent, an intelligent AI assistant created by Nous Research..."

2. AGENTS.md（开发指南/任务角色，slot #2）
   └── 项目仓库中的 AGENTS.md 或 .hermes.md

3. .cursorrules（项目规则，slot #3）
   └── 项目 .cursorrules 文件

4. /personality 覆盖（临时，slot #4）
   ├── 预定义: helpful/concise/technical/creative/teacher/...
   └── 自定义: config.yaml agent.personalities.<name>

5. 平台上下文（自动注入）
6. 记忆（MEMORY.md + USER.md）
7. 技能索引
8. 额外系统提示（config.yaml agent.system_prompt_extra）
```

### 预定义人格

```
/personality technical    → 详细、精确的技术专家
/personality concise      → 简洁明了
/personality creative     → 创新思维
/personality teacher      → 耐心教导
/personality kawaii       → 可爱风格
/personality catgirl      → 猫娘
/personality pirate       → 海盗
/personality shakespeare  → 莎士比亚
/personality noir         → 黑色侦探
/personality philosopher  → 哲学家
/personality hype         → 热情洋溢
```

### SOUL.md 安全

- 注入扫描：`SOUL.md` 内容经过 `scan_for_threats(scope="context")` 扫描
- 如果包含 prompt injection 模式，内容被 `[BLOCKED]` 替换
- 安全 fallback：空/无效文件使用默认身份

---

## 16. 部署模型

### 常规部署（Mac/Linux）

```bash
# 官方安装脚本
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
# 安装脚本（setup-hermes.sh）：
#   1. 安装 uv（如果未安装）
#   2. uv venv --python 3.11
#   3. uv pip install -e .
#   4. 创建 ~/.hermes/ 目录结构
#   5. 复制 .env.example → .env
#   6. 创建 ~/.local/bin/hermes 符号链接
#   7. 运行设置向导

# 手动安装
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent
uv venv -p 3.11
source .venv/bin/activate
uv pip install -e ".[dev]"
```

### 多个终端后端

| 后端 | 隔离级别 | 适用场景 |
|------|---------|----------|
| local | 无 | 开发、个人使用 |
| docker | 完整（namespace, cap-drop） | 安全沙箱、CI/CD |
| ssh | 网络边界 | 远程开发、强大硬件 |
| modal | 云 VM | 临时云端计算 |
| daytona | 云容器 | 托管云端开发环境 |
| singularity | namespace | HPC、共享机器 |

### Docker 后端深度

```yaml
terminal:
  backend: docker
  docker_image: "nikolaik/python-nodejs:python3.11-nodejs20"
  docker_run_as_host_user: true
  docker_mount_cwd_to_workspace: true
  docker_forward_env: ["GITHUB_TOKEN"]
  docker_volumes:
    - "/home/user/projects:/workspace/projects"
  container_cpu: 1
  container_memory: 5120
  timeout: 180
```

- **单一容器**：所有 Hermes 进程共享（session、/new、delegate_task）
- **持久化工作空间**：`/workspace` 跨调用持久
- **容器生命周期**：标签标记（`hermes-agent=1`），退出自动清理
- **安全加固**：`--cap-drop ALL`, `--security-opt no-new-privileges`, `--pids-limit 256`

### Android/Termux 部署

```bash
pkg install python git
pip install uv
uv venv -p 3.11
source .venv/bin/activate
uv pip install -e .
```

特殊考虑：
- 使用 `pip` 而非 uv（bionic libc 与 C 扩展的兼容性问题）
- `constraints-termux.txt` 提供了 termux 特殊的依赖约束
- ADB 集成用于 Android 设备管理
- 终端工具在 Termux 中工作正常（无额外隔离）

### 多设备 / 多 Profile

```bash
hermes profile create work --model anthropic/claude-opus-4.6
hermes profile create research --provider openai-codex
hermes profile switch work    # 切换当前 profile
```

每个 profile 独立的：
- `~/.hermes/profiles/<name>/` 目录
- `config.yaml`、`.env`、`auth.json`
- `skills/`、`memories/`、`cron/`
- `state.db`（独立 SQLite 数据库）

### 安装脚本构成

`setup-hermes.sh`（462 行）：
1. **平台检测**：Termux vs 常规
2. **依赖安装**：uv 或 venv + pip
3. **Python 检查**：需要 3.11+
4. **虚拟环境创建**：uv venv -p 3.11
5. **依赖安装**：uv pip install -e .（按平台选择 extra）
6. **环境配置**：复制 .env.example → .env
7. **符号链创建**：ln -s hermes → ~/.local/bin/hermes
8. **设置向导**：hermes setup（可选）

---

## 17. 项目健康度

### 开发活跃度

| 指标 | 数值 |
|------|------|
| 总提交数 | 14,215 |
| 2026 年 1-7 月提交数 | ~14,155 |
| 日均提交（6月） | ~47/天 |
| 活跃贡献者（6月） | 15+ |
| 主要贡献者（6月） | Teknium(695), Brooklyn Nicholson(488), kshitijk4poor(234) |
| 代码规范性 | Conventional Commits（feat/fix/refactor/chore/docs/test） |

### 提交质量分析

```
提交特征：
- feat(gateway): 网关功能（频繁）
- fix(desktop): 桌面端修复（活跃）
- fix(browser): 浏览器工具修复
- refactor(image-gen): 大规模重构
- test(codex): 测试覆盖率持续增加
- chore: 代码库维护（author_map, release）
```

### 代码质量信号

1. **严格的依赖锁定**：`pyproject.toml` 中所有核心依赖使用 `==X.Y.Z` 精确锁定
2. **安全优先**：`SECURITY.md`（15K 字），`tools/threat_patterns.py` 威胁检测
3. **跨平台支持**：macOS, Linux, Windows, Termux，docker
4. **测试覆盖**：`tests/` 目录 136 个文件，包含单元测试和集成测试
5. **文档详尽**：`AGENTS.md`（71K 字开发指南），文档站 30+ 页面
6. **国际化**：`locales/` 多语言支持
7. **CI/CD**：`.github/` workflows，Docker 构建

---

## 18. 已知限制与痛点

### 源码层面

| 痛点 | 详情 |
|------|------|
| **巨文件问题** | `cli.py`（16K 行）、`gateway/run.py`（20K 行）、`run_agent.py`（6K 行）— 虽在逐步分解，但仍很庞大 |
| **配置复杂度** | `cli-config.yaml.example` 1,382 行，字段间相互依赖复杂，新手容易配置错误 |
| **Windows 兼容性** | `hermes_bootstrap.py` 专门解决 Windows UTF-8 问题，日志轮换也需要 Windows 特殊处理 |
| **C 扩展脆弱性** | `pydantic-core`、`PyNaCl`、`cryptography` 等 C 扩展在 Termux 和旧系统上易出错 |
| **Python 版本限制** | `requires-python = ">=3.11,<3.14"` — 因 C 扩展 wheel 兼容性 |

### 功能层面

| 痛点 | 详情 |
|------|------|
| **Agent 缓存膨胀** | 128 个 agent LRU 缓存，在大量活跃网关会话中可能造成内存压力 |
| **FTS5 跨网络限制** | WAL 模式在 NFS/SMB 上不可用，需降级到 DELETE 模式 |
| **工具 schema 膨胀** | 每个核心工具都发送到所有 API 调用，增加 token 消耗 |
| **MCP 启动阻塞** | 早期 MCP 发现阻塞网关启动，后来才移到异步执行 |
| **Docker 持久化** | 单一容器的隔离不足，多代理共享同一工作空间 |
| **记忆上限** | MEMORY.md 2,200 字符限制对复杂项目太紧 |

### 生态系统

| 痛点 | 详情 |
|------|------|
| **插件发现** | 插件需手动启用，无市场/注册中心 |
| **技能标准** | 兼容 agentskills.io，但生态尚在早期 |
| **多平台状态同步** | 网关重启后会话恢复复杂，需 freshness window |
| **更新风险** | `hermes update` 中途失败会导致模块状态不一致 |

---

## 19. 教学指南：如何理解 Hermes

### 核心心法：窄腰架构（Narrow Waist）

```
     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
     │    CLI UI    │     │   Telegram   │     │   Discord    │  ← 前端（宽）
     └──────┬───────┘     └──────┬───────┘     └──────┬───────┘
            │                    │                    │
            └────────────────────┼────────────────────┘
                                 │
                        ┌────────▼────────┐
                        │   AIAgent Core   │  ← 窄腰（核心会话循环，最小接口）
                        └────────┬────────┘
                                 │
            ┌────────────────────┼────────────────────┐
            │                    │                    │
     ┌──────▼───────┐   ┌───────▼──────┐   ┌────────▼──────┐
     │    Tools     │   │  Providers   │   │   Memory      │  ← 后端（宽）
     │  (70+ tools) │   │  (30+ 提供者) │   │  (5+ 类型)    │
     └──────────────┘   └──────────────┘   └───────────────┘
```

**教学启示**：Hermes 不是"单个 AI 应用"，而是一个**智能体操作系统**。核心的 `AIAgent` 是薄层，所有能力都在边缘扩展。

### 理解关键概念

#### 1. 工具 ≠ 函数调用

教学点：传统 LLM 函数调用是静态的，Hermes 的工具系统是**动态可发现的**：

```
静态 → JSON schema 硬编码
Hermes → 每个工具文件 import 时自动 registry.register()
       → check_fn 按运行时条件动态启用/禁用
       → 28 个工具集可组合过滤
       → MCP 服务器动态注册新工具
       → 插件可注册自定义工具
```

#### 2. 技能 ≠ Prompt

教学点：技能是**结构化知识文档**，不是简单的系统提示片段：

```
普通 Prompt → 全量注入（消耗 token，难以管理）
Hermes 技能 → 三层渐进式披露（索引→全文→引用文件）
           → 带 YAML 元数据（平台兼容性、条件激活）
           → 支持模板变量和内联 shell
           → AI 可自主创建（/learn 命令）
```

#### 3. 网关 ≠ Webhook 转发

教学点：网关是**有状态的异步事件处理器**：

```
普通 Webhook → 无状态转发
Hermes 网关 → 每个平台独立 asyncio Task
           → 平台无关的 session 抽象
           → 用户认证和授权
           → 消息格式统一（text → Markdown → platform-native）
           → 代理缓存（LRU + 空闲 TTL）
```

#### 4. 配置 == 操作系统设置

教学点：配置系统类似操作系统的注册表：

```yaml
model.provider → 类似 PATH 环境变量（自动发现）
terminal.backend → 类似虚拟化层（local/docker/ssh 统一接口）
platforms.* → 类似设备驱动程序
skills.* → 类似软件包管理
cron.* → 类似系统定时任务
mcp_servers.* → 类似动态链接库
```

### 教学演示路径

推荐按这个顺序教学：

1. **最小演示**：`pip install` → `hermes setup` → `hermes chat` → 一句话问答
2. **工具调用**：展示 `terminal` 和 `read_file` 工具的执行过程
3. **多平台**：启动 `hermes gateway` → 通过 Telegram 发送消息
4. **技能**：`/learn` 创建一个技能 → 在新会话中使用
5. **记忆**：展示跨会话记住用户偏好
6. **子智能体**：`delegate_task` 并行执行
7. **Cron**：设置定时任务自动执行
8. **自定义工具**：编写插件注册自定义工具

---

*本文档由 Hermes Agent 自身（在人类指导下）分析生成。分析基于 2,780 个 Python 源文件、14,215 次 Git 提交、及官方完整文档。*
