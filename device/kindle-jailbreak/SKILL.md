---
name: kindle-jailbreak
description: Kindle 越狱与 KOReader 安装工作流 — 设备兼容性判断、越狱步骤、KOReader 安装。覆盖 Kindle 3/4/5/PW/Touch/Voyge/Oasis 各代。调查阶段不执行任何写入操作。
version: 1.5.0
author: hermes-agent
platforms: [macos, linux]
metadata:
  hermes:
    tags: [kindle, koreader, jailbreak, ko-reader, e-reader, mobile-read]
---

# Kindle 越狱与 KOReader 安装

## 触发条件

用户提到以下任意关键词时加载：
- "Kindle 越狱"
- "Kindle jailbreak"
- "KOReader"
- "kindletool"
- 在 Kindle 设备上安装第三方阅读器

## 核心原则

### 用户指令模式识别（经多次纠正后沉淀）

用户有固定的沟通模式。提前识别可以节省多轮对话：

| 用户说 | 含义 | 立即执行 |
|--------|------|----------|
| "不要继续猜测" / "进入验证模式" / "不要理论" / "不要编造步骤" | 停止分析！证据优先 | 关闭理论模式 → 检查文件系统（`ls /Volumes/Kindle/` → `disabled-updates/` → `documents/`） |
| "输出：已确认事实/未确认事实/下一步唯一动作" | 要求结构化报告 | 按此三段式格式输出，不加分析过程 |
| "完全授权 你自己去做" / "你来搞定" | 用户想最小化参与 | 如果 SSH 可用就无人化执行；否则给唯一一条命令让用户执行 |
| 用户长段中文无标点 | 意识流，期望我主动结构 | 提炼关键信息，不要逐字回复 |
| "都说了是免费服务器" / "你一下子开那么多请求" | **NVIDIA 40 RPM 打满了！** | 立即停止所有 SSH/curl 操作，等 10 秒再继续 |

### NVIDIA 40 RPM 硬上限（此条优先于所有操作） ⚠️

NVIDIA 免费 API 有 **40 requests per minute** 硬上限。超限会导致：
- API 超时/挂起数分钟
- SSH 连接 hang
- iteration 5/90 死锁模式

**所有** `ssh` 和 `curl` 调用后必须：
```bash
# 必须加！否则会打满 RPM
sleep 3
# 批处理原则：能塞进一条命令的绝不拆成多条
# 坏的：下载 → sleep → 解压 → sleep → 复制 → sleep
# 好的：ssh user@host "curl ... && unzip ... && cp ... && sync"
```

**禁止在同一轮对话中连续发起 3 个以上串行 SSH/curl 操作。**
如果被用户提醒 \"不要开太多请求\"，立即停止并等待 10 秒再继续。

## 已知支持的型号（截至 2025 年）

| 型号 | 代数 | 固件范围 | 越狱状态 | 签名选择 |
|------|------|----------|----------|----------|
| Kindle 3 (Keyboard) | 3rd | 3.3.x ~ 3.4.x | ✅ 完全支持，最稳定 | ⚠️ **K3 使用 KDK 签名版 KUAL 是正常的。** 不存在"MKK 签名版 KUAL"——KUAL 本身就是 KDK 签名。MKK（MobileRead Kindlet Kit）是提供证书链的独立组件，不是 KUAL 的版本分类。K3 安装 KUAL 需要 MKK 证书链（2014 MKK + 2025 keystore 更新），然后 KDK 签名版 KUAL 即可正常工作。KDK 签名版 ≠ 需要 Test Kindle 注册。Test Kindle 错误通常是因为证书链不完整（MKK 2014 未装或 keystore 过期）。 |
| Kindle 4 | 4th | 4.1.x ~ 4.2.x | ✅ 支持 | KDK 或 MKK |
| Kindle 5 | 5th | 5.0.x ~ 5.1.x | ✅ 支持 | KDK 或 MKK |
| Kindle Paperwhite 1 | PW1 | 5.2.x ~ 5.4.x | ✅ 支持 | KDK 或 MKK |
| Kindle Paperwhite 2 | PW2 | 5.4.x ~ 5.6.x | ✅ 支持 | KDK 或 MKK |
| Kindle Paperwhite 3 | PW3 | 5.6.x ~ 5.8.x | ✅ 支持 | KDK 或 MKK |
| Kindle Paperwhite 4 | PW4 | 5.8.x ~ 5.13.x | ✅ 支持 | KDK 或 MKK |
| Kindle Paperwhite 5 | PW5 | 5.14.x ~ 5.16.x | ⚠️ 部分支持，取决于固件 | — |
| Kindle 10 | 10th | 5.12.x ~ 5.14.x | ⚠️ 部分支持 | — |
| Kindle 11 | 11th | — | ⚠️ 取决于固件版本 | — |
| Kindle 12 | 12th | — | ❌ 不支持，越狱工具未发布 | — |

## 用户提供 Shell 脚本 → Bridge 适配执行模式（2026-06-11 模式识别）

当用户发来一个 shell 脚本（比如诊断脚本、检查脚本），预期我在 Kindle 本机上执行时，需要**主动进行路径翻译**，不能直接执行。

### 路径映射规则

用户脚本写的是 Kindle 本机路径（`/koreader`, `/mnt/us/`, `/var/local/`），需翻译为 Mac USB 挂载路径：

| 用户脚本中的 Kindle 路径 | Mac USB 挂载等效路径 |
|------------------------|---------------------|
| `/koreader/` | `/Volumes/Kindle/koreader/` |
| `/mnt/us/` | `/Volumes/Kindle/` |
| `/documents/` | `/Volumes/Kindle/documents/` |
| `/developer/` | `/Volumes/Kindle/developer/` |
| `/var/local/` | **不可见**（Kindle 系统分区，USB 不暴露） |
| `/opt/` | **不可见**（Kindle 系统分区） |
| `ps \| grep koreader` | 不可行（Mac 不能查 Kindle 进程） |
| `logread` | 不可行（Kindle 系统日志，USB 不可见） |
| `date -s` | 不可行（需 SSH/USBNet） |

### 典型处理流程

1. 用户发一个 Kindle shell 脚本
2. **识别 Kindle-native 命令**并标记为不可执行（`ps`, `logread`, `date -s`, `/var/local/` 访问）
3. **翻译文件路径**：`/koreader` → `/Volumes/Kindle/koreader/`
4. **通过 Bridge 执行翻译后的脚本**（Mac 端执行文件系统操作）
5. **回传结果**并标注哪些检查项因权限不足无法执行
6. 对于真正需要在 Kindle 上执行的命令（启动 koreader、检查进程），告知用户需要在 Kindle 本机搜索栏输入或通过 KUAL 操作

### Kindle 诊断脚本 → Bridge 翻译对照表（快速参考）

当用户发一个 shell 脚本要你"在 Kindle 上执行"时，用此对照表快速翻译每条命令：

| 用户写的 Kindle 命令 | 翻译为 Bridge shell 命令 | 可执行？ |
|----------------------|-------------------------|----------|
| `ls -l /koreader` | `ls -la /Volumes/Kindle/koreader/` | ✅ |
| `ls -l /documents` | `ls -la /Volumes/Kindle/documents/` | ✅ |
| `ls -l /developer` | `ls -la /Volumes/Kindle/developer/` | ✅ |
| `ls -l /mnt/us/xxx` | `ls -la /Volumes/Kindle/xxx` | ✅ |
| `find /koreader -name "*.sh"` | `find /Volumes/Kindle/koreader -name "*.sh"` | ✅ |
| `du -sh /koreader` | `du -sh /Volumes/Kindle/koreader/` | ✅ |
| `cat /var/local/developer.keystore` | 不可见（系统分区） | ❌ |
| `ls /var/local/` | 不可见（系统分区） | ❌ |
| `ps \| grep koreader` | 不可行（Mac 不能查 Kindle 进程） | ❌ |
| `/koreader/koreader.sh` | 不可行（ARM 二进制 + 需 Kindle 框架） | ❌ |
| `logread` | 不可行（Kindle 系统日志，USB 不可见） | ❌ |
| `date -s "2025-04-01"` | 不可行（需 SSH/USBNet） | ❌ |
| 检查 `<某个文件>` 是否存在 | `test -f /Volumes/Kindle/... && echo FOUND \|\| echo NOT_FOUND` | ✅ |
| 检查文件 MD5/SHA | `shasum -a 256 /Volumes/Kindle/...` | ✅ |

**处理流程**：
1. 扫描用户脚本中每行命令
2. 标记 ❌ 命令（需要 Kindle 本机操作或在搜索栏输入）
3. 翻译 ✅ 命令为 Bridge shell 格式
4. 批量执行翻译后的命令
5. 返回结果时标注哪些检查项因权限不足无法执行
6. 对于 ❌ 命令，告知用户需要手动在 Kindle 搜索栏输入或通过 KUAL 操作

**输出格式示例**：
```
# Kindle KOReader 状态（通过 Bridge 间接检查）

可执行的检查：
- /koreader/ → ✅ 1015 文件，92MB ✓
- /koreader/koreader.sh → ✅ 存在 + 可执行 ✓
- /documents/KUAL-KDK-1.0.azw2 → ✅ 131KB ✓

不可执行的检查（需在 Kindle 上操作）：
- 启动 koreader → 搜索栏输入 ~run /koreader/koreader.sh
- 查进程 → 只能在 Kindle 本机 ps
- 查系统日志 → 搜索栏输入 ;dm 或 ;log
```

### 示例

用户发：
```sh
ls -l /koreader
/koreader/koreader.sh >/tmp/koreader_run.log 2>&1 &
ps | grep koreader
```

处理：
- ✅ `ls -l /koreader` → Bridge shell：`ls -la /Volumes/Kindle/koreader/`
- ❌ `/koreader/koreader.sh` → 不能在 Mac 上执行（ARM 二进制 + 需要 Kindle 框架）
- ❌ `ps | grep koreader` → 不能在 Mac 上查询 Kindle 进程

正确响应：翻译文件检查部分 + 告知用户需要手动在 Kindle 搜索栏输入 `~run /koreader/koreader.sh` 或通过 KUAL 启动。

### 关键坑

- **不要直接在 Mac 上运行 koreader.sh！** 这是 ARM 二进制，Mac 是 x86_64/ARM64，架构不兼容
- **不要用 Bridge shell 执行 `chmod +x` 后直接 run** — 即使架构匹配，也需要 Kindle 的 framebuffer 环境
- **文件检查用 Bridge shell，程序运行必须由用户在 Kindle 上操作**
- **Bridge shell 命令中避免特殊符号**：`echo === step ===` 在 zsh 上会触发 `== not found` 错误。用 `echo ALL_DONE` 替代。
- **文件完整性校验不能用纯 `find | wc -l`**：需要对比 zip vs deployed 的差异才能发现缺失文件。用 `scripts/validate-koreader-deploy.py`

## DeviceCerts/keystore 下载（通过 Bridge 从 Docker 到 Kindle，2026-06-11 验证）

本 session 验证了完整的 keystore 自动部署流程：从 MobileRead 下载 → Docker 解压 → scp 到 Mac → cp 到 Kindle。

### 下载（Docker 容器内直接用 curl，无需 Referer）

```bash
curl -sL -o /tmp/DevCerts-20250419-KeyStore.zip \
  'https://www.mobileread.com/forums/attachment.php?attachmentid=215127&d=1745098511' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
# HTTP 200, 103KB → 成功
```

### Docker 内解压（Python zipfile，因容器无 unzip）

```python
import zipfile
z = zipfile.ZipFile('/tmp/DevCerts-20250419-KeyStore.zip')
z.extract('Update-mkk-20250419-k3w-B008_keystore-install.bin', '/tmp/')
# 文件确认: 10,067 bytes
```

### scp 到 Mac

```bash
scp -o StrictHostKeyChecking=no -i /opt/data/home/.ssh/id_ed25519 \
  /tmp/Update-mkk-20250419-k3w-B008_keystore-install.bin \
  macos@host.docker.internal:/tmp/
```

