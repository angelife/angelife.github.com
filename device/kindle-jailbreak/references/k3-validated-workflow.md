# K3 验证部署流程（2026-06-04 实测）

## 验证结果

**部署包**：`/opt/data/kindle_k3_usb_deploy.zip`
- 文件数：1032 | 大小：42.0 MB
- SHA256：`a147190ef29cf042047b4985e6f6be89257114426d2d9d4ce81b36d80124b524`

**Host Mac 路径**：`/macos/.hermes-docker/minimaxlab/kindle_k3_usb_deploy.zip`
**导出命令**：`docker cp 0f6990dc817d:/opt/data/kindle_k3_usb_deploy.zip ~/Downloads/`

---

## K3 关键行为纠正（已验证）

所有 K3 操作必须遵循，违背则必定失败：

### 1. KUAL 是 AZW 文档，不是 .bin 更新包
- K3 上 KUAL 是 `.azw2` 格式，放入 `/documents/` 后在 Home 作为**书 entry** 出现
- **不是** Settings → Update Your Kindle → 选 KUAL bin（那是 K4+ 方式）
- 误用 .bin 安装 KUAL = KUAL 永远不出现

### 2. MRPI 不是自动执行的
- 必须：Home → 点击搜索栏 → 输入 `;log mrpi` → MRPI 菜单打开
- KUAL menu 里的 "Helper → Install MR Packages" 就是调 MRPI，两者等价
- 等 MRPI 自动运行 = 错误假设

### 3. KOReader 需要 menu.json 才能被 KUAL 发现
- `/extensions/koreader/menu.json` = KUAL 菜单入口
- `/koreader/` = KOReader 主程序（实际运行时代码）
- 两个路径必须同时存在，缺一不可

### 4. KDK vs MKK 签名决定设备是否能运行
- KDK 签名 KUAL → 设备必须在 Amazon 注册 Test Kindle → 未注册 K3 报错 "not registered as Test Kindle"
- MKK 签名 KUAL → 不需要设备注册 → 未注册 K3 可正常运行
- 下载 KUAL 时必须确认是 MKK 签名版，不是 KDK 版

---

## 执行步骤（K3 K3W / K3G / K3GB，固件 3.3.x）

```
Step 1 — Jailbreak
  cp Update_jailbreak.bin → /Volumes/Kindle/
  Settings → Update Your Kindle → 选 bin → 重启

Step 2 — 确认 MKK 签名版 KUAL（不是 KDK）
  从 MobileRead t=233936 + t=213336 下载 MKK 版本

Step 3 — 安装 MKK 证书（如需要切换签名）
  cp Update_mkk-*.bin → /Volumes/Kindle/
  Settings → Update Your Kindle → 每个 bin 单独执行 → 重启

Step 4 — 安装 KUAL（AZW 文档方式）
  cp KUALBooklet.azw → /Volumes/Kindle/documents/
  Home 出现 KUAL 书 entry

Step 5 — USB 复制 extensions + koreader
  extensions/MRInstaller/ → /Volumes/Kindle/extensions/MRInstaller/
  extensions/koreader/   → /Volumes/Kindle/extensions/koreader/
  koreader/              → /Volumes/Kindle/koreader/
  mrpackages/             → /Volumes/Kindle/mrpackages/

Step 6 — 打开 KUAL → KOReader → Start KOReader (no framework)
  （无设备条件的条目，K3 上必定可见）
```

---

## KOReader menu.json 分析（实测 2026-06）

KOReader `extensions/koreader/menu.json` 中可靠的 K3 启动项：

```json
{
  "name": "Start KOReader (no framework)",
  "action": "/mnt/us/koreader/koreader.sh",
  "params": "--kual --framework_stop"
}
```

此条目**无 `if` 设备条件**，K3 上必定可见。其他带 `if: "KindleVoyage"` 条件的条目在 K3 上被隐藏。

---

## USB 检测问题（最常见阻断项）

K3 套装 micro-USB 线通常是**充电专用**（无 D+/D- 数据线）：
```bash
ls /Volumes/Kindle/          # 挂载点不出现 = 线不对
diskutil list | grep -i kindle  # 无输出 = Mac 看不到
```
换用确认有数据功能的安卓手机线。

---

## Docker 环境限制

USB 操作必须在 **Mac 终端**执行，不走 Docker 容器：
- `/opt/data/` 在容器内，Mac 看不到
- `/Volumes/Kindle` 在 Mac 上，容器内不存在
- `docker cp` 可以传输文件，但 USB 检测和弹出必须在 Mac 终端

Docker 容器只负责：URL 验证、文件校验、生成部署文档。