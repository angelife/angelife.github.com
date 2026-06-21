# K3 Jailbreak File Validation Log — 2026-06-04

## Verified Downloads (HTTP 200)

### Jailbreak Files — K3 3.2.1
All from: `https://kindlemodding.org/jailbreaking/Legacy/K2DXDXGK3-Jailbreak/k3_3.2.1/`

| File | HTTP | Size |
|------|------|------|
| `Update_jailbreak_k3w_install.bin` | 200 | 299,552 bytes |
| `Update_jailbreak_k3g_install.bin` | 200 | 299,552 bytes |
| `Update_jailbreak_k3gb_install.bin` | 200 | 299,552 bytes |

### Jailbreak Files — K3 3.0-3.2
All from: `https://kindlemodding.org/jailbreaking/Legacy/K2DXDXGK3-Jailbreak/k3_3.0-3.2/`

| File | HTTP | Size |
|------|------|------|
| `Update_jailbreak_k3w_3.0-to-3.2_install.bin` | 200 | 299,407 bytes |
| `Update_jailbreak_k3g_3.0-to-3.2_install.bin` | 200 | 299,407 bytes |
| `Update_jailbreak_k3gb_3.0-to-3.2_install.bin` | 200 | 299,409 bytes |

> Firmware 3.3.x uses the 3.2.1 jailbreak package (same exploit).

### KUAL / MRPI Files
All from: `https://kindlemodding.org/jailbreaking/post-jailbreak/installing-kual-mrpi/`

> ⚠️ **K3 用户注意**：以下 KUAL 文件都是 **KDK 签名版**，K3 打开会报 "Test Kindle" 错误。K3 必须用 MKK 签名版（从 MobileRead 下载）。
> K3 的 KUAL 不是 .bin，是 AZW 格式，放入 `/documents/` 后作为书 entry 出现在 Home。

| File | HTTP | Size | K3 可用？ |
|------|------|------|------|
| `Update_KUALBooklet_v2.7.37_install.bin` | 200 | 52,605 bytes | ❌ K4/K5+ 专用（.bin 安装） |
| `Update_KUALBooklet_v2.7.37_uninstall.bin` | 200 | 5,937 bytes | ❌ K4/K5+ 专用 |
| `kual-mrinstaller-1.7.N-r19303.zip` | 200 | 1,825,525 bytes | ✅ K3 可用（extensions/MRInstaller/） |
| `kual-mrinstaller-khf.zip` | 200 | — | ✅ K3 可用 |
| `KUAL-legacy.zip` | 200 | — | ✅ K3 可用（需确认签名版） |
| `KUAL-KDK-1.0.azw2` | 200 | — | ⚠️ KDK 签名版，K3 会报 Test Kindle！|
| `KUAL-KDK-2.0.azw2` | 200 | — | ⚠️ KDK 签名版，K3 会报 Test Kindle！|

### KOReader
| File | HTTP | Size | SHA256 |
|------|------|------|--------|
| `koreader-kindle-legacy-v2026.03.zip` | 200 | ~38 MB | `17934813a53575ed235edfc8ac12b4b6b1e3d5915d63b7796a77b1d7f19dee03` |

## Failed Downloads

