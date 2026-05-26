# 安知生 angelife

This repository publishes the site at https://angelife.github.io/.

The legacy static site is preserved at https://angelife.github.io/old-site/.

The new site is a Hugo-published knowledge system for `安知生 / angelife / 蝉识录`:

- AI 原生知识生产线
- Obsidian Markdown 主库
- Hugo 发布网站
- Git 版本护法

## Workflow

1. Collect raw material in `hugo-site/00_inbox`.
2. Refine material with AI into the Obsidian vault structure.
3. Move mature drafts to `hugo-site/60_网站发布稿` or `hugo-site/content/series`.
4. Preview locally with Hugo:

   ```sh
   /usr/local/bin/hugo server --source hugo-site --buildDrafts
   ```

5. Publish the site output to the repository root:

   ```sh
   ./publish.sh
   ```

6. Commit and push with Obsidian Git or normal Git.

The previous root-site snapshot is kept at the Git tag
`legacy-root-site-before-hugo-root-publish`.
