# changelog.yaml 写入规则

> 本文档固化 `hugo-site/data/changelog.yaml` 的写入流程。
> 违反本规则导致构建失败，由操作者自负。

---

## 核心原则

**changelog.yaml 不能由 AI 自由追加。**

NVIDIA 只能生成标准 YAML 块草案。本地 Mac 按固定模板插入。
插入后必须 Hugo 构建验证。通过后才能 release。

---

## 写入流程

### NVIDIA 职责

1. 在交接报告中提供 `changelog_yaml_block.yaml` 文件
2. 该文件只含标准 YAML 块，不含文件拼接指令
3. 不在 NVIDIA 端直接 `cat >>` 任何文件

### 本地 Mac 职责

1. 将 `changelog_yaml_block.yaml` 内容插入 `hugo-site/data/changelog.yaml`
2. 插入位置：`releases` 数组的开头（最新版本在前）或末尾（按项目习惯）
3. **插入后必须先运行构建验证**：

```bash
cd /Users/macos/angelife.github.com
hugo --gc --cleanDestinationDir --minify -s hugo-site
```

4. Hugo 通过后才能执行 release

---

## 标准 YAML 块格式

```yaml
  - version: "0.0.00"
    date: "YYYY-MM-DD"
    title: "版本标题"
    summary: |
      要点一
      要点二
      要点三
    files_changed:
      - "文件路径1"
      - "文件路径2"
    control: "人类用户 + ChatGPT / 剑妈"
    execution: "NVIDIA"
    environment: "Docker Hermes / macOS"
    authorized: true/false
```

---

## YAML 报错处理

如果 Hugo 构建报错且确认是 changelog.yaml 格式问题：

1. **立即停止发布流程**
2. 先回滚到上一次正确的 changelog.yaml：

```bash
git restore --source=HEAD -- hugo-site/data/changelog.yaml
```

3. 重新检查 YAML 块格式（缩进、冒号、引号）
4. 修正后重新插入
5. 再次 Hugo 验证
6. 确认通过后再 release

---

## 禁止事项

- ❌ `cat changelog_yaml_block.yaml >> hugo-site/data/changelog.yaml`（盲目追加）
- ❌ 未构建就 release
- ❌ 同一版本多次插入（会导致重复条目）
- ❌ 手动修改已发布的 changelog.yaml 条目
- ❌ 让 AI 直接操作仓库中的 changelog.yaml

---

## 版本号与 authorized 字段

- `authorized: false` — 内容就绪，待发布授权
- `authorized: true` — 已获授权，已发布

发布后由执行者将 `false` 改为 `true`，同时 commit 一起推送。

---

## 责任链

- NVIDIA：生成标准 YAML 块草案，不操作仓库文件
- 本地 Mac：插入、构建验证、发布
- 谁构建，谁验证，谁负责