#!/usr/bin/env bash
# Commit and push whatever the run produced. Retries on a racing push, since the
# job pushes more than once and main can move underneath it.
set -euo pipefail
MSG="${1:-ojv-linkedin run}"
git config user.name "ojv-linkedin bot"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
git add -A
if git diff --cached --quiet; then
  echo "Nothing to commit."
  exit 0
fi
git commit -q -m "$MSG"
for attempt in 1 2 3 4 5; do
  if git push -q 2>/dev/null; then
    echo "Pushed on attempt $attempt."
    exit 0
  fi
  echo "Push rejected, rebasing and retrying (attempt $attempt)."
  git pull --rebase --autostash -q origin "$(git rev-parse --abbrev-ref HEAD)" || true
  sleep $((attempt * 3))
done
echo "::warning::Could not push after 5 attempts. The result is in the job workspace only."
exit 0
