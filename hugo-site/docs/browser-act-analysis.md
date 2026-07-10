# BrowserAct 评估与 Hermes Browser Provider 架构设计

> 用途：给代码审查型 AI 阅读，评估 BrowserAct 是否适合集成到 Hermes，以及需要什么适配层。
> 生成日期：2026-07-10
> 来源：土同学（Hermes Agent on Mac）

---

## 1. 现状：Hermes 的浏览器依赖

### 1.1 当前实现

Hermes 在 Mac 上跑了一个 Chrome CDP 实例（端口 9222），通过 Playwright `connectOverCDP()` 控制。用途：

- **Gemini Web 桥接**（`hermes-gemini-web` skill）：向 gemini.google.com 发送 prompt，让 Gemini 用免费 Imagen 生成 Hugo 文章封面图
- 潜在的 Web AI 外援通道（ChatGPT/Claude/Perplexity Web 版）

### 1.2 痛点

Google 反自动化检测频繁触发（reCAPTCHA / Sorry Page），根因：

1. **裸 CDP 暴露自动化特征** — `navigator.webdriver` 等 fingerprint 点未隐藏
2. **代理出口 IP 信誉低** — 数据中心 IP，Google 信任分不足
3. **无自动验证码解决** — 触发后只能人工手动过，阻断自动化流程

### 1.3 尝试方案

`web-ai-cdp-bridge` skill 封装了通用 CDP 桥接架构（core/composer/reader + adapters），但在"过验证"这一层是空的——captcha 解决依赖人工。

---

## 2. BrowserAct 是什么

### 2.1 基础信息

- GitHub: `browser-act/skills` — **4.3k stars**, 201 forks, 359 commits
- 公司名也叫 BrowserAct，定位 "Browser automation CLI built for AI agents"
- 开源了两个核心 skill: `browser-act` + `browser-act-skill-forge`
- 商业模式：**免费增值**（stealth ≤5 个免费，managed proxy/高级功能付费）

### 2.2 三层反封锁架构

| 层级 | CDP bridge（当前） | BrowserAct |
|------|-------------------|------------|
| 环境层（指纹伪装） | ❌ 裸 CDP | ✅ Stealth 指纹 + TLS 轮换 + 代理切换 |
| 执行层（验证码） | ❌ 人工 | ✅ `solve-captcha` 支持多家厂商 |
| 人工层（兜底） | ✅ 人工 | ✅ `remote-assist` 跨平台远程接力 |

### 2.3 三种浏览器模式

| 模式 | 场景 | key trait |
|------|------|-----------|
| `chrome` | 复用本地 Chrome 登录态 | Profile import 或 CDP attach |
| `stealth` privacy | 无痕批量采集 | 每次新指纹 + 新代理，零残留 |
| `stealth` fixed | 登录态账号操作 | 稳定指纹 + 稳定 IP |

### 2.4 对比：为什么不是竞品

| 工具 | 定位 | 与 BrowserAct 差异 |
|------|------|-------------------|
| Playwright | 通用浏览器自动化框架 | 无反检测、无验证码解决、无人工接力 |
| Browserbase | 云端浏览器基础设施 | 商业产品，非 CLI-first，不能本地跑 |
| Skyvern | No-code 自动化 | 不是为 Agent CLI 设计的 |
| Bright Data Agent Browser | 企业级代理+浏览器 | 付费，不能本地部署 |

---

## 3. 关键假设验证

### ⚠️ 以下结论需要进一步验证，当前证据不足：

**假设 A：BrowserAct 能解决 Gemini CAPTCHA**

当前证据：仅公众号文章提到 "reCAPTCHA v3 0.9 分" 和 "stealth 指纹伪装通过检测"。
但 **Google Gemini 的风控不是单一指纹检测**，它综合：
- IP reputation（数据中心 IP 仍是低分）
- 账号历史与行为模式
- Cookie 完整性
- 地理一致性
- TLS/网络特征

**Stealth 浏览器可以降低触发频率，但不能保证 CAPTCHA 消失。**

**假设 B：BrowserAct 可以在 Intel Mac 上安装**

