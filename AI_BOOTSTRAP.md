# angelife AI 接手启动说明

本文件是 angelife 项目的 AI 记忆恢复入口。任何 AI、机器人、执行代理、命令手臂，在接手本项目之前，必须先读本文件。

## 1. 项目基本信息

项目名称：angelife / 安知生

本地仓库：
/Users/macos/angelife.github.com

Hugo 源站：
/Users/macos/angelife.github.com/hugo-site

公开站点：
https://angelife.github.io/

当前部署方式：
本地 Hugo 构建 → 安全同步到 GitHub Pages master/root → 精确 git add → commit → tag → push。

不得擅自切换为 GitHub Actions 在线 Hugo 构建。

## 2. 当前核心分工

当前真实链路是：

剑妈定法，NVIDIA 干活，本地 Mac 补完。

### 剑妈

剑妈是设计师和总控。

负责：
- 方向
- 架构
- 规则
- 口径
- 任务拆解
- 验收标准
- 文章定稿方向
- 项目法度
- 纠偏

### NVIDIA

NVIDIA 是当前具体做事者。

定位：
Docker Hermes 独立实例，NVIDIA API / NIM + Minimax 免费模型，高 token / 免费 token 累活执行代理。

负责：
- 读包
- 检查包
- 内容生成
- 内容整理
- 规则一致性检查
- 日志草案
- Obsidian 记录内容
- Hugo 源文件内容准备
- 交接报告
- 环境障碍识别

NVIDIA 当前限制：
- 无 /Users/macos/angelife.github.com 访问权限
- 无 Hugo 命令
- 不直接 rsync
- 不 git add / commit / tag / push
- 不直接线上验证
- 不直接写入本地 Obsidian Vault

### 本地 Mac

本地 Mac 不是设计师，不是内容生产者，不重新决策。

本地 Mac 只负责完成 NVIDIA 因 Docker 限制做不了的本机动作：
- 访问本地仓库
- 复制已生成文件进仓库
- 把剑妈 / NVIDIA 生成好的 Obsidian 内容写入 Vault
- 运行 Hugo
- 安全 rsync / release
- 执行 git add / commit / tag / push
- curl 线上验证
- 检查本地保护文件

### Obsidian

Obsidian 是本地低成本工作台，不是内容生产者，不是 AI 执行代理。

Obsidian 用于：
- 查看
- 检查
- 轻修改
- 归档
- 上传
- 中转
- 自动归档

Obsidian 内容由剑妈 + NVIDIA 生成。  
本地 Mac 只负责写入，不生成内容。

### 后备工具

以下工具暂为后备，不默认启用：
- 蝉师傅 / 本机 Hermes
- 龙虾 / OpenClaw
- Reasonix
- Codex
- Claude Code

只有 NVIDIA 或本地 Mac 无法完成任务时，才考虑启用后备工具。

## 3. 署名追责规则

angelife 项目实行：

谁干活，谁署名。  
谁操作，谁负责。  
谁出问题，能回溯。

每轮必须记录：
- 总控 / 设计者
- 内容生成者
- 包检查者
- 文件落盘者
- Obsidian 内容生成者
- Obsidian 实际写入者
- Hugo 构建者
- rsync 执行者
- git add 执行者
- commit 执行者
- tag 执行者
- push 执行者
- 线上验证者
- 发布授权者
- 最终验收者
- 异常与风险

禁止写模糊表述：
- AI 已完成
- 系统自动完成
- 执行代理已处理
- 已发布

必须写具体责任者，例如：
- 内容生成：剑妈 + NVIDIA
- 包检查：NVIDIA
- 文件落盘：本地 Mac
- Hugo 构建：本地 Mac
- 发布授权：人类用户
- 最终验收：人类用户 + ChatGPT / 剑妈

## 4. 发布规则

固定发布流程：
本地 Hugo 构建 → 安全 rsync / release → 精确 git add → commit → tag → push → 线上验证。

