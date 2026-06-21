# Angelife Skills 共享仓库

所有 Hermes 机器人共享的 skills，托管在 angelife.github.com 的 `skills` 分支。

## 仓库地址

```
git@github.com:angelife/angelife.github.com.git
分支: skills
```

## 初始化（每个机器人首次）

```bash
# 1. 克隆 skills 分支到本地
git clone --branch skills git@github.com:angelife/angelife.github.com.git /opt/data/skills-shared

# 2. 配置 git 身份
cd /opt/data/skills-shared
git config user.email "hermes-<角色>@angelife.io"
git config user.name "<角色>同学 (Hermes)"

# 3. 配置 Hermes 加载外部 skills
# 在 config.yaml 中:
# skills:
#   external_dirs:
#     - /opt/data/skills-shared
```

## 日常使用

```bash
# 拉取最新 skills（每次会话前）
scripts/sync-skills.sh pull

# 创建/修改 skill 后
scripts/sync-skills.sh push

# 查看本地改了啥
scripts/sync-skills.sh status
```

## 谁都可以贡献

- 木同学（本容器）：技术 / 工具类
- 土同学（Mac）：本地操作 / 发布类
- 金同学（Docker gold）：决策 / 质量类

创建一个新 skill 后，跑 `sync-skills.sh push`，其他人下次 `pull` 就能用到。

## 规则

- 不提交 secrets（API key、token、密码写在 config.yaml 或 .env）
- 每个 skill 一个目录，必须有 SKILL.md
- 修改别人的 skill 前先 pull 最新版
- push 冲突时优先 `git pull --rebase` 再推
