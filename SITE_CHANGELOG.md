# angelife 内部版本日志

本文件用于 AI 接手时查看详细版本演化。公开版本摘要见 `/changelog/` 和 `hugo-site/data/changelog.yaml`。

## v0.6.5｜发布高速公路与泥巴地文章

日期：2026-05-28  
执行者：Reasonix  
发布方式：本地 Hugo 生成 -> rsync 到仓库根目录 -> commit -> push -> git tag  
commit：提交后以 tag `v0.6.5` 指向的 release commit 为准  
tag：v0.6.5

### 本次目标

- 将用户提供的《高速公路与泥巴地：AI时代的本土化生存》整理为 Hugo 正式文章。
- 按既定流程构建站点、同步根目录静态产物并发布。
- 同步更新公开 changelog、内部日志、每日工作日志、交接日志和项目状态文件。

### 修改文件

- `hugo-site/content/posts/highway-and-muddy-road-ai-localization/index.md`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `PROJECT_STATUS.md`
- `BUILD_HANDOFF.md`
- `hugo-site/data/changelog.yaml`

### 具体修改

- 新增正式文章《高速公路与泥巴地：AI时代的本土化生存》。
- 文章 slug：`highway-and-muddy-road-ai-localization`。
- 分类：`AI时代`。
- 标签：`AI工作流`、`本土化`、`国产替代`、`判断力`、`系统韧性`、`不失正见`。
- 封面状态：`cover_status: prompt_ready`，待真实封面图生成后接入。

### 构建与发布

- Hugo 构建命令：`hugo --source hugo-site --destination hugo-site/public --cleanDestinationDir --minify`
- 构建结果：Hugo `v0.147.4` 构建通过，213 pages，0 errors。
- rsync：已完成，`hugo-site/public/` 已同步到仓库根目录。

### 线上验证

- `/posts/highway-and-muddy-road-ai-localization/`：本地静态产物已生成并验证目标路径。
- `/changelog/`：本地生成产物将包含 `v0.6.5`。

### 遇到的问题

- 无。

### 已解决

- 无。

### 未完成

- 正式 commit、push、tag 和线上验证需在后续步骤完成后补入。
- 封面图未接入，`cover_status: prompt_ready`。

### 下次接手注意

先读 `PROJECT_STATUS.md`，再读 `BUILD_HANDOFF.md`、`AI_WORK_RULES.md`、`SITE_STYLE_GUIDE.md`、`SITE_CHANGELOG.md`、`DAILY_WORK_LOG.md`、`hugo-site/data/changelog.yaml`。继续使用本地 Hugo 生成 + rsync 根目录发布，不要切 GitHub Actions，不要提交 `_incoming/`。

## v0.6.4｜接入付费墙与迷雾墙文章封面图

日期：2026-05-28  
执行者：Reasonix  
发布方式：本地 Hugo 生成 -> rsync 到仓库根目录 -> commit -> push -> git tag  
commit：提交后以 tag `v0.6.4` 指向的 release commit 为准  
tag：v0.6.4

### 本次目标

- 将 ChatGPT 生成的封面图接入《付费墙与迷雾墙：AI时代真正昂贵的是判断》文章。
- 拷贝封面图到 `hugo-site/static/images/posts/paywall-and-mist-wall/cover.png`。
- 更新文章 front matter，加入 `cover` 字段。
- 更新视觉资产记录为 `cover_status: image_ready`。
- 同步更新所有日志和治理文件。

### 修改文件

- `hugo-site/static/images/posts/paywall-and-mist-wall/cover.png`
- `hugo-site/content/posts/paywall-and-mist-wall/index.md`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `PROJECT_STATUS.md`
- `BUILD_HANDOFF.md`
- `hugo-site/data/changelog.yaml`

### 具体修改

- 新增封面图至 `static/images/posts/paywall-and-mist-wall/cover.png`。
- 文章 `index.md` 加入 `cover` front matter：`image: "/images/posts/paywall-and-mist-wall/cover.png"`。
- 视觉资产状态从 `prompt_ready` 更新为 `image_ready`。

### 构建与发布

- Hugo 构建命令：`hugo --source hugo-site --destination hugo-site/public --cleanDestinationDir --minify`
- 构建结果：Hugo `v0.147.4` 构建通过，206 pages，0 errors。静态文件 356 → 357（封面图）。
- rsync：已完成，`hugo-site/public/` 已同步到仓库根目录。

### 线上验证

