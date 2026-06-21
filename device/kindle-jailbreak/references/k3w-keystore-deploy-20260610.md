# K3W B008 KUAL 部署诊断（2026-06-10 session 记录）

## 设备

- Kindle Keyboard 3G (D00901, k3w-B008)
- 固件 3.4.1
- 已越狱

## 当前状态

| 项目 | 状态 | 备注 |
|------|------|------|
| MKK 2014 (`Update_mkk-20141129-k3w-B008_install.bin`) | Update 灰显 + 根目录无 .bin | 疑似已安装（Update 灰显 = 已安装信号） |
| keystore 2025 (`Update-mkk-20250419-k3w-B008_keystore-install.bin`) | 已放入 Kindle 根目录 | 用户执行了 Update，但 disabled-updates/ 不存在 |
| KUAL-KDK-1.0.azw2 | ✅ 在 documents/ | 131069 bytes, NiLuJe 2025-04-19 包 |
| disabled-updates/ | ❌ 不存在 | K3 从未创建此目录 |
| KUAL 打开报错 | not registered as a Test Kindle | 两次 Update 后仍报 |

## 关键发现

1. MKK 2014 安装判断：disabled-updates/ 从未出现在 K3 上 → 不能靠此目录判断。实际信号是：Update Your Kindle 灰显 + 根目录 .bin 消失 = 已安装。
2. keystore installer 未生效：虽然 Update-mkk-20250419-k3w-B008_keystore-install.bin 被放入并执行 Update，但 Test Kindle 错误不变，说明要么 installer 被 K3 拒绝执行，要么 KUAL 签名不是 keystore 能修复的问题。
3. KUAL 文件仍报 Test Kindle：NiLuJe 2025-04-19 包的 KUAL-KDK-1.0.azw2 在证书链（疑似）安装后仍报错。

## 未测试的诊断方法

- 改系统时间到 2025-04-01 前 → 打开 KUAL → 如果正常 = 纯 keystore 问题，installer 没生效
- SSH 到 Kindle（通过 USBNetwork）→ 直接检查 /var/local/java/keystore/developer.keystore 状态
- 换一个 KUAL 构建（不同来源的 KDK 签名版）

## 容器→Mac 文件传输

SSH to Mac + SCP 已验证可用（详见 references/scp-container-to-mac.md）