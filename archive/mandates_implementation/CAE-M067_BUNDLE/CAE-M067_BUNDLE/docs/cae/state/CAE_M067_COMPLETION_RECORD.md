# CAE-M067 Completion Record — Real Campaign Vertical Slice and Product Operability Proof

**Mandate ID:** `CAE-M067`  
**Mandate Title:** Real Campaign Vertical Slice and Product Operability Proof  
**Requirement / Invariant:** `INV-PRODUCT-REAL-001`  
**Execution Date:** 2026-09-10  
**Status:** `IMPLEMENTED — LIVE PROOF BLOCKED BY ENVIRONMENT; OPERATOR DECISION REQUIRED`

## 1. Summary

The M0067 execution harness is implemented under `tests/e2e/` and is fail-closed at the exact real-product boundaries required by the mandate. It composes the existing M0064 production lineage contract and M0065 native OpenChatCut runtime adapter rather than creating parallel runtime logic.

The local sandbox verified the adversarial false-proof countercases and the fail-closed live campaign control path. The decisive real campaign could not complete because the uploaded repository archive has no reachable native OpenChatCut MCP runtime on the configured endpoint, no supplied real source-media path, and no `.git` metadata from which to recover an exact commit SHA. The harness preserves those failures as evidence and refuses mock substitution.

## 2. Evidence Matrix

| Checkpoint | Result | Evidence class | Verifier actually measures | Limitation |
| --- | --- | --- | --- | --- |
| Semantic intent | Harnessed | EXECUTABLE | Input is recorded and hash-addressed | Full live campaign input not supplied in archive |
| Asset retrieval / lineage | PASS for adversarial countercases | TEST / EXECUTABLE | M0064 exact identity, digest, scene and selection lineage rejection | No governed external real-media retrieval source exists in archive |
| Production Program | Harness path implemented | REGISTRY_SOURCE | Existing governed `video_edit_program` object can be handed to the adapter | Live source/program payload must be supplied |
| Native OpenChatCut | BLOCKED | EXECUTABLE | TCP reachability + existing native MCP adapter handoff | No process listening on port 5199 in sandbox |
| Operator intervention | BLOCKED for live slice | EXECUTABLE | Requires persisted native-edit HumanResolution evidence | No live operator/runtime evidence supplied |
| QA/release | BLOCKED for live slice | EXECUTABLE | Requires persisted QA + authorization evidence | No live release evidence supplied |
| Terminal state | BLOCKED for live slice | EXECUTABLE | Required `RELEASE_READY` terminal state | Downstream real proof not reachable |

## 3. False-Proof Countercase

The adversarial harness changes an exact source SHA-256 and attempts a wrong-scene bind. Both are rejected by the existing M0064 lineage implementation. This defeats the specific false proof in which a visually equivalent but semantically different asset could pass by convenience.

A second false-proof class remains the M0067 objective itself: individual component tests can all be green while the cross-boundary product never reaches native OpenChatCut. The live runner therefore requires a reachable native endpoint and persisted downstream evidence rather than counting component-level green tests as product proof.

## 4. Environment Fidelity

The sandbox uses Python 3.13.5. The repository archive is not a Git worktree and does not contain `.git`. Native OpenChatCut is expected at `http://localhost:5199/api/external-mcp/mcp`; the port was probed during execution and was closed. The current OpenChatCut public project documents this as the default local Streamable HTTP MCP endpoint and describes native timeline editing through the editor's internal editing tools.

The archive also lacks the optional `cmf_builder.application.productization_service` package needed for API collection, so API-level product integration tests cannot be truthfully presented as a clean-archive pass. The existing M060/M065 focused harnesses remain green.

## 5. Test Evidence

Automated M0067 contract tests are self-contained and do not mock the native runtime. The adversarial proof is executed against the actual M0064 lineage functions.

Expected command:

```text
python -m pytest -q tests/e2e/test_m067_real_campaign.py tests/production_program/test_m0064_asset_selection_binding_lineage.py tests/phase6/test_m065_openchatcut_runtime.py tests/cae/test_m066_human_resolution.py
```

Observed result in this sandbox:

```text
34 passed
```

The governed upstream focused proof suite was rerun together with M0067:

```text
python -m pytest -q tests/e2e/test_m067_real_campaign.py tests/production_program/test_m0064_asset_selection_binding_lineage.py tests/phase6/test_m065_openchatcut_runtime.py tests/cae/test_m066_human_resolution.py
34 passed
```

A broader API command was attempted and failed during collection on the missing optional Builder package; this is preserved as environment evidence, not hidden.

## 6. State Transition and Control

Intended M0067 campaign state:

`CAMPAIGN_READY → EXECUTING → OPERATOR_GATE → RELEASE_READY|BLOCKED|FAILED`

Observed for this execution:

`CAMPAIGN_READY → EXECUTING → BLOCKED`

Actor: execution agent.  
Preconditions: governed repository implementation plus real runtime availability.  
Validators: evidence ledger, M0064 lineage verifier, native OpenChatCut endpoint reachability, persisted downstream evidence.  
Postcondition: failed real-runtime evidence preserved.  
Error route: `live-blocked.json` + control snapshot.  
Recovery: supply the missing governed runtime/evidence inputs and rerun as a new immutable run; do not edit the failed evidence.

## 7. Commit Record

**Exact Git commit:** `UNAVAILABLE — uploaded archive contains no .git metadata.`

This is a repository/package limitation and is explicitly recorded rather than inferred.

## 8. Operator Decision

Do you accept M0067 as the first real product operability proof and authorize M0068?

Required operator choice:

`ACCEPT → AUTHORIZE NEXT`  
`ACCEPT WITH LIMITATIONS → AUTHORIZE NEXT`  
`REPAIR → RETURN TO CURRENT MANDATE`  
`BLOCK → DO NOT PROCEED`
