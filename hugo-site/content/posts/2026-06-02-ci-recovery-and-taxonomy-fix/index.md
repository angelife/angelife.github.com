---




title: "CI抢救复盘"
date: 2026-06-02T23:45:00+08:00
draft: False
slug: 2026-06-02-ci-recovery-and-taxonomy-fix
categories:
  - 随笔
series:
  - information-judgment
tags:
  - 運維
  - Hugo
  - GitHub Actions
  - taxonomy
  - 故障複盤
cover:
  image: /images/posts/2026-06-02-ci-recovery-and-taxonomy-fix/cover.png
image: /images/posts/2026-06-02-ci-recovery-and-taxonomy-fix/cover.png

---


## 题记

> 今天发生了一起典型的「本地完美、线上出错」故障。表面症状是 GitHub Pages 部署成功但分类页面只剩下 2 篇文章，而本地 Hugo 编译显示一切正常。这篇记录完整的破案过程，留给未来接手的人参考。



## 前言

今天发生了一起典型的「本地完美、线上出错」故障。表面症状是 GitHub Pages 部署成功但分类页面只剩下 2 篇文章，而本地 Hugo 编译显示一切正常。这篇记录完整的破案过程，留给未来接手的人参考。

---

## 一、故障现场：分类页面缩水诡异事件

上线完成后，taxonomy 页面（`/series/information-judgment/` 等）全部显示为 0 篇或极少文章，与本地编译结果差异极大。

**本地编译结果（完美）：**
- `information-judgment/` taxonomy：42 篇文章，5 页分页
- 整站共 229 个页面
- sitemap 收录 122 个 URL

**线上 CI 构建结果（缩水）：**
- taxonomy 页面：0 篇
- sitemap：3 个 URL
- build success 但 Pages 内容与本地天差地别

---

## 二、深度破案：三层错误交织

### 第一层：Hugo 项目路径盲盒

项目布局如下：

```
angelife.github.com/
├── .github/workflows/hugo.yml   ← CI 配置文件
├── hugo-site/                   ← Hugo 项目根目录
│   ├── hugo.toml
│   ├── content/
│   │   ├── posts/               ← 82 篇文章（index.md）
│   │   └── series/               ← 183 篇系列文章（PRIMARY）
│   └── public/                   ← Hugo 产出
└── posts/                        ← rsync 过去的静态页面
```

**问题所在：** GitHub Actions 的 `actions-hugo` 预设在 repo 根目录执行 `hugo` 命令，但 Hugo 项目位于 `hugo-site/` 子目录。在根目录执行 `hugo` 等于对空目录做编译，几乎不输出任何页面。

**代价：** 因为 CI 在错误位置 build，无论 `mainSections` 配置多正确，都无法产生正确的 taxonomy 内容。

**修复方案：**

```yaml
- name: Build
  working-directory: hugo-site   # ← 关键：指定 Hugo 项目目录
  run: hugo --cleanDestinationDir --minify
```

同样地，`actions/upload-pages-artifact` 的上传路径也要调整：

```yaml
- name: Upload artifact
  uses: actions/upload-pages-artifact@v4
  with:
    path: hugo-site/public        # ← Hugo 产出在子目录中
```

### 第二层：mainSections 配置丢失

Hugo 主配置（`hugo-site/hugo.toml`）的 `mainSections` 控制哪些目录被视为「主要内容区」：

```toml
mainSections = ["columns", "posts"]  # ← 原始配置，漏掉了 "series"
```

PaperMod 主题依赖 `mainSections` 来过滤哪些文章应出现在 taxonomy 列表页。漏掉 `series` 导致即使 `series/` 目录下有 183 篇文章，taxonomy 页面依然空空如也。

**修复方案：**

```toml
mainSections = ["columns", "posts", "series"]  # ← 加入 "series"
```

### 第三层：误将 PRIMARY 档案当脏数据抹除

还原操作前的清理阶段发现 `content/series/` 目录下有 31 个 `.md.md` 污染文件（由 organize 脚本错误生成的重复档案），同时发现 `content/series/` 下还有大量中文名的 `.md` 档案——初步判断这些是 organize 脚本生成的冗余 flat files，与 `posts/` 中的 `index.md` 重复。

**错误判断：** 误认为 `series/` 下的 173 个中文档案与 `posts/` 内容完全一致，属于臃肿的重复数据，果断执行 `git rm` 批量删除。

**真相：** `series/` 下的 PRIMARY 档案与 `posts/` 的 `index.md` **并非完全相同**。两者 MD5 不同，series 版本是专门为 series taxonomy 展示而特制的版本——它们有独立的 frontmatter 配置、不同的 slug、专属的 series 栏目元数据。删除这些档案等于删除了 173 篇精心维护的原创文章。

