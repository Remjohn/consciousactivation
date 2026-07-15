# Acceptance Criteria

The following criteria preserve the confirmed ST-01.01 acceptance contract and make its authorized Format 02 condition explicit.

## AC-01 — Create one governed run

**Given** all dependency outputs are accepted, covered authority is available, and the authorized target is `atomic_content_harness` with profile `2d_character_animation/format02_minimal_coach_theatre`  
**When** the Harness Architect selects exactly that one compilation target/profile and starts the governed lifecycle  
**Then** the run has stable identity, explicit authority, replay-safe initial state, compiler and operator bindings, and target-specific required work.

## AC-02 — Resume without hidden replacement or repeated decision

**Given** a run has committed events, a valid checkpoint and a recorded human decision receipt  
**When** an authorized operator resumes it  
**Then** the same run identity is restored from the newest valid checkpoint/event sequence, the human decision is referenced rather than replayed, and outstanding target-specific work is preserved.

## AC-03 — Reject ambiguous or unauthorized target selection

**Given** zero targets, multiple targets, an unknown target, a conversational profile, or an external-target execution request  
**When** run creation is requested  
**Then** the request fails with a typed reason, no target is defaulted, no run/event/checkpoint is committed, and no VAE or Delegation behavior is activated.

## AC-04 — Enforce legal lifecycle transitions

**Given** a governed run and its immutable target profile  
**When** an authorized actor requests a legal transition with satisfied prerequisites and the expected stream version  
**Then** exactly one typed event is appended, state advances once, a deterministic command receipt is returned, and replay yields the same state.

## AC-05 — Reject invalid transitions and unsafe waivers

**Given** an invalid lifecycle edge, incomplete prerequisite, stale stream version, unauthorized actor, expired waiver, or waiver that attempts to bypass a non-waivable production gate  
**When** the command is evaluated  
**Then** it returns a typed rejection, records observable failure context outside authoritative state, and appends no state-changing event.

## AC-06 — Preserve idempotency

**Given** an accepted command identity  
**When** the identical command is retried  
**Then** the original event and receipt identities are returned without duplicate mutation; reusing the identity with different payload is rejected.

## AC-07 — Fail closed on invalid resume state

**Given** a corrupt or policy-incompatible checkpoint  
**When** resume is requested  
**Then** the run is not silently reset, no human decision is replayed, a diagnostic identifies the invalid checkpoint/input, and authoritative state remains unchanged.

## AC-08 — Preserve compatibility and authority boundaries

**Given** the shared lifecycle and three governed compilation-target identities  
**When** the bounded implementation is inspected and tested  
**Then** shared lifecycle semantics remain target-profile versioned, only Format 02 is executable, Format 02 is still merely `contract_compatible`, and no generated harness, evidence, workflow, Control Tower, VAE, Delegation, conversational, or certification behavior exists locally.

## AC-09 — Produce completion evidence

**Given** all preceding criteria pass  
**When** Story completion is evaluated  
**Then** success/failure observability evidence, exact test results, changed-file hashes, rollback evidence, gate dispositions and a `ST-01.01:StoryCompletionReceipt` are emitted with run/story/artifact/authority/version/provenance/outcome/failure-context fields.

