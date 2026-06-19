---
title: "發布事故復盤（二）：當一切都正常時，我們仍然以為系統壞了"
date: 2026-06-19T10:00:00+08:00
draft: false
slug: 2026-06-19-publish-pipeline-incident-2
categories:
  - 火·AI
series: ["ai-bu-yin"]
tags:
  - 故障複盤
  - 發布
  - 認知偏差
  - 調試方法論
---

摘要

2026 年 6 月 19 日，我們對 angelife.github.io 的發布鏈路進行了一次完整排查。

起因很簡單：
新文章似乎沒有出現在網站上。

於是開始了一場長達數小時的調查。

## 第一階段：懷疑發布鏈路

最初看到網站上的最新文章停留在數小時之前。

因此產生第一個判斷：
新文章沒有發布成功。

## 第二階段：懷疑 GitHub Pages

發現 Workflow 全綠，但 Deployments 頁面顯示 **Last deployed 2 weeks ago**。

## 第三階段：懷疑 Hugo

接著檢查 Build、Artifact、Deploy 確認全部正常。

## 第四階段：最重要的測試

新增測試文章《發布鏈路測試》，Commit ，CI Success，但 URL 返回 404。

## 真相

測試文章沒有設定 ，Hugo 使用標題作為 slug。
實際生成的是 ，而不是預期的英文字符串 URL。

我們驗證的是錯誤 URL。

## 最終結論

經過完整驗證：
- Git 正常
- SSH 正常
- GitHub Actions 正常
- GitHub Pages 正常
- Hugo 正常
- 發布腳本可工作
- 新文章可正常上線

事故並不是系統故障。
而是觀測錯誤。

## 後續改進

**一、所有新文章強制 slug**

**二、Hermes 系統檢查模式要求：**
- 優先輸出原始命令結果
- 禁止推測
- 禁止腦補

**三、發布驗證標準化**

發布成功定義：
- Push 成功
- CI 成功
- 文章 URL 返回 200

## 結語

這次事故沒有修復一個壞掉的系統。
而是修復了一個錯誤的認知。

排查最大的敵人不是 Bug。
而是錯誤的假設。

如果假設錯了。
越努力排查。
離真相反而越遠。
