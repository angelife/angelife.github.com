# changelog.yaml 写入速查

## 文件结构

- 顺序：**最新版本在前**（newest-first），不是 appended
- 第一个 entry 从第 1 行开始（`- version: "v0.6.42"`），每个 entry 包含完整字段
- entry 之间以**空行**分隔
- **插入位置**：在第一个 entry 结束后、第二个 entry 开始前插入新版本

## 正确插入位置

```yaml
# Line 0  : - version: "v0.6.42"
# Lines 1-21 : first entry content (date, title, commit, tag, summary[], changed[])
# Line 22   : (blank line)
# Line 23   : - version: "v0.6.40"  ← 新条目插这里之前
```

即：找到第一个完整 entry 结束后的空行，在空行**之后**插入新 entries。

## 错误做法

❌ 在文件顶部（第 0 行之前）插入 —— 会把第一条记录截断，只剩 `- version:` 行
❌ 用 `cat >>` 盲目追加到文件末尾 —— changelog 是 newest-first，不是 append
❌ 在文件中间任意位置插入 —— 会打乱现有顺序

## Python 插入脚本

```python
new_entries = [...]  # list of dicts, each with version/date/tag/title/summary/changed

def format_yaml_entry(entry):
    lines = []
    lines.append(f'- version: "{entry["version"]}"')
    lines.append(f'  date: "{entry["date"]}"')
    lines.append(f'  title: "{entry["title"]}"')
    lines.append(f'  commit: "以 tag {entry["tag"]} 指向的 release commit 为准"')
    lines.append(f'  tag: "{entry["tag"]}"')
    lines.append('  summary:')
    for s in entry['summary']:
        lines.append(f'    - "{s}"')
    lines.append('  changed:')
    for c in entry['changed']:
        lines.append(f'    - "{c}"')
    return '\n'.join(lines)

entries_text = '\n\n'.join(format_yaml_entry(e) for e in new_entries)

with open('/repo/hugo-site/data/changelog.yaml') as f:
    lines = f.read().split('\n')

# Find the blank line after the first entry (line 22 in the known layout)
# Safer: find first blank line that's followed by "- version:"
blank_idx = None
for i, line in enumerate(lines):
    if line.strip() == '' and i + 1 < len(lines) and lines[i+1].startswith('- version:'):
        blank_idx = i
        break

insert_idx = blank_idx  # insert after this blank line
new_lines = lines[:insert_idx] + [entries_text] + lines[insert_idx:]

with open('/repo/hugo-site/data/changelog.yaml', 'w') as f:
    f.write('\n'.join(new_lines))
```

## 验证步骤

1. `head -30 /repo/hugo-site/data/changelog.yaml` — 确认第一个 entry 完整（version + date + title + commit + tag + summary + changed 都在）
2. `grep -n "^- version:" /repo/hugo-site/data/changelog.yaml | head -5` — 确认新 entry 在正确位置
3. `python3 -c "import yaml; yaml.safe_load(open('/repo/hugo-site/data/changelog.yaml'))"` — YAML 格式验证

## 回退

若插入后 YAML 损坏：
```bash
cd /repo && git restore --source=HEAD -- hugo-site/data/changelog.yaml
```
然后重新插入（修复 Python 脚本后）。

## 场景：本轮 v0.7.13 补全

- 需补：v0.7.0, v0.7.1, v0.7.2, v0.7.3, v0.7.4, v0.7.5, v0.7.6, v0.7.7, v0.7.8, v0.7.9, v0.7.10, v0.7.11, v0.7.12, v0.7.13
- 插入位置：v0.6.42 entry 结束后（line 22 blank 行之后）
- 原始文件 625 行 → 插入后 798 行
- 补完后 commit message：`git commit -m "v0.7.13: changelog.yaml 补全 v0.7.0-v0.7.13 版本日志"`