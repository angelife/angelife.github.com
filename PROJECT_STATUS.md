# angelife 网站项目总控进度

## 当前阶段

网站工作流稳定期 / 内容发布期。

## 当前固定发布方式

本地 Hugo 生成 -> rsync 到仓库根目录 -> commit -> push -> git tag。

## 当前版本状态

- 当前版本：v0.6.32 待发布
- 最新 commit：尚未 commit
- 最新 tag：尚未 tag
- 线上状态：v0.6.31 已发布；本地有待发布改动（about 页面定稿+封面图、AI 执行代理规则一致性整理、日志补全）

### v0.6.32 待发布内容

- **about 页面定稿**：更新 `hugo-site/content/about/index.md`，由剑妈提供最新版说明，包含封面图接入（/images/about/cover.png）
- **AI 执行代理规则完善**：`AI_EXECUTION_AGENTS.md` 新增 NVIDIA 执行代理完整描述；`HERMES_COST_RULES.md` 新增 NVIDIA 练功房隔离要求；各治理文件统一"NVIDIA"名称和执行代理同级原则
- **规则一致性整理**：统一所有文件中的"NVIDIA"称呼和执行代理同级原则描述
- **日志补全**：更新 `SITE_CHANGELOG.md`、`DAILY_WORK_LOG.md`、`PROJECT_STATUS.md`、`BUILD_HANDOFF.md`、`hugo-site/data/changelog.yaml`
- **尚未 Hugo 构建**：待发布前执行 `hugo --gc --cleanDestinationDir --minify -s hugo-site`
- **尚未 commit / tag / push**：等待用户授权后由指定执行代理使用 `./tools/angelife-release v0.6.32 '<commit message>'` 统一发布

### v0.6.32 安全规则补全说明

- **安全 rsync 漏洞已修复**：原排除项缺少 .gitignore、.gitmodules、publish.sh、tools/，rsync --delete 模式曾误删，已由用户 git restore 恢复，本轮补齐排除清单
- **后续发布必须保护**：.gitignore、.gitmodules、publish.sh、tools/，禁止裸 rsync
- **所有执行代理必须署名留痕**：禁止匿名施工，禁止只写"已完成"不写执行者

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
- About 页更新，反映当前真实建站工作流。
- 受控发布脚本 `tools/angelife-release` 已创建。
- 受控发布脚本套件 `tools/angelife-{status,check,cost-log,release}` 已创建（含 `--yes` 非交互参数）
- AI 消耗记录制度已加入项目治理体系。

## 进行中

- 受控发布脚本已写入，后续发布必须使用 `tools/angelife-release`。
- AI 消耗记录制度已上线，后续每轮任务必须记录 AI token 与费用。
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
- 正式发布必须使用 `tools/angelife-release` 脚本。
- Reasonix 不直接裸跑 git push/tag。
- Hermes 不自行拼接发布流程。
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
