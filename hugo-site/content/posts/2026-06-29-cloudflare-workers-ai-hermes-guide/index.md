---
title: "WorkerAI指南"
date: 2026-06-29T12:00:00+08:00
draft: false
slug: cloudflare-workers-ai-hermes-guide
categories:
  - "技术"
series:
  - ai-bu-yin
tags:
  - Cloudflare
  - Workers AI
  - Hermes
  - OpenAI
  - 教程
cover: []
---

最近发现 Cloudflare Workers AI 提供了一个不错的免费推理额度：**每天 10,000 Neurons**（约等于数百万 token），支持通义千问、Llama、Gemini 等多种模型，而且走的是标准 OpenAI API 兼容接口，可以直接接入 Hermes Agent 多模型框架。

本文记录从零配置到实际可用的完整过程，不涉及任何个人敏感信息。

## 一、Cloudflare Workers AI 是什么？

Cloudflare Workers AI 是 Cloudflare 推出的边缘推理服务，部署在全球 300+ 数据中心，延迟低，支持：

- 文本生成（Qwen3-30B、Llama 3.1、Gemini 等）
- 图像生成
- 语音转文字
- Embedding 等

免费套餐每天提供 **10,000 Neurons**，按 token 计费：
- Qwen3-30B-A3B-FP8：0.051 / 1M tokens（最便宜）
- IBM Granite 4.0：0.03 / 1M tokens（更便宜但能力弱）
- 其他模型价格略高

对于日常对话和简单任务，免费额度足够。

## 二、准备工作

### 2.1 注册 Cloudflare 账号

访问 https://dash.cloudflare.com 注册或登录。

### 2.2 获取 Account ID

登录 Cloudflare Dashboard 后，在左侧菜单找到 **Account Details**，可以看到你的 Account ID（一串 32 位的十六进制字符串）。

## 三、创建 API Token

这是最关键的一步。Workers AI 需要 **Account API Token**（不是 User API Token），权限要精确配置。

### 3.1 进入令牌创建页面

在 Cloudflare Dashboard 左侧菜单：

```
Account API tokens → Create Token
```

### 3.2 选择权限模板

选择 **"Edit"** 模板（比 "Read" 更完整），然后选择 **"Custom"**。

### 3.3 配置权限

在 Custom Policy 中，展开 **AI & Machine Learning** 分类，找到 **Workers AI**，将以下两个权限都打开：

- ✅ **Read** — 读取模型列表
- ✅ **Edit** — 调用模型

其他服务（DNS、App Security 等）不需要勾选，保持默认即可。

### 3.4 创建 Token

滚动到页面底部，点击 **"Create Token"** 按钮。

创建成功后，页面会显示你的 **Account API Token**，格式为：

```
cfat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**⚠️ 重要：这个 Token 只显示一次，必须立即复制保存！**

## 四、配置 Hermes Agent

### 4.1 保存 API Key 到环境变量

编辑 `~/.hermes/.env` 文件（如果不存在则创建）：

```bash
CLOUDFLARE_API_KEY=*** 4.2 添加 Provider 配置

编辑 `~/.hermes/config.yaml`，在 `providers:` 部分下添加：

```yaml
providers:
  # ... 已有的 providers ...
  
  cloudflare-workers-ai:
    base_url: "https://api.cloudflare.com/client/v4/accounts/你的AccountID/ai/v1"
    api_key: ${CLOUDFLARE_API_KEY}
    timeout: 120
    max_tokens: 8192
```

### 4.3 配置可用模型

在 `custom_providers:` 部分添加具体模型列表：

```yaml
custom_providers:
  cloudflare-workers-ai:
    type: openai-api
    base_url: "https://api.cloudflare.com/client/v4/accounts/你的AccountID/ai/v1"
    api_key: ${CLOUDFLARE_API_KEY}
    timeout: 120
    max_tokens: 8192
    models:
      - "@cf/qwen/qwen3-30b-a3b-fp8"      # 通义千问 30B，推荐 ⭐
      - "@cf/qwen/qwq-32b"                  # Qwen 推理模型
      - "@cf/qwen/qwen2.5-coder-32b-instruct"  # 代码专用
      - "@cf/ibm-granite/granite-4.0-h-micro"  # IBM 轻量模型
```

