# 多 AI 协作处理同一 Kindle 的冲突避免（2026-06-11 实战记录）

## 背景

2026-06-11 的 Kindle K3 部署 session 中，用户分配了两个 AI：
- AI A：负责越狱（找 jailbreak bin，准备 MKK）
- AI B（Hermes）：负责 KOReader 文件准备、keystore 部署、完整性验证

## 发现的变化（AI A 操作后）

| 项目 | 变化 |
|------|------|
| `Update-mkk-20250419-k3w-B008_keystore-install.bin` | **被移除**（根目录清空） |
| `autostart_koreader.sh` | **被移除** |
| `runme.sh` | **被移除** |
| `koreader_backup_*`（2 个目录） | **被删除** |
| `launchpad/koreader.ini` | **消失**（目录变空） |

## 协调原则

1. **不重复下载** — 先问用户另一台是否已处理
2. **每次操作前重新验证** — 其他 AI 可能清理了文件
3. **输出变更摘要** — 让用户知道哪些文件变化了
4. **不假设状态** — 即使前一轮你刚部署过，其他 AI 可能已删除

## 冲突检测

```bash
# 拍快照
ssh ... 'find /Volumes/Kindle -type f | sort' > /tmp/kindle_snapshot_before.txt

# 重新验证
ssh ... 'find /Volumes/Kindle -type f | sort' | diff /tmp/kindle_snapshot_before.txt -
# 输出显示删除/新增的文件
```

## 恢复策略

如果其他 AI 删除了你需要的关键文件：

1. 不要重复下载 — 文件在 Docker 本地可能还有缓存
2. 直接从 Docker scp 到 Mac 再 cp 到 Kindle
3. 部署后立即验证

```bash
# 从 Docker 重新补全缺失文件
scp -o StrictHostKeyChecking=no -i /opt/data/home/.ssh/id_ed25519 \
  /opt/data/kindle/mkk/DevCerts/Update-mkk-20250419-k3w-B008_keystore-install.bin \
  macos@host.docker.internal:/tmp/

ssh ... 'cp /tmp/Update-mkk-20250419-k3w-B008_keystore-install.bin /Volumes/Kindle/ && sync'
```