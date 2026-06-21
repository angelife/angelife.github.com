# K3 MKK 公开下载源（2026-06-05 session 验证）

## 核心发现

**Error 003 根因**：developer.keystore（Kindlet 运行时证书）于 2025-04-17 过期。
2014 MKK 证书写入的是过期证书，KUAL 无法签名验证 → Error 003。

**Update Your Kindle 消失** = OTA 证书写入成功（正常现象），与 Error 003 无关。

## Session 验证过的公共下载（均 HTTP 200，无需账号）

| 文件 | URL | 大小 | local path |
|------|-----|------|------------|
| MKK 证书包（mkk.tar.xz） | `https://storage.gra.cloud.ovh.net/v1/AUTH_2ac4bfee353948ec8ea7fd1710574097/mr-public/Touch/kindle-mkk-20141129-r18833.tar.xz` | 295KB | ~/kindle_k3_fix/mkk.tar.xz |
| DevCerts-20250419.zip | `https://www.mobileread.com/forums/attachment.php?attachmentid=215127&d=1745098511` | 103KB | ~/kindle_k3_fix/DevCerts-20250419.zip |
| KUAL 工具包（kual.tar.xz） | `https://storage.gra.cloud.ovh.net/v1/AUTH_2ac4bfee353948ec8ea7fd1710574097/mr-public/KUAL/KUAL-v2.7.37-gfcb45b5-20250419.tar.xz` | 220KB | ~/kindle_k3_fix/kual.tar.xz |

## 文件提取

```bash
# MKK 证书包
tar -xf mkk.tar.xz
# → DevCerts/Update_mkk-20141129-k3w-B008_install.bin（k3w-B008 用）

# DevCerts zip
python3 -c "import zipfile; z=zipfile.ZipFile('DevCerts-20250419.zip'); print(z.namelist())"
# 提取对应型号（k3w-B008）
python3 -c "
import zipfile
with zipfile.ZipFile('DevCerts-20250419.zip') as z:
    data = z.read('Update-mkk-20250419-k3w-B008_keystore-install.bin')
    open('Update-mkk-20250419-k3w-B008_keystore-install.bin','wb').write(data)
"

# KUAL 包
tar -xf kual.tar.xz
# → KUAL-KDK-1.0.azw2（k3w 用，放入 documents/）
```

## 完整安装序列（k3w-B008 / D00901）

```
Kindle 根目录：
  Update_mkk-20141129-k3w-B008_install.bin  → Settings → Update Your Kindle → 重启
  Update-mkk-20250419-k3w-B008_keystore-install.bin  → Settings → Update Your Kindle（重见）→ 重启

Kindle documents/：
  KUAL-KDK-1.0.azw2  → Home 出现书 entry → 打开 KUAL → 无 Error 003 = 成功
```

## 型号 vs 证书文件对照

| 型号 | 设备代码 | 证书文件名 |
|------|---------|-----------|
| K3 WiFi | k3w-B008 | Update_mkk-*-k3w-B008* |
| K3 3G | k3g-B006 | Update_mkk-*-k3g-B006* |
| K2 | k2-B002 | Update_mkk-*-k2-B002* |
| K4 | — | k4-ALL* |
| K5 | — | k5-ALL* |

**注意**：k3g ≠ k3w，不能混用。