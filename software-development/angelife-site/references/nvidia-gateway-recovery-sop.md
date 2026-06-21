# NVIDIA_GATEWAY_RECOVERY.md 速查

> 摘要自 v0.6.37 生成的完整 SOP 文档。完整版见项目根目录 NVIDIA_GATEWAY_RECOVERY.md。

## 故障判断流程

先区分是容器/Hermes/gateway/Telegram 哪层问题：

```
docker ps
docker logs --tail=120 hermes-minimaxlab
docker exec hermes-minimaxlab ls /run/service/gateway-default/
docker exec hermes-minimaxlab ps aux | grep -i gateway
```

## 关键经验

**如果 `/run/service/gateway-default/` 里有 `down` 文件，gateway 已被 s6 标记为下线。**
这是最常见的 NVIDIA 不回复原因。

## 恢复命令

```bash
# 删除 down 文件并让 s6 重新加载
docker exec hermes-minimaxlab rm -f /run/service/gateway-default/down
docker exec hermes-minimaxlab /package/admin/s6-2.15.0.0/command/s6-svc -u /run/service/gateway-default
```

## 禁止事项（故障时）

- ❌ docker stop / restart / rename / run / attach
- ❌ 立即挂载主库
- ❌ 立即做 git 操作或发布

## 恢复后验证

Telegram 发 `/start` 和 `ping`，观察 docker logs 有无新日志。