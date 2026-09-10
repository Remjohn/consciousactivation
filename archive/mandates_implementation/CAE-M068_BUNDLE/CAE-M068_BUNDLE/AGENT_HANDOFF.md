# CAE-M068 — Production Readiness and Residual-Gap Certification

## Mandate ID & Title

**Mandate ID:** `CAE-M068`  
**Mandate Title:** `Production Readiness and Residual-Gap Certification`  
**Requirement / Invariant:** `INV-CERT-REAL-001`

## Summary Table (File changed | What changed | Invariant proven)

| File changed | What changed | Invariant proven |
|---|---|---|
| `docs/cae/evidence/M068/CAE_M068_PRODUCTION_READINESS_CERTIFICATION_REPORT.md` | Added the final cross-boundary certification report, 10-criterion evaluation, evidence scope, false-proof countercase, state transition, limitations, and operator gate. | `INV-CERT-REAL-001` is fail-closed: production readiness is not claimed while decisive real-runtime evidence is blocked. |
| `docs/cae/evidence/M068/CAE_M068_READINESS_MATRIX.json` | Added the machine-readable readiness matrix mapping M0058–M0067 to `VERIFIED`, `PARTIAL`, or `BLOCKED` with exact evidence references. | Every completion criterion is explicitly classified against observed evidence. |
| `docs/cae/evidence/M068/CAE_M068_RESIDUAL_GAP_LEDGER.json` | Added the immutable residual-gap ledger, closure requirements, authority lanes, and proposed next campaign frontier. | Open readiness blockers remain explicit and cannot be converted into status inflation. |
| `docs/cae/evidence/M068/CAE_M068_EVIDENCE_MANIFEST.json` | Added SHA-256 manifest for upstream M0067 evidence plus M0068 report, matrix, ledger, log, state, and test. | Evidence provenance is content-addressed; exact Git commit is recorded as unavailable because the archive contains no `.git`. |
| `docs/cae/evidence/M068/CAE_M068_VERIFICATION_TEST_LOG.md` | Added exact commands, outputs, environment failures, live preflight/campaign results, and final automated counts. | Verification fidelity and environment/code failure distinction are preserved. |
| `docs/cae/state/CAE_M068_COMPLETION_RECORD.md` | Added the M0068 control-state record and required operator decision. | `EVIDENCE_COMPLETE → CERTIFY → BLOCKED` is captured with recovery and stop conditions. |
| `tests/cae/test_m068_production_readiness_certification.py` | Added self-contained tests for the 10-criterion matrix, evidence references, blocker preservation, manifest hashes, report/state consistency, and next-campaign boundary. | Certification artifacts are structurally and semantically self-consistent. |

## Files Added and Files Modified (with exact relative repository destination paths and rationale)

### Files Added

`docs/cae/evidence/M068/CAE_M068_PRODUCTION_READINESS_CERTIFICATION_REPORT.md`  
Rationale: required final Production Readiness Certification Report.

`docs/cae/evidence/M068/CAE_M068_READINESS_MATRIX.json`  
Rationale: required 10-criterion certification/readiness matrix.

`docs/cae/evidence/M068/CAE_M068_RESIDUAL_GAP_LEDGER.json`  
Rationale: required residual-gap ledger and next campaign frontier.

`docs/cae/evidence/M068/CAE_M068_EVIDENCE_MANIFEST.json`  
Rationale: required exact evidence and provenance manifest.

`docs/cae/evidence/M068/CAE_M068_VERIFICATION_TEST_LOG.md`  
Rationale: required verification test log with command/output fidelity.

`docs/cae/state/CAE_M068_COMPLETION_RECORD.md`  
Rationale: required control-state update and operator gate record.

`tests/cae/test_m068_production_readiness_certification.py`  
Rationale: comprehensive self-contained M0068 certification tests.

### Files Modified

None. The supplied archive has no Git metadata, so file modification state is established by the bundle contents and execution record rather than an inferred Git diff.

## Exact paste instructions and post-apply commands (migrations, setup, scripts)

1. Copy the seven added files from this bundle into the exact repository destinations shown above, preserving paths.
2. No database migrations are required by M0068. No application/source feature changes are authorized by this mandate.
3. Ensure the repository is a Git worktree before the final operator gate so the exact commit SHA can be captured.
4. For the decisive next real-runtime campaign, provide:
   - a reachable native OpenChatCut MCP endpoint at the configured URL;
   - governed real source media plus retrieval/provenance/rights evidence;
   - persisted operator HumanResolution evidence;
   - QA/release authorization evidence.
5. Run the certification test and the preserved focused proof commands below.
6. Do not start the proposed next campaign as part of M0068. Await the operator decision.

Post-apply verification commands:

```bash
python -m pytest -q tests/cae/test_m068_production_readiness_certification.py

python -m pytest -q tests/e2e/test_product_e2e_fixture.py tests/e2e/test_live_e2e_proof_harness.py tests/asset_intelligence/test_cinematic_corpus_m062.py tests/asset_intelligence/test_cinematic_retrieval_m063.py tests/production_program/test_m0064_asset_selection_binding_lineage.py tests/phase6/test_m065_openchatcut_runtime.py tests/cae/test_m066_human_resolution.py tests/e2e/test_m067_real_campaign.py

python tests/e2e/m067_real_campaign_harness.py preflight --artifact-root .cae-m067-artifacts/preflight

python tests/e2e/m067_real_campaign_harness.py live --artifact-root .cae-m067-artifacts/live
```

Expected live behavior until the required environment is supplied: `preflight`/`live` remain fail-closed and may exit `2`; such failures are evidence of an unavailable prerequisite, not a passing production proof.

## Test Command (exact pytest/test command to verify)

```bash
python -m pytest -q tests/cae/test_m068_production_readiness_certification.py
```

## Expected Test Results (number of automated tests, all passing)

**11 automated tests; 11 passing; 0 failing.**

The separately rerun focused upstream proof command completed **64 passed, 0 failed**. A broader combined command also attempted `tests/mandates/test_cae_m059_control_surface.py` and failed at collection because `psycopg` is unavailable in the sandbox. This is preserved in `CAE_M068_VERIFICATION_TEST_LOG.md` as an environment dependency failure and does not alter the M068 test result.

**Certified operational status:** `BLOCKED`  
**Operator decision required:** accept, accept with limitations, repair, or block.

**Exact Git commit SHA:** unavailable in the supplied archive because `.git` metadata is absent.  
**Source archive SHA-256:** `ed8dab3cf191a356469fbf749dfa53ef6c6b216123df880e1eab30ee6c50f252`