优先使用：
./tools/angelife-release --yes <version> "<message>"

如果脚本不可用：
立即停下报告。不得裸 rsync。不得手写临时发布流程。

禁止：
- git add .
- 提交 _incoming/
- 提交 .reasonix/
- 裸 rsync --delete
- 删除 tools/
- 删除 publish.sh
- 删除 .gitignore
- 删除 .gitmodules
- 删除微信认证文件
- 恢复 GitHub Actions 在线 Hugo 构建
- 多个执行代理同时操作仓库
- 未授权发布
- 匿名施工

## 5. 必须保护的文件

微信认证文件：
- hugo-site/static/0847745cb78663855a3a1732c9c6a130.txt
- 0847745cb78663855a3a1732c9c6a130.txt

内容必须是：
01413348ab0d5b381a2e7099ba2600ed57ad50d3

线上必须可访问：
https://angelife.github.io/0847745cb78663855a3a1732c9c6a130.txt

必须保护：
- .git/
- .github/
- hugo-site/
- _incoming/
- .reasonix/
- docs/
- tools/
- .gitignore
- .gitmodules
- publish.sh
- README.md
- LICENSE
- AI_BOOTSTRAP.md
- PROJECT_STATUS.md
- BUILD_HANDOFF.md
- AI_WORK_RULES.md
- AI_EXECUTION_AGENTS.md
- HERMES_COST_RULES.md
- SITE_STYLE_GUIDE.md
- SITE_CHANGELOG.md
- DAILY_WORK_LOG.md

## 6. 内容工作流

内容流转规则：
- 碎片和半成品先进入本地整理层 / Obsidian
- 剑妈负责观点定稿和结构判断
- NVIDIA 负责生成、整理、分类、日志草案和交接
- Hugo 只接收定稿
- 网站只发布成品

不得把未成熟碎片直接发布到网站。

相似主题处理原则：
- 能合并就合并
- 有独立价值才新建文章
- 重复观点并入 canonical 文章
- 过时内容归档

## 7. 文章包规则

文章包必须写清：
- 推荐执行者
- 总控 / 验收者
- 是否需要用户授权
- 是否只能单代理操作
- cover_status
- Hugo 目标路径
- changelog 建议
- DAILY_WORK_LOG 建议
- 执行链 / 署名追责字段

封面规则：
- 有真实图片才能写 cover.image
- 没有真实图片必须写 cover_status: prompt_ready
- 不得伪造 cover.png
- 不得写不存在的图片路径

## 8. 当前版本状态

已发布：
- v0.6.33：更新 /site-workflow/，公开当前协作制度
- v0.6.34：热修流程图静态资源 404

本轮：
- v0.6.35：固化 AI 接手记忆与项目规则

后续任务：
- v0.7.0：旧 Blogger 内容回流工程
- 来源：https://angelifex.blogspot.com/

v0.7.0 原则：
- 剑妈制定迁移策略和分类框架
- NVIDIA 抓取、整理、分类、去重、再加工
- 本地 Mac 实际写入 Hugo、构建、发布、验证
- 不无脑搬运
- 能合并就合并
- 有独立价值才新建文章
- 谁干活谁署名
- 长期目标：人类参与降到最低，最终 0 参与自动化

## 9. AI 开工前检查清单

任何 AI 开工前必须确认：
- 已读 AI_BOOTSTRAP.md
- 已读 PROJECT_STATUS.md
- 已读 BUILD_HANDOFF.md
- 已读 AI_WORK_RULES.md
- 已读 AI_EXECUTION_AGENTS.md
- 已读 DAILY_WORK_LOG.md
- 已读 SITE_CHANGELOG.md
- 已确认当前 git status
- 已确认当前最新 tag
- 已确认本轮自己能做什么、不能做什么
- 已确认是否需要用户授权

最终口径：

剑妈定法。  
NVIDIA 干活。  
本地 Mac 补完。  
谁干活，谁署名。  
谁出问题，能回溯。