- `/posts/paywall-and-mist-wall/`：封面图已接入，静态产物验证通过。
- 封面图 URL：`/images/posts/paywall-and-mist-wall/cover.png`。

### 遇到的问题

- `~` 在 shell 命令中未展开，改用完整路径 `/Users/macos/Downloads/` 后正常。

### 已解决

- 封面图已成功接入文章。

### 未完成

- 正式 commit、push、tag 和线上验证需在后续步骤完成后补入。

### 下次接手注意

先读 `PROJECT_STATUS.md`，再读 `BUILD_HANDOFF.md`、`AI_WORK_RULES.md`、`SITE_STYLE_GUIDE.md`、`SITE_CHANGELOG.md`、`DAILY_WORK_LOG.md`、`hugo-site/data/changelog.yaml`。继续使用本地 Hugo 生成 + rsync 根目录发布，不要切 GitHub Actions，不要提交 `_incoming/`。

## v0.6.3｜发布付费墙与迷雾墙文章

日期：2026-05-28  
执行者：Reasonix  
发布方式：本地 Hugo 生成 -> rsync 到仓库根目录 -> commit -> push -> git tag  
commit：提交后以 tag `v0.6.3` 指向的 release commit 为准  
tag：v0.6.3

### 本次目标

- 将用户提供的《付费墙与迷雾墙：AI时代真正昂贵的是判断》整理为 Hugo 正式文章。
- 按既定流程构建站点、同步根目录静态产物并发布。
- 同步更新公开 changelog、内部日志、每日工作日志、交接日志和项目状态文件。

### 修改文件

- `hugo-site/content/posts/paywall-and-mist-wall/index.md`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `PROJECT_STATUS.md`
- `BUILD_HANDOFF.md`
- `hugo-site/CODEX_HANDOFF.md`
- `hugo-site/data/changelog.yaml`

### 具体修改

- 新增正式文章《付费墙与迷雾墙：AI时代真正昂贵的是判断》。
- 文章 slug：`paywall-and-mist-wall`。
- 分类：`AI时代`。
- 标签：`AI写作`、`判断力`、`规则意识`、`现实规则`、`不失正见`。
- 使用本地 Hugo 构建 + rsync 根目录发布。

### 构建与发布

- Hugo 构建命令：`hugo --source hugo-site --destination hugo-site/public --cleanDestinationDir --minify`
- 发布命令：`rsync -a --delete ... hugo-site/public/ ./`
- 构建结果：Hugo `v0.147.4` 构建通过，206 pages，0 errors。
- rsync：已完成，`hugo-site/public/` 已同步到仓库根目录。

### 线上验证

- `/posts/paywall-and-mist-wall/`：本地静态产物已生成并验证目标路径。
- `/changelog/`：本地生成产物将包含 `v0.6.3`。

### 遇到的问题

- 无。

### 已解决

- 无。

### 未完成

- 正式 commit、push、tag 和线上验证需在后续步骤完成后补入。

### 下次接手注意

先读 `PROJECT_STATUS.md`，再读 `BUILD_HANDOFF.md`、`AI_WORK_RULES.md`、`SITE_STYLE_GUIDE.md`、`SITE_CHANGELOG.md`、`DAILY_WORK_LOG.md`、`hugo-site/data/changelog.yaml`。继续使用本地 Hugo 生成 + rsync 根目录发布，不要切 GitHub Actions，不要提交 `_incoming/`。

## v0.6.2｜发布 AI 时代经验瓶颈文章

日期：2026-05-28  
执行者：Codex  
发布方式：本地 Hugo 生成 -> rsync 到仓库根目录 -> commit -> push -> git tag  
commit：提交后以 tag `v0.6.2` 指向的 release commit 为准  
tag：v0.6.2

### 本次目标

- 将用户提供的《AI时代，经验才是最大的瓶颈》整理为 Hugo 正式文章。
- 按既定流程生成封面图、构建站点、同步根目录静态产物并发布。
- 同步更新公开 changelog、内部日志、每日工作日志、交接日志和项目状态文件。

### 修改文件

- `BUILD_HANDOFF.md`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `PROJECT_STATUS.md`
- `hugo-site/CODEX_HANDOFF.md`
- `hugo-site/data/changelog.yaml`
- `hugo-site/content/posts/ai-era-experience-is-the-bottleneck/index.md`
- `hugo-site/content/posts/ai-era-experience-is-the-bottleneck/cover.png`

