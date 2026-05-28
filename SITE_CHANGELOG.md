# angelife 内部版本日志

本文件用于 AI 接手时查看详细版本演化。公开版本摘要见 `/changelog/` 和 `hugo-site/data/changelog.yaml`。

## v0.6.18｜新增受控发布脚本 tools/angelife-release

日期：2026-05-29
执行者：Reasonix
发布方式：受控发布脚本 tools/angelife-release
commit：提交后以 tag `v0.6.18` 指向的 release commit 为准
tag：v0.6.18

### 本次目标

- 新增 `tools/angelife-release` 受控发布脚本，统一执行 angelife 项目的正式发布流程。
- 以后 Hermes 或 Reasonix 不应自由发挥发布命令，而应在用户授权后调用这个脚本。
- 写入项目治理文档：Reasonix 不直接裸跑 git push/tag，Hermes 不自行拼接发布流程。
- 更新所有治理文档版本号至 v0.6.18。

### 修改文件

- 新增：`tools/angelife-release` — 受控发布脚本
- `AI_WORK_RULES.md` — 新增受控发布脚本规则 + 硬性禁止新增
- `BUILD_HANDOFF.md` — 版本号 v0.6.18 + 新增受控发布脚本说明
- `PROJECT_STATUS.md` — 版本号更新 + 新增受控脚本相关条目
- `SITE_CHANGELOG.md` — 新增 v0.6.18 版本日志
- `DAILY_WORK_LOG.md` — 新增今日日志
- `hugo-site/data/changelog.yaml` — 新增 v0.6.18 公开日志

### 脚本功能

`tools/angelife-release <version> '<commit message>'`

1. 检查当前目录必须是 `/Users/macos/angelife.github.com`。
2. 检查当前分支必须是 master。
3. 检查 version 参数不能为空。
4. 检查 commit message 参数不能为空。
5. 禁止 `git add .`（通过精准逐个添加替代）。
6. 禁止提交 `_incoming/`。
7. 禁止提交 `.reasonix/`。
8. 执行 Hugo 清洁构建：`hugo --gc --cleanDestinationDir --minify -s hugo-site`。
9. rsync Hugo 产物到仓库根目录。
10. 精准 git add 本轮修改内容，显式排除 `_incoming/` 和 `.reasonix/`。
11. git commit 使用传入 commit message。
12. git tag 使用传入 version。
13. git push origin master。
14. git push origin <version>。
15. 输出收工确认信息。

### 构建与发布

- 纯治理 + 脚本新增轮，Hugo 构建通过脚本自动执行。
- `tools/angelife-release` 已 chmod +x。

### 线上验证

- 无模板/CSS/内容变更，纯治理文件 + 新增脚本。
- 线上站点不受影响。

## v0.6.17｜更新 about 页以反映当前真实建站工作流

## v0.6.16｜固化 Hermes / Reasonix 手机远控分工规则

日期：2026-05-28
执行者：Reasonix
发布方式：本地 Hugo 生成 -> rsync 到仓库根目录 -> commit -> push -> git tag
commit：提交后以 tag `v0.6.16` 指向的 release commit 为准
tag：v0.6.16

### 本次目标

- 固化 Hermes / Reasonix 手机远控分工规则。
- 写入 Hermes 不得夺权、Reasonix 为执行工、Hermes 为总控和 terminal 手臂的正式分工。
- 定义 Hermes 代跑 shell 白名单。
- 记录手机远控链路打通全流程经验。
- 无模板/CSS/内容变更——纯治理固化轮。

### 修改文件

