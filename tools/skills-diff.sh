#!/usr/bin/env bash
# Compare the skills pinned in this repo (.claude/skills/) against the user-level copies in
# $CLAUDE_CONFIG_DIR/skills. Nothing syncs automatically — see docs/SKILLS-PINNED.md.
#
#   tools/skills-diff.sh                 report drift for every pinned skill
#   tools/skills-diff.sh <skill>         show the full diff for one skill
#   tools/skills-diff.sh --pull <skill>  adopt the user-level version into the repo
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PINNED="$ROOT/.claude/skills"
USER_SKILLS="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills"

# PixelStrata skills are pinned by its git tag, not against a user-level copy.
VENDORED="pixelstrata pixelorama godot-mcp"
is_vendored() { case " $VENDORED " in *" $1 "*) return 0 ;; *) return 1 ;; esac; }

if [ "${1:-}" = "--pull" ]; then
  s="${2:-}"
  [ -n "$s" ] || { echo "usage: $0 --pull <skill>" >&2; exit 2; }
  is_vendored "$s" && { echo "'$s' is vendored from PixelStrata — update it per docs/STACK.md §4" >&2; exit 1; }
  [ -d "$USER_SKILLS/$s" ] || { echo "no user-level skill '$s' in $USER_SKILLS" >&2; exit 1; }
  rm -rf "$PINNED/$s"
  cp -R "$USER_SKILLS/$s" "$PINNED/$s"
  echo "pulled $s -> .claude/skills/$s  (review with 'git diff', then commit)"
  exit 0
fi

if [ -n "${1:-}" ]; then
  s="$1"
  [ -d "$PINNED/$s" ] || { echo "'$s' is not pinned in this repo" >&2; exit 1; }
  [ -d "$USER_SKILLS/$s" ] || { echo "'$s' has no user-level copy to compare against" >&2; exit 1; }
  diff -ru "$PINNED/$s" "$USER_SKILLS/$s"
  exit $?
fi

drift=0
for d in "$PINNED"/*; do
  [ -d "$d" ] || continue
  s="$(basename "$d")"
  if is_vendored "$s"; then
    printf '[--] %-24s vendored (PixelStrata v0.3.0)\n' "$s"
  elif [ ! -d "$USER_SKILLS/$s" ]; then
    printf '[--] %-24s no user-level copy (repo copy is the only one)\n' "$s"
  elif diff -rq "$d" "$USER_SKILLS/$s" >/dev/null 2>&1; then
    printf '[ok] %-24s identical to user-level\n' "$s"
  else
    n="$(diff -rq "$d" "$USER_SKILLS/$s" 2>/dev/null | wc -l | tr -d ' ')"
    printf '[!!] %-24s DRIFTED (%s files differ) — %s %s\n' "$s" "$n" "$(basename "$0")" "$s"
    drift=1
  fi
done

echo
if [ "$drift" -eq 0 ]; then
  echo "no drift"
else
  echo "drift found. Review with '$(basename "$0") <skill>', adopt with '--pull <skill>'."
fi
exit 0
