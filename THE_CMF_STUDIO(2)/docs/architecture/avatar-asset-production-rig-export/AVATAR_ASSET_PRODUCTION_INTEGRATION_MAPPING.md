# Avatar Asset Production Integration Mapping

Avatar Asset Production + Rig Export V1 defines how the avatar physically exists. It is separate from Avatar Performance, which defines what the avatar does.

## 1. Avatar Performance Layer

Recommended call site:

```text
AvatarPerformancePlan
-> expression plate names
-> body pose names
-> gesture/action intent
-> Avatar Asset Production approved plates, body layers, action clips, and runtime payloads
```

Mapping rules:

- `AvatarPerformancePlan` chooses expression plate and body pose.
- Avatar Asset Production supplies approved face plates, canonical body layers, action timeline clips, and runtime payload manifests.
- Performance logic must stay in `AvatarPerformanceLayerService`.
- Asset production must not decide primitive/SFL meaning, audience proxy behavior, or scene performance state.
- Both layers must preserve the no-lip-sync policy.

## 2. Project Workspace / Artifact Store

Recommended storage:

```text
client_workspaces/<client_slug>/libraries/avatar/
client_workspaces/<client_slug>/runs/<run_id>/assets/avatar/
```

Recommended artifact categories:

- Face plates: `ArtifactCategory.AVATAR`
- Paper body layers: `ArtifactCategory.AVATAR`
- Stretchy, Spine, DragonBones, and Remotion payload manifests: `ArtifactCategory.MANIFEST`
- QA and continuity receipts: `ArtifactCategory.RECEIPT`

V1 integration tests register face plate read models into the workspace artifact store and compile an avatar library manifest. No file-byte materialization is required by this bundle.

## 3. Capability Preflight

Avatar Asset Production V1 is manifest-only and does not require provider/runtime execution.

Future real production should call Capability Preflight before any generating or runtime step:

```text
CapabilityPreflightService.run_preflight(
  pipeline_id=PipelineId.AVATAR_64_STATE_LIBRARY_GENERATION,
  ideogram_configured=...,
  flux_configured=...,
  sample_approved=...
)
```

Rules:

- Real provider image generation for plates/layers requires preflight.
- Batch generation remains blocked until sample approval.
- Stretchy, Spine, DragonBones, Remotion, and FFmpeg execution must be gated through runtime/local-worker preflight when those adapters exist.

## 4. Video Editing Engine

Recommended downstream shape:

```text
AvatarRemotionLayerPayload
-> Video timeline avatar layer props later
-> Remotion timeline render later
```

V1 payloads are not final renders. They must not execute renderers, Remotion, FFmpeg, or providers.

## 5. Template Preview / Atlas

Format 02 template preview can later display avatar slots from Avatar Asset Production manifests:

- face plate slot
- body layer slot
- prop socket slot
- action timeline clip slot
- Remotion layer payload inspector

Template Preview should remain deterministic SVG/read-model only until a real preview renderer is separately gated by Capability Preflight.

## 6. Stretchy Studio

V1 only emits `StretchyStudioImportManifest`.

The manifest prepares:

- PSD/layer source refs
- canonical layer mapping
- skeleton hints
- mesh candidates
- shape-key candidates
- prop sockets
- action timeline refs

Real Stretchy Studio integration should be a future local tool or worker adapter. This bundle must not call Stretchy Studio.

## 7. Spine / DragonBones

V1 only emits export manifests:

- `SpineExportManifest` requires license confirmation.
- `DragonBonesExportManifest` requires JS runtime compatibility.
- `AvatarRigExportManifest` references the target-specific manifests.

Real export execution should be implemented later through a gated local worker or tool adapter.
