from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PRD = ROOT / "prd"
ORDER = ['00-document-purpose.md', '01-vision-product-promise.md', '02-users-jobs-journeys.md', '03-glossary.md', '04-doctrine-product-principles.md', '05-features/index.md', '05-features/F01-product-constitution-autonomous-authority.md', '05-features/F02-visual-asset-demand-intake.md', '05-features/F03-asset-ontology-reference-production.md', '05-features/F04-immutable-asset-lifecycle.md', '05-features/F05-composition-intent-image-conditioned-geometry.md', '05-features/F06-multi-method-resolution-routing.md', '05-features/F07-dynamic-specialist-workcell.md', '05-features/F08-visual-capability-registry.md', '05-features/F09-visual-production-plan-ir.md', '05-features/F10-event-sourced-production-runtime.md', '05-features/F11-visual-asset-memory-recurrence.md', '05-features/F12-hybrid-visual-compute-fabric.md', '05-features/F13-visual-capability-development.md', '05-features/F14-visual-evaluation-profiles.md', '05-features/F15-repair-invalidation-reruns.md', '05-features/F16-budget-programs-candidate-portfolios.md', '05-features/F17-steering-intelligence-cmf-okf-retrieval.md', '05-features/F18-control-tower-supervisory-console.md', '05-features/F19-asynchronous-service-delegation.md', '05-features/F20-constraint-conflicts-amendments.md', '05-features/F21-benchmarks-certification-release1.md', '05-features/F22-versioning-readiness-development-capsule.md', '06-cross-cutting-nfrs.md', '07-asset-families-release-scope.md', '08-success-metrics.md', '09-non-goals-anti-goals.md', '10-mvp-release-plan.md', '11-risks-mitigations.md', '12-assumptions-open-questions.md', '13-implementation-readiness-handoff.md']
LINK_RE = re.compile(r"(\[[^\]]+\]\()([^)]+)(\))")

def strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end >= 0:
            return text[end + 5:].lstrip()
    return text

def rebase_links(text: str, source_rel: str) -> str:
    source_dir = Path(source_rel).parent
    def repl(match):
        prefix, target, suffix = match.groups()
        if target.startswith(("http://", "https://", "#", "mailto:", "asset://", "visual-memory://", "benchmark://", "registry://")):
            return match.group(0)
        base, *frag = target.split("#", 1)
        if not base:
            return match.group(0)
        rebased = (source_dir / base).as_posix()
        # Normalize relative path segments without touching filesystem.
        parts = []
        for part in rebased.split("/"):
            if part in ("", "."):
                continue
            if part == "..":
                if parts:
                    parts.pop()
                else:
                    parts.append("..")
            else:
                parts.append(part)
        rebased = "/".join(parts)
        if frag:
            rebased += "#" + frag[0]
        return prefix + rebased + suffix
    return LINK_RE.sub(repl, text)

header = """---
title: PRD: CMF Visual Asset Editor
product: CMF Visual Asset Editor
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
source: sharded_prd
---

# PRD: CMF Visual Asset Editor

> Combined reading view generated from the canonical shards listed in [`index.md`](index.md). Edit the shards, not this file.
"""
parts = [header]
for rel in ORDER:
    text = strip_frontmatter((PRD / rel).read_text(encoding="utf-8"))
    parts.append("\n\n---\n\n" + rebase_links(text, rel))
(PRD / "PRD_COMBINED.md").write_text("".join(parts).rstrip() + "\n", encoding="utf-8")
print(PRD / "PRD_COMBINED.md")
