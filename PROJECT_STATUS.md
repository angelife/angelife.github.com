# angelife 网站项目总控进度

## 当前阶段

网站工作流稳定期 / 内容发布期。

## 当前固定发布方式

本地 Hugo 生成 -> rsync 到仓库根目录 -> commit -> push -> git tag。

## 当前版本状态

- 当前版本：v0.6.10
- 最新 commit：提交后以 tag `v0.6.10` 指向的 release commit 为准
- 最新 tag：v0.6.10
- 线上状态：本轮细化 Kindle 阅读模式 — 模板层移除导航、搜索入口、分类导航；顶部只保留站点名和版块名；普通页面不受影响；本地 Hugo 构建和 rsync 已完成，push 后等待 GitHub Pages 线上刷新。

## 版本号规则

`v2026.05.27-05` 及以前为日期流水版本；自 `v0.6.0` 起，angelife 网站改用 SemVer：`vMAJOR.MINOR.PATCH`。

- `MAJOR`：网站架构、发布方式、主题结构发生破坏性变化。
- `MINOR`：新增功能、栏目、搜索、评论、日志系统、内容体系。
- `PATCH`：修复样式、错字、链接、图片、分类、小 bug。

## 已完成

- Hugo 站点基本搭建。
- 首页五行栏目。
- 首页 full-width 修复。
- AI 文章上线。
- 火·AI 首页卡片显示新文章。
- 日课导航。
- 站内搜索。
- 文章页窄栏书页排版。
- 本地生成发布流程确认。
- SemVer 版本号规则。
- 搜索增强：高亮、上下文摘要、排序优化。
- giscus 评论系统预留。
- ChatGPT 高反馈系统文章上线。
- AI 时代经验瓶颈文章上线。
- `publish.sh` 已保护根目录治理文档，避免后续 `rsync --delete` 误删。

## 进行中

- 评论正式启用，等待 GitHub Discussions / giscus 参数。
- 公开 changelog 持续维护。
- 内部日志持续维护。
- 项目总控进度持续维护。

## 未完成

- 五行栏目默认封面图。
- 栏目 slug 统一。
- 移动端细节检查。
- 更多旧站内容迁移。
- Google Groups 内容整理。
- Notion 内容整理。
- 建站总控流程图接入 `hugo-site/static/images/workflow/site-control-map.png`。
- giscus `repoId` / `categoryId` 填入并按文章启用 `comments: true`。

## 当前风险 / 注意事项

- 不要切 GitHub Actions。
- 不要 `git add .`。
- 不要提交 `_incoming/`。
- 文章源文件 push 不等于网站上线，必须 `rsync`。
- 首页卡片可能是静态列表，新增重点文章后要检查。
- 不要破坏首页宽屏布局。
- 不要破坏文章页窄栏书页风格。
- 不要忘记每轮更新日志和创建 Git tag。
- giscus 未配置前不应显示评论区。
- 不要切换发布方式。
- 本轮新文章为正式发布内容，不进入 `_incoming/`。
- 当前版本号规则为 SemVer，本轮使用 `v0.6.2`，不是日期流水版本。

## 下一步优先级

1. 开启 GitHub Discussions。
2. 安装/授权 giscus，填入 `repoId` / `categoryId`。
3. 补充并接入网站项目总控流程可视化图。
4. 建立五行栏目默认封面图策略。
5. 梳理栏目 slug 与中文分类的长期命名规则。
6. 检查移动端首页、文章页、搜索页细节。
7. 继续迁移旧站中有长期价值的文章。
8. 整理 Google Groups / Notion 内容进入工作流。

## 下个 AI 接手第一步

先读 `PROJECT_STATUS.md`，再读 `BUILD_HANDOFF.md`、`AI_WORK_RULES.md`、`SITE_STYLE_GUIDE.md`、`SITE_CHANGELOG.md`、`DAILY_WORK_LOG.md`、`hugo-site/data/changelog.yaml`。
