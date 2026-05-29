# NVIDIA / Hermes Telegram Gateway 故障恢复 SOP

> 本文档记录当 Telegram 中 NVIDIA 无响应时的标准诊断与恢复流程。
> 每次恢复必须署名，谁操作谁负责。

---

## 故障现象

Telegram 里 @angelife_bot（或对应 bot token）不回复，但 Docker 容器可能仍然 running。

可能原因（由轻到重）：
1. gateway 进程被 s6 标记为 down（最常见）
2. gateway 进程崩溃但容器存活
3. Hermes 主进程挂了
4. Telegram Bot Token 失效
5. Telegram 侧限制（flood wait / ban）

---

## 正确判断流程

**第一步：区分是哪种故障**

| 层级 | 检查命令 |
|------|----------|
| 容器存活 | `docker ps` |
| Hermes 主进程 | `docker logs --tail=60 hermes-minimaxlab` |
| gateway 状态 | `docker exec hermes-minimaxlab ls /run/service/gateway-default/` |
| s6 supervisor | `docker exec hermes-minimaxlab /package/admin/s6-2.15.0.0/command/s6-svc -l /run/service/gateway-default` |

**第二步：检查 gateway-down 文件**

```bash
docker exec hermes-minimaxlab ls -la /run/service/gateway-default/
```

如果看到 `down` 文件，说明 s6 将 gateway 置于下线状态。
**这是最常见的 NVIDIA 不回复原因。**

---

## 禁止事项（故障时禁止做）

以下行为无论什么情况，故障时禁止执行：

- ❌ `docker stop` — 会中断所有 s6 托管进程
- ❌ `docker rename` — 可能破坏 s6 service 路径
- ❌ `docker run` — 重建容器会丢失主库挂载（若有）
- ❌ `docker restart` — 同上，且不解决问题
- ❌ `docker attach` — 干扰 s6 前台管理
- ❌ 立即挂载主库 `/repo` — 诊断未完成就操作仓库
- ❌ 立即发布 README 或做任何 git 操作

---

## 标准检查命令（按顺序执行）

```bash
# 1. 容器状态
docker ps

# 2. 容器最近日志（看有没有明显报错）
docker logs --tail=120 hermes-minimaxlab

# 3. gateway service 目录状态
docker exec hermes-minimaxlab ls -la /run/service/gateway-default/

# 4. s6 service 列表（看有没有 marked as down）
docker exec hermes-minimaxlab /package/admin/s6-2.15.0.0/command/s6-svc -l /run/service/gateway-default

# 5. gateway 进程是否存活
docker exec hermes-minimaxlab ps aux | grep -i gateway

# 6. Hermes 主进程
docker exec hermes-minimaxlab ps aux | grep -i hermes
```

---

## 关键经验

> **如果 `/run/service/gateway-default/` 里有 `down` 文件，gateway 已被 s6 置为下线。**
> 这通常是因为 gateway 进程连续失败超过阈值，s6 自动将它降权。
> 恢复方法是让 s6 重新读取 service 状态，而不是重启容器。

---

## 标准恢复命令

### 场景一：gateway-default 有 down 文件

```bash
# 1. 删除 down 文件
docker exec hermes-minimaxlab rm -f /run/service/gateway-default/down

# 2. 让 s6 重新加载并启动 gateway
docker exec hermes-minimaxlab /package/admin/s6-2.15.0.0/command/s6-svc -u /run/service/gateway-default

# 3. 等待3秒，检查进程是否起来
sleep 3
docker exec hermes-minimaxlab ps aux | grep -i gateway

# 4. 验证：Telegram 发 /start，观察 docker logs 有无新日志
docker logs --tail=30 hermes-minimaxlab
```

### 场景二：gateway 进程不存在且无 down 文件

```bash
# 1. 先查 s6 日志
docker exec hermes-minimaxlab cat /run/service/gateway-default/logs/current

# 2. 手动触发 s6 启动
docker exec hermes-minimaxlab /package/admin/s6-2.15.0.0/command/s6-svc -u /run/service/gateway-default

# 3. 等待5秒后验证
sleep 5
docker exec hermes-minimaxlab ps aux | grep -i gateway
```

---

## 恢复后验证

按顺序执行，全部通过才算恢复成功：

1. **Telegram 发 `/start`** — 应有响应
2. **Telegram 发 `ping`** — 应回 pong
3. **观察 docker logs** — 确认有新的 bot 处理日志
4. **多发几次不同命令** — 确认非偶发性故障

如果以上任何一步失败，停止操作，记录当前状态，报告给总控。

---

## 恢复后必须更新日志

每次恢复操作后，必须在 DAILY_WORK_LOG.md 或本次对话中记录：

```
时间：
故障现象：
诊断步骤：
恢复操作：
操作者：
结果：
```

---

## 责任链

- 谁诊断：记录诊断步骤和发现
- 谁决定恢复：记录恢复方案
- 谁操作：记录执行的具体命令
- 谁验证：记录验证结果

**禁止匿名恢复。** 不署名的恢复操作视为无效操作。