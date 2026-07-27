---
title: "Batch 2 Asset Program Compilers Build Receipt"
status: "implemented"
implemented_at: "2026-06-25"
batch: "Batch 2 - Asset and Program Compilers"
specs:
  - "TS-CMF-093"
  - "TS-CMF-094"
  - "TS-CMF-095"
  - "TS-CMF-096"
  - "TS-CMF-097"
  - "TS-CMF-098"
  - "TS-CMF-099"
  - "TS-CMF-100"
  - "TS-CMF-101"
  - "TS-CMF-102"
  - "TS-CMF-103"
  - "TS-CMF-104"
  - "TS-CMF-105"
  - "TS-CMF-106"
  - "TS-CMF-110"
  - "TS-CMF-111"
  - "TS-CMF-112"
  - "TS-CMF-113"
  - "TS-CMF-114"
  - "TS-CMF-115"
  - "TS-CMF-116"
  - "TS-CMF-117"
  - "TS-CMF-118"
  - "TS-CMF-119"
---

# Batch 2 Asset Program Compilers Build Receipt

## Implemented Files

- `THE CMF STUDIO/src/ccp_studio/contracts/asset_program_compilers.py`
- `THE CMF STUDIO/src/ccp_studio/repositories/asset_program_compilers.py`
- `THE CMF STUDIO/src/ccp_studio/services/asset_program_compiler_service.py`
- `THE CMF STUDIO/src/ccp_studio/api/v1/asset_program_compilers.py`
- `THE CMF STUDIO/src/ccp_studio/generated/typescript/asset_program_compiler_contracts.ts`
- `THE CMF STUDIO/tests/cmf_studio/test_batch2_asset_program_compilers.py`

## Runtime Coverage

- Animation Studio migration manifest, rig edit operation, headless frame render request/receipt, and avatar export worker job/receipt.
- Geometrics still visual scene specs with Skia/SAM3/PRETEXT bindings and deterministic Skia render receipts.
- Carousel slide library loader from `registries/composition/carousel_slide_composition_library.v1.json`, sequence planner, builder program, atlas route receipt, and export receipt.
- Single-image/SuperVisual registry snapshot, archetype route decision, primitive triad family contract, provider job planner, layer materialization, Skia scene compiler, golden fixture, and eval review receipt.
- VideoEditProgram with four canonical video format scenes, OTIO audit manifest, proxy render contract, and final FFmpeg render contract.
- 2D character genesis, 64-pose rig contract, provider adapter sandbox decision, transcript-timed performance program, render receipt, and repair plan path.
- Conscious sequencing kernel, Interview Brief V2 hypothesis/acquisition plan, live ingredient coverage, cue suppression, expression ingredient inventory, content sequence handoff packages, sequence eval receipt, and learning receipt.
- CMF registry boundary enforcement so loaded registries must live under `THE CMF STUDIO`.

## Verification

Commands run:

```powershell
python -m pytest "THE CMF STUDIO/tests/cmf_studio/test_batch2_asset_program_compilers.py"
python -m pytest "THE CMF STUDIO/tests/cmf_studio" -k "carousel or single_image or supervisual or skia or geometrics"
python -m pytest "THE CMF STUDIO/tests/cmf_studio" -k "two_d_character or papercut or animation or avatar"
python -m pytest "THE CMF STUDIO/tests/cmf_studio" -k "video_edit or otio or sequence or ingredient or interview_brief"
python -m pytest "THE CMF STUDIO/tests/cmf_studio"
```

Results:

- Batch 2 direct suite: 7 passed.
- Still visual/Skia filter: 3 passed, 470 deselected.
- Animation/2D character filter: 13 passed, 460 deselected.
- Video/sequence filter: 26 passed, 447 deselected.
- Full CMF Studio regression: 471 passed, 2 skipped.

## Exit Criteria Status

- Pydantic contracts validate for carousel, SuperVisual, single image, 2D character, sequence, and parent video edit programs.
- Registry loaders validate CMF-owned registry bundles and block paths outside `THE CMF STUDIO`.
- Skia/Geometrics and video render contracts are deterministic and receipt-backed.
- `VideoEditProgram` emits OTIO audit, proxy render, and final render contracts.
- `TwoDCharacterSceneProgram` compiles transcript-timed character performance cues.
- `ContentSequenceProgram` hands off to still visual/video compilers and blocks unsupported guest truth.
- Golden/negative fixtures cover each compiler family.
