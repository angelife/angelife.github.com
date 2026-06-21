---
name: wechat-hermes
description: Hermes Agent 通过 iLink Bot API 连接个人微信（WeChat/Weixin）的配置与使用
---

# WeChat (Weixin) + Hermes iLink Bot 集成

## 平台限制（先读再动手）

- iLink Bot 是**独立 bot 身份**（如 `a5ace6fd482e@im.bot`），不是你个人微信号
- 群聊基本不可用：iLink 不转发普通微信群的 @mention 事件
- DMs 私聊可以正常工作
- 群政策建议设为 `disabled`，避免 gateway 启动时报警

## 前置要求

- iLink 账号：https://ilink.bot 注册
- App ID + Token（iLink 控制台获取）
- Hermes 安装在**Mac 本机**（非 Docker 容器内）

## 快速启动（Mac 本机 terminal）

```bash
hermes gateway setup
# 选择: Weixin / WeChat
# 填入 iLink App ID 和 Token
# 终端生成二维码 → 用微信扫码确认
hermes pairing approve   # 首次配对
hermes gateway run       # 启动网关（后台运行）
```

## 环境变量

```bash
WEIXIN_APP_ID=your_ilink_app_id
WEIXIN_TOKEN=your_ilink_token
WEIXIN_GROUP_POLICY=disabled   # 推荐默认禁用群聊
```

## Docker 容器内限制

`hermes gateway` **必须在 Mac 本机运行**，不在容器内。

- 容器内只能查看文档：`https://hermes-agent.nousresearch.com/docs/user-guide/messaging/#weixin-wechat`
- 配置在 Mac 本机执行

### 为什么 Docker 里跑不通

iLink Bot 的 OAuth 扫码流程需要双向网络连通：
- 微信服务器 → Mac 本机（回调）
- Mac 本机 → iLink 服务器（长连接）

Docker 容器通常无法完整实现这个握手（取决于 Docker 网络模式 + 是否有公网 IP）。即使 gateway 能启动，二维码也出不来或扫码后无法回调。

**已验证可行方案：**
- Mac 本机 Hermes 实例负责 gateway 运维（扫码、配对、启动）
- Docker 里的 NVIDIA 实例负责接收指令和执行任务
- 两者通过共享 `/repo` 文件或跨平台消息（telegram → wechat relay）同步状态

**Docker 实例的职责边界：**
- ✅ 接收用户指令并执行（写文件、git 操作、生图等）
- ✅ 通过 WeChat 平台回复用户
- ❌ 不负责 gateway 运维、扫码、配对

## 配对验证

首次连接后：

```bash
hermes pairing approve
```

## 故障排查

| 症状 | 根因 | 解决 |
|------|------|------|
| 扫码后 bot 无法加入群 | iLink 限制，非配置问题 | 群聊默认禁用，正常 |
| 私聊收不到消息 | 未完成配对 | `hermes pairing approve` |
| Docker 内跑 gateway 报 not found | gateway 必须在宿主机 | 在 Mac terminal 操作 |
| gateway 启动报警 WEIXIN_GROUP_POLICY | 群功能默认禁用 | 设为 `disabled` 即可 |