### 具体修改

- 新增正式文章《AI时代，经验才是最大的瓶颈》。
- 文章 slug：`ai-era-experience-is-the-bottleneck`。
- 分类：`火·AI`、`AI时代`。
- 标签：`AI`、`经验`、`判断力`、`信息筛选`、`方法论`、`个人知识系统`。
- 使用 imagegen 生成克制的编辑类封面图，并复制到文章 bundle 内。
- 按当前 Hugo 文章格式使用 front matter 渲染标题，正文不重复插入一级标题。

### 构建与发布

- Hugo 构建命令：`./publish.sh`
- 发布命令：`./publish.sh` 内执行 `rsync -a --delete hugo-site/public/ ./`
- 构建结果：Hugo `v0.147.4` 构建通过，192 pages，0 errors。
- rsync：已完成，`hugo-site/public/` 已同步到仓库根目录。

### 线上验证

- `/posts/ai-era-experience-is-the-bottleneck/`：本地静态产物已生成并验证目标路径。
- `/changelog/`：本地生成产物已包含 `v0.6.2`。

### 遇到的问题

- 当前 Codex 工作目录不是 angelife 仓库，实际仓库位于 `/Users/macos/angelife.github.com`。
- 实际仓库不在当前 writable sandbox root 内，写入时按权限流程执行。
- 文章初始发布时间晚于本机当前时间，Hugo 默认不发布未来文章；已将发布时间调为 `2026-05-28T12:40:00+08:00` 后重新构建。

### 已解决

- 已定位正确仓库和 Hugo 源站目录。
- 已确认当前版本号规则为 SemVer，本轮使用 `v0.6.2`。
- 已按文章页规范避免正文重复一级标题。

### 未完成

- 正式 commit、push、tag 和线上验证需在提交后完成。

### 下次接手注意

先读 `PROJECT_STATUS.md`，再读 `BUILD_HANDOFF.md`、`AI_WORK_RULES.md`、`SITE_STYLE_GUIDE.md`、`SITE_CHANGELOG.md`、`DAILY_WORK_LOG.md`、`hugo-site/data/changelog.yaml`。继续使用本地 Hugo 生成 + rsync 根目录发布，不要切 GitHub Actions，不要提交 `_incoming/`。

## v0.6.1｜发布 ChatGPT 高反馈系统文章并保护根目录治理文档

日期：2026-05-28  
执行者：Codex  
发布方式：本地 Hugo 生成 -> rsync 到仓库根目录 -> commit -> push -> git tag  
commit：提交后以 tag `v0.6.1` 指向的 release commit 为准  
tag：v0.6.1

### 本次目标

- 将用户提供的 ChatGPT 高反馈系统文章整理为 Hugo 正式文章。
- 按既定流程生成封面图、构建站点、同步根目录静态产物并发布。
- 修正 `publish.sh` 排除清单，避免 `rsync --delete` 删除根目录治理文档和站点校验 txt 文件。
- 同步更新公开 changelog、内部日志、每日工作日志、交接日志和项目状态文件。

### 修改文件

- `BUILD_HANDOFF.md`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `PROJECT_STATUS.md`
- `publish.sh`
- `hugo-site/CODEX_HANDOFF.md`
- `hugo-site/data/changelog.yaml`
- `hugo-site/content/posts/chatgpt-daily-progress-feedback-system/index.md`
- `hugo-site/content/posts/chatgpt-daily-progress-feedback-system/cover.png`

### 具体修改

- 新增正式文章《和 ChatGPT 在一起，我重新找回了天天进步的感觉》。
- 文章 slug：`chatgpt-daily-progress-feedback-system`。
- 分类：`火·AI`、`日课`、`AI时代`、`个人知识资产`。
- 标签：`ChatGPT`、`AI陪练`、`个人成长`、`高反馈环境`、`知识系统`。
- 使用 imagegen 生成克制的编辑类封面图，并复制到文章 bundle 内。
- `publish.sh` 增加根目录治理文档和 `*.txt` 排除项。

### 构建与发布

- Hugo 构建命令：`./publish.sh`
- 发布命令：`./publish.sh` 内执行 `rsync -a --delete hugo-site/public/ ./`
- 构建结果：Hugo `v0.147.4` 构建通过，183 pages，0 errors。
- rsync：已完成，`hugo-site/public/` 已同步到仓库根目录。

### 线上验证

