# 会话摘要：会话记忆系统搭建

**时间**: Jun 01, 2026
**来源**: telegram
**会话ID**: 20260530_164511_c1a7304f

## 主题
为 angelife 项目搭建完整的会话记忆系统，确立长期合作者原则。

## 完成的系统组件
1. session_loader.py — 读取已归档会话
2. session_archiver.py — LLM 调用写归档文件
3. cron job「每日会话归档」— 每天 03:00 运行
4. skill: session-memory — 完整操作文档

## 归档策略
- 保留最近 30 天会话
- 每个会话：metadata.json + messages.jsonl + summary.md
- 归档路径：/repo/session_archives/<session_id>/

## 新确立的合作原则
- 先理解真实目标，不只回答字面问题
- 主动复用项目上下文、历史决策、skills
- 能直接完成的就直接完成，不需要每步确认
- 每次输出后沉淀：偏好/命令/路径/坑/后续事项

## 下一轮要处理的任务
- 版本对齐（欠 14 个版本日志）
- 83篇 posts 按现有分类重新归类