# Pollinations Prompt Archive

Tested prompts for angelife article covers. Each entry: topic → prompt → result.

---

## 1. 大衍神君的第一人（Xianxia × Cyberpunk 机械军团）

**Topic**: 孤身王者 + 万千机械傀儡，Xianxia 玄幻 × 赛博朋克融合
**Style keywords**: dark xianxia fantasy meets cyberpunk sci-fi, intricate bronze and gold mechanical ornaments, glowing orange core eyes, geometric formation, volumetric red fog, hyperdetailed, 8k, masterpiece

```
A lone master in flowing dark robes standing on a jade platform in an infinite dark void,
his face partially obscured by shadow, one hand raised commanding,
surrounded by thousands of glowing mechanical puppet figures arranged in perfect geometric formation like a vast army of soldiers,
each puppet has intricate bronze and gold mechanical ornaments with glowing orange core eyes,
dramatic low-angle cinematic shot,
dark xianxia fantasy meets cyberpunk sci-fi,
volumetric red fog, particles of gold light floating,
hyperdetailed, 8k, masterpiece
```
**Output**: 90KB PNG, 1024×1024. Success.

---

## 2. 震之随六五（惊雷裂空，中心不动）

**Topic**: 震卦意象——惊雷闪电中守住中心不动摇
**Style keywords**: ink-wash painting meets cinematic rendering, deep indigo sky, violet lightning, golden inner light, ancient Chinese cosmological atmosphere

```
A lone dark silhouette of a wise person standing calm and motionless at the center of a thundering storm,
dramatic purple lightning bolts splitting the dark sky in all directions,
the person radiates a soft golden inner light that remains perfectly still amid the chaos,
dark misty water below,
ancient Chinese cosmological atmosphere,
heavy storm clouds swirling at the edges but the center stays clear,
ink-wash painting meets cinematic rendering,
deep indigo and black sky,
brilliant white and violet lightning,
subtle gold light from the central figure,
hyperdetailed, 8k, masterpiece
```
**Output**: 68KB PNG, 1024×1024. Success.

---

## 3. NVIDIA 独立施工日志（赛博控制室）

**Topic**: AI 智能体在控制室指挥多机械臂——自动化施工的视觉隐喻
**Style keywords**: cyberpunk control room, multiple robotic arms, holographic screens, calm golden light

```
A lone AI agent standing at a central command console,
multiple robotic arms and glowing holographic screens arranged in a semicircle around it,
each screen displaying different tasks: writing, code, design, deployment,
the central agent radiates calm golden light while the robotic arms execute in perfect synchrony,
cyberpunk control room aesthetic,
dark blue and gold color palette,
hyperdetailed, 8k, masterpiece
```
**Output**: 117KB PNG, 1024×1024. Success.

---

## Prompt Engineering Patterns

### Proven style fusions
- `dark xianxia fantasy meets cyberpunk sci-fi` — reliable dramatic aesthetic
- `ink-wash painting meets cinematic rendering` — Chinese cosmological feel
- `Studio Ghibli meets dark noir` — when you want soft + moody

### Reliable quality boosters
- `, hyperdetailed, 8k, masterpiece` at end
- `dramatic low-angle cinematic shot` for impact
- `volumetric fog / particles of gold light floating` for depth
- `intricate [element] with [glowing feature]` for mechanical detail

### ComfyUI upgrade path
When GPU is available, reuse these prompts in Flux Dev with:
```
Negative prompt: blurry, low quality, deformed, extra fingers, bad anatomy
Steps: 30, CFG: 7, Sampler: DPM++ 2M Karras
```

---

## Current State (2026-06-01)

### Agnes AI key — INVALID
- Key `sk-sp1...` tested against `https://apihub.agnes-ai.com` → `"无效的令牌"`
- Base URL 确认为 `https://apihub.agnes-ai.com`（非 `api.agnes-ai.com`）
- Request ID: `20260601121819473299343F8sdJgmE`（向 Agnes 客服报 bug 时需要）
- **结论**: Pollinations 是当前唯一可用方案，无需任何 API key

### Pollinations — WORKING ✅
- 测试结果：200 OK，84KB PNG，1024×1024
- 无需注册、无需 key、完全免费
- ⚠️ 偶发性 522（origin unreachable）— 重试即可，通常 2-3 次内成功

### CRITICAL: JPEG Default + format=png Requirement
- Pollinations 默认返回 **JPEG**（magic bytes `FF D8 FF`），即使 URL 包含 `.png` 或文件名是 `.png`
- 2026-06-01 实测：83 篇封面全部 FAIL 判定为损坏，文件实际上是有效的 83KB JPEG
- **必须在 URL 中加 `format=png`**：`?format=png` 参数强制 PNG 输出
- 验证逻辑必须同时接受 PNG (`\x89PNG\r\n\x1a\n`) 和 JPEG (`\xff\xd8\xff`) 的 magic bytes

### Rate Limit Behavior (2026-06-01 实测)
- 免费账户限流触发后，`curl` 返回 200 但文件是错误页面（< 1KB）
- 重试机制有效：3 次尝试，指数退避 5s → 12.5s，第二次重试通常成功
- 无错误时建议间隔 2.5s；有错误时间隔 5s 起步，逐次加倍
- 85 篇预计耗时 25-30 分钟（考虑重试退避）

### pflex_ key 说明（历史记录，忽略）
- 用户曾提供 `pflex_...` 格式的 key
- `pflex_` 是 PicFlex 的 key 前缀，不是 Pollinations
- 两者是不同的服务：PicFlex = 付费的 ChatGPT-Image2；Pollinations = 免费
- 之前的 522 错误测试用的是错误的 API 端点，与 Pollinations 本身可用性无关

### Upgrade Path（待启用）
| 方案 | 质量 | 成本 | 状态 |
|------|------|------|------|
| Pollinations | 良好 | 免费 | ✅ 主力 |
| Replicate FLUX.1-schnell | 顶级 | ~$0.003/张 | ⚠️ 需注册 |
| PicFlex ChatGPT-Image2 | 顶级 | 12 credits/张 | ⚠️ 需 key |
| Agnes AI | 未知 | 未知 | ❌ key无效 |

---

*Archived by NVIDIA, 2026-05-29. All outputs tested on Pollinations AI v2.*
*Updated 2026-06-01: JPEG default, format=png, rate limit retry behavior.*