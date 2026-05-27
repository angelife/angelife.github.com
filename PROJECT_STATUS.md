# angelife 网站项目总控进度

## 当前阶段

网站结构升级期 / 内容体系与工作流稳定期。

## 当前固定发布方式

本地 Hugo 生成 -> rsync 到仓库根目录 -> commit -> push -> git tag。

## 当前版本状态

- 当前版本：v2026.05.27-05
- 最新 commit：提交后以 tag `v2026.05.27-05` 指向的 release commit 为准
- 最新 tag：v2026.05.27-05
- 线上状态：本轮已生成并同步 `/changelog/`、`/site-workflow/` 和顶部“更新”导航；推送后等待 GitHub Pages 线上刷新。

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

## 进行中

- AI 接手规范体系。
- 公开 changelog。
- 内部日志。
- 项目总控进度。

## 未完成

- 五行栏目默认封面图。
- 栏目 slug 统一。
- 移动端细节检查。
- 更多旧站内容迁移。
- Google Groups 内容整理。
- Notion 内容整理。
- 建站总控流程图接入 `hugo-site/static/images/workflow/site-control-map.png`。

## 当前风险 / 注意事项

- 不要切 GitHub Actions。
- 不要 `git add .`。
- 不要提交 `_incoming/`。
- 文章源文件 push 不等于网站上线，必须 `rsync`。
- 首页卡片可能是静态列表，新增重点文章后要检查。
- 不要破坏首页宽屏布局。
- 不要破坏文章页窄栏书页风格。
- 不要忘记每轮更新日志和创建 Git tag。

## 下一步优先级

1. 补充并接入网站项目总控流程可视化图。
2. 检查移动端首页、文章页、搜索页细节。
3. 建立五行栏目默认封面图策略。
4. 梳理栏目 slug 与中文分类的长期命名规则。
5. 继续迁移旧站中有长期价值的文章。
6. 整理 Google Groups 内容进入 Inbox。
7. 整理 Notion 内容进入 Obsidian / Hugo 工作流。
8. 为重点长文补齐 cover 和摘要。

## 下个 AI 接手第一步

先读 `PROJECT_STATUS.md`，再读 `BUILD_HANDOFF.md`、`AI_WORK_RULES.md`、`SITE_STYLE_GUIDE.md`、`SITE_CHANGELOG.md`、`DAILY_WORK_LOG.md`、`hugo-site/data/changelog.yaml`。
