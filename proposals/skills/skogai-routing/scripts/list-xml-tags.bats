#!/usr/bin/env bats
# Regression tests for list-xml-tags.sh. Run with:
#   bats list-xml-tags.bats
# (or `mise exec bats -- bats list-xml-tags.bats` if bats isn't on PATH.)

setup() {
  SUT="$BATS_TEST_DIRNAME/list-xml-tags.sh"
}

# Builds a fake skill root under bats' per-test tmp dir: ROOT/scripts/list-xml-tags.sh
# (a copy of the real script under test) plus whatever the caller adds under ROOT.
# This exercises the real BASH_SOURCE-relative logic without depending on this
# repo's actual on-disk layout.
make_skill_root() {
  local root
  root="$(mktemp -d -p "$BATS_TEST_TMPDIR")"
  mkdir -p "$root/scripts"
  cp "$SUT" "$root/scripts/list-xml-tags.sh"
  chmod +x "$root/scripts/list-xml-tags.sh"
  echo "$root"
}

# --- Regression 1: default paths resolve relative to the skill's own root, ---
# --- not the caller's cwd.                                                 ---
@test "regression 1: default paths resolve relative to skill root, not caller cwd" {
  root="$(make_skill_root)"
  printf '<foo>bar</foo>\n' >"$root/SKILL.md"
  unrelated_cwd="$(mktemp -d -p "$BATS_TEST_TMPDIR")"

  run bash -c "cd '$unrelated_cwd' && '$root/scripts/list-xml-tags.sh'"

  [ "$status" -eq 0 ]
  [[ "$output" == *"SKILL.md: foo"* ]]
}

# --- Regression 2: missing workflows/references/templates must not kill ---
# --- the script under set -euo pipefail.                                ---
@test "regression 2: survives missing workflows/references/templates dirs" {
  root="$(make_skill_root)"
  printf '<foo>bar</foo>\n' >"$root/SKILL.md"
  # Deliberately do NOT create workflows/, references/, templates/.

  run "$root/scripts/list-xml-tags.sh"

  [ "$status" -eq 0 ]
  [[ "$output" == *"SKILL.md: foo"* ]]
}

@test "symlink indirection mirrors .claude/skills -> proposals/skills" {
  real_root="$(make_skill_root)"
  printf '<foo>bar</foo>\n' >"$real_root/SKILL.md"

  link_parent="$(mktemp -d -p "$BATS_TEST_TMPDIR")"
  ln -s "$real_root" "$link_parent/skogai-routing"
  unrelated_cwd="$(mktemp -d -p "$BATS_TEST_TMPDIR")"

  run bash -c "cd '$unrelated_cwd' && '$link_parent/skogai-routing/scripts/list-xml-tags.sh'"

  [ "$status" -eq 0 ]
  [[ "$output" == *"SKILL.md: foo"* ]]
}

@test "explicit args override defaults entirely" {
  root="$(make_skill_root)"
  printf '<foo>bar</foo>\n' >"$root/SKILL.md"
  mkdir -p "$root/extra"
  printf '<baz>qux</baz>\n' >"$root/extra/note.md"

  run "$root/scripts/list-xml-tags.sh" "$root/extra"

  [ "$status" -eq 0 ]
  [[ "$output" == *"note.md: baz"* ]]
  [[ "$output" != *"SKILL.md"* ]]
}

@test "tag extraction dedups repeated tags and strips attributes" {
  root="$(make_skill_root)"
  cat >"$root/SKILL.md" <<'EOF'
<alpha>
  <beta class="x" id='y'>hello</beta>
</alpha>
<alpha>second</alpha>
EOF

  run "$root/scripts/list-xml-tags.sh"

  [ "$status" -eq 0 ]
  # alpha appears 3x (open, close, open) and beta 2x (open w/ attrs, close);
  # each name must be reported exactly once, first-seen order, attrs stripped.
  [[ "$output" == *"SKILL.md: alpha beta"* ]]
}

@test "file with no xml content reports placeholder" {
  root="$(make_skill_root)"
  printf 'just plain text, no tags here\n' >"$root/SKILL.md"

  run "$root/scripts/list-xml-tags.sh"

  [ "$status" -eq 0 ]
  [[ "$output" == *"SKILL.md: (no xml tags)"* ]]
}

@test "multiple matching files are reported in sorted order" {
  root="$(make_skill_root)"
  mkdir -p "$root/references"
  printf '<x/>\n' >"$root/references/zzz.md"
  printf '<x/>\n' >"$root/references/aaa.md"
  printf '<x/>\n' >"$root/references/mmm.md"

  run "$root/scripts/list-xml-tags.sh" "$root/references"

  [ "$status" -eq 0 ]
  order="$(printf '%s\n' "$output" | grep -o '[a-z]*\.md')"
  expected=$'aaa.md\nmmm.md\nzzz.md'
  [ "$order" = "$expected" ]
}

@test "no matching paths (defaults) exits 0 with empty output" {
  root="$(make_skill_root)"
  # No SKILL.md, no workflows/references/templates: nothing exists at all.

  run "$root/scripts/list-xml-tags.sh"

  [ "$status" -eq 0 ]
  [ -z "$output" ]
}

@test "no matching paths (explicit nonexistent arg) exits 0 with empty output" {
  root="$(make_skill_root)"

  run "$root/scripts/list-xml-tags.sh" "$root/does-not-exist"

  [ "$status" -eq 0 ]
  [ -z "$output" ]
}

@test "shellcheck runs clean against list-xml-tags.sh" {
  if ! command -v shellcheck >/dev/null 2>&1; then
    skip "shellcheck not on PATH"
  fi
  run shellcheck "$SUT"
  [ "$status" -eq 0 ]
}
