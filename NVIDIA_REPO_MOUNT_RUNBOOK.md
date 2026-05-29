# NVIDIA 主库挂载预检与安全启动方案

> 本文档基于 v0.6.38 实际容器配置检查生成。
> 本轮不执行挂载，不重启容器，不做任何变更。

---

## 容器实际启动参数

从 `docker inspect` 提取关键信息：

| 项目 | 值 |
|------|-----|
| 容器名 | `hermes-minimaxlab` |
| 镜像 | `nousresearch/hermes-agent:latest` |
| Entrypoint | `/init /opt/hermes/docker/main-wrapper.sh` |
| 用户 | root |
| 工作目录 | `/workspace` |
| 重启策略 | no（无自动重启） |
| 网络 | bridge（172.17.0.2） |
| 平台 | linux/amd64 |
| s6 监督 | 启用（s6-overlay） |

---

## 当前挂载状态

从 `HostConfig.Binds` 和 `Mounts` 提取：

| 宿主机路径 | 容器路径 | 读写 | 说明 |
|-----------|---------|------|------|
| `/Users/macos/.hermes-docker/minimaxlab` | `/opt/data` | RW | Hermes 数据目录 |
| `/Users/macos/angelife.github.com` | `/workspace/angelife.github.com` | RW | **主库已挂载** |

**关键发现：主库已经挂载。挂载路径是 `/workspace/angelife.github.com`，不是 `/repo`。**

容器内 `/workspace/angelife.github.com` = 宿主机的 `/Users/macos/angelife.github.com`。

---

## 当前 env / service / gateway 状态

**环境变量**：
```
HERMES_HOME=/opt/data
HERMES_WEB_DIST=/opt/hermes/hermes_cli/web_dist
HOME=/root
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
WorkingDir=/workspace
```

**进程状态**（`ps aux`）：
```
PID  CMD
 17  /bin/sh -e /run/s6/basedir/scripts/rc.init top ...
 37  s6-supervise main-hermes
120  s6-supervise gateway-default
122  s6-supervise gateway-default/log
123  s6-log ... /opt/data/logs/gateways/default
130  hermes (main agent)
207  hermes gateway run ← Telegram gateway 进程，运行中
```

**s6 service 目录**：
- `/run/service/main-hermes` → 存活
- `/run/service/gateway-default` → 存活，无 `down` 文件

**结论**：
- Telegram gateway 正在运行（PID 207）
- s6 supervise 正常工作
- 无 down 文件
- gateway 进程状态正常

---

## 为什么之前手写 docker run 可能失败

常见失败原因：

1. **路径错误**：尝试挂载到 `/repo` 而不是实际可用的 `/workspace/angelife.github.com`
2. **工作目录不一致**：容器的 `WorkingDir` 是 `/workspace`，如果挂载到其他路径，文件不在预期位置
3. ** Entrypoint 差异**：不使用 `/init /opt/hermes/docker/main-wrapper.sh` 会导致 s6 服务无法正常启动
4. **重启策略丢失**：手写 `docker run` 如果不加 `--restart=no`，可能得到不同行为
5. **未保留现有挂载**：漏了 `/opt/data` 挂载会导致 Hermes 配置丢失

---

## 主库访问方式（已可用）

**正确路径**：在容器内使用 `/workspace/angelife.github.com`

```bash
# 验证主库可访问
cd /workspace/angelife.github.com
ls README.md AI_BOOTSTRAP.md hugo-site

# 检查 git 状态
cd /workspace/angelife.github.com
git status -sb
```

---

## 推荐方案：安全添加 /repo 别名路径

如果不希望每次写 `/workspace/angelife.github.com`，可以在**本轮不重启容器**的情况下：

**方案 A（本轮不推荐，等授权后执行）**：
创建新的带 `/repo` 别名的容器，同时确保：
1. 保留现有两个挂载
2. 保留 Entrypoint
3. 不修改 RestartPolicy
4. 验证 Telegram gateway 在新容器中仍正常

