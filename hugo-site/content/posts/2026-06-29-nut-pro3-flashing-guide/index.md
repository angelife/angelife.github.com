---
title: "Pro3刷机"
date: 2026-06-29T20:30:00+08:00
draft: false
description: "从诊断异常重启到准备刷机——Smartisan Nut Pro 3（delta）EDL 线刷 GSI 路线全记录"
tags: ["坚果Pro3", "Smartisan", "EDL", "GSI", "LineageOS", "9008", "刷机"]
categories: ["刷机"]
---

## 前言

本文记录了给一台 **坚果 Pro 3（DT1902A，代号 delta）** 从 Smartisan OS Android 10 刷成 LineageOS GSI 的完整准备过程。目的是方便日后回顾，拿到 EDL 线后可以直接继续。

**注意：这不是给坚果 3（U3/oscar）的教程，两者芯片不同，资源不通。**

---

## 一、设备信息

| 项目 | 值 |
|------|-----|
| 型号 | DT1902A |
| 设备代号 | delta |
| 芯片 | 高通骁龙 855（SM8150 / msmnile） |
| 当前系统 | Smartisan OS Android 10（QKQ1.191222.002） |
| 内核 | Linux 4.14.117-perf+ |
| 存储 | 224G UFS（已用 42G） |
| RAM | 7.3GB |
| Treble | ✅ 支持（ro.treble.enabled=true） |
| 分区 | A/B 双槽 |
| VNDK | 29（Android 10 vendor） |
| 屏幕 | 1080×2340，400dpi |
| 连接 | USB 3.0 Type-C |

---

## 二、原始问题诊断

### 症状

- 日常异常重启（有时一天多次）
- 系统卡死后自动重启
- 电池掉电极快

### 排查过程

| 检查项 | 结果 |
|--------|------|
| dmesg（内核日志） | 无 kernel panic、无 OOM、无 thermal 关机痕迹 |
| logcat crash/events | IMS FATAL 错误（VoLTE 栈启动失败，但不导致系统级重启） |
| 进程/内存 | 699 个进程，3.3G/7.3G 已用，无内存压力 |
| 温度 | 29°C，正常 |
| boot reason | `reboot`（通用重启，非 watchdog/panic） |
| pstore/ramoops（内核崩溃转储） | 不存在，说明关机不是 kernel panic |
| tombstone（native crash） | 目录存在但权限不够 |
| dropbox（系统事件箱） | 3 次 SYSTEM_BOOT，2 次 SYSTEM_FSCK（非正常断电证据） |

### 关键发现

**系统每次启动都报 4 个 WTF 错误**（system_server_wtf），但都是锤子 ROM 的通病，不会导致重启：

1. `AlarmManager: SysUI package not found!`
2. `SystemServer: BOOT FAILURE starting UsbcameraService`（SecurityException）
3. `ActivityManager: SDK_VERSION check mismatch（27 vs 29）`
4. `SystemServer: BOOT FAILURE starting perspective client`（NullPointerException）

**电池严重亏电**（2%~3%），插 Mac USB 仅 485mA 慢充。

**SYSTEM_FSCK 确认每次都是非正常断电**——persist 分区 journal 恢复，说明系统每次都是突然掉电关机。

### 结论

**不是硬件故障，是电池老化 + Smartisan ROM 太烂。** Mi8 比它还老一年（845 vs 855），刷了 LineageOS 跑得稳稳的。这台机器刷掉 Smartisan OS 大概率能救活。

---

## 三、Bootloader 情况

```
fastboot getvar unlocked → no
fastboot getvar secure → yes
```

已确认的状态：

| 命令 | 结果 |
|------|------|
| `fastboot flashing unlock` | ❌ 需要 unlocktoken（锤子从未给过） |
| `fastboot oem unlock` | ❌ unknown command |
| `fastboot oem edl` | ❌ unknown command |
| `fastboot flash *` | ❌ locked 不让写 |

**官方不解锁，只能走 EDL 9008 模式。**

---

## 四、刷机路线

### 为什么选 EDL？

```
正常刷机：解锁 bootloader → fastboot flash → 校验签名
EDL 刷机：绕过锁直接从芯片底层写存储
```

高通所有芯片出厂都内置 **Sahara/Firehose 协议**，在 bootROM 里，OEM 关不掉。通过物理 EDL 线（短接 D+/D- 信号）触发进入 9008 模式，PC 端发送 programmer 文件后就能对手机做任何操作。

### 为什么不能刷 TWRP？

坚果 Pro 3（delta）的第三方开发基本为零：
- ❌ 没有 TWRP
- ❌ 没有第三方 ROM（LineageOS 官方不支持）
- ❌ 找不到公开的 programmer 文件

**走 Project Treble GSI 路线**：因为支持 Treble，可以直接刷通用系统镜像到 system 分区。

---

## 五、材料清单

### ✅ 已备好

| 材料 | 大小 | 说明 |
|------|:----:|------|
| edl.py（Mac 版 EDL 刷机工具） | — | 替代 Windows 的 QFIL，在 `/tmp/edl/` |
| phhusson squeak vndklite floss GSI | 2.3GB | AOSP Android 14，vndklite 兼容 VNDK 29 |
| **LineageOS 23.2 GAPPS EXT4 GSI** | **1.1GB** | **Android 16，带谷歌服务**（用户从 SourceForge 手动下载） |
| Magisk v19.3 | 5.1MB | 刷完系统后装 root（ZIP 包） |
| QPST Toolkit | 45MB | Windows 版线刷工具（备用，Mac 上用不到） |
| 官方线刷包（坚果3 U3 的，不通用） | 486MB | 存着参考分区布局 |

