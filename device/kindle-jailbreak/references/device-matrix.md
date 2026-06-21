# Kindle 型号对照与固件参考（截至 2026-06）

## 本会话确认的设备

### Kindle 3 (Keyboard) — ✅ 越狱完全支持

- **固件版本**：3.3.x（出厂版本，已确认）
- **越狱状态**：最稳定的越狱目标，漏洞成熟
- **越狱文件来源**：**全部公开可下载，不需要 MobileRead 账号**
  - jailbreak .bin：`https://kindlemodding.org/jailbreaking/Legacy/K2DXDXGK3-Jailbreak/k3_3.2.1/Update_jailbreak_k3w_install.bin`
  - KUAL Booklet：`https://kindlemodding.org/jailbreaking/post-jailbreak/installing-kual-mrpi/KUALBooklet.azw`（备选：KUAL-KDK-1.0.azw2）
  - MRPI zip：`https://kindlemodding.org/jailbreaking/post-jailbreak/installing-kual-mrpi/kual-mrinstaller-1.7.N-r19303.zip`
- **KOReader 包**：选 `koreader-kindle-legacy-v{版本}.zip`
  - 直接下载：`https://github.com/koreader/koreader/releases/download/v2026.03/koreader-kindle-legacy-v2026.03.zip`
  - SHA256（v2026.03）：`17934813a53575ed235edfc8ac12b4b6b1e3d5915d63b7796a77b1d7f19dee03`
- **KOReader 安装后入口**：Home 出现 KUAL 书 entry → 打开 → 选 KOReader

**正确安装流程（K3 键盘版，已验证 2026-06-04）：**
1. jailbreak .bin → USB 复制到 Kindle 根目录 → Settings → Update Kindle → 重启
2. KUAL-KDK-1.0.azw2 → USB 复制到 `/Volumes/Kindle/documents/`（**不是根目录，不是 Update**）
   → 重启后 Home 出现 KUAL 书 entry（书图标，不是设置里的更新条目）
3. MRPI zip → USB 解压复制 extensions/ + 创建 mrpackages/ + KOReader zip 解压到 extensions/koreader/ 和 koreader/
4. Home 打开 KUAL 书 → KUAL 菜单选 KOReader → Start KOReader (no framework)

**⚠️ K3 关键区别：KUAL 在 K3 上是 AZW 文档（书entry），不是固件更新 .bin。K4+ 才用 Update .bin 方式安装 KUAL。**

**MRPI 触发方式**（不是自动执行）：
- Home 界面 → 点击搜索栏 → 输入 `;log mrpi` → 回车 → MRPI 菜单打开

---

## 其他已确认信息

### Smartisan DT1902A（POS 收单设备）

- **品牌**：Smartisan（联想旗下）
- **系统**：Android 10（API 29）
- **连接**：adb devices 识别为 `8a765553`
- **问题**：根分区 100% 满（/dev/root 3.0G 已用尽）
- **注意**：与 Kindle 越狱无关，是收款机设备

---

## 已知不支持的型号

| 型号 | 原因 |
|------|------|
| Kindle 12 代（2024） | 越狱工具尚未发布 |
| 固件 ≥ 5.16.x（部分型号） | 漏洞被封堵 |