---
name: wechat-article-extractor
description: "提取微信公众号文章内容（标题 + 正文）from mp.weixin.qq.com links using curl + Python。免 API、免登录，适用所有 Hermes 容器。"
version: 1.0.0
author: 木同学
platforms: [linux, macos]
metadata:
  hermes:
    tags: [wechat, 公众号, article, extractor, curl]
    related_skills: [hermes-agent]
---

# WeChat 公众号文章提取器

## 何时用

用户分享了一个 `https://mp.weixin.qq.com/s/xxx` 链接，需要阅读文章内容，或者需要转发 / 分析该文章。

## 步骤

### 1. 提取文章 ID

链接格式：`https://mp.weixin.qq.com/s/<文章ID>`

文章 ID 是 `s/` 后面到结尾（或 `?` 前）的那串字符。

### 2. 单行命令提取

```bash
curl -sL -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" "https://mp.weixin.qq.com/s/<文章ID>" | \
python3 -c "
import sys, re, html
c = sys.stdin.read()
# 标题
t = re.search(r'var msg_title\s*=\s*\"([^\"]+)\"', c)
print('标题:', t.group(1) if t else '(未知)')
# 正文
r = re.search(r'id=\"js_content\"[^>]*>(.*?)</div>\s*<script', c, re.DOTALL)
if r:
    text = re.sub(r'<[^>]+>', '\n', r.group(1))
    text = re.sub(r'\n[ \t]*\n', '\n', html.unescape(text)).strip()
    print('\\n正文:')
    print(text)
else:
    print('(无法提取正文，公众号可能有限制)')
"
```

### 3. 提取结果处理

- 标题优先取 `msg_title` 变量
- 正文在 `id="js_content"` 的 div 中
- 某些公众号可能有阅读限制（需登录），此时正文提取为空

### 4. 配合其他技能

- 提取后可以 `delegate_task` 给子 agent 做总结/分析
- 可作为 `hermes-agent` 的网页内容输入源

## 注意事项

- User-Agent 必须带，否则微信返回空页面
- 部分公众号开启了 IP 限制或登录墙，此时需要浏览器方案
- 如果 curl 不生效，改用 `browser_navigate` 加载页面后读取 DOM

## 示例输出

```
标题: SkyClaw-v1 昆仑万维开源模型

正文:
引言

昆仑万维SkyClaw系列...
```
