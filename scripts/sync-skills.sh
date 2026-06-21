#!/bin/bash
# Skills Sync Script
# Run on startup: pulls latest skills from shared repo
# Run after new skill: commits and pushes to shared repo
# Usage: sync-skills.sh pull|push|status
# Location: /opt/data/skills-shared/scripts/sync-skills.sh

SKILLS_DIR="$(dirname "$(dirname "$0")")"
cd "$SKILLS_DIR" || exit 1

case "$1" in
  pull)
    echo "[skills-sync] Pulling latest from origin/skills..."
    git pull origin skills 2>&1
    echo "[skills-sync] Done."
    ;;
  push)
    echo "[skills-sync] Committing and pushing changes..."
    if git diff --quiet && git diff --cached --quiet; then
        # Check for untracked files
        if [ -z "$(git ls-files --others --exclude-standard)" ]; then
            echo "[skills-sync] Nothing to commit."
            exit 0
        fi
    fi
    git add -A
    git commit -m "skills: auto-sync update - $(date '+%Y-%m-%d %H:%M')"
    git pull --rebase origin skills 2>&1
    git push origin skills 2>&1
    echo "[skills-sync] Sync complete."
    ;;
  status)
    git status --short
    ;;
  *)
    echo "Usage: $0 pull|push|status"
    exit 1
    ;;
esac
