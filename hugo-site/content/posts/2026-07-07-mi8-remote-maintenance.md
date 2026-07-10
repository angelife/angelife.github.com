---
title: "小米 8 单 USB-C 口远程维护实录：从 USB 断线到有线 TCP ADB 稳定运维"
date: 2026-07-07
tags: [Android, Mi8, ADB, 以太网, 远程维护, Magisk]
---

## 背景

Xiaomi Mi 8（dipper）只有 **一个 USB-C 口**。当你插入 USB-C 转以太网适配器让它走有线网络时，USB ADB 会立刻断开，这不是软件问题，而是硬件层面的设备角色互斥。

如果你需要在插网卡后继续远程操作手机，有几条路可以走：

| 方案 | 可行性 | 说明 |
|------|--------|------|
| WiFi ADB | 低 | Mi8 WiFi 损坏或不可用时无效 |
| USB Hub + 同时接网卡和 ADB | 硬件上不成立 | 单口只能服务一个主设备角色 |
| TCP ADB（临时） | 中 | 插网卡前开，但重启/断网后失效 |
| TCP ADB + service.d 持久化 | **高** | 本文方案 |

## 核心解法：Magisk service.d 持久化 TCP ADB

思路很简单：**在还连着 USB 的时候，提前把 TCP ADB 开起来，并设为 Magisk 开机自启。** 之后拔 USB、插网卡，都能通过网络继续操作。

### 第一步：静态 IP 脚本

在手机上创建 `/data/local/tmp/eth-setup/eth-static.sh`：

```bash
#!/system/bin/sh
set -e
IFACE=$(ls /sys/class/net/ | grep -E '^eth|^en' | head -n 1)
[ -z "$IFACE" ] && exit 0
ifconfig "$IFACE" 192.168.1.26 netmask 255.255.255.0 up
ip route replace default via 192.168.1.1 dev "$IFACE"
mkdir -p /data/local/tmp/eth-setup
echo nameserver 223.5.5.5 > /data/local/tmp/eth-setup/resolv.conf
echo nameserver 8.8.8.8 >> /data/local/tmp/eth-setup/resolv.conf
```

> **注意**：这里用 `ip route replace` 而不是传统 `route add`。实测发现旧写法会静默失败，导致手机有 IP 但上不了网，踩过这个坑。

把这个脚本链接到 Magisk 自启目录：

```bash
ln -sf /data/local/tmp/eth-setup/eth-static.sh /data/adb/service.d/eth-static.sh
chmod 755 /data/adb/service.d/eth-static.sh
```

这样无论网卡什么时候被识别，或者手机什么时候重启，`service.d` 都会自动把 IP、网关、DNS 配好。

### 第二步：TCP ADB 持久化

创建 `/data/local/tmp/adb-tcp-service.sh`：

```bash
#!/system/bin/sh
setprop service.adb.tcp.port 5555
stop adbd 2>/dev/null || true
start adbd
```

同样挂到 `service.d`：

```bash
ln -sf /data/local/tmp/adb-tcp-service.sh /data/adb/service.d/adb-tcp.sh
chmod 755 /data/adb/service.d/adb-tcp.sh
```

从此每次开机，手机都会自动在 `192.168.1.26:5555` 上监听 TCP ADB。

### 第三步：操作流程

**首次设置（有 USB 线的时候）**：

```
1. USB 连接 Mi8
2. adb start-server
3. adb shell 'su 0 -c "setprop service.adb.tcp.port 5555; stop adbd; start adbd"'
4. adb connect 192.168.1.26:5555
5. 验证：ip addr show eth0 | grep inet
6. 拔 USB
7. 插网卡
8. adb connect 192.168.1.26:5555
```

**持久化后（日常）**：

```
1. 插网卡
2. 等 10-15 秒
3. adb connect 192.168.1.26:5555
```

不需要再碰 USB。

## 容易踩的坑

### 坑 1：默认网关缺失

症状：`ip addr` 里 `eth0` 已经有 `192.168.1.26/24`，但 `ping 8.8.8.8` 超时。

根因：`ip route` 里只有 `192.168.1.0/24 dev eth0`，**缺 `default via 192.168.1.1`**。

验证：

```bash
adb shell 'ip route show default'
```

看到只有链路路由，没有默认网关，就是这个问题。

修复：

```bash
adb shell 'su 0 -c "ip route replace default via 192.168.1.1 dev eth0"'
```

本文的静态 IP 脚本已经用 `ip route replace`，不会再有这个问题。

### 坑 2：ping 超时不等于 DNS 不通

遇到网络不通时，先查路由，再查 DNS。顺序：

```bash
# 1. 网关通不通？
ping -c2 192.168.1.1

# 2. 公网 IP 通不通？（绕开 DNS）
ping -c2 8.8.8.8

# 3. DNS 解析通不通？
ping -c2 mirrors.aliyun.com
```

如果公网 IP 通但域名不通，才是 DNS 问题。

### 坑 3：`service.d` 脚本的错误输出被吞掉

不要用 `>/dev/null 2>&1 || true` 掩盖关键错误。调试时把输出打到日志里，出问题能立刻定位。

### 坑 4：拔 USB 后 TCP ADB 连不上

检查顺序：

1. `ping 192.168.1.26` — 手机有线 IP 起来了吗？
2. `cat /proc/net/arp | grep 192.168.1.26` — 同网段能看到 ARP 吗？
3. `ip route show default` — 网关有了吗？
4. 前三跳都通，再查 `iptables` 和路由器 AP 隔离。

## 为什么这个方案稳

**不用 WiFi** — 有线直连，延迟低、不受无线干扰。

**不依赖单次操作窗口** — `service.d` 是 Magisk 原生机制，开机执行，脚本幂等，反复重启也不会累积副作用。

**可回退** — 如果 TCP ADB 出了什么问题，插回 USB 就能立刻恢复控制权，不会把手机锁死在远程状态。

**低侵入** — 所有脚本都在 `/data/local/tmp/` 和 `/data/adb/service.d/`，不碰系统分区，刷机不会丢。

## 环境数据

| 项目 | 值 |
|------|----|
| 设备 | Xiaomi Mi 8 (dipper) |
| 系统 | LineageOS 22.2 / Android 15 |
| Root | Magisk |
| MAC | `00:e0:4c:36:17:0c` |
| 有线 IP | `192.168.1.26/24` |
| 网关 | `192.168.1.1` |
| DNS | `223.5.5.5`, `8.8.8.8` |
| TCP ADB | `192.168.1.26:5555` |
| 网卡 | USB-C 转以太网适配器 |

## 总结

Mi8 单 USB-C 口的远程维护问题，本质上是**把“一次性手动操作”变成“开机自动执行”**。通过 Magisk `service.d` 同时处理静态 IP + TCP ADB 开机自启，就不再需要在每次插拔网卡时抓 USB 窗口。这套方案已经过实际部署验证，是目前成本最低、侵入最小的远程维护路径。
