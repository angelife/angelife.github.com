# 未 commit 改动审计要点

## 2026-06-12 实战案例：剑妈 naosense 风格化改造

### 背景
ChatGPT/剑妈在 Mac 上修改了本地仓库，但未 commit/push。改动目标："向 naosense 风格靠拢"。

### 审计步骤复现

1. `git status` → 发现 5 个 modified + 5 个 untracked
2. `git diff --stat` → CSS -869/+367 行，模板全部重写
3. 逐文件审查：
   - **hugo.toml**: 菜单从 10 项减到 7 项，删除了所有五行独立导航
   - **list.html**: 删掉 Paginator、火·AI交叉查询、home filtering
   - **single.html**: 删掉 breadcrumbs、draft 标记、post_meta 模板
   - **index.html**: 从"精于心简于形"改为文章列表（hugo.toml 无 homeInfoParams）
   - **CSS**: 从 904 行精简到 304 行，五行变量全部删除
4. `hugo --gc --minify` → ✅ 384 pages, 0 errors

### 发现的关键问题
- 改造计划 `.hermes/REFACTOR_PLAN.md` 声称"保留五行栏目"，但实际导航菜单删除了所有五行入口
- `baseof.html` 未被修改（可能漏了）
- 自定义模板覆盖了 PaperMod 默认行为（footer.html, header.html）
- 备份文件 `css/angelife-brand.css.bak` 存在，可恢复

### 总结格式（以后参考）
🔴 导航五行入口删除 | 🟡 list.html 无分页 | 🟢 CSS 风格变更