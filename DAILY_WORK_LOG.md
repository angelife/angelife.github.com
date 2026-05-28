# angelife 每日工作日志

## 2026-05-28｜v0.6.14｜固化 Kindle 阅读模式治理规则

### 今天做了什么

- 治理固化轮，无模板/CSS/内容变更。
- AI_WORK_RULES.md：新增 Kindle 不可破坏规则 + 验收强制要求。
- SITE_STYLE_GUIDE.md：新增 Kindle 阅读模式独立小节（5 条核心原则）。
- BUILD_HANDOFF.md：新增 Kindle 接手交接确认。
- PROJECT_STATUS.md、SITE_CHANGELOG.md、DAILY_WORK_LOG.md、changelog.yaml 同步更新。

### 修改文件

- `AI_WORK_RULES.md`
- `SITE_STYLE_GUIDE.md`
- `BUILD_HANDOFF.md`
- `PROJECT_STATUS.md`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `hugo-site/data/changelog.yaml`

### 构建状态

Hugo `v0.147.4` 构建通过，223 pages，0 errors。

### 版本号

v0.6.14，tag v0.6.14

### 验收

- Kindle 目录页：无导航词 ✓（此前已固化）
- Kindle 文章页：无导航词和 footer ✓（此前已固化）
- 普通首页：导航完整保留 ✓

## 2026-05-28｜v0.6.13｜修复 Kindle 文章页外层 PaperMod 壳

### 今天做了什么

- 根因：baseof.html 用 `hasPrefix .RelPermalink "/kindle/"` 判断 Kindle 页面，单条件在 KindlePage outputFormat 下偶发不匹配。
- 修复：改为 `$isKindle` 变量，三重判断（RelPermalink / Section / Layout），统一控制 body class、header、footer 渲染。
- 验证：Kindle 文章页和目录页均无导航词和 Powered by。

### 修改文件

- `hugo-site/layouts/_default/baseof.html`
- `SITE_CHANGELOG.md`、`DAILY_WORK_LOG.md`、`PROJECT_STATUS.md`、`BUILD_HANDOFF.md`、`hugo-site/data/changelog.yaml`

### 构建状态

Hugo `v0.147.4` 构建通过，223 pages，0 errors。

### commit / tag / 版本号

- 版本号：v0.6.13
- tag：v0.6.13

## 2026-05-28｜v0.6.12｜重新同步 Kindle 线上静态产物

### 今天做了什么

- 本地 Kindle 模板已正确，但线上 GitHub Pages 有导航残留。
- 执行 `hugo --gc --cleanDestinationDir --minify` 强制清洁构建。
- 全量 rsync 覆盖根目录静态产物。
- 排除 `.reasonix/` 避免 rsync 警告。
- 重新 push 确保线上部署的是完全清洁的 Kindle 产物。

### 验收结果

- Kindle 目录/文章页：无导航词、无 Powered by、无 id=menu ✓
- 普通页面：导航完整保留 ✓

### 修改文件

- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `PROJECT_STATUS.md`
- `BUILD_HANDOFF.md`
- `hugo-site/data/changelog.yaml`

### 构建状态

Hugo `v0.147.4` 构建通过，223 pages，0 errors。

### commit / tag / 版本号

- 版本号：v0.6.12
- tag：v0.6.12

## 2026-05-28｜v0.6.11｜Kindle/手机自动跳转 + 双版本规则固化

### 今天做了什么

- 创建 `reader-redirect.js`：Kindle 设备/手机用户自动跳转 Kindle 阅读版。
- 条件加载脚本：仅非 Kindle 页面加载，Kindle 页面不重复加载。
- `?normal=1` 出口：Kindle 页面可返回图文版，记录偏好后不再自动跳走。
- `?reader=1`/`?kindle=1` 入口：可强制进入阅读模式。
- 更新 Kindle 模板页脚：文章页增加「本文图文版」链接，目录页增加「返回首页图文版」。
- 固化双版本发布规则到 `AI_WORK_RULES.md`、`SITE_STYLE_GUIDE.md`、`BUILD_HANDOFF.md`。
- 更新公开 changelog、内部详细日志、项目状态。

