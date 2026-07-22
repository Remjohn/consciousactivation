# CCP Avatar Asset Production + Rig Export V1 Integration Bundle

This bundle builds the physical avatar asset-production layer.

## Why this is separate from Avatar Performance

Avatar Performance Layer V1 defines:

```text
what the avatar does
expression plate
body pose
gesture clip
audience proxy plan
performance state
```

Avatar Asset Production + Rig Export V1 defines:

```text
how the avatar physically exists
face plates
paper body layers
PSD/layer requirements
Stretchy Studio import manifest
Spine export manifest
DragonBones export manifest
Remotion avatar layer payload
QA and rig continuity receipts
```

## Purpose

Format 02 cannot become real production until avatar assets and rig exports exist.

This bundle creates contracts and deterministic services for:

```text
AvatarCharacterSpec
AvatarAssetProductionPlan
AvatarPSDLayerRequirement
AvatarFacePlateApprovalSet
AvatarPaperBodyLayerSet
AvatarRigExportManifest
StretchyStudioImportManifest
SpineExportManifest
DragonBonesExportManifest
AvatarActionTimeline
AvatarCharacterQAReport
AvatarRigContinuityReceipt
AvatarRemotionLayerPayload
```

## Stretchy Studio posture

V1 treats Stretchy Studio as an external authoring/runtime target through manifests only.

It does not call Stretchy Studio.

It prepares import manifests for:

```text
PSD / layered source
layer mapping
skeleton hints
mesh candidates
shape-key candidates
prop sockets
action clips
```

## Apply after

Recommended:

```text
Avatar Performance Layer V1
Project Workspace + Artifact Store V1
Template Preview / Atlas V1
Capability Preflight + Provider Menu V1
```

## Do not

```text
Do not call Stretchy Studio.
Do not call Spine.
Do not call DragonBones.
Do not call Remotion.
Do not render.
Do not call providers.
Do not add UI/API endpoints.
Do not add lip sync.
Do not add phonemes.
Do not add visemes.
Do not create talking avatar assets.
```

## Hard laws

```text
Avatar asset production V1 is no-lip-sync.
Face plates cannot carry phoneme/viseme keys.
Mouth animation is disabled.
Face plate approval set requires the 8 canonical expressions.
Paper body layer set requires canonical body layers.
PSD layer requirements cannot contain path traversal.
Stretchy Studio import manifest requires PSD/layer source, skeleton hints, mesh candidates, and prop sockets.
Spine export manifest requires license confirmation.
DragonBones export manifest requires JS-runtime compatibility declaration.
Action timeline clips require positive duration and no lip-sync.
QA report fails if required face plates, body layers, bones, sockets, or no-lip-sync policy are missing.
Rig continuity receipt fails if identity anchors, face plates, body layers, or rig version drift.
```

## V1 limitations

```text
manifest/contracts only
no real PSD parsing
no real Stretchy Studio integration
no real Spine export
no real DragonBones export
no real Remotion render
no provider calls
no UI/API endpoints
```
