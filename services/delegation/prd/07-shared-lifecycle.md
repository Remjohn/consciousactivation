---
title: Shared Lifecycle
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: draft_for_review
created: '2026-07-13'
updated: '2026-07-13'
---


# 7. Shared Delegation Lifecycle

The external lifecycle describes the cross-product commitment. It does not expose Visual Asset Editor production nodes or Content Harness internal sequencing states.

## States

- **`DRAFT`** — Demand exists under Content Harness authority but has not been submitted. Owner: `content_harness`. Terminal: `false`.

- **`SUBMITTED`** — A valid submission message is under boundary validation or has entered routing. Owner: `content_harness`. Terminal: `false`.

- **`REJECTED`** — Submission failed contract, authority, integrity, compatibility, or admission validation. Owner: `delegation_protocol`. Terminal: `true`.

- **`ACCEPTED`** — The VAE accepted the negotiated demand for execution. Owner: `visual_asset_editor`. Terminal: `false`.

- **`IN_PROGRESS`** — Production is active; internal details remain product-private. Owner: `visual_asset_editor`. Terminal: `false`.

- **`RESULT_READY`** — A production-accepted Asset Result awaits downstream acknowledgement. Owner: `visual_asset_editor`. Terminal: `false`.

- **`RESULT_REJECTED`** — The current result failed downstream compatibility acknowledgement for a stable protocol reason. Owner: `content_harness`. Terminal: `false`.

- **`COMPLETED`** — A valid result was acknowledged and the delegation completed. Owner: `delegation_protocol`. Terminal: `true`.

- **`AMENDMENT_REQUIRED`** — Execution cannot continue without a demand-owned or policy-owned change. Owner: `visual_asset_editor`. Terminal: `false`.

- **`SUPERSEDED`** — This demand version was replaced by a newer authoritative version. Owner: `content_harness`. Terminal: `true`.

- **`COST_APPROVAL_REQUIRED`** — Further work requires a new budget authorization. Owner: `visual_asset_editor`. Terminal: `false`.

- **`CAPABILITY_GAP`** — No certified production capability can satisfy the current demand. Owner: `visual_asset_editor`. Terminal: `false`.

- **`HUMAN_REVIEW_REQUIRED`** — Automation reached a governed exception boundary. Owner: `visual_asset_editor`. Terminal: `false`.

- **`CANCELLATION_REQUESTED`** — A validated cancellation request blocks new work pending safe stop. Owner: `content_harness`. Terminal: `false`.

- **`CANCELLED`** — Production stopped safely and a disposition receipt was emitted. Owner: `visual_asset_editor`. Terminal: `true`.

- **`PARTIAL_RESULT_READY`** — A typed subset is ready under the declared completion policy. Owner: `visual_asset_editor`. Terminal: `false`.

- **`INVALIDATED`** — The result requires revalidation for current use; history remains valid. Owner: `owning_product`. Terminal: `true`.

- **`REVOKED`** — The result or asset is blocked for new and active consumption. Owner: `visual_asset_editor_or_integrity_authority`. Terminal: `true`.

- **`REPLACED`** — A governed replacement was validated for future use. Owner: `owning_product`. Terminal: `true`.

## Canonical transitions

| From | To | Authoritative trigger | Authority |

|---|---|---|---|

| `DRAFT` | `SUBMITTED` | `visual_asset_submission` | `content_harness` |

| `SUBMITTED` | `REJECTED` | `submission_receipt.rejected` | `delegation_protocol` |

| `SUBMITTED` | `ACCEPTED` | `submission_receipt.accepted` | `visual_asset_editor` |

| `ACCEPTED` | `IN_PROGRESS` | `visual_asset_event.execution_started` | `visual_asset_editor` |

| `IN_PROGRESS` | `RESULT_READY` | `asset_result_contract` | `visual_asset_editor` |

| `IN_PROGRESS` | `PARTIAL_RESULT_READY` | `asset_result_contract.partial` | `visual_asset_editor` |

| `RESULT_READY` | `COMPLETED` | `result_acknowledgement.accepted` | `content_harness` |

| `RESULT_READY` | `RESULT_REJECTED` | `result_acknowledgement.rejected` | `content_harness` |

| `RESULT_REJECTED` | `IN_PROGRESS` | `visual_asset_event.revalidation_started` | `visual_asset_editor` |

| `ACCEPTED` | `AMENDMENT_REQUIRED` | `amendment_proposal` | `visual_asset_editor` |

| `IN_PROGRESS` | `AMENDMENT_REQUIRED` | `amendment_proposal` | `visual_asset_editor` |

| `AMENDMENT_REQUIRED` | `SUPERSEDED` | `demand_supersession` | `content_harness` |

| `ACCEPTED` | `COST_APPROVAL_REQUIRED` | `budget_escalation_request` | `visual_asset_editor` |

| `IN_PROGRESS` | `COST_APPROVAL_REQUIRED` | `budget_escalation_request` | `visual_asset_editor` |

| `COST_APPROVAL_REQUIRED` | `IN_PROGRESS` | `budget_escalation_response.approved` | `content_harness` |

| `COST_APPROVAL_REQUIRED` | `CAPABILITY_GAP` | `budget_escalation_response.denied_capability_gap` | `content_harness` |

| `ACCEPTED` | `CAPABILITY_GAP` | `delegation_failure.capability_gap` | `visual_asset_editor` |

| `IN_PROGRESS` | `CAPABILITY_GAP` | `delegation_failure.capability_gap` | `visual_asset_editor` |

| `ACCEPTED` | `HUMAN_REVIEW_REQUIRED` | `delegation_failure.human_exception` | `visual_asset_editor` |

| `IN_PROGRESS` | `HUMAN_REVIEW_REQUIRED` | `delegation_failure.human_exception` | `visual_asset_editor` |

| `SUBMITTED` | `CANCELLATION_REQUESTED` | `cancellation_request` | `content_harness` |

| `ACCEPTED` | `CANCELLATION_REQUESTED` | `cancellation_request` | `content_harness` |

| `IN_PROGRESS` | `CANCELLATION_REQUESTED` | `cancellation_request` | `content_harness` |

| `CANCELLATION_REQUESTED` | `CANCELLED` | `cancellation_receipt` | `visual_asset_editor` |

| `SUBMITTED` | `SUPERSEDED` | `demand_supersession` | `content_harness` |

| `ACCEPTED` | `SUPERSEDED` | `demand_supersession` | `content_harness` |

| `IN_PROGRESS` | `SUPERSEDED` | `demand_supersession` | `content_harness` |

| `COMPLETED` | `INVALIDATED` | `invalidation_notice` | `owning_product` |

| `COMPLETED` | `REVOKED` | `revocation_notice` | `visual_asset_editor_or_integrity_authority` |

| `COMPLETED` | `REPLACED` | `replacement_notice_and_ack` | `owning_product` |

| `INVALIDATED` | `REPLACED` | `replacement_notice_and_ack` | `owning_product` |

| `REVOKED` | `REPLACED` | `replacement_notice_and_ack` | `owning_product` |

## Projection rules

- Product events change shared state only after envelope, schema, authority, compatibility and transition validation.
- Internal progress events may update observability while preserving the same shared state.
- Terminal states reject ordinary progress events.
- Post-completion invalidation, revocation and replacement use dedicated message types.
- The projection must be reconstructible from the append-only audit sequence.
