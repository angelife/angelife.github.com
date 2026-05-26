# Codex Handoff：angelife Hugo 新站

## 项目路径

Hugo 源码目录：

/Users/macos/angelife.github.com/hugo-site

GitHub Pages 仓库根目录：

/Users/macos/angelife.github.com

线上站点：

https://angelife.github.io/

## 新站定位

AI时代的正见与系统化。

核心口号：

儒家为体，AI 为用，易理为象，技术为器，作品为证。

## 已完成工作

1. 首页文案已重写。
2. 关于页已重写，并加入：
   - 新站制作过程
   - ChatGPT / Codex / Reasonix / DeepSeek / 人 的协作分工
   - 为什么选择 Obsidian
   - 系统维护方式
   - Mermaid 协作流程图
3. 五篇新站核心文章已重写。
4. 两篇旧文已按 KISS 原则改造成新版整理稿。
5. 新增十篇文章，覆盖：
   - AI时代重新开局
   - 从聪明到系统化
   - 信息源瘦身
   - 公共理性与反操弄
   - 边界感
   - 结丹隐喻
   - 元婴隐喻
   - 个人网站
   - Kindle / KOReader / AI 阅读闭环
   - 不失正见
6. 首页宽屏排版已收紧。
7. Hugo 构建通过，最近一次构建约 145 页，0 错误。

## 当前工作流

内库：Obsidian  
外站：Hugo  
版本：Git  
部署：hugo-site/public/ rsync 到仓库根目录  
线上：GitHub Pages

发布命令：

cd /Users/macos/angelife.github.com/hugo-site
hugo --minify

cd /Users/macos/angelife.github.com
rsync -av hugo-site/public/ ./

git status --short
git diff --stat

git add -A
git commit -m "..."
git push origin master

## 重要规则

不要修改：
- old-site/
- themes/
- public/，除非是最终部署步骤
- 已经整理好的文章，除非明确要求

谨慎修改：
- layouts/
- static/css/

优先修改：
- content/
- static/css/angelife-brand.css
- layouts/index.html，仅限首页模板确实需要调整时

## 写作规则

KISS：Keep It Simple and Straightforward。

文章要求：
- 短句
- 短段
- 清楚
- 稳重
- 少术语
- 少情绪
- 不写成聊天记录
- 不写成玄学
- 不写成控诉书

正文内部标题只用 ## 和 ###，不要用 #。

每篇文章必须有：
- title
- date
- draft: false
- summary
- tags
- series
- slug

## 检查命令

构建：

hugo --minify

残留检查：

rg -n "所有材料先进 Inbox|Git 备份护法|辨识信息与时代|公开界面|AI 布印|患者|教育转化|民智不开|文化程度.*低|女人为什么|邪教信徒|^# 结论|^# 背景|^# 核心判断" content layouts

旧文 HTML 残留检查：

rg -n "<li>|</ul>|</tr>|<tbody>" content/posts/2014-04-13-reference content/posts/2014-04-16-ref2

## 下一步建议任务

1. 检查首页为什么“最新文章”没有完整显示新增十篇文章。
2. 检查 Mermaid 图在 about 页面是否能正常渲染。
3. 检查新增十篇文章是否都在栏目页和站点地图中。
4. 如果 Mermaid 不渲染，可以增加 Hugo Mermaid 支持，或改成纯文本流程图。
5. 优化首页“最新文章”列表逻辑，让它显示最近 10–12 篇普通内容页。
6. 最后部署到线上，并确认 https://angelife.github.io/ 已更新。

## Codex 接手方式

进入项目目录后，先不要改文件。

第一步只读检查：
- pwd
- git status --short
- git log --oneline -5
- hugo --minify
- find content/series content/projects content/posts -maxdepth 3 -type f -name "*.md" | sort

然后给出计划，再等待确认。
