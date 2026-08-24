# CAE WP-08 — Reality Contact and Reward-Hacking Resistance

**Status:** `COMPLETE_PENDING_OPERATOR_REVIEW`
**Work package:** WP-08 — reality-contact testing and reward-hacking resistance
**Scope:** the existing staging-only evidence-to-AIR first slice; no evaluator,
legacy service, API route, registry consumer, or durable schema was added.

## Objective and work-package boundary

Turn the operational claims of `CAE-EVID-001` into governed, contrastive E3
tests. The package tests whether the real staging adapter can be made to appear
successful while violating its source, authentication, concurrency, operator,
or receipt-lineage conditions. It does not claim a human judgment, semantic
direction, SDA/SFL fit, anti-centroid quality, audience response, or any E4
outcome.

Allowed artifacts were the WP-08 test-governance manifest, the bounded staging
proof, and CAE implementation records. Production architecture is unchanged.

## Test-governance contract

[The suite manifest](../evaluations/EVIDENCE_TO_AIR_FIRST_SLICE_WP08_EVALUATION_SUITE.yaml)
defines six material tests using the required governance fields: claim ID,
class, subject, fixture provenance, fidelity, execution path, assertions,
expected failure, reward-hacking scenario, taste/anti-centroid risk, evidence
status, and receipt requirement.

| Test | Primary class | Operational claim | Adversarial condition | Result |
|---|---|---|---|---|
| `WP08-ENV-001` | `ENVIRONMENT_FIDELITY` | source bytes correspond to staged metadata | metadata-only success with different bytes | PASS |
| `WP08-RH-001` | `REWARD_HACK` | capture requires a verified source | asset exists but is only `STAGED` | PASS — rejected |
| `WP08-RH-002` | `REWARD_HACK` | idempotency identifies one canonical command | reuse valid key with changed quoted text | PASS — conflict |
| `WP08-RH-003` | `REWARD_HACK` | assessment requires independently authenticated evidence | proposal before authentication; capture actor self-authenticates | PASS — rejected |
| `WP08-STATE-001` | `STATE` | state/decision guards prevent false advancement | stale expected version; empty decision | PASS — rejected with no domain side effect |
| `WP08-CLAIM-001` | `REWARD_HACK` | a structural receipt cannot assert quality proof | execution receipt carries unearned semantic/taste result | PASS — fields remain unverified/not-applicable |

## Executed E3 proof

`python scripts/cae/verify_wp08_reality_contact.py` performed one real staging
run. It uploaded a unique object to the private `cae-media` bucket, downloaded
its bytes through the Supabase Storage API, and compared their SHA-256 to the
asset metadata used by the transition fixture. It then executed the positive
five-step path and all listed negative paths inside a force-rolled-back
PostgreSQL transaction. The temporary object was deleted in `finally`.

The run passed all assertions, including exact cardinality of five commands,
envelope receipts, execution receipts, and receipt-evidence links. The test
did not leave database fixtures or a Storage object behind.

## What this proves

- The staging PostgreSQL/Supabase Storage topology supports the bounded
  transition and receipt/evidence-lineage claims at `E3_PRODUCTION_SHAPED`.
- The tested shortcuts cannot produce a falsely advanced transition in the
  actual adapter path.
- The receipt layer preserves the distinction between `TRACEABLE` evidence
  lineage and semantic/taste/anti-centroid proof.

## What this does not prove

| Claim category | Status | Reason |
|---|---|---|
| semantic correctness / SDA direction | `UNVERIFIED` | no semantic evaluator or registry-consuming runtime exists |
| taste / anti-centroid integrity | `NOT_APPLICABLE` to this slice | the lifecycle has no content-quality output to assess |
| authenticated human truth | `UNVERIFIED` | fixture actors and source are test-controlled |
| audience/world outcome | `E4_NOT_ATTEMPTED` | no live human or external outcome was observed |
| real existing-service integration | `E2/E3_NOT_PROVEN` | no Interview Expression or AIR service route invokes the adapter |

## Discovery: verified-source authority boundary

`capture_evidence()` checks that its source `media_asset.lifecycle_state` is
`VERIFIED`. That is the correct current operation precondition, but the adapter
does not itself fetch bytes from Storage or establish that lifecycle state. The
WP-08 fixture independently downloaded and hashed its object before creating
the `VERIFIED` fixture record, so the environment assertion is meaningful; it
does not prove that a future upstream writer cannot forge `VERIFIED` metadata.

This is an explicit integration requirement for the next vertical slice, not a
reason to relabel the current adapter as an end-to-end source-verification
system. The existing bounded contract must retain the upstream verification
boundary until an authorized source bridge supplies provenance.

## Exact operator decision

**Promote WP-08 and authorize WP-09 to bind one real existing evidence-source
path into the CAE verified-source contract, preserving current SQLite service
authority until transition-by-transition cutover evidence exists and requiring
explicit media-verification provenance before the bridge may set `VERIFIED`?**
