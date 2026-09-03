#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-}"
if [[ -z "$TARGET" ]]; then
  TARGET="$(pwd)"
fi

BUNDLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ ! -d "$TARGET/.git" ]]; then
  echo "Target is not a git repository: $TARGET" >&2
  exit 1
fi

echo "Checking original BMAD tree..."
"$BUNDLE_DIR/scripts/validate_upstream.sh" "$TARGET"

echo "Installing CAE-BMAD overlay..."

mkdir -p "$TARGET/.caebmad"
rm -rf "$TARGET/.caebmad/module" "$TARGET/.caebmad/method" "$TARGET/.caebmad/skills" "$TARGET/.caebmad/templates" "$TARGET/.caebmad/research" "$TARGET/.caebmad/_config"

cp -R "$BUNDLE_DIR/module" "$TARGET/.caebmad/module"
cp -R "$BUNDLE_DIR/docs" "$TARGET/.caebmad/method"
cp -R "$BUNDLE_DIR/skills" "$TARGET/.caebmad/skills"
cp -R "$BUNDLE_DIR/templates" "$TARGET/.caebmad/templates"
cp -R "$BUNDLE_DIR/research" "$TARGET/.caebmad/research"
mkdir -p "$TARGET/.caebmad/_config"

# Preserve a reproducibility record.
commit="$(git -C "$TARGET" rev-parse HEAD)"
remote="$(git -C "$TARGET" remote get-url origin 2>/dev/null || true)"
cat > "$TARGET/.caebmad/_config/upstream-manifest.yaml" <<EOF
source_url: "$remote"
source_commit: "$commit"
caebmad_version: "1.0.0"
original_bmad_preserved: true
EOF

echo "Validating installed overlay..."
if [[ -f "$TARGET/scripts/validate_caebmad.py" ]]; then
  :
fi

echo
echo "CAE-BMAD installed."
echo "Original BMAD files were preserved."
echo "Next: caebmad-product-reconstruction"
