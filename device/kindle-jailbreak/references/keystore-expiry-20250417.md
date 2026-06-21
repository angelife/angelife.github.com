# developer.keystore 过期诊断（2025-04-17）

## 核心理由

Kindlet Runtime 使用 `/var/local/java/keystore/developer.keystore` 验证 KUAL（及所有 Kindlet）的签名。
此 keystore 于 **2025-04-17 到期**。

**来源**：NiLuJe（KUAL 维护者），MobileRead t=225030 post #1295（2025-04-18 22:57 UTC）

> _@NiLuJe Looks like the "developer.keystore" used by KUAL expired yesterday (April 17th). So Kindles now don't want to open KUAL_
> — shamanNS 报告

> _Rebuilt both KUAL builds in the first post against an updated keystore_
> — NiLuJe 回应

## 影响范围

- **所有 Kindle 型号**：K3/K4/K5/PW/Touch/Voyage/Oasis/Kindle 10/11
- **不限固件版本**，不限越狱状态

## 两种错误形式（同根因）

| 机型 | 显示错误信息 |
|------|-------------|
| K3 及部分旧设备 | `"The permissions to open the requested title have expired."` |
| K4/K5/PW2+/Oasis/Voyage | `"Internal Error: 003"` 或 `"Error 003"` |

**来源**：MobileRead t=367665 — K3 用户 Ebookus (post #4), K4 用户 sepd (post #3)

## 诊断步骤（通过 USB 存储模式）

当用户报告 permissions expired 或 Error 003 时，通过检查 Kindle USB 存储目录来判断修复进度：

### 1. 检查 disabled-updates/ 目录
- `.bin` 文件 = 已下载但未安装（或安装后未被系统移到别处）
- `.bin.last-greyed` 后缀 = **该 bin 已经安装过**（Settings → Update Your Kindle 中灰显的标志）

### 2. 检查根目录是否有 .bin 文件
- 根目录下有 `.bin` = 等待安装（Settings → Update 可见）
- 根目录下无 `.bin` = 没有待安装的更新

### 3. 判断 keystore 更新是否已完成
- `Update-mkk-20250419-k3w-B008_keystore-install.bin` 文件不存在（既不在根目录也不在 disabled-updates/）→ **从未下载安装**
- `Update_mkk-20141129-k3w-B008_install.bin` 在 disabled-updates/ 中 + 根目录无此文件 → MKK 2014 已安装

### 4. 检查 documents/KUAL 文件类型
- `KUAL-KDK-1.0.azw2` = KDK 签名版（可能同时有 Test Kindle 问题）
- KUAL Booklet bin 文件在 K3 上会安装到 `developer/KUAL/` 但不产生 Home 图标

### 5. 完整状态评估表

| 文件在 disabled-updates/ 中 | 含义 |
|----------------------------|------|
| `Update_mkk-20141129-*.bin.last-greyed` | MKK 2014 已安装 |
| `Update_KUALBooklet_v*.bin.last-greyed` | KUAL Booklet 已安装（仅 K4+ 有效） |
| 无 `keystore-install.bin` 相关文件 | 2025 keystore 更新未装 |

## 临时修复（仅供验证）

改系统时间到 2025-04-01（aha, t=367665 post #13, 2025-04-18）：
需 USBNetwork SSH：`date -s "2025-04-01"`
然后打开 KUAL。重启后需重设。

**这也证明了**根因是 keystore 过期，而非其他原因。

## 正式修复

从 NiLuJe DevCerts-20250419-KeyStore.zip（attachmentid=215127）
中取对应机型的 keystore update .bin。

K3W (B008) 文件：`Update-mkk-20250419-k3w-B008_keystore-install.bin`

**安装**：复制到 Kindle 根目录 → Settings → Update Your Kindle

K3 成功案例（whatever4kindle, t=367665, 2025-04-19）：
> _the updated certifications worked with the kindle 3 keyboard_

## 验证 keystore 已更新

USBNetwork SSH：
```bash
ls -la /var/local/java/keystore/developer.keystore
```
正常文件约 1.8KB，时间戳 > 2025-04-17 = 已更新。

或直接：装完后打开 KUAL，无报错 = 成功。

## 与 Test Kindle 错误的区别

| 错误 | 根因 | 修复 |
|------|------|------|
| permissions expired / Error 003 | keystore 2025-04-17 过期 | 装 2025 keystore update bin |
| not registered as Test Kindle | 用了 KDK 版 KUAL | 换 MKK 签名版 |

**两个错误可共存**。KUAL 是 KDK 版且 keystore 也过期时，先报 Test Kindle 错误。
装 MKK 签名版后 Test Kindle 消失，只剩下 permissions expired（如果 keystore 仍未更新）。

## USBNetwork SSH 连接故障排查

连接到 K3 USBNetwork 时常见模式：

| 现象 | 含义 | 处理 |
|------|------|------|
| `Connection closed by 192.168.2.1 port 22` | 端口有回应但连接被拒绝 | root SSH key 未配置或密码不匹配 |
| `Connection timed out during banner exchange` | SSH 协议协商失败 | 可能是旧版 dropbear 限制 |
| 无响应（timeout） | USBNetwork 未运行 | 检查 Kindle 上的 USB 网络设置 |
| 能 ping 但 SSH 拒绝 | 服务在运行但 auth 失败 | 尝试空密码或已知 key |

K3 上 USBNetwork 的默认地址是 `192.168.2.1`，默认用户 `root`，密码通常为空。
如果 SSH 连接被拒绝但端口有回应，说明 USBNetwork 的 dropbear 在运行但认证配置不匹配。

## 应用实例（2026-06-09 K3W B008）

完整诊断路径记录：

1. 用户报告 KUAL 报 `permissions expired`
2. `ls /Volumes/Kindle/` → 只有 audible/documents/koreader/music/system，无根目录 .bin
3. 用户此前执行了 KOReader deploy 脚本，删除了 developer/、disabled-updates/、extensions/
4. 判断：Kindle 被恢复出厂设置或 KOReader deploy 脚本覆盖了文件结构
5. 下载 DevCerts-20250419-KeyStore.zip 到 ~/Downloads/（105KB）
6. 解压后找到 `Update-mkk-20250419-k3w-B008_keystore-install.bin`
7. 复制到 /Volumes/Kindle/ 根目录
8. SHA256: 222275c6183d22e251cc639c5c3c7dc071025413fd4f57227c7f40e2c5ed3894
9. 待用户在 Kindle 上选择 Settings → Update Your Kindle

关键教训：KOReader deploy 脚本不应覆盖 Kindle 根目录。如果已覆盖，需要从零重装 MKK 证书链 + keystore + KUAL。

## 引用汇总

- NiLuJe 确认 keystore 过期: t=225030 post #1295
- DevCerts 修复包: attachmentid=215127 (103KB)
- K3 修复成功: t=367665 whatever4kindle (2025-04-19)
- 改日期临时方案: t=367665 post #13 aha (2025-04-18)
- K4 Error 003: t=367665 post #3 sepd
- K3 permissions expired: t=367665 post #4 Ebookus
- K4NT RuntimeException 修复: t=367665 post #9 — 删 hotfix bin
- 文件清单诊断法: 2026-06-09 Hermes Agent session, 通过 disabled-updates/ 和 .last-greyed 后缀验证安装状态
- USBNetwork SSH Connection closed 但端口回应: 同 session