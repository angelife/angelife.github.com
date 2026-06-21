# v0.6.38 容器检查结果速查

> 来源：v0.6.38 任务，NVIDIA 对运行中容器执行完整检查。

## 关键发现

主库已挂载，但路径不是 `/repo`，而是 `/workspace/angelife.github.com`。

## 实际挂载链路

```
宿主机 /Users/macos/angelife.github.com
  → 容器 /workspace/angelife.github.com  （docker inspect 确认）
  → 符号链接 /repo（需手动创建，或等待新容器方案）
```

## 容器实际参数

| 项目 | 值 |
|------|-----|
| 容器名 | `hermes-minimaxlab` |
| 镜像 | `nousresearch/hermes-agent:latest` |
| Entrypoint | `/init /opt/hermes/docker/main-wrapper.sh` |
| 用户 | root |
| 工作目录 | `/workspace` |
| 网络 | bridge（172.17.0.2） |
| 重启策略 | no |

## 挂载清单

```json
"Binds": [
  "/Users/macos/.hermes-docker/minimaxlab:/opt/data",
  "/Users/macos/angelife.github.com:/workspace/angelife.github.com"
]
```

注意：没有 `/repo` 挂载。`/repo` 需要通过 symlink 指向 `/workspace/angelife.github.com` 或等新容器方案。

## s6 服务状态

- `main-hermes`：✅ 存活
- `gateway-default`：✅ 存活，无 `down` 文件
- Telegram gateway 进程：✅ 运行中（PID 207）

## /repo 路径方案

**方案一（临时，本轮可执行）**：
```bash
docker exec hermes-minimaxlab ln -sf /workspace/angelife.github.com /repo
```
重启后丢失。

**方案二（推荐，等授权后执行）**：
新建容器，同时挂载两路径：
```
/Users/macos/angelife.github.com:/repo
/Users/macos/angelife.github.com:/workspace/angelife.github.com
```

## v0.6.39 验证结果

v0.6.39 任务中，NVIDIA 成功通过 `/repo` 直接写入主库文件（symlink 已由本地 Mac 创建）。

验证命令：
```bash
cd /repo && pwd && git status -sb && ls README.md AI_BOOTSTRAP.md hugo-site
```

## 快速诊断命令

```bash
# 1. 容器状态
docker ps

# 2. 挂载情况
docker inspect hermes-minimaxlab --format '{{json .Mounts}}' | jq

# 3. 主库是否可访问
ls /repo/README.md
git -C /repo status -sb

# 4. gateway 状态
docker exec hermes-minimaxlab ls /run/service/gateway-default/
# 若有 down 文件：docker exec hermes-minimaxlab /package/admin/s6-2.15.0.0/command/s6-svc -u /run/service/gateway-default
```