# Bot Diagnostics Script

Comprehensive script to check Telegram bot status in a group: identity, group membership, permissions, and send capability.

## Usage

```bash
# Save as check_bots.py
python3 check_bots.py [-1001234567890]
```

## Script

```python
#!/usr/bin/env python3
"""
Bot diagnostics: check all bots in a Telegram group.
Usage: python3 check_bots.py [chat_id]

Checks for each bot:
1. getMe — bot identity (username, ID)
2. getChat — group exists and accessible
3. getChatMember — membership status, permissions
4. sendMessage — actual send capability
"""

import urllib.request, json, os, sys

GID = int(sys.argv[1]) if len(sys.argv) > 1 else -1003926068725

# Edit this dict: label → path to token file
BOT_TOKENS = {
    "🟡 金 @peterchan90_bot": "/tmp/swarm_token.txt",
    "🔵 水 @masterchan19840907_bot": "/tmp/token_water.txt",
    "🔴 火 @SwarmDiscussionBot": "/tmp/token_fire.txt",
}

def check_bot(label, token):
    try:
        # 1. Bot identity
        url = f'https://api.telegram.org/bot{token}/getMe'
        resp = urllib.request.urlopen(url, timeout=5)
        me = json.loads(resp.read())
        bot_id = me['result']['id']
        bot_uname = me['result']['username']
        print(f"\n✅ {label} (ID={bot_id})")
        
        # 2. Group access
        url = f'https://api.telegram.org/bot{token}/getChat?chat_id={GID}'
        resp = urllib.request.urlopen(url, timeout=5)
        chat = json.loads(resp.read())
        if chat.get('ok'):
            title = chat['result'].get('title', '?')
            print(f"   群: {title}")
        else:
            print(f"   群: ❌ {chat.get('description')}")
            return
        
        # 3. Membership and permissions
        url = f'https://api.telegram.org/bot{token}/getChatMember?chat_id={GID}&user_id={bot_id}'
        resp = urllib.request.urlopen(url, timeout=5)
        member = json.loads(resp.read())
        m = member.get('result', {})
        status = m.get('status', 'unknown')
        print(f"   状态: {status}")
        if status == 'administrator':
            print(f"   权限: 管理员 | 发消息: ✅")
        elif status == 'member':
            print(f"   权限: 普通成员 | 发消息: ✅")
        elif status == 'left':
            print(f"   权限: ❌ 不在群中")
        elif status == 'kicked':
            print(f"   权限: ❌ 被踢出")
        
        # 4. Send test message
        url = f'https://api.telegram.org/bot{token}/sendMessage'
        payload = json.dumps({'chat_id': GID, 'text': f'🧪 {label} 诊断测试'}).encode()
        req = urllib.request.Request(url, data=payload,
                                      headers={'Content-Type': 'application/json'})
        resp = urllib.request.urlopen(req, timeout=10)
        result = json.loads(resp.read())
        if result.get('ok'):
            print(f"   发消息: ✅ 成功")
        else:
            print(f"   发消息: ❌ {result.get('description')}")
            
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:100]
        print(f"\n❌ {label}: HTTP {e.code}")
        if e.code == 403: print(f"   原因: Bot被阻止或无权操作")
        elif e.code == 400: print(f"   原因: {body}")
        else: print(f"   {body}")
    except Exception as e:
        print(f"\n❌ {label}: {e}")

if __name__ == "__main__":
    print(f"Bot Diagnostics for group: {GID}")
    print("=" * 50)
    for label, path in BOT_TOKENS.items():
        if os.path.exists(path):
            with open(path) as f:
                token = f.read().strip()
            if token and '***' not in token:
                check_bot(label, token)
            else:
                print(f"\n❌ {label}: token 无效或已遮蔽")
        else:
            print(f"\n❌ {label}: 未找到 token 文件 ({path})")
    print("\n" + "=" * 50)