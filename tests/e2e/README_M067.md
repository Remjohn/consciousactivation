# CAE-M067 — Real Campaign Vertical Slice and Product Operability Proof

`tests/e2e/m067_real_campaign_harness.py` is the governed M0067 execution harness. It reuses the repository's existing M0064 production binding and M0065 native OpenChatCut adapter and refuses to substitute a fake/mock/stub runtime.

## Required live inputs

A decisive real campaign requires all of the following in the execution environment:

```text
OPENCHATCUT_MCP_URL              default: http://localhost:5199/api/external-mcp/mcp
CAE_M067_SOURCE_MEDIA            path to a real non-synthetic source artifact
CAE_M067_VIDEO_PROGRAM_JSON      path to the already-governed video_edit_program payload
CAE_M067_OPERATOR_EVIDENCE_JSON  path to persisted HumanResolution/native-edit evidence
CAE_M067_RELEASE_EVIDENCE_JSON   path to persisted QA + operator release evidence
```

The harness captures a cryptographic evidence ledger, receipt IDs, checkpoint transitions, environment fidelity, and control-state snapshot. It does not invent upstream artifacts or convert synthetic repository fixtures into production proof.

## Commands

Contract tests:

```bash
python -m pytest -q tests/e2e/test_m067_real_campaign.py tests/production_program/test_m0064_asset_selection_binding_lineage.py tests/phase6/test_m065_openchatcut_runtime.py tests/cae/test_m066_human_resolution.py
```

Adversarial false-proof proof:

```bash
python tests/e2e/m067_real_campaign_harness.py adversarial --artifact-root .cae-m067-artifacts
```

Live preflight:

```bash
python tests/e2e/m067_real_campaign_harness.py preflight --artifact-root .cae-m067-artifacts/preflight
```

Live real campaign:

```bash
python tests/e2e/m067_real_campaign_harness.py live --artifact-root .cae-m067-artifacts
```

`live` returns exit code `2` and writes `live-blocked.json` when a required real boundary is unavailable. That failure is preserved; it is never converted into PASS.

## Evidence boundary

Measured by the harness: checkpoint presence, evidence hashing, environment identity, native OpenChatCut endpoint reachability, exact source bytes supplied to the OpenChatCut adapter, and the existing M0064 lineage false-proof defenses.

Not measured until the required live evidence inputs are supplied: operator judgment quality, actual native timeline mutation, persisted human-resolution refresh/reopen, final QA, release authorization, and downstream shipment.

Current uploaded archive limitation: it contains no `.git` metadata, so an exact repository commit SHA cannot be recovered from the archive itself.