### 验收结果

- Kindle 页面无普通导航 ✓
- 普通页面保留完整导航 ✓
- JS 已部署到 /js/reader-redirect.js ✓
- 正常页面已加载脚本 ✓
- /kindle/ 和 /kindle/posts/<slug>/ 均可打开 ✓

### 修改文件

- 新增：`hugo-site/static/js/reader-redirect.js`
- 修改：`hugo-site/layouts/partials/extend_head.html`
- 修改：`hugo-site/layouts/_default/single.kindle.html`
- 修改：`hugo-site/layouts/kindle/list.html`
- 修改：`AI_WORK_RULES.md`、`SITE_STYLE_GUIDE.md`、`BUILD_HANDOFF.md`、`PROJECT_STATUS.md`
- 修改：`SITE_CHANGELOG.md`、`DAILY_WORK_LOG.md`、`hugo-site/data/changelog.yaml`

### 构建状态

Hugo `v0.147.4` 构建通过，223 pages，0 errors。

### commit / tag / 版本号

- 版本号：v0.6.11
- tag：v0.6.11

## 2026-05-28｜v0.6.10｜Kindle 阅读模式细化：模板层移除导航

### 今天做了什么

- 修改 `baseof.html`：Kindle 页面跳过 PaperMod 完整导航和页脚渲染。
- Kindle 文章页模板和目录页模板加入简约顶栏：`安知生 angelife ／ Kindle 阅读版`。
- 页脚改为纯文字极简版权 + 返回链接。
- 清理 `kindle.css`：删除不再使用的 `.footer` 和重复的 `.kindle-footer` 样式。

### 验收结果

- Kindle 目录页和文章页源代码中无 `id=menu`、无 `nav`、无导航词。
- 普通页面导航完整保留。

### 修改文件

- `hugo-site/layouts/_default/baseof.html`
- `hugo-site/layouts/_default/single.kindle.html`
- `hugo-site/layouts/kindle/list.html`
- `hugo-site/static/css/kindle.css`
- 日志/治理文件

### 构建状态

Hugo `v0.147.4` 构建通过，223 pages，0 errors。

### commit / tag / 版本号

- 版本号：v0.6.10
- tag：v0.6.10

## 2026-05-28｜v0.6.9｜重构为独立 Kindle 电子书阅读模式

### 今天做了什么

- 将 Kindle 模式从"网页兼容"重构为"独立电子书阅读模式"。
- 使用 Hugo output format 为每篇文章自动生成独立 Kindle 文章页 `/kindle/posts/<slug>/`。
- 创建 `layouts/_default/single.kindle.html`：纯文字、无封面、无标签、无分享、无评论，只有标题+日期+正文+上一篇/下一篇。
- 创建 `layouts/kindle/list.html`：纯文字文章目录，链接到 Kindle 独立文章页。
- 创建 `layouts/_default/baseof.html`：通过 `hasPrefix .RelPermalink "/kindle/"` 自动注入 `body.kindle-mode`。
- 完全重写 `static/css/kindle.css`：使用 `body.kindle-mode` 选择器，serif 字体，强制去掉所有装饰。
- 更新 `hugo.toml`、`content/posts/_index.md` cascade 配置。

### 做到什么程度

Kindle 阅读模式从"微调兼容"变成了"独立电子书入口"：
- 目录页像 Kindle 书架
- 文章页像纯电子书正文
- 所有 Kindle 页面自动带 `kindle-mode` class

### 遇到什么问题

- `.OutputFormat.Name` 在 Hugo v0.147 的某些 page 类型中不可用，改用 `.RelPermalink` 前缀判断。
- `layouts/section/kindle.html` 未被 Hugo 识别，移至 `layouts/kindle/list.html` 后正常。

### 已解决什么

