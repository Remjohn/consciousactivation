# VAE GNM Main-Avatar Facial Geometry and Expression Reference Plan

## Governing decision

GNM is a subordinate Visual Asset Editor tool.

```yaml
product_owner: Visual Asset Editor
pipeline_core_owner: false
interview_expression_owner: false
```

GNM creates controllable 3D head geometry and expression references for visual
generation and editing. It does not own interview analysis, Expression Moments,
identity meaning, visual taste, or production acceptance.

## Primary purpose

Provide a repeatable facial-geometry spine for the approved Conscious Activations main
avatar and generate precise expression, pose, and gaze reference packs from bounded
visual-expression specifications.

## Main-avatar stack

```text
Canonical main-avatar identity and character bible
        ↓
approved source-image set
        ↓
fitted or manually approved GNM identity geometry profile
        ↓
bounded expression, pose, and gaze controls
        ↓
GNM mesh and reference passes
        ↓
ComfyUI image generation or image editing
        ↓
VAE evaluation
        ↓
Avatar Asset Result
```

GNM is only the facial geometry and expression embodiment. Hair, body, costume,
illustration style, environment, and complete visual identity remain separate governed
assets or profiles.

## Immediate deterministic baseline

Use the existing GNM semantic expression sampler and model controls before training a
new model.

Inputs:

```yaml
avatar_expression_reference_request:
  avatar_identity_profile_ref: required
  desired_expression:
    semantic_labels: []
    blend_weights: {}
    intensity: 0.0
    asymmetry: {}
  head_pose: {}
  gaze: {}
  camera_views:
    - front
    - three_quarter
    - profile
  seed: required
  output_passes:
    - rgb
    - depth
    - normals
    - silhouette
    - landmarks
    - semantic_masks
```

Outputs:

```yaml
gnm_avatar_reference_pack:
  mesh_ref: required
  multiview_render_refs: []
  depth_refs: []
  normal_refs: []
  silhouette_refs: []
  landmark_refs: []
  mask_refs: []
  control_program_ref: required
  execution_receipt_ref: required
```

## Main-avatar identity rule

Do not use GNM demographic semantic identity sampling as the canonical main-avatar
identity.

The initial avatar profile must be fitted or manually approved from governed source
images and stored as a pinned identity-geometry profile. If production-quality fitting
cannot be completed in the campaign, use an explicitly approved temporary identity
profile and mark it as development-only.

## ComfyUI integration

GNM runs in an isolated Python worker. ComfyUI receives the resulting control pack.

Target VAE paths:

```text
02_VISUAL_ASSET_EDITOR/
  src/cmf_vae/domain/avatar/
    avatar_identity_profile.py
    expression_reference_spec.py
    gnm_reference_pack.py

  src/cmf_vae/application/avatar_expression/
    compile_expression_reference.py
    generate_avatar_reference_pack.py

  src/cmf_vae/adapters/gnm/
    model_loader.py
    identity_profile.py
    expression_compiler.py
    mesh_generator.py
    reference_renderer.py
    receipts.py

  src/cmf_vae/adapters/comfyui/gnm/
    request_mapper.py
    workflow_client.py
    result_mapper.py

  comfyui/workflows/
    gnm_avatar_expression_reference_v1.json
    gnm_avatar_expression_edit_v1.json

  tests/stage5/gnm/
```

Initial workflows:

1. `gnm_avatar_expression_reference_v1`
   - create a new avatar visual from the approved avatar identity plus GNM reference
     passes;

2. `gnm_avatar_expression_edit_v1`
   - change the expression of an approved avatar image while retaining the avatar's
     established appearance.

## Relationship to Interview Expression

There is no direct dependency.

```text
Interview Expression product
    may emit an Expression Moment and Asset Package Spec

Atomic Harness Pipeline
    may determine that an avatar visual is required

Delegation
    carries a Visual Asset Demand

VAE
    invokes GNM when the chosen production plan calls for a 3D expression reference
```

Interview Expression must not:

- import GNM;
- create GNM model parameters;
- load GNM weights;
- require GNM for completion;
- treat GNM output as evidence of a person's actual inner state.

## Future Programmed Model candidate

The launch does not require fine-tuning.

A future learned capability claim may translate a bounded expression description into
named GNM controls and bounded residuals:

```text
desired avatar expression
+ intensity
+ asymmetry
+ head pose
+ gaze
+ expression phase
→ named GNM control program
→ deterministic GNM parameter compiler
```

The learned model should not initially emit an unconstrained full expression vector.

## Seven-day lane outcome

1. Pin GNM source and model-data identities.
2. Load one approved backend.
3. Create or approve one main-avatar identity geometry profile.
4. Generate a neutral mesh.
5. Generate at least five controlled expression reference packs.
6. Export mesh plus front, three-quarter, and profile renders.
7. Produce depth, normal, silhouette, landmark, and mask passes where supported.
8. Execute one ComfyUI reference-generation or expression-edit workflow.
9. Validate file existence, hashes, identity continuity, and requested expression.
10. Emit VAE-owned asset and execution receipts.

This outcome is a parallel enhancement. It does not block the minimum release unless
explicitly promoted into the launch scope by the integrator.
