# SCP from Docker Container to Mac Host（2026-06-10 验证）

## 问题

Docker 容器需要将文件传输到 Mac 宿主机（如复制到 `/Volumes/Kindle`）。
HTTP server 方式在 Docker Desktop for Mac 上**不工作**：

```
容器内 python3 -m http.server 9997
→ Mac: curl http://172.17.0.2:9997/file  → exit=52（空响应）
→ Mac: curl http://host.docker.internal:9997/file  → 不通（DNS 解析到不同 IP）
```

## 解决方案

使用 `scp` 走 SSH 协议通过 `host.docker.internal`：

```bash
# 从容器传到 Mac ~/Downloads
scp -o StrictHostKeyChecking=no -i ~/.ssh/id_ed25519 \
  /opt/data/path/to/file \
  macos@host.docker.internal:~/Downloads/

# 然后在 Mac 上操作（通过 SSH）
ssh -o StrictHostKeyChecking=no -i ~/.ssh/id_ed25519 macos@host.docker.internal \
  "cp ~/Downloads/file /Volumes/Kindle/ && sync"
```

## 前提

- Mac 已开启 Remote Login（SSH）
- Hermes 公钥已在 Mac 的 `~/.ssh/authorized_keys` 中
- `host.docker.internal` DNS 解析可工作（Docker Desktop for Mac 自动设置）

## 已验证（2026-06-10 实际执行）

```
scp .../Update_mkk-20141129-k3w-B008_install.bin macos@host.docker.internal:~/Downloads/kindle_fix/
→ 成功（exit=0，文件传输到 Mac）

ssh macos@host.docker.internal "cp ~/Downloads/kindle_fix/file.bin /Volumes/Kindle/ && sync"
→ 成功（文件出现在 Kindle 根目录）
```

## 对比

| 方法 | 结果 |
|------|------|
| 容器 HTTP server + Mac curl `host.docker.internal:PORT` | ❌ |
| 容器 HTTP server + Mac curl `172.17.0.2:PORT` | ❌ |
| SCP via `host.docker.internal` | ✅ |
| SSH + `curl -o` from Mac to external | ✅ |