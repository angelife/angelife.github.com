---
name: angelife-site
description: "Angelife Hugo 网站项目全栈管理 — 治理规则维护 + Hugo 写作工作流 + GitHub Pages 部署。覆盖多文件一致性修正、发布安全、文章生命周期、Taxonomy 配置、PaperMod 主题、KOReader 等。"
version: 1.2.0
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [angelife, hugo, governance, authoring, deployment, github-pages, git-submodule]
    related_skills: [free-image-generation]
---

# Angelife Site — 全栈管理技能

## 触发条件

对 angelife Hugo 网站项目的**任何**操作需求：
- 修改治理规则文件（术语一致性、多文件修正）
- 写作新文章 / 修改旧文
- Hugo 构建与 GitHub Pages 部署
- Git 操作（add / commit / tag / push）
- 检查网站问题（404、build 失败、taxonomy 异常、其他代理的未 commit 改动）
- 审计其他代理（剑妈/Codex/Claude Code）在本地仓库的修改
- 事故归档（INCIDENT_REPORTS）

## 核心架构

### 文件结构
```
/repo/                              ← Docker 内挂载点（对应 Mac /Users/macos/angelife.github.com）
  hugo-site/                        ← Hugo 项目根目录
    content/                        ← 文章源（posts/, series/, columns/）
    static/                         ← 静态资源（图片等）
    themes/PaperMod/                 ← git submodule（子模块）
    hugo.toml                       ← Hugo 配置
    public/                         ← Hugo 构建产物（不进入 git）
  _private/                         ← 内部治理文档（不在 git）
    INCIDENT_REPORTS/               ← 事故归档
  SITE_CHANGELOG.md                 ← 内部版本日志
  DAILY_WORK_LOG.md                 ← 每日工作日志
  AI_EXECUTION_AGENTS.md            ← AI 代理身份定义
  AI_WORK_RULES.md                  ← AI 工作硬性规则
  HERMES_COST_RULES.md              ← 练功房规则
  BUILD_HANDOFF.md                  ← 建站交接手册
  SITE_STYLE_GUIDE.md               ← 风格规范
```

### 关键原则

1. **同级代理原则**：NVIDIA / Hermes / Codex / Claude Code 都是 AI 执行代理，无阶级差异，只有工具特长和成本不同。
2. **天使群五行分工（2026-06-20 确立）**：用户运营一个 Telegram 群（Angelife Tse），其中每个 bot 有明确角色：
   - **木同学（当前 NVIDIA Hermes 实例）** — 技术顾问，负责写稿、技术排查、批量操作。写完后通知土审查发布。不碰 git push。
   - **土同学（@sir_chan_bot）** — Mac 本地 Hermes，负责本地预览、配图挂接、发布上线（git/rsync）。实际操作者。
   - **金同学（@peterchan90_bot）** — gold profile Hermes，CEO/CTO 角色，负责决策、把关、拆问题。不下场实操。
   - **火同学（@SwarmDiscussionBot）** — 方向讨论。
   - **水同学（@masterchan19840907_bot）** — 智慧评论。
   - **⚠️ 群聊寻址规则**：每条消息先看收件人。前缀为"木同学"/@NVIDIA2012_bot → 才接手处理。前缀为其他同学名字的指令 → 不回应、不参与、不确认。没前缀的通用问题才判断是否该接。
   - **⚠️ 不要制造剧情**：用户明确指出火和水两位同学"压根没来"，不要在任何汇报或消息中提及他们或编造他们的状态。
3. **发布链路**：木同学/金同学写稿 → 通知土同学 → 土同学本地预览 → 土同学审查发布。**木同学不执行 git push/rsync。**
4. **写文章前先查现有分类**：在创建 Hugo 文章之前，必须先 grep 查看现有文章的 `categories` 和 `tags` 用法。现有栏目：`火·AI`、`一人公司`、`易理`、`日课`、`AI时代`、`AI工作流`、`个人成长`、`判断力`。不确定时用 `火·AI` 为主分类。
5. **写文章前必须先查是否有相似文章**：内容高度相似 → 合并到旧文；主题相关角度不同 → 关联 + 链接；独立话题才写新文。
6. **精确 git add**：不得使用 `git add .`，必须逐文件指定。
7. **NUL-safe git add**：涉及中文路径必须用 NUL-safe 方式。
8. **发布验证**：Git push 成功 ≠ 任务完成。必须验证网站可访问（6 项检查清单）。
9. **PaperMod submodule**：每次在 Mac 上预览前必须 `git submodule update --init --recursive`。

---

## 一、治理规则维护

### 触发条件

修改 / 校正 / 更新任意一个项目治理规则文件时触发：
- `AI_EXECUTION_AGENTS.md` — AI 代理身份、权限、边界
- `HERMES_COST_RULES.md` — 低成本练功规则
- `AI_WORK_RULES.md` — AI 工作硬性禁止和固定流程
- `BUILD_HANDOFF.md` — 建站交接手册
- `SITE_STYLE_GUIDE.md` — 网站风格规范
- `SITE_CHANGELOG.md` — 内部版本日志
- `DAILY_WORK_LOG.md` — 每日工作日志
- `hugo-site/data/changelog.yaml` — 公开 changelog

