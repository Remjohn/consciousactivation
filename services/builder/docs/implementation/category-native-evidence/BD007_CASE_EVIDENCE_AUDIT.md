# BD-007 Case Evidence Audit

Date: 2026-07-17  
Scope: ST-06.03 development-only, non-certifying evidence  
Verdict: `PASS_WITH_EXPERIMENT_AMENDMENT_REQUIRED`

## Existing frozen contract

The v1 experiment requires every executable case to use exactly one
`CorpusMemberBinding` from the canonical 48-member BD-004 archive admission. That rule
is implemented in `experiment_contracts.py` and repeated in the case manifest and
trial plan. It is valid historical governance and has not been modified.

The admitted archive can support two cases:

1. Short-Form Edited Video through admitted member 152.
2. Format 02 / 2D Character Animation through admitted member 54.

It contains no admitted conversational member and no admitted generic
`NOT_APPLICABLE` control member. The four-case v1 experiment is therefore not
executable as written.

## Generic non-Activative control

The completed PX-AM-001 package contains a repository-owned generic operator manifest
fixture for `generic_text_summary_v1`. Its PZ-01 and PZ-04 receipts prove deterministic
governed ingestion, explicit generic mode, category non-applicability, immutable
compilation, portable export, and non-production/non-certification boundaries.

This is suitable as existing governed repository evidence for a generic negative
control. It is not BD-004 archive evidence and must never be labeled as such. The
fixture's placeholder provenance reference is synthetic fixture data, not external
source authority.

Disposition: `ADMITTED_EXISTING_GOVERNED_REPOSITORY_EVIDENCE`, pending approval of the
experiment amendment that adds a typed repository-evidence binding.

## Structural conversational control

The repository contains:

- the exact fifth constitutional category and four structural conversational profiles;
- the Shared Activative Core schema;
- the conversational-expression schema;
- an uncertified ReelCast structural example with an Activative Call, intended
  reaction, micro-commitment, and non-empty wrong-reading lock but no Reaction Receipt
  or Expression Moment;
- the ST-06.01 one-of-five category receipt; and
- the ST-06.02 structural profile-registry receipt.

Together these can support a repository-owned synthetic structural conversational
control. The case must use `reelcast_expression`, remain `UNCERTIFIED`, keep Reaction
Receipt and Expression Moment collections empty, and assert that no human reaction or
truth was observed. The example is a contract fixture, not a real profile, transcript,
human-reaction corpus, or proof of conversational production behavior.

Disposition: `ADMITTED_SYNTHETIC_STRUCTURAL_CONTROL`, pending approval of the
experiment amendment that adds a typed synthetic-structural binding.

## Amendment consequence

No case is removed. The proposed v2 experiment retains all four cases, two arms, three
repeats, the frozen 17-dimension rubric, and all nine non-compensable failures. It
changes only the source-binding union so a case can cite either an admitted BD-004
archive member or exact hash-pinned repository evidence with its own authority chain.

Semantic breadth is retained, but evidence maturity becomes heterogeneous:

- Short-form and Format 02 are development-only admitted historical evidence.
- Conversational is synthetic structural evidence.
- Generic is a repository-owned non-Activative control.

This is sufficient only to test ST-06.03 category-native-versus-flattened behavior in
a development branch. It cannot close broader provider comparison, real conversational
evidence, production benchmarking, production readiness, or certification.

The amendment remains inactive until explicit governed human approval. Until then,
BD-007 remains deferred and no request hash or provider call may be created.