### ❌ 还需要

| 材料 | 说明 |
|------|------|
| **EDL 线（工程线/9008 线）** | 淘宝十几块，或自制（短接 USB 数据线绿+白线） |
| **Pro3 的 programmer 文件** | 插上 EDL 线后尝试通用 SM8150 programmer |

### 📦 下载资源

- **TWRP 线刷包 + 底包（U3/oscar，不通用）**：`https://pan.baidu.com/s/1rclOXtZ7SgMfO3xV25MSLA` 密码 `6b33`
- **Magisk v19.3**：`https://pan.baidu.com/s/1UgLGnM5AdpUgv4wQwBp5Wg` 密码 `prmf`
- **线刷工具**：`https://pan.baidu.com/s/11H3ZDzJZhruOFxxNY4ZmmA` 密码 `o5j7`
- **LineageOS 23.2 GAPPS EXT4 GSI**：`https://sourceforge.net/projects/misterztr-gsi/files/LineageOS/Android%2016/LineageOS-23.2-20260524-GAPPS-EXT4-GSI.7z/download`

### 💾 手机数据备份

已备份至 Mac `/Users/macos/nut3_backup/`（2.4GB）：

| 内容 | 大小 |
|------|:----:|
| DCIM（相册） | 29MB |
| Pictures（图片） | 588MB（1608 张） |
| Download（下载文件） | 1.9GB |
| Documents（文档） | 小 |
| 联系人 | 已导出 |
| 短信 | 已导出 |
| 通话记录 | 已导出 |

---

## 六、刷机流程（EDL 线到手后操作）

### 前提条件

- Mac 已安装 `edl.py`（`/tmp/edl/`）
- Python 3.14（或 3.11）已安装依赖
- 手机数据已备份
- 准备好 GSI 镜像（`.img` 文件——需要先解压 7z）

### Step 1：解压 LineageOS GSI

```bash
# 安装 7zip 解压工具
brew install sevenzip

# 解压获取 .img 文件
7z x ~/Downloads/LineageOS-23.2-20260524-GAPPS-EXT4-GSI.7z -o/tmp/los23/
```

得到 `system.img`（约 3.2GB）。

### Step 2：让手机进入 EDL 模式（9008）

1. 手机彻底关机（等屏幕全黑）
2. EDL 线插电脑 USB 口
3. 按住 EDL 线上的开关，插入手机
4. 等待约 3 秒后松手
5. 终端确认：`ls /dev/cu.usb*` 或 `python3 edl.py` 检测到设备

### Step 3：用 edl.py 刷分区

```bash
cd /tmp/edl

# 连接设备并刷入 GSI（以 LineageOS 为例）
python3 edl.py --loader=prog_firehose_ddr.elf \
  --memory=ufs \
  flash system /tmp/los23/system.img

# 刷 boot 分区（可能需要原厂 boot 或 Magisk patched boot）
# python3 edl.py flash boot /path/to/boot.img
```

> **注意**：需要正确的 `prog_firehose_ddr.elf`（SM8150 通用 programmer）。如果 edl.py 无法识别，可能要找 Pro3 专用 programmer。

### Step 4：首次启动

```bash
# 重启到系统
python3 edl.py reboot
```

### Step 5：刷 Magisk（可选）

将 Magisk ZIP 放到手机存储，在系统中安装 Magisk Manager → 选择修补 boot。或者用 TWRP（如果能进的话）。

---

## 七、替代方案

如果 EDL 刷 GSI 失败，还有备用方案：

| 方案 | 说明 |
|------|------|
| phhusson squeak GSI（vndklite floss） | 已下载 2.3GB，Android 14，兼容性更好 |
| MisterZtr LineageOS 22.2 GSI | Android 15，VNDK 兼容性可能更好 |
| Andy Yan's LineageOS GSI | 经典 GSI 项目 |
| phhusson treble_experimentations | 最活跃的 GSI 项目，定期更新 |

---

## 八、教训总结

1. **坚果 Pro 3 ≠ 坚果 3**——前者是骁龙 855（delta），后者是骁龙 625（oscar），资源完全不互通
2. **Smartisan 第三方开发几乎为零**——不像小米有庞大的社区支持
3. **EDL 线是锤子机器的唯一出路**——没有官方解锁，只能走硬件后门
4. **Programmer 文件是关键瓶颈**——即使有了 EDL 线，没有对应的 firehose loader 也不行
5. **GSI + Treble 是没第三方 ROM 时的救命方案**——VNDK 版本兼容性要注意

---

## 九、参考链接

- [edl.py（Mac 高通刷机工具）](https://github.com/bkerler/edl)
- [MisterZtr LineageOS GSI](https://sourceforge.net/projects/misterztr-gsi/)
- [phhusson treble_experimentations](https://github.com/phhusson/treble_experimentations)
- [百度网盘下载工具 BaiduPCS-Go](https://github.com/qjfoidnh/BaiduPCS-Go)
- [免登录百度网盘在线解析站](https://baidu.erranium.com)
- [坚果3刷机指南（参考，设备不同注意区分）](https://www.mintimate.cn/2019/11/30/%E5%9D%9A%E6%9E%9C3%E5%88%B7%E9%AD%94%E8%B6%A3/)