### 核心原则

- **同级代理，无阶级差异**：NVIDIA / Hermes / Codex / Claude Code 都是 AI 执行代理，无阶级差异。
- **天使群五行分工（2026-06-20）**：木同学（技术顾问，写稿为主）、土同学（本地操作，审查发布）、金同学（决策把关）。火和水不在线时不要编造状态。
- **发布链路**：木/金写稿 → 通知土 → 土预览后发布。木同学不执行 git push/rsync。
- **单代理操作**：同一时间只能一个代理操作仓库。
- **Surgical scope**：修正规则文件时，只改需要改的表述，不扩大任务范围，不重写整段，不修改 Hugo 文章。
- **不发布**：除非用户明确授权，否则不执行 git add / commit / tag / push / rsync / Hugo 构建。

### 标准工作流

1. **读取所有相关文件**（一起读取）
2. **分析一致性**：检查旧文件中是否存在与新原则冲突的表述
3. **Surgical 修正**：只修改需要修正的表述
4. **三段式输出**：修正了哪些文件 / 修正了哪些错误 / 是否发布
5. **不发布**：等待用户授权

### 版本同步 5 文件清单

治理规则修正必须同步更新以下 5 个文件：

| 文件 | 更新内容 |
|------|---------|
| `SITE_CHANGELOG.md` | 顶部新增版本日志（含日期、执行者、变更清单） |
| `DAILY_WORK_LOG.md` | 顶部新增当日工作日志（含修改清单、待发布文件清单、AI 成本） |
| `PROJECT_STATUS.md` | 版本号更新为"vX.Y.Z 待发布"，新增待发布内容说明 |
| `BUILD_HANDOFF.md` | 版本号更新 + 新增本轮工作说明节 |
| `hugo-site/data/changelog.yaml` | 顶部新增公开 changelog 条目 |

### 治理规则修正输出格式

报告格式必须包含"口径核查"栏目，按以下标注：

| 标注 | 含义 |
|------|------|
| ✅ | 页面/文档已直接体现，无需补充 |
| ⚠️ 部分通过，需补充 | 页面/文档未直接体现，需要本地 Mac 补充说明或操作 |

---

## 二、Hugo 写作工作流

### 文章文件位置

```
hugo-site/content/posts/<slug>/index.md
```

Slug 必须与目录名匹配。

### Front Matter 模板

项目使用 **TOML** 格式（`+++` 分隔符），部分旧文使用 YAML，新文章统一用 TOML：

```toml
+++
title = "Article Title"
date = "2026-06-20"
draft = false
slug = "article-slug"
categories = ["火·AI", "一人公司"]
tags = ["tag1", "tag2"]
description = "简要描述"
cover = "/images/posts/article-slug.png"
cover_alt = "Descriptive alt text"
+++
```

### Key rules

- `draft = false` — draft 文章被 `hugo --buildDrafts` 跳过
- **⚠️ 草稿陷阱（2026-06-19 实测）**：`draft = true` 时 Hugo 默认构建完全跳过该文章，`public/` 里无产出，Pages 404。写完立刻改为 `draft = false`，不要"先放草稿等整理"后再改。
- `categories` 和 `tags` 使用 TOML inline array 格式（`["A", "B"]`），每行一个也行
- `cover` 路径相对于 `static/`：`/images/posts/article-slug.png` → `static/images/posts/article-slug.png`
- **不要用** `cover_status: prompt_ready` — 使用实际的图片路径

### 发布验证测试（构建前自检）

在新增或修改文章后，**必须先本地验证构建输出**，再走发布流程：

1. **构建**：`hugo --cleanDestinationDir`
2. **检查单篇文章输出**：`public/posts/{slug}/index.html` 是否存在
3. **验证 HTML 内容**：title、description、keywords、og:meta 是否正确
4. **确认文章出现在列表**：`public/posts/index.html` 包含文章标题（`grep -c "标题"` 应 ≥ 1）
5. **确认主页有变化**（如适用）：首页 index.html 更新
6. **清理测试痕迹**：测试用完后 `rm content/posts/test-*.md` + 重建

**示例（测试→验证→清理一键流程）**：
```bash
# 创建测试
cat > content/posts/2026-06-20-test-publish.md << 'EOF'
+++
title = "发布测试"
date = "2026-06-20"
draft = false
type = "post"
categories = ["测试"]
tags = ["测试"]
description = "发布功能验证"
+++
测试内容
EOF

# 构建
hugo --cleanDestinationDir

# 验证
ls public/posts/发布测试/index.html && echo "✅ page exists"
grep -c "发布测试" public/posts/index.html && echo "✅ in listing"

# 清理
rm content/posts/2026-06-20-test-publish.md
hugo --cleanDestinationDir
```

