# changelog.yaml 写入规则速查

> 摘要自 v0.6.37 生成的 CHANGELOG_YAML_RULES.md。完整版见项目根目录。

## 核心原则

- NVIDIA 只生成 `changelog_yaml_block.yaml` 标准 YAML 块草案
- **NVIDIA 可以更新 changelog.yaml**（约束是「禁止盲目 cat append」，不是禁止修改）
- 更新时必须：① 用 Python `yaml.safe_load` 预验证格式 ② 按版本号顺序插入正确位置 ③ Hugo 验证通过后才能 release
- 本地 Mac 按模板插入 `hugo-site/data/changelog.yaml` 的 `releases` 数组（两者皆可更新，以协调为准）
- 插入后必须先运行：`hugo --gc --cleanDestinationDir --minify -s hugo-site`
- Hugo 通过后才能 release

## 标准 YAML 块格式

```yaml
- version: "0.0.00"
  date: "YYYY-MM-DD"
  title: "版本标题"
  commit: "提交后以 tag vX.Y.Z 指向的 release commit 为准"
  tag: "vX.Y.Z"
  summary:
    - "要点一"
    - "要点二"
  changed:
    - "/posts/slug/"
    - "/changelog/"
```

## 标准 YAML 块格式

```yaml
- version: "0.0.00"
  date: "YYYY-MM-DD"
  title: "版本标题"
  summary: |
    要点一
    要点二
  files_changed:
    - "文件路径1"
    - "文件路径2"
  control: "人类用户 + ChatGPT / 剑妈"
  execution: "NVIDIA"
  environment: "Docker Hermes / macOS"
  authorized: true/false
```

## 禁止事项

- ❌ `cat block.yaml >> changelog.yaml`（盲目追加，会破坏 YAML 结构）
- ❌ 未 Hugo 构建验证就 release
- ❌ 同一版本重复插入（会创建重复条目）
- ❌ 不预验证直接插入（YAML 格式错误会导致 Hugo 构建失败）

## YAML 报错处理

```bash
git restore --source=HEAD -- hugo-site/data/changelog.yaml
# 修正 YAML 块格式后重新插入
```

## authorized 字段

- `authorized: false` — 内容就绪，待发布授权
- `authorized: true` — 已发布

发布后由执行者将 false 改为 true，连同 commit 一起推送。