# Angelife Notes

This folder is the Obsidian vault and Hugo source for the site.

## Workflow

1. Open this folder in Obsidian: `hugo-site`.
2. Write posts in `content/posts`.
3. Use `templates/post.md` for new articles.
4. Keep drafts as `draft = true`.
5. When ready, set `draft = false`.
6. Use Obsidian Git to commit and sync.

## Local Preview

```sh
hugo server --source hugo-site --buildDrafts
```

## KISS Rules

- One writing place: `content/posts`.
- One publishing path: GitHub Pages.
- One community plugin: Obsidian Git.
- Use Markdown files as the source of truth.