### 4.4 重启 Hermes Gateway

```bash
hermes gateway restart
```

重启完成后，Hermes 会自动加载新的 provider。

## 五、测试验证

### 5.1 命令行直接测试 API

```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/你的AccountID/ai/v1/chat/completions" \
  -H "Authorization: Bearer *** \
  -H "Content-Type: application/json" \
  -d '{
    "model": "@cf/qwen/qwen3-30b-a3b-fp8",
    "messages": [{"role": "user", "content": "你好"}],
    "max_tokens": 50
  }'
```

成功返回应该包含完整的 JSON 响应。

### 5.2 在 Hermes 中测试

在 Hermes 对话中使用 `@cloudflare-workers-ai` 前缀指定模型：

```
@cloudflare-workers-ai 你好
```

或者直接用缩写 `@cf`：

```
@cf 你好
```

### 5.3 测试中英文输出

通义千问 30B 对中英文支持都很好：

```
@cf 请用中文解释一下量子计算的基本原理
@cf Explain quantum entanglement in simple terms
```

## 六、可用模型一览

| 模型 ID | 名称 | 价格 | 推荐场景 |
|---------|------|------|---------|
| `@cf/qwen/qwen3-30b-a3b-fp8` | 通义千问 30B | 0.051/1M | 通用对话 ⭐ |
| `@cf/qwen/qwq-32b` | QwQ 32B | 0.051/1M | 推理/数学 |
| `@cf/qwen/qwen2.5-coder-32b-instruct` | Qwen Coder 32B | 0.051/1M | 代码生成 |
| `@cf/ibm-granite/granite-4.0-h-micro` | IBM Granite | 0.03/1M | 轻量任务 |

## 七、常见问题

### Q1: 为什么返回 401 认证错误？

使用了 User API Token（`cfut_` 开头）而非 Account API Token（`cfat_` 开头）。Workers AI 需要 Account 级别的 Token。

### Q2: Token 的权限要开哪些？

只需要 **Workers AI** 的 Read 和 Edit。不要开 DNS、Cloud Functions 等其他权限，安全第一。

### Q3: 免费额度用完了怎么办？

Cloudflare 免费套餐每月 10,000 Neurons。对于日常使用基本够用。如果需要更多，可以升级到 Pro 计划（20 美元/月），Neurons 额度大幅提升。

### Q4: 延迟怎么样？

Workers AI 部署在 Cloudflare 全球边缘节点，延迟通常在 200-800ms 之间，取决于你和最近节点的距离。

### Q5: 可以用作默认模型吗？

可以。在 `~/.hermes/config.yaml` 中修改 `model.default` 为 `cf/qwen3-30b-a3b-fp8` 即可。但建议保留更强的模型作为默认，Workers AI 作为备选。

## 八、进阶配置：多模型协作

Hermes Agent 支持多模型框架（MoA），可以将 Cloudflare Workers AI 与其他模型（如 OpenRouter、本地模型等）组合使用：

```yaml
# 示例：多模型 fallback
model:
  default: opencode-zen/free  # 首选
fallback_providers:
  - cloudflare-workers-ai    # 备选
  - freellmapi               # 本地备选
```

这样在当前模型不可用或配额耗尽时，自动切换到 Cloudflare Workers AI。

## 九、总结

Cloudflare Workers AI 是目前免费推理服务中性价比最高的选择之一：

- ✅ 每天 10,000 Neurons 免费
- ✅ 支持通义千问、Llama、Gemini 等多种模型
- ✅ OpenAI API 兼容，接入简单
- ✅ 全球边缘部署，延迟低
- ✅ 安全性好（细粒度权限控制）

适合：
- 日常对话助手
- 代码生成辅助
- 多模型框架的免费 fallback
- 开发测试阶段

配置完成后，你的 Hermes Agent 就多了一个强大的免费推理后端。

---

*本文所有配置示例使用虚构的 Account ID 和 Token，实际操作时替换为你自己的真实值。*