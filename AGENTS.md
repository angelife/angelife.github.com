# AGENTS.md — 本项目唯一项目规则入口

> 本项目以 `AGENTS.md` 为唯一项目规则入口。
> `.hermes.md` / `CLAUDE.md` / `.cursorrules` 不存在或不承担规则职责。
> 如需更新规则，只改此文件，不要新增同级规则文件。

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).

## Project Rules

### Hugo 站点
- Hugo 站点在 `hugo-site/` 子目录下，不是根目录
- 所有 Hugo 命令（hugo server / hugo build）必须在 `hugo-site/` 下执行
- 文章在 `hugo-site/content/posts/<slug>/index.md`
- 封面图在 `hugo-site/static/images/posts/<slug>/cover.png`

### Browser Provider
- Browser Provider 代码在 `~/.hermes/skills/web-ai-cdp-bridge/provider/`
- OpenBridge 守护进程管理：`cd ~/.openbridge/repo && node packages/daemon/dist/cli/index.js status`
- OpenBridge API 端口：10088
- 旧 CDP bridge 在 `~/.hermes/skills/web-ai-cdp-bridge/scripts/ask.js`
- 新 OpenBridge 入口：`~/.hermes/skills/web-ai-cdp-bridge/scripts/ask-openbridge.js`

### Git
- 提交信息格式：`type: description`（feat/fix/chore/docs/refactor）
- 不要直接推送到 main 分支（除非明确要求）