- 独立 Kindle 文章页正常渲染，目录链接指向 Kindle 文章页。

### 未完成什么

- 无。

### 修改文件

- 新增：`hugo-site/layouts/_default/single.kindle.html`
- 新增：`hugo-site/layouts/kindle/list.html`
- 新增：`hugo-site/layouts/_default/baseof.html`
- 修改：`hugo-site/static/css/kindle.css`
- 修改：`hugo-site/content/kindle/_index.md`
- 修改：`hugo-site/content/posts/_index.md`
- 修改：`hugo-site/hugo.toml`
- 修改：`SITE_CHANGELOG.md`、`DAILY_WORK_LOG.md`、`PROJECT_STATUS.md`、`BUILD_HANDOFF.md`、`hugo-site/data/changelog.yaml`

### 构建状态

Hugo `v0.147.4` 构建通过，223 pages，0 errors。

### 发布状态

已按固定方式执行 rsync，根目录静态产物已更新。

### commit / tag / 版本号

- 版本号：v0.6.9
- commit：提交后以 tag `v0.6.9` 指向的 release commit 为准
- tag：v0.6.9

## 2026-05-28｜v0.6.8｜新增 Kindle Paperwhite 阅读模式

### 今天做了什么

- 为 angelife 网站增加 Kindle KPW5 / 电子墨水屏阅读优化模式。
- 新增 `/kindle/` 入口：文章列表按日期倒序，无封面大图，黑白高对比。
- 创建 `hugo-site/static/css/kindle.css`，通过 `@media (monochrome)` 条件激活全站 Kindle 优化。
- 创建 `hugo-site/layouts/section/kindle.html` 作为 `/kindle/` 页面模板。
- 创建 `hugo-site/content/kindle/_index.md` 内容页。
- 在 `hugo.toml` 主导航增加「Kindle版」条目。
- 在 `extend_head.html` 中加载 `kindle.css`。

### 做到什么程度

Kindle 阅读模式已创建并发布。普通桌面端、手机端不受影响。

### 遇到什么问题

- 最初将模板放在 `layouts/page/` 目录，但 `content/kindle/_index.md` 是 section 类型。将模板移到 `layouts/section/` 后正常渲染。

### 已解决什么

- Kindle 页面已正常生成，包含 9 篇文章列表。

### 未完成什么

- 无。

### 修改文件

- 新增：`hugo-site/content/kindle/_index.md`
- 新增：`hugo-site/layouts/section/kindle.html`
- 新增：`hugo-site/static/css/kindle.css`
- 修改：`hugo-site/hugo.toml`
- 修改：`hugo-site/layouts/partials/extend_head.html`
- 修改：`SITE_CHANGELOG.md`
- 修改：`DAILY_WORK_LOG.md`
- 修改：`PROJECT_STATUS.md`
- 修改：`BUILD_HANDOFF.md`
- 修改：`hugo-site/data/changelog.yaml`

### 构建状态

Hugo `v0.147.4` 构建通过，215 pages，0 errors。

### 发布状态

已按固定方式执行 rsync，根目录静态产物已更新。

### commit / tag / 版本号

- 版本号：v0.6.8
- commit：提交后以 tag `v0.6.8` 指向的 release commit 为准
- tag：v0.6.8

## 2026-05-28｜v0.6.7｜发布机器执行文章并修复 404

### 今天做了什么

- 将长期滞留于 untracked 状态的文章《机器执行，经验指挥：AI 时代真正昂贵的东西》正式纳入 git 跟踪并发布上线。
- 修复线上 `/posts/ai-machine-executes-experience-commands/` 404 问题。
- 文章源文件 front matter 已确认：draft: false，slug、title、categories、tags 均正常。
- 封面状态记录为 `cover_status: prompt_ready`，未写入 front matter cover 字段。
- 更新公开 changelog、内部详细日志、每日工作日志、交接日志和项目状态文件。

### 做到什么程度

文章已正式发布，线上 404 已修复。

