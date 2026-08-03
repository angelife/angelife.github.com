---
title: "MacBook i3 键盘失灵排查：一场从 fcitx5 到 libinput 的七轮排查"
date: 2026-08-03T15:00:00+08:00
draft: false
slug: macbook-i3-keyboard-debug
categories:
  - "土·基建"
tags:
  - "linux"
  - "arch"
  - "i3"
  - "keyboard"
  - "debug"
---

## 问题

水同学的 MacBookPro12,1 装了 Arch Linux + i3。某天从 xfce 切换到 i3 后，物理键盘无法输入字母数字，但 i3 快捷键（Mod+Return、Mod+Space 等）正常。

症状很诡异：
- 字母键按了没反应，终端里打不出字
- 但 Mod 快捷键还能用
- 候选框能弹出来（fcitx5 在运行）
- 外接键盘也试过，一样不行

排查花了七轮对话，验证了十多个假设，最终根因是一个看似无害的 Xorg 配置项。

## 排查地图

问题涉及多层：物理键盘 → 内核 evdev → libinput → Xorg X Input → X11 应用。我画了一张完整的地图，把每一层标上已排除和未验证，避免盲目试错。

```
物理键盘 (USB HID)
    ↓ 已排除：硬件正常 (evtest 能读到 KEY_A/B/C)
内核 evdev (/dev/input/event6)
    ↓ 已排除：权限、udev 规则、seat 都正常
libinput (用户态库)
    ↓ 疑似断点：DEVICE_ADDED 有，KEYBOARD_KEY 没有
xf86-input-libinput (Xorg 驱动)
    ↓ 已排除：非驱动问题
Xorg X Input Extension
    ↓ 已排除：设备层级正常，无 floating，无 grab
X11 应用 (alacritty/kitty)
    ↓ 已排除：换终端也一样
```

## 被排除的假设

第一轮怀疑 fcitx5。关闭输入法后仍然不行，排除。

第二轮怀疑 alacritty 的 XIM 实现。换 kitty，问题依旧，排除。

第三轮怀疑 floating slave——设备挂错层级。`xinput list` 显示 id=8 正常挂在 master keyboard(3) 下，排除。

第四轮怀疑 XGrabKey 冲突。`xprop -root` 没有 grab，i3 快捷键正常，排除。

第五轮怀疑 logind/seat 状态。`loginctl show-session` 显示 session 108 (seat0, Active=yes)，没有残留 xfce session，排除。

第六轮怀疑 EVIOCGRAB。但 `evtest` 一直能读到事件，如果有进程 grab 了 event6，evtest 也应该读不到。排除。

测错节点？`xinput list` 只显示一个 Apple 设备，`libinput list-devices` 确认 Kernel: /dev/input/event6，排除。

## 真正的断点

六轮排除了所有上层之后，问题锁定在 libinput 层。

`evtest` 能读到物理按键事件，但 `libinput record /dev/input/event6` 只输出 DEVICE_ADDED，没有任何 KEYBOARD_KEY 事件。

```
/dev/input/event6: root 382 F.... systemd-logind
                 root 74289 F.... Xorg
```

两个进程都打开了 event6，但 libinput 收不到事件。

重启 Xorg 依然如此——说明不是 session 切换的临时状态问题。

## 根因

最终发现：`/etc/X11/xorg.conf.d/40-trackpad-touchpad.conf` 里有一行：

```
Option "DisableWhileTyping" "true"
```

这行配置是给触控板的，但 Apple MacBookPro12,1 的内置键盘和触控板是**同一个 USB 设备**（vendor 05ac, product 0273），共享同一个 `/dev/input/event6`。libinput 在处理这个复合设备时，`DisableWhileTyping` 选项的错误地影响了整个键盘事件链路。

移除这一行后，键盘恢复正常。

```bash
# 原来的配置（有问题）
Section "InputClass"
    Identifier "Apple Trackpad bcm5974"
    MatchIsTouchpad "on"
    MatchProduct "bcm5974"
    Driver "libinput"
    Option "Tapping" "true"
    Option "NaturalScrolling" "true"
    Option "DisableWhileTyping" "true"  # ← 问题在这里
    Option "PalmDetection" "true"
EndSection

# 修复后（移除了 DisableWhileTyping）
Section "InputClass"
    Identifier "Apple Trackpad bcm5974"
    MatchIsTouchpad "on"
    MatchProduct "bcm5974"
    Driver "libinput"
    Option "Tapping" "true"
    Option "NaturalScrolling" "true"
    Option "PalmDetection" "true"
EndSection
```

## 验证

```bash
DISPLAY=:0 xinput test 8
# key press   57
# key press   31
# key release 57
```

键盘正常了。

## 经验总结

1. **排查前先画地图**。把系统分层，每层标上已排除/未验证，避免重复做已经做过的测试。

2. **不要相信"看起来正常"的日志**。Xorg 日志里 device removed + re-added 看起来像正常 hotplug，但重启后问题依旧说明这不是临时状态。

3. **复合设备是坑**。Apple MacBookPro12,1 的键盘和触控板共享同一个 USB 接口，X11 的 InputClass 按 product 匹配时可能影响错误范围之外的设备。

4. **evtest 比 xinput 更可信**。evtest 直接读内核 evdev，绕过 libinput 和 X Input。如果 evtest 能读到但 xinput 读不到，断点就在 libinput 层。

5. **重启 Xorg 不是万能药**。这个问题重启 Xorg 多少次都没用，因为 libinput 的输入类配置在每次启动时都会被重新加载同样的错误选项。

## 附：排查命令速查

```bash
# 1. evtest 验证内核层
sudo evtest /dev/input/event6

# 2. xinput test 验证 X Input 层
DISPLAY=:0 xinput test 8

# 3. libinput debug-events 验证 libinput 层
sudo libinput debug-events --device /dev/input/event6 --verbose

# 4. 设备层级检查
DISPLAY=:0 xinput list

# 5. 检查 grab
DISPLAY=:0 xprop -root | grep -i grab

# 6. 检查 session 状态
loginctl show-session $(loginctl | grep seat0 | awk '{print $1}') -p Active -p State

# 7. 检查 event6 谁在打开
sudo fuser -v /dev/input/event6
```
