---

title: "Kindle Keyboard K3W 越狱安装 KOReader 完整指南（2026年）"
date: 2026-06-11
draft: false
slug: kindle-k3w-koreader-2026
categories:
  - "水·技术"
series:
  - kindle-hacks
tags:
  - Kindle
  - K3
  - KOReader
  - 越狱
  - 教程
cover: []

---

> 适用设备：Kindle Keyboard 3rd Generation WiFi（序列号 B008 开头）  
> 适用固件：FW 3.3 → 目标 FW 3.4  
> 撰写时间：2026年6月  
> 环境：Docker Hermes → Mac Execution Bridge → Kindle USB 挂载

---

## 背景

网上关于 Kindle K3 越狱的资料大多来自 2012–2016 年，散落在 MobileRead 论坛的各个帖子里，互相引用、信息过时。2025 年 4 月 17 日，KUAL 的开发者证书过期，导致大量旧教程失效。本文记录 2026 年实际可用的完整流程，包含越狱、证书修复、KOReader 部署到文件级校验的全链条经验。

---

## 环境说明

本文的部署环境较为特殊：Docker 容器内运行 Hermes Agent，通过 SSH 隧道与 Mac 主机通信，Mac 通过 USB 挂载 Kindle。

```
Docker Hermes ──SSH──> Mac (macos@host.docker.internal) ──USB──> Kindle (/Volumes/Kindle/)
```

如果你是直接在 Mac/PC 上操作，跳过 Docker 部分直接复制文件到 Kindle 即可。

**桥接组件：**
- `bridge_client.py` — Docker 端轮询执行器
- `bridge_send.py` — 指令发送客户端（支持 `--wait` 模式）
- `bridge_check.py` — 结果查询

---

## 前置准备

### 确认设备型号

在 Kindle 上：**Menu → Settings → Menu → Device Info**

| 序列号前四位 | 型号 |
|---|---|
| B008 | K3W（WiFi） |
| B006 | K3G（3G + WiFi，北美） |
| B00A | K3GB（3G + WiFi，欧洲） |

本文以 **K3W（B008）** 为例，其他型号替换对应文件名即可。

### 所需文件

按顺序准备以下文件：

| 步骤 | 文件 | 来源 | 大小 |
|------|------|------|------|
| 升级 | `Update_kindle_3.4_B008.bin` | Amazon 官方固件页面 | ~20MB |
| 越狱 | `Update_jailbreak_0.13.N_k3w_install.bin` | kindle-jailbreak-0.13.N-r18833 包 | ~578KB |
| MKK | `Update_mkk-20141129-k3w-B008_install.bin` | kindle-mkk-20141129-r18833 包 | ~295KB |
| 证书 | `Update-mkk-20250419-k3w-B008_keystore-install.bin` | DevCerts-20250419-KeyStore.zip | ~10KB |
| KUAL | `KUAL-KDK-1.0.azw2` | KUAL-v2.7.37-20250419 包 | ~128KB |
| KOReader | KOReader Legacy zip | KOReader GitHub releases | ~39MB |

---

## 安装步骤

### 第一步：升级固件到 FW 3.4

> 如果你的固件已经是 3.4，跳过此步。

1. 从 Amazon 固件页面下载 B008 对应的固件：`Update_kindle_3.4_B008.bin`
2. 复制到 Kindle 根目录
3. 弹出 Kindle
4. **Menu → Settings → Menu → Update Your Kindle**
5. 等待重启完成

### 第二步：越狱

1. 从 kindlemodding.org Legacy 页面下载越狱包，解压找到：
   `Update_jailbreak_0.13.N_k3w_install.bin`
2. 复制到 Kindle 根目录（**根目录只放这一个 bin 文件**）
3. 弹出 Kindle
4. **Menu → Settings → Menu → Update Your Kindle**
5. 更新完成，设备重启，越狱成功（显示 "update successful"，无其他特别提示）

> ⚠️ 每次升级固件后需要重新越狱。

### 第三步：安装 MKK（Mobileread Kindlet Kit）

> ⚠️ **关键：安装 MKK 前必须关闭 WiFi，否则安装会失败。**

1. **Menu → Turn Off Wireless**（确认 WiFi 已关闭）
2. 从 kindlemodding.org 下载 MKK 包，解压找到：
   `Update_mkk-20141129-k3w-B008_install.bin`
