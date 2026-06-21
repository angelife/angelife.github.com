# NVIDIA API 控频 & curl 替代 requests

## 40 RPM 硬性上限（INC-20260530-001 血训）

NVIDIA Integrate API 免费 tier 硬限 **40 RPM**（每分钟40次）。超过后返回 HTTP 429，迭代第5轮起开始 hang 住几分钟。

### 规则：每调必等

**所有** LLM 调用（`vision_client.py`、`feedback_hindsight.py`、任何直接调 NVIDIA `/v1/chat/completions` 的脚本）完成后必须等 2 秒：

```python
import time
# ... API 调用 ...
time.sleep(2)  # 放在 return 前，拿到答案后等，等完再返回
```

### 已在用的文件（验证通过）

| 文件 | 行号 | 位置 |
|------|------|------|
| `/opt/data/vision_client.py` | 47, 50 | `return {"success": ...}` 前 |
| `/opt/data/storage/feedback_hindsight.py` | 73 | `return content` 前（RATE_SLEEP=2 常量）|

### 新写 LLM 客户端时

在所有 return 语句前加 `time.sleep(2)`。用 grep 确认：

```bash
grep -n "return" vision_client.py | grep -v "time.sleep"
```

如果有漏掉的 return，在该行前插入。

## Docker 环境不能用 requests

**症状**：`ModuleNotFoundError: No module named 'requests'`

**原因**：Docker 基础镜像未装 requests，且网络受限无法 `pip install`。

### 正确做法：subprocess + curl

```python
import subprocess, json

result = subprocess.run(
    ["curl", "-s", "--max-time", "15",
     "-H", f"Authorization: Bearer {os.environ['NVIDIA_API_KEY']}",
     "-H", "Content-Type: application/json",
     "-d", json.dumps({"model": "meta/llama-3.2-11b-vision-instruct",
                       "messages": [{"role": "user", "content": prompt}],
                       "max_tokens": 512}),
     "https://integrate.api.nvidia.com/v1/chat/completions"],
    capture_output=True, text=True
)
resp = json.loads(result.stdout)
```

**参数说明**：
- `--max-time 15`：硬超时15秒，替代 `requests` 的 `timeout=15`
- `capture_output=True`：等价于 `stdout=PIPE, stderr=PIPE`
- `text=True`：返回字符串而非字节，替代 `.json()`
- 无 `stream=True`：curl 默认非流式，兼容性好

### 不要用

- ❌ `requests.post(..., timeout=15)` — 缺 requests 模块
- ❌ `urllib.request` — Docker 可能也缺依赖
- ❌ 任何需要 `pip install` 的 HTTP 库