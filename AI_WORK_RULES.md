# angelife AI 工作规则

本文件适用于所有接手 angelife 网站的 AI，包括 ChatGPT、Codex、Claude、DeepSeek、Reasonix 或其他 AI。

## 接手前必读

任何 AI 接手前必须先读：

- `PROJECT_STATUS.md`
- `BUILD_HANDOFF.md`
- `AI_WORK_RULES.md`
- `SITE_STYLE_GUIDE.md`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `hugo-site/data/changelog.yaml`

## 硬性禁止

- 不准临时切换 GitHub Actions 在线构建。
- 不准修改 workflow，除非用户明确要求。
- 不准 `git add .`。
- 不准提交 `_incoming/`。
- 不准发布 `_incoming/`。
- 不准改完不写日志。
- 不准破坏首页宽屏布局。
- 不准破坏文章页窄栏书页风格。
- 不准只提交 Hugo 源文件而忘记 `rsync` 根目录静态产物。
- 不准大范围重写文章正文，除非用户明确要求。
- 不准删除 `old-site/`、`themes/`、`public/` 历史内容，除非用户明确要求。

## 固定发布流程

继续使用：

```text
本地 Hugo 生成 -> rsync 到仓库根目录 -> commit -> push -> git tag
```

## 版本号规则

`v2026.05.27-05` 及以前为日期流水版本；自 `v0.6.0` 起，angelife 网站改用 SemVer：`vMAJOR.MINOR.PATCH`。

- `MAJOR`：网站架构、发布方式、主题结构发生破坏性变化。
- `MINOR`：新增功能、栏目、搜索、评论、日志系统、内容体系。
- `PATCH`：修复样式、错字、链接、图片、分类、小 bug。

每次提交后必须创建对应 Git tag。

## 搜索与评论规则

- 维护搜索时必须确认 `/search/` 可打开，关键词能命中文章，并有上下文摘要。
- 搜索索引应覆盖 `title`、`summary` / `description`、`content`、`categories`、`tags`、`permalink`。
- 评论系统优先 giscus，不准引入 Disqus。
- giscus 未配置 `repoId` / `categoryId` 时，评论区必须默认隐藏。
- `comments: true` / `comments: false` 应由文章 front matter 控制；旧日志、资料归档、短日课默认不开。

## 每轮收工必须输出

- 版本号。
- 修改目标。
- 修改文件。
- 具体改动。
- 影响页面。
- Hugo 构建结果。
- `rsync` 是否完成。
- commit hash。
- git tag。
- 是否未提交 `_incoming`。
- 线上验证结果。
- 下轮接手提示。

## Git 添加规则

不要使用 `git add .`。

按任务范围精确添加源文件和根目录静态产物。每次提交前必须运行：

```bash
git status --short
git diff --cached --stat
git diff --cached --name-only | rg '^_incoming|^\.github/workflows/'
```

如果发现 `_incoming/` 或未授权 workflow 修改，必须取消暂存并重新检查。
