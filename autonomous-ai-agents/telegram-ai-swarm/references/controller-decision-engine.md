# Controller Decision Engine — complete reference

This file documents the Controller design pattern that is the core of any Telegram AI Swarm.

## Philosophy

> AI agents are NOT free-chatting entities. They are functions called by the Controller.

The Controller is the single point of truth for all decisions: whether to respond, which agents to invoke, and in what order.

## Flow

```
1. Telegram message arrives → EventReceiver normalizes to MessageEvent
2. Controller.receive(event) → ControllerDecision
   a. Check auth (allowed_chats, mention gate)
   b. Check global cooldown
   c. Skip empty/short messages
   d. Run loop detection (text similarity check)
   e. Select agents (0-2) based on message intent
   f. Build AgentExecution(s) with per-agent prompts
3. Scheduler.execute_round(executions) → run agents serially
   a. For each execution: build prompt → call LLM → update state
   b. Apply per-agent cooldown
   c. Update last_ai_message for loop detection
4. Send each response to Telegram via bot.send_message()
```

## Complete models.py (data types)

```python
@dataclass
class MessageEvent:
    chat_id: int
    user_id: int
    user_name: str
    text: str
    message_id: int
    is_group: bool
    timestamp: float
    is_mention: bool = False
    is_reply_to_bot: bool = False

@dataclass
class AgentConfig:
    name: str
    label: str
    role: str
    system_prompt: str
    cooldown_seconds: int = 15
    max_tokens: int = 1024

@dataclass
class AgentExecution:
    agent_name: str
    agent_label: str
    system_prompt: str
    user_message: str
    recent_history: list[str]
    max_tokens: int
    chat_id: int

@dataclass
class ControllerDecision:
    should_respond: bool
    executions: list[AgentExecution] = field(default_factory=list)
    reason: str = ""

@dataclass
class ChatSession:
    chat_id: int
    history: list[dict] = field(default_factory=list)
    agent_cooldowns: dict[str, float] = field(default_factory=dict)
    last_ai_timestamp: float = 0.0
    no_progress_count: int = 0
    last_ai_message: str = ""
```

## Agent selection logic (intent-based v1)

```python
question_words = ["?", "？", "如何", "为什么", "怎么", "什么", "吗", "哪个", "有没有"]
opinion_words = ["我觉得", "我认为", "我的观点", "同意", "不同意", "反对", "支持", "应该", "必须", "不能"]
summary_words = ["总结", "汇总", "归纳", "结论", "综上所述", "谈谈"]

if has_question:
    candidates = ["agent_a", "agent_c"]  # analysis + creative
elif has_opinion:
    candidates = ["agent_a", "agent_b"]  # analysis + skeptic
elif has_summary:
    candidates = ["agent_a", "agent_d"]  # analysis + summary
else:
    candidates = ["agent_a"]  # analysis only
```

## Loop detection (trigram Jaccard similarity)

```python
def _text_similarity(a: str, b: str) -> float:
    def ngrams(s, n=3):
        return {s[i:i+n].lower() for i in range(len(s)-n+1)}
    grams_a = ngrams(a)
    grams_b = ngrams(b)
    intersection = grams_a & grams_b
    union = grams_a | grams_b
    return len(intersection) / len(union) if union else 0.0
```

If similarity > 0.85, increment `no_progress_count`. When it reaches 3, stop AI for this chat entirely.