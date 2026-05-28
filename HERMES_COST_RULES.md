# Hermes 省 Token 执行规则

本规则适用于 angelife Hugo 网站项目中所有 Hermes / Hermers 执行任务。

核心原则：

> ChatGPT / 剑妈负责思考、写作、策略、文章定稿和任务拆解。
> Hermes 只负责本地文件操作、Hugo 构建、rsync、精确 git add、commit、tag、push。
> Hermes 是执行代理，不是写作代理，不是策略代理，不是排障研究员。

---

## 1. 默认省 Token 模式

Hermes 每次任务默认进入省 Token 模式。

必须遵守：

- 不重写文章；
- 不改写正文；
- 不总结观点；
- 不输出长篇解释；
- 不全文 cat 长文件；
- 不扫描无关目录；
- 不自行扩展任务；
- 不主动研究项目历史；
- 不输出大段命令日志；
- 不把正常过程写成分析报告。

每一步只返回最短状态，例如：

```text
✅ 检查完成
✅ Hugo 构建通过
✅ rsync 已同步
✅ commit/tag 已完成
✅ push 完成
```

---

## 2. 固定执行顺序

```text
1. pwd + git status -sb → 确认仓库状态
2. Hugo 构建
3. rsync 到仓库根
4. 更新日志文件（如果需要）
5. 精确 git add
6. git commit
7. git tag（版本号顺延）
8. git push origin master && git push origin <tag>
```

每个步骤成功后，输出一行状态。

---

## 3. 省 Token 检查

- 检查任何文件时，只用 `test -f` 或 `ls -lh`（一行）；
- 读取文件只用 `head -5` 或 `grep -c`；
- 不全文 cat，除非该文件 < 500 字节且必需；
- 不 grep 全仓库；
- 不看 themes/ 内部；
- 不看 node_modules/；
- 不看 .git/objects/。

---

## 4. 版本号顺延规则

- 每次发布新版本号从当前 `vMAJOR.MINOR.PATCH` 的 `PATCH+1` 开始；
- 例如：v0.6.26 → 下一版本 v0.6.27；
- 不跳号，不改 MAJOR/MINOR，除非用户明确要求。

---

## 5. 禁止操作

- 禁止 `git add .`
- 禁止 `git init`
- 禁止 `git pull`
- 禁止 `git merge`
- 禁止 `git rebase`
- 禁止 `git reset --hard`
- 禁止 `rm -rf`
- 禁止提交 `_incoming/`
- 禁止启用 GitHub Actions 在线 Hugo 构建
- 禁止新增 `.github/workflows/` 文件

---

## 6. 遇到异常时

- 立刻停止；
- 不自行修复；
- 报告原因和最后一步状态；
- 等待用户指令。

---

## 7. 日志更新要求

- 更新 `DAILY_WORK_LOG.md`：每天最新一次日志之前插入新条目；
- 更新 `SITE_CHANGELOG.md`：最新版本之前插入；
- 更新 `PROJECT_STATUS.md`：仅更新当前版本号和 tag 行；
- 更新 `BUILD_HANDOFF.md`：仅更新当前版本号行；
- 更新 `hugo-site/data/changelog.yaml`：文件顶部插入新条目。
