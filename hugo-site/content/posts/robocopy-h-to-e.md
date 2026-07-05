---
title: "Win10 整盘镜像备份备忘：H 盘 → E 盘"
date: 2026-07-05
---

## 场景
Win10 (192.168.1.25) 要把 H 盘完整镜像到 E 盘根目录，不重建 `H_backup` 目录，直接落到 `E:\`。

## 命令
```cmd
robocopy H:\ E:\ /E /R:0 /W:0 /XD "E:\System Volume Information" /LOG+:C:\tools\h_to_e.log /NP /NFL /MT:16
```

## 说明
- `H:\ E:\`：源盘 H，目标盘 E 根目录
- `/E`：复制所有子目录，包括空目录
- `/R:0`：失败不重试
- `/W:0`：重试间隔 0 秒
- `/XD "E:\System Volume Information"`：排除系统还原文件夹
- `/LOG+`：追加日志
- `/NP`：不显示百分比
- `/NFL`：不显示文件名
- `/MT:16`：16 线程并行

## 结论
这条命令可直接用于 Win10 本地整盘备份，保持目录结构，错误跳过，日志可核对。