- `AI_WORK_RULES.md` — 新增第 14 条硬性禁止 + Hermes/Reasonix 手机远控工作流小节
- `BUILD_HANDOFF.md` — 新增手机远控操作指南小节
- `PROJECT_STATUS.md` — 更新版本号
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md` — 新增详细 Hermes/Reasonix 经验日志
- `hugo-site/data/changelog.yaml`

### 具体修改

**AI_WORK_RULES.md：**
- 硬性禁止新增第 14 条：Hermes 是总控入口，Reasonix 是执行工，Hermes 不得自行 patch/git add/commit/tag/push。
- 新增「Hermes / Reasonix 手机远控工作流」小节：固定链路、代跑 shell 白名单。

**BUILD_HANDOFF.md：**
- 新增「手机远控操作指南（v0.6.16+）」小节：前台运行方式、目录确认、权限边界。

**DAILY_WORK_LOG.md：**
- 新增 2026-05-28 Hermes/Reasonix 手机远控链路打通与权限边界调整日志。

### 构建与发布

- 纯治理文件更新，无 Hugo 构建变更。
- 不涉及 Hugo 构建和 rsync。

### 线上验证

- 无模板/CSS/内容变更，纯治理文件更新。
- 线上站点不受影响。

## v0.6.17｜更新 about 页以反映当前真实建站工作流

日期：2026-05-29
执行者：Reasonix
发布方式：本地 Hugo 生成 -> rsync 到仓库根目录 -> commit -> push -> git tag
commit：提交后以 tag `v0.6.17` 指向的 release commit 为准
tag：v0.6.17

### 本次目标

- 更新 /about/ 页面，反映当前真实建站工作流。
- Obsidian 不再被表述为深度接入自动化流程。
- Codex 不再被表述为当前主施工流。
- 新增当前真实链路展示：剑妈总编 → 蝉师傅 → Hermes → Reasonix → Hugo → rsync → Git → GitHub Pages。
- 同步更新所有治理文件和公开 changelog。

### 修改文件

- `hugo-site/content/about.md` — 完全重写 about 页正文
- `PROJECT_STATUS.md` — 版本号更新
- `BUILD_HANDOFF.md` — 版本号更新
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `hugo-site/data/changelog.yaml`

### 具体修改

**about.md：**
- 删除旧版中 Obsidian 深度参与建造的描述（Obsidian 当前不是主流程）。
- 删除旧版中 Codex 作为当前施工队的描述（Codex 不再是当前主施工流）。
- 删除旧版 5 层维护体系（日常收集/定期整理/Obsidian 内库/Hugo 外站/Git 部署），改为更平实的表述。
- 新增当前真实工作流链路。
- 新增角色分工描述：剑妈（总编）、蝉师傅（Telegram 入口）、Hermes（远程总控）、Reasonix（执行工）、DeepSeek（背后模型）、用户（最终决策）。
- 更新 Mermaid 流程图，反映当前真实链路。
- 注明 Obsidian 为未来方向，当前未深度接入。

**PROJECT_STATUS.md：**
- 版本从 v0.6.16 → v0.6.17
- 线上状态描述更新
- 已完成列表增加 About 页更新

**BUILD_HANDOFF.md：**
- 版本号更新至 v0.6.17

### 构建与发布

- Hugo 构建结果：待构建后确认
- rsync：待执行

### 线上验证

- /about/ 页面需要阅读确认工作流描述准确
- 治理文档版本号一致

### 未完成

- 无

### 下次接手注意

先读 `PROJECT_STATUS.md`，再读 `BUILD_HANDOFF.md`、`AI_WORK_RULES.md`、`SITE_STYLE_GUIDE.md`、`SITE_CHANGELOG.md`、`DAILY_WORK_LOG.md`、`hugo-site/data/changelog.yaml`。

## v0.6.15｜收尾提交：Kindle 治理固化后的静态产物同步

日期：2026-05-28
执行者：Hermes / Reasonix
发布方式：本地 Hugo 生成 -> rsync 到仓库根目录 -> commit -> push -> git tag
commit：提交后以 tag `v0.6.15` 指向的 release commit 为准
tag：v0.6.15

### 本次目标

- v0.6.14 治理文件更新后的静态产物全量提交。
- 确保 GitHub Pages 线上站点与本地治理文件更新一致。
- 无模板/CSS/内容变更。

### 修改文件

- Hugo 重新生成的全部静态产物（约 115 个文件）。
- 日志/治理文件：SITE_CHANGELOG.md、DAILY_WORK_LOG.md、PROJECT_STATUS.md、BUILD_HANDOFF.md、hugo-site/data/changelog.yaml

### Hugo 构建结果

223 pages，0 errors。

### git status 最终状态

仅剩 `.reasonix/` 和 `_incoming/` 未提交。

## v0.6.14｜固化 Kindle 阅读模式治理规则

日期：2026-05-28  
执行者：Reasonix  
发布方式：本地 Hugo 生成 -> rsync 到仓库根目录 -> commit -> push -> git tag  
commit：提交后以 tag `v0.6.14` 指向的 release commit 为准  
tag：v0.6.14

### 本次目标

- 将 Kindle 阅读模式规则正式写入项目治理文档和风格规范。
- 不修改任何模板、CSS 或文章内容——纯治理固化轮。

### 修改文件

- `AI_WORK_RULES.md` — 新增 Kindle 不可破坏规则 + Kindle 验收强制要求
- `SITE_STYLE_GUIDE.md` — 新增「Kindle 阅读模式」独立小节
- `PROJECT_STATUS.md` — 更新版本号与项目状态
- `BUILD_HANDOFF.md` — 新增 Kindle 接手交接确认 + 版本号更新
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `hugo-site/data/changelog.yaml`

### 具体修改

**AI_WORK_RULES.md：**
- 硬性禁止新增：不得破坏 Kindle 独立输出
- 文章双版本规则下新增 Kindle 验收强制要求（5 条）

**SITE_STYLE_GUIDE.md：**
- 新增 Kindle 阅读模式小节（5 条核心原则）

**BUILD_HANDOFF.md：**
- 新增 Kindle 接手交接确认小节

### 构建与发布

- Hugo 构建结果：Hugo `v0.147.4` 构建通过，223 pages，0 errors。
- rsync：已完成。

### 线上验证

- 无模板/CSS/内容变更，纯治理文件更新。
- /kindle/、/kindle/posts/<slug>/、/posts/<slug>/、首页均不受影响。

## v0.6.13｜修复 Kindle 文章页外层 PaperMod 壳

日期：2026-05-28  
执行者：Reasonix  
发布方式：本地 Hugo 生成 -> rsync 到仓库根目录 -> commit -> push -> git tag  
commit：提交后以 tag `v0.6.13` 指向的 release commit 为准  
tag：v0.6.13

### 本次目标

- 修复 Kindle 文章页（/kindle/posts/<slug>/）仍输出普通导航和 PaperMod footer 的问题。
- /kindle/ 目录页已干净，但文章页仍走普通 baseof/header/footer 包裹。
- 原因：baseof.html 中 `hasPrefix .RelPermalink "/kindle/"` 条件在某些构建场景下对 KindlePage outputFormat 未生效。
- 修复：改用 `$isKindle` 多条件变量（RelPermalink / Section / Layout 三重判断），统一控制 header/footer 渲染。

### 修改文件

- `hugo-site/layouts/_default/baseof.html` — 多条件 $isKindle 变量替代单条件 hasPrefix
- 日志/治理文件

### 验收

- Kindle 文章页：0 导航词、0 Powered by
- Kindle 目录页：0 导航词
- 普通首页：导航完整保留

### Hugo 构建

223 pages，0 errors

## v0.6.12｜重新同步 Kindle 线上静态产物

日期：2026-05-28  
执行者：Reasonix  
发布方式：本地 Hugo 生成 -> rsync 到仓库根目录 -> commit -> push -> git tag  
commit：提交后以 tag `v0.6.12` 指向的 release commit 为准  
tag：v0.6.12

### 本次目标

- 本地 Kindle 产物已验证干净，但线上出现导航残留。
- 执行强制清洁构建（`--gc --cleanDestinationDir`）并全量 rsync 覆盖根目录静态产物。
- 重新推送确保 GitHub Pages 部署的是完全清洁的 Kindle 模板。
- 在 rsync 中增加 `.reasonix/` 排除项。

### 验收

- Kindle 目录页和文章页：无导航词、无 Powered by、无 id=menu
- 普通页面：导航完整保留
- rsync 已排除 `.reasonix/`

### Hugo 构建

223 pages，0 errors

## v0.6.11｜Kindle/手机自动跳转阅读模式 + 双版本发布规则固化

日期：2026-05-28  
执行者：Reasonix  
发布方式：本地 Hugo 生成 -> rsync 到仓库根目录 -> commit -> push -> git tag  
commit：提交后以 tag `v0.6.11` 指向的 release commit 为准  
tag：v0.6.11

### 本次目标

- 新增 Kindle / 手机用户自动跳转阅读模式。
- 新增 `?normal=1` 出口，可返回图文版并记录偏好。
- 固化文章双版本发布规则：一份 Markdown 源文件 → 普通版 + Kindle 版。
- 更新治理文档写入双版本规则。

### 新增文件

- `hugo-site/static/js/reader-redirect.js` — 前端自动跳转脚本

### 修改文件

- `hugo-site/layouts/partials/extend_head.html` — 条件加载 reader-redirect.js
- `hugo-site/layouts/_default/single.kindle.html` — 页脚加入图文版出口链接
- `hugo-site/layouts/kindle/list.html` — 页脚加入图文版出口链接
- `AI_WORK_RULES.md` — 新增双版本发布规则章节
- `SITE_STYLE_GUIDE.md` — 新增双版本规则
- `BUILD_HANDOFF.md` — 新增双版本维护说明
- `PROJECT_STATUS.md` — 更新版本号
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `hugo-site/data/changelog.yaml`

### 自动跳转规则

- Kindle 设备访问首页 → 跳转 `/kindle/`
- Kindle 设备访问文章页 → 跳转 `/kindle/posts/<slug>/`
- 手机端访问首页 → 跳转 `/kindle/`
- 手机端访问文章页 → 跳转 `/kindle/posts/<slug>/`
- 已存 `normal` 模式 → 不跳转
- 已在 `/kindle/` 路径 → 不跳转
- 桌面端 → 不跳转

### 双版本发布规则

每篇文章只维护一份 Markdown 源文件，Hugo 自动输出：

- 普通图文版：`/posts/<slug>/`
- Kindle 阅读版：`/kindle/posts/<slug>/`

封面图只服务普通版。发布验收必须同时检查两个版本。

### Hugo 构建

223 pages，0 errors

## v0.6.10｜Kindle 阅读模式细化：模板层移除导航

日期：2026-05-28  
执行者：Reasonix  
发布方式：本地 Hugo 生成 -> rsync 到仓库根目录 -> commit -> push -> git tag  
commit：提交后以 tag `v0.6.10` 指向的 release commit 为准  
tag：v0.6.10

### 本次目标

- 在模板层面完全移除 Kindle 页面的主导航、搜索入口、分类导航等不必要 HTML。
- 顶部只保留：站点名「安知生 angelife」 + 版块名「Kindle 阅读版」。
- 页脚只保留简版权和返回链接。
- 确认普通桌面端、手机端不受影响。

### 修改文件

- `hugo-site/layouts/_default/baseof.html` — Kindle 路径跳过 `partialCached "header.html"` 和 `footer.html`
- `hugo-site/layouts/_default/single.kindle.html` — 加入 `kindle-topbar` 和 `kindle-footer`
- `hugo-site/layouts/kindle/list.html` — 加入 `kindle-topbar` 和 `kindle-footer`
- `hugo-site/static/css/kindle.css` — 新增 `kindle-topbar` / `kindle-footer` 样式，删除不再使用的 CSS
- `SITE_CHANGELOG.md`、`DAILY_WORK_LOG.md`、`PROJECT_STATUS.md`、`BUILD_HANDOFF.md`、`hugo-site/data/changelog.yaml`

### 验收

- 查看 Kindle 页面源代码：无 `id=menu`、无 `class=.nav`、无「金·判断」「木·蝉识」「搜索」等导航词
- 普通页面导航完整保留

### Hugo 构建

223 pages，0 errors

## v0.6.9｜重构为独立 Kindle 电子书阅读模式

日期：2026-05-28  
执行者：Reasonix  
发布方式：本地 Hugo 生成 -> rsync 到仓库根目录 -> commit -> push -> git tag  
commit：提交后以 tag `v0.6.9` 指向的 release commit 为准  
tag：v0.6.9

### 本次目标

- 将 Kindle 模式从"网页兼容"重构为"独立电子书入口"。
- 新增独立 Kindle 文章页 `/kindle/posts/<slug>/`，通过 Hugo output format 自动生成。
- 目录页链接指向 Kindle 独立文章页。
- 使用 `body.kindle-mode` 类强制激活 Kindle CSS，不依赖 monochrome 媒体查询。
- 完整隐藏封面图、标签、分享、评论、装饰性元素。

### 技术方案

- Hugo `[outputFormats.Kindle]` — 自动为每篇 post 生成 `/kindle/posts/<slug>/index.html`
- `content/posts/_index.md` — cascade 设置 `outputs = ["HTML", "Kindle"]`
- `layouts/_default/single.kindle.html` — Kindle 文章页模板（纯文字、无装饰、上一篇/下一篇导航）
- `layouts/kindle/list.html` — Kindle 目录模板（文章列表，链接到 Kindle 文章页）
- `layouts/_default/baseof.html` — 通过 `hasPrefix .RelPermalink "/kindle/"` 注入 `kindle-mode` 类
- `static/css/kindle.css` — 完全重写，使用 `body.kindle-mode` 选择器，serif 字体

### 修改文件

- 新增：`hugo-site/layouts/_default/single.kindle.html`
- 新增：`hugo-site/layouts/kindle/list.html`
- 新增：`hugo-site/layouts/_default/baseof.html`
- 修改：`hugo-site/static/css/kindle.css`（完全重写）
- 修改：`hugo-site/content/kindle/_index.md`（移除 layout 字段）
- 修改：`hugo-site/content/posts/_index.md`（添加 cascade outputs）
- 修改：`hugo-site/hugo.toml`（添加 outputFormats.Kindle）
- 修改：`SITE_CHANGELOG.md`、`DAILY_WORK_LOG.md`、`PROJECT_STATUS.md`、`BUILD_HANDOFF.md`、`hugo-site/data/changelog.yaml`

### 构建与发布

- Hugo 构建结果：Hugo `v0.147.4` 构建通过，223 pages，0 errors。
- rsync：已完成。

### 线上验证

- `/kindle/` — 纯文字目录页，无封面图、无卡片、无装饰
- `/kindle/posts/<slug>/` — 独立 Kindle 文章页，body.kindle-mode 类激活
- 普通桌面页、手机页不受影响

## v0.6.8｜新增 Kindle Paperwhite 阅读模式

日期：2026-05-28  
执行者：Reasonix  
发布方式：本地 Hugo 生成 -> rsync 到仓库根目录 -> commit -> push -> git tag  
commit：提交后以 tag `v0.6.8` 指向的 release commit 为准  
tag：v0.6.8

### 本次目标

- 为 angelife 网站增加 Kindle KPW5 / 电子墨水屏阅读优化模式。
- 新增 `/kindle/` 入口页面：黑白高对比、大字号、文章列表优先、无封面图、无复杂装饰。
- 新增 `kindle.css`：通过 `@media (monochrome)` 条件激活，全站生效但仅在 Kindle 浏览器或窄屏下改变样式。
- 新增主导航入口。
- 同步更新所有日志和治理文件。

### 新增文件

- `hugo-site/content/kindle/_index.md`
- `hugo-site/layouts/section/kindle.html`
- `hugo-site/static/css/kindle.css`

### 修改文件

- `hugo-site/hugo.toml` — 新增 Kindle版 导航条目
- `hugo-site/layouts/partials/extend_head.html` — 加载 kindle.css
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `PROJECT_STATUS.md`
- `BUILD_HANDOFF.md`
- `hugo-site/data/changelog.yaml`

### 构建与发布

- Hugo 构建结果：Hugo `v0.147.4` 构建通过，215 pages，0 errors。
- rsync：已完成。

### 线上验证

- `/kindle/`：已生成，包含 9 篇最新文章列表，无封面图，简单条目布局。
- `/css/kindle.css`：已部署。
- 普通首页和文章页不受影响。

## v0.6.7｜发布机器执行经验指挥文章并修复 404

日期：2026-05-28  
执行者：Reasonix  
发布方式：本地 Hugo 生成 -> rsync 到仓库根目录 -> commit -> push -> git tag  
commit：提交后以 tag `v0.6.7` 指向的 release commit 为准  
tag：v0.6.7

### 本次目标

- 将长期滞留于 untracked 状态的文章《机器执行，经验指挥：AI 时代真正昂贵的东西》正式纳入 git 跟踪并发布上线。
- 修复线上 `/posts/ai-machine-executes-experience-commands/` 404 问题。
- 同步更新所有日志和治理文件。

### 修改文件

- `hugo-site/content/posts/ai-machine-executes-experience-commands/index.md`
- `posts/ai-machine-executes-experience-commands/index.html`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `PROJECT_STATUS.md`
- `BUILD_HANDOFF.md`
- `hugo-site/data/changelog.yaml`

### 具体修改

- 将 untracked 状态的文章源文件及静态产物正式提交到 git。
- 文章 slug：`ai-machine-executes-experience-commands`。
- 分类：`火·AI`、`AI时代`。
- 标签：`AI工作流`、`自动化`、`经验`、`AI时代`、`个人系统`、`托管人生`。
- 封面状态：`cover_status: prompt_ready`，封面图待后续接入。

### 构建与发布

- Hugo 构建结果：Hugo `v0.147.4` 构建通过，213 pages，0 errors。
- rsync：已完成，`hugo-site/public/` 已同步到仓库根目录。

### 线上验证

- `/posts/ai-machine-executes-experience-commands/`：静态产物已生成并验证目标路径，不再 404。

## v0.6.6｜接入高速公路与泥巴地文章封面图

日期：2026-05-28  
执行者：Reasonix  
发布方式：本地 Hugo 生成 -> rsync 到仓库根目录 -> commit -> push -> git tag  
commit：提交后以 tag `v0.6.6` 指向的 release commit 为准  
tag：v0.6.6

### 本次目标

- 将 ChatGPT 生成的封面图接入《高速公路与泥巴地：AI时代的本土化生存》文章。
- 拷贝封面图到 `hugo-site/static/images/posts/highway-and-muddy-road-ai-localization/cover.png`。
- 更新文章 front matter，加入 `cover` 字段。
- 更新视觉资产记录为 `cover_status: image_ready`。
- 同步更新所有日志和治理文件。

### 修改文件

- `hugo-site/static/images/posts/highway-and-muddy-road-ai-localization/cover.png`
- `hugo-site/content/posts/highway-and-muddy-road-ai-localization/index.md`
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `PROJECT_STATUS.md`
- `BUILD_HANDOFF.md`
- `hugo-site/data/changelog.yaml`

### 具体修改

- 新增封面图至 `static/images/posts/highway-and-muddy-road-ai-localization/cover.png`。
- 文章 `index.md` 加入 `cover` front matter。
- 视觉资产状态从 `prompt_ready` 更新为 `image_ready`。

### 构建与发布

- Hugo 构建结果：Hugo `v0.147.4` 构建通过，213 pages，0 errors。
- rsync：已完成，`hugo-site/public/` 已同步到仓库根目录。

### 线上验证

- `/posts/highway-and-muddy-road-ai-localization/`：封面图已接入。
- 封面图 URL：`/images/posts/highway-and-muddy-road-ai-localization/cover.png`。

### 未完成

- 正式 commit、push、tag 和线上验证需在后续步骤完成后补入。

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

先读 `PROJECT_STATUS.md`，再读 `BUILD_HANDOFF.md`、`AI_WORK_RULES.md`、`SITE_STYLE_GUIDE.md`、`SITE_CHANGELOG.md`、`DAILY_WORK_LOG.md`、`hugo-site/data/changelog.yaml`。

## v0.6.17｜更新 about 页以反映当前真实建站工作流

日期：2026-05-29
执行者：Reasonix
发布方式：本地 Hugo 生成 -> rsync 到仓库根目录 -> commit -> push -> git tag
commit：提交后以 tag `v0.6.17` 指向的 release commit 为准
tag：v0.6.17

### 本次目标

- 更新 /about/ 页面，反映当前真实建站工作流。
- obsidian 不再被表述为深度接入自动化流程。
- Codex 不再被表述为当前主施工流。
- 新增当前真实链路展示：剑妈总编 → 蝉师傅 → Hermes → Reasonix → Hugo → rsync → Git → GitHub Pages。
- 同步更新所有治理文件和公开 changelog。

### 修改文件

- `hugo-site/content/about.md` — 完全重写 about 页正文
- `PROJECT_STATUS.md` — 版本号更新
- `BUILD_HANDOFF.md` — 版本号更新
- `SITE_CHANGELOG.md`
- `DAILY_WORK_LOG.md`
- `hugo-site/data/changelog.yaml`

### 具体修改

**about.md：**
- 删除旧版中 Obsidian 深度参与建造的描述（Obsidian 当前不是主流程）。
- 删除旧版中 Codex 作为当前施工队的描述（Codex 不再是当前主施工流）。
- 删除旧版 5 层维护体系（日常收集/定期整理/Obsidian 内库/Hugo 外站/Git 部署）——趋向平实。
- 新增当前真实工作流链路。
- 新增角色分工描述：剑妈（总编）、蝉师傅（Telegram 入口）、Hermes（远程总控）、Reasonix（执行工）、DeepSeek（背后模型）、用户（最终决策）。
- 更新 Mermaid 流程图，反映当前真实链路。
- 注明 Obsidian 为未来方向，当前未深度接入。

**PROJECT_STATUS.md：**
- 版本从 v0.6.16 → v0.6.17
- 线上状态描述更新
- 已完成列表增加 About 页更新

**BUILD_HANDOFF.md：**
- 版本号更新至 v0.6.17

### 构建与发布

- Hugo 构建结果：待构建后确认
- rsync：待执行

### 线上验证

- /about/ 页面需要阅读确认工作流描述准确
- 治理文档版本号一致

### 未完成

- 无

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
