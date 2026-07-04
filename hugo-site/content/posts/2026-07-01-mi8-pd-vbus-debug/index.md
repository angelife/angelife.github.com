---
title: "USB调试"
date: 2026-07-01
draft: false
categories: ["土·正见"]
tags: ["小米8", "USB网卡", "PD", "VBUS", "PMI8998", "kernel", "排障"]
---

## 背景

Mi8（dipper, SD845）插 AX88179 千兆 USB 网卡，重启前一切正常：Type-C 检测到 Sink → VBUS 输出 → DWC3 切 host → XHCI 启动 → USB 设备枚举 → `ax88179_178a` 驱动绑定。重启后再插，Type-C 检测通过、DWC3 退出低功耗、XHCI 启动，但 **VBUS 始终不输出**，设备无任何枚举迹象，15 秒后 DWC3 回低功耗模式。

这篇文章记录从「现象 → 数据收集 → 排除红鲱鱼 → 定位真正根因」的完整过程。

<!--more-->

## 第一轮分析：PD 协商失败？

重启后的 dmesg 显示清晰的失败链：

```
[814.861] usbpd usbpd0: Type-C Sink connected        ← 物理连接 OK
[815.920] msm-dwc3: DWC3 exited from low power mode  ← PMIC 准备切 host
[815.925] xhci-hcd: xHCI Host Controller             ← XHCI 启动
[816.022] usbpd usbpd0: Error sending Source_Capabilities: -14 ← PD 协商失败
...重复 8 次...
[831.439] msm-dwc3: DWC3 in low power mode            ← 放弃
```

同时检查 PMIC 的 PDO（Power Data Object，PMIC 注册的供电能力），发现 `pdo1` 到 `pdo7` 全部为 `00000000`，`smb2-vbus` 和 `ext_5v_boost` 两个 regulator 均为 disabled。

初步结论很自然：「PDO 全零 → PD 引擎无能力可发 → Source_Capabilities 失败 → VBUS 不使能 → 设备不枚举」。

但这是错误的。

## 转机：发现红鲱鱼

重启前有一次成功捕获的 dmesg（`dmesg_cap3.txt`），我把它拉回来重新审查：

```
[2197.461] Type-C Sink connected
[2198.516] DWC3 exited from low power mode
[2198.518] XHCI 启动
[2198.621] usbpd usbpd0: Error sending Source_Capabilities: -14 ← 也在报！
[2198.760] usb 1-1: new high-speed USB device number 2          ← 但设备照样枚举
[2198.906] New USB device found: 0b95:1790
[2199.315] ax88179_178a eth0: registered
[2199.656] ax88179_178a eth0: Failed to read reg 0x0040: -32
[2199.678] ax88179_178a eth1: registered
[2200.013] ax88179_178a eth1: Failed to read reg index 0x0040: -32
...Source_Capabilities:-14 一直报到捕获结束...
```

**关键发现：`Source_Capabilities: -14` 在重启前就存在且从未阻止设备枚举。** PD 协商失败时，Type-C 默认 VBUS（靠 CC 线上的 Rd/Rp 电阻配置、不依赖 PD）仍应提供 5V/500mA——USB 2.0 High-Speed 设备靠这个就能枚举。

重启前，默认 VBUS 正常输出 → 设备枚举成功 → 驱动绑定（`-32` 错误是另一回事，不影响链路层）。
重启后，默认 VBUS **不输出** → 设备死寂。

**结论：`-14` 是恒存噪音，不是根因。** 真正的差异在于 PMIC 在 Type-C Sink 连接后是否拉起 VBUS，与 PD 协商无关。

## 第二层：PMIC 状态对比

### 重启前（成功时 PMIC 状态）

dmesg 中能看到 PMI8998 smb2 充电器在插入前后的完整投票状态：

```
[2193.518] PMI: Weak charger detected: voting 500mA ICL
[2193.520] PMI: Reverse boost detected: voting 0mA to suspend input
[2193.534] USB Type-C disconnect
[2193.536] DWC3 in low power mode
[2197.461] OTG_VOTER: val: 0
[2197.461] Type-C Sink connected
[2197.461] USB_ICL: 0 (voted by OTG_VOTER)
[2198.516] DWC3 exit LP
[2198.518] XHCI start
[2198.760] usb 1-1: new device ← VBUS 可用
```

PMIC 从「Mac USB 断开」到「AX88179 插入」的状态机转换完整，VBUS 在默认 current 模式下被正确启用。

### 重启后（失败时 PMIC 状态）

```
[810.054] USB Type-C disconnect
[810.082] DWC3 in low power mode
[814.861] Type-C Sink connected
[815.920] DWC3 exit LP
[815.925] XHCI start
[816-831] Source_Capabilities:-14 ×8
[831.439] DWC3 in low power mode
```