### 五行分类系统（五行栏目系统）

网站使用五行作为分类系统，**不是旧 Blogger 栏目**（信仰/教会史/志愿服务/心理学/杂文/经验 等）。

| 五行栏目 | 含义 | 对应旧分类迁移方向 |
|---|---|---|
| 金·判断 | discernment, judgment, analysis | 心理学/哲学/方法/社会/杂文/经验/推荐/笔记/感言/病症/分析 |
| 木·蝉识 | knowledge, recorded wisdom, history | 教会史/个人知识资产 |
| 水·易理 | change, patterns, transformation | 易理 |
| 火·AI | technology, automation, AI era | AI时代/一人公司/系统主控 |
| 土·正见 | correct view, faith, foundation | 信仰/反民粹与反邪/儒家与正见 |

### PaperMod 封面图片标准

| Section | Front matter 字段 | 示例 |
|---------|-------------------|------|
| `posts/` | `cover:`（嵌套，非字符串） | `cover: { image: /images/..., alt: "..." }` |
| `series/` | `images:`（列表，PaperMod 标准） | `images: ["/images/from-clever-to-system.png"]` |

常见错误 `can't evaluate field image in type string` — 这意味着 `cover:` 被设为普通字符串而非嵌套结构。

### 配图生成

使用 Pollinations.ai 生成封面（见 `free-image-generation` 技能）。

**必须包含 `format=png`**：
```
https://image.pollinations.ai/prompt/{encoded}?width=800&height=600&seed=N&nologo=true&format=png
```

验证下载文件时，接受 PNG 和 JPEG 魔术字节（`\\x89PNG...` 和 `\\xff\\xd8\\xff`）。

### Agnes AI 画图 (备选)

当 Agnes AI 配置为 image_gen provider 时：
- **⚠️  `/v1/models` 是公共端点**，不需要认证也返回 200。测试 key 有效必须用 `/v1/images/generations`（返回 401 = key 无效）
- **⚠️  terminal 输出遮蔽**：`grep` config.yaml 看到的 `sk-...H6rl` 不是文件真实内容，用 Python `len()` 或 hex 确认实际 key 长度
- Pollinations 是更可靠的免费方案，Agnes 作为备选
- plugin 依赖 env `AGNES_API_KEY`，s6 环境不自动注入此变量，需 Hermes 自加载 .env 机制

### 草稿模式

用户可能要求先放草稿再自行整理。详见 `references/incoming-draft-pattern.md`。

关键规则：不添加 frontmatter、不放入 `content/posts/`、直接放入 `_incoming/<slug>/index.md`。

### Git Submodule — 必须初始化

PaperMod 主题是 git submodule：

PaperMod 主题是 git submodule：
```
hugo-site/themes/PaperMod → https://github.com/adityatelange/hugo-PaperMod.git
```

在 Mac 上预览前必须初始化：
```bash
cd /Users/macos/angelife.github.com
git submodule update --init --recursive
hugo server -s hugo-site --disableFastRender
```

---

## 三、GitHub Pages 部署

### 关键架构

**GitHub Pages 从 git 仓库根目录直接服务文件，不运行 `hugo build`**。

| 资产位置 | Hugo 构建？ | 在 git？ | GitHub Pages 服务？ |
|---|---|---|---|
| `hugo-site/static/` | → 复制到 `public/` | ✅ 进入 git | ❌ 不自动 |
| `hugo-site/public/` | 每次构建生成 | ❌ 不进入 git | ❌ 不服务 |
| 仓库根目录（如 `/favicon.ico`） | — | ✅ 进入 git | ✅ 直接服务 |

### .github/workflows/hugo.yml 必须存在

workflow 文件必须作为**真实文件**存在于 `.github/workflows/hugo.yml`，不在 git 对象存储中。

正确配置（必须在 `hugo-site/` 子目录构建）：
```yaml
- name: Build with Hugo
  working-directory: hugo-site   # ← 必须指向子目录
  run: hugo --gc --minify --baseURL "${{ steps.pages.outputs.base_url }}/"
- name: Upload artifact
  uses: actions/upload-pages-artifact@v3
  with:
    path: ./hugo-site/public    # ← 必须上传子目录产物
```

### 发布完成验证清单（v0.7.19+ 强制）

Git push 成功 ≠ 任务完成。网站必须可访问才算完成。

| # | 检查项 | 方法 |
|---|--------|------|
| 1 | 网站构建成功 | GitHub Actions workflow `conclusion: success` |
| 2 | GitHub Actions 成功 | API 查询 |
| 3 | 目标页面 HTTP 200 | `curl -I https://target/url/ -m 15` |
| 4 | 抽样验证 ≥3 页面可访问 | 逐个 curl 检查 |
| 5 | 导航链接无 404 | 抽样 nav URLs |
| 6 | 首页正常加载 | `curl -s -o /dev/null -w "%{http_code}" https://angelife.github.io/` |

