#!/bin/sh
# Human sign-off for the staged changes; check-protected.sh accepts it once.
git diff --cached --name-only | git -c core.excludesFile=.protected check-ignore --no-index --stdin | sed 's/^/  /'
printf "Did you make these changes yourself? [y/N] "
read -r answer
[ "$answer" = "y" ] || exit 1
git write-tree > "$(git rev-parse --git-path protected-signoff)"
echo "Signed off. Commit again."