### Bridge 复制到 Kindle 根目录

```bash
BRIDGE_WAIT_TIMEOUT=30 python3 /opt/data/bridge/bridge_send.py --wait shell \
  '{"commands":["cp /tmp/Update-mkk-20250419-k3w-B008_keystore-install.bin /Volumes/Kindle/ && sync && ls -lh /Volumes/Kindle/Update-mkk-20250419-k3w-B008_keystore-install.bin"]}'
# → 9.8KB 文件在 Kindle 根目录
```

### 验证结果

```bash
ssh ... 'ls -lh /Volumes/Kindle/Update-mkk-20250419-k3w-B008_keystore-install.bin'
# → -rwx------ macos staff 9.8K
```

### 多 AI 协作模式（2026-06-11 验证）

当多个 AI 同时处理同一 Kindle 时（一台做越狱，另一台做文件准备），需协调避免冲突：

**协调原则**：
1. **不重复下载** — 先确认对方是否已下载的文件（用户会说"另一个机器正在下载"）
2. **不重复部署** — 另一台可能清理了根目录（`*.bin`、`*.sh`、备份目录被移除），部署前重新验证
3. **状态同步** — 每次操作 Kindle 根目录之前，先检查有哪些文件，输出为摘要让对方知道变更

**典型协作场景**：
- AI A: 越狱（写 jailbreak.bin、处理 MKK 安装）
- AI B: 文件准备（下载 KOReader、keystore、KUAL，验证完整性）
- 协调：AI B 先确认 AI A 已完成越狱后再部署 keystore，否则顺序错乱

**冲突检测**：
```bash
# 比较两次检查的文件变化
diff <(ssh ... 'find /Volumes/Kindle -type f | sort') <(cat /tmp/kindle_snapshot_before.txt)
# 发现 *.bin 文件消失、*.sh 消失、备份目录消失 = 另一台处理过
```

### KOReader 部署到 Kindle USB（通过 Mac Execution Bridge，2026-06-11 验证）

### 前提
- Bridge 已启动并运行（bridge_client.py PID 在运行）
- Kindle 已通过 USB 挂载到 Mac（`/Volumes/Kindle/`）
- KOReader zip 已在 Docker 容器内就绪

### 部署流程

**Step 1: scp zip 到 Mac**
```bash
scp -o StrictHostKeyChecking=no -i /opt/data/home/.ssh/id_ed25519 \
  /opt/data/kindle/koreader/koreader-kindle-legacy-v2026.03.zip \
  macos@host.docker.internal:~/Downloads/
```

**Step 2: nohup 后台解压到 Kindle（因 USB FAT32 写入慢，不能同步等）**
```bash
ssh -o StrictHostKeyChecking=no -i /opt/data/home/.ssh/id_ed25519 \
  macos@host.docker.internal \
  'KINDLE="/Volumes/Kindle"; ZIP="$HOME/Downloads/koreader-kindle-legacy-v2026.03.zip"; \
   if [ -d "$KINDLE/koreader" ] && [ "$(ls -A $KINDLE/koreader 2>/dev/null)" ]; then \
     mv "$KINDLE/koreader" "${KINDLE}/koreader_backup_$(date +%s)"; fi; \
   nohup bash -c "unzip -q -o $ZIP -d $KINDLE && sync && \
     echo UNZIP_DONE_AT_$(date +%s) > ~/Downloads/koreader_deploy_done.txt" \
     > ~/Downloads/koreader_deploy.log 2>&1 & echo "PID=$!"'
```

**Step 3: 轮询完成（每次间隔 15-20s）**
```bash
ssh ... 'cat ~/Downloads/koreader_deploy_done.txt 2>/dev/null && echo "DONE" || echo "STILL_RUNNING"'
```

**Step 4: 验证（1015 文件 = 完成）**
```bash
ssh ... 'du -sh /Volumes/Kindle/koreader/; find /Volumes/Kindle/koreader -type f | wc -l'
```

### 验证结果（2026-06-11）

| 检查项 | 值 |
|--------|----|
| 文件数 | 1015 |
| 总大小 | 92MB |
| `koreader.sh` | ✅ 存在 + 可执行 |
| `luajit` | ✅ 存在 + 可执行 |
| `fbink` | ✅ 存在 + 可执行 |
| `launchpad/koreader.ini` | ✅ 启动器配置 |
| KUAL-KDK-1.0.azw2 | ✅ 在 documents/ (131KB, KDK 签名版) |

### 已知坑

#### KOReader 解压后缺失 6 个文件（extensions/ + launchpad/）

KOReader zip 是 1021 个文件，直接 `unzip -o` 到 USB 后**不等于**全部到位。2026-06-11 实测发现 6 个文件缺失：

```
Missing: 6
  ❌ extensions/koreader/README.txt
  ❌ extensions/koreader/bin/koreader-ext.sh
  ❌ extensions/koreader/bin/libkohelper.sh
  ❌ extensions/koreader/config.xml
  ❌ extensions/koreader/menu.json
  ❌ launchpad/koreader.ini
```

**根因**：zip 解压后 `extensions/koreader/` 和 `launchpad/` 的某些文件可能因 `koreader/` 目录名冲突（zip 中 `koreader/` 是顶层，但 `extensions/koreader/` 是子路径）而被漏掉。

**验证方法**：
```bash
python3 -c "
import zipfile
z = zipfile.ZipFile('koreader-kindle-legacy-v2026.03.zip')
# Mac 上已部署的文件
kindle_files = set()
for line in open('/dev/stdin'):  # 从 find 结果 piped
    kindle_files.add(line.strip().replace('/Volumes/Kindle/', ''))
missing = set(z.namelist()) - kindle_files
print(f'Missing: {len(missing)}')
for f in sorted(missing):
    print(f'  ❌ {f}')
" <<< "$(find /Volumes/Kindle/koreader /Volumes/Kindle/extensions /Volumes/Kindle/launchpad -type f)"
```

**修复**：
```bash
# 从 zip 单独提取 extensions/ 和 launchpad/
python3 -c "
import zipfile
z = zipfile.ZipFile('/tmp/koreader-kindle-legacy-v2026.03.zip')
for f in z.namelist():
    if f.startswith('extensions/') or f.startswith('launchpad/'):
        z.extract(f, '/tmp/koreader_fix/')
"
cp -a /tmp/koreader_fix/extensions/koreader /Volumes/Kindle/extensions/
cp -a /tmp/koreader_fix/launchpad/koreader.ini /Volumes/Kindle/launchpad/
```

#### Bridge shell 命令 JSON 编码陷阱（2026-06-11 实测）

Bridge 的 `shell` action 使用 `commands` 数组，每条命令用 `&&` 串接。zsh 对 `===` 等符号会解析为特殊语法：

```bash
# ❌ 会报错：zsh:1: == not found
python3 /opt/data/bridge/bridge_send.py --wait shell \
  '{"commands":["echo === step1 === && ls /Volumes/Kindle/"]}'

# ✅ 正确：用 && 拼接完整命令，不加多余特殊符号
python3 /opt/data/bridge/bridge_send.py --wait shell \
  '{"commands":["mkdir -p /Volumes/Kindle/launchpad && cp /tmp/koreader.ini /Volumes/Kindle/launchpad/ && sync && ls /Volumes/Kindle/launchpad/ && echo ALL_DONE"]}'
```

**规则**：
- `commands` 数组内每条是单行 shell 命令，`echo` 中的 `===`、`---` 等符号由 zsh 解释，可能触发 `== not found`
- 最安全方案：**合并为一条长命令，用 `&&` 串接，最后 `echo ALL_DONE` 作为成功标记**
- 避免在 `echo` 内使用 `===`、`---`、或者括号等特殊符号
- 命令字符串内不加多余空格或换行符

#### SSH timeout，SSH 默认 ConnectTimeout 不够。用 nohup 后台方案分离部署与等待。
- **zip 文件名准确**: JSON 内 shell 命令中的文件名写错（如 `koreander` vs `koreader`）会导致 `unzip: cannot find file`。解压前先用 `ls -lh "$ZIP"` 验证。
- **旧目录自动备份**: 如果 `/Volumes/Kindle/koreader/` 已有内容，自动 mv 为 `koreader_backup_<timestamp>`。
- **chmod**: zip 内文件通常已有 +x 权限，但建议解压后验证 `stat` 确认。

---

| 项目 | 结论 |
|------|------|
| 最新版本 | **v2026.03**（2026-03-17 发布，5222 次下载） |
| 架构 | 32-bit ARM Little Endian（✅ 匹配 K3 i.MX3x ARMv5） |
| K3 专用文件 | ✅ `event_map_keyboard.lua`, `k3_alt_and_top_row.lua`, `keyboard_layout.lua` |
| FW 版本检查 | **KOReader 本身无 FW 版本检查。** `koreader.sh` 未引用 3.3/3.4/version。FW 3.3 兼容性只取决于 KUAL 启动器，不是 KOReader |
| KUAL 入口 | `extensions/koreader/menu.json` 中 "Start KOReader (no framework)" 条目**无条件**（无 `if` 设备条件），K3 上必定可见 |
| 下载地址 | `https://github.com/koreader/koreader/releases/download/v2026.03/koreader-kindle-legacy-v2026.03.zip` |
| SHA256 | `17934813a53575ed235edfc8ac12b4b6b1e3d5915d63b7796a77b1d7f19dee03` |
| 文件大小 | 40,592,260 bytes（1021 个文件） |

**`kindle-legacy` vs `kindle` vs `kindlehf` vs `kindlepw2`：**

| 变体 | 适用设备 |
|------|----------|
| `kindle-legacy` | **K2/K3/DX/DXG**（ARMv5，最老架构） |
| `kindle` | K4/K5/Touch（ARMv6/v7） |
| `kindlehf` | Kindle 8/10（高分辨率） |
| `kindlepw2` | PW2/PW3/Voyage/Oasis（高 DPI） |

**K3 必须用 `kindle-legacy` 变体。** 使用其他变体会因架构不兼容（ARMv5 vs ARMv7）导致 `koreader.sh` 能跑但 reader 二进制崩溃。

**K3 MKK 公开下载源（2026-06-04 验证，2026-06-11 校验和更新）**

**详细 URL、校验和、Docker 本地路径、安装流程见 `references/k3-mkk-public-downloads-20260605.md`**

**2026-06-11 验证的 SHA256（Docker 容器内下载）**：

```bash
# 全部下载到 /opt/data/kindle/mkk/
├── mkk.tar.xz
│   SHA256: 3d7289f1ddcf18cebb67053cd33ac5ecd7b4a8116bd11d3c75dd6f220a7d8d9d
│   └── DevCerts/Update_mkk-20141129-k3w-B008_install.bin
│       SHA256: 44b695739774d46f50815eccdf253a10f0014e46e4d0411dafd6265b4b8cc859
│       SIZE: 90,038 bytes
│   └── DevCerts/Update_mkk-20141129-k3w-B008_uninstall.bin
│       SHA256: 853b75c1f6d8d05f5f078262cfafd2312e9f176df64d8fa0fc168c2e7ea89705
│       SIZE: 18,542 bytes
├── DevCerts-20250419.zip
│   SHA256: 48426add32e3567aeba9eebd639b7e3d9bd1d1bed2266a55bf23473e77acc863
│   └── Update-mkk-20250419-k3w-B008_keystore-install.bin
│       SHA256: 222275c6183d22e251cc639c5c3c7dc071025413fd4f57227c7f40e2c5ed3894
│       SIZE: 10,067 bytes
```

**Docker 本地路径（可直接用于 kindle_cp 或 file_copy）**：

| 文件 | Docker 路径 |
|------|-----------|
| MKK installer | `/opt/data/kindle/mkk/DevCerts/Update_mkk-20141129-k3w-B008_install.bin` |
| Keystore installer | `/opt/data/kindle/mkk/DevCerts/Update-mkk-20250419-k3w-B008_keystore-install.bin` |
| KOReader zip | `/opt/data/kindle/koreader/koreader-kindle-legacy-v2026.03.zip` |