### 通道 B：自定义服务器（rsync/SSH 发布）

> 用户确认：GitHub push 只是源文件备份，rsync 到自定义服务器才是实际发布。
> 当前 Docker 环境通过 Mac Execution Bridge 完成 rsync。

```
Docker Hermes --SSH--> Mac (macos@host.docker.internal) --rsync--> 服务器
```

**流程：**
1. Hugo 构建在 Docker 内完成：`/opt/data/hugo --minify -s hugo-site`
2. 静态产物：`cp -a hugo-site/public/. /repo/`
3. git commit + tag（源文件备份到 GitHub）
4. 通过 Mac Bridge 执行 rsync 到服务器
5. 发布前必须报用户确认

### GitHub Pages Source 设置（v0.7.22 血训）

**⚠️ Pages Source 必须设为 GitHub Actions（2026-06-19 重现）**

GitHub Pages 有两条独立部署路径：
1. **GitHub Actions 模式**（正确）：workflow 上传 artifact，Pages 服务 artifact — 新文章立即可见
2. **Deploy from a branch 模式**（错误）：Pages 用自己独立的构建，忽略 Actions artifact — 文章永远是旧的，Actions 全绿但 Pages 404

**症状**：Actions `conclusion: success`、git push 成功，但 `https://angelife.github.io/posts/<slug>/` 全部 404。

**修复**：GitHub 仓库 → Settings → Pages → Source → 选择 **"GitHub Actions"** → Save。

Settings → Pages → Source → 必须选择 **"GitHub Actions"**，否则即使 CI 成功，Pages 也使用自己的独立构建，忽略我们的 artifact。

### GitHub Actions CI Debug 命令

```bash
# 等待 Actions 完成
sleep 120

# 检查 Actions 状态
curl -s "https://api.github.com/repos/angelife/angelife.github.com/actions/runs?per_page=1" \
  -H "Accept: application/vnd.github+json" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); r=d['workflow_runs'][0]; print(r['head_sha'], r['status'], r['conclusion'])"

# 检查目标页面
for url in \
  "https://angelife.github.io/" \
  "https://angelife.github.io/series/information-judgment/" \
  "https://angelife.github.io/series/chan-shi-lu/"; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$url" -m 15)
  echo "$code $url"
done
```

---

## 四、Taxonomy 配置（关键陷阱）

### `[taxonomies]` 部分定义会禁用内置 Taxonomy

在 `hugo.toml` 中添加 `[taxonomies]` 时，如果只定义部分 taxonomy：

```toml
[taxonomies]
  series = "series"
```

Hugo 会**静默禁用**内置的 `categories` 和 `tags`。它们停止生成页面，不报错。

**必须包含所有 taxonomy**：
```toml
[taxonomies]
  series = "series"
  categories = "categories"
  tags = "tags"
```

### `mainSections` 是 PaperMod taxonomy filter

`mainSections` 控制 PaperMod taxonomy list 模板显示哪些 section 的文章。如果 `series` 不在 `mainSections` 中，所有 series taxonomy page 显示 0 篇文章。

```toml
mainSections = ["columns", "posts", "series"]
```

### Taxonomy URL 冲突（Section vs Taxonomy）

`content/series/` 创建 Section at `/series/`。`series` Taxonomy 也想要 `/series/`。Hugo 解析为 Section，忽略 Taxonomy 文章。

**解决**：将菜单 URL 改为 section path（英文 slug），而非 taxonomy path（中文）。

| 五行栏目 | 正确 URL |
|----------|---------|
| 金·判断 | `/series/information-judgment/` |
| 木·蝉识 | `/series/chan-shi-lu/` |
| 水·易理 | `/series/yi-notes/` |
| 火·AI | `/series/ai-bu-yin/` |
| 土·正见 | `/series/confucian-framework/` |

### Taxonomy frontmatter 值必须匹配 URL slug

文章中 `series: ["信息判断"]`（中文 display name）不会匹配 `/series/information-judgment/`（英文 URL slug）。必须使用英文 slug：
```yaml
series: ["information-judgment"]
```

---

## 五、关键事故教训

### 事故归档制度

`_private/INCIDENT_REPORTS/` 是重大事故内部手册，必须入 `.gitignore`。

### 发布安全规则（P0 血训）

**最高阻塞规则（INC-20260529-001 血训）**：修 release 脚本的版本，禁止用 release 脚本自发布。release 脚本自发布形成循环依赖。

### `git checkout` 残留文件（v0.7.22 血训）

在 detached HEAD 状态执行 `git checkout {旧commit}` 时，若磁盘文件与目标 commit 内容不同，`git checkout` **不会覆写磁盘**。症状：git status 显示 clean，但实际文件数与 HEAD 不一致。

诊断：
```python
head_files = subprocess.run(["git", "ls-tree", "-r", "HEAD", "--", "content/posts/"], capture_output=True, text=True)
disk_count = len(glob.glob("content/posts/**/*.md", recursive=True))
head_count = len([l for l in head_files.stdout.split('\n') if '.md' in l])
```

