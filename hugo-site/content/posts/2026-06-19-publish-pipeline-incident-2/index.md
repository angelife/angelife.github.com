---
title: "发布事故复盘（二）：当一切都正常时，我们仍然以为系统坏了"
date: 2026-06-19T10:00:00+08:00
draft: false
slug: 2026-06-19-publish-pipeline-incident-2
categories:
  - 火·AI
series:
  - ai-bu-yin
tags:
  - 故障複盤
  - 發布
  - 認知偏差
  - 調試方法論
---

摘要

2026 年 6 月 19 日，我们对 angelife.github.io 的发布链路进行了一次完整排查。

起因很简单：
新文章似乎没有出现在网站上。

于是开始了一场长达数小时的调查。

## 第一阶段：怀疑发布链路

最初看到网站上的最新文章停留在数小时之前。

因此产生第一个判断：
新文章没有发布成功。

## 第二阶段：怀疑 GitHub Pages

发现 Workflow 全绿，但 Deployments 页面显示 **Last deployed 2 weeks ago**。

## 第三阶段：怀疑 Hugo

接著检查 Build、Artifact、Deploy 确认全部正常。

## 第四阶段：最重要的测试

新增测试文章《发布链路测试》，Commit ，CI Success，但 URL 返回 404。

## 真相

测试文章没有设定 ，Hugo 使用标题作为 slug。
实际生成的是 ，而不是预期的英文字符串 URL。

我们验证的是错误 URL。

## 最终结论

经过完整验证：
- Git 正常
- SSH 正常
- GitHub Actions 正常
- GitHub Pages 正常
- Hugo 正常
- 发布脚本可工作
- 新文章可正常上线

事故并不是系统故障。
而是观测错误。

## 后续改进

**一、所有新文章强制 slug**

**二、Hermes 系统检查模式要求：**
- 优先输出原始命令结果
- 禁止推测
- 禁止脑补

**三、发布验证标准化**

发布成功定义：
- Push 成功
- CI 成功
- 文章 URL 返回 200

## 结语

这次事故没有修复一个坏掉的系统。
而是修复了一个错误的认知。

排查最大的敌人不是 Bug。
而是错误的假设。

如果假设错了。
越努力排查。
离真相反而越远。