---

## developer.keystore 过期 — KUAL 失效根因诊断（2026-06-08 更新）

### 核心事实

Kindlet 运行时使用 `/var/local/java/keystore/developer.keystore` 验证 KUAL 签名。
这个 keystore 在 **2025-04-17 过期**（NiLuJe 确认，t=225030 post #1295）。

此过期影响**所有** Kindle 型号（K3/K4/K5/PW/KT/Oasis/Voyage/Kindle 10/11），不限于特定代。

### 两种表现形式的同一根因

| 机型 | 显示的错误信息 | 来源 |
|------|---------------|------|
| K3 及部分旧设备 | `"The permissions to open the requested title have expired. Please contact customer service."` | t=367665 post #4 (Ebookus, K3) |
| K4/K5+/部分 PW | `"Internal Error: 003"` 或 `"Error 003"` | t=367665 post #3 (sepd, K4) |

**两者根因完全相同**：developer.keystore 过期。错误信息差异取决于 Kindle 固件版本和 Kindlet Runtime 的本地化字符串。

**Settings → Update Your Kindle 消失 ≠ KUAL 失效的原因**：消失的是 OTA 签名证书（让设备接受 .bin 更新），与 KUAL 的 Kindlet 证书是两套独立系统。

### 临时修复方案

**改系统时间到 2025-04-17 之前**（aha, t=367665 post #13，2025-04-18）：

> _"So I tried changing the date to an earlier one manually with the usbNetwork hack. That worked! A temporary fix but a fix nonetheless."_

方法：通过 USBNetwork ssh 进入 Kindle，执行：

```bash
date -s "2025-04-01"
```

然后打开 KUAL。重启后时间恢复，所以每次重启后需重设。**不是正式修复**，仅用于临场验证。

### 正式修复方案

**修复路径（K3W k3w-B008）**：

| 步骤 | 文件 | 作用 |
|------|------|------|
| 1（已完成） | `Update_mkk-20141129-k3w-B008_install.bin` | OTA 签名证书（写入成功，Update 消失 = 正常） |
| **2（缺失项）** | `Update-mkk-20250419-k3w-B008_keystore-install.bin` | **刷新 developer.keystore（解决 Error 003）** |
| 3 | `KUAL-KDK-1.0.azw2` → `/documents/` | KUAL 启动器 |

**公共下载源（无需 MobileRead 账号）**：
```
DevCerts-20250419.zip:
https://www.mobileread.com/forums/attachment.php?attachmentid=215127&d=1745098511
```
解压后取 `Update-mkk-20250419-k3w-B008_keystore-install.bin`（**不是** k3g-B006，是 k3w-B008）。

**安装顺序**：
1. 2014 MKK（OTA 证书）→ Update Your Kindle → 重启 → Update 消失
2. 2025 keystore（keystore 刷新）→ Update Your Kindle（重新出现）→ 重启
3. KUAL-KDK-1.0.azw2 → `/documents/` → Home 打开 KUAL → 无报错

**来源**：`winbamstudios/kindle3jailbreak` GitHub repo（OVH 公有云镜像）

| 文件 | URL | 大小 | 状态 |
|---|---|---|---|
| MKK 证书包 | `https://storage.gra.cloud.ovh.net/v1/AUTH_2ac4bfee353948ec8ea7fd1710574097/mr-public/Touch/kindle-mkk-20141129-r18833.tar.xz` | 295KB | ✅ HTTP 200 |
| DevCerts Keystore 2025 | `https://www.mobileread.com/forums/attachment.php?attachmentid=215127&d=1745098511` | 103KB | ✅ HTTP 200 |
| KUAL 工具包 | `https://storage.gra.cloud.ovh.net/v1/AUTH_2ac4bfee353948ec8ea7fd1710574097/mr-public/KUAL/KUAL-v2.7.37-gfcb45b5-20250419.tar.xz` | 220KB | ✅ HTTP 200 |

**MKK.tar.xz 包含 K3W 需要的文件**：`DevCerts/Update_mkk-20141129-k3w-B008_install.bin`

**KUAL.tar.xz 包含**：
- `KUAL-KDK-1.0.azw2` — K3 用（放入 /documents/ 作为书 entry）
- `Update_KUALBooklet_v2.7.37_install.bin` — K4+ 用（Settings → Update）
- `Update_KUALBooklet_hotfix_v2.7.37_install.bin` — 热修复版

**devcerts.zip（MobileRead 附件）**：`Update-mkk-20250419-k3w-B008_keystore-install.bin`

**K3 需要安装两段**：先装 2014 MKK 证书（建信任链），再装 2025 keystore（更新证书）。然后才能用 KUAL。

**安装顺序（K3W）**：
1. 解压 mkk.tar.xz → `DevCerts/Update_mkk-20141129-k3w-B008_install.bin` → 放 Kindle 根目录 → Settings → Update
2. 解压 devcerts.zip → `Update-mkk-20250419-k3w-B008_keystore-install.bin` → 放 Kindle 根目录 → Settings → Update
3. 解压 kual.tar.xz → `KUAL-KDK-1.0.azw2` → 放 `/documents/` → Home 出现书 entry
4. 打开 KUAL → 菜单出现 → 完成

> ⚠️ KUAL.tar.xz 里的 `KUAL-KDK-1.0.azw2` 必须在 MKK 证书安装**之后**才能正常运行（否则报 Test Kindle 错误）。顺序不能乱。

> ⚠️ **K3 必须用 MKK 签名版 KUAL**：kindlemodding.org 的 KUAL 是 **KDK 签名版**，一打开就报 "Test Kindle" 错误。K3 需要 MKK 签名版，**有公开下载渠道，不需要 MobileRead 账号**，详见上方「K3 MKK 公开下载源」章节。

## 关键教训（2026-06-04 K3 "Test Kindle" 修复 session）

**⚠️ K3 的 Test Kindle 错误根因已确认**：
kindlemodding.org 的 KUAL 是 **KDK 签名版**（Amazon Test Kindle 官方证书），不是 MKK 社区签名版。K3 未注册为 Test Kindle，**一打开 KUAL 就报错**，不是选菜单才报错。

**GitHub 上无 MKK/KUAL 仓库（已验证 2026-06-04）**：
- ❌ `angelife/kindle-mkk` — 404（不存在）
- ❌ `angelife/kindle-kual` — 404（不存在）
- 这些仓库地址是旧计划中的占位符，从未创建

**OVH 公有云有公开镜像**（已验证 HTTP 200，2026-06-04）：
- `storage.gra.cloud.ovh.net` 上有 MobileRead 原始文件的完整镜像
- `devcerts.zip`（attachmentid=215127）不需要登录即可下载
- URL 来源：`winbamstudios/kindle3jailbreak` GitHub README（非官方镜像，URL 可能变化）

**MKK 文件清单**（全部需要 MobileRead 账号下载）：
1. `Update_mkk-20141129-k3w-B008_install.bin` — MKK 证书包（帖子 t=233936）
2. `Update-mkk-20250419-k3w-B008_keystore-install.bin` — MKK keystore 更新（帖子 t=213336）
3. MKK 签名版 KUAL Booklet — 同上帖子

**完整修复流程（K3W，2026-06-04 验证，无需 MobileRead 账号）**：

1. Mac Terminal 下载所有文件（见上方「K3 MKK 公开下载源」表格）
2. 解压 mkk.tar.xz → `DevCerts/Update_mkk-20141129-k3w-B008_install.bin` → 放 Kindle 根目录
3. 解压 devcerts.zip → `Update-mkk-20250419-k3w-B008_keystore-install.bin` → 放 Kindle 根目录
4. 解压 kual.tar.xz → `KUAL-KDK-1.0.azw2` → 放 `/documents/`
5. **删除旧的 KDK 签名版 KUAL**（/documents/KUAL-KDK-1.0.azw2 存在则先删）
6. Kindle 根目录有 bin → Settings → Update Your Kindle（安装 2014 MKK 证书，等待重启）
7. 重启后再 Update Your Kindle（安装 2025 keystore，等待重启）
8. 打开书库的 KUAL-KDK-1.0.azw2 → **不再报 Test Kindle 错误 = 成功**

## KUAL 签名与 MKK 证书链的真实关系（2026-06-09 重要修正）

**重要修正**：此前版本错误地认为"K3 需要 MKK 签名版 KUAL"或"KDK 版 KUAL 需要 Test Kindle 注册"。经 Claude/ChatGPT 和 2025-2026 社区反馈纠正：

### 核心事实

1. **KUAL 本身只有 KDK 签名版**，不存在独立的"MKK 签名版 KUAL"
2. **MKK（MobileRead Kindlet Kit）** 是提供**证书链**的组件，不是 KUAL 的签名类型
3. **KDK 签名版 KUAL 在 K3 上正常使用**——前提是 MKK 证书链完整

### 安装顺序（2025-2026 社区验证成功率最高的方案）

```
1. 固件升级到 3.4.3（可选但推荐，部分 KUAL 构建要求 ≥ 3.4）
2. Jailbreak（kindlemodding.org 下载）
3. 安装 MKK 2014 证书包（Update_mkk-20141129-k3w-B008_install.bin）
4. 安装 DevCerts 2025 keystore 更新（Update-mkk-20250419-k3w-B008_keystore-install.bin）
5. 放入 KUAL-KDK-1.0.azw2 到 /documents/
6. 打开 KUAL（正常启动）
```

**不装 MKK 2014 直接装 2025 keystore 可能无效**——社区报告显示缺底层信任链时，keystore 更新不起作用。

### 四种错误 vs 根因对应表（2026-06-10 重要更新）

| 错误信息 | 根因 | 修复 |
|---------|------|------|
| `permissions to open this title have expired` (K3) / `Error 003` (K4+) | **developer.keystore 过期**（2025-04-17） | 装 DevCerts-20250419 中的 keystore installer .bin |
| `not registered as a Test Kindle` — **已安装 MKK 2014 + keystore 2025 后仍然出现**（2026-06-10 新发现） | **K3 FW 3.3 不兼容 KUAL 2025 版最低固件检查** — 即使 MKK 2014 + 2025 keystore 全部正确安装，KUAL-KDK-1.0.azw2 (NiLuJe 2025-04-19 构建) 在 FW 3.3 上仍报 Test Kindle。这不是证书链问题，是 KUAL 打包时设置的最低 FW 版本检查（≥ 3.4） | 升级固件到 3.4.3，或使用不检查 FW 版本的旧版 KUAL |
| `not registered as a Test Kindle` — **证书链未正确安装时** | **证书链不完整**（MKK 2014 未装 / keystore 过期），或 KUAL 不是从官方渠道下载 | 先装 MKK 2014，再装 2025 keystore |
| `requires a new version of Kindle software` | **K3 固件太低（3.3）**，KUAL 打包时要求 ≥ 3.4 | 升级到 3.4.3 固件 |

**关键诊断分叉（2026-06-10 实战验证）**：当 K3 FW 3.3 装上 MKK 2014 + keystore 2025 后仍报 Test Kindle 时，不要继续怀疑证书链。确认方法：
1. 检查 `disabled-updates/` 状态（如果空或不存在，但 Update 灰显且根目录无 .bin = 已安装）
2. 检查 FW 版本（Settings → Device Info → About: 3.3.x = 问题在此）
3. 结论：Test Kindle on FW 3.3 after full cert chain = **需要升级固件**，不是缺证书

**关键**：Test Kindle 报错通常意味着 MKK 2014 证书未被正确安装，或 keystore 已过期，导致签名验证链断裂。证书链完整时，KDK 签名版 KUAL 在未注册 Test Kindle 的 K3 上也可正常运行。

### KUAL-KDK-1.0.azw2 vs KUAL-KDK-2.0.azw2

| 文件 | 区别 | K3 兼容性 |
|------|------|-----------|
| `KUAL-KDK-1.0.azw2` (131,069 字节) | 旧版 KUAL，兼容性最好 | K3 优先选择 |
| `KUAL-KDK-2.0.azw2` (131,070 字节) | 新版 KUAL，UI 改进 | K3 可用，但部分构建要求 FW ≥ 3.4 |

