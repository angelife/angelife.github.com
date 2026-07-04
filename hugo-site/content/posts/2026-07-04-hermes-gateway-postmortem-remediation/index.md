---
title: "Hermes Gateway 二次崩溃排障复盘：不是“又崩了”，而是四层叠加故障"
date: 2026-07-04
draft: false
categories: ["土·正见"]
tags: ["排障", "Hermes", "Gateway", "Telegram", "可观测性", "配置漂移"]
---

## 这件事为什么值得单独写一期

6 月底至今，Hermes Gateway 出现了两次级联故障：第一次是 Telegram 超时/403/polling conflict，紧接着是二次崩溃把 gateway 进程本身也退出了。很多人的处理方式是“重启、祈祷、别再触发”，然后写一句“环境抖动”。这次我们没有接受这个结论。

这篇文章只记录两件事：**根因是什么**，以及 **修复过程中哪些结论是已验证的，哪些只是代码级完成但尚未被真实流量碰过**。

什么值得吹、什么硬证据支持、什么其实还没验证，全部分开列。这是这次最重要的方法论：证据纪律比重启次数更重要。

---

## 2. 连续 crash 时间线

### 2.1 trigger 1：首次故障（gateway 还活着）

- `gateway.error.log` 中记录到 Telegram 侧 `Timed out`
- 波特消息发送退化为“只回不发送”，此时 gateway 进程仍存活
- 同时 `errors.log` 中出现 `Pool timeout` / `403 Authorization failed`

### 2.2 trigger 2：二次崩溃（gateway 进程直接退出）

- 在首次故障未恢复时，`gateway setup` 和 `gateway stop` 操作在极短时间窗口内并行触发
- 多个 gateway 实例同时启停，导致 Telegram 单 bot 多实例 polling conflict
- TUI 侧伴随 `write EIO` 错误及 `SIGHUP/SIGTERM` 信号
- gateway 自行退出

**根因分层：** “第一次崩溃”不是 gateway 退出，“第二次退出”才是；而第二步不是独立故障，是“第一次故障还没完全处理时，又叠加了一个并行启停动作”。

---

## 3. 四类叠加根因

这四件事不是互相替代，而是同时成立：

## 3.1 多实例并发启停触发 Telegram polling 互踢

- 关键证据：gateway.error.log 中存在多组 `hermes-gateway_0`、`hermes-gateway_1` 同时出现
- Telegram 单 bot 被多个实例同时轮询，触发 `403 Authorization failed` / `Polling heartbeat probe failed` / `Pool timeout`

## 3.2 fallback provider freellmapi 链路不可用

- `freellmapi-freellmapi-1` docker 容器存活，服务健康
- 但本地测试返回 `Invalid API key`，当前配置的 key 已失效
- fallback 命中后会返回 `NO_REPLY` 拉长响应超时，但不产生真实回复

## 3.3 config.yaml fallback_providers YAML 拼接残留

- 存在一条错误拼接：
```yaml
- nvidia/deepseek-ai/deepseek-v4-flash- nvidia/z-ai/glm-5.1
```
- 这不是有意的第三个 provider，而是两条 provider 被错误拼贴成一行
- 修改后 `fallback_providers` 长度为 3，YAML 语法校验通过

## 3.4 Cloudflare qwen3-30b max_tokens 超限

- 报错原始信息：
```text
max_tokens=65536 cannot be greater than max_model_len=max_total_tokens=32768
```
- 同时伴随：
```text
RuntimeError: Context length exceeded (320 tokens). Cannot compress further.
```
- 根因：`qwen-oauth`/`custom` 插件的 `default_max_tokens=65536` 在无用户配置时生效，超出 Cloudflare Workers 模型上限

---

## 4. 修复与验证状态

### 4.1 ✅ STEP 1：fallback_providers 拼接清理

- **操作：** 删除错误拼接条目，保留三条独立 provider 定义
- **验证：** `yaml.safe_load` 通过；`fallback_providers` 长度=3 ✅
- **状态：** 已验证完成

### 4.2 ⚠️ STEP 2：freellmapi fallback 可用性——不可验证

这个状态不是“失败”，而是**可观测性不足**。

- `gateway.error.log` 中有 provider/base_url/model 的请求级证据，但**这些日志行本身没有行首时间戳**
- `freellmapi` 无公开 `/metrics` 访问日志，服务侧计数无法作为证据
- 因此无法做“主 provider 改坏 → 触发 fallback → 服务侧计数 +1 → 时间窗口对齐”的双侧闭环验证

**结论：** 服务本身可用，但当前两边都缺时间戳，无法验证 fallback 路径是否被真实命中过。记为**证据缺口**，不标记为已验证。

**额外发现：** Hermes 日志系统缺行首时间戳，这个问题比 STEP 2 本身更基础，会持续拖累未来的所有排障。

### 4.3 🔧 STEP 3：max_tokens 65,536 → 28,000

