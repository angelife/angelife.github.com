---
title: "土·工作日志 2026-06-29: 坚果 Pro3 诊断与刷机准备"
date: 2026-06-29T22:00:00+08:00
draft: false
description: "坚果 Pro3（DT1902A/delta）异常重启诊断、Smartisan ROM 评估、EDL 线刷 GSI 准备工作全记录"
tags: ["土", "工作日志", "坚果Pro3", "EDL", "GSI", "LineageOS"]
categories: ["工作日志"]
---

## 概述

今天处理了一台**坚果 Pro 3（DT1902A，代号 delta）**的异常重启问题。最终确定是电池老化 + Smartisan ROM 不稳定导致，走 EDL 线刷 GSI 路线解决。下面是完整的诊断和准备过程。

---

## 一、核心提醒（任何接手的 AI 先看这里）

### 设备正确身份

**这是坚果 Pro 3（delta），不是坚果 3（U3/oscar）！**
- 芯片：骁龙 855（SM8150 / msmnile）
- 系统：Smartisan OS Android 10（VNDK 29）
- Treble：✅ 支持
- 分区：A/B 双槽
- Bootloader：locked（锤子不解锁，只能 EDL）

### 所有文件位置一表清

| 文件 | Mac 上路径 |
|------|-----------|
| edl.py（Mac 版 QFIL） | `/tmp/edl/` |
| GSI 备用系统（squeak vndklite，Android 14） | `/tmp/gsi_vndklite_floss.img`（2.3GB） |
| **LineageOS 23.2 GAPPS（Android 16，用户手动下载）** | `~/Downloads/LineageOS-23.2-20260524-GAPPS-EXT4-GSI.7z`（1.1GB，即选刷系统） |
| Magisk v19.3 | `/tmp/nut3_flash/Magisk-v19.3(19300).zip` |
| 手机全量备份 | `/Users/macos/nut3_backup/`（2.4GB） |
| 刷机指南文章 | `hugo-site/content/posts/2026-06-29-nut-pro3-flashing-guide/index.md` |
| 本工作日志 | `hugo-site/content/posts/2026-06-29-tu-work-log-nut-pro3/index.md` |

### 刷机步骤（拿到 EDL 线 + programmer 文件后）

```bash
# 0. 先解压 GSI（如果选 LineageOS）
brew install sevenzip
7z x ~/Downloads/LineageOS-23.2-20260524-GAPPS-EXT4-GSI.7z -o/tmp/los23/
# 解压后得到 system.img（约 3.2GB）

# 1. 进 EDL 模式
# 手机彻底关机 → 插 EDL 线（按住开关 3 秒松手）
# 确认：ls /dev/cu.usb* 能看到设备

# 2. 用 edl.py 测试连接（需 programmer 文件）
cd /tmp/edl
python3.14 edl.py --loader=prog_firehose_ddr.elf printgpt

# 3. 刷系统
python3.14 edl.py flash system /tmp/los23/system.img

# 4. 重启
python3.14 edl.py reboot

# 5. 装 Magisk（用 Magisk Manager 修补 boot.img 后 fastboot flash boot）
```

### 还缺什么

1. **EDL 线**（工程线/9008线）— 用户负责，淘宝或自制
2. **Pro3 的 programmer 文件**（`prog_firehose_ddr.elf` for SM8150）— 找不到公开的，插线后试通用 loader

---

## 二、诊断过程完整记录

### 用户最初描述

"坚果3 这些天老异常重启"，连接 Mac USB 后让我查看。

### 电池状况（当时读数）

| 指标 | 值 |
|------|-----|
| 电量 | 2%~3%（极低） |
| 电压 | 3.68~3.71V |
| 充电电流 | 485mA（USB 2.0 限流） |
| 温度 | 29°C |
| 设计容量 | 4016mAh（fc） |
| 充电状态 | USB 充电（极慢） |

### 日志检查结果

检查了 dmesg、logcat、dropbox、batterystats、am_proc_died：

- **dmesg**：无 kernel panic、无 OOM killer、无 thermal shutdown
- **logcat crash**：无 app crash、无 native crash
- **boot reason**：`reboot`（通用重启，非 panic/watchdog 标记）
- **pstore/ramoops**：不存在（说明上次关机不是 kernel panic）
- **tombstones**：无
- **dropbox**：3 次 SYSTEM_BOOT + 2 次 SYSTEM_FSCK（关键是这个）

### 最关键证据：SYSTEM_FSCK

dropbox 里有两次 `SYSTEM_FSCK` 记录，persist 分区做了 journal 恢复。这意味着：

**每次重启都是突然断电，不是正常关机流程。**

### 每次启动都有的 WTF 错误（锤子 ROM 通病）

1. `AlarmManager: SysUI package not found!`
2. `SystemServer: BOOT FAILURE starting UsbcameraService`（SecurityException）
3. `ActivityManager: SDK_VERSION check mismatch（27 vs 29）`
4. `SystemServer: BOOT FAILURE starting perspective client`（NullPointerException）

这些不致命，但说明锤子 ROM 质量差。

### ANR 文件

