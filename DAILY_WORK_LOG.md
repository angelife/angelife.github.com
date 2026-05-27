# angelife 每日工作日志

## 2026-05-27｜v0.6.0｜改用 SemVer、增强搜索并预留 GitHub 评论

### 今天做了什么

- 将版本号规则从日期流水切换为 SemVer。
- 增强 `/search/`：命中词高亮、上下文摘要、无结果提示、排序优化。
- 搜索索引增加 `description`，继续覆盖标题、摘要、正文、分类、标签和链接。
- 预留 giscus 评论系统，默认隐藏，等待 GitHub Discussions 和 giscus 参数。
- 检查流程图候选路径，未找到图片，`/site-workflow/` 保留 TODO。
- 同步更新公开 changelog、内部日志、每日工作日志和项目总控进度。

### 做到什么程度

功能增强层完成。搜索可作为知识库入口使用，评论系统已具备安全预留结构，SemVer 规则已进入治理文档。

### 遇到什么问题

- 未找到项目总控流程图素材。
- giscus 缺少 `repoId` / `categoryId`，不能正式显示评论区。

### 已解决什么

- 以 `v0.6.0` 作为 SemVer 起点。
- giscus 默认 `enabled = false`，缺少必要参数时不会显示空白评论区。
- 搜索可显示高亮和上下文。

### 未完成什么

- 接入 `hugo-site/static/images/workflow/site-control-map.png`。
- 用户开启 GitHub Discussions、安装/授权 giscus 后，填写 `repoId` / `categoryId` 并按文章开启 `comments: true`。

### 下一个 AI 应该从哪里接手

先读 `PROJECT_STATUS.md`，再按 `AI_WORK_RULES.md` 的必读清单阅读全部交接文件。评论正式启用前，先确认 GitHub Discussions 和 giscus 参数。

### 修改文件

- `BUILD_HANDOFF.md`
- `AI_WORK_RULES.md`
- `SITE_STYLE_GUIDE.md`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `PROJECT_STATUS.md`
- `hugo-site/data/changelog.yaml`
- `hugo-site/content/site-workflow.md`
- `hugo-site/layouts/_default/index.json`
- `hugo-site/layouts/_default/search.html`
- `hugo-site/layouts/partials/comments.html`
- `hugo-site/static/css/angelife-brand.css`
- `hugo-site/hugo.toml`

### 构建状态

Hugo `v0.147.4` 构建通过，174 pages，0 errors。

### 发布状态

已按固定方式执行 `rsync -av hugo-site/public/ ./`，根目录静态产物已更新。

### commit / tag / 版本号

- 版本号：v0.6.0
- commit：提交后以 tag `v0.6.0` 指向的 release commit 为准
- tag：v0.6.0

## 2026-05-27｜v2026.05.27-05｜建立统一 AI 接手规范与项目进度体系

### 今天做了什么

- 建立建站交接手册 `BUILD_HANDOFF.md`。
- 建立统一 AI 工作规则 `AI_WORK_RULES.md`。
- 建立网站风格规范 `SITE_STYLE_GUIDE.md`。
- 建立内部详细版本日志 `SITE_CHANGELOG.md`。
- 建立每日/每轮工作日志 `DAILY_WORK_LOG.md`。
- 建立项目总控进度视图 `PROJECT_STATUS.md`。
- 建立公开更新日志数据 `hugo-site/data/changelog.yaml`。
- 建立公开 `/changelog/` 页面。
- 建立公开 `/site-workflow/` 建站模式日志页面。
- 顶部导航增加“更新”入口。

### 做到什么程度

治理层第一版完成，可供下一个 AI 接手时快速理解发布方式、禁止事项、风格边界、当前进度和回退方法。

### 遇到什么问题

- Git commit hash 无法预先写入被提交文件。
- 尚未找到用户提到的“网站项目总控流程可视化图.png”。

### 已解决什么

- 以 Git tag 作为文档内稳定可回退锚点。
- `/site-workflow/` 先保留流程图 TODO，不阻塞构建和发布。

### 未完成什么

- 补充并接入 `hugo-site/static/images/workflow/site-control-map.png`。
- 后续版本继续细化公开 changelog 展示。

### 下一个 AI 应该从哪里接手

先读 `PROJECT_STATUS.md`，再按 `AI_WORK_RULES.md` 的必读清单阅读全部交接文件。

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

### 构建状态

Hugo `v0.147.4` 构建通过，174 pages，0 errors。

### 发布状态

已按固定方式执行 `rsync -av hugo-site/public/ ./`，根目录静态产物已更新。

### commit / tag / 版本号

- 版本号：v2026.05.27-05
- commit：提交后以 tag `v2026.05.27-05` 指向的 release commit 为准
- tag：v2026.05.27-05