### Git 操作安全规则 — 禁止 Docker 端直接 Push（INC-20260620-001 血训）

**2026-06-20 严重事故**：Docker 端 `angelife-clone/` 的 git 仓库落后远程 14 个 commit（停留在 6月3日版 `1dcf332`），在该状态下执行 `git push` 导致覆盖远程 master，线上站点回滚到 6月3日版，所有 6月19日文章不可访问。

#### 核心规则

1. **所有 git push 必须从 `/repo/`（Mac 绑定挂载）执行**。`/repo/` 自动与 Mac 文件系统同步，是权威数据源。
2. **禁止从 Docker 端 `angelife-clone/` 直接 git push**，除非已验证本地 HEAD 与远程一致。
3. **push 前必须执行同步检查**：
   ```bash
   git fetch origin master
   git rev-list --count --left-right origin/master...HEAD
   # 输出示例: "0 3" (本地领先3, 落后0) — 安全可push
   # 输出示例: "0 0" (完全一致)
   # 输出示例: "2 1" 或非 "0 X" 的值 — 有分歧，需要确认
   ```
4. **禁止 `git push --force`**（风险极高，可能覆盖远程历史）。
5. **SSH key 加载**：容器重启后必须重新加载：
   ```bash
   eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_ed25519
   ```
   push 前验证：`ssh -T git@github.com` 确认认证通过。

#### 网站回滚故障恢复流程

当用户报告"网站内容变旧了"时：

1. 查远程 HEAD SHA：`curl -s https://api.github.com/repos/angelife/angelife.github.com/git/refs/heads/master | python3 -c "import sys,json; print(json.load(sys.stdin)['object']['sha'])"`
2. 查 Actions 最近一次成功部署的 SHA：
   ```bash
   curl -s "https://api.github.com/repos/angelife/angelife.github.com/actions/runs?per_page=3&status=success" \
     -H "Accept: application/vnd.github+json" | \
     python3 -c "import sys,json; [print(r['head_sha'][:7], r['display_title']) for r in json.load(sys.stdin)['workflow_runs']]"
   ```
3. 查 `/repo/` 本地 HEAD：`cd /repo && git log --oneline -1`
4. 如果本地 HEAD 正确但远程错误 → force-push 恢复：
   ```bash
   cd /repo
   git fetch origin master
   git push origin master --force  # 仅在确认本地 HEAD 是正确版本后执行
   ```
5. 等待 GitHub Actions 重新部署，然后验证线上的 6 项检查清单（见"发布完成验证清单"）。

### `git add -A` 部分失败（v0.7.20 新增）

`git add -A` 遇到中文文件名时可能在内部 pipe 处理中部分失败，但 commit 仍完成（只 commit 了成功 add 的文件），没有错误提示。

**commit 后必须立即验证**：
```bash
git ls-tree -r HEAD -- {path} | grep "\.md$" | wc -l
```
对比本地 `ls {path}/*.md | wc -l`，不一致说明有文件未进 commit。

### `git status --short` 干净不等于 commit 完整

`git status --short` 只报告 tracked 文件变更，**不报告 untracked 文件**。organize script 批量创建文件后，即使 `git status --short` 显示 clean，80 个文件可能仍留在 working directory 作 untracked。

### 中文文件名 GitHub push 成功但 raw CDN 返回 404（v0.7.19 血训）

包含中文字符的文件名 `git commit` 成功且 `git ls-tree` 显示，但 GitHub raw content URL 返回 HTTP 404。Workaround：重命名为拼音后再 push。

### Hugo slug 生成去除 `[]` 括号（v0.7.6 血训）

Hugo 处理 title 字符串时去除 `[]` / `（）` 括号生成 URL slug。迁移脚本从文件名生成 slug 时应同步去除。

### PaperMod RSS 模板不兼容 Hugo 0.124+（v0.7.12 血训）

Hugo 0.124+ 将 `site.Author` 改为 `interface{}`。即使 `{{ with site.Author }}` 也报错。必须使用 `site.Params.author` 覆盖。

---

## 六、发布安全

### 受控发布脚本

正式发布必须使用 `tools/angelife-release`，不得裸跑 git 命令。详见 `AI_WORK_RULES.md`。

### rsync 静默规则

rsync 详细输出必须重定向到日志文件，不得刷屏：
```bash
rsync -a --delete hugo-site/public/ ./ > "$RSYNC_LOG" 2>&1
```

### changelog.yaml 必须 YAML 验证后再插入

1. 用 Python `yaml.safe_load` 预验证格式
2. 按 `releases` 数组结构插入（最新版本在前）
3. Hugo 构建验证通过后才能 release

---

## Container 环境限制

### 文件系统架构

