# Angelife Notes

This repository publishes the site at https://angelife.github.io/.

The legacy static site is preserved at https://angelife.github.io/old-site/.

## Workflow

1. Write in Obsidian using the vault at `hugo-site`.
2. Preview locally with Hugo:

   ```sh
   /usr/local/bin/hugo server --source hugo-site --buildDrafts
   ```

3. Publish the site output to the repository root:

   ```sh
   ./publish.sh
   ```

4. Commit and push with Obsidian Git or normal Git.

The previous root-site snapshot is kept at the Git tag
`legacy-root-site-before-hugo-root-publish`.
