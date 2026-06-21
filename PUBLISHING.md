# 木同学发稿规则 (PUBLISHING RULES)

## 核心原则
- 木同学负责**写文章**，土同学负责**发布**
- 木同学**不得在容器内执行任何 git push 操作**（不论是 `--force` 还是普通 push）
- 木同学**不得自行修改 git 历史**、不得 force push、不得 rebase

## 木同学的发文流程

### 1. 写文章
将 `.md` 文件写入以下目录：
```
/workspace/angelife.github.com/hugo-site/content/posts/<your-article>/index.md
```
这个目录通过 bind mount 与 Mac 宿主机实时同步，土同学能立即看到。

### 2. 文章格式要求
- frontmatter 必须有 `title`、`date`、`categories`、`tags`
- categories 取值：金·判断 / 木·蝉识 / 水·易理 / 火·AI / 土·正见
- 署名规范：`—— 木 · 安知生`
- 文件路径推荐 slug 名称（英文或拼音），不要用中文

### 3. 通知发布
写完后在群里 @土同学，说「文章已就绪，请发布」
土同学会从 Mac 宿主执行：
```bash
hugo --gc --minify -s hugo-site
git add -A
git commit -m "posts: <your-article-title>"
git push origin master
```
GitHub Actions 自动部署。

## 仓库说明 (木同学注意!)

### 容器内有两个网站仓库

| 路径 | 用途 | git push 权限 |
|------|------|---------------|
| `/workspace/angelife.github.com/` | **正式工作目录**，bind mount 与 Mac 实时同步 | ❌ 禁止 push |
| `/opt/data/angelife-clone/` | **冷备份**，保留旧版资料供查阅 | ❌ 完全禁止 git 操作 |

### 注意事项
- 写文章**必须**用 `/workspace/angelife.github.com/`（bind mount），不要用 `angelife-clone`
- `angelife-clone` 是旧的冷备份，仅供**只读查阅**，禁止在任何情况下从中执行 git push
- 容器内没有 SSH key，即使 push 也会失败，请不要尝试

## 有疑问
在群里 @土同学 或 @金同学 沟通，不要自行尝试绕过。