```
Mac OS          Docker 容器
/Users/  ──bind──→  /run/host_mark/Users
                       ├── /opt/data/        （Docker working dir, session data）
                       └── /workspace/angelife.github.com/
                              └── /repo → /workspace/angelife.github.com/  （symlink）
```

**要点**：
- `/repo/` 是 Mac `~/angelife.github.com/` 的**直接绑定挂载**（非独立副本）
- 验证方法：`readlink -f /repo` → `/workspace/angelife.github.com`；`df -h /repo` → `/run/host_mark/Users`
- 在 `/repo/` 写入文件 → **立即可见**在 Mac `~/angelife.github.com/`
- 这意味 Docker 内 `hugo build` 可以直接输出到 Mac 本地仓库，不需要额外拷贝
- 但 Git 操作（push/fetch）建议在 Mac Terminal 侧执行（SSH key 和网络更稳定）

### 已知限制

- **Docker 内 Hugo 可用**：`/opt/data/hugo v0.162.1`（此 Docker 实例有 Hugo 二进制）
- **rsync 不可用**：容器内无 rsync 二进制，用 `cp -a hugo-site/public/. /repo/` 代替
- **USB 设备不可穿透**：Docker 容器内看不到 /Volumes/Kindle 等 Mac USB 设备
- **通过 Mac Execution Bridge 可以打通执行断层**（详见下节）

### Mac Execution Bridge（打通执行断层）

所有上述限制的**根因**：Hermes 的控制平面在 Docker，执行平面在 Mac。这不是单个工具缺失问题，是架构断层。

**Bridge 方案**（详见 `kindle-jailbreak` 技能中的 Mac Execution Bridge 章节）：

```
Hermes (Docker) ←─SSH→ Mac executor (轮询) → Hugo build / rsync / git
```

| Bridge 动作 | 替代原来 | 
|-------------|---------|
| `hugo_build` | 在 Mac 上跑 `hugo --minify` |
| `rsync_deploy` | 在 Mac 上跑 rsync 到服务器 |
| `shell` | 在 Mac 上跑任意命令 |

**Bridge 启动**（Mac 上跑一次）：
```bash
mkdir -p ~/bridge/outbox
# 传 executor 脚本（从 Docker）
scp -o StrictHostKeyChecking=no -i ~/.ssh/id_ed25519 \
    /opt/data/bridge/mac_executor.sh \
    macos@host.docker.internal:~/bridge/
# 启动
nohup bash ~/bridge/mac_executor.sh &
```

**Bridge 就绪后**，Hermes 可以直接触发 Hugo 构建和 rsync 部署：

### ⚠️ Mac Execution Bridge — 关键陷阱（2026-06-12 血训）

#### 1. Bridge shell stdout 不可靠
Bridge 的 `shell` 命令回传的 stdout 可能**不完整或被截断**：
- 大量文件 rsync 失败时（如 `open (2)` errors），stdout 被截断到 ~100K chars
- 有时 `ls` 输出为空但目录实际存在（SSH 链路不稳定或 executor 轮询间隔导致）
- **规则**：不要仅凭 Bridge shell 的 stdout 判定文件是否存在。关键路径（目录存在性、文件完整性）需用 `--wait` 模式 + 显式 exit code 检查，或请用户在 Mac Terminal 上直接 `ls` 确认。

#### 2. `--wait` 比异步模式更可靠
`bridge_send.py --wait shell '{}'` 阻塞等待结果，返回更完整的 stdout。
异步模式（`bridge_send.py shell` → `sleep N` → `bridge_check.py`）有时会丢失 stdout 内容（仅返回 `{}`），导致误判：
```bash
# 推荐（阻塞等待，结果更完整）
python3 /opt/data/bridge/bridge_send.py --wait shell '{"commands":["ls -la ~/angelife.github.com/"]}'

# 不推荐（可能丢失 stdout）
python3 /opt/data/bridge/bridge_send.py shell '{"commands":["ls -la ~/angelife.github.com/"]}'
sleep 6
python3 /opt/data/bridge/bridge_check.py cmd_xxx
```

#### 3. SSH 超时是重复故障模式
Mac Bridge 执行 git push/clone/fetch 时 SSH 经常超时（`SSH timeout`），原因可能是：
- Docker 容器内 SSH key 加载不足（`ssh-add` 状态丢失）
- `host.docker.internal` 路由不稳定
- Mac 端 sshd 的连接数限制
- **workaround**：对 git 操作设 `--wait` + 较长 timeout（30s+），失败后重试一次

#### 4. `rm -rf` 在 Bridge 上可能比预期删除更多
Bridge shell `rm -rf` 由于路径解析差异或 executor 的 cwd 问题，可能删除目标之外的目录。
- **规则**：不要通过 Bridge 执行递归删除。需要清理文件时，逐个文件指定路径，或请用户在 Mac Terminal 上操作。
- 替代方案：用 `cp -a` 覆盖而非 `rm + cp`。

