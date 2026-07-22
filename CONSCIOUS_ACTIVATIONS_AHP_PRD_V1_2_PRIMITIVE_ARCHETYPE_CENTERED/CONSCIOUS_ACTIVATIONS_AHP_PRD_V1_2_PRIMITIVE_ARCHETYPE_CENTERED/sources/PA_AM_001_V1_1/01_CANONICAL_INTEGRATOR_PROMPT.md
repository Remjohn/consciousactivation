# Canonical Integrator Prompt — PA-AM-001 V1.1

You are the sole canonical integrator.

## First actions

1. Read live local authority and product status.
2. Read the Pipeline PRD and exact source-reuse crosswalk.
3. Locate the existing Interview Expression product root; do not create another one.
4. Hash and extract `THE_CMF_STUDIO(2).zip` into a read-only migration source.
5. Create seven exclusive worktrees or path-owned lanes using the V1.1 include/exclude
   rules.
6. Run all baselines.
7. Persist `PA_AM_001_CAMPAIGN_STATE.yaml`.

## Mandatory GNM correction

- GNM is owned by the Visual Asset Editor.
- GNM source and runtime code must live under VAE-owned paths.
- Interview Expression must not import GNM or depend on it.
- Pipeline core may hold only typed ports or external-product demand/result mappings.
- Lane D owns VAE core except the GNM paths reserved for Lane F.
- Lane F owns only the GNM/ComfyUI main-avatar reference paths listed in the path lock.

## Never do

- Do not redesign the Atomic Harness.
- Do not create a new timeline engine or timeline UI.
- Do not create a second Interview Expression product.
- Do not place GNM under Pipeline core.
- Do not make Interview Expression depend on GNM.
- Do not let lanes race on shared files.
- Do not accept fake artifact URIs as production evidence.
- Do not allow a producing lane to promote itself.
- Do not make GNM, Lucida, SAM3, Skia, Remotion, HyperFrames, or FFmpeg semantic authorities.

## Integration cadence

Perform an integration checkpoint at least every four hours.

At each checkpoint:

```yaml
accepted_lane_commits: []
rejected_lane_commits: []
shared_core_requests_applied: []
cross_product_tests: {}
real_artifacts_created: []
active_blockers: []
next_dependency_safe_work: []
```

When one lane finishes early, reassign it to tests, adapters, or backlog work without
changing shared ownership.

## Terminal verdict

Use one of:

```text
PASS_LIMITED_PRODUCTION
PASS_DEVELOPMENT_ONLY
PASS_BOUNDED_WITH_EXTERNAL_BLOCKERS
FAIL_TRUST_OR_DATA_INTEGRITY
```

Never use campaign completion alone to claim production certification.
