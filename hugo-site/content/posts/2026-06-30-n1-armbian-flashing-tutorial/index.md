---
title: "N1刷机"
slug: "n1-armbian-flashing-tutorial"
date: 2026-06-30T12:00:00.000+08:00
draft: false
description: "斐讯 N1 盒子从拆机到 Armbian 系统部署的完整指南，包含风险分析和推荐方案"
categories:
  - "火·硬件"
series: ["n1-hardware"]
tags:
  - "斐讯N1"
  - "Armbian"
  - "刷机教程"
  - "开源硬件"

---

# 斐讯 N1 盒子刷 Armbian 完全教程（2026 版）

> **核心结论**：2026 年完全可行，ophub 维护活跃（内核 6.6.x LTS），社区成熟，闲鱼硬件成本 30-80 元。

---

## 一、硬件规格

| 项目 | 规格 |
|------|------|
| CPU | Amlogic S905D (Cortex-A53 4核) |
| GPU | Mali-450 |
| 内存 | 2GB RAM |
| 存储 | 8GB eMMC |
| 网络 | 千兆 RJ45 + WiFi AC 双频 + BT 4.1 |
| 视频 | 4K 60fps 硬件解码 |
| 电源 | 12V/2A |
| USB | 2x USB 2.0 |

---

## 二、刷机方案对比

### 方案 A：Armbian（⭐ 推荐）

**适合场景**：Docker 服务器、Home Assistant、NAS、Web 服务器、边缘计算

| 项目 | 说明 |
|------|------|
| 优势 | 通用 Linux，可跑 Docker、Home Assistant、各类应用 |
| 劣势 | 配置复杂度高，内存占用较大 |
| 推荐版本 | Debian Bookworm 或 Ubuntu Server (Minimal) |
| 推荐内核 | Linux 6.6 LTS |

### 方案 B：OpenWrt

**适合场景**：旁路由、DNS 过滤、流量监控

| 项目 | 说明 |
|------|------|
| 优势 | 网络功能强，配置简单 |
| 劣势 | 功能单一，不适合做通用服务器 |
| 来源 | 恩山论坛 F 大固件 |

### 方案 C：Android（❌ 不推荐）

- 性能浪费，无 Linux 生态
- 投屏不稳定、卡顿

---

## 三、准备工作

### 所需硬件

- [ ] 斐讯 N1 盒子
- [ ] USB 2.0 U 盘 8GB+（**必须 USB 2.0，不要 USB 3.0**）
- [ ] USB 键盘
- [ ] USB 鼠标
- [ ] HDMI 显示器/电视
- [ ] 网线
- [ ] 路由器
- [ ] 电脑（Windows/Mac/Linux）

### 所需软件

**Mac 用户**：
```bash
brew install android-platform-tools  # ADB 工具
brew install balenaetcher            # 写盘工具
```

