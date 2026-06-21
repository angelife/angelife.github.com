# Telegram Bot Token 管理与 Gateway 切换

> 2026-06-19 木同学实测记录。

## 切换 bot（2026-06-19 实测）

当需要把 gateway 从旧的 bot 切换到新的 bot：

```bash
# 1. 加载 SSH key（容器重启后 ssh-agent 丢失，必须重建）
eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_ed25519

# 2. 编辑 .env 替换 TELEGRAM_BOT_TOKEN
# 3. 重启 gateway（新 PID 会改变）
# 4. 验证
curl -s --max-time 8 https://api.telegram.org/bot${TOKEN}/getMe
```

## ⚠️ Bot Token 脱敏 Mask 陷阱（2026-06-19 血训）

**症状**：Python 代码出现 SyntaxError，但代码逻辑看起来完全正确。

**根因**：在 `.env` 文件里写 `TELEGRAM_BOT_TOKEN=***` 时，`split('=',1)` 拿到的是字符串 `"***"`。当 Python 代码里出现字面 `"***"` 时，mask 工具把它当成变量赋值语法的一部分，导致解析失败。

**错误代码（会崩）：**
```python
token = ln.strip().split('=', 1)[1]  # 遇到 *** 行时报 SyntaxError
```

**正确代码（安全）：**
```python
env = {}
with open('.env') as f:
    for ln in f:
        if '=' in ln and not ln.startswith('#'):
            k, v = ln.strip().split('=', 1)
            env[k] = v
token = env.get('TELEGRAM_BOT_TOKEN', '')
```

**原则**：不要在代码里写 `TELEGRAM_BOT_TOKEN` 变量名字符串，改用 `.get()` 从字典取。

## 验证 bot 切换成功

| 检查项 | 方法 |
|--------|------|
| PID 改变 | `ps aux \| grep gateway` — 新的 PID，不同于旧的 |
| HTTPS 连接 | `ss -tp \| grep <pid>` — 应有 2 个 ESTABLISHED 到 api.telegram.org |
| bot 身份 | `curl -s https://api.telegram.org/bot${TOKEN}/getMe` — 返回新 bot 用户名 |
| polling 模式 | `curl -s https://api.telegram.org/bot${TOKEN}/getWebhookInfo` — url 字段为空 |

## Gateway 重启后 Polling 验证

用 `curl` 直接打 Telegram API，不需要 Python：

```bash
# 直接发消息测试 outbound
curl -s --max-time 10 -X POST \
  "https://api.telegram.org/bot${TOKEN}/sendMessage" \
  --data-urlencode "chat_id=${CHAT_ID}" \
  --data-urlencode "text=Gateway 重启测试 $(date)"

# 看最近 update（测试 inbound polling）
curl -s --max-time 8 \
  "https://api.telegram.org/bot${TOKEN}/getUpdates?limit=3&timeout=5"
```

## Bot Token 格式

标准格式：`数字:字母数字字符串`，例如 `8881645488:AAHVZDu6YcpzsxxO4rAuAUhcNWsBl6dqvEk`

- `:` 前是 bot ID
- `:` 后是认证 token
- `len()` 应约 45-55 字符