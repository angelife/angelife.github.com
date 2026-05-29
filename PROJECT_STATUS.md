# angelife 网站项目总控进度

## 当前阶段

网站工作流稳定期 / 内容发布期。

## 当前固定发布方式

本地 Hugo 生成 -> rsync 到仓库根目录 -> commit -> push -> git tag。

## 当前版本状态

- 当前版本：v0.6.33 待发布
- 最新 commit：尚未 commit
- 最新 tag：尚未 tag
- 线上状态：v0.6.31 已发布；本地有待发布改动（site-workflow 页面更新 + 流程图接入 + 日志补全）

### v0.6.33 待发布内容

- **site-workflow 页面更新**：`hugo-site/content/site-workflow/index.md` 更新为最新版《建站模式日志》，明确「本地为主场，AI 为外援」
- **项目总控流程图接入**：`hugo-site/static/images/workflow/site-control-map.png`（2MB），路径 `/images/workflow/site-control-map.png`
- **日志补全**：更新 `SITE_CHANGELOG.md`、`DAILY_WORK_LOG.md`、`PROJECT_STATUS.md`、`BUILD_HANDOFF.md`、`hugo-site/data/changelog.yaml`
- **尚未 Hugo 构建**：待 macOS 本机执行 `hugo --gc --cleanDestinationDir --minify -s hugo-site`
- **尚未 rsync / commit / tag / push**：等待 macOS 本机执行安全 rsync 后由指定执行代理发布

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

## v0.6.35 状态更新

本轮新增 `AI_BOOTSTRAP.md`，用于 AI 接手时恢复项目记忆。

当前核心分工：

- 剑妈：设计师 + 总控
- NVIDIA：具体做事者
- 本地 Mac：补完 NVIDIA 因 Docker 限制无法完成的本机动作
- Obsidian：本地低成本查看、检查、轻修改、上传、中转和自动归档工作台

责任规则：

谁设计，谁署名。  
谁生成，谁署名。  
谁写入，谁署名。  
谁构建，谁署名。  
谁发布，谁署名。  
谁验证，谁署名。  
谁出问题，能回溯。

后续任务：

v0.7.0：旧 Blogger 内容回流工程。来源：https://angelifex.blogspot.com/

## v0.6.36 — 2026-05-29

**状态**：✅ 内容就绪，待发布授权

**本轮完成**：
- README.md 重写为 AI 接手入口（剑妈 + NVIDIA）
- 内部日志块草案（NVIDIA）
- 最终交接报告（NVIDIA）

**待本地 Mac 执行**：
- 复制 README.md 等文件到仓库对应路径
- Hugo 构建
- tools/angelife-release v0.6.36 "Update README as AI onboarding entry point"（待授权）
- git add / commit / tag / push（待授权）
- 线上验证（待授权）

**本轮不启用**：蝉师傅、龙虾、Reasonix、Codex、Claude Code

**发布授权**：❌ 未授权

**后续任务**：v0.7.0 旧 Blogger 内容回流工程（见 BUILD_HANDOFF.md）## v0.6.37 — 2026-05-29

**状态**：✅ 内容就绪，待发布授权

**本轮完成**：
- `NVIDIA_GATEWAY_RECOVERY.md` 新增（SOP 文档）
- `CHANGELOG_YAML_RULES.md` 新增（YAML 写入规则）
- `NVIDIA_MAIN_REPO_MOUNT_PLAN.md` 新增（挂载规划）
- `AI_BOOTSTRAP.md` 追加（新增文档引用）
- `README.md` 追加（新增文档引用）
- 内部日志文件草案（NVIDIA）
- `changelog_yaml_block.yaml` 标准块（NVIDIA）

**待本地 Mac 执行**：
- 将追加内容合并入 AI_BOOTSTRAP.md / README.md 末尾
- 将日志块追加入对应文件
- 将 `changelog_yaml_block.yaml` 插入 `hugo-site/data/changelog.yaml`
- Hugo 构建
- tools/angelife-release v0.6.37（待授权）
- git add / commit / tag / push（待授权）
- 线上验证（待授权）

**本轮不启用**：蝉师傅、龙虾、Reasonix、Codex、Claude Code

**主库挂载**：本轮不执行，见 `NVIDIA_MAIN_REPO_MOUNT_PLAN.md`

**发布授权**：❌ 未授权

**后续任务**：v0.7.0 旧 Blogger 内容回流工程（见 BUILD_HANDOFF.md）## v0.6.38 — 2026-05-29

**状态**：✅ RUNBOOK 就绪，待 /repo 路径方案确认

**本轮完成**：
- 容器配置完整分析（docker ps / inspect / logs / env / ps / services）
- `NVIDIA_REPO_MOUNT_RUNBOOK.md` 生成
- 内部日志文件草案

**关键发现**：
- 主库已挂载至 `/workspace/angelife.github.com`
- `/repo` 路径不存在，需通过 symlink 创建或修改容器启动参数
- Telegram gateway 运行正常（PID 207）
- s6 supervise 正常工作，无 down 文件
- Docker 镜像落后 1 个 commit（warning 提示）

**待本地 Mac 执行**：
- 决定 /repo 路径方案（symlink 或新容器）
- 如选 symlink：`docker exec hermes-minimaxlab ln -sf /workspace/angelife.github.com /repo`
- Hugo 构建验证（后续）
- tools/angelife-release（待授权）
- git 操作（待授权）

**本轮不启用**：蝉师傅、龙虾、Reasonix、Codex、Claude Code

**发布授权**：❌ 未授权

**后续任务**：v0.7.0 旧 Blogger 内容回流工程（见 BUILD_HANDOFF.md）
## v0.6.39 — 2026-05-29

**状态**：✅ NVIDIA 直接写主库成功，待本地 Mac 发布

**里程碑**：
- NVIDIA 已进入“直接写主库文件”阶段
- `/repo` 路径已验证可写
- v0.6.39 文件已通过 /repo 直接写入主库

**NVIDIA 当前权限**：
- 直接写入 /repo 文件：✅
- git add / commit / tag / push：❌ 禁止
- release：❌ 禁止

**本地 Mac 职责**：
- 检查 git diff
- 插入 hugo-site/data/changelog.yaml（按模板）
- Hugo 构建
- tools/angelife-release（待授权）
- git push（待授权）

**本轮不启用**：蝉师傅、龙虾、Reasonix、Codex、Claude Code

**发布授权**：❌ 未授权

**后续任务**：v0.7.0 旧 Blogger 内容回流工程

## v0.6.40 — 2026-05-29

**状态**：✅ 文章已落盘，待本地 Mac 发布

**里程碑**：
- NVIDIA 已进入“直接写 Hugo 正式文章源文件”试运行阶段
- 本轮文章 slug：zhen-to-sui-touching-the-pattern
- 封面状态：cover_status: prompt_ready

**NVIDIA 当前权限**：
- 直接写入 /repo/hugo-site/content/posts/：✅
- git / release：❌ 禁止

**本地 Mac 职责**：
- Hugo 构建
- tools/angelife-release（待授权）
- git push（待授权）
- 线上验证：/posts/zhen-to-sui-touching-the-pattern/ / changelog/ 微信认证文件

**发布授权**：❌ 未授权