### 遇到什么问题

- 文章源文件长期存在于 content 目录中，但从未 `git add` 和 `git commit`，导致 Hugo 构建时包含该页，但 GitHub Pages 部署的 git 仓库中不存在该文件。

### 已解决什么

- 已将该文章纳入 git 跟踪，按既定流程完成构建、rsync、commit、tag、push。

### 未完成什么

- 封面图待 ChatGPT 生成后接入。

### 下一个 AI 应该从哪里接手

先读 `PROJECT_STATUS.md` 和 `AI_WORK_RULES.md`。本轮文章已正式发布，`_incoming/` 不纳入提交范围。

### 修改文件

- `hugo-site/content/posts/ai-machine-executes-experience-commands/index.md`
- `posts/ai-machine-executes-experience-commands/index.html`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `PROJECT_STATUS.md`
- `BUILD_HANDOFF.md`
- `hugo-site/data/changelog.yaml`

### 构建状态

Hugo `v0.147.4` 构建通过，213 pages，0 errors。

### 发布状态

已按固定方式执行 rsync，根目录静态产物已更新。`_incoming/` 不纳入提交范围。

### commit / tag / 版本号

- 版本号：v0.6.7
- commit：提交后以 tag `v0.6.7` 指向的 release commit 为准
- tag：v0.6.7

## 2026-05-28｜v0.6.6｜接入高速公路与泥巴地文章封面图

### 今天做了什么

- 将 ChatGPT 生成的封面图接入已发布的《高速公路与泥巴地：AI时代的本土化生存》。
- 拷贝封面图到 `hugo-site/static/images/posts/highway-and-muddy-road-ai-localization/cover.png`。
- 更新 front matter 接入 `cover` 字段：图片路径、alt 文本、caption。
- 更新视觉资产记录为 `cover_status: image_ready`。
- 更新公开 changelog、内部详细日志、每日工作日志、交接日志和项目状态文件。

### 做到什么程度

文章封面图已正式接入，作为 `v0.6.6` 发布。

### 遇到什么问题

- 无。

### 已解决什么

- 封面图已成功部署，Hugo 构建 213 pages, 0 errors。

### 未完成什么

- commit、push、tag 和线上验证在后续步骤完成后补入最终收工报告。

### 下一个 AI 应该从哪里接手

先读 `PROJECT_STATUS.md` 和 `AI_WORK_RULES.md`。本轮封面图已接入发布，`_incoming/` 不纳入提交范围。

### 修改文件

- `hugo-site/static/images/posts/highway-and-muddy-road-ai-localization/cover.png`
- `hugo-site/content/posts/highway-and-muddy-road-ai-localization/index.md`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `PROJECT_STATUS.md`
- `BUILD_HANDOFF.md`
- `hugo-site/data/changelog.yaml`

### 构建状态

Hugo `v0.147.4` 构建通过，213 pages，0 errors。静态文件 358。

### 发布状态

已按固定方式执行 rsync，根目录静态产物已更新。

### commit / tag / 版本号

- 版本号：v0.6.6
- commit：提交后以 tag `v0.6.6` 指向的 release commit 为准
- tag：v0.6.6

## 2026-05-28｜v0.6.5｜发布高速公路与泥巴地文章

## 2026-05-28｜v0.6.4｜接入付费墙与迷雾墙文章封面图

### 今天做了什么

- 将 ChatGPT 生成的封面图接入已发布的《付费墙与迷雾墙：AI时代真正昂贵的是判断》。
- 拷贝封面图到 `hugo-site/static/images/posts/paywall-and-mist-wall/cover.png`。
- 更新 front matter 接入 `cover` 字段：图片路径、alt 文本、caption。
- 更新视觉资产记录为 `cover_status: image_ready`。
- 更新公开 changelog、内部详细日志、每日工作日志、交接日志和项目状态文件。

### 做到什么程度

文章封面图已正式接入，作为 `v0.6.4` 发布。

### 遇到什么问题

