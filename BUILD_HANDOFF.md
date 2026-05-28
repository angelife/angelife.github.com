# angelife 建站交接手册

本文件是任何 AI 接手 angelife 网站前必须阅读的建站交接手册。

## 当前固定发布方式

固定流程：

1. 在 `hugo-site/` 本地运行 Hugo 构建。
2. 将 `hugo-site/public/` 用 `rsync` 同步到仓库根目录。
3. 提交源文件和根目录静态产物。
4. `git push origin master`。
5. 创建并推送 Git tag，作为可回退备份点。

当前最新版本：`v0.6.14`。

标准命令：

```bash
cd /Users/macos/angelife.github.com/hugo-site
hugo --cleanDestinationDir --minify

cd /Users/macos/angelife.github.com
rsync -av hugo-site/public/ ./
touch .nojekyll

git status --short
git commit -m "..."
git push origin master
git tag -a VERSION -m "VERSION: ..."
git push origin VERSION
```

## 当前不优先使用 GitHub Actions 在线构建

当前不默认切换到 GitHub Actions 在线构建。原因：

- 线上实际读取的是仓库根目录静态产物。
- 本地 Hugo `v0.147.4` 构建稳定。
- GitHub Actions 曾因 `Hugo latest` / PaperMod `rss.xml` 兼容问题失败。

除非用户明确授权，不要临时切换部署模式，不要修改 workflow。

## 目录职责

- `hugo-site/`：Hugo 源站目录。
- 仓库根目录：GitHub Pages 实际发布目录。
- `hugo-site/public/`：本地构建产物，构建后通过 `rsync` 同步到仓库根目录。
- `_incoming/`：临时素材区，不提交、不发布。
- `old-site/`：旧站历史版本，保留用于追溯，不随意删除。

## 每轮修改要求

每次修改必须：

- 更新版本号。
- 更新 `SITE_CHANGELOG.md`。
- 更新 `DAILY_WORK_LOG.md`。
- 更新 `PROJECT_STATUS.md` 中的当前状态。
- 如影响公开站点，更新 `hugo-site/data/changelog.yaml`。
- 运行 `hugo --cleanDestinationDir --minify`，必须 0 errors。
- `rsync -av hugo-site/public/ ./` 到仓库根目录。
- 提交后创建 Git tag。

注意：推荐使用仓库根目录 `./publish.sh`。脚本已排除根目录治理文档、站点校验 txt、Git 元数据和 Hugo 源站目录，避免 `rsync --delete` 误删非发布产物。

## 版本号规则

`v2026.05.27-05` 及以前为日期流水版本；自 `v0.6.0` 起，angelife 网站改用 SemVer：`vMAJOR.MINOR.PATCH`。

- `MAJOR`：网站架构、发布方式、主题结构发生破坏性变化，例如 `v1.0.0`、`v2.0.0`。
- `MINOR`：新增功能、栏目、搜索、评论、日志系统、内容体系，例如 `v0.6.0`。
- `PATCH`：修复样式、错字、链接、图片、分类、小 bug，例如 `v0.6.1`。

每次发布必须创建同名 Git tag，tag 是可回退备份点。

## 文章双版本维护（v0.6.11+）

以后每篇文章不写两份正文。

一份 Markdown 源文件 → Hugo 自动生成两个版本：
- 普通图文版 `/posts/<slug>/`
- Kindle 阅读版 `/kindle/posts/<slug>/`

封面图只服务普通版。发布验收必须同时检查两个版本。

## Kindle 接手交接确认（v0.6.14+）

Kindle 阅读模式规则已固化到 `AI_WORK_RULES.md` 和 `SITE_STYLE_GUIDE.md`。

- 修改 layout/header/footer/baseof/single/list/outputFormats 前必须先读 `AI_WORK_RULES.md` 中的 Kindle 不可破坏规则和验收要求。
- 每次发布文章后必须验收普通版和 Kindle 版。
- Kindle 版是独立输出（Hugo outputFormat），不是 CSS 隐藏变体。
- 不得提交 `_incoming/`。
- 不得提交 `.reasonix/`。
- 不得 `git add .`。

## 搜索与评论维护

- 站内搜索依赖首页 JSON 输出与 `/search/` 页面，搜索索引必须包含标题、摘要、正文、分类、标签和链接。
- 搜索增强应保持轻量，不要引入复杂后端。
- 评论系统优先预留 giscus，基于 GitHub Discussions。
- giscus 未配置 `repoId` / `categoryId` 前必须隐藏评论区，不得显示空白报错区。
- 正式启用评论前，需要用户在 GitHub 仓库开启 Discussions，安装/授权 giscus，并提供 `repoId` / `categoryId`。

## 回退方式

统一使用非破坏式回退：

```bash
git checkout VERSION -- .
git commit -m "Rollback site to VERSION"
git push origin master
```

不要使用 force push 回退，除非用户明确要求。
