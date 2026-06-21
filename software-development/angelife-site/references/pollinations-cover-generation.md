# Pollinations 批量配图避坑指南（v0.7.18 实测）

## ⚠️ 关键修复（v0.7.18）

Pollinations **默认返回 JPEG**（header `FF D8 FF`），不是 PNG（`89 50 4E 47`）。脚本如果只检查 PNG header，会把大量有效图片误判为 FAIL 并删除。

### 正确配置

**1. URL 必须加 `format=png`**：
```
https://image.pollinations.ai/prompt/<URL 编码后的描述>?width=800&height=600&seed=<唯一值>&format=png&nologo=true
```

**2. Header 校验必须兼容 JPEG + PNG**：
```python
# PNG 检查
if data[:8] == b'\x89PNG\r\n\x1a\n':
    return 'png'
# JPEG 检查
if data[:3] == b'\xff\xd8\xff':
    return 'jpeg'
```

**3. 指数退避重试**（Pollinations 免费账户限流）：
```python
delay = 5.0 * pow(2.5, attempt - 1)  # [5s, 12.5s, 31.25s]
time.sleep(delay)
```
最多 3 次重试，单次请求失败不跳过，必须重试到底。

## 核心问题

批量生成封面图时，多个帖子会得到**完全相同的图**（md5sum 一致）。v0.7.16 验证结果：93 个封面文件，只有 20 个不同的 md5。

## 根因

Pollinations 的 URL 随机性依赖客户端参数或时间戳。如果 prompt 变化不够大、或随机种子相同，多个帖子会拿到同一张图。

## 验证命令

```bash
find /workspace/angelife.github.com/images/posts -name "cover.png" | xargs md5sum | awk '{print $1}' | sort | uniq -c | sort -rn
# 理想：每个 md5 出现 1 次
```

## seed 唯一化

每个 URL 用标题 md5 hash 作为 seed：
```python
import hashlib
seed = int(hashlib.md5(slug_dir.encode()).hexdigest()[:8], 16) % 1000000
```

## 脚本路径

`/opt/data/regen_covers.py` — 批量封面生成脚本（已修复 v0.7.18）

## 完整 Git 工作流

封面生成完成后，完整发布流程：
```bash
cd /workspace/angelife.github.com
git add -A images/
git status  # 确认 staged 文件
git commit -m "v0.7.X: 描述"
git tag v0.7.X
git push origin master && git push origin v0.7.X
```