缺少 `OTG_VOTER`/`USB_ICL` 等电源投票事件。regulator 状态查询确认：

| 节点 | 状态 |
|------|------|
| `smb2-vbus` (regulator.84) | **disabled**, users=0 |
| `ext_5v_boost` (regulator.86) | **disabled**, users=0 |
| `usb/boost_current` | 0 |
| `dual_role_usb/mode` | `ufp` |

## 第三层：验证辅助性假设

为了排除「第一次成功是因为某个 sysfs 写入歪打正着」的可能，重建了操作时序：

- **第一次插入**（`dmesg -c` 清空前）：无任何 sysfs 写入 → 成功枚举
- **第三次插入**（`dmesg_cap3.txt`，18:38）：`asix new_id` 已写入 → 仍成功
- `asix new_id` 只改 USB 驱动匹配表，不影响 PMIC VBUS——排除此变量

## 系统级接口排查

### kernel debugfs

```
/sys/kernel/debug/regulator     → 不存在（CONFIG_REGULATOR_DEBUG 未开）
/sys/kernel/debug/pmic-votable  → 不存在
```

QTI 标准的 votable 框架存在（PMI8998 的 qpnp-smb2 驱动使用 `OTG_VOTER`、`BOOST_BACK_VOTER`、`WEAK_CHARGER_VOTER` 等投票者），但未暴露 sysfs，无法直接观测投票状态。

### logcat

`logcat -b all` 环缓冲已滚过 18:58 的失败插入窗口，只能看到 19:04 以后的 boot 完成内容。USD HAL 状态：

| 模块 | 状态 |
|------|------|
| `vendor.usb-hal-1-3` | ✅ running |
| `vendor.usbgadget-hal` | ✅ running |
| `UsbPortManager` boot status | `port=otg_default, mode=dual, role=device/sink, supported=[source:host, source:device, sink:host, sink:device]` |
| SELinux denial | 1 条 boot 时对 `usbd` 的 `call` 拒绝，运行时无拦截 |

**USB HAL 存在且运行正常，但无法确认它在 Sink 插入后是否投票要求 VBUS。**

## 当前结论

**根因：PMIC（PMI8998）的 OTG boost 控制器在重启后未正确初始化，导致 Type-C Sink 连接后 VBUS 不输出。** 具体来说：

1. 不是 PD 协商问题——`-14` 在成功时也出现
2. 不是 PDO 配置问题——PDO 全零在成功时也全零
3. 不是 SELinux/权限问题——运行时无拦截
4. 不是 HAL 未运行——USB HAL 正常
5. **是 PMIC 的 VBUS 使能机制在重启后失效**——`smb2-vbus` 保持 disabled，没有恢复正常状态

### 可控的操作入口

| 节点 | 可写 | 预期效果 |
|------|------|----------|
| `dual_role_usb/otg_default/mode` → `dfp` | ✅ | 强制切 host 模式，绕过 PD 协商 |
| `pd_vbus` | ✅（内容为空） | 直接使能 VBUS（需确定写入值） |
| `hard_reset` | ✅ | 触发 PD 硬复位重启协商 |

### 开放问题

1. Votable 框架中 `OTG_VOTER` 的实际投票值是多少——没有 debugfs 无法回答
2. 重启前的 `Reverse boost detected: voting 0mA` 事件——是否在 PMIC 中 latch 成持久状态？
3. 写 `dual_role_usb/mode=dfp` 是否能绕过整个 PD/协商流程、直接钳制 VBUS 输出？这是下一步最直接的验证方向

## 调试方法论笔记

1. **不要被最明显的错误输出带偏**。`Source_Capabilities: -14` 反复出现而且致命感很强，但对比成功/失败两个场景后发现它是恒存噪音。
2. **对比法拆解「噪音 vs 根因」**。关键不是「这个错误是什么意思」，而是「为什么成功时同样有这个错误但设备能用？」——真正的差异藏在另一个维度。
3. **Layer-by-layer，先只读后写入**。regulator → power_supply → dual_role_usb → PD 寄存器 → 驱动源码，每层确认完再进下一层。
4. **重建时序排除「巧合」**。验证重启前成功那次是否受到了 sysfs 写入的副作用影响——确认没有，把变量范围锁定在 reboot 本身。
5. **4.9 内核上缺乏调试接口是常态**。`CONFIG_REGULATOR_DEBUG`、debugfs、tracefs 等内核调试设施在 LineageOS 的旧内核分支上通常不开，需要走 `/sys` class 和 dmesg 两条主线。

—— 土 · 安知生
