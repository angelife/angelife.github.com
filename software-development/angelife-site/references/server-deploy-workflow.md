# 发布与部署工作流（v0.7.19 完整版）

## 重要澄清

**angelife 的部署目标是 GitHub 仓库 + GitHub Pages。**

- Hugo 源文件仓库：`git@github.com:angelife/angelife.github.com.git`
- GitHub Pages 从仓库根目录的静态文件提供服务
- 不是"自定义服务器 rsync"，也不需要额外上传步骤

## 发布完成标准（强制，v0.7.19+）

**Git Push 成功 ≠ 任务完成。网站可访问才算完成。**

| # | 检查项 | 验证方法 |
|---|--------|----------|
| 1 | 网站构建成功 | GitHub Actions `conclusion: success` |
| 2 | GitHub Actions 成功 | API 查询 workflow runs |
| 3 | 目标页面 HTTP 200 | `curl -I <URL> -m 15` |
| 4 | 抽样验证 ≥3 页面 | 逐个 URL 检查 |
| 5 | 导航链接无 404 | 抽样检查栏目菜单 |
| 6 | 首页正常加载 | `curl -s -o /dev/null -w "%{http_code}" https://angelife.github.io/` |

**验证顺序**：Push 后等 ~2 分钟 → 查 Actions → 逐个 HTTP 检查 → 全部 200 才算完成。

**阻塞时必须声明原因**，不得将"Git Push 成功"视为完成。

## 正确的发布流程

```
1. Hugo 源文件 commit + push（GitHub Actions 自动构建）
   cd /workspace/angelife.github.com
   git add <精确文件>
   git commit -m "vX.Y.Z: ..."
   git push origin master

2. 等待 GitHub Actions 完成（约 2 分钟）
   curl -s "https://api.github.com/repos/angelife/angelife.github.com/actions/runs?per_page=1" \
     -H "Accept: application/vnd.github+json" | \
     python3 -c "import sys,json; d=json.load(sys.stdin); r=d['workflow_runs'][0]; print(r['head_sha'], r['status'], r['conclusion'])"

3. 验证所有 6 项标准（见上表）
```

## Hugo Section vs Taxonomy URL 架构（v0.7.19 实测）

**发现问题**：中文 taxonomy 页面（`/series/信息判断/`）在 GitHub Pages 上 404，本地正常。

**根因**：`content/series/english-slug/_index.md` 创建 **Section** 页面（`/series/english-slug/`），posts 的 `series: [中文]` 字段应生成 **Taxonomy** 页面（`/series/中文/`），但 GitHub Pages 构建版本中后者未生成。两套 URL 指向不同内容。

**已验证结果**：
- `/series/information-judgment/`（Section）→ **200** ✅
- `/series/信息判断/`（Taxonomy）→ **404** ❌

**已采用修复**：菜单 URL 从中文 taxonomy 路径改为英文 section 路径（`/series/information-judgment/` 等），所有栏目页恢复正常。

**不要用静态重定向**：之前的重定向方案（`static/series/english-slug/index.html` → `meta refresh`）会导致无限重定向循环，因为 Hugo 生成的内容和静态重定向路径重叠。

## 历史纠正（v0.7.16 实测纠正）

INC-20260529-001 后形成的"必须 rsync 到自定义服务器"认知是事故后的过度补偿。实际项目使用 GitHub Pages，无需自建服务器。若确实需要自建服务器（独立域名、跳过 GitHub Pages），才需要 rsync 到 VPS。

## 禁止事项

- ❌ 假设存在"自定义服务器"需要 rsync 上传
- ❌ push 后声称"待服务器上线"——GitHub Pages 就是上线地址
- ❌ 猜测部署目标而不直接问用户
- ❌ 将"Git Push 成功"视为任务完成（v0.7.19+ 强制禁止）
- ❌ 用静态重定向解决 Hugo Section/Taxonomy URL 冲突（会循环）

## 服务器连接信息（仅当真正需要自建服务器时）

SSH 连接信息存储在 Mac 本机 `~/.ssh/config`，Docker 容器内不可见。fingerprint（SHA256:OwABsi6upN34A5hoi2542vCrYmy4BwxNUgxBIesr01Y）可验证服务器身份，但不能反推 IP。若服务器 IP 找不到，直接问用户。

## 快速诊断命令

```bash
# 检查所有栏目页
for slug in information-judgment chan-shi-lu yi-notes ai-bu-yin confucian-framework anti-populism; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "https://angelife.github.io/series/$slug/")
  echo "$slug: $code"
done

# 检查 Actions 最新状态
curl -s "https://api.github.com/repos/angelife/angelife.github.com/actions/runs?per_page=1" \
  -H "Accept: application/vnd.github+json" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); r=d['workflow_runs'][0]; print(r['head_sha'][:8], r['status'], r['conclusion'])"
```