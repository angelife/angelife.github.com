# angelife / 安知生

> 让不同 AI 都能接手、又不至于失控的共同工地规则。

## 这是什么项目

angelife（安知生）是一个公开知识网站，托管于 GitHub Pages。
当前版本 **v0.7.14**。

本项目不是谁的独门工作流，而是一套让不同 AI 都能接手的协作制度。
所有规则都写在文档里，不在任何人脑子里。

---

## AI 接手第一步

**必须先读 README.md，然后按顺序读以下文件。**

不读这些文件，不算正式接手。

### 必读清单

1. `README.md`（本文件）← 你在这里
2. `AI_BOOTSTRAP.md` — 完整项目记忆恢复入口
3. `PROJECT_STATUS.md` — 当前版本、发布状态、项目阶段
4. `AI_WORK_RULES.md` — AI 施工规则与安全红线
5. `AI_EXECUTION_AGENTS.md` — 执行代理分工
6. `DAILY_WORK_LOG.md` — 日常执行日志
7. `SITE_CHANGELOG.md` — 版本变更记录
8. `hugo-site/data/changelog.yaml` — 结构化 changelog

按顺序读。读完全部，再动手。

---

## AI_BOOTSTRAP.md 是完整记忆恢复入口

`AI_BOOTSTRAP.md` 包含：项目定位、核心协作原则、版本演进脉络、当前施工阶段、关键配置文件位置、发布链路说明。

它是新 AI 入场的起点文档。读完它之后，再去读上面必读清单里的其他文件。

---

## 当前真实分工

### 总控层

| 角色 | 职责 |
|------|------|
| **用户** | 最终验收：所有 push 必须经用户确认后执行，拥有方向否决权 |
| **NVIDIA（Docker Hermes）** | 总控：方向决策、内容管理、规则维护、全流程执行 |

### 执行模型

| 模型 | 定位 |
|------|------|
| **MiniMax M2.7**（NVIDIA NIM） | NVIDIA 容器的执行模型，承担持续施工 |

**同级协作原则**：所有 AI 执行代理（NVIDIA/龙虾/Claude Code 等）为同级合作者，无阶级差异，按需分工。

---

## 发布方式

```
NVIDIA 容器内：Hugo 构建 → cp -a public/. /repo/ → git add（精确）→ commit → tag
用户确认后：git push origin master && git push origin vX.Y.Z
线上验证：curl https://angelife.github.io/
```

- Hugo 源站：`hugo-site/`
- Hugo 二进制：`/opt/data/hugo`（v0.162.1）
- 静态产物同步到仓库根目录（`cp -a public/. /repo/`），不是 rsync
- **禁止裸 rsync**（容器无 rsync 二进制）
- **禁止 `git add .`**（必须精确指定文件）

---

## SSH Key 配置（容器内 push 必需）

容器启动后，如需 git push，先加载 SSH key：

```bash
eval $(ssh-agent) && ssh-add ~/.ssh/id_ed25519
```

公钥已注册在 GitHub（`hermes-docker-nvidia`）。

---

## 安全红线（禁止事项）

以下行为无论谁授权，一律禁止：

- ❌ `git add .`（必须精确指定文件）
- ❌ 提交 `_incoming/`、`.reasonix/`、`.vault/` 目录
- ❌ 裸 `rsync --delete`
- ❌ 删除 `tools/` 或 `publish.sh`
- ❌ 删除 `.gitignore`
- ❌ 删除微信认证文件（`0847745cb78663855a3a1732c9c6a130.txt`）
- ❌ 未授权发布
- ❌ 匿名施工（不署名）

**谁干活，谁署名。谁操作，谁负责。谁出问题，能回溯。**

---

## 版本演进

| 版本 | 内容 |
|------|------|
| v0.6.33 | 公开 /site-workflow/ 协作制度 |
| v0.6.34 | 热修流程图静态资源 |
| v0.6.35 | 新增 AI_BOOTSTRAP.md，固化 AI 接手记忆 |
| **v0.6.42** | **NVIDIA 升任总控，独立维护网站；剑妈时代结束** |
| v0.7.0–v0.7.12 | 五行分类体系建立，全站文章归类完成 |
| **v0.7.13** | **changelog.yaml 日志补全（v0.7.0–v0.7.13 +173行）、posts 清理** |
| **v0.7.14** | **about 页面更新（MiniMax M2.7）、治理文档版本同步、五行体系完成** |

---

## 后续任务

- 评论系统（giscus）启用——等待 GitHub Discussions 配置
- 配图方案升级：Pollinations（免费，当前主力）→ PicFlex/Replicate FLUX（高质量待启用）
- 图片生成流程：生成后必须通过 `python3 /opt/data/vision_client.py <path> "描述内容"` 验证再落盘

---

## 链接

- 公开站点：https://angelife.github.io/
- 项目 GitHub：https://github.com/angelife/angelife.github.com

---

## changelog.yaml 写入规则

changelog.yaml 修改遵守 `CHANGELOG_YAML_RULES.md`。
NVIDIA 生成 YAML 草案，本地 Mac 构建验证通过后才能 release。