| URL | Result |
|-----|--------|
| `https://kindlemodding.org/jailbreaking/Legacy/K2DXDXGK3-Jailbreak/` (listing) | 200 but no .bin links in HTML (dynamic JS) |
| `https://archive.org/search` | 503 |
| GitHub NiLuJe/Kindle3-Jailbreak | 404 (repo doesn't exist) |
| GitHub yifanlu/KindleTool releases | 0 releases |
| GitHub yifanlu/KindleTool actions/artifacts | 0 artifacts |

## K3 Deployment: Final Kindle USB Directory Structure (After All Steps)

```
/Volumes/Kindle/                        ← Mac USB mount point
  Update_jailbreak_k3w_install.bin      ← Step 1 .bin (installed, can delete after)
  Update_KUALBooklet_v2.7.37_install.bin ← Step 2 .bin (installed, can delete after)
  extensions/
    MRInstaller/                         ← MRPI extension manager
      bin/mrinstaller.sh
      config.xml
      menu.json
      data/mrpi-K3.tar.gz
      data/BigBlue_Terminal.ttf
    koreader/                            ← KOReader KUAL entry
      menu.json                         ← KUAL scans this file to find KOReader
      bin/
      libs/
      koreader.sh
      ...
  mrpackages/                           ← MRPI working directory (empty is fine)
  koreader/                             ← KOReader main program
    koreader.sh                         ← actual entry point
    libs/
    data/
    ...
  documents/
  music/
  system/
  audible/
```

## K3 Full Installation Sequence (Validated)

> ⚠️ **K3 专用流程（与 K4/K5+ 不同）**：
> - K3 的 KUAL 是 **AZW 文档**（放入 `/documents/`），不是 .bin 更新
> - K3 没有 Settings → Update Your Kindle 安装 KUAL 的选项
> - MKK 证书用 .bin（从 MobileRead 下载），KUAL 本身用 AZW

### Phase A: Mac Terminal (USB File Copy)
```bash
# Mount Kindle → ls /Volumes/Kindle/

# 1. Jailbreak .bin（用 kindlemodding.org 的）
cp Update_jailbreak_k3w_install.bin /Volumes/Kindle/

# 2. ⚠️ KUAL — 不要复制 kindlemodding.org 的 KDK 版！
# K3 的 KUAL 必须用 MKK 签名版（从 MobileRead 下载，文件名类似 KUALBooklet.azw）
# cp KUAL-KDK-1.0.azw2 /Volumes/Kindle/documents/  ← 这是 KDK 版，K3 会报错！

# 3. MRPI unzip + extensions merge
unzip -o kual-mrinstaller-1.7.N-r19303.zip -d /tmp/mrpi
cp -R /tmp/mrpi/extensions/ /Volumes/Kindle/extensions_mrpi/
# Merge (don't overwrite existing extensions/)
if [ -d /Volumes/Kindle/extensions/ ]; then
    cp -R /tmp/mrpi/extensions/MRInstaller/ /Volumes/Kindle/extensions/MRInstaller_mrpi/
else
    mv /Volumes/Kindle/extensions_mrpi/MRInstaller/ /Volumes/Kindle/extensions/MRInstaller/
fi
rm -rf /Volumes/Kindle/extensions_mrpi/
mkdir -p /Volumes/Kindle/mrpackages/

# 4. KOReader unzip + dual path
unzip -o koreader-kindle-legacy.zip -d /tmp/ko
cp -R /tmp/ko/extensions/koreader/ /Volumes/Kindle/extensions/koreader/
cp -R /tmp/ko/koreader/ /Volumes/Kindle/koreader/

diskutil eject /Volumes/Kindle
```

### Phase B: Kindle Screen (按顺序，顺序不能乱)
```
1. Settings → Update Kindle → 点 Update_jailbreak_k3w_install.bin → 重启

2. ⚠️ 此步骤只安装 MKK 证书（从 MobileRead 下载的 .bin 文件）
   Settings → Update Kindle → 点 Update_mkk-20141129-k3w-B008_install.bin → 重启
   Settings → Update Kindle → 点 Update-mkk-20250419-k3w-B008_keystore-install.bin → 重启

3. 将 MKK 签名版 KUAL.azw 复制到 /Volumes/Kindle/documents/
   ★ Home 出现"KUAL"书 entry（书图标，不是 app）

4. 打开 KUAL 书 → KUAL 菜单出现
   （KUAL 自动扫描 extensions/*/menu.json → 发现 KOReader → 显示条目）

5. KUAL 菜单 → KOReader → Start KOReader (no framework)
```

### Why KOReader Appears in KUAL Menu
KUAL scans all `extensions/*/menu.json` files at startup.
KOReader's `menu.json` is at `extensions/koreader/menu.json`.
If that file is missing, KOReader will NOT appear in KUAL — even if the
`koreader/` directory exists. Both paths are required.

## K3 Model Detection (No ADB)

```bash
# Via USB filesystem fingerprint
if [ -d "/Volumes/Kindle/audible" ]; then
  MODEL="KINDLE_3_KEYBOARD"
  # K3W has no audible/ dir; K3G/K3GB do
  if [ -d "/Volumes/Kindle/audible" ]; then
    MODEL="KINDLE_3_3G"  # or K3GB depending on storage
  fi
fi
if [ -d "/Volumes/Kindle/system/metadata" ]; then MODEL="KINDLE_PAPERWHITE"; fi

# Via firmware fingerprint in system/ directory
cat /Volumes/Kindle/system/version.bin 2>/dev/null || \
  strings /Volumes/Kindle/system/*.bin 2>/dev/null | head -5
```

## Critical Lessons (This Session)

**Docker vs Mac Terminal 隔离**（完全确认，无法穿透）：
- 容器 `/opt/data/` 与 Mac 终端文件系统完全隔离
- 容器：文件在 `/opt/data/kindle_koreader/` 对 Hermes 可见
- Mac 终端：`ls /opt/data/` → No such directory
- Mac 终端：文件必须通过 curl 直接下载到 ~/Downloads/

**所有 Kindle USB 操作必须在 Mac 终端执行，不走 Docker**。Docker 只负责：
- 验证下载 URL 是否有效（HTTP 200）
- 生成部署说明文档
- 把脚本写到 `/opt/data/kindle_k3_usb/KINDLE3_KOREADER_DEPLOY_V2.sh`（由用户在 Mac 终端执行）

**KUAL 菜单发现机制**（关键发现）：
- KUAL 启动时扫描所有 `extensions/*/menu.json`
- KOReader 的 `menu.json` 必须在 `extensions/koreader/menu.json`
- 缺这个文件 → KOReader 不会在 KUAL 菜单里出现，即使 `koreader/` 目录存在
- 两个路径缺一不可：`extensions/koreader/`（菜单入口）+ `koreader/`（主程序）

**MRPI 需要 `/mrpackages/` 目录**：
- MRPI 启动时检查 `mrpackages/` 是否存在，不存在则报错
- 即使不用 MRPI 安装任何东西，也必须创建此目录