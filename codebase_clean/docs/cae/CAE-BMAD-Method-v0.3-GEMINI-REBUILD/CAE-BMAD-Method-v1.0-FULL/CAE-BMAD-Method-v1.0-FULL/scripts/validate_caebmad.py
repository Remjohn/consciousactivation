#!/usr/bin/env python3
from pathlib import Path
import re, sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
cae = root / ".caebmad"

required = [
    cae / "module/module.yaml",
    cae / "module/module-help.csv",
    cae / "method/CAE_BMAD_METHOD.md",
    cae / "method/CAE_BMAD_SOURCE_AUTHORITY.md",
    cae / "method/CAE_BMAD_ARTIFACT_GOVERNANCE.md",
    cae / "method/CAE_BMAD_UPSTREAM_POLICY.md",
    cae / "skills/caebmad-product-reconstruction/SKILL.md",
    cae / "skills/caebmad-product-brief/SKILL.md",
    cae / "skills/caebmad-prd/SKILL.md",
    cae / "skills/caebmad-architecture/SKILL.md",
    cae / "skills/caebmad-epics-stories/SKILL.md",
    cae / "skills/caebmad-ui/SKILL.md",
    cae / "skills/caebmad-brownfield/SKILL.md",
    cae / "skills/caebmad-handoff/SKILL.md",
    cae / "skills/caebmad-review/SKILL.md",
]
missing = [str(p) for p in required if not p.exists()]
if missing:
    print("FAIL: missing CAE-BMAD files")
    for m in missing:
        print("  ", m)
    sys.exit(1)

# Validate skill frontmatter and substantive file size.
skills = list((cae / "skills").glob("*/SKILL.md"))
for p in skills:
    txt = p.read_text(encoding="utf-8")
    if not txt.startswith("---\n"):
        raise SystemExit(f"FAIL: no frontmatter: {p}")
    if not re.search(r"^name:\s*\S+", txt, flags=re.M):
        raise SystemExit(f"FAIL: no name frontmatter: {p}")
    if not re.search(r"^description:\s*.+", txt, flags=re.M):
        raise SystemExit(f"FAIL: no description frontmatter: {p}")
    words = re.findall(r"\b[\w'-]+\b", txt)
    if len(words) < 300:
        raise SystemExit(f"FAIL: CAE skill too small to be a serious method file ({len(words)} words): {p}")

# Every major workflow must have step files.
major = ["caebmad-product-reconstruction","caebmad-prd","caebmad-architecture",
         "caebmad-epics-stories","caebmad-ui","caebmad-brownfield","caebmad-handoff","caebmad-review"]
for name in major:
    steps = list((cae / "skills" / name / "steps").glob("step-*.md"))
    if len(steps) < 4:
        raise SystemExit(f"FAIL: {name} needs substantive step architecture; found {len(steps)}")

print(f"PASS: {len(skills)} CAE skill entrypoints validated.")