#### 5. Git 操作首选 Mac 本地终端
GitHub 认证（SSH key）、git push/clone 等操作在 Mac 终端比在 Docker 内稳定得多。
- Docker 内 `git push` 遇到中文路径或 SSH key 问题时经常失败
- **当 Bridge SSH 不稳定时**：直接告知用户用 Mac Terminal 执行具体命令，而不是反复通过 Bridge 重试

---

## 七、审查其他代理的修改（剑妈/Codex/Claude Code）

### 触发条件

用户要求"检查别人改了什么"、"看看有什么问题"、"审查改动"等，指向未 commit 的本地改动。

### 工作流

1. **先确认范围**：用户说"检查网站"时，必须先判断是否是指**本地未 commit 改动**而非线上。Angelife 项目优先检查 `git status`——很多改动尚未 push。

2. **git status → git diff**：
   查看未 commit 和 untracked 文件，评估改动量级和涉及范围。

3. **逐项审查**：对每个改动文件分类检查：
   - `hugo.toml` — 导航菜单是否保留五行栏目？baseURL/theme/taxonomies 是否改变？
   - `layouts/` — 是否覆盖了 PaperMod 默认模板？是否删除了分页、面包屑、火·AI交叉查询逻辑？
   - `css/` — 是否重写了五行配色体系？备份文件是否存在？
   - 新增文件 — 是否新增了自定义 templates/cover/partial 导致覆盖？

4. **检查清单（针对剑妈型改造）**：

   | 检查项 | 安全态 | 危险信号 |
   |--------|--------|---------|
   | 五行导航 | 保留所有 7 项 | 被简化为"文章/栏目/归档" |
   | list.html | 有 Paginator 分页 + IsHome 过滤 | 变成无分页 flat `.Pages` |
   | 火·AI交叉 | category 交叉查询存在 | 被删除 |
   | single.html | 面包屑/草稿标记/paperMod meta | 精简到标题+日期 |
   | CSS 五行变量 | `--phase-*` 变量保留 | 被替换为黑白灰 |
   | 首页 | "精于心简于形"入口页 | 改为文章列表 |
   | baseof.html | 未被覆盖 | 被自定义覆盖 |

5. **运行 Hugo build 验证**：
   关注 Pages 总数、0 errors、static files 数量。

6. **总结报告格式**：
   - 先给结论（有/无问题，严重程度）
   - 逐文件列出改动内容，标注删了什么、增加了什么
   - 🔴 数据/功能丢失 / 🟡 功能退化 / 🟢 风格变化
   - 附备份文件位置

---

## 八、网站改版原则（用户偏好 v2026-06-12）

### 核心原则：主题默认优先

用户明确偏好：**不要从零写自定义 CSS/模板，先用 PaperMod 默认效果，在其基础上少量修改。**

错误做法（别再做）：
- ❌ 写大量自定义 CSS（`.simple-home` 等）并覆盖主题布局
- ❌ 删掉 `layouts/index.html` 然后手写完整首页模板
- ❌ 自定义首页 + 自定义文章列表样式

正确做法：
1. **删掉自定义 layouts/index.html**，让 PaperMod 的 `_default/list.html` 渲染首页
2. 首页内容写在 `content/_index.md`（markdown body 自动显示在列表前）
3. 只调整 `hugo.toml` 参数（开关、文字、布局选项）
4. 只有非常必要时才加少量 CSS（在 `static/css/` 追加，不覆盖主题文件）

### 精简版配置参数（简洁路线）

当走"精于心，简于形"路线时：

```toml
[params]
  defaultTheme = "light"
  ShowReadingTime = false
  ShowBreadCrumbs = false
  ShowPostNavLinks = false
  ShowCodeCopyButtons = false
  DateFormat = "2006-01-02"
  mainSections = ["posts"]  # 只显示 posts，不显示 columns/series
```

### 首页简化的正确方式

1. `content/_index.md` 写 markdown 内容（栏目链接、关于信息）
2. PaperMod 自动在内容下方列出文章列表（由 `_default/list.html` 渲染）
3. 如果需要在首页额外过滤文章，改 `hugo.toml` 的 `mainSections` 即可
4. 去掉花哨：封面图、导航面包屑、阅读时间估算、上一篇/下一篇链接

### 版本升级时检查

| 配置项 | 旧值（花哨） | 新值（简洁） |
|--------|-------------|-------------|
| `ShowReadingTime` | true | false |
| `ShowBreadCrumbs` | true | false |
| `ShowPostNavLinks` | true | false |
| `mainSections` | `["columns", "posts", "series"]` | `["posts"]` |
| 自定义首页模板 | 复杂 card/grid 布局 | 删掉，用主题默认 list |

---

## 八、内容合并规则

**写新文章前必须查重**：

| 情况 | 操作 |
|------|------|
| 内容高度相似或重叠 | **合并到现有文章** — 添加新角度到旧文，保持原 URL/slug |
| 同一主题，不同角度 | **链接和交叉引用** — 添加内部链接 + tags/series 分类 |
| 真正独立的新话题 | 写新文章 |

