# K3 多 KUAL 版本共存陷阱（2026-06-10 session 发现）

## 发现经过

2026-06-10 session，SSH 诊断 K3W B008 Kindle 文件系统时发现：

```
/Volumes/Kindle/documents/
├── KUAL-KDK-1.0.azw2    (131,069 字节 — 旧版，K3 FW 3.3 可用)
└── KUAL-KDK-2.0.azw2    (131,070 字节 — 新版，要求 FW ≥ 3.4)
```

用户不知情地有**两个 KUAL 文件**。这导致：
- Kindle Home 上出现 **两个 KUAL 书条目**
- 用户打开任一个都可能失败，但失败原因不同
- v2.0 报 `requires newer firmware`（FW 3.3 不满足 ≥ 3.4 要求）
- v1.0 报 `permissions expired`（keystore 过期，与 FW 无关）

## 诊断方法

```bash
# 检查 /documents/ 中所有 KUAL 文件
ls -la /Volumes/Kindle/documents/KUAL*
```

如果输出有多个 KUAL-* 文件，每个都会在 Kindle Home 上产生独立书条目。

## 修复

- **FW 3.3**：只保留 `KUAL-KDK-1.0.azw2`，删除 v2.0
- **FW 3.4.3**：两个都可保留，v2.0 能用

**大小对比**：
| 文件 | 大小 | 含义 |
|------|------|------|
| `KUAL-KDK-1.0.azw2` | 131,069 字节 | 旧版，不检查 FW 版本 |
| `KUAL-KDK-2.0.azw2` | 131,070 字节 | 新版，要求 FW ≥ 3.4 |

## 为什么会有两个

用户可能在多次尝试中下载不同来源的 KUAL：
1. 从 kindlemodding.org 下载（可能同时提供了 v1.0 和 v2.0）
2. 从 KUAL.tar.xz（NiLuJe 2025-04-19 包）解压的默认是 v1.0
3. 从其他来源（如 GitHub 或论坛）下载到 v2.0

K3 不做文件名去重，多个 AZW2 文件都会注册为独立书条目。

## 经验教训

诊断 K3 KUAL 问题时，**必须检查 `documents/` 中是否有多个 KUAL 文件**。一个常见的误诊场景是：用户报告打开 KUAL 报错，实际上打开的是不兼容的 v2.0 而非 v1.0。