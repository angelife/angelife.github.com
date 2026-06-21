# 事故归档速查

> v0.6.41-hotfix 建立。对应完整版：`/repo/_private/INCIDENT_REPORTS/README.md`

## 目录结构

```
_private/INCIDENT_REPORTS/          ← 必须入 .gitignore
├── README.md                        制度说明
├── INDEX.md                         事故索引（编号/日期/等级/关键词/状态/报告路径）
├── TEMPLATE.md                      报告模板（18个字段）
└── INC-YYYYMMDD-NNN-title.md       完整内部报告（不对外公开）

INCIDENT_REPORTS_PUBLIC/             ← 可跟踪，不入 .gitignore
└── INC-YYYYMMDD-NNN-title.public.md 脱敏摘要（仅发原则，不发路径/命令/token）
```

## 事故等级

| 等级 | 说明 |
|------|------|
| P0 | 仓库数据丢失、发布系统清洗、严重安全事件 |
| P1 | 重要功能失效、流程受阻、需人工干预 |
| P2 | 次要问题、不影响主线、可后续修复 |

## 归档要求

1. 每次 P0/P1 事故必须编号归档
2. 事故不入 INDEX，不算归档完成
3. 归档必须包含：完整复盘 + 新增规则 + 后续任务

## INC-20260529-001：release 脚本自发布导致仓库清洗（P0）

**一句话教训**：修 release 脚本的版本，禁止用 release 脚本自发布。

**五条新规则**：
1. 发布工具永远不能自发布
2. 事故后必须先查状态，不得重跑长流程
3. 重大事故必须编号归档
4. rsync --delete 必须有明确目标目录，禁止在仓库根目录直接执行覆盖自身
5. Docker bind mount 危险操作必须先确认路径

**脱敏摘要**：`/repo/INCIDENT_REPORTS_PUBLIC/INC-20260529-001-release-script-wiped-repo.public.md`

## 关键词索引（方便快速定位）

| 关键词 | 相关事故 |
|--------|---------|
| release | INC-20260529-001 |
| rsync | INC-20260529-001 |
| Docker | INC-20260529-001 |
| git add | INC-20260529-001 |
| 中文路径 | INC-20260529-001 |