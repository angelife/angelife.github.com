# K3 KOReader 部署验证参考（2026-06-04 实测）

## 关键纠正（来自大衍神君反馈）

| 错误认知 | 正确认知 |
|---|---|
| KUAL Booklet .bin 通过 Settings → Update 安装 | **K3 上 KUAL 是 AZW 文档**，复制到 `/documents/` 后作为书 entry 出现在 Home |
| MRPI 自动出现在 KUAL 菜单 | MRPI 必须通过 `;log mrpi` 在搜索栏触发，不是自动执行 |
| KOReader 自动出现在 KUAL 菜单 | KOReader 通过 `extensions/koreader/menu.json` 被 KUAL 发现，必须有 menu.json |
| 直接把 KOReader zip 解压到 Kindle 根目录即可 | 必须同时存在：`/extensions/koreader/menu.json`（KUAL 发现）+ `/koreader/`（主程序） |

## 验证过的文件清单

| 文件 | 路径 | 大小 | 用途 |
|---|---|---|---|
| Update_jailbreak_k3w_install.bin | kindlemodding.org | 299,552 B | K3W Jailbreak |
| KUAL-KDK-1.0.azw2 | kual/ 目录（含在 MRPI zip 里） | 131,667 B | K3 KUAL 启动器 |
| kual-mrinstaller-1.7.N-r19303.zip | MRPI zip | 1,825,525 B | MRPI 扩展管理器 |
| koreader-kindle-legacy.zip | GitHub Release | ~44 MB | KOReader 主程序 |
| extensions/koreader/menu.json | 解压后 | 1,900 B | KUAL 菜单入口 |
| koreader.sh | /koreader/koreader.sh | 18,957 B | KOReader 启动脚本 |
| mrinstaller.sh | /extensions/MRInstaller/bin/ | 40,408 B | MRPI 入口脚本 |
| mrpi-K3.tar.gz | /extensions/MRInstaller/data/ | 442,411 B | K3 专用 MRPI 数据 |

## USB 部署结构（经验证）

```
kindle_k3_usb_deploy/              ← 直接复制整个目录到 /Volumes/Kindle/
├── Update_jailbreak.bin           ← K3W jailbreak（安装后删除）
├── documents/
│   └── KUAL-KDK-1.0.azw2          ← KUAL 书entry（Home 显示书图标）
├── extensions/
│   ├── MRInstaller/                ← MRPI 扩展管理器
│   │   ├── menu.json               ← KUAL 发现入口
│   │   ├── config.xml
│   │   ├── bin/mrinstaller.sh
│   │   └── data/mrpi-K3.tar.gz
│   └── koreader/                   ← KOReader KUAL 扩展
│       ├── menu.json               ← KUAL 发现 KOReader
│       ├── config.xml
│       └── bin/koreader-ext.sh
├── mrpackages/                     ← MRPI 工作目录（空目录）
└── koreader/                       ← KOReader 主程序（完整）
    ├── koreader.sh                 ← 启动脚本
    ├── libs/, ffi/, frontend/, plugins/, fonts/, data/
    └── ...
```

## KOReader menu.json 关键入口

```json
{
  "name": "Start KOReader (no framework)",
  "priority": 4,
  "action": "/mnt/us/koreader/koreader.sh",
  "params": "--kual --framework_stop"
}
```

**此条目无 `if` 条件，K3 上必定可见。** 其他"Start KOReader"条目有 `if: "KindleVoyage"` 条件，K3 上被隐藏。

## K3 正确安装流程

```
Jailbreak → 重启 → 插 USB
KUAL.azw → /documents/ → 重启后 Home 出现 KUAL 书 entry
打开 KUAL 书 → KUAL 扫描 extensions/*/menu.json → 发现 KOReader
KUAL → KOReader → Start KOReader (no framework)
```

MRPI 触发：`;log mrpi` 在 Home 搜索栏输入 → MRPI 菜单打开

## 目录

`/opt/data/kindle_k3_usb_deploy/` — 验证过的清洁部署目录（44MB, 1030个文件）
`/opt/data/kindle_k3_usb_deploy.zip` — 可分享的打包文件