当前不成立。PyPI 上 `browser-act-cli` v1.0.5 提供的 wheel 平台：
- ✅ `macosx_11_0_arm64`（Apple Silicon）
- ✅ `manylinux_2_17_x86_64`（Linux）
- ✅ `win_amd64`（Windows）
- ❌ `macosx_xx_x_x86_64`（Intel Mac 缺失）
- ❌ sdist（没有源码包）

Intel Mac 目前无法通过 `uv tool install` 或 `pip install` 安装。

---

## 4. Hermes Browser Provider 抽象层设计（已实现）

### 4.1 三层架构

```python
BrowserProvider      — navigate / click / input / screenshot / find_images
ChallengeHandler     — detect / solve / escalate (captcha, login)
HumanAssist          — request / wait / resume (manual override)
```

文件: `~/.hermes/skills/web-ai-cdp-bridge/provider/`

### 4.2 CAPTCHA 状态机

```
DETECTED → AUTO_SOLVING → [ok → RESOLVED]
                          ↘ [fail → HUMAN_REQUESTED → HUMAN_WAITING → RESOLVED]
                                                                      ↘ TIMEOUT
```

### 4.3 验证结果

✅ Phase 1 已完成: BrowserProvider + ChallengeStateMachine + ConsoleHumanAssist
✅ 所有接口通过 Python 验证测试
✅ CDPProvider 封装现有 Node.js 脚本，零破坏性改动

### 4.2 文件结构

```
hermes/
  providers/
    browser/
      __init__.py
      interface.py          # BrowserProvider ABC
      cdp_provider.py       # 现有 CDP 实现（保持兼容）
      browseract_provider.py  # BrowserAct 封装
      manual_provider.py    # 纯人工接管（debug/fallback）
      registry.py           # 注册表 + 自动选择逻辑
  skills/
    gemini-web/
      image_generator.py    # 只用 Provider，不直接调 CDP
```

### 4.3 迁移路径

| 阶段 | 内容 | 影响 |
|------|------|------|
| Phase 1 | 提取 `interface.py`，`cdp_provider.py` 封装现有逻辑 | 零改动，纯重构 |
| Phase 2 | `gemini-web` skill 切换到 Provider 接口 | 功能不变，解耦 |
| Phase 3 | `browseract_provider.py`（等 x86_64 wheel 或换 arm） | 新后端，不影响 CDP |
| Phase 4 | `manual_provider.py` | 人工兜底标准化 |
| Phase 5 | Provider 自动选择（CDP → BrowserAct → Manual fallback） | 全自动后续 |

---

## 5. 问题总结（供外部 AI 诊断）

### 核心问题

| # | 问题 | 严重程度 | 优先级 |
|---|------|---------|--------|
| 1 | Hermes 缺少浏览器后端的抽象层，当前 CDP 桥接与 Gemini skill 耦合 | 架构债 | P1 |
| 2 | Intel Mac 无法装 BrowserAct（无 x86_64 wheel） | 阻塞 | P2 |
| 3 | Gemini Web 的 CAPTCHA 不能靠单一 stealth 解决，需要完整策略 | 不确定性 | P1 |
| 4 | 现有 CDP bridge 无自动 fingerprint 伪装 | 功能缺失 | P2 |
| 5 | 现有 CDP bridge 无 CAPTCHA 自动解决能力 | 功能缺失 | P1 |

### 需要外部 AI 判断的关键问题

1. **BrowserAct 是否值得集成？** 还是应该直接补 CDP bridge 的 stealth/captcha 层？
2. **Intel Mac 不支持 BrowserAct 的情况下**，是否有等价替代方案（undetected-chromedriver、selenium-stealth 等）？
3. **Hermes 是否需要一个 Browser Provider 抽象层？** 还是继续保持当前的直接 CDP 调用？
4. **Gemini Web 的免费额度** vs Gemini API 付费，哪种长期更划算？
5. **当前 CDP bridge 的最佳修复路径**：
   - 路径 A：补 stealth 指纹伪装（fast, partial fix）
   - 路径 B：集成 BrowserAct（需要 x86_64 支持或换设备）
   - 路径 C：放弃 Web 版，全走 API（可靠但花钱）
   - 路径 D：混合 — API 做主要推理，Web 做画图等 API 不支持的功能