**方案 B（立即可用，本轮即可执行）**：
直接在当前容器内创建符号链接，将 `/repo` 指向 `/workspace/angelife.github.com`：

```bash
# 本轮可执行，不影响运行中的容器
docker exec hermes-minimaxlab ln -sf /workspace/angelife.github.com /repo

# 验证
docker exec hermes-minimaxlab ls -la /repo
```

**方案 B 风险**：重启后丢失（因为 symlink 在容器文件系统内，重启会丢失）。适合立即验证用。

---

## 完整启动命令（方案 A 的参考，不在本轮执行）

```bash
docker run -d \
  --name hermes-minimaxlab-new \
  --hostname hermes-minimaxlab \
  -v /Users/macos/.hermes-docker/minimaxlab:/opt/data \
  -v /Users/macos/angelife.github.com:/repo \
  -v /Users/macos/angelife.github.com:/workspace/angelife.github.com \
  --entrypoint "/init" \
  --restart=no \
  nousresearch/hermes-agent:latest \
  /opt/hermes/docker/main-wrapper.sh
```

**注意**：
- 同时保留 `/repo` 和 `/workspace/angelife.github.com` 两种挂载（兼容不同路径的引用）
- 必须保留 `/opt/data` 挂载（Hermes 配置）
- Entrypoint 必须保持 `/init /opt/hermes/docker/main-wrapper.sh`

---

## 回滚方案

如果新容器启动后 Telegram gateway 异常：

```bash
# 停止新容器
docker stop hermes-minimaxlab-new

# 恢复旧容器（如有备份镜像）
# 旧容器 ID 或名称在切换前记录

# 如果需要恢复：使用 docker commit 保存新容器状态，然后回退
docker stop hermes-minimaxlab-new
docker rm hermes-minimaxlab-new

# 验证旧容器正在运行
docker ps | grep hermes-minimaxlab
```

---

## 验证命令（/repo 路径就绪后）

```bash
# 基本结构验证
ls /repo/README.md /repo/AI_BOOTSTRAP.md /repo/hugo-site

# Git 状态（只读）
cd /repo && git status -sb

# Hugo 源存在性
ls /repo/hugo-site/content/ /repo/hugo-site/static/

# 微信认证文件存在（不得删除）
ls /repo/0847745cb78663855a3a1732c9c6a130.txt
```

---

## 初期权限限制

即使 `/repo` 路径可用，NVIDIA 初期权限：

| 权限 | 状态 |
|------|------|
| 读取 `/repo` 文件 | ✅ 可用 |
| 写入 `/repo` 文件 | ✅ 可用（但必须精确） |
| git add | ❌ 禁止 |
| git commit | ❌ 禁止 |
| git tag | ❌ 禁止 |
| git push | ❌ 禁止 |
| `./tools/angelife-release` | ❌ 禁止 |

---

## 禁止事项

- ❌ `git add .` — 必须精确指定文件
- ❌ 提交 `_incoming/` 或 `.reasonix/`
- ❌ 删除微信认证文件
- ❌ 未授权发布
- ❌ 直接重启运行中的容器（先报告）
- ❌ 匿名施工

---

## 责任链

- 配置分析：NVIDIA（本文件）
- 主库路径确认：NVIDIA
- symlink 创建（如执行）：本地 Mac
- 新容器启动（如执行）：本地 Mac
- 回滚操作（如需要）：本地 Mac
- 验证：本地 Mac + 人类用户

---

## 附件：当前 docker run 参考

以下是从 `docker inspect` 还原的启动命令（仅供参考，不执行）：

```bash
# 还原现有容器参数的参考命令
docker ps --format "{{.ID}} {{.Image}} {{.Command}}" | grep hermes-minimaxlab

# 当前容器实际使用的完整参数
# Image: nousresearch/hermes-agent:latest
# Entrypoint: /init /opt/hermes/docker/main-wrapper.sh
# Binds:
#   /Users/macos/.hermes-docker/minimaxlab:/opt/data
#   /Users/macos/angelife.github.com:/workspace/angelife.github.com
# WorkingDir: /workspace
```