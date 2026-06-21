# Mac Execution Bridge — 可靠性陷阱（2026-06-12）

## 问题 1：Bridge shell stdout 不可靠

Bridge `shell` 命令回传的 stdout 可能不完整。具体表现：
- 大量输出（100K+ chars）被截断，剩余部分丢在 `[OUTPUT TRUNCATED]` 后
- 某些命令似乎返回空 stdout，但 Mac 实际执行成功
- `bridge_check.py` 轮询有时返回 `{}`（空输出），即使 Mac 端实际有 stdout

**验证方法**：
- `CMD_STATUS: $?` 检查 exit code（0=成功，非0=失败）
- `ls -la` 输出对比 exit code（exit 0 + 空输出 ≠ 目录不存在）
- 关键路径请用户在 Mac Terminal 上直接确认

## 问题 2：rsync exit code 23（部分错误）

症状：
```
rsync: open (2) in /Users/macos/angelife.github.com: No such file or directory
rsync error: some files could not be transferred (code 23)
```

原因：目标目录不存在或路径层次不对。rsync --delete 删除不存在的目标子目录时不报错，但 open errors 表示目标路径缺失。

**修复**：先 `cp -a` 再清理旧文件，或确保目标目录完整。

## 问题 3：SSH 超时

Docker → Mac 的 SSH 连接经常超时（30s 不够）。症状：
- `fork/exec /usr/bin/ssh: operation timed out`
- git push/clone/fetch 无一例外

**已知条件**：
- Mac 端 bridge executor 在运行（PID 63722）
- 短 shell 命令（`ls`, `echo`）正常返回
- SSH key 已存在（`~/.ssh/id_ed25519`）
- 但 git 操作和长命令 SSH 超时

**workaround**：短命令用 `--wait` + 15s timeout。长命令/ssh 操作换到 Mac Terminal。

## 问题 4：Bridge executor 停止

bridge_client.log 显示 executor 曾收到退出信号：
```
[Wed Jun 10 21:25:46 CST 2026] Mac Execution Bridge 启动 | PID: 63722
[21:42:26] 收到退出信号，停止执行器
```

重启方式：
```bash
# Mac 上
mkdir -p ~/bridge
# 传 executor 脚本
scp -o StrictHostKeyChecking=no -i ~/.ssh/id_ed25519 \
    /opt/data/bridge/mac_executor.sh \
    macos@host.docker.internal:~/bridge/
# 启动
nohup bash ~/bridge/mac_executor.sh &
```