# Hugo 构建流程（Docker NVIDIA 独立执行）

## 触发条件

用户说「直接发布」「本地生成页面」或要求执行 Hugo 构建时，触发本流程。

## 完整步骤

### 1. 确认 Hugo 源文件位置

```
/workspace/angelife.github.com/hugo-site/   ← Hugo 源（content/layouts/themes 等）
/workspace/angelife.github.com/              ← Hugo 产物输出目录（public/ 里的文件）
```

**不是** `/repo/hugo-site/` — 仓库直接在 `/workspace/angelife.github.com/`。

### 2. 下载 Hugo（若未安装）

```bash
export PATH="$HOME/bin:$PATH"
cd /tmp
curl -sL https://github.com/gohugoio/hugo/releases/download/v0.147.0/hugo_extended_0.147.0_linux-amd64.tar.gz -o hugo.tar.gz
tar -xzf hugo.tar.gz hugo
mv hugo ~/bin/
hugo version   # 验证
```

**版本要求**：PaperMod 主题要求 Hugo ≥0.146.0。老版本会报错：
```
ERROR => hugo v0.146.0 or greater is required for hugo-PaperMod to build
```

### 3. 构建

```bash
export PATH="$HOME/bin:$PATH"
cd /workspace/angelife.github.com/hugo-site
hugo --destination /workspace/angelife.github.com 2>&1 | tail -20
```

成功输出示例：
```
                   | EN
-------------------+------
  Pages            | 427
  Paginator pages  |  37
  Non-page files   |   7
  Static files     | 462
  Processed images |  14
  Aliases          | 116
Total in 6911 ms
```

### 4. 常见报错与修复

| 报错 | 原因 | 修复 |
|------|------|------|
| `partial "google_analytics.html" not found` | PaperMod 主题引用缺失文件 | `touch layouts/partials/google_analytics.html` |
| `hugo-PaperMod to build` | Hugo 版本 < 0.146.0 | 升级到 v0.147.0 |
| `Module "PaperMod" is not compatible` | Hugo 版本 < 0.146.0（同上） | 同上 |
| `Permission denied` 写 /usr/local/bin | 无 root 权限 | `mv hugo ~/bin/` 加 PATH |

### 5. Git 提交与发布

vault 每 ~10 分钟自动 commit Hugo 产物（commit 无描述消息）。NVIDIA 应：

```bash
cd /workspace/angelife.github.com
git add <具体文件>   # 不要 git add .
git commit -m "v0.X.Y: 描述"
git tag v0.X.Y
git push origin master
git push origin v0.X.Y
```

**版本状态文件同步**（若需要）：
- `README.md` — 版本号
- `PROJECT_STATUS.md` — 版本+commit+发布状态

## 架构速查

```
/workspace/angelife.github.com/          ← git 仓库根目录（= 线上 public 内容）
  hugo-site/                              ← Hugo 源文件
    content/  layouts/  themes/  data/     ← 编辑内容在这里
    public/                               ← Hugo 构建产物（不要直接编辑）
  posts/  categories/  about/  index.html  ← Hugo 产物（由 hugo-site/public/ 输出到这里）
  hugo-site/public/                       ← 构建中间目录（无用，输出到了上级）
```

构建命令中 `--destination /workspace/angelife.github.com` 表示直接输出到仓库根目录（覆盖原 Hugo 产物）。

## Git push 时机

vault 会自动 commit Hugo 产物。NVIDIA 做版本更新后应立即 push，避免 vault commit 打断工作流。