**Windows 用户**：
- [USB Burning Tools](https://dl.google.com/dl/android/usb_burning_tool_2072.exe)（晶晨线刷工具）
- [Rufus](https://rufus.ie/) 或 [Win32 Disk Imager](https://sourceforge.net/projects/win32diskimager/)
- [balenaEtcher](https://www.balena.io/etcher/)

### 下载镜像

从 [ophub amlogic-s9xxx-armbian Releases](https://github.com/ophub/amlogic-s9xxx-armbian/releases/) 下载：
- 推荐：`Armbian_trixie_save_2025.09`（Debian Trixie）
- 或：`Armbian_bookworm_save_2025.09`（Debian 12 Bookworm，推荐新手）

---

## 四、详细刷机步骤

### 第一步：降级解锁 Bootloader（仅新机/高版本固件需要）

**判断条件**：固件版本为 2.19 且原厂系统可直接跳至第二步。

1. 连接 N1：HDMI 显示器 + 网线 + 电源
2. 等待 5 分钟让盒子自动升级到最新版本
3. 记录屏幕显示的 IP 地址
4. 在电视界面，连续点击"固件版本"4 次，直到显示"ADB 已开启"
5. 电脑终端连接：
   ```bash
   adb connect <N1_IP_ADDRESS>
   ```
6. 运行降级工具（Windows 用 `run.bat`，Mac/Linux 用 `adb shell` 执行脚本）
7. 选择选项 `(2)` 使用 N1 降级
8. 输入 N1 的 IP 地址
9. 按任意键开始，等待完成，N1 自动重启

### 第二步：制作 USB 启动盘

1. 下载选定的 Armbian 镜像（.img.gz 文件）
2. 解压镜像文件
3. 插入 U 盘，使用以下工具写入：

   **balenaEtcher**（推荐，跨平台）：
   - 选择镜像 → 选择 U 盘 → Flash
   
   **Rufus**（Windows）：
   - 选择镜像 → 选择 U 盘 → 写入模式选 **DD 模式**
   
   **Mac/Linux 命令行**：
   ```bash
   # 找到 U 盘设备（如 /dev/disk2）
   diskutil list
   # 卸载 U 盘
   diskutil unmountDisk /dev/disk2
   # 写入镜像
   sudo dd if=Armbian.img of=/dev/disk2 bs=1m
   ```

### 第三步：从 USB 启动 Armbian

1. 将制作好的 U 盘插入 N1 **靠近 HDMI 口的 USB 接口**
2. 连接键盘和显示器
3. 通过 ADB 触发启动：
   ```bash
   adb connect <N1_IP_ADDRESS>
   adb shell reboot update
   ```
4. **N1 黑屏后，拔掉电源**
5. **将 U 盘插入靠近 HDMI 的 USB 口**
6. **重新通电**
7. 等待系统启动，看到命令行界面
8. 登录：
   - 用户名：`root`
   - 密码：`1234`
9. 首次登录会提示修改密码，按提示操作
10. 创建普通用户时按 `Ctrl+C` 可跳过

> ⚠️ **权限检查**：登录后执行 `ls -l /`，确保所有目录所有者为 `root root`。如果看到 `1023 1023`，说明 U 盘权限被 Android 篡改，需重新制作 U 盘。

### 第四步：将 Armbian 写入 eMMC（永久安装）

1. 在 Armbian 终端执行：
   ```bash
   armbian-install
   ```
2. **关键选择**：输入 `(101)` 选择 Phicomm-N1 型号
3. **文件系统**：输入 `(1)` 选择 ext4
4. 等待写入完成，看到 `Installation successful`
5. 执行 `poweroff` 关机
6. **拔掉 U 盘**
7. 重新通电，系统从 eMMC 启动

> ⚠️ **不要使用 `/root/install.sh`**，该脚本有 Bug。必须用 `armbian-install` 命令。

### 第五步：初始配置

#### 5.1 更换国内镜像源

**清华源（推荐）**：
```bash
mv /etc/apt/sources.list /etc/apt/sources.list.bak
cat > /etc/apt/sources.list << EOF
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ jammy main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ jammy-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ jammy-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ jammy-security main restricted universe multiverse
EOF

cat > /etc/apt/sources.list.d/armbian.list << EOF
deb https://mirrors.tuna.tsinghua.edu.cn/armbian/ jammy main jammy-utils
EOF

apt update
apt upgrade -y
```

#### 5.2 修改时区

```bash
cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
date -R  # 验证应显示 CST 时间
```

#### 5.3 配置静态 IP（可选）

```bash
# 停止 NetworkManager
systemctl stop NetworkManager
systemctl disable NetworkManager

# 配置网络
mv /etc/network/interfaces /etc/network/interfaces.bak
cat > /etc/network/interfaces << EOF
auto eth0
iface eth0 inet static
    address 192.168.1.100/24    # 根据你的网段修改
    gateway 192.168.1.1          # 你的网关
    dns-nameservers 223.5.5.5 8.8.8.8
EOF

reboot
```

#### 5.4 开启 Swap/Zram（⚠️ 重要！）

N1 只有 2GB 内存，不开 Swap 跑 Docker 必崩：

```bash
# 创建 4GB swap 文件
fallocate -l 4G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile

# 永久生效
echo '/swapfile none swap sw 0 0' >> /etc/fstab

# 验证
free -h
```

#### 5.5 安装 Docker

```bash
# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh --mirror Aliyun

# 加入 docker 用户组（非 root 用户需要）
usermod -aG docker <你的用户名>

# 安装 Portainer 管理面板
docker run -d -p 9000:9000 --name portainer \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce

# 开机自启
docker update --restart=always portainer
```

> ⚠️ 所有 Docker 镜像必须选择 **arm64** 架构！

#### 5.6 开启 WiFi 热点（可选）

```bash
sudo armbian-config
# 进入 Network -> Hotspot
# 配置 SSID 和密码
```

或手动配置：
```bash
sudo systemctl enable hostapd
```

---

## 五、常用命令速查

```bash
# 系统配置
armbian-config          # 图形化配置工具（网络、时区、中文等）
armbian-apt             # 更换软件源
armbian-update          # 更新系统内核

# Docker 管理
docker ps -a            # 查看所有容器
docker logs -f <容器名> # 查看日志
docker exec -it <容器名> bash  # 进入容器

# 性能监控
htop                    # 实时监控
df -h                   # 磁盘空间
free -h                 # 内存使用
```

---

## 六、常见问题排查

### 问题 1：U 盘无法识别 / 无法启动

**原因**：USB 3.0 U 盘兼容性、插错 USB 口、通电前未插入 U 盘

**解决**：
1. 换 USB 2.0 U 盘（SanDisk Cruzer Blade 8GB/16GB）
2. 确认插入**靠近 HDMI 口**的 USB 接口
3. 操作时序：**断电 → 插 U 盘 → 等 5 秒 → 通电**

### 问题 2：WiFi / 网卡不可用 / 只能百兆

**原因**：DTB 文件不匹配

**解决**：
```bash
# 查看当前 DTB
ls /boot/dtb/amlogic/
# 手动指定 DTB（编辑 /boot/uEnv.txt 或 extlinux.conf）
FDT=/dtb/amlogic/meson-gxl-s905d-phicomm-n1.dtb
```

### 问题 3：SSH 卡死 / 突然断开

**原因**：2GB 内存 OOM

**解决**：
1. 确认 Swap 已开启：`free -h`
2. 限制 Docker 容器内存：
   ```bash
   docker run --memory=512m ...
   ```
3. 不要安装桌面环境

### 问题 4：中文乱码

```bash
# 修改编码
sed -i 's/LC_ALL="C"/LC_ALL="zh_CN.UTF-8"/' /etc/environment
source /etc/environment
```

### 问题 5：刷回 Android

1. 安装 USB Burning Tools
2. 解压 `N1_mod_by_webpad_v2.2_20180920.img.7z`
3. 运行烧录软件，选择 Android 固件
4. **取消勾选**"擦除 flash"和"擦除 bootloader"
5. 点击"开始"
6. 用 USB 双公头线连接盒子靠近 HDMI 的 USB 口
7. 通电，自动写入（约 3-4 分钟）

---

## 七、资源链接

| 资源 | 链接 |
|------|------|
| ophub Armbian | https://github.com/ophub/amlogic-s9xxx-armbian/releases/ |
| 恩山论坛 | https://www.right.com.cn/forum/ |
| 降级教程 | https://www.right.com.cn/forum/thread-340279-1-1.html |
| DTB 优化 | https://www.right.com.cn/forum/thread-510423-1-1.html |
| 视频教程 | https://www.bilibili.com/video/BV18u411v7aK/ |

---

## 八、关键避坑总结

1. **U 盘必须是 USB 2.0**，不要 USB 3.0
2. **断电后插 U 盘再通电**，通电状态下插 U 盘权限会被 Android 篡改
3. **不要用 `/root/install.sh`**，用 `armbian-install` 命令
4. **必须开 Swap**（至少 2GB，推荐 4GB），否则跑 Docker 必崩
5. **只装 Server/Minimal 版本**，别装桌面环境
6. **所有 Docker 镜像选 arm64 架构**
7. **编辑 nEnv.ini/uEnv.ini 用 Notepad++ 或 VSCode**，不要用 Windows 记事本（换行符问题）
