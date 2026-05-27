---
title: "建站模式日志"
url: "/site-workflow/"
summary: "angelife 网站的建站、发布、交接与回退方式"
---

angelife 当前采用固定发布方式：

> 本地 Hugo 生成 -> rsync 到仓库根目录 -> commit -> push -> git tag

Hugo 源站位于 `hugo-site/`，GitHub Pages 实际读取仓库根目录静态产物。也就是说，只提交 `hugo-site/content/` 并不等于网站上线，必须先构建，再把 `hugo-site/public/` 同步到仓库根目录。

## 版本号规则

`v2026.05.27-05` 及以前为日期流水版本；自 `v0.6.0` 起，angelife 网站改用 SemVer：`vMAJOR.MINOR.PATCH`。

- `MAJOR`：网站架构、发布方式、主题结构发生破坏性变化。
- `MINOR`：新增功能、栏目、搜索、评论、日志系统、内容体系。
- `PATCH`：修复样式、错字、链接、图片、分类、小 bug。

## 为什么不默认用 GitHub Actions

当前不优先使用 GitHub Actions 在线构建，原因是：

- 线上实际读取根目录静态产物；
- 本地 Hugo `v0.147.4` 构建稳定；
- GitHub Actions 曾因 `Hugo latest` / PaperMod `rss.xml` 兼容问题失败。

除非明确授权，后续 AI 不应临时切换部署方式。

## 每次修改后的固定动作

每次修改都要：

1. 更新公开 changelog。
2. 更新内部日志。
3. 更新项目总控进度。
4. 本地运行 Hugo 构建。
5. `rsync` 到仓库根目录。
6. commit 并 push。
7. 创建 Git tag 作为可回退版本。

回退方式采用非破坏式回退：

```bash
git checkout VERSION -- .
git commit -m "Rollback site to VERSION"
git push origin master
```

## AI 接手规则

所有 AI 接手前必须先读：

- `PROJECT_STATUS.md`
- `BUILD_HANDOFF.md`
- `AI_WORK_RULES.md`
- `SITE_STYLE_GUIDE.md`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `hugo-site/data/changelog.yaml`

## 当前网站结构

- 首页：五行主入口，保持宽屏画卷式结构。
- 文章：窄栏、安静、书页感阅读体验。
- 日课：每日文章与即时思考。
- 搜索：盘活知识库，支持命中词高亮、上下文摘要、分类和标签检索。
- 更新日志：记录网站演化。

文章排版借鉴 yangzhiping.com 的克制、窄栏、书页感，但不照抄。

## 评论系统

评论系统优先采用 giscus，基于 GitHub Discussions。

正式启用前，需要用户在 GitHub 仓库开启 Discussions，安装/授权 giscus，并提供 `repoId` / `categoryId`。在缺少这些参数前，评论区默认隐藏，不显示空白报错区。

文章可用 front matter 控制：

```yaml
comments: true
comments: false
```

正式长文可开启评论；日课短文、旧日志和资料归档默认不开。

## 项目总控流程图

TODO：等待补充 `hugo-site/static/images/workflow/site-control-map.png` 后，在此处显示项目总控流程图。

<!--
![angelife 网站项目总控流程图](/images/workflow/site-control-map.png)
-->