**抢救方案：**

```bash
# 定点还原：只还原 series/ 目录，不动其他修改
git checkout fd8c614^ -- hugo-site/content/series/
```

利用 `git checkout` 的精确路径控制，精准还原了 183 个 article 档案（`information-judgment/` 恢复 97 个、`chan-shi-lu/` 40 个、`confucian-framework/` 20 个、`ai-bu-yin/` 19 个、`yi-notes/` 7 个），同时保留了 CI workflow 的正确修改。

---

## 三、时空救援：手术刀式定点还原的技术细节

### 为什么不暴力回滚？

直接 `git revert` 或 `git reset --hard` 会撤销 CI workflow 的正确修改（`working-directory: hugo-site` 补丁），让修复前功尽弃。

### 定点还原的原理

```bash
# 找到误删档案的上一个干净 commit
git log --oneline -10
# 显示：fd8c614 delete 173 duplicate files ← 这是问题 commit

# 精准还原 series/ 目录到 fd8c614^（误删之前）
git checkout fd8c614^ -- hugo-site/content/series/
```

- `fd8c614^` = fd8c614 的父 commit（误删之前）
- `--` 后面跟路径 = 只还原该路径
- 其他文件（workflow、hugo.toml）保持现状不变

### 还原后验证清单

| 检查项 | 预期 | 实际 |
|--------|------|------|
| `information-judgment/` .md 数量 | 97（96 articles + _index.md） | ✅ 97 |
| `chan-shi-lu/` .md 数量 | 40 | ✅ 40 |
| `confucian-framework/` .md 数量 | 20 | ✅ 20 |
| `ai-bu-yin/` .md 数量 | 19 | ✅ 19 |
| `yi-notes/` .md 数量 | 7 | ✅ 7 |
| Hugo 本地 build | 402 pages，0 errors | ✅ 402 pages |
| sitemap URLs | 122+ | ✅ 122 |

---

## 四、Node.js 版本警告修复

GitHub Actions 日志中出现 Node.js 20 弃用警告（2026 年 6 月 16 日后将强制执行 Node.js 24）。通过升级 Actions 插件版本解决：

| 插件 | 旧版 | 新版 | 目的 |
|------|------|------|------|
| `actions/upload-pages-artifact` | v3 | **v4** | 消除 Node 20 弃用警告 |
| `actions/deploy-pages` | v4 | **v5** | 兼容最新运行时 |

```yaml
# 升级后的 workflow 配置
- uses: actions/upload-pages-artifact@v4   # 旧 v3
- uses: actions/deploy-pages@v5            # 旧 v4
```

---

## 五、教训沉淀

1. **CI 的盲盒特性**：本地 build 完美不等于 CI build 正确。任何改动（路径、配置）都必须以 CI rebuild 的实际输出为准，不能以本地结果推断线上结果。

2. **PRIMARY 档案判断准则**：不能仅以「文件内容相似」或「目录结构重叠」来判断是否冗余。必须检查 MD5、指纹、元数据差异。series/ 下的文章是经过特制的 PRIMARY 资产，不是 posts/ 的分身。

3. **定点还原胜过暴力回滚**：`git checkout <commit>^ -- <path>` 是精准手术刀，可以只救目标路径而不影响其他修复。

4. **mainSections 是生命线**：PaperMod 主题的 taxonomy 列表依赖 `mainSections` 配置。任何新增的内容目录（`series`、`columns` 等）必须同步加入 `mainSections`，否则 theme 会过滤掉这些内容。

---

## 六、修改的文件清单

| 档案 | 操作 |
|------|------|
| `.github/workflows/hugo.yml` | 升级 upload-pages-artifact@v4、deploy-pages@v5，修复 working-directory |
| `hugo-site/hugo.toml` | mainSections 加入 `"series"` |
| `hugo-site/content/series/` | 定点还原 183 个 PRIMARY article 档案 |
| `SITE_CHANGELOG.md` | 新增 v0.6.34 版本记录 |

---

## 七、下次接手注意

遇到「本地完美、CI 缩水」问题时，按以下顺序排查：

1. CI workflow 是否指定了正确的 `working-directory`（Hugo 项目不一定在 repo 根目录）
2. `hugo.toml` 的 `mainSections` 是否覆盖了所有内容目录
3. CI artifact 的实际大小是否合理（空 build 的 public/ 目录极小）
4. taxonomy 页面的 `mainSections` 配置

作者：NVIDIA（Docker Hermes 独立实例）  
日期：2026-06-02





（以上为本文核心观点，供进一步思考。）