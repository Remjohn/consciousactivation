# M0077 — ArcReel Production Review / Regeneration Mapping

Status: **IMPLEMENTED / OPERATOR REVIEW REQUIRED**

## External behavior source

| Field | Evidence |
|---|---|
| Repository | `https://github.com/ArcReel/ArcReel` |
| Frozen release | `v0.29.0` |
| Exact commit | `6ddedc775e7fe5f398b10081ab741985f7dceda7` |
| License | GNU Affero General Public License v3 (`AGPL-3.0`) |
| Exact source file | `agent_runtime_profile/.claude/skills/generate-storyboard/SKILL.md` |
| Exact source file | `agent_runtime_profile/.claude/skills/generate-video/SKILL.md` |
| Current-main note | Current ArcReel skill structure has evolved beyond this frozen path. Current-main material was used only to corroborate that this remains an active workbench pattern; the adapter is based on the exact frozen files above. |

## Extracted behavior → CAE mapping

| ArcReel behavior | CAE target / authority | Extracted contract | Excluded behavior |
|---|---|---|---|
| Load/generate → review checkpoint → approve / edit / regenerate | `editorial_storyboard_program` + `STORYBOARD_STATE_MACHINE_V1` | Treat the external flow as a review interaction over existing CAE storyboard state. Approval maps to the existing `storyboard_editorial_approval` gate and COMMANDER lane. | No ArcReel project/workflow state is copied into CAE. |
| Local image adjustment distinct from changing the underlying generation intent | `ChangeRequestProgramModel` / revision API | Map local adjustment to the existing revision compilation path. Keep edit and generation intent distinct. | No ArcReel editing tool, image prompt, or provider call is imported. |
| Changing underlying storyboard intent causes explicit regeneration | Existing `operator_request_regeneration` / candidate lineage | Map regeneration to operator-commanded, constrained regeneration with immutable predecessor/rejected-candidate lineage and decision receipt. | No model/provider routing or external generation queue is adopted. |
| Timeline/canvas inspection | `TimelineProjectionModel` | Inspect the canonical timeline projection; use existing native revision contracts for edits. | No second canvas model or persisted ArcReel timeline authority. |
| Historical outputs are kept usable and not silently replaced | `EditorialDecisionReceiptRecord` + candidate predecessor lineage | Preserve rejected/superseded candidate identity and operator receipt. | No ArcReel version store or rollback implementation is copied. |
| Stage-specific progression and resumable review | Existing CAE storyboard / visual-derivative state machines | Use the already-canonical CAE state transitions and gates rather than reimplementing stage state in the adapter. | No external workflow scheduler/state machine adoption. |
| Evidence/quality checks before generation and result-status distinctions | Existing evidence verification, dual-axis QA and release gate | Require source evidence lineage and fail closed on stale/unauthorized/malformed requests. | No provider checkpoint semantics or external runtime health is treated as CAE evidence. |

## Evidence-first constraint

For this extraction, the adapter enforces source lineage before review/production actions: `RETRIEVE → TRANSFORM → COMPOSE → GENERATE` remains a CAE production-ordering constraint. The adapter does not generate anything and therefore stops at the interaction-contract boundary.

## Adapter boundary

`programs/visual_derivative_production_program/reference/arc_reel_review_adapter.py` is an isolated, deterministic reference component. It:

- represents an observed external interaction without importing an external state model;
- validates actor, approval, evidence provenance and state freshness;
- maps the interaction to an existing CAE target/operation/lane;
- emits a deterministic SHA-256 mapping fingerprint for replay/evidence;
- performs no network calls, provider selection, model invocation, database writes, rendering, or state transition.

The adapter therefore cannot establish external runtime reachability or visual quality. Those remain operator/runtime evidence obligations.

## Authority mapping

1. CAE semantic meaning remains authoritative upstream of the adapter.
2. Canonical storyboard and visual-derivative state machines remain the only state authorities.
3. Existing revision APIs remain the only revision program authority for timeline/canvas edits.
4. Existing editorial discovery regeneration remains the only candidate-regeneration authority.
5. Human operator approval remains the promotion gate.