### K3 升级必要性判断框架（2026-06-10）

| 场景 | 升级到 3.4.3 建议 | 原因 |
|------|-------------------|------|
| KOReader 工作正常 | ❌ 不升级 | 当前状态已满足阅读需求，升级会清除越狱 |
| KOReader 报 "requires newer firmware" | ⚠️ 可能需要 | 先确认 FW 版本，再决定是否值得重越狱 |
| KUAL 打不开（permissions expired） | ❌ 不升级 | 装 2025 keystore 即可修复，与 FW 版本正交 |
| MKK + keystore 全部装完仍报 Test Kindle | ⚠️ 考虑升级 | 此时问题在 FW 版本检查（KUAL 要求 ≥ 3.4） |
| 用户想用最新版 KUAL 功能 | ⚠️ 考虑升级 | 接受重越狱成本，准备好 MKK 文件 |
| 用户明确要求升级 | ✅ 执行 | 用户决定优先于技术建议 |

升级前提检查清单：
1. ✅ 已下载正确的 3.4.3 .bin（K3 最高固件）
2. ✅ 准备好升级后的重新越狱工具链（MKK 2014 + 2025 keystore + KUAL）
3. ✅ 备份当前 KOReader 配置（koreader/settings/ 目录）
4. ⚠️ 接受固件升级 + 越狱交互的风险

K3 的最高固件是 3.4.3。Amazon 官方下载已下线。

**已知失效的来源（已验证 2026-06-10）**：
- ❌ Internet Archive Timegate — 返回 HTML 页面，不是 .bin 文件
- ❌ Internet Archive CDX API（web.archive.org/cdx/search）— 从 Docker 容器内不可达（exit 35 SSL）
- ❌ kindlemodding.org /firmware/Legacy/ — 404
- ❌ OVH 公有云镜像 mr-public/Firmware/ — 404
- ❌ Amazon S3 原始 URL — 404

**可能的来源**：
- MobileRead 论坛 t=233932 — 需注册账号下载附件
- GitHub 搜索 `update_kindle_3.4.3.bin` （未验证）
- 已知有固件备份的社区成员

**不升级固件的替代方案**：
- 如果 KUAL 报 "requires newer firmware" 或 "not registered as a Test Kindle" 且证书链已完整（MKK 2014 + keystore 2025）：**问题不在证书，在 FW 版本**
- 使用不检查 FW 版本的旧版 KUAL 构建（需自行构建或从社区获取）

## 关键工具

| 工具 | 用途 | 地址 |
|------|------|------|
| KindleTool | 创建/解压 Kindle 更新包 | https://github.com/NiLuJe/KindleTool |
| KOReader | 开源阅读器，支持 PDF/DjVu/EPUB/FB2 | https://github.com/koreader/koreader |
| MobileRead 论坛 | 越狱讨论主战场 | https://www.mobileread.com/forums/forumdisplay.php?f=150 |
| **KindleModding Wiki** | **越狱文件镜像（GitHub Pages，含 K3 jailbreak .bin 文件）** | https://kindlemodding.org/jailbreaking/Legacy/K2DXDXGK3-Jailbreak/ |

> **重要更新（2026-06-04）**：KindleModding Wiki 的 KUAL 是 **KDK 签名版**，K3 不能用。MKK 文件**必须**从 MobileRead 账号下载，没有公开镜像。jailbreak .bin 仍可从 kindlemodding.org 下载。

## 工作流

### Step 0：确认设备型号和固件版本

**用户操作**（或在 Kindle 屏幕上查看）：
```
Settings → Menu → About My Kindle
```

得到两个信息：
1. **型号名称**（e.g., "Kindle Paperwhite 5"）
2. **固件版本**（e.g., "5.16.2.1"）

**或通过 USB 连接后读取**（Mac 终端）：
```bash
ls /Volumes/Kindle/
# 查找 system/ 目录下的 .bin 文件或版本信息
```

### Step 1：判断可行性

- 如果是 Kindle 12 代 → 告知目前不支持，等待社区更新
- 如果固件 ≥ 5.16.x → 部分功能受限，但可能有解
- 如果是 Kindle 3/4/5/PW1-4 → 继续 Step 2

### Step 2：获取越狱包

**K3 文件（2026-06 已验证）**：

来源：https://kindlemodding.org/jailbreaking/Legacy/K2DXDXGK3-Jailbreak/（jailbreak）和 https://kindlemodding.org/jailbreaking/post-jailbreak/installing-kual-mrpi/（KUAL/MRPI）

> ⚠️ **关键警告**：kindlemodding.org 的 KUAL 是 **KDK 签名版**，**K3 不能用**。K3 必须用 MKK 签名版 KUAL（从 MobileRead 下载）。kindlemodding.org 的 KUAL 适合 K4/K5+，不适合 K3。

```bash
# 在 Mac 终端直接下载（不需要 Docker）
mkdir -p ~/Downloads/kindle_k3
cd ~/Downloads/kindle_k3

# Jailbreak（K3W = Keyboard WiFi）—— 可从 kindlemodding.org 下载
curl -L "https://kindlemodding.org/jailbreaking/Legacy/K2DXDXGK3-Jailbreak/k3_3.2.1/Update_jailbreak_k3w_install.bin" \
  -o Update_jailbreak_k3w_install.bin

# KOReader（约 38 MB）—— 可从 GitHub 下载
curl -L "https://github.com/koreader/koreader/releases/download/v2026.03/koreader-kindle-legacy-v2026.03.zip" \
  -o koreader-kindle-legacy.zip

# ⚠️ KUAL — 不要从这里下载（KDK 签名版，K3 报 Test Kindle 错误）
# curl -L "https://kindlemodding.org/jailbreaking/post-jailbreak/installing-kual-mrpi/KUALBooklet.azw" \
#   -o KUAL-KDK-1.0.azw2

# MRPI（K3 需要）—— 可从 kindlemodding.org 下载
curl -L "https://kindlemodding.org/jailbreaking/post-jailbreak/installing-kual-mrpi/kual-mrinstaller-1.7.N-r19303.zip" \
  -o kual-mrinstaller-1.7.N-r19303.zip
```

> **K3 唯一的 KUAL 来源**：必须从 MobileRead 注册账号后下载 MKK 签名版。详见上方「关键教训」章节。

其余文件来源：
- MobileRead 论坛帖子附件（`Update_mkk-20141129_k3_install.bin` 等）— K3 KUAL 安装**必须**，无替代来源

文件名规律（通用）：
- `Update_*.bin` — 越狱核心包
- `KUAL*.bin` — KUAL 启动器
- `koreader-*.zip` — KOReader 安装包

### Step 3：复制到 Kindle 并安装（K3 完整流程）

**在 Mac 终端执行（不是 Docker）**：

```bash
# 1. 确认 Kindle 已挂载
ls /Volumes/Kindle/

# 2. 复制 jailbreak 和 KUAL AZW 到对应位置（J3 使用 AZW，K4+ 用 .bin）
cp ~/Downloads/kindle_k3/Update_jailbreak_k3w_install.bin /Volumes/Kindle/
# K3: AZW 放入 documents/（不是 .bin，不走 Settings → Update）
cp ~/Downloads/kindle_k3/KUAL-KDK-1.0.azw2 /Volumes/Kindle/documents/

# 3. 解压 MRPI 并复制 extensions 目录
unzip -o ~/Downloads/kindle_k3/kual-mrinstaller-1.7.N-r19303.zip -d /tmp/mrpi_extracted
cp -R /tmp/mrpi_extracted/extensions/ /Volumes/Kindle/extensions_mrpi/

# Merge MRPI's MRInstaller into existing extensions/ (don't overwrite)
if [ -d /Volumes/Kindle/extensions/ ]; then
    cp -R /tmp/mrpi_extracted/extensions/MRInstaller/ /Volumes/Kindle/extensions/MRInstaller_mrpi/
else
    mv /Volumes/Kindle/extensions_mrpi/MRInstaller/ /Volumes/Kindle/extensions/MRInstaller/
fi
rm -rf /Volumes/Kindle/extensions_mrpi/

# 4. 创建 MRPI 工作目录（MRPI 需要此目录）
mkdir -p /Volumes/Kindle/mrpackages/

# 5. 解压 KOReader（同时写两个位置，兼容性最好）
unzip -o ~/Downloads/kindle_k3/koreader-kindle-legacy.zip -d /tmp/ko_unpack

# KUAL 通过扫描 extensions/*/menu.json 来发现入口
mkdir -p /Volumes/Kindle/extensions/koreader
cp -R /tmp/ko_unpack/extensions/koreader/* /Volumes/Kindle/extensions/koreader/

# KOReader 主程序（实际启动时用）
cp -R /tmp/ko_unpack/koreader/ /Volumes/Kindle/koreader/

# 6. 安全弹出
diskutil eject /Volumes/Kindle
```

**在 Kindle 屏幕上操作（按顺序，顺序不能乱）：**

> ⚠️ **K3 关键区别**：KUAL 在 K3 上是 AZW 文档（书entry），不是固件更新 .bin。K5+ 以后的设备才用 Update .bin 方式安装。

```
Step 1 → Settings → Update Kindle → 点 Update_jailbreak_k3w_install.bin
    （等待安装完成，设备自动重启）

Step 2 → 重开后，将 KUAL-KDK-1.0.azw 复制到 /Volumes/Kindle/documents/
    （不是 .bin 文件，不需要走 Settings → Update Kindle）
    ★ Home 图书列表里出现"KUAL"书entry（书图标）

Step 3 → 打开 KUAL 书 → KUAL 菜单出现
    （KUAL 此时已自动扫描 extensions/*/menu.json，
      发现 extensions/koreader/menu.json → 显示 KOReader 条目）

Step 4 → KUAL 菜单里选 KOReader → Start KOReader
```

### K3 KUAL 安装方式（重要修正）

**错误理解**：KUAL Booklet .bin 通过 Settings → Update Kindle 安装
**正确理解（K3）**：KUAL 是 AZW 文档，放入 `/documents/` 后作为书entry出现在 Home

| 安装方式 | 设备 |
|---|---|
| `Update_KUALBooklet_v2.7.37_install.bin` via Settings → Update | K4/K5/PW/Touch/Voyage/Oasis（K3 不适用） |
| `KUAL-KDK-1.0.azw2` 复制到 `/documents/` → Home 出现书 entry | **K3（Keyboard）唯一方式** |

K3 上安装 KUAL 的正确 .bin 文件是 `Update_KUALBooklet_v2.7.37_install.bin` 用于 **K4+ 设备**。K3 唯一可用的是 AZW 格式。

### KOReader 启动入口（核心知识点）

KOReader 的 `extensions/koreader/menu.json` 中有一条关键入口：

```json
{
  "name": "Start KOReader (no framework)",
  "action": "/mnt/us/koreader/koreader.sh",
  "params": "--kual --framework_stop"
}
```

此条**无 `if` 设备条件**，K3 上必定可见，是最可靠的启动方式。

**KUAL 菜单发现机制**：KUAL 启动器通过扫描 `extensions/*/menu.json` 来自动发现入口项。KOReader 必须同时存在于：
1. `/extensions/koreader/menu.json` — **KUAL 菜单入口**
2. `/koreader/` — **KOReader 主程序**

**MRPI 触发方式**：在 Home 搜索栏输入 `;log mrpi` → 回车 → MRPI 菜单打开。KUAL 的 Helper → Install MR Packages 入口**本身就是调 MRPI**，`;log mrpi` 是备用直接触发方式。

**K3 原厂固件不会从 `extensions/` 自动启动程序**，Jailbreak + KUAL 是唯一可靠的启动链路。

| `koreader-check-k3.sh` | Run on Mac to verify K3 KOReader readiness (model, KUAL, keystore, update, ZIP checksum) | `scripts/koreader-check-k3.sh` |
| `validate-koreader-deploy.py` | Python 3 script that compares zip vs deployed files to detect missing extensions/launchpad/etc | `scripts/validate-koreader-deploy.py` |

