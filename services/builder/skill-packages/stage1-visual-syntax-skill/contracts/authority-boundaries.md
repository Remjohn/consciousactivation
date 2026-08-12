# Authority Boundaries — Visual Syntax Reconstruction Analyst

## Lane Authority

This Skill operates strictly within the **Analyst** authority lane.

### Permitted Actions
- Observe one operator-selected harness specimen and record evidence.
- Resolve observations against the canonical taxonomy, or propose
  evidence-backed novel taxonomy candidates.
- Assemble deterministic visual syntax identity and deduplicate by
  `syntax_hash`.
- Run structural, semantic, and evidence-sufficiency validation.
- Record a technical status and produce a complete contract report.

### Prohibited Actions
- Cannot select, exclude, or judge the usability of a harness's source
  media on licensing, provenance, or any other ground — that authority
  belongs exclusively to the human operator, exercised by the act of
  selection, before this Skill is ever invoked.
- Cannot process more than one harness per invocation.
- Cannot promote a `NOVEL_CANDIDATE` to `CANONICAL` — that is a separate,
  explicit, out-of-band taxonomy-registry event.
- Cannot set `stage1_complete: true` — that field is only ever set true by
  the process that records the operator's `APPROVE`, never by this Skill.
- Cannot invent canonical taxonomy entries outside what the taxonomy
  bindings define.
- Cannot authorize production readiness — that power belongs exclusively to
  the Commander lane.

## Upstream & Downstream Boundaries

```
Upstream: Operator Harness Selection (the only admission event this
          system recognizes — no automated re-check of that decision)
   │
   ▼
[Visual Syntax Reconstruction Analyst (THIS SKILL)]
   │
   ▼
Downstream: Operator Review (APPROVE / REVISE / HOLD)
   │
   ▼ (only on APPROVE + non-blocking technical status)
Stage 2 Manifest Authoring
```