### 迁移后内容去重（Post-Migration Dedup）

从旧站（Blogger）批量导入历史文章后，需要对比新导入的旧文章 vs 现有新站文章，按以下逻辑处理：

1. **同内容不同标题** → 保留新站版本（7-10字短标题），删除旧版本
2. **旧站特有内容**（新站未覆盖）→ 保留旧文章

**实践方法论（2026-06-20 实测）**：

1. **列出双方文章清单**：对比 git tracked vs untracked 文件。`git ls-tree -r HEAD --name-only` 列出已有文章，`git ls-files --others --exclude-standard` 列出新导入文章。
2. **检查标题相似度**：逐篇提取 title frontmatter，按主题分组（反邪教、志愿服务、教会史、心理学等），寻找可能重复的标题。
3. **关键词交叉搜索**：在新站文章中搜索旧文的关键词（如"白岩松""东方闪电""克尔凯郭尔"），看是否有重叠。`grep -rl` 在新站 article 目录排除旧文目录。
4. **内容比对**：对疑似重复的文章，实际读取文章内容（read_file 前 30-50 行），确认是否为同一篇文章。特别注意"由旧稿整理而来"的改写版——改写版（2025+ 短分析框架）和原旧文（2011-2012 长篇第一手记录）有独立价值，不是重复。
5. **文件大小比对**：用 `wc -c` 对比文章大小，明显不同的文章不是重复。
6. **分类和系列检查**：同一系列名（如 information-judgment）不等同于内容重复，要读实际内容判断。

详见 `references/blogger-hugo-migration.md` 中的「Post-Migration Content Deduplication」章节。

**关键陷阱**：
- "由旧稿整理而来"的改写文章 ≠ 内容重复。改写版（2025+）是短分析框架，原旧文（2011-2012）是长篇第一手记录，两者有独立价值。
- 同一系列名 ≠ 同一内容。新旧文章可能共用 `information-judgment` 系列但主题不同。

---

## 参考资料

### 核心治理参考
- `references/article-frontmatter-format.md` — frontmatter 标准格式
- `references/article-writing-workflow.md` — 写作完整工作流
- `references/changelog-yaml-rules.md` — changelog.yaml 写入规则
- `references/release-script-safety.md` — 发布安全规则
- `references/incident-reporting.md` — 事故归档速查
- `references/vault-auto-commit-and-git-workflow.md` — vault 自动提交行为

### Hugo 技术参考
- `references/front-matter-examples.md` — 真实文章 front matter 示例
- `references/hugo-pitfalls.md` — Hugo 常见陷阱
- `references/hugo-template-override-pitfalls.md` — 模板覆盖问题
- `references/papermod-rss-override.md` — PaperMod RSS 模板修复
- `references/blogger-hugo-migration.md` — Blogger 迁移脚本
- `references/wuxing-five-element-classification.md` — 五行分类系统

### 部署与 GitHub Pages
- `references/github-pages-deploy-lessons.md` — GitHub Pages 部署事故速查
- `references/disabled-workflow-debug.md` — workflow 缺失诊断
- `references/pages-deployment-source.md` — Pages 两套独立部署路径
- `references/chinese-filename-github-404.md` — 中文文件名问题
- `references/ssh-key-setup.md` — SSH key 配置
- `references/git-checkout-residue.md` — git checkout 残留文件

### Taxonomy 与结构
- `references/mainSections-taxonomy-filter-bug.md` — mainSections filter bug
- `references/taxonomy-architecture.md` — series/ vs posts/ vs columns/ 渲染逻辑
- `references/section-taxonomy-url-conflict.md` — Section/Taxonomy URL 冲突
- `references/columns-series-slug-conflicts.md` — columns/ 与 series/ slug 冲突
- `references/series-flat-files-not-duplicates.md` — series/ flat files 不是重复

### 图片与 Pollinations
- `references/pollinations-cover-generation.md` — Pollinations 配图
- `references/batch-cover-generation.md` — 批量封面生成
- `references/picflex-api.md` — PicFlex API

### 发布与版本
- `references/version-sync.md` — 版本号同步
- `references/version-audit-v0712.md` — 版本对齐审计
- `references/changelog-insertion-pattern.md` — changelog.yaml 插入位置

### 其他
- `references/docker-bind-mount-hugo-debug.md` — Docker bind mount + Hugo
- `references/hugo-html-injection-workaround.md` — HTML 注入 workaround
- `references/security-rsync.md` — 安全 rsync
- `references/server-deploy-workflow.md` — 服务器部署工作流
- `references/severity-rules.md` — 事故等级

### 脚本
- `scripts/slug-conflict-scan.py` — slug 冲突扫描（series/ vs posts/、MD5 去重）

### 审计参考
- `references/uncommitted-changes-audit.md` — 未 commit 改动审计要点与实战案例

---

## 相关技能

- `free-image-generation` — Pollinations/PicFlex 免费配图生成（被本技能引用）