#### validate-koreader-deploy.py

## 文件传输到 Kindle（Bridge 模式，2026-06-10）

重要：文件在 Mac 上 vs 在 Docker 容器内，用不同方式传输。

### 方案 A：文件已在 Mac 上（常用）

```bash
python3 /opt/data/bridge/bridge_send.py --wait shell \
  '{"commands":["cp ~/Downloads/book.epub /Volumes/Kindle/documents/ && echo COPY_OK"]}'
```

优点：不需要 Docker 中转、无额外开销。

### 方案 B：文件在 Docker 容器内

```bash
python3 /opt/data/bridge/bridge_send.py --wait kindle_cp \
  '{"source":"/tmp/book.epub","dest":"documents/book.epub"}'
```

源文件必须在 Docker 容器内（不在 Mac 上），否则 scp 报 No such file or directory。

### 方案 C：文件名含中文

```bash
# 1. Mac 上重命名
python3 /opt/data/bridge/bridge_send.py --wait shell \
  '{"commands":["cp ~/Downloads/中文书名.epub /tmp/english.epub && echo OK"]}'
# 2. 用 shell cp 写到 Kindle
python3 /opt/data/bridge/bridge_send.py --wait shell \
  '{"commands":["cp /tmp/english.epub /Volumes/Kindle/documents/ && echo OK"]}'
```

当用户明确说"不要安装"、"只做文件搜集"、"生成文件清单"时，走此分支。

### 标准输出格式（6列 Manifest）

生成 `/opt/data/<target_device>/MANIFEST.md`，格式固定为：

```
文件名
SHA256
下载地址
镜像地址
适用机型
适用固件
```

### K3 已知文件清单（已验证）

**KOReader legacy** — GitHub Release 有完整包
- SHA256: `17934813a53575ed235edfc8ac12b4b6b1e3d5915d63b7796a77b1d7f19dee03`
- URL: `https://github.com/koreader/koreader/releases/download/v2026.03/koreader-kindle-legacy-v2026.03.zip`
- 适用: K2/K3/DX/DXG，固件 2.5.8-3.4.x

**K3 jailbreak 文件（已验证可直接下载，不需要 MobileRead）**：
- K3 jailbreak .bin — kindlemodding.org（见 Step 2 下载命令）
- KUAL-KDK-1.0.azw2 — kindlemodding.org（KDK 签名版，K5+ 用，K3 会报错）

**MKK 相关文件（2026-06-04 验证：全部可公开下载）**：
- `DevCerts/Update_mkk-20141129-k3w-B008_install.bin` — MKK 证书（mkk.tar.xz 里）
- `Update-mkk-20250419-k3w-B008_keystore-install.bin` — keystore 更新（devcerts.zip 里）
- MKK 签名版 KUAL Booklet — KUAL.tar.xz 里（`KUAL-KDK-1.0.azw2`）

> ⚠️ **重要修正**：错误认知是"MKK 文件必须从 MobileRead 下载"。实际上 `storage.gra.cloud.ovh.net` 公有云有完整镜像，不需要 MobileRead 账号。devcerts.zip 附件（attachmentid=215127）也不需要登录即可下载。

### Internet Archive 研究技巧（CDX API）

查找已删除网页的原始 URL：
```bash
# 查 MobileRead 帖子的存档版本
curl -s "https://web.archive.org/cdx/search/cdx?url=mobileread.com/forums/*jailbreak*&output=text&fl=original&limit=10"

# 查找特定 .bin 文件的存档
curl -s "https://web.archive.org/cdx/search/cdx?url=*/Update_jailbreak*.bin&output=text&fl=original,statuscode&limit=10"

# 获取帖子的时间线
curl -s "https://web.archive.org/web/timemap/link/https://www.mobileread.com/forums/showthread.php?t=225936"
```

### GitHub NiLuJe 工具链

所有开源工具的源码都在 https://github.com/NiLuJe/，但**预编译发布文件**需要从 MB 下载：
- KindleTool — 有 GitHub Release: `https://github.com/NiLuJe/KindleTool/releases`
- KUAL_Booklet — 无 Release，源码在 GitHub，bin 在 MB
- KOReader — 有 GitHub Release，直接下

## Docker 环境注意事项

**关键陷阱：Docker 容器内 `/opt/data/` 与 Mac 终端文件系统完全隔离**

这是本 session 最反复出现的阻断项。Docker 容器和 Mac 是两个独立的文件系统：
- `/opt/data/kindle_koreader/` 在**容器内**，Mac 终端 `ls /opt/data/` 看不到
- `/Volumes/Kindle` 在**Mac 系统上**，Docker 容器内不存在
- `docker cp` 需要 docker CLI 访问运行中的容器，且 Mac 终端默认不用这个方式

**Docker mount 路径在 Mac Finder 中不可访问（2026-06-04 实测）**：
- 容器内 `/macos/.hermes-docker/minimaxlab/` 在 Mac Finder 中不存在
- 原因：Docker 容器和 Mac 文件系统隔离，mount 路径只在容器内有效
- **正确做法**：让用户在 Mac Terminal 直接执行 curl 下载文件到 `~/kindle_k3_fix/`，不要依赖 Docker 容器作为中转站

**最简工作流（用户在 Mac 终端执行，一行命令搞定）**：
```bash
mkdir -p ~/kindle_k3_fix && cd ~/kindle_k3_fix && \
curl -sL "https://storage.gra.cloud.ovh.net/v1/AUTH_2ac4bfee353948ec8ea7fd1710574097/mr-public/Touch/kindle-mkk-20141129-r18833.tar.xz" -o mkk.tar.xz && tar -xf mkk.tar.xz && \
curl -sL "https://www.mobileread.com/forums/attachment.php?attachmentid=215127&d=1745098511" -o devcerts.zip && \
curl -sL "https://storage.gra.cloud.ovh.net/v1/AUTH_2ac4bfee353948ec8ea7fd1710574097/mr-public/KUAL/KUAL-v2.7.37-gfcb45b5-20250419.tar.xz" -o kual.tar.xz && tar -xf kual.tar.xz && \
echo "完成，文件在 ~/kindle_k3_fix/"
```

