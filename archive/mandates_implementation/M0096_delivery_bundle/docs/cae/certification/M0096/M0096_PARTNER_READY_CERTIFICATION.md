# M0096 — Partner-Ready Evidence-First Visual Production Vertical Slice

**Status:** `BLOCKED — OPERATOR DECISION REQUIRED`  
**Production readiness:** `NOT-READY`  
**Partner-ready:** `NO`  
**Execution date:** 2026-09-11  
**Campaign:** `E2 CERTIFICATION`

## Certification basis

This bounded certification audits and composes the existing CAE path rather than creating competing authorities. The snapshot already contains the canonical Storyboard session/revision model, deterministic TransformationIntent/TransformationRecipe compilation, Visual Asset Studio operator surface, M0065 OpenChatCut adapter, and M0067 real-campaign fail-closed harness.

The current run does **not** honestly establish the terminal partner-ready state because required reality-contact boundaries are unavailable.

## Gate matrix

| Gate | Class | Status | Evidence | Limitation |
|---|---|---:|---|---|
| Current constitution / precedence mapping | `MIGRATION` + `TEST` | PASS | Current canonical relocated constitution hashes to the precedence-contract authority hash; dated authority pack exists under `docs/AUTHORITY_PACK/...` | Literal mandate paths are absent; creating copies would create competing authority. |
| Existing Storyboard + Transformation chain reuse | `EXECUTABLE` + `TEST` | PASS (audit) | Existing M0079/M0083/M0085 artifacts and canonical source paths | Current Python product tests are not reproducible in this dependency-incomplete sandbox. |
| Evidence-first order and false-proof countercase | `TEST` + `DOCUMENT` | PASS (audit) | `RETRIEVE → TRANSFORM → COMPOSE → GENERATE`; `test_good_looking_but_ungrounded_asset_is_blocked` | Audit verifies control presence, not perceptual quality. |
| Real governed source retrieval | `EXECUTABLE` | BLOCKED | M0067 live environment fidelity reports `source_media.present=false` | No real source media artifact was supplied. |
| Native OpenChatCut reachability | `EXECUTABLE` | BLOCKED | M0067 live probe: `ConnectionRefusedError: [Errno 111] Connection refused` | Native runtime not reachable; no mock fallback permitted. |
| Operator correction / persisted revision | `EXECUTABLE` | NOT REACHED | Existing contract requires immutable feedback and `GOOD` before compile | Cannot execute live correction without source/runtime path. |
| Optional SAM3 tracking | `HYPOTHESIS` / `OPERATOR_DECISION_REQUIRED` | NOT PROVEN | No native SAM3 path is reachable in this supplied snapshot/run | Do not claim SAM3 capability from documentation alone. |
| Runtime receipt / QA / release authorization | `EXECUTABLE` | NOT REACHED | M0067 ledger stops at runtime precondition failure | No final preview, native receipt, or release authorization exists. |
| Exact current CAE commit | `EXECUTABLE` | BLOCKED | `git metadata present=false`, `git_commit_sha=null` | Supplied archive contains no `.git`; exact commit cannot be truthfully manufactured. |

## Live blocking evidence

Exact command:

```bash
python tests/e2e/m067_real_campaign_harness.py live --artifact-root /tmp/m0096-live
```

Observed result: exit code `2`, status `REAL_CAMPAIGN_BLOCKED`, terminal state `BLOCKED`.

Decisive observed conditions:

- Native endpoint: `http://localhost:5199/api/external-mcp/mcp`
- OpenChatCut: unreachable; `ConnectionRefusedError: [Errno 111] Connection refused`
- `CAE_M067_SOURCE_MEDIA`: unset / `null`
- Real source media: absent
- Git metadata: absent
- Native runtime, operator intervention, QA/release and terminal release were not reached
- No mock runtime or synthetic success receipt was used

The append-only M0067 evidence manifest from this run is preserved under `docs/cae/evidence/M0096/M0096_M067_LIVE_BLOCKER_EVIDENCE.json`.

## Environment/test limitation

The first dependency-backed focused test collection failed on `ModuleNotFoundError: No module named 'psycopg'`. A temporary external shim was then used only to identify the next missing repository dependency, `cmf_builder`; no shim was committed and no product success was inferred. Installing `psycopg[binary]` was attempted but the environment could not resolve the package index (`Temporary failure in name resolution`).

The new M0096 certification audit is intentionally stdlib-only and passes. It verifies the authority mapping, canonical brownfield path, evidence-first controls and live fail-closed gate, but it does not substitute for dependency-complete product execution.

## Operator visual/semantic gate

No real campaign preview was generated. Therefore the operator has not yet inspected a real preview, judged perceptual quality, verified semantic faithfulness of a transformation, confirmed absence of gratuitous attention, or approved source lineage for a partner deliverable.

## Conclusion

**M0096 cannot be certified partner-ready from the supplied snapshot and environment.** The correct terminal state is `BLOCKED`, not a fabricated success state.

### Operator decision required

Select exactly one:

`APPROVE` — accept this bounded blocked certification.  
`APPROVE-WITH-LIMITATIONS` — accept with the listed limitations and route the missing runtime/source/commit evidence to the next controlled execution context.  
`REJECT` — return the mandate for repair/re-execution.

The execution agent does not self-promote.
