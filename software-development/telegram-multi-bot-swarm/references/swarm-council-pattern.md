# Swarm Council Pattern — Multi-Agent Orchestration

三种变体：External-LLM Council（NVIDIA API 并发）、Hermes-native Council（Hermes 自身串行模拟）、Hybrid Council（Hermes + LLM 组合）。

## Pattern D1: External-LLM Council (NVIDIA DeepSeek 并发)

适合需要真正并行、Agent 各自独立调用 LLM 的场景。5 个 Agent 用 threading 并发请求 LLM API。

### 架构

```
用户输入
  ↓
Hermes → council.py (orchestrator)
  ↓
并行调用 5 个 LLM (threading)
  ├── 🟢 wood (收集) → 事实、数据、候选方案
  ├── 🔴 fire (创意) → 创新想法、突破点、风险假设
  ├── 🟤 earth (整合) → 执行路线图、工作拆解
  ├── 🟡 gold (审核) → 问题清单、风险报告、修正建议
  └── 🔵 water (总结) → 最终结论、SOP
  ↓
Hermes 汇总 → 共识/分歧/建议/风险 → 单条消息发送到群
```

### 代码结构

```
telegram-ai-swarm/
├── council/
│   ├── __init__.py            # 模块入口
│   ├── config.json            # 五行分工 + System Prompt + project_rules
│   ├── llm_adapter.py         # LLM 适配器（urllib内建库, 无httpx依赖）
│   ├── swarm_council.py       # 核心调度引擎（并发→汇总→多轮→防死循环）
│   └── hermes_council.py      # Hermes-native Council（D2 变体）
├── council_handler.py          # Telegram 入口
└── run_council.py              # 快速启动脚本
```

### llm_adapter.py 关键设计

```python
# 无需 httpx/pyyaml — 只用 Python 内建库
import json, urllib.request, threading

class LLMAdapter:
    def __init__(self, config):
        self.model = config["model"]          # "deepseek-ai/deepseek-v4-flash"
        self.base_url = config["base_url"]    # "https://integrate.api.nvidia.com/v1"
        self.api_key = config["api_key"]
        self.timeout = config.get("request_timeout", 90)
        self.max_retries = config.get("max_retries", 3)

    def _build_payload(self, messages, max_tokens, json_mode=True):
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7,
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}  # 强制 JSON 输出
        return payload

    def chat(self, messages, max_tokens=1024, json_mode=True):
        """返回 response text 或 None。3 次重试 + 指数退避。"""
        url = f"{self.base_url}/chat/completions"
        data = json.dumps(self._build_payload(messages, max_tokens, json_mode)).encode()
        req = urllib.request.Request(url, data=data,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"})
        for attempt in range(1, self.max_retries + 1):
            try:
                resp = urllib.request.urlopen(req, timeout=self.timeout)
                return json.loads(resp.read())["choices"][0]["message"]["content"].strip()
            except urllib.error.HTTPError as e:
                logger.warning(f"HTTP {e.code}: {e.read()[:200]}")
                if attempt < self.max_retries: time.sleep(2.5 ** attempt)
            except urllib.error.URLError:  # Timeout
                if attempt < self.max_retries: time.sleep(2.0)
            except Exception as e:
                if attempt < self.max_retries: time.sleep(1.0)
        return None
```

### 并行调用

```python
from threading import Thread

def call_agent_parallel(adapter, agents, user_message, history=None):
    results = {}
    lock = threading.Lock()

    def _call(agent):
        messages = [{"role": "system", "content": agent["system_prompt"]}]
        if history: messages.extend(history)
        messages.append({"role": "user", "content": user_message})
        result = adapter.chat_json(messages)
        with lock: results[agent["name"]] = (agent["name"], result)

    threads = [Thread(target=_call, args=(a,), daemon=True) for a in agents]
    for t in threads: t.start()
    for t in threads: t.join()
    return [results.get(a["name"], (a["name"], None)) for a in agents]
```

### 安全规则（swarm_council.py）

```python
MAX_ROUNDS = 3           # 硬上限，到顶强制结束
DISAGREEMENT_THRESHOLD = 0.6  # 分歧 ≥ 0.6 才触发第二轮

# 分歧计算：基于 confidence 的方差
def _calc_disagreement(responses):
    confidences = [r["confidence"] for r in responses if r and "confidence" in r]
    if len(confidences) < 2: return 0.0
    mean = sum(confidences) / len(confidences)
    return min(1.0, sum((c-mean)**2 for c in confidences) / len(confidences) * 2.0)
```

### 第二轮辩论机制

仅当 `disagreement >= DISAGREEMENT_THRESHOLD` 且 `round < MAX_ROUNDS` 时触发：
- 只有低置信度 Agent 被指定发言
- 其他人不得插话
- 第二轮 context 包含争议点描述

### 输出格式

```
🟢 **【木·收集】**
_观点..._
· 建议1
· 建议2

🔴 **【火·创意】**
_观点..._
...

━━━━━━━━━━━━━━━━━━━
📊 **【Hermes 总结 — 第1轮】**
✅ 共识
  · wood: ...
📌 建议下一步
  · ...
⚠️ 风险提示
  · ...
⏱ 25s · 1轮 · consensus_reached
```