之后在 Finder 拖文件到 Kindle：
- `~/kindle_k3_fix/DevCerts/Update_mkk-20141129-k3w-B008_install.bin` → Kindle **根目录**
- `~/kindle_k3_fix/DevCerts/Update-mkk-20250419-k3w-B008_keystore-install.bin` → Kindle **根目录**（来自 devcerts.zip）
- `~/kindle_k3_fix/KUAL-KDK-1.0.azw2` → Kindle **documents/**

Docker 容器只负责：
- 验证下载 URL 是否有效（HTTP 200）
- 生成部署日志和安装说明
- 把文件清单和步骤文档化

## kindletool 运行时依赖（关键陷阱）

kindletool 依赖 `libarchive.so.13`（Linux）或等效动态库。**Docker 容器内几乎必定缺失**，且在无 root 环境中无法通过 apt/pip/conda 安装。

**症状**：`kindletool: error while loading shared libraries: libarchive.so.13: cannot open shared object file`

**解决方案（已验证有效）**：
1. **Mac 本机安装**（最可靠）：`brew install kindletool` → 直接在 Mac 终端运行，不走 Docker
2. **静态二进制**：GitHub Release 无静态构建，NiLuJe 的 CI artifacts 需登录 GitHub 才能访问

**不要在此技能会话内（Docker 容器）尝试修复 kindletool**。所有 kindletool 相关操作（构建 update.bin、解压 .bin 文件）都应在 Mac 本机终端执行，或者直接绕过 kindletool 走 direct USB copy 路径。

## Mac Execution Bridge（Docker ⇄ Mac 执行平面桥接）

### 问题本质

Hermes 在 Docker 容器内，Kindle USB / Mac 文件系统 / Hugo build / rsync / token 注入全部在 Mac 物理层。这是**控制平面与执行平面被 Docker 切断**。

### 架构

```
Hermes (Docker)                     Mac (macos@host.docker.internal)
   │                                      │
   ├─ bridge_send.py ───── inbox ──────►  │  (writes JSON to /opt/data/bridge/inbox/)
   │                                      │
   │                                      ├─ bridge_client.py (2s poll loop)
   │                                      │   dispatches via SSH
   │                                      │   writes result → outbox/
   │                                      │
   ├─ bridge_check.py ◄── outbox ───────  │  (reads response from /opt/data/bridge/outbox/)
   │                                      │
   └─ bridge_check.py --clean ────────►   │  (removes consumed results)
```

**Components:**
- `/opt/data/bridge/bridge_send.py` — dispatch command to Mac. Prints `cmd_id`.
- `/opt/data/bridge/bridge_client.py` — long-running daemon (2s poll loop). Writes results to outbox.
- `/opt/data/bridge/bridge_check.py` — query results. Supports `--all` and single `cmd_id`.
- `/opt/data/bridge/bridge_check.py --clean` — clean all consumed results from inbox + outbox.

**SSH Config:**
- Key: `/opt/data/home/.ssh/id_ed25519`
- User: `macos@host.docker.internal`
- Port: 22 (default)
- ConnectTimeout: 10s

### Dispatch Patterns

#### shell — execute arbitrary commands
```bash
# Quick dispatch (returns cmd_id immediately)
python3 /opt/data/bridge/bridge_send.py shell '{"commands":["echo hello","uname -a"]}'

# Dispatch with --wait (recommended — blocks ~6s, returns result JSON directly)
# Exit codes: 0=success, 2=timeout, 3=bridge error, other=SSH exit code
python3 /opt/data/bridge/bridge_send.py --wait shell '{"commands":["echo hello","uname -a"]}'
```

#### file_copy — copy file from Docker to Mac
⚠️ **Source file MUST exist on Docker first.** scp runs Docker→Mac; missing file → exit 255.
```bash
ls -la /tmp/myfile.txt  # verify first
python3 /opt/data/bridge/bridge_send.py --wait file_copy '{"source":"/tmp/myfile.txt","dest":"bridge/myfile.txt"}'
```

#### kindle_cp — copy file from Docker to Kindle USB
Two-step: scp Docker→Mac then mv Mac→/Volumes/Kindle/.
```bash
python3 /opt/data/bridge/bridge_send.py --wait kindle_cp \
  '{"source":"/tmp/keystore.bin","dest":"documents/keystore.bin"}'
```
**Parameters:** `source` (not `src`), `dest` (not `destination`). Default dest: `documents/<basename>`.

**Safety:** mount check, auto-creates dest dir, overwrite logging, temp cleanup on all failure paths.

⚠️ **Known pitfall: files already on Mac don't need kindle_cp.** If source is already on Mac (e.g. `~/Downloads/book.epub`), use `shell` instead:
```bash
python3 /opt/data/bridge/bridge_send.py --wait shell \
  '{"commands":["cp /path/on/mac/file /Volumes/Kindle/documents/ && echo COPY_OK"]}'
```
This is faster (no scp intermediary) and avoids the "scp needs file on Docker" pitfall.

#### token_inject — inject bot tokens to Mac
```bash
python3 /opt/data/bridge/bridge_send.py token_inject \
  '{"tokens":{"telegram":"12345:ABC","discord":"xyz"}}'
```
Writes to `/tmp/token_<name>.txt` on Mac with `chmod 600`.

#### hugo_build & rsync_deploy (Angelife-specific)
Hugo build: `hugo_build` action has stale default paths. Use `shell` instead:
```bash
python3 /opt/data/bridge/bridge_send.py --wait shell \
  '{"commands":["cd ~/angelife.github.com/hugo-site && hugo --minify"]}'
```
rsync:
```bash
python3 /opt/data/bridge/bridge_send.py --wait shell \
  '{"commands":["rsync -avz --delete ~/angelife.github.com/hugo-site/public/ user@server:/path/"]}'
```

### Querying Results

#### Primary: use --wait (single-call pattern)
```bash
python3 /opt/data/bridge/bridge_send.py --wait shell '{"commands":["echo hello"]}'
# Blocks ~6s, returns result JSON, sets exit code per task status
```
`--wait` exit codes:
- `0` = task success (JSON result with status="ok")
- `2` = timeout (no result after BRIDGE_WAIT_TIMEOUT seconds, default 30s)
- `3` = bridge error (kindle not mounted, scp failure, unknown action, invalid params)
- other = SSH exit code of the remote command

#### Fallback: send + sleep + check (for async/background)
```bash
python3 /opt/data/bridge/bridge_send.py shell '{"commands":["echo hello"]}'
# → prints cmd_1781108126_2bfe37
sleep 6
python3 /opt/data/bridge/bridge_check.py --all
python3 /opt/data/bridge/bridge_check.py --clean
```

⚠️ **Do NOT use `process(wait)` to wait for bridge tasks.** Bridge cmd_ids are not Hermes processes.

### Pressure Test Results (2026-06-10)

| Metric | Value |
|--------|-------|
| Success rate | 10/10 (100%) |
| Avg response | 6.42s |
| Max response | 6.52s |
| Min response | 6.35s |
| Lost tasks | 0 |

Hugo build (402 pages, Intel Mac): ~5.4s.

### Starting / Restarting Bridge Client

```bash
ps aux | grep bridge_client | grep -v grep
kill $(ps aux | grep bridge_client | grep -v grep | awk '{print $2}') 2>/dev/null
sleep 1
# In Hermes: terminal("python3 /opt/data/bridge/bridge_client.py", background=True)
# notify_on_complete=False — this is a long-lived daemon
sleep 3
python3 /opt/data/bridge/bridge_send.py --wait shell '{"commands":["echo BRIDGE_ALIVE"]}'
```

### Known Risks & Fixes

#### 🔴 SSH PATH Deficiency
Non-login shell (`ssh cmd` without `-t`) does NOT load `~/.zshrc` or `~/.bashrc`. `bridge_client.py`'s `ssh_run()` auto-prepends `export PATH=/usr/local/bin:/opt/homebrew/bin:$PATH &&` to every command chain.

#### 🟡 Shell 命令中的特殊符号 — zsh 解析陷阱
Avoid `===`, `---`, `>>>` in `echo` statements — zsh interprets them as operators. Use `echo ALL_DONE` instead.

#### 🟡 Bridge shell command JSON encoding
Keep commands as a single long string joined with `&&`. Final `echo ALL_DONE` as success marker.

#### 🟡 Chinese/unicode filenames
Rename to ASCII first: `for f in *.epub; do cp "$f" /tmp/english.epub && echo OK; done`

### Large File Deploy to Kindle USB (FAT32)

39MB+ files take 40+ seconds to unzip on FAT32. SSH sessions time out. Use background pattern:

```bash
# Step 1: scp zip from Docker to Mac
scp -o StrictHostKeyChecking=no -i /opt/data/home/.ssh/id_ed25519 \
  /opt/data/kindle/koreader/koreader-kindle-legacy-v2026.03.zip \
  macos@host.docker.internal:~/Downloads/

# Step 2: Background unzip on Mac (nohup + marker file)
ssh -o StrictHostKeyChecking=no -i /opt/data/home/.ssh/id_ed25519 \
  macos@host.docker.internal \
  'KINDLE="/Volumes/Kindle"; ZIP="$HOME/Downloads/koreader-kindle-legacy-v2026.03.zip"; \
   nohup bash -c "unzip -q -o $ZIP -d $KINDLE && sync && \
     echo UNZIP_DONE_AT_$(date +%s) > $HOME/Downloads/deploy_done.txt" \
     > $HOME/Downloads/deploy.log 2>&1 & echo "PID=$!"'

# Step 3: Poll (check marker file)
sleep 15
ssh ... 'cat ~/Downloads/deploy_done.txt 2>/dev/null || echo "STILL_RUNNING"'

# Step 4: Verify
ssh ... 'find /Volumes/Kindle/koreader -type f | wc -l'
```

### Cleaning Up

```bash
python3 /opt/data/bridge/bridge_check.py --clean
```

### Verification: 9-Point Kindle Status Check

Use `shell` to run the checklist (`scripts/kindle-check.sh` on Mac):

```bash
python3 /opt/data/bridge/bridge_send.py --wait shell \
  '{"commands":["ls -la /Volumes/Kindle/","ls -la /Volumes/Kindle/documents/","ls -la /Volumes/Kindle/developer/","ls -la /Volumes/Kindle/disabled-updates/ 2>&1 || echo NO_DISABLED_UPDATES"]}'
```

Output format:
1. Model (USB Product ID 0x0004 = K3, Vendor 0x1949 = Lab126)
2. Firmware version (on-device, USB hides this)
3. Jailbreak status (koreader/ exists?)
4. KUAL status (documents/KUAL-KDK-*.azw2 exists?)
5. MKK status (disabled-updates/ has MKK .last-greyed?)
6. developer.keystore (developer/keystore/ exists?)
7. Update menu visibility (root has .bin?)
8. Root file list
9. Documents list

### References

- `references/kindle-bridge-2026-06-10.md` — mount verification, kindle_cp test results, FAT32 quirk
- `references/hardening-2026-06-10.md` — bridge hardening: PATH fix, --wait mode, mount check fix
- `references/stability-test-2026-06-10.md` — detailed pressure test data and timing analysis

### Scripts

- `scripts/kindle-check.sh` — Mac-side 9-point Kindle status diagnostic (copy via file_copy, run via shell)

## SSH 到 Mac 宿主机（备用方案，Bridge 更优）


### SSH到Mac方案：SSH 到 Mac 宿主机实现无人化

2026-06-09 session 发现，可以通过 SSH 从 Docker 容器直接登录 Mac 宿主机，完全绕过 docker cp 和用户手动粘贴命令的限制。

详见本章节上方的「SSH 到 Mac 宿主机操作」子章节。

### 旧的解决方案（保留向后兼容）

**重要前提**：对于 K3，即使通过 USB 把 KOReader 文件复制进去，**没有 KUAL 启动器也无法启动**。K3 原厂固件不识别 `extensions/` 里的可执行文件。USB Copy 仅适用于已越狱并安装了 KUAL 的设备，或 KPW 等支持浏览器直接运行脚本的机型。

## SSH 到 Mac 的完整重新部署脚本（2026-06-09 验证可用）

当从 Docker 容器内 SSH 到 Mac 宿主后，可以用一个脚本完成全部操作：

```bash
#!/bin/bash
# 从 Docker 容器内无人化重新部署 K3W B008
# 前提：SSH 到 Mac 的 authorized_keys 已配置

MAC="macos@192.168.1.4"
SSH_CMD="ssh -o StrictHostKeyChecking=no -i ~/.ssh/id_ed25519"

echo "=== Step 1: Check Kindle mounted ==="
$SSH_CMD $MAC "ls /Volumes/Kindle/" || { echo "Kindle not mounted"; exit 1; }

echo "=== Step 2: Download files (macOS ~/Downloads) ==="
$SSH_CMD $MAC "curl -sL -o ~/Downloads/DevCerts.zip 'https://www.mobileread.com/forums/attachment.php?attachmentid=215127&d=1745098511'"
sleep 4
$SSH_CMD $MAC "curl -sL -o ~/Downloads/KUAL.tar.xz 'https://storage.gra.cloud.ovh.net/v1/AUTH_2ac4bfee353948ec8ea7fd1710574097/mr-public/KUAL/KUAL-v2.7.37-gfcb45b5-20250419.tar.xz'"

echo "=== Step 3: Extract ==="
sleep 3
$SSH_CMD $MAC "cd ~/Downloads && unzip -o DevCerts.zip -d DevCerts_2025 && mkdir -p KUAL_unpack && tar -xf KUAL.tar.xz -C KUAL_unpack"

echo "=== Step 4: Copy keystore to Kindle ==="
sleep 3
$SSH_CMD $MAC "cp ~/Downloads/DevCerts_2025/Update-mkk-20250419-k3w-B008_keystore-install.bin /Volumes/Kindle/ && sync"

echo "=== Step 5: Copy KUAL to documents ==="
sleep 3
$SSH_CMD $MAC "mkdir -p /Volumes/Kindle/documents && cp ~/Downloads/KUAL_unpack/KUAL-KDK-1.0.azw2 /Volumes/Kindle/documents/ && sync"

echo "=== Step 6: Verify ==="
sleep 3
$SSH_CMD $MAC "ls -la /Volumes/Kindle/Update-mkk-20250419-k3w-B008_keystore-install.bin && ls -la /Volumes/Kindle/documents/KUAL-KDK-1.0.azw2 && echo 'DONE - now run Update Your Kindle on device'"
```

**注意**：此脚本使用 KDK 签名版 KUAL。如果 K3 报 "Test Kindle" 错误，需替换为 MKK 签名版 AZW2。

**NVIDIA RPM 注意**：SSH 命令之间加了 sleep 3-4 保证不超限。

**包位置**：`/opt/data/kindle_k3_usb_deploy.zip`（42 MB）
**SHA256**：`a147190ef29cf042047b4985e6f6be89257114426d2d9d4ce81b36d80124b524`

> ⚠️ **注意**：此部署包包含的是 KDK 签名版 KUAL（会导致 K3 报 Test Kindle 错误）。MKK 修复需单独下载 MKK 文件（必须从 MobileRead）。

**导出到 Mac**：
```bash
docker cp 0f6990dc817d:/opt/data/kindle_k3_usb_deploy.zip ~/Downloads/
```

**部署包结构**（直接复制整个目录到 `/Volumes/Kindle/`）：
```
kindle_k3_usb_deploy/
├── Update_jailbreak.bin         ← Step 1: Settings → Update Kindle
├── documents/
│   └── KUAL-KDK-1.0.azw2        ← ⚠️ KDK 签名版，K3 会报 Test Kindle 错误！
│                                  K3 需要从 MobileRead 下载 MKK 签名版
├── extensions/
│   ├── MRInstaller/             ← Step 3: USB copy（MRPI 不自动执行）
│   └── koreader/                ← Step 3: KUAL 发现入口
├── mrpackages/                  ← Step 3: 空目录
└── koreader/                   ← Step 3: 主程序
    └── koreader.sh             ← 启动脚本
```

**执行顺序**：
1. jailbreak .bin → Settings → Update Kindle → 重启
2. KUAL.azw → `/documents/` → Home 出现 KUAL 书 entry
3. 全部 extensions/ + koreader/ → USB copy
4. 打开 KUAL 书 → KOReader → Start KOReader (no framework)
5. MRPI（备用）：`;log mrpi` 在 Home 搜索栏输入

**KOReader 启动入口**（K3 可靠方式）：
- KUAL 菜单 → KOReader → **Start KOReader (no framework)**（无设备条件）
- 其他"Start KOReader"条目因带 `if: "KindleVoyage"` 条件在 K3 上不可见

**操作步骤**（在 Mac 终端执行）：
```bash
# 1. 确认 Kindle 已挂载
ls /Volumes/Kindle/

# 2. 解压 KOReader
unzip -o koreader-kindle-legacy.zip -d /tmp/koreader_unpack

# 3. KUAL 发现 KOReader 的关键：menu.json 必须在 extensions/koreader/
mkdir -p /Volumes/Kindle/extensions/koreader
cp -R /tmp/koreader_unpack/extensions/koreader/* /Volumes/Kindle/extensions/koreader/
cp -R /tmp/koreader_unpack/koreader/* /Volumes/Kindle/koreader/

# 4. 同步并弹出
sync
diskutil eject /Volumes/Kindle
```

**KOReader 双路径机制**：
- `/Volumes/Kindle/extensions/koreader/menu.json` — KUAL 菜单入口（KUAL 扫描此文件发现 KOReader）
- `/Volumes/Kindle/koreader/` — KOReader 主程序（KUAL 实际启动时执行 `koreader/koreader.sh`）

两个路径缺一不可。

## SSH 到 Mac 宿主机操作（2026-06-09 验证并通过用户授权使用）

### 一次性设置（用户只需做一次）

1. Mac 开启 Remote Login：**System Settings → General → Sharing → Remote Login**
2. 在 Mac Terminal 执行以下命令添加 Hermes 公钥：
   ```bash
   mkdir -p ~/.ssh && echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJHkIWHtNlyqH8NTWt6M+eBdTN/69LYbqXDa12yc9M9h hermes-docker-nvidia" >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys
   ```

### 连接命令

**推荐方式（无需知道 Mac IP）**：
```bash
ssh -o StrictHostKeyChecking=no -i ~/.ssh/id_ed25519 macos@host.docker.internal "command"
```

**备用方式（显式 IP）**：
```bash
ssh -o StrictHostKeyChecking=no -i ~/.ssh/id_ed25519 macos@192.168.1.4 "command"
```

- 用户名：`macos`（已验证，Docker Desktop 容器内自动映射）
- SSH key：`~/.ssh/id_ed25519`（位于 `/opt/data/home/.ssh/id_ed25519`）
- **关键发现**：`host.docker.internal` 作为 SSH 目标在 Docker Desktop for Mac 上可直接工作，无需知道 Mac 的局域网 IP。Hermes 容器已有 Mac 的 SSH 授权。
- Mac IP（备用）：通常 `192.168.1.x`，Docker Desktop 也可能用 `192.168.65.1` 或 `192.168.65.254`

### 已验证可执行的操作（2026-06-09 session）

```bash
# 检查 Kindle 文件系统
ssh ... "ls -la /Volumes/Kindle/"
ssh ... "ls -la /Volumes/Kindle/disabled-updates/"
ssh ... "ls -la /Volumes/Kindle/documents/"
ssh ... "ls -la /Volumes/Kindle/developer/"

# 下载文件到 Mac ~/Downloads
ssh ... "curl -sL -o ~/Downloads/DevCerts.zip 'URL' && ls -la"

# 解压
ssh ... "cd ~/Downloads && unzip -o DevCerts.zip && ls"

# 复制到 Kindle
ssh ... "cp file.bin /Volumes/Kindle/ && sync"

# 安全弹出（可能失败，直接拔线即可）
ssh ... "diskutil eject /Volumes/Kindle"  # 经常被 loginwindow 拒绝

# SHA256 校验
ssh ... "shasum -a 256 /Volumes/Kindle/file.bin"
```

### K3 KUAL 重新部署流程（从出厂重置状态开始）

当 Kindle 被恢复出厂设置后，需要重新安装全部组件。已验证的完整流程：

1. **下载所有文件**（使用 SSH 到 Mac 自动完成）：
   ```bash
   curl -sL "https://storage.gra.cloud.ovh.net/v1/AUTH_2ac4bfee353948ec8ea7fd1710574097/mr-public/Touch/kindle-mkk-20141129-r18833.tar.xz" -o ~/Downloads/mkk.tar.xz
   # (解压获取 Update_mkk-20141129-k3w-B008_install.bin)
   
   curl -sL "https://www.mobileread.com/forums/attachment.php?attachmentid=215127&d=1745098511" -o ~/Downloads/DevCerts.zip
   # (解压获取 Update-mkk-20250419-k3w-B008_keystore-install.bin)
   
   curl -sL "https://storage.gra.cloud.ovh.net/v1/AUTH_2ac4bfee353948ec8ea7fd1710574097/mr-public/KUAL/KUAL-v2.7.37-gfcb45b5-20250419.tar.xz" -o ~/Downloads/KUAL.tar.xz
   # (解压获取 KUAL-KDK-1.0.azw2 — 注意这是 KDK 签名版)
   ```

2. **复制 keystore 更新包到 Kindle 根目录**：
   ```bash
   cp ~/Downloads/DevCerts_2025/Update-mkk-20250419-k3w-B008_keystore-install.bin /Volumes/Kindle/
   sync
   ```

3. **在 Kindle 上执行 Update**
   - Home → Menu → Settings → Menu → Update Your Kindle
   - 选 keystore-install.bin → 等重启
   - 这是最关键的一步：装完 keystore 后 permissions expired 问题修复

4. **复制 KUAL AZW2 到 documents**
   ```bash
   cp ~/Downloads/KUAL-v2.7.37/KUAL-KDK-1.0.azw2 /Volumes/Kindle/documents/
   sync
   ```

5. **验证**
   - Home 出现 KUAL 书条目
   - 打开 KUAL → 不再报 permissions expired

### 已知限制

- KUAL-KDK-1.0.azw2 仍是 KDK 签名版。如果打开报 "The device is not registered as a Test Kindle"，需要换 MKK 签名版（需从 MobileRead 或社区下载）。
- 安装 keystore 更新包后，**permissions expired 问题立即解决**。即使 KUAL 签名类型有问题，keystore 修复是独立步骤。
- diskutil eject 可能被 loginwindow 拒绝（"Dissenter" 错误）。安全做法：在 Finder 弹出，或直接拔 USB。

### 容器→Mac 文件传输（scp）

**2026-06-10 验证**：容器的 HTTP server 无法被 Mac 访问（Docker 网络隔离）。改用 `scp` 走 SSH 协议，`host.docker.internal` 可直通 Mac。

详见 `references/scp-container-to-mac.md`

### 建立 SSH 连接的前提

1. **Mac 开启 Remote Login (SSH)**：System Settings → General → Sharing → Remote Login
2. **将 Hermes 的 SSH 公钥添加到 Mac 的 authorized_keys**（用户只需执行一次）：
   ```bash
   mkdir -p ~/.ssh && echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIJHkIWHtNlyqH8NTWt6M+eBdTN/69LYbqXDa12yc9M9h hermes-docker-nvidia" >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys
   ```
3. **从 Docker 容器内 SSH**：
   ```bash
   ssh -o StrictHostKeyChecking=no -i ~/.ssh/id_ed25519 macos@192.168.1.4 "command"
   ```
3. **从 Docker 容器内 SSH**：
   ```bash
   ssh -o StrictHostKeyChecking=no -i ~/.ssh/id_ed25519 macos@192.168.1.4 "command"
   ```

### SSH 后的操作流程

一旦 SSH 到 Mac，可以完全接管：
- `ls /Volumes/Kindle/` — 检查 Kindle 文件系统
- `cp file.bin /Volumes/Kindle/` — 复制文件
- `curl -o ~/Downloads/file.zip URL` — 下载文件
- `unzip` — 解压
- `shasum -a 256 file` — 校验

### 注意事项

- Mac 用户名通常是 `macos`（已验证 2026-06-09）
- Mac 本地 IP 通常是 `192.168.1.4`（可变的，需确认）
- SSH key 路径：`~/.ssh/id_ed25519`
- USB 存储路径：`/Volumes/Kindle/`

## 诊断模式 vs 修复模式（用户期望管理）

用户要求诊断时，优先做到 **证据收集 → 根因定位 → 最小修复方案**，不要先做理论分析再问下一步。

### 用户说的"不要猜测"= 立即切换模式

当用户明确说"不要继续猜测"、"不要给推测"、"进入验证模式"、"不要理论"时：

1. **停止任何新增的理论分析**。已经分析过的结论不重复，不扩展
2. **立即切换为证据收集模式**：
   - 检查 Kindle 文件系统（通过 Mac Terminal 或 SSH）
   - 检查 `disabled-updates/` 中的 `.bin.last-greyed` 文件判断安装状态
   - 检查 `documents/` 中 KUAL 的文件名判断签名类型
   - 检查根目录是否有待安装的 .bin 文件
3. **输出格式**：已确认事实 / 未确认事实 / 下一步唯一动作
4. **不要问"要不要我装这个"**——如果根因已锁定，直接给出修复步骤

### 证据收集优先级（从最易获取的开始）

| 优先级 | 检查项 | 通过什么方式 |
|--------|--------|-------------|
| 1 | Kindle 根目录文件清单 | `ls /Volumes/Kindle/` (Mac Terminal) |
| 2 | documents/ 中 KUAL 文件 | `ls /Volumes/Kindle/documents/` |
| 3 | disabled-updates/ 中的 .bin 文件 | `ls /Volumes/Kindle/disabled-updates/` |
| 4 | developer/ 目录（KUAL 配置） | `ls /Volumes/Kindle/developer/` |
| 5 | /var/local/java/keystore/ 状态 | SSH root@192.168.2.1 |
| 6 | Kindle 系统时间 | Settings → Device Info 或 SSH `date` |

### 输出格式

```markdown
# 已确认事实
- 文件 X 存在/不存在 → 含义
- 错误类型 → 对应根因

# 未确认事实
- 需要验证 Y 才能确定

# 下一步唯一动作
- 唯一需要做的事：Z
- 执行方法：具体命令
```

## KUAL 安装状态诊断（通过 disabled-updates/ 文件判断）

这是通过 USB 存储模式判断当前安装进度的**唯一可靠方法**。不要猜测"可能装过"——直接检查文件。

### 关键陷阱：MKK 2014 已安装的判断方法（2026-06-10 重要更新）

**2026-06-10 实测发现**：MKK 2014 安装完成后，Kindle 的行为是：
- `disabled-updates/` 可能**完全为空**（不是 `.last-greyed`），不一定是 `*.last-greyed`
- 根目录 `*.bin` **完全清空**
- **唯一可靠信号**：Settings → Menu → **Update Your Kindle 灰显**
- 如果 Update 灰显且根目录无 `.bin` = **MKK 2014 确已安装**

**诊断步骤（2026-06-10 验证）**：
```bash
# 1. 先检查 Update 灰显状态（用户确认）
# 2. 再检查根目录
ls -la /Volumes/Kindle/*.bin
# 如果空 + Update 灰显 = MKK 已装
# 3. 如果仍有 Test Kindle 错误 = 缺 keystore，不是缺 MKK
```

**不要仅凭 `disabled-updates/` 为空就判断"未安装"**。Kindle 安装后可能直接删除 .bin 而不保留备份。

### 关键陷阱：MKK .bin 安装后从根目录消失

**MKK 证书 .bin 通过 Settings → Update 成功安装后，Kindle 会自动将 .bin 从根目录移到 `disabled-updates/`**。这意味着：
- `ls /Volumes/Kindle/*.bin` 返回空 **≠** 没有安装过 —— 可能已安装完成
- 配合 **Update Your Kindle 灰显** 即可确认安装成功
- 2026-06-10 实测：SSH 后 `ls /Volumes/Kindle/*.bin` 返回 `no matches found`，但 Update 菜单灰显 = MKK 2014 已安装

**诊断方法**：先检查根目录 `ls *.bin`，如果为空则检查 `disabled-updates/` 和 Update 菜单状态，不要仅凭根目录为空判断"未安装"。

### 文件后缀含义

| 文件位置 | 后缀 | 含义 |
|---------|------|------|
| 根目录 | 无后缀 | 待安装（Settings → Update Your Kindle 可见） |
| `disabled-updates/` | `.bin.last-greyed` | **已安装**（Update 菜单已灰显） |
| `disabled-updates/` | 无后缀 `.bin` | 已下载/安装过的备份（不是 pending） |
| `documents/` | `.azw2` | KUAL for K3（Kindlet 应用） |
| `developer/KUAL/` | 目录 | KUAL Booklet 已安装（K3 不生效） |

### 完整诊断清单

检查以下文件的状态，判断当前修复进度：

```bash
# 1. 根目录 — 有 .bin 文件 = 有更新等待安装
ls -la /Volumes/Kindle/*.bin 2>/dev/null

# 2. disabled-updates/ — .last-greyed = 已安装
ls -la /Volumes/Kindle/disabled-updates/

# 3. documents/ — KUAL 文件名决定签名类型
ls -la /Volumes/Kindle/documents/KUAL*

# 4. 开发者证书相关
ls -la /Volumes/Kindle/developer/
```

### 设备状态快速诊断模板

执行9点调查（2026-06-10 验证方法）：

```bash
# 检查挂载和基本信息
diskutil info /Volumes/Kindle
ls -la /Volumes/Kindle/
ls -la /Volumes/Kindle/documents/
ls -la /Volumes/Kindle/developer/
ls -la /Volumes/Kindle/disabled-updates/ 2>&1
```

输出格式：
1. 型号（从 USB Product ID 或 serial prefix 识别）
2. 固件版本（需在 Kindle 屏幕上查看，USB 不可见）
3. 越狱状态（KUAL/KOReader 目录存在 = 已越狱）
4. KUAL 是否存在
5. MKK 是否存在
6. developer.keystore 是否存在
7. Update Your Kindle 菜单状态（根目录有 .bin = 可点）
8. 根目录文件列表
9. documents 目录文件列表

### 状态评估表
|--------|---------|---------|------|
| KUAL-KDK-1.0.azw2 在 documents/ | ✅ 存在 | ❌ 不存在 | K3 需要 AZW2 作为 KUAL 入口 |
| 根目录无 .bin | ✅ 正常 | ❌ 有 .bin | 有更新等待安装 |
| disabled-updates/ 含 keystore-install.bin.last-greyed | ✅ 装过 keystore | ❌ 无此文件 | **keystore 未更新** |
| disabled-updates/ 含 MKK.bin.last-greyed | ✅ MKK 2014 已装 | ❌ 无 | MKK 2014 未安装 |
| developer/KUAL/ 存在 | ✅ Booklet 已装 | ❌ 不存在 | K3 不需要（booklet 不产生入口） |

### 今日 session 的典型诊断流程（2026-06-09 K3W B008 permissions expired）

**用户现象**：KUAL 打开报 `permissions expired`

**诊断路径**：
1. `ls /Volumes/Kindle/` → 根目录无 .bin，无 pending 更新
2. `ls /Volumes/Kindle/disabled-updates/` → `Update_mkk-20141129-k3w-B008_install.bin` 存在（已下载但非 .last-greyed），`Update_KUALBooklet_v2.7.37_install.bin.last-greyed` 存在（已安装）
3. `ls /Volumes/Kindle/documents/` → `KUAL-KDK-1.0.azw2`（KDK 签名版）
4. 结论：MKK 2014 已下载但未真正安装（不是 .last-greyed），2025 keystore 从未下载，KUAL 是 KDK 版

**发现**：`.last-greyed` 后缀是识别"已安装"的唯一可靠方法。普通 `.bin` 在 `disabled-updates/` 中只表示文件存在，不代表已执行。

## 常见错误处理

### "The permissions to open the requested title have expired"

- **直接根因**：`developer.keystore` 于 **2025-04-17** 过期。影响所有 Kindle 型号。
- **深层根因可能**：MKK 2014 证书链未完整建立（`.bin` 在 `disabled-updates/` 中但**无 `.last-greyed` 后缀**，表示实际未通过 Settings → Update 安装过）。2025 keystore 更新需要在 MKK 2014 证书之上叠加，若底层缺失则补丁无效。
- **来源**：NiLuJe t=225030 post #1295；t=367665（K3 K4 PW5 多用户报告）
- **修复**：两步走——① 确认 MKK 2014 已安装（检查 `.last-greyed`）；② 安装 DevCerts-20250419-KeyStore.zip（attachmentid=215127）中的 keystore installer .bin
- **K3 已验证**：whatever4kindle, t=367665 (2025-04-19)：_"the updated certifications worked with the kindle 3 keyboard"_
- **临时绕过**：改系统时间到 2025-04-01（aha, t=367665 post #13, 需 USBNetwork SSH：date -s "2025-04-01"）
- **注意**：此错误与 Error 003 **根因相同**，区别仅在于固件版本/机型不同显示的本地化字符串不同
- **与 "requires newer firmware" 关系**：K3 FW 3.3 上 KUAL-KDK 可能报此错误，这是 KUAL 的版本检查（要求 FW ≥ 3.4），**与 keystore 过期正交**。需升级到 3.4.3 或使用不检查 FW 的 KUAL 构建。

### 诊断关键：`.last-greyed` 后缀（⚠️ 2026-06-10 修正：disabled-updates/ 可能根本不存在）

`disabled-updates/` 中的 `.bin` 文件必须有 `.last-greyed` 后缀才代表已通过 Settings → Update 成功安装。纯 `.bin` 无后缀 = 文件存在但从未执行。

**2026-06-10 实测修正**：`disabled-updates/` 可能**完全不存在**，这⛑不是异常。K3 越狱后可能：
- `disabled-updates/` 从未创建
- 根目录 .bin 被直接删除（不是移到 disabled-updates）
- Update Your Kindle 菜单直接灰显且无任何历史安装记录

此时**唯一可靠的安装判断方法**：根目录无 `.bin` + Update 灰显 = 已安装。

```bash
# 判断 MKK 2014 是否真正安装
ls -la /Volumes/Kindle/disabled-updates/*mkk*  # 检查后缀

# 判断 keystore 是否已更新
ls -la /Volumes/Kindle/disabled-updates/*keystore*  # 检查后缀
```

### Update Your Kindle 永远不会执行 .bin（2026-06-10 新发现）

**重要诊断发现**：K3 上 `disabled-updates/` 目录可能**从未创建**，即使 Update 按钮看似可点。这有两种含义：

| 现象 | 含义 |
|------|------|
| `disabled-updates/` **不存在** | .bin 从未被执行（签名不匹配、固件拒绝执行、或 Update 按钮本身已损坏） |
| `disabled-updates/` 存在含 `.bin` 无 `.last-greyed` | 文件存在但从未通过 Settings → Update 执行 |
| `disabled-updates/` 含 `.bin.last-greyed` | ✅ 已成功安装 |

**如果 Update 是灰色 + 根目录 .bin 消失 + disabled-updates/ 不存在**：
- Kindle 可能把 .bin 当作无效文件直接删除了（不是移动到 disabled-updates）
- 这表明 OTA 更新机制被越狱时的防 OTA 证书禁用，或者 .bin 签名与 K3 固件版本不兼容

**诊断方法**：改系统时间到 2025-04-01 前，然后尝试打开 KUAL（不走 Update）
- Settings → Device Info → Set Date/Time → 改为 2025年3月
- 回 Home 点 KUAL → 如果正常打开 → 100% 是 keystore 过期问题，只是 installer 未生效
- 如果仍报 Test Kindle → 问题在证书链不完整，不只是 keystore 过期

### 与 K3 3.3 "requires newer firmware" 的关系（2026-06-09 发现）

K3 FW 3.3 上，KUAL-KDK 打开时可能同时报两种错误：
1. "requires newer firmware version to open this title" → KUAL 打包时指定的最低 FW 版本 > 3.3。需升级到 3.4.3 或构造不限制 FW 的 KUAL。
2. "permissions have expired" → keystore 过期。与 FW 版本正交。

这两个错误可共存。解决顺序：先升级 FW（解决版本检查），再修 keystore（解决签名过期）。

- 详见 `references/keystore-expiry-20250417.md`
- 诊断案例：`references/k3-permissions-expired-diagnosis-20260609.md`

### "The device is not registered as a Test Kindle"（2026-06-09 修正）

- **根因**（修正后）：**证书链不完整**。MKK 2014 未通过 Settings → Update 正确安装（`disabled-updates/` 中有 .bin 但无 `.last-greyed` 后缀），或 keystore 已过期。
- **K3 真实情况**：KUAL 本身就是 KDK 签名版。证书链完整时（MKK 2014 + 2025 keystore），KDK 签名版 KUAL 在未注册 Test Kindle 的 K3 上可以正常运行。没有单独的"MKK 签名版 KUAL"。
- **修复**：① 检查 `disabled-updates/` 中是否有 `*mkk-20141129*.last-greyed`（确认 MKK 2014 已安装）；② 若没有，从根目录放 .bin 执行 Update；③ 然后装 2025 keystore 更新
- **附加**：K3 固件 3.3 用户还需要升级到 3.4.3 才能运行最新 KUAL（见上方 K3 FW 章节）
  先报 Test Kindle 错误。需要先解决签名类型问题（换 MKK 版）再处理 keystore 过期。

### "Internal Error: 003"

- **根因**：同 permissions expired — developer.keystore 于 2025-04-17 过期
- **来源**：t=367665 post #3 (sepd, K4)；NiLuJe t=225030 post #1295
- **修复**：同上（装 DevCerts-20250419-KeyStore.zip 中的 keystore installer）
- **注意**：K3 显示 permissions expired，K4+ 显示 Error 003 — 同一问题

### "An error occurred: main class instantiation threw a RuntimeException"

- **根因**（K4NT only）：KUAL.tar.xz 中的 `Update_KUALBooklet_hotfix_v2.7.37_install.bin` 在 K4NT 上不兼容
- **来源**：whatever4kindle, t=367665 (2025-04-19): _just needed to uninstall the hotfix bin file included in the KUAL compressed file that actually does nothing in older kindles but cause trouble_
- **修复**：在 KUAL 书 entry 上长按 → 删除此项目，然后用非 hotfix 版的普通 booklet
- **K4NT 用户 sepd 确认**：_i needed to update the uninstall.bin after the runtime error it is fixed now_

### 其他常见问题

- **MobileRead 附件 404** → 换帖子或搜索 GitHub releases
- **固件版本太新** → 查 MobileRead 最新兼容性列表
- **USB 不识别** → 换线，检查 Mac 是否给了 USB 权限

### USB 检测故障排查（Kindle K3 专用）

**症状**：Kindle 插入 Mac USB 后，`/Volumes/Kindle` 不存在，`diskutil list` 无输出，`dmesg | grep -i usb` 无 kindle 条目。

**最常见原因：充电线≠数据线**
- K3 包装自带的 micro-USB 线通常是**充电专用**（只有 VCC/GND，无 D+/D- 数据线）
- 从 USB 充电器拔下来插到 Mac，Mac 完全看不到设备

**排查步骤**：
1. 换一根确认能传数据的 micro-USB 线（安卓手机数据线一般可以）
2. 点亮 Kindle 屏幕（部分 K3 在屏幕锁定时不开启 USB 存储模式）
3. 插到 Mac 正面 USB 口（别用 Hub）
4. 等待约 10 秒，再检查 `/Volumes/Kindle` 是否出现

**Docker 穿透限制（已确认无效方案）**：即使 Mac 能看到 Kindle，Docker 容器内 `ls /dev/bus/usb/` 仍为空。USB 检测和文件复制**必须在 Mac 终端执行，不走 Docker**。
- ❌ `docker cp` — 需要 docker CLI，Mac 终端不用这个方式
- ❌ SMB 共享 — Mac 防火墙或未开启文件共享导致 445 端口从容器内不可达
- ❌ `host.docker.internal` — 解析到 192.168.65.254，但该 IP 的 USB/SMB 服务不对容器网络开放
- ❌ SSH — 22 端口从容器内不可达（Mac 未开启远程登录，或防火墙阻止）

**最终结论**：Docker 容器和 Mac USB 外设之间存在 Linux VM 隔离层（linuxkit），所有文件传输操作必须由用户在 Mac 终端执行，或通过 HTTP server 中转（Mac 开 python3 -m http.server，容器内 curl 下载）。

### 注意：不再依赖用户逐条粘贴命令

**2026-06-09 更新**：建立 SSH 到 Mac 的通道后，Docker 容器可以无人化执行 Kindle 文件操作。
详见上方「SSH 到 Mac 宿主机操作」章节。

**Docker 穿透限制**：即使 Mac 能看到 Kindle，Docker 容器内 `ls /dev/bus/usb/` 仍为空。USB 检测和文件复制**必须在 Mac 终端执行，不走 Docker**。
- **安装后无法启动 KOReader** → 检查是否正确安装了 KUAL 启动器
- **kindletool: error while loading shared libraries** → libarchive.so.13 缺失，切换到 Mac 本机 `brew install kindletool` 或走 direct USB copy 路径