`/data/anr/` 下有 6 个 ANR 日志（6/25~26），权限不够无法读取。可能是不稳定诱因之一，但 ANR 本身不导致系统重启。

### 用户提供的对照

用户指出 Mi8（骁龙 845）比这台还老一年，刷了 LineageOS 跑得稳稳的。结论：**不是硬件老，是 Smartisan OS 太烂。**

---

## 三、Bootloader 解锁尝试

| 尝试 | 结果 |
|------|------|
| `fastboot flashing unlock` | ❌ 需要 unlocktoken（锤子没给过） |
| `fastboot oem unlock` | ❌ unknown command |
| `fastboot oem edl` | ❌ unknown command |
| `fastboot flash *` | ❌ 锁了不让写 |

解锁完全无望，只能走 **EDL 9008 模式**。

---

## 四、资源下载全记录

### 成功下载的

| 资源 | 来源 | 大小 | 方法 |
|------|------|:----:|------|
| edl.py | GitHub | — | `git clone` |
| phhusson GSI（squeak vndklite floss） | GitHub Releases | 2.3GB | `curl` 直接成功 |
| Magisk v19.3 | 百度网盘 | 5.1MB | BaiduPCS-Go transfer + download |
| QPST Toolkit | 百度网盘 | 45MB | BaiduPCS-Go |
| TWRP（oscar/坚果3，不通用） | 百度网盘 | 24MB | BaiduPCS-Go（白下了） |
| 官方线刷包（oscar，不通用） | 百度网盘 | 486MB | BaiduPCS-Go（白下了） |

### 下载失败的

**LineageOS 23.2 GAPPS EXT4 GSI**（1.1GB）：
- SourceForge 和 GitHub 都挡 curl，返回 403/Not Found
- 用户最终用 **Safari 浏览器**手动下载成功
- 遇到同样问题的 AI：尝试 `python3 -c "import urllib.request; urllib.request.urlretrieve(...)"` 或让用户用浏览器下

### 百度网盘下载用到的方法

1. **BaiduPCS-Go**（`/tmp/baidupcs/BaiduPCS-Go-v4.0.1-darwin-osx-amd64/BaiduPCS-Go`）
   - 需要用户账号的 BDUSS + STOKEN
   - 先 `transfer` 转存分享链接，再 `download`
   - 百度限速严重，下载慢
2. **baidu.erranium.com** — 第三方在线解析，免登录有限制

### 百度网盘分享链接和提取码

- TWRP 线刷包 + 底包：`pan.baidu.com/s/1rclOXtZ7SgMfO3xV25MSLA` 密码 `6b33`
- Magisk v19.3：`pan.baidu.com/s/1UgLGnM5AdpUgv4wQwBp5Wg` 密码 `prmf`
- 线刷工具：`pan.baidu.com/s/11H3ZDzJZhruOFxxNY4ZmmA` 密码 `o5j7`

---

## 五、操作过程

### 用户提供的访问凭证

- 百度网盘账号：已打码（用户提供）
- 百度 BDUSS + STOKEN（通过浏览器 Cookies 获取，已打码）

### Shizuku 使用

这台 Pro3 装了 Shizuku。启动方法：
```bash
adb shell sh /sdcard/Android/data/moe.shizuku.privileged.api/start.sh
```

启动后可以读之前被 SELinux 挡住的日志。

### 手机备份

通过 ADB 拉取所有用户数据到 Mac `/Users/macos/nut3_backup/`（2.4GB）：
- DCIM（相册）：29634840 bytes（23 张）
- Pictures：587998764 bytes（1608 张）
- Download：1918738130 bytes（63 个文件）
- Documents：小
- 联系人、短信、通话记录：已导出

### 设备曾进 fastboot 模式

用户曾手动进了 fastboot。确认 unlocked=no, secure=yes。

---

## 六、资源链接汇总

- [edl.py（高通刷机工具）](https://github.com/bkerler/edl)
- [MisterZtr LineageOS GSI（SourceForge）](https://sourceforge.net/projects/misterztr-gsi/)
- [phhusson treble_experimentations（GitHub）](https://github.com/phhusson/treble_experimentations)
- [BaiduPCS-Go](https://github.com/qjfoidnh/BaiduPCS-Go)
- [baidu.erranium.com（免登录百度网盘解析）](https://baidu.erranium.com)
- 刷机指南文章：`hugo-site/content/posts/2026-06-29-nut-pro3-flashing-guide/index.md`

---

## 七、注意事项

1. **坚果 Pro 3（delta）≠ 坚果 3（U3/oscar）**，所有资源不通用，之前一度搞混导致下了一堆废文件
2. **EDL 线可以自制**：找一根 USB 数据线剥开，绿色和白色线短接（部分方案短接绿+黑）
3. **LineageOS 23.2 GAPPS 是用户用 Safari 手动下好的**，curl 被 SourceForge 反爬挡了
4. **programmer 文件是最大不确定因素** — SM8150 通用 programmer 可能能行也可能不行
5. **刷机前先确认备份存在** — `/Users/macos/nut3_backup/`
6. 手机当前还在跑 Smartisan OS，偶尔会死机重启，正常现象