- `/posts/chatgpt-daily-progress-feedback-system/`：本地静态产物已生成并验证目标路径。
- `/changelog/`：本地生成产物已包含 `v0.6.1`。

### 遇到的问题

- 当前 Codex 工作目录不是 angelife 仓库，实际仓库位于 `/Users/macos/angelife.github.com`。
- 原 `publish.sh` 排除清单不完整，`rsync --delete` 会删除根目录治理文档；本轮已修复脚本并恢复文档。
- 文章初始发布时间晚于本机当前时间，Hugo 默认不发布未来文章；已将发布时间调为 `2026-05-28T12:20:00+08:00` 后重新构建。

### 已解决

- 已定位正确仓库和 Hugo 源站目录。
- 已按现有 SemVer 规范选择 `v0.6.1`。
- 已保护根目录治理文档和站点校验 txt 文件。

### 未完成

- 正式 commit、push、tag 和线上验证需在提交后完成。

### 下次接手注意

先读 `PROJECT_STATUS.md`，再读 `BUILD_HANDOFF.md`、`AI_WORK_RULES.md`、`SITE_STYLE_GUIDE.md`、`SITE_CHANGELOG.md`、`DAILY_WORK_LOG.md`、`hugo-site/data/changelog.yaml`。继续使用本地 Hugo 生成 + rsync 根目录发布，不要切 GitHub Actions，不要提交 `_incoming/`。

## v0.6.0｜改用 SemVer、增强搜索并预留 GitHub 评论

日期：2026-05-27  
执行者：Codex  
发布方式：本地 Hugo 生成 -> rsync 到仓库根目录 -> commit -> push -> git tag  
commit：提交后以 tag `v0.6.0` 指向的 release commit 为准  
tag：v0.6.0

### 本次目标

- 将版本号从日期流水切换为 SemVer。
- 增强站内搜索，加入命中词高亮、上下文摘要和更合理排序。
- 预留 giscus 评论系统，未来可通过 GitHub Discussions 启用文章评论。
- 尝试补上 `/site-workflow/` 的项目总控流程图。
- 同步更新公开 changelog、内部日志、每日工作日志和项目总控进度。

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

### 具体修改

- 写明 `v2026.05.27-05` 及以前为日期流水版本，自 `v0.6.0` 起改用 SemVer：`vMAJOR.MINOR.PATCH`。
- 搜索索引增加 `description` 字段，搜索范围覆盖标题、摘要、正文、分类、标签和链接。
- 搜索结果支持 `<mark>` 高亮、命中上下文摘要、无结果提示和更合理排序。
- 新增 `layouts/partials/comments.html`，按 giscus 参数和页面类型安全渲染评论。
- 在 `hugo.toml` 预留 `[params.giscus]`，默认 `enabled = false`。
- 在治理文档和 `/site-workflow/` 中写入评论启用条件和维护规则。

### 构建与发布

- Hugo 构建命令：`hugo --cleanDestinationDir --minify`
- 发布命令：`rsync -av hugo-site/public/ ./`
- 构建结果：Hugo `v0.147.4` 构建通过，174 pages，0 errors。
- rsync：已完成，`hugo-site/public/` 已同步到仓库根目录。

### 线上验证

- `/search/`：本地静态产物已验证，测试关键词均命中新文章。
- `/changelog/`：本地生成产物已验证。
- `/site-workflow/`：本地生成产物已验证。

### 遇到的问题

- 本轮未在指定位置找到 `site-control-map.png` 或 `网站项目总控流程可视化图.png`，因此 `/site-workflow/` 继续保留流程图 TODO。
- giscus 需要 GitHub Discussions、giscus 授权、`repoId` 和 `categoryId`，本轮只能安全预留，不能正式显示。

### 已解决

- SemVer 规则已写入治理文档和公开 changelog 数据。
- 搜索体验已增强。
- 评论系统已有可配置、可隐藏的 giscus 预留实现。

### 未完成

- 上传并接入 `hugo-site/static/images/workflow/site-control-map.png`。
- 正式启用 GitHub Discussions 和 giscus，并填写 `repoId` / `categoryId`。

### 下次接手注意

先读 `PROJECT_STATUS.md`，再读 `BUILD_HANDOFF.md`、`AI_WORK_RULES.md`、`SITE_STYLE_GUIDE.md`、`SITE_CHANGELOG.md`、`DAILY_WORK_LOG.md`、`hugo-site/data/changelog.yaml`。不要切换发布方式，不要提交 `_incoming/`。

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
