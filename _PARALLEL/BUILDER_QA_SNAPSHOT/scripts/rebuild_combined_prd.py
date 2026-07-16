from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECTION_ORDER = ['prd/00-document-purpose.md', 'prd/01-vision-product-promise.md', 'prd/02-users-jobs-journeys.md', 'prd/03-glossary.md', 'prd/04-doctrine-product-principles.md', 'prd/05-features/index.md', 'prd/05-features/F01-governed-product-lifecycle.md', 'prd/05-features/F02-configured-evidence-workspace.md', 'prd/05-features/F03-visual-syntax-first.md', 'prd/05-features/F04-atomicity-draft-harness-model.md', 'prd/05-features/F05-dependency-driven-genesis.md', 'prd/05-features/F06-canonical-harness-ir.md', 'prd/05-features/F07-capability-module-phase-contract.md', 'prd/05-features/F08-reference-spr-context.md', 'prd/05-features/F09-canonical-skill-ecology.md', 'prd/05-features/F10-skill-composition-jit-capsules.md', 'prd/05-features/F11-behavioral-evaluation-benchmarks.md', 'prd/05-features/F12-harness-control-tower.md', 'prd/05-features/F13-repair-readiness-authorization.md', 'prd/05-features/F14-format-categories-sequencing.md', 'prd/05-features/F15-development-capsule-handoff.md', 'prd/05-features/F16-v2-migration-release.md', 'prd/05-features/F17-three-compilation-targets.md', 'prd/05-features/F18-builder-workflow-runtime.md', 'prd/06-cross-cutting-nfrs.md', 'prd/07-format-category-constitutions.md', 'prd/08-success-metrics.md', 'prd/09-non-goals-anti-goals.md', 'prd/10-mvp-release-plan.md', 'prd/11-risks-mitigations.md', 'prd/12-assumptions-open-questions.md', 'prd/13-implementation-readiness-handoff.md']

def strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end >= 0:
            return text[end + 5:].lstrip()
    return text

parts = ["# CMF Atomic Harness Builder Next — Combined PRD\n"]
for rel in SECTION_ORDER:
    section = strip_frontmatter((ROOT / rel).read_text(encoding="utf-8"))
    if rel == "prd/05-features/index.md":
        section = section.replace("](F", "](05-features/F")
    parts.append(section)
(ROOT / "prd/PRD_COMBINED.md").write_text("\n\n---\n\n".join(parts).rstrip() + "\n", encoding="utf-8")
print(ROOT / "prd/PRD_COMBINED.md")
