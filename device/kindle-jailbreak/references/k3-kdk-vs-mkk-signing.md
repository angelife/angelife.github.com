# K3 KDK/MKK 签名与证书链 — 2026-06-09 修正版

## 重要修正

**此前的 "KDK vs MKK" 二分法是错误理解。** KUAL 只有 KDK 签名版，不存在独立的"MKK 签名版 KUAL"。

## 真实架构

KUAL（Kindle Unified Application Launcher）在 K3 上以 Kindlet 应用（AZW2 格式）运行。其签名验证链如下：

```
KUAL-KDK-1.0.azw2  (KDK 签名)
  ↓  使用
Kindlet Runtime (Java VM)
  ↓  验证签名
developer.keystore  (签名证书/keystore)
  ↓  提供信任链
MKK (MobileRead Kindlet Kit)
  ↓  建立信任
Jailbreak (系统级访问)
```

### 关键纠正

| 旧错误认知 | 实际情况 |
|-----------|---------|
| "K3 需要 MKK 签名版 KUAL" | 不存在这种东西。KUAL 就是 KDK 签名版。 |
| "KDK 版需要 Test Kindle 注册" | 证书链完整时，KDK 版 KUAL 在未注册 K3 上也可正常使用。Test Kindle 错误通常是因为 keystore 过期或 MKK 2014 未正确安装。 |
| "kindlemodding.org 的 KUAL 不能用于 K3" | 可以用于 K3，只要 MKK 证书链完整。但 NiLuJe 2025 包的 KUAL 要求 FW ≥ 3.4（低版本会报"requires newer firmware"） |

## 三种错误 vs 根因

| 错误 | 根因 | 修复 |
|------|------|------|
| `permissions to open this title have expired` | keystore 过期 (2025-04-17) | 装 2025 keystore 更新 |
| `not registered as a Test Kindle` | 证书链断裂（MKK 未装 / keystore 过期 / KUAL 文件问题） | 先 MKK 2014，再 2025 keystore |
| `requires a new version of Kindle software` | K3 FW 3.3 < KUAL 要求的最低版本 | 升级到 3.4.3 |

## 验证正确的安装序列（2025-2026 社区验证）

```
1. 固件升级到 3.4.3（可选但建议）
2. Jailbreak
3. MKK 2014 证书包 → Update Your Kindle → 重启
4. DevCerts 2025 keystore → Update Your Kindle → 重启
5. KUAL-KDK-1.0.azw2 → /documents/ → 打开
```

## 来源

- Claude/ChatGPT 纠正（2026-06-09 多模型交叉验证）
- MobileRead t=367665, t=225030
- NiLuJe：keystore 于 2025-04-17 过期（t=225030 post #1295）