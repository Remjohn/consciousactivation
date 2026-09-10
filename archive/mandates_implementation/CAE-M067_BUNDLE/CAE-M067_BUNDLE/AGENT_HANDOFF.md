# Mandate ID & Title

**Mandate ID:** `CAE-M067`  
**Mandate Title:** Real Campaign Vertical Slice and Product Operability Proof  
**Requirement / Invariant:** `INV-PRODUCT-REAL-001`

# Summary Table

| File changed | What changed | Invariant proven |
| --- | --- | --- |
| `tests/e2e/m067_real_campaign_harness.py` | Added fail-closed M0067 real/adversarial campaign harness with hash-addressed append-only evidence, environment-fidelity probing, native OpenChatCut admission, state/control evidence, and preserved blocked-run receipts. | Real-product proof cannot be claimed unless native runtime and real source inputs are present; no mock runtime fallback. |
| `tests/e2e/test_m067_real_campaign.py` | Added 8 self-contained M0067 contract/invariant tests covering checkpoints, state grammar, mock rejection, fidelity, adversarial false proofs, manifest hashing, and blocked-run evidence preservation. | M067 evidence/control contract is executable and fail-closed. |
| `tests/e2e/README_M067.md` | Added exact live inputs, commands, evidence boundaries, and blocked-run semantics. | Operator can run the same proof without a developer-only backdoor. |
| `docs/cae/state/CAE_M067_COMPLETION_RECORD.md` | Added durable completion/control record with evidence matrix, environment fidelity, false-proof countercase, tests, state transition, commit limitation, and operator decision gate. | Product operability status is explicit and cannot be inferred from green component tests. |
| `docs/cae/evidence/M067/CAE_M067_E2E_REPORT.json` | Added machine-readable report of the adversarial pass and blocked real campaign, with measured/not-measured/false-proof declarations. | Evidence fidelity and limitations are explicit. |
| `docs/cae/evidence/M067/CAE_M067_ARTIFACT_MANIFEST.json` | Added hash-addressed durable artifact manifest plus transient-run manifest hashes. | Evidence is tamper-evident and traceable to the exact run outputs. |
| `docs/cae/evidence/M067/CAE_M067_RUNTIME_RECEIPTS.json` | Added native-runtime receipt status showing no EXECUTED receipt was issued when OpenChatCut was unreachable. | No fake native-runtime success can satisfy the invariant. |
| `docs/cae/evidence/M067/CAE_M067_OPERATOR_DECISION_RECORD.json` | Added the exact M0067 operator decision question, choices, recommended disposition, and required closure evidence. | Operator authorization remains a human control gate. |
| `docs/cae/evidence/M067/CAE_M067_RESIDUAL_GAP_LEDGER.json` | Added explicit open gaps and closure conditions for runtime, source retrieval, operator intervention, release evidence, and Git identity. | Residual product-operability gaps remain visible and actionable. |

# Files Added and Files Modified

## Files Added

- `AGENT_HANDOFF.md` — this handoff and exact post-apply verification instructions.
- `tests/e2e/m067_real_campaign_harness.py` — M0067 execution harness.
- `tests/e2e/test_m067_real_campaign.py` — M0067 tests.
- `tests/e2e/README_M067.md` — operator/run instructions.
- `docs/cae/state/CAE_M067_COMPLETION_RECORD.md` — durable mandate completion/control record.
- `docs/cae/evidence/M067/CAE_M067_E2E_REPORT.json` — E2E evidence report.
- `docs/cae/evidence/M067/CAE_M067_ARTIFACT_MANIFEST.json` — artifact hash manifest.
- `docs/cae/evidence/M067/CAE_M067_RUNTIME_RECEIPTS.json` — runtime receipt status.
- `docs/cae/evidence/M067/CAE_M067_OPERATOR_DECISION_RECORD.json` — operator decision gate.
- `docs/cae/evidence/M067/CAE_M067_RESIDUAL_GAP_LEDGER.json` — residual gap ledger.

## Files Modified

None. The uploaded repository had no Git metadata; all files above are new additions and no unrelated repository path was modified.

# Exact paste instructions and post-apply commands

1. Copy every file in this bundle to the exact repository-relative destination shown by its path under `CAE-M067_BUNDLE/`. Do not rename or flatten directories.
2. From the repository root, run the mandate-focused regression exactly:

```bash
python -m pytest -q tests/e2e/test_m067_real_campaign.py tests/production_program/test_m0064_asset_selection_binding_lineage.py tests/phase6/test_m065_openchatcut_runtime.py tests/cae/test_m066_human_resolution.py
```

3. Run environment preflight:

```bash
python tests/e2e/m067_real_campaign_harness.py preflight --artifact-root .cae-m067-artifacts
```

4. Run the adversarial campaign:

```bash
python tests/e2e/m067_real_campaign_harness.py adversarial --artifact-root .cae-m067-artifacts
```

5. To attempt the decisive real campaign, use a real Git worktree with a reachable native OpenChatCut runtime and provide all required upstream evidence inputs. Set:

```bash
export OPENCHATCUT_MCP_URL=http://localhost:5199/api/external-mcp/mcp
export CAE_M067_SOURCE_MEDIA=/absolute/path/to/real-source-media.mp4
export CAE_M067_VIDEO_PROGRAM_JSON=/absolute/path/to/governed-video-edit-program.json
export CAE_M067_OPERATOR_EVIDENCE_JSON=/absolute/path/to/persisted-human-resolution-evidence.json
export CAE_M067_RELEASE_EVIDENCE_JSON=/absolute/path/to/persisted-qa-release-evidence.json
```

Then run:

```bash
python tests/e2e/m067_real_campaign_harness.py live --artifact-root .cae-m067-artifacts
```

The live command must reach `REAL_CAMPAIGN_PASS` and `RELEASE_READY` before M0067 can be accepted as the first real product-operability proof. Exit code `2` is an intentional fail-closed result for a missing real boundary; it must not be converted to PASS.

6. Record the exact Git commit SHA and obtain the operator decision in `docs/cae/evidence/M067/CAE_M067_OPERATOR_DECISION_RECORD.json` before authorizing M0068.

# Test Command

```bash
python -m pytest -q tests/e2e/test_m067_real_campaign.py tests/production_program/test_m0064_asset_selection_binding_lineage.py tests/phase6/test_m065_openchatcut_runtime.py tests/cae/test_m066_human_resolution.py
```

# Expected Test Results

**34 automated tests, all passing.**

Observed in the uploaded sandbox: `34 passed in 0.16s`.

The decisive live vertical slice did **not** pass in this sandbox: native OpenChatCut at `http://localhost:5199/api/external-mcp/mcp` was unreachable, no real source-media input was supplied, and the archive contained no `.git` metadata. Those limitations are preserved as evidence and are the reason the operator decision remains `BLOCK` pending real-runtime execution.