- `~` 在 run_command 中未展开为 home 目录，改用完整路径 `/Users/macos/Downloads/` 后正常。

### 已解决什么

- 封面图已成功部署，Hugo 构建 206 pages, 0 errors。

### 未完成什么

- commit、push、tag 和线上验证在后续步骤完成后补入最终收工报告。

### 下一个 AI 应该从哪里接手

先读 `PROJECT_STATUS.md` 和 `AI_WORK_RULES.md`。本轮封面图已接入发布，`_incoming/` 不纳入提交范围。

### 修改文件

- `hugo-site/static/images/posts/paywall-and-mist-wall/cover.png`
- `hugo-site/content/posts/paywall-and-mist-wall/index.md`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `PROJECT_STATUS.md`
- `BUILD_HANDOFF.md`
- `hugo-site/data/changelog.yaml`

### 构建状态

Hugo `v0.147.4` 构建通过，206 pages，0 errors。静态文件 357。

### 发布状态

已按固定方式执行 rsync，根目录静态产物已更新。

### commit / tag / 版本号

- 版本号：v0.6.4
- commit：提交后以 tag `v0.6.4` 指向的 release commit 为准
- tag：v0.6.4

## 2026-05-28｜v0.6.3｜发布付费墙与迷雾墙文章

### 今天做了什么

- 将用户提供的《付费墙与迷雾墙：AI时代真正昂贵的是判断》整理为 Hugo 正式文章。
- 按 slug `paywall-and-mist-wall` 创建文章 bundle。
- 归入 `AI时代`。
- 添加 `AI写作`、`判断力`、`规则意识`、`现实规则`、`不失正见` 标签。
- 更新公开 changelog、内部详细日志、每日工作日志、交接日志和项目状态文件。

### 做到什么程度

文章已进入正式发布流，作为公开长文发布，不放入 `_incoming/`。

### 遇到什么问题

- 无。

### 已解决什么

- 按既定流程完成构建、rsync、日志更新。

### 未完成什么

- commit、push、tag 和线上验证在后续步骤完成后补入最终收工报告。

### 下一个 AI 应该从哪里接手

先读 `PROJECT_STATUS.md` 和 `AI_WORK_RULES.md`。本轮文章已经正式发布，不需要再从 `_incoming/` 处理。

### 修改文件

- `hugo-site/content/posts/paywall-and-mist-wall/index.md`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `PROJECT_STATUS.md`
- `BUILD_HANDOFF.md`
- `hugo-site/CODEX_HANDOFF.md`
- `hugo-site/data/changelog.yaml`

### 构建状态

Hugo `v0.147.4` 构建通过，206 pages，0 errors。

### 发布状态

已按固定方式执行 rsync，根目录静态产物已更新。`_incoming/` 不纳入提交范围。

### commit / tag / 版本号

- 版本号：v0.6.3
- commit：提交后以 tag `v0.6.3` 指向的 release commit 为准
- tag：v0.6.3

## 2026-05-28｜v0.6.2｜发布 AI 时代经验瓶颈文章

### 今天做了什么

- 将用户提供的《AI时代，经验才是最大的瓶颈》整理为 Hugo 正式文章。
- 按建议 slug 创建文章 bundle：`ai-era-experience-is-the-bottleneck`。
- 归入 `火·AI`、`AI时代`。
- 添加 `AI`、`经验`、`判断力`、`信息筛选`、`方法论`、`个人知识系统` 标签。
- 使用 imagegen 生成并接入文章封面图。
- 更新公开 changelog、内部详细日志、每日工作日志、交接日志和项目状态文件。

### 做到什么程度

文章已进入正式发布流，作为公开长文发布，不放入 `_incoming/`，也不作为未发布储备稿处理。

### 遇到什么问题

- 默认 Codex 工作目录为空且不是 Git 仓库，需要重新定位到 `/Users/macos/angelife.github.com`。
- 实际仓库不在当前 writable sandbox root 内，写入时需要按权限流程执行。
- 文章初始发布时间写在本机当前时间之后，Hugo 未将其输出；已改为 `2026-05-28T12:40:00+08:00`。