---

## Pattern D2: Hermes-native Council（本次构建）

**不需要外部 LLM 调用**。Hermes 自身依次以五个 Agent 角色思考并生成回复。

### 适用场景
- LLM API 不可用/超时时
- 需要 100% 可靠性（无 timeout/限流/429）
- 快速原型验证
- 与 Pattern D1 互补——D1成功时用D1，失败时fallback到D2

### 架构

```python
# 每个 Agent 的回复由 Hermes 自身在同一 session 内逐条生成
# 通过 callback 机制：Hermes 调用 council.deliberate(question, callback=self._agent_callback)
# callback 收到 (agent_name, prompt) → 返回 JSON dict

class HermesCouncil:
    def deliberate(self, question, callback=None):
        for agent_name in AGENT_ORDER:  # ["wood", "fire", "earth", "gold", "water"]
            prompt = self._make_agent_prompt(agent_name, question)
            result = callback(agent_name, prompt)  # Hermes 实现
            responses.append((agent_name, result))
        # Hermes 汇总
        return summary
```

### 关键差异 vs Pattern D1

| | D1 External-LLM | D2 Hermes-native |
|---|---|---|
| LLM 调用 | 5 个并行 HTTP 请求 | 0 个外部请求 |
| 速度 | ~90-180s (受 API 影响) | ~20-30s |
| 可靠性 | 低（timeout/429/限流） | 高（全本地） |
| 并发 | threading 并行 | 串行 |
| 依赖 | NVIDIA API / API Key | 无 |
| 独立性 | Agent 可独立思考 | Hermes 模拟全部 |

---

## System Prompts（五行分工 v2）

### 木（收集）— 讨论起点
```markdown
你是「木」，职责是信息收集、搜索资料、调研分析、发散思考、提出新方向。
每次接到问题：
1. 收集相关事实和数据
2. 进行发散性思考，提出新方向
3. 输出候选方案
你是讨论的起点，负责发现问题和收集信息。
```

### 火（创意）— 扩展边界
```markdown
你是「火」，职责是创意生成、头脑风暴、方案扩展、风险假设、机会发现。
每次接到问题：
1. 在木的基础上扩展方案
2. 提出创新想法和突破点
3. 识别机会和风险假设
你是创新资源，负责扩展讨论的边界。
```

### 土（整合）— 落地执行
```markdown
你是「土」，职责是整合信息、建立框架、项目规划、资源协调、中间决策。
每次接到问题：
1. 综合木和火的全部观点
2. 建立执行框架和路线图
3. 制定协作计划
你是执行中心，负责把思维变成可执行的计划。
```

### 金（审核）— 质量门
```markdown
你是「金」，职责是审核、质疑、风险控制、逻辑验证、质量检查。
每次接到问题：
1. 审核土的计划
2. 提出质疑和风险
3. 输出修正建议
你是质量门，负责确保计划可行和稳健。
```

### 水（总结）— 归档输出
```markdown
你是「水」，职责是总结归纳、反思优化、知识沉淀、经验提炼、最终输出。
每次接到问题：
1. 归纳所有观点
2. 提炼核心结论
3. 输出可存档的结果
你是最终输出的责任人，负责把讨论变成可传承的知识。
```

---

## angelife 项目约束（project_rules）

所有 Agent 输出必须遵守：
- 人类用户 + ChatGPT（剑妈）为最终控制者，Hermes 是执行代理，不是总控
- 未经授权禁止发布、git push、rsync、部署
- 所有 Agent 输出必须保留工作日志和交接记录
- Agent 建议不得超出 angelife 工作流规则

## Pitfalls

### LLM API 相关
- **NVIDIA DeepSeek V4 60s timeout 频繁** (~50% 的调用会超时)。解决方案：将 timeout 提升到 90s，配合 3 次重试
- **NVIDIA 40 RPM 硬限**：5 个并行 Agent 可能触发 429。`time.sleep(2)` rate-limit guard 是必需的
- **无 httpx/pyyaml**：Hermes Docker 环境没有 pip，必须使用 urllib.request（内建）+ json（内建）

### 架构相关
- **单入口单输出**：只有 Hermes 对外发消息。Agent 不独立连接 Telegram。避免 409/Token 冲突
- **Bot 互盲不可用**：不要尝试让独立 Bot 互相看到对方消息——Telegram 硬限制
- **防死循环**：MAX_ROUNDS=3 硬上限 + 分歧阈值检测

### Hermes-native Council
- 串行调用 5 个 Agent 可能导致"思维同质化"——因为同一个模型模拟不同角色容易趋同
- 建议 D1 为主、D2 为 fallback 的组合策略
- `callback` 机制要求 Hermes session 内有对应实现

## 验证

```bash
# 测试 External-LLM Council
cd /opt/data/telegram-ai-swarm
python3 -c "
from council.swarm_council import SwarmCouncil
c = SwarmCouncil()
r = c.deliberate('如何提升写作习惯？')
print(r['full_output'])
"

# 测试发送到群（由 Hermes 发送，无需外部 bot token）
send_message(-1003926068725, output)
```