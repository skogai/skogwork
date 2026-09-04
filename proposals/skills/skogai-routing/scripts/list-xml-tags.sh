#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -eq 0 ]; then
  SKILL_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
  set -- "$SKILL_ROOT/SKILL.md" "$SKILL_ROOT/workflows" "$SKILL_ROOT/references" "$SKILL_ROOT/templates"
fi

existing=()
for path in "$@"; do
  [ -e "$path" ] && existing+=("$path")
done
if [ "${#existing[@]}" -eq 0 ]; then
  exit 0
fi

find "${existing[@]}" -type f \( -name '*.md' -o -name 'SKILL.md' \) -print 2>/dev/null |
  sort |
  while IFS= read -r file; do
    tags=$({ grep -Eoh '</?[A-Za-z][A-Za-z0-9_-]*[^>]*>' "$file" 2>/dev/null || true; } |
      sed -E 's/^<\///; s/^<//; s/[ >].*$//' |
      awk '!seen[$0]++' |
      paste -sd ' ' -)

    if [ -n "$tags" ]; then
      printf '%s: %s\n' "$file" "$tags"
    else
      printf '%s: %s\n' "$file" "(no xml tags)"
    fi
  done
