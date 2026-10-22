#!/bin/sh
# Blocks commits that touch files listed in .protected unless a human ran scripts/sign-off-protected.sh.
protected=$(git diff --cached --name-only | git -c core.excludesFile=.protected check-ignore --no-index --stdin)
[ -z "$protected" ] && exit 0

token=$(git rev-parse --git-path protected-signoff)
if [ -f "$token" ] && [ "$(cat "$token")" = "$(git write-tree)" ]; then
  rm "$token"
  exit 0
fi

echo "These files are off limits to agents (see .protected):" >&2
echo "$protected" | sed 's/^/  /' >&2
echo "If you are an agent: do not edit these files. Undo your changes and stop." >&2
# Find the parent `git commit` so the retry can reuse its -m message.
pid=$PPID
for _ in 1 2 3 4 5 6; do
  args=$(ps -o command= -p "$pid")
  case "$args" in *" commit -m "*) message=${args#* commit -m }; break;; esac
  pid=$(ps -o ppid= -p "$pid" | tr -d ' ')
done
retry=scripts/sign-off-protected.sh
[ -n "$message" ] && retry="$retry && \\
git commit -m '$(printf %s "$message" | sed "s/'/'\\\\''/g")'"
echo "If you are a human, copy and run:" >&2
echo >&2
printf "%s\\n" "$retry" >&2
exit 1
