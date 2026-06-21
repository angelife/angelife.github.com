# Hermes Docker 进程布局与内存占用

## 典型进程布局

Hermes Docker 容器启动后，默认有三个 Hermes 相关进程：

```
PID  ├─ 1  s6-svscan                         ← PID 1
     ├── main-hermes (sleep infinity)         ← s6 槽位，零内存
     ├── <CMD: hermes>                        ← 主程序（交互 CLI / hermes chat）
     │     约 130–180 MB RSS
     ├── <gateway-default: hermes gateway run> ← 网关（Telegram 等平台）
     │     约 200–250 MB RSS
     └── <第二 CLI 会话>                       ← 另一终端接入（如 docker exec）
           约 250–300 MB RSS
```

### 各进程职责

| 进程 | 来源 | 必要？ |
|---|---|---|
| `main-hermes` (sleep infinity) | s6-rc.d 槽位，无操作 | 可忽略（零内存） |
| **CMD hermes** (PID 最早) | 容器入口 `main-wrapper.sh` 执行的交互 CLI | 容器主进程，一般不必要额外占用 |
| **gateway-default** | cont-init 注册的 gateway 服务 | 与外部平台通信的核心 |
| **第二 CLI 会话** | 用户 `docker exec` 或二次接入 | 临时诊断用，用完可退出 |

### 典型内存总开销

三实例并行时合计可达 **600-700 MB RSS**:

- CMD hermes: ~150 MB
- 第二 CLI: ~250 MB (当前对话会话)
- gateway: ~220 MB
- Hugo server (如有): +120 MB

## 诊断方法

### 查看当前进程树

```sh
ps aux --forest | grep hermes
```

关注 RSS 列（第 6 列，单位 KB），识别出所有 hermes 进程。

### 识别 Gateway 进程

```sh
ps aux | grep "gateway run" | grep -v grep
# 通常一个，约 200+ MB RSS
```

### 识别 CMD 与二次 CLI

CMD 进程是最早启动的（START 时间与容器启动一致），通常绑定 pts/0：
```sh
ps aux | grep "pts/0.*hermes" | grep -v grep
```

二次 CLI 绑定 pts/1+，或者没有 TTY（'?'）：
```sh
ps aux | grep "pts/1.*hermes" | grep -v grep
```

## 瘦身方案

### 方案 A: 仅 Gateway + 当前会话

保留 gateway 和当前 CLI 会话，杀掉 CMD 主进程：
- CMD hermes 通常有单独 TTY 且不需要交互
- 杀掉后可释放 ~130-180 MB
- 风险：CMD 退出可能导致容器 exit（取决于容器配置），建议确认容器重启策略为 `always`

### 方案 B: 仅 Gateway

如果不需 CLI 交互，只留 gateway：
- 从 Mac 主机调整容器启动命令：`docker run ... hermes gateway run`
- 或进入容器后启动 gateway，退出所有的 CLI 会话
- 此时内存 ~220-250 MB

### 方案 C: 纯 CLI 模式

停掉 gateway（`/command/s6-svc -d /run/service/gateway-default/`），只用一个 CLI 会话：
- memory ~130-180 MB
- 适合不需要 Telegram 等平台连接的情况

### 确认容器重启策略

确保不管用哪种方案，容器不会因为杀掉进程而退出：
```sh
docker inspect <容器名> | grep -A5 RestartPolicy
# "RestartPolicy": {"Name": "always"} 或 "unless-stopped" 为安全
```

## Hugo Server 处理

容器内如果有多余的 Hugo server 进程（root 用户运行，约 120 MB）：
- 通常是容器启动时外部脚本拉起的，不在 s6 服务链中
- 在容器内以 hermes 用户无法 kill（root 进程）
- 从 Mac 主机用 `docker exec` 可杀：`docker exec <容器名> kill <PID>`
- 容器重启后不再出现，因为它不是 s6 注册服务