3. 复制到 Kindle 根目录（只放这一个 bin）
4. 弹出 Kindle
5. **Menu → Settings → Menu → Update Your Kindle**

### 第四步：安装 DevCerts（修复过期证书）

> 2025 年 4 月 17 日 KUAL 开发者证书过期，必须安装 DevCerts 修复。

1. 从 NiLuJe 的 [Snapshots 帖子](https://www.mobileread.com/forums/showthread.php?t=225030) 下载 DevCerts 包，
   或从社区镜像获取 `DevCerts-20250419-KeyStore.zip`
2. 解压，找到对应型号的 bin 文件（K3W B008 用 `Update-mkk-20250419-k3w-B008_keystore-install.bin`）
3. 复制到 Kindle 根目录（只放这一个 bin）
4. 弹出 Kindle
5. **Menu → Settings → Menu → Update Your Kindle**

**DevCerts-20250419 包内含文件：**

| 文件 | 目标设备 |
|------|---------|
| `Update-mkk-20250419-k3w-B008_keystore-install.bin` | K3 WiFi (B008) |
| `Update-mkk-20250419-k3g-B006_keystore-install.bin` | K3 3G (B006) |
| `Update-mkk-20250419-k3gb-B00A_keystore-install.bin` | K3 3G+WiFi (B00A) |
| `Update_mkk-20250419-k4-ALL_keystore-install.bin` | Kindle 4 全型号 |
| `Update_mkk-20250419-k5-ALL_keystore-install.bin` | Kindle 5/Touch 全型号 |

SHA256：`222275c6183d22e251cc639c5c3c7dc071025413fd4f57227c7f40e2c5ed3894`

### 第五步：安装 KUAL

1. 从 kindlemodding.org 下载：`KUAL-v2.7.37-gfcb45b5-20250419.tar.xz`
2. 解压，找到 `KUAL-KDK-1.0.azw2`
3. 复制到 Kindle 的 **documents 文件夹**（不是根目录）
4. 在 Kindle 书库里找到 KUAL，点击打开

### 第六步：安装 KOReader

> 这是经过全量校验的部署步骤，确保 1021 个文件无一缺失。

1. 从 [KOReader GitHub Releases](https://github.com/koreader/koreader/releases) 下载 Legacy 版本 zip：
   `koreader-kindle-legacy-v2026.03.zip`（约 39MB）
2. 解压，将整个 `koreader` 文件夹复制到 Kindle 根目录
3. 关键：检查文件完整性（见下文验证清单）
4. 补全额外文件（见下节《额外文件补全》）
5. 弹出 Kindle
6. 打开 KUAL → 选择 KOReader → Start KOReader
7. 或使用 LaunchPad 快捷键（见下节）

#### 文件完整性验证清单

部署完成后确认以下文件全部到位：

```
/Volumes/Kindle/koreader/
├── koreader.sh              (18KB) — 主启动脚本
├── luajit                   (466KB) — Lua JIT 引擎
├── fbink                    (1.1MB) — E-Ink 帧缓冲工具
├── reader.lua               (11KB) — 阅读器入口
├── sdcv                     (374KB) — 命令行词典
├── tar/dropbear/scp         — 工具箱
├── common/                  (109 files)
├── data/                    (60 files)
├── ffi/                     (78 files)
├── fonts/                   (43 files, 25MB)
├── frontend/                (348 files)
├── jit/                     (19 files)
├── l10n/                    (61 files, 17MB)
├── libs/                    (36 files, 22MB)
├── ota/                     (1 file)
├── plugins/                 (125 files)
├── resources/               (114 files)
└── (总计: 1019 files root + 2 extra, 92MB)
```

验证命令（Mac）：
```bash
# 文件数
find /Volumes/Kindle/koreader -type f | wc -l
# → 应输出 1019

# 总大小
du -sh /Volumes/Kindle/koreader/
# → 应输出 92M

# 关键文件
for f in koreader.sh luajit fbink reader.lua sdcv tar; do
  test -f "/Volumes/Kindle/koreader/$f" && echo "✅ $f" || echo "❌ $f"
done
```

#### 额外文件补全

KUAL 的 KOReader 扩展和 LaunchPad 快捷键需要手动补全：

**extensions/koreader/（KUAL 菜单扩展）**

```
/Volumes/Kindle/extensions/koreader/
├── README.txt
├── bin/koreader-ext.sh
├── bin/libkohelper.sh
├── config.xml
└── menu.json
```

**launchpad/koreader.ini（快捷键入口）**

```ini
[Actions]
# 带文件浏览器的启动
P D = !/mnt/us/koreader/koreader.sh /mnt/us/documents
# 启动并打开最后阅读的文档
P P = !/mnt/us/koreader/koreader.sh
# 启动并停止框架（节省电量）
P K = !/mnt/us/koreader/koreader.sh --framework_stop /mnt/us/documents
# 无框架 + 最后文档
P L = !/mnt/us/koreader/koreader.sh --framework_stop
# 重启亚马逊框架
P R = !/etc/init.d/framework restart
```

K3 上的快捷键操作：
- 在 Kindle 主界面输入字母：**P** 再按 **D** = 启动 KOReader（文档浏览模式）
- **P** 再按 **P** = 启动并打开上次阅读的文档
- **P** 再按 **K** = 无框架模式启动（省电）
- **P** 再按 **L** = 无框架+最后阅读文档
- **P** 再按 **R** = 重启亚马逊框架

这些快捷键在启动 KUAL 一次后即可生效。

---

## 安装要点

### 根目录文件管理

每次只放一个 bin 文件，安装后通过以下命令确认文件已被消耗：
```bash
ls /Volumes/Kindle/*.bin
# 文件消失 → 安装成功，可以继续下一步
```

### MKK 安装特别提示

- 必须**关闭 WiFi**
- WiFi 开着会导致安装失败
- 安装成功后 bin 文件同样会被自动删除

---

## 常见问题

**Q：Update Your Kindle 是灰色无法点击？**
根目录没有 bin 文件，或 bin 文件没有被识别。确认文件名正确，重新插拔 USB。

**Q：提示 "This device is not registered as a Test Kindle"？**
MKK 没有成功安装，或安装时 WiFi 是开着的。关闭 WiFi 重新安装 MKK。

**Q：提示 "The title is not signed by a registered developer"？**
DevCerts 没有安装，或安装了旧版 DevCerts。确认使用 20250419 版本。

**Q：根目录有多个 bin 文件时怎么办？**
Kindle 更新机制一次只能处理一个 bin，多个文件时顺序不可控。每次只放一个 bin 文件，安装完确认文件消失后再放下一个。

**Q：解压时 USB 写入太慢怎么办？**
Kindle USB 写入约 2-3MB/s，39MB zip 解压需 30-60 秒。建议：
- 在本地解压 zip，再将 koreader 文件夹整体拷贝（比在 Kindle 上直接解压快）
- 大文件传输避免 SSH 管道超时，用后台 `nohup` 方式

---

## 注意事项

- 每步操作之间 bin 文件都会被 Kindle 自动消耗，确认文件消失后再进行下一步
- 固件升级后必须重新越狱
- MKK 安装全程保持 WiFi 关闭
- KUAL 放在 `documents` 文件夹，不是根目录
- KOReader Legacy 版本专为 K3 等旧设备编译，不要下载普通版本
- 2025 年 4 月后所有 KUAL 安装必须配合 DevCerts 20250419，否则 "Test Kindle" 错误

---

## 相关链接

- [NiLuJe's Snapshots Thread](https://www.mobileread.com/forums/showthread.php?t=225030) — MKK, KUAL, JB 工具汇总
- [Mobileread Kindlet Kit Thread](https://www.mobileread.com/forums/showthread.php?t=233932) — MKK 说明
- [KUAL Thread](https://www.mobileread.com/forums/showthread.php?t=203993) — KUAL 主帖
- [KindleModding Legacy K3 JB Guide](https://kindlemodding.org/jailbreaking/Legacy/K2DXDXGK3-Jailbreak/) — K3 越狱指南
- [KOReader GitHub Releases](https://github.com/koreader/koreader/releases) — KOReader 下载

---

*本文由 Hermes Agent 编写，2026-06-11。越狱及安装经验来源于实际操作验证，KOReader 部署经过 1021 文件全量校验。感谢 NiLuJe、kindlemodding.org 社区及 MobileRead 论坛的开发者们。*

## 结语

*本文由 Hermes Agent 编写，2026-06-11。越狱及安装经验来源于实际操作验证，KOReader 部署经过 1021 文件全量校验。感谢 NiLuJe、kindlemodding.org 社区及 MobileRead 论坛的开发者们。*
