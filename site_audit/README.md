# site-audit

Hugo 静态站点排版体检系统。

双检测：Markdown 源码层 + 浏览器渲染层。输出结构化和可视化报告。

**Status: v1.0 RC** — 2026-07-11

- 160/160 pytest 测试通过（100%，1.67s，22 个测试文件）
- 全站审计评分 80/100，0 严重、0 主要问题
- 证据模型 v1.0 定型，50 个证据 JSON 文件（2,689 元素）

## 安装

```bash
cd site-audit/
pip install -r requirements.txt
playwright install chromium
```

## 用法

```bash
# 源码层审计
python -m site-audit.cli /path/to/project --skip-render

# 完整审计（Source + Render）
python -m site-audit.cli .

# 指定线上 URL
python -m site-audit.cli . --url https://example.com

# 限制扫描页数
python -m site-audit.cli . --max-pages 50
```

## 输出

- `site_audit_report.json` — 结构化数据
- `site_audit_report.html` — 可读 HTML 报告
- `evidence/` — 视觉问题截图

## 评分

| 严重度 | 扣分 | 规则 |
|--------|------|------|
| critical | -10 | 水平溢出、低对比度(<3:1) |
| major | -5 | 标题跳级、字体<12px、对比度不足 |
| minor | -1 | 中西文间距、空行缺失 |

满分 100，最低 0。

## 测试

```bash
cd site-audit/
python -m pytest tests/ -v
```

## 项目结构

```
site-audit/
├── cli.py                 # CLI 入口
├── scanner/               # 源码层（markdown-it-py）
│   ├── markdown.py        # 文件解析
│   ├── headings.py        # 标题层级/空行
│   ├── spacing.py         # 中西文间距
│   └── scanner.py         # 编排器
├── renderer/              # 渲染层（Playwright）
│   ├── server.py          # Hugo server 控制
│   ├── browser.py         # Chromium 控制
│   ├── contrast.py        # WCAG 对比度
│   └── overflow.py        # 移动端溢出/字号
├── scoring/score.py       # 评分
├── reporter/              # 报告（JSON + HTML）
├── models/issue.py        # 数据模型
└── tests/                 # 测试
```

## 限制

- 渲染层需要 `hugo-site/` 目录结构
- 对比度检查仅在渲染页面工作
- 最大 500 markdown 文件、100 页面

## 已知问题（v1.0 RC）

- **6,763 个次要问题** — 全部为格式偏好，不影响功能：
  - 5,522 个中西文间距（81.6%）— 中文与 ASCII 字符间缺空格，主要在旧博客迁移内容
  - 1,241 个标题空行（18.4%）— 标题前缺空行，系统性模式
- 0 严重问题、0 主要问题
- 建议：标题空行可批量自动修复；CJK 间距可一次性归一化处理
