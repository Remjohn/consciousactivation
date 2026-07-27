# Avatar Asset Production Existing System Audit

Branch: `feat/avatar-asset-production-rig-export-v1`

Baseline before bundle integration:

- `PYTHONPATH=src python -m compileall -q src`: passed
- `PYTHONPATH=src python -m pytest -q tests/cmf_studio`: passed, `798 passed, 10 skipped`

## 1. Existing Avatar Performance Files Found

The repo already has a complete no-lip-sync Avatar Performance Layer:

- `src/ccp_studio/contracts/avatar_performance.py`
- `src/ccp_studio/services/avatar_performance_service.py`
- `src/ccp_studio/services/avatar_face_plate_service.py`
- `src/ccp_studio/services/avatar_body_rig_service.py`
- `src/ccp_studio/services/avatar_clip_library_service.py`
- `src/ccp_studio/services/avatar_performance_eval_service.py`
- `src/ccp_studio/services/avatar_render_payload_service.py`
- `src/ccp_studio/services/avatar_prop_attachment_service.py`
- `src/ccp_studio/services/audience_proxy_service.py`
- `src/ccp_studio/services/format02_avatar_performance_adapter_service.py`
- `registries/canonical/avatar_performance/`
- `registries/canonical/skills/shared/avatar_performance/`
- `tests/cmf_studio/test_avatar_performance_layer_v1.py`

This bundle must not overwrite these files. The asset-production bundle should provide physical asset manifests and export payloads that the performance layer can consume later.

## 2. Existing Avatar Identity, Face, Body, and Rig Files Found

Current avatar performance contracts already define:

- `AvatarIdentityProfile`
- `AvatarHybridDesignSpec`
- `AvatarFacePlate`
- `AvatarFacePlateSet`
- `AvatarLayer`
- `AvatarLayerGraph`
- `AvatarRigBone`
- `AvatarPivotMap`
- `AvatarBodyRigManifest`
- `AvatarBodyPose`
- `AvatarBodyPoseLibrary`
- `AvatarGestureClip`
- `Avatar64StateActingLibrary`
- `AvatarPerformancePlan`
- `AvatarRenderPayload`

The repo also has an older paper-cut rig manifest surface:

- `src/ccp_studio/contracts/rig_manifest.py`
- `src/ccp_studio/services/rig_validation_service.py`
- `tests/cmf_studio/test_paper_cut_rig_and_creative_libraries.py`

The older `rig_manifest` file uses UUID-oriented creative library contracts and includes fields such as `mouth_shape_refs`; it is a separate historical rig validation surface. The Avatar Asset Production bundle can be added as a new typed V1 manifest layer without mutating this existing contract.

## 3. Existing Render Payload Files Found

Current render-adjacent files include:

- `src/ccp_studio/services/avatar_render_payload_service.py`
- `src/ccp_studio/contracts/video_editing_engine.py`
- `src/ccp_studio/services/video_render_contract_service.py`
- `src/ccp_studio/services/video_timeline_workbench_service.py`
- `registries/canonical/skills/engines/video/29_video.remotion_props.compile.skill.yaml`
- `tests/cmf_studio/test_video_editing_engine_v1.py`
- `tests/cmf_studio/test_video_timeline_workbench_backend_v1.py`

These surfaces compile payloads and fake render receipts only. The new bundle must stay manifest/read-model only and must not call Remotion, FFmpeg, providers, or renderers.

## 4. Existing Operator-Web Avatar UI Files Found

No dedicated Avatar Library Builder screen was found. Avatar-related strings currently appear indirectly in:

- `operator-web/src/App.jsx`
- `operator-web/src/data.js`
- `operator-web/src/styles.css`
- `operator-web/src/components/timeline/ProxyPreviewPanel.jsx`
- `operator-web/src/components/timeline/TrackLaneStack.jsx`
- `operator-web/src/fixtures/videoTimelineWorkbench.fixture.js`
- `operator-web/src/lib/supervisualViewModel.js`
- `operator-web/src/styles/supervisual.css`
- `operator-web/src/styles/timeline.css`

This integration should not add UI or API routes.

## 5. Existing Stretchy, Spine, and DragonBones References Found

Existing references are registry/docs-oriented rather than executable tool adapters:

- Avatar performance runtime targets include `stretchy_studio_authoring`, `spine_runtime`, `dragonbones_runtime`, and `remotion_layer`.
- `registries/canonical/ontology/master_glossary.v1.csv` contains provider/tool entries for Spine Runtime and Stretchy Studio.
- Historical build docs reference rig authoring, export workers, Remotion, Motion Canvas, and 2D character runtime work.

No real Stretchy Studio, Spine, DragonBones, Remotion, or FFmpeg execution should be introduced in this branch.

## 6. Existing Lip-Sync, Phoneme, and Viseme References Found

Existing no-lip-sync policy is already present:

- `registries/canonical/avatar_performance/no_lipsync_policy.v1.json`
- `src/ccp_studio/contracts/avatar_performance.py` rejects lip sync, phoneme keys, and viseme keys in Avatar Performance contracts.
- `tests/cmf_studio/test_avatar_performance_layer_v1.py` verifies no-lip-sync behavior.

Historical tests/docs also mention `mouth_flap`, especially older paper-cut rig preview checks. Those should remain untouched. The new asset-production layer must explicitly reject lip sync, phonemes, visemes, jaw drivers, and mouth-flap clips.

## 7. Naming Conflicts

Potential overlap:

- `AvatarFacePlate` and `AvatarFacePlateSet` already exist in `avatar_performance.py`.
- `AvatarBodyRigManifest` already exists in `avatar_performance.py`.
- `RigManifest` exists in `rig_manifest.py`.
- Runtime target names for Stretchy Studio, Spine, DragonBones, and Remotion already exist as avatar-performance enum values.

Resolution:

- Keep Avatar Performance as the behavioral planning owner.
- Add Avatar Asset Production as the physical asset, PSD/layer, tool-manifest, export-manifest, QA, and continuity owner.
- Do not modify existing performance or legacy rig files unless a narrow compatibility import issue is discovered during tests.

## 8. Additive Application Decision

The bundle can be applied additively. It should introduce:

- `src/ccp_studio/contracts/avatar_asset_production.py`
- Asset-production services under `src/ccp_studio/services/`
- `registries/canonical/avatar_asset_production/`
- `registries/canonical/skills/shared/avatar_asset_production/`
- fixtures and tests under new paths

No existing Avatar Performance, rig validation, video render, or operator-web file needs to be overwritten for the V1 manifest integration.

## 9. Files That Require Merge Instead of Copy

No target files were found that require merge before bundle application. If the unzipped bundle contains package `__init__.py` files or other broad exports, those should not be copied unless tests prove an additive export is required.
