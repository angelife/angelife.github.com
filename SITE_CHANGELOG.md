# angelife 内部版本日志

本文件用于 AI 接手时查看详细版本演化。公开版本摘要见 `/changelog/` 和 `hugo-site/data/changelog.yaml`。

## v2026.05.27-05｜建立统一 AI 接手规范与项目进度体系

日期：2026-05-27  
执行者：Codex  
发布方式：本地 Hugo 生成 -> rsync 到仓库根目录 -> commit -> push -> git tag  
commit：提交后以 tag `v2026.05.27-05` 指向的 release commit 为准  
tag：v2026.05.27-05

### 本次目标

建立 angelife 网站统一 AI 接手规范、版本日志、每日工作日志、项目总控进度和可回退版本备份体系。

### 修改文件

- `BUILD_HANDOFF.md`
- `AI_WORK_RULES.md`
- `SITE_STYLE_GUIDE.md`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `PROJECT_STATUS.md`
- `hugo-site/data/changelog.yaml`
- `hugo-site/content/changelog.md`
- `hugo-site/content/site-workflow.md`
- `hugo-site/layouts/_default/changelog.html`
- `hugo-site/hugo.toml`

### 具体修改

- 新增建站交接手册，固定本地 Hugo 生成 + rsync 根目录发布流程。
- 新增 AI 工作规则，明确所有 AI 接手前必读文件与禁止事项。
- 新增网站风格规范，明确首页宽屏、文章窄栏、栏目和配图规则。
- 新增内部版本日志、每日工作日志和项目总控进度。
- 新增公开 `/changelog/` 页面和 `hugo-site/data/changelog.yaml`。
- 新增 `/site-workflow/` 建站模式日志页面。
- 顶部导航增加“更新”入口。
- 明确每次修改必须创建 Git tag 作为可回退备份点。

### 构建与发布

- Hugo 构建命令：`hugo --cleanDestinationDir --minify`
- 发布命令：`rsync -av hugo-site/public/ ./`
- 构建结果：Hugo `v0.147.4` 构建通过，174 pages，0 errors。
- rsync：已完成，`hugo-site/public/` 已同步到仓库根目录。

### 线上验证

- `/changelog/`：本地生成产物已验证。
- `/site-workflow/`：本地生成产物已验证。
- 顶部导航“更新”：本地生成产物已验证。

### 遇到的问题

- Git commit hash 无法预先写入被提交文件；最终精确 commit hash 在收工报告中输出，文档内以 tag 作为可回退锚点。
- 用户提供的“网站项目总控流程可视化图.png”当前未在仓库中发现，公开页面先保留 TODO。

### 已解决

- 建立统一治理文档体系。
- 建立公开 changelog 和建站模式说明页。
- 明确回退命令和 tag 备份规则。

### 未完成

- 上传并接入 `hugo-site/static/images/workflow/site-control-map.png`。
- 后续版本继续补充公开更新日志。

### 下次接手注意

先读 `PROJECT_STATUS.md`，再读 `BUILD_HANDOFF.md`、`AI_WORK_RULES.md`、`SITE_STYLE_GUIDE.md`、`SITE_CHANGELOG.md`、`DAILY_WORK_LOG.md`、`hugo-site/data/changelog.yaml`。