### 已解决什么

- 已确认 angelife 仓库、Hugo 源站、发布脚本、版本规则和日志要求。
- 已按 SemVer 规则生成本轮版本号 `v0.6.2`。
- 已按当前文章格式保留 front matter 标题，正文不重复插入一级标题。

### 未完成什么

- commit、push、tag 和线上验证在后续步骤完成后补入最终收工报告。

### 下一个 AI 应该从哪里接手

先读 `PROJECT_STATUS.md` 和 `AI_WORK_RULES.md`。本轮文章已经正式发布，不需要再从 `_incoming/` 处理。

### 修改文件

- `BUILD_HANDOFF.md`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `PROJECT_STATUS.md`
- `hugo-site/CODEX_HANDOFF.md`
- `hugo-site/data/changelog.yaml`
- `hugo-site/content/posts/ai-era-experience-is-the-bottleneck/index.md`
- `hugo-site/content/posts/ai-era-experience-is-the-bottleneck/cover.png`

### 构建状态

Hugo `v0.147.4` 构建通过，192 pages，0 errors。

### 发布状态

已按固定方式执行 `./publish.sh`，根目录静态产物已更新。`_incoming/` 不纳入提交范围。

### commit / tag / 版本号

- 版本号：v0.6.2
- commit：提交后以 tag `v0.6.2` 指向的 release commit 为准
- tag：v0.6.2

## 2026-05-28｜v0.6.1｜发布 ChatGPT 高反馈系统文章

### 今天做了什么

- 将用户提供的《和 ChatGPT 在一起，我重新找回了天天进步的感觉》整理为 Hugo 正式文章。
- 按建议 slug 创建文章 bundle：`chatgpt-daily-progress-feedback-system`。
- 归入 `火·AI`、`日课`、`AI时代`、`个人知识资产`。
- 添加 `ChatGPT`、`AI陪练`、`个人成长`、`高反馈环境`、`知识系统` 标签。
- 使用 imagegen 生成并接入文章封面图。
- 修正 `publish.sh` 排除清单，防止发布时误删根目录治理文档和站点校验 txt 文件。
- 更新公开 changelog、内部详细日志、每日工作日志、交接日志和项目状态文件。

### 做到什么程度

文章已进入正式发布流，作为公开长文发布，不放入 `_incoming/`，也不作为未发布储备稿处理。

### 遇到什么问题

- 默认 Codex 工作目录为空且不是 Git 仓库，需要重新定位到 `/Users/macos/angelife.github.com`。
- 首次运行发布脚本后发现 `rsync --delete` 会删除根目录治理文档，需要补充排除项。
- 文章初始发布时间写在本机当前时间之后，Hugo 未将其输出；已改为 `2026-05-28T12:20:00+08:00`。

### 已解决什么

- 已确认 angelife 仓库、Hugo 源站、发布脚本、版本规则和日志要求。
- 已按 SemVer 规则生成本轮版本号 `v0.6.1`。
- 已恢复根目录治理文档，并更新 `publish.sh` 防止后续重复误删。

### 未完成什么

- commit、push、tag 和线上验证在后续步骤完成后补入最终收工报告。

### 下一个 AI 应该从哪里接手

先读 `PROJECT_STATUS.md` 和 `AI_WORK_RULES.md`。本轮文章已经正式发布，不需要再从 `_incoming/` 处理。

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

### 构建状态

Hugo `v0.147.4` 构建通过，183 pages，0 errors。

### 发布状态

已按固定方式执行 `./publish.sh`，根目录静态产物已更新。`_incoming/` 已加入脚本排除项，未纳入提交范围。

### commit / tag / 版本号

- 版本号：v0.6.1
- commit：提交后以 tag `v0.6.1` 指向的 release commit 为准
- tag：v0.6.1

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
