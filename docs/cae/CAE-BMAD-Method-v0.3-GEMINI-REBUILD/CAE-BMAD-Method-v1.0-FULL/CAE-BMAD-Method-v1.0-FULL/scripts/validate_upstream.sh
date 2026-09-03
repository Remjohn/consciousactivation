#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-.}"

required_dirs=(
  "src/core-skills"
  "src/bmm-skills"
  "src/scripts"
  "tools"
  "docs"
)

echo "Validating BMAD base: $TARGET"

for d in "${required_dirs[@]}"; do
  if [[ ! -d "$TARGET/$d" ]]; then
    echo "FAIL: missing mandatory original directory: $d" >&2
    exit 1
  fi
done

required_files=(
  "src/core-skills/bmad-help/SKILL.md"
  "src/core-skills/bmad-deep-recon/SKILL.md"
  "src/core-skills/bmad-advanced-elicitation/SKILL.md"
  "src/core-skills/bmad-review/SKILL.md"
  "src/core-skills/bmad-customize/SKILL.md"
  "src/core-skills/bmad-brainstorming/SKILL.md"
  "src/core-skills/bmad-forge-idea/SKILL.md"
  "src/core-skills/bmad-party-mode/SKILL.md"
)

for f in "${required_files[@]}"; do
  if [[ ! -f "$TARGET/$f" ]]; then
    echo "FAIL: missing mandatory original skill: $f" >&2
    exit 1
  fi
done

# BMM locations evolved between releases, so find equivalent capabilities.
check_any() {
  local label="$1"; shift
  for pattern in "$@"; do
    if find "$TARGET/src/bmm-skills" -path "*${pattern}*" -name SKILL.md -print -quit | grep -q .; then
      echo "OK: $label"
      return 0
    fi
  done
  echo "FAIL: missing BMM capability: $label" >&2
  return 1
}

check_any "Product Brief" "bmad-product-brief" "bmad-create-product-brief"
check_any "PRD" "bmad-prd"
check_any "UX" "bmad-ux" "bmad-create-ux-design"
check_any "Architecture" "bmad-architecture" "bmad-create-architecture"
check_any "Epics and Stories" "bmad-create-epics-and-stories"
check_any "Implementation Story" "bmad-create-story"
check_any "Development Story" "bmad-dev-story"
check_any "Code Review" "bmad-code-review"
check_any "Project Context" "bmad-project-context"

echo "PASS: mandatory BMAD upstream structure is present."
