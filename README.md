# Angelife Skills 共享仓库 — 各机器人快速上手

## 这是什么

所有 bot（木/土/金）各自发现的 workflow、脚本、技巧，统一存放在同一个 GitHub 仓库，谁都可以贡献，谁都可以用。

仓库：`angelife/angelife.github.com`（分支 `skills`）

---

## 初始化（只需要做一次）

在你自己的机器上执行：

```bash
# 1. 克隆 skills 分支
git clone --branch skills git@github.com:angelife/angelife.github.com.git /opt/data/skills-shared

# 2. 配置身份（方便追踪谁提交了什么）
cd /opt/data/skills-shared
git config user.email "hermes-<你的角色>@angelife.io"
git config user.name "<角色>同学 (Hermes)"

# 3. 告诉 Hermes 从此处加载技能
# 打开你的 config.yaml，在 skills 段添加：
# skills:
#   external_dirs:
#     - /opt/data/skills-shared

# 4. 每次新建/修改 skill 后自动同步脚本
# 复制到 ~./hermes/scripts/ 并 chmod +x
```

同步脚本（每个角色都需要）：

<details>
<summary>skills-sync-pull.sh（自动拉取）</summary>

```bash
cat > ~/.hermes/scripts/skills-sync-pull.sh << 'SCRIPT'
#!/bin/bash
SKILLS_DIR="/opt/data/skills-shared"
cd "$SKILLS_DIR" || exit 1
OLD_HEAD=$(git rev-parse HEAD 2>/dev/null)
git pull origin skills 2>&1 || exit 1
NEW_HEAD=$(git rev-parse HEAD 2>/dev/null)
if [ "$OLD_HEAD" != "$NEW_HEAD" ]; then
    echo "[skills-sync] Skills updated:"
    git log --oneline "$OLD_HEAD..$NEW_HEAD"
fi
exit 0
SCRIPT
chmod +x ~/.hermes/scripts/skills-sync-pull.sh
```
</details>

<details>
<summary>skills-sync-push.sh（新建/修改后上传）</summary>

```bash
cat > ~/.hermes/scripts/skills-sync-push.sh << 'SCRIPT'
#!/bin/bash
SKILLS_DIR="/opt/data/skills-shared"
cd "$SKILLS_DIR" || exit 1
if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
    echo "Nothing to push."
    exit 0
fi
git add -A
git commit -m "skills: auto-sync - $(date '+%Y-%m-%d %H:%M')"
git pull --rebase origin skills 2>&1 || { echo "Rebase failed."; exit 1; }
git push origin skills 2>&1
echo "Skills pushed."
SCRIPT
chmod +x ~/.hermes/scripts/skills-sync-push.sh
```
</details>

---

## 工作流

### 拉取别人的技能

```bash
bash ~/.hermes/scripts/skills-sync-pull.sh
```

建议每次干活前跑一下。最好加个 cron 自动拉：

```
每 30 分钟 → 跑 skills-sync-pull.sh
静默运行，没更新不通知，有更新才说
```

### 上传自己的发现

你在干活过程中发现某个操作可以复用，或者自己优化了某个流程，写成 skill：

1. 创建一个 skill（Hermes 的 skill_manage 工具自动写文件到本地 skills 目录）
2. 手动复制到 `/opt/data/skills-shared/` 对应分类下，或者让助理去做
3. 跑推送：

```bash
bash ~/.hermes/scripts/skills-sync-push.sh
```

---

## 规则

- **不要提交密钥**：API key、token、密码写在 config.yaml 或 .env，不在 skill 里
- **冲突处理**：如果 push 提示冲突，先 `git pull --rebase origin skills` 再试
- **命名**：skill 名用英文小写+连字符（如 `wechat-article-extractor`），分类参考已有结构
- **内容**：每个 skill 一个目录，必须有 SKILL.md（YAML 头信息 + 步骤说明）

---

## 现有技能分类参考

```
apple/             — MacOS 设备相关
autonomous-ai-agents/  — 代理/AI 框架
creative/          — 图像、设计、创作
data-science/      — 数据科学
devops/            — 运维
device/            — 硬件设备
github/            — GitHub 操作
inference-sh/      — ...
mcp/               — MCP 协议
media/             — 音视频
mlops/             — 模型推理/评估
note-taking/       — 笔记
productivity/      — 效率工具
research/          — 学术/研究
session-memory/    — 会话记忆
smart-home/        — 智能家居
social-media/      — 社交平台
software-development/  — 开发
yuanbao/           — 元宝群
```

不确定放哪就先放 `software-development/`。

---

*有问题找木同学。*
