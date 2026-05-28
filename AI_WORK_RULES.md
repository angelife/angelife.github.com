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
- 不准破坏 Kindle 阅读模式的独立输出。Kindle 版是独立阅读输出，不是普通页面的 CSS 隐藏变体。修改 header、footer、baseof、single、list、outputFormats 或导航模板时，必须同时验收普通版和 Kindle 版。不得让 `/kindle/` 或 `/kindle/posts/<slug>/` 输出 PaperMod 普通导航、普通 footer 或桌面站点 chrome。

- Hermes 是手机远程总控和 Telegram 入口。Reasonix 是项目执行工。Hermes 默认不得直接修改项目文件，不得自行 patch，不得自行扩大 git add，不得擅自 commit/tag/push。当 Reasonix 在 headless/MCP 场景下无法执行 shell 命令时，Hermes 可以作为 terminal 手臂代跑 shell，但必须严格执行 Reasonix 明确列出的命令，不得自由发挥。
- 正式发布必须使用 `tools/angelife-release` 脚本，Reasonix 不直接裸跑 git push/tag，Hermes 不自行拼接发布流程。

## 固定发布流程

继续使用受控发布脚本：

```bash
./tools/angelife-release <version> '<commit message>'
```

等价于以下标准流程：

```text
本地 Hugo 生成 -> rsync 到仓库根目录 -> commit -> push -> git tag
```

## 受控发布脚本规则（v0.6.18+）

- 以后正式发布优先使用 `tools/angelife-release`。
- Reasonix 不直接裸跑 `git push` / `git tag`。
- Hermes 不自行拼接发布流程。
- 发布权交给用户授权 + 固定脚本。
- Hermes 只负责代跑脚本，不得自行 patch 或修复 Reasonix 输出。
- Reasonix 输出修改后如需代跑，应直接输出 `./tools/angelife-release <version> '<commit message>'` 命令。

调用方式：

```bash
cd /Users/macos/angelife.github.com
./tools/angelife-release v0.6.18 'chore: add controlled release workflow'
```

脚本内部已实现：
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

## 文章双版本发布规则（v0.6.11 起固化）

每篇文章只维护一份 Markdown 源文件，Hugo 自动输出两个版本：

- 普通图文版：`/posts/<slug>/`
- Kindle 阅读版：`/kindle/posts/<slug>/`

由 `content/posts/_index.md` 的 `cascade` 配置自动控制：

[cascade]
  outputs = ["HTML", "Kindle"]

发布验收必须同时检查两个版本：

| 检查项 | 普通图文版 | Kindle 阅读版 |
|--------|-----------|--------------|
| 封面图 | 正常显示 | 不显示 |
| 导航 | 完整导航 | 无主导航/搜索/分类导航 |
| 标签/评论/分享 | 正常 | 不显示 |

封面图只服务普通图文版；不为 Kindle 版单独维护图片或第二份正文。

### Kindle 验收强制要求

每次修改后必须执行以下验收：

1. `/kindle/` 目录页无普通导航（grep 金·判断/木·蝉识/搜索/id="menu" /kindle/index.html 应为 0）
2. `/kindle/posts/<slug>/` 文章页无普通导航和 footer（grep Powered by/PaperMod/id="menu" 应为 0）
3. `/posts/<slug>/` 普通文章页必须保留正常导航
4. 首页普通导航必须保留
5. 不得通过 `display:none` 临时遮挡来伪造 Kindle 模式——模板层必须已剥离

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

## Hermes / Reasonix 手机远控工作流

固定链路：

手机 Telegram → Hermes 总控 → terminal → reasonix run → Reasonix 执行 → Hermes 按 Reasonix 明确命令代跑 shell → Hugo 构建 → rsync → 精准 git add → commit → tag → push

Hermes 代跑 shell 白名单：

pwd、ls、cat、grep、rg、git status、git diff、git log、hugo --gc --cleanDestinationDir --minify -s hugo-site、rsync -av hugo-site/public/ ./、精准 git add <文件列表>、git commit、git tag、git push

任何超出白名单的命令必须先汇报并等待用户确认。

## Git 添加规则

不要使用 `git add .`。

按任务范围精确添加源文件和根目录静态产物。每次提交前必须运行：

```bash
git status --short
git diff --cached --stat
git diff --cached --name-only | rg '^_incoming|^\.github/workflows/'
```

如果发现 `_incoming/` 或未授权 workflow 修改，必须取消暂存并重新检查。