**代码级修复已完成**，但存在新的判定问题：

- 修改内容：`/Users/macos/.hermes/hermes-agent/plugins/model-providers/qwen-oauth/__init__.py:79` + `/Users/macos/.hermes/hermes-agent/plugins/model-providers/custom/__init__.py:71`
- 将 `default_max_tokens` 从 65,536 改为 28,000

**但这里的验证前提发生了变化：**

- 我们确认 `@cf/qwen/qwen3-30b-a3b-fp8` 在近期日志中**只有 watchdog 一个调用方**
- STEP 3.5 已经把这个唯一调用方改成了 no_agent 脚本，不再走 LLM 调用链
- 因此这个 provider 当前**没有真实流量**可以验证 28,000 是否生效

**状态：** 代码级修复完成，**运行时刻验证缺流量**。这不是“修复无效”，而是“配置正确但从未被真实流量触碰”。这和 STEP 2 的可观测性缺口是同一类问题。

**补一句配置漂移风险：** qwen3-30b 目前唯一调用方已经被移除，28000 这个值可能永远不会被验证。无人使用的 provider 配置在后续改动中容易被忽略或写错。

### 4.4 ✅ STEP 3.5：watchdog 去 agent 化改造

这是优先级最高的一次改动，直接切断了“watchdog 走 LLM → 触发 context length exceeded → cron 失败”的链路。

**改动：**

- cron job `da2b5692cb9b` 已设置为 `no_agent=true`
- 指向 `/Users/macos/.hermes/scripts/watchdog_no_agent.sh`
- 脚本只做三件事：
  1. 读 `gateway.pid` 判断进程是否存活
  2. 读 `gateway.error.log` 最近 10 分钟内容
  3. 统计 `Pool timeout` / `403` / `polling conflict` 关键词数量并决策

**证据链闭环：**

| 验证点 | 证据 |
|---|---|
| 脚本不是空壳 | 正常执行 `recent_errors=0`，注入已知错误后变为 `recent_errors=1` |
| 执行期间无 LLM 调用 | 手动测试窗口内 `provider=` 路由日志为 0 条 |
| cron 入口无并行风险 | `cronjob list` 确认仅 `da2b5692cb9b` 指向该脚本 |

**状态：** 已验证完成

### 4.5 ✅ STEP 4：重复启停保护——已有实现更优

原计划要求“加 PID 文件锁”，实际核查后发现 Hermes 已有更完善的保护机制：

**现有实现：**

- `/Users/macos/.hermes/hermes-agent/gateway/run.py:19383` 的 `start_gateway` 入口一开始就做了 duplicate-instance guard
- 使用 `fcntl.flock(..., LOCK_EX | LOCK_NB)` 做跨进程互斥
- 配合 `gateway.pid` 里的 `pid + start_time` 做 PID reuse 防护

**真实并发测试结果（无 `--replace` 场景）：**

```text
第二次无 --replace 启动被拒绝：
❌ Gateway already running (PID 499).
```

- 退出码 1
- 原 PID 499 未变
- 新进程未产生

**生产 restart 路径补充测试：**

实际执行 `hermes gateway restart` 一次，exit 0，新 PID 8355 接管成功。但窗口内捕获到 Telegram 侧记录：
`This Updater is already running!`

这说明 restart 过程中存在短暂双实例在线窗口，不是理想中的“旧实例完全退出 → 新实例上线”。这是已知残余风险，需单独评估，不归入当前排障范围。

**结论：不加重复实现，当前已有可工作的 duplicate-start prevention；生产 restart 路径存在短暂 overlap，暂不标记为“已验证根治”。**

---

## 5. 一项未解的遗留问题

在 HERMES 系统中，以下两类问题仍未进入已验证状态：

- **STEP 2：日志无行首时间戳** → 任何 fallback/路由类故障都卡在“两边对不上时间”
- **STEP 3：qwen3-30b = 零调用** → 28000 这个修复处于“配置正确但从未被真实流量碰过”的状态

这两类问题的共同特征：**代码级修复 ≠ 已验证修复，中间差一次真实流量命中**。

如果以后再次出现同类故障，会是“老修复本来就没生效过”还是“新 bug”，这个区分很重要。建议尽快评估最小修复面：

> 只给 `conversation_loop` 的请求级日志加 monotonic timestamp + request_id，不改路由逻辑，不需要上 Prometheus/ELK。

---

## 6. 这是一篇方法论文章

总结这篇复盘真正想强调的三件事：

1. **双层时间戳缺失是最隐蔽的障碍**——不是今天这个排查不会卡住，是未来任何类似排障都会继续卡
2. **“代码已改”和“已被真实流量验证”是两种状态，必须分开记录**——混淆这两者会导致日后误判
3. **不要为了完成 STEP 的字面任务，在已工作的东西上叠加同名机制**——`flock + PID reuse` 已经比裸 PID 文件更强，此时正确动作是“记录已有实现”，不是“再造轮子”
