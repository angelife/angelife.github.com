# 五行团队技能体系重构方案 v1

参考 claude-for-legal-ZH 的技能架构模式（垂直领域 + 共享工作流 + 冷启动面试 + 三级路由），重新设计五行团队各 bot 的技能体系。

---

## 一、现状问题

| 问题 | 表现 |
|------|------|
| 技能散落 | 各 bot 各自一堆 skill，缺少统一分类和路由 |
| 角色模糊 | SOUL.md 简单泛化，没做到角色专属深度 |
| 没有冷启动 | 新 bot 上线后要反复教，没有自动化的初始化流程 |
| 跨 bot 共享差 | 同样的工作流（如发报告、排障）每个 bot 各自实现一份 |

---

## 二、目标架构

```
五行技能体系
├── 共享基座 (Shared Layer)
│   ├── shared-workflows/     — 跨 bot 通用工作流
│   ├── shared-knowledge/     — 跨 bot 通用知识库
│   └── routing/              — 任务分发与路由规则
│
├── 垂直领域 (Vertical Skills)
│   ├── 土 · 中枢/
│   ├── 金 · 执行/
│   ├── 水 · 机动/
│   ├── 火 · 安全/
│   └── 木 · 待定/
│
├── 冷启动面试 (Cold-Start)
│   ├── bot-profile/          — 各 bot 的角色画像模板
│   └── user-preference/      — 用户偏好记录
│
└── 路由层 (Routing)
    ├── c1-direct/            — 常规任务直接匹配 bot
    ├── c2-deep-dispatch/     — 复杂任务跨 bot 协调
    └── c3-user-override/     — 用户明确指定
```

---

## 三、垂直领域设计

### 土同学 · 中枢（本机 Mac）

**定位**：综合判断、任务调度、信息整合、历史经验

| 技能 | 说明 |
|------|------|
| `command-center` | 任务接收 -> 分析 -> 分发 -> 追踪 -> 闭环 |
| `systems-thinking` | 系统分析框架（存量/流量/反馈回路） |
| `hindsight-ops` | 跨会话记忆管理、经验沉淀 |
| `skill-curator` | 技能库维护、版本管理、跨 bot 同步 |
| `infrastructure-audit` | 全局基础设施巡检与健康报告 |

### 火同学 · 安全（Mac 1.23）

**定位**：攻防专家、渗透测试、漏洞分析、OSINT

| 技能 | 说明 |
|------|------|
| `web-security` | OWASP Top 10、SSRF、SQLi、XSS、JWT |
| `network-pentest` | 扫描、协议攻击、C2 |
| `exploit-development` | PoC 开发、Fuzzing、Shellcode |
| `osint-recon` | 信息收集、资产测绘、社工 |
| `cloud-security` | AWS/GCP/K8s 安全审计 |
| `mobile-security` | Android/iOS 渗透、Frida、逆向 |
| `ai-security` | Prompt 注入、模型越狱、对抗样本 |

### 金同学 · 执行（Mi8）

**定位**：外部接口、自动化流水线、持续作业

| 技能 | 说明 |
|------|------|
| `api-gateway` | 外部 API 集成、Webhook、代理管理 |
| `cron-ops` | 定时任务编排、Watchdog 监控 |
| `gitops` | GitHub 自动化、CI/CD 集成 |
| `provider-failover` | Provider 容灾、fallback 链管理 |
| `deploy-pipeline` | Hugo 发布、远程部署 |

### 水同学 · 机动（Mi6）

**定位**：数据采集、灵活机动、轻量响应

| 技能 | 说明 |
|------|------|
| `data-collector` | 数据采集、爬虫、日志抓取 |
| `device-ops` | Android 设备管理、ADB 自动化 |
| `quick-response` | 即时应答、轻量查询、快捷操作 |
| `monitor-watchdog` | 资源监控、阈值告警 |

---

## 四、共享基座

### Shared Workflows

| 工作流 | 用途 | 使用的 bot |
|--------|------|-----------|
| `moa-sourcing` | MoA 信息检索与交叉验证 | 土、金 |
| `reporting-handoff` | 会话闭环与交接报告 | 全 bot |
| `hermes-troubleshooting` | Gateway / Provider / Telegram 排障 | 全 bot |
| `hugo-publish` | Hugo 站发布流程 | 土、金 |
| `bot-healthcheck` | 各 bot 健康检查报告 | 土（调度） |

### Routing Rules

| 任务类型 | 主 bot | 备 bot |
|---------|--------|--------|
| Web 安全分析 | 🔥 火 | 🪨 土 |
| 系统架构设计 | 🪨 土 | 🔥 火 |
| 定时任务/API 集成 | 🥇 金 | 🪨 土 |
| 数据采集/ADB | 💧 水 | 🥇 金 |
| 代码审查/发布 | 🥇 金 | 🪨 土 |
| 渗透测试 | 🔥 火 | — |
| 跨 bot 协调 | 🪨 土 | — |
| 应急响应 | 🔥 火（主攻）+ 🪨 土（协调）| |

---

## 五、冷启动面试

每个新 bot 上线时执行 `cold-start-intake`，产出 `~/.hermes/` 下的结构化画像：

```yaml
bot-profile.yaml
├── identity:          # 角色声明
│   ├── element:       金/水/火/土/木
│   ├── role:          中枢/执行/机动/安全
│   └── specialization: [领域列表]
├── preferences:       # 偏好
│   ├── temperature:   0.3/0.7/1.0
│   ├── response-style: terse/detailed
│   └── escalation:    { uncertainty: 0.7, conflict: 0.6 }
├── knowledge:         # 已装载的知识域
│   └── skills: [已安装的 skill 列表]
└── constraints:       # 边界
    ├── cannot-do: [技能边界外]
    └── must-confirm: [高风险操作]
```

---

## 六、实施步骤

### Phase 1 — 本机整理（当前网络）

1. ✅ 土同学现有技能按新目录结构重组（已装 graphify、hermes-troubleshooting）
2. 创建 `shared-workflows/` 目录，提取通用工作流
3. 创建冷启动画像模板

### Phase 2 — 到家后部署

4. 火同学：推送 SOUL.md + fire-security-expert 技能
5. 金同学：按执行角色补强技能
6. 水同学：按机动角色补强技能

### Phase 3 — 持续优化

7. 路由规则落地：土同学根据任务类型自动分配 bot
8. 冷启动面试流程落地
9. 定期技能审计与清理
