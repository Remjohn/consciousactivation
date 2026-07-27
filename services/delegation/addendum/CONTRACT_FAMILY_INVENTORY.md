---
title: Contract Family Inventory
product: CMF Content Harness ↔ Visual Asset Editor Delegation Protocol
version: 0.1.0-draft
status: reference
created: '2026-07-13'
updated: '2026-07-13'
---


# Contract Family Inventory

| Contract | Producer | Consumer | Purpose | Lifecycle effect |
|---|---|---|---|---|

| `delegation-envelope` | `boundary_service` | `all_products` | Common metadata and integrity wrapper for protocol messages. | `none` |

| `visual-asset-demand` | `content_harness` | `visual_asset_editor` | Authoritative immutable visual demand resource. | `DRAFT` |

| `visual-asset-submission` | `content_harness` | `delegation_protocol` | Submits one demand under an execution policy. | `DRAFT→SUBMITTED` |

| `submission-receipt` | `delegation_protocol_or_vae` | `content_harness` | Accepts or rejects a submission after validation and admission. | `SUBMITTED→ACCEPTED|REJECTED` |

| `visual-asset-event` | `visual_asset_editor` | `delegation_protocol_and_content_harness` | Projects VAE progress or exceptions into the shared lifecycle. | `ACCEPTED|IN_PROGRESS` |

| `delegation-set` | `content_harness` | `delegation_protocol_and_vae` | Coordinates related independent demands under shared constraints. | `none` |

| `budget-authorization` | `content_harness` | `delegation_protocol_and_vae` | Authorizes Budget Program, ceilings, and escalation policy. | `none` |

| `budget-escalation-request` | `visual_asset_editor` | `content_harness` | Requests additional authorized production envelope. | `→COST_APPROVAL_REQUIRED` |

| `budget-escalation-response` | `content_harness` | `visual_asset_editor` | Approves or denies a budget extension. | `COST_APPROVAL_REQUIRED→IN_PROGRESS|CAPABILITY_GAP` |

| `cancellation-request` | `content_harness` | `visual_asset_editor` | Authoritatively requests safe cancellation. | `→CANCELLATION_REQUESTED` |

| `cancellation-receipt` | `visual_asset_editor` | `content_harness` | Records safe stop, disposition, and compute. | `CANCELLATION_REQUESTED→CANCELLED` |

| `constraint-conflict` | `visual_asset_editor` | `content_harness` | Reports infeasibility without mutating demand. | `→AMENDMENT_REQUIRED|CAPABILITY_GAP` |

| `amendment-proposal` | `visual_asset_editor` | `content_harness` | Proposes typed non-binding field-level changes. | `→AMENDMENT_REQUIRED` |

| `amendment-response` | `content_harness` | `visual_asset_editor` | Accepts, rejects, or requests alternatives. | `AMENDMENT_REQUIRED` |

| `demand-supersession` | `content_harness` | `delegation_protocol_and_vae` | Links a new demand version and declares changed authority fields. | `old→SUPERSEDED` |

| `selective-invalidation-receipt` | `visual_asset_editor` | `content_harness` | Explains reuse, invalidation, and resume point after change. | `none` |

| `asset-result-contract` | `visual_asset_editor` | `content_harness` | Returns production-accepted assets, geometry, evaluations, and receipts. | `IN_PROGRESS→RESULT_READY|PARTIAL_RESULT_READY` |

| `result-acknowledgement` | `content_harness` | `delegation_protocol_and_vae` | Accepts or rejects current downstream consumption compatibility. | `RESULT_READY→COMPLETED|RESULT_REJECTED` |

| `invalidation-notice` | `owning_product` | `delegation_protocol_and_consumers` | Requires revalidation because dependencies or authority context changed. | `COMPLETED→INVALIDATED` |

| `revocation-notice` | `visual_asset_editor_or_integrity_authority` | `delegation_protocol_and_consumers` | Blocks new/active consumption for a critical defect or integrity issue. | `COMPLETED→REVOKED` |

| `replacement-notice` | `owning_product` | `delegation_protocol_and_consumers` | Proposes a governed replacement result or asset. | `INVALIDATED|REVOKED→REPLACED after ack` |

| `delegation-failure` | `detecting_product_or_protocol` | `decision_owner` | Carries stable failure family, code, responsibility, retry, and invalidation semantics. | `exception-dependent` |

| `delegation-audit-receipt` | `delegation_protocol` | `audit_consumers` | Append-only chained validation and transition evidence. | `none` |

| `compatibility-manifest` | `content_harness_or_vae` | `delegation_protocol` | Declares supported protocol/message versions, features, profiles, and limitations. | `none` |

| `contract-migration` | `authorized_migration_service` | `delegation_protocol_and_products` | Creates a new immutable contract representation with equivalence evidence. | `none` |

## V1.1 constitutional contract overlay

`visual-asset-demand@1.1` is the canonical demand representation. It retains
the stronger closed local geometry and identity model while adding exact
Activative lineage, Activation Contract, Visual Semantic Pack, Visual Narrative
Program, Feature Contracts, T/V routing, and non-empty wrong-reading locks.
`compatibility-manifest` now describes behavioral modes and evaluator evidence;
`contract-migration` records the immutable owner-context V1-to-V1.1 transform.
No other message family or lifecycle effect changes.
