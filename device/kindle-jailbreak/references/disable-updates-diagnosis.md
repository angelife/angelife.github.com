# disabled-updates/ 诊断法 — 判定 KUAL 安装状态

## 背景

通过 USB 存储模式无法直接访问 Kindle 系统日志或 `/var/local/java/keystore/`。
唯一可靠的安装状态证据来自 `disabled-updates/` 目录和根目录的 .bin 文件状态。

## 文件后缀含义

| 文件位置 | 后缀 | 含义 |
|---------|------|------|
| 根目录 | 无后缀 `.bin` | 待安装（Settings → Update Your Kindle 可见） |
| `disabled-updates/` | `.bin.last-greyed` | **已安装**（Update 菜单已灰显） |
| `disabled-updates/` | 无后缀 `.bin` | 已下载但未安装的备份（非 grayed 状态） |
| `documents/` | `.azw2` | KUAL for K3（Kindlet 应用，非 .bin 更新） |
| `developer/KUAL/` | 目录 | KUAL Booklet 已安装（K3 不生效） |

## 关键陷阱

- 文件存在于 `disabled-updates/` 但**没有** `.last-greyed` 后缀 = **未安装**，只是下载/备份
- 文件名相同但在根目录 = **pending**，在 `disabled-updates/` = **已处理**
- `.last-greyed` 的文件大小通常与原始 .bin 相同

## 完整诊断清单

```bash
# 1. 根目录 — 有 .bin 文件 = 有更新等待安装
ls -la /Volumes/Kindle/*.bin

# 2. disabled-updates/ — .last-greyed = 已安装
ls -la /Volumes/Kindle/disabled-updates/

# 3. documents/ — KUAL 文件名决定签名类型
ls -la /Volumes/Kindle/documents/KUAL*

# 4. 开发者证书相关
ls -la /Volumes/Kindle/developer/
```

## 状态评估表

| 检查项 | 正常状态 | 异常状态 | 含义 |
|--------|---------|---------|------|
| KUAL-KDK-1.0.azw2 在 documents/ | ✅ 存在 | ❌ 不存在 | K3 需要 AZW2 作为 KUAL 入口 |
| 根目录无 .bin | ✅ 已全部安装 | ❌ 有 .bin | 有更新等待安装 |
| keystore-install.bin.last-greyed 存在 | ✅ 装过 keystore | ❌ 无此文件 | **keystore 未更新** |
| MKK.bin.last-greyed 存在 | ✅ MKK 2014 已装 | ❌ 无 | MKK 2014 未安装 |
| developer/KUAL/ 存在 | ✅ Booklet 已装 | ❌ 不存在 | K3 不需要（booklet 不产生入口） |

## 应用实例（2026-06-09 K3W B008）

用户现象：KUAL 打开报 "permissions expired"

诊断路径：
1. `ls /Volumes/Kindle/` → 根目录无 .bin
2. `ls /Volumes/Kindle/disabled-updates/` → 
   - `Update_mkk-20141129-k3w-B008_install.bin`（存在，无 .last-greyed → **未安装**）
   - `Update_KUALBooklet_v2.7.37_install.bin.last-greyed`（存在 → **已安装**）
   - `KUAL-KDK-1.0.azw2.bak`（存在）
   - `KUAL-KDK-1.0.azw2.v2737.bak`（存在）
   - ❌ keystore-install.bin 或其 .last-greyed **不存在**
3. `ls /Volumes/Kindle/documents/` → `KUAL-KDK-1.0.azw2`（KDK 签名版）
4. 结论：MKK 2014 未装、2025 keystore 从未存在、KUAL 是 KDK 版