# v0.6.XX 日志追加块标准格式

> 来源：v0.6.33–v0.6.39 持续使用验证。

## 标准追加块格式

每个版本需要在以下文件末尾追加内容（不是覆盖，是追加）：

### DAILY_WORK_LOG.md 追加块

```markdown
## YYYY-MM-DD — v0.6.XX 发布

**本轮目标**：...

**版本**：
- 当前：v0.6.XX-1（已发布）
- 目标：v0.6.XX

**三者分工**：
- 剑妈 = 设计师 + 总控：...
- NVIDIA = 具体做事者：...
- 本地 Mac = ...

**执行链**：
- 方向/架构/口径：人类用户 + ChatGPT / 剑妈
- 文件生成：NVIDIA（通过 /repo 直接写入 或 /opt/data/vXXXX-pickup/）
- Hugo 构建：待本地 Mac 执行
- release：待本地 Mac（待授权）
- git：待本地 Mac（待授权）

**发布授权**：❌ 未授权

**本轮不启用**：蝉师傅、龙虾、Reasonix、Codex、Claude Code

**后续任务**：...
```

### SITE_CHANGELOG.md 追加块

```markdown
## v0.6.XX — YYYY-MM-DD

**标题**：...

**摘要**：
- ...

**修改文件**：
- `xxx.md`（新增/追加）
- ...

**总控 / 设计**：人类用户 + ChatGPT / 剑妈
**具体做事**：NVIDIA
**执行环境**：Docker Hermes（NVIDIA）/ macOS（本地 Mac 补完）
```

### PROJECT_STATUS.md 追加块

```markdown
## v0.6.XX — YYYY-MM-DD

**状态**：✅ 内容就绪，待发布授权

**本轮完成**：
- ...

**待本地 Mac 执行**：
- 文件复制到仓库（若用 pickup 模式）
- Hugo 构建
- tools/angelife-release（待授权）
- git add / commit / tag / push（待授权）
- 线上验证

**发布授权**：❌ 未授权

**后续任务**：...
```

### BUILD_HANDOFF.md 追加块

```markdown
## v0.6.XX 构建交接 — YYYY-MM-DD

**版本**：v0.6.XX
**目标**：...

**上游交付物**：
- `xxx.md`（新增/追加）
- ...

**本地 Mac 接收检查清单**：
□ 确认文件已正确追加
□ Hugo 构建无报错
□ tools/angelife-release（待授权）
□ git add 精确指定文件（不用 git add .）
□ git commit -m 含版本号 v0.6.XX
□ git tag v0.6.XX
□ git push && git push --tags（待授权）
□ 线上验证

**发布前必须停下的条件**：
- Hugo 构建报错
- tools/angelife-release 不可用
- 微信认证文件缺失

**交接方**：NVIDIA
**接收方**：本地 Mac
**验收方**：人类用户 + ChatGPT / 剑妈
```

### changelog_yaml_block.yaml 标准块

```yaml
- version: "0.6.XX"
  date: "YYYY-MM-DD"
  title: "版本标题"
  summary: |
    要点一
    要点二
    要点三
  files_changed:
    - "xxx.md"
    - "yyy.md"
  control: "人类用户 + ChatGPT / 剑妈"
  execution: "NVIDIA"
  environment: "Docker Hermes（NVIDIA）/ macOS（本地 Mac 补完）"
  authorized: false
```

**注意**：此块不能 `cat >>` 直接追加到 changelog.yaml，必须由本地 Mac 按模板插入 releases 数组。

## 版本号规则

自 v0.6.0 起采用 SemVer：`vMAJOR.MINOR.PATCH`
- PATCH：样式、文案、标签、链接、图片、日志、流程等小范围优化与修复
- MINOR：新增重要栏目、功能或内容体系
- MAJOR：网站架构、主题、发布方式发生破坏性变化