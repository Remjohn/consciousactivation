# CMF STUDIO Tech Specs

This directory contains implementation-facing tech specs generated from `docs/epics.md` stories.

Each spec must preserve the legacy ERA3/BMAD writing discipline while adapting it to the CMF STUDIO greenfield architecture:

- Python-first runtime with Pydantic v2 contracts, FastAPI APIs, durable workflows, DSPy programs, and Pi orchestration.
- TypeScript only for PWA, Telegram Mini App, Remotion, Motion Canvas, and generated contract consumers.
- Legacy Inventory as read-only intelligence, fixture, registry, eval, doctrine, or worker-asset source. No direct production imports.
- Every state mutation through the Command Bus.
- Every spec mapped to FR IDs, canonical pipeline stage, entry object, exit object, validation contract, allowed actor or service, and required receipt.
- Every spec includes CBAR tension, failure scenario, resolution demand, downstream proof, tests, and a spec audit receipt.

## Initial Dependency Order

1. `TS-CMF-001-contract-kernel-command-spine.md`
2. `TS-CMF-002-pipeline-stage-orchestration-records.md`
3. `TS-CMF-003-python-dspy-pi-bmad-spec-workflow.md`
4. `TS-CMF-004-organization-and-brand-workspace-lifecycle.md`
5. `TS-CMF-005-role-based-production-permissions.md`
6. `TS-CMF-006-commercial-entitlements-without-offer-drift.md`
7. `TS-CMF-007-pwa-and-telegram-state-parity.md`
8. `TS-CMF-008-versioned-consent-records.md`
9. `TS-CMF-009-recording-setup-and-source-artifact-gate.md`
10. `TS-CMF-010-consent-blockers-across-workflows.md`
11. `TS-CMF-011-voice-dna-boost-eligibility-and-audio-classification.md`
12. `TS-CMF-012-consent-and-source-review-surface.md`
13. `TS-CMF-013-migration-ledger-inventory-and-hashing.md`
14. `TS-CMF-014-registry-conversion-fixtures-and-evals.md`
15. `TS-CMF-015-jit-skill-compiler-saturation-and-contrast.md`
16. `TS-CMF-016-legacy-import-hidden-prompt-and-template-gates.md`
17. `TS-CMF-017-intentional-orchestration-migration-contracts.md`
18. `TS-CMF-018-brand-genesis-intake-and-session-creation.md`
19. `TS-CMF-019-64-state-acting-library.md`
20. `TS-CMF-020-paper-cut-rig-and-creative-libraries.md`
21. `TS-CMF-021-brand-context-version-locking-and-forking.md`
22. `TS-CMF-022-production-gate-to-locked-brand-context.md`
23. `TS-CMF-023-research-fields-and-evidence-capture.md`
24. `TS-CMF-024-guest-dossier-audience-reality-context-premise-and-resonance.md`
25. `TS-CMF-025-matrix-of-edging-brief.md`
26. `TS-CMF-026-interviewer-pre-induction.md`
27. `TS-CMF-027-interview-asset-contract-and-quality-gate.md`
28. `TS-CMF-028-cral-context-premise-emotional-dna-and-root-down-induction.md`
29. `TS-CMF-029-complete-expression-session-creation.md`
30. `TS-CMF-030-source-ingestion-transcript-alignment-and-provenance.md`
31. `TS-CMF-031-anchor-hit-and-expression-moment-candidate-detection.md`
32. `TS-CMF-032-expression-moment-review-and-boundary-control.md`
33. `TS-CMF-033-archetype-and-asset-derivative-routing.md`
34. `TS-CMF-034-guest-asset-pack-spec-generation.md`
35. `TS-CMF-035-rejected-candidate-and-coalition-fatality-memory.md`
36. `TS-CMF-036-complete-editing-session-creation-from-approved-source.md`
37. `TS-CMF-037-scenespec-creative-state-and-render-contract-compilation.md`
38. `TS-CMF-038-ideogram-4-compositionjob-lineage.md`
39. `TS-CMF-039-layer-manifests-animation-plans-edl-captions-and-sonic-plans.md`
40. `TS-CMF-040-revision-and-reconstruction-audit.md`
41. `TS-CMF-041-scene-containers-creative-subsystems-and-asset-roll-orchestration.md`
42. `TS-CMF-042-provider-capability-registry-and-job-receipts.md`
43. `TS-CMF-043-deterministic-remotion-and-motion-canvas-rendering.md`
44. `TS-CMF-044-generative-provider-adapters.md`
45. `TS-CMF-045-self-hosted-comfyui-docker-gpu-worker.md`
46. `TS-CMF-046-comfyui-template-migration-to-worker-assets.md`
47. `TS-CMF-047-audio-caption-timeline-and-mix-assembly.md`
48. `TS-CMF-048-provider-job-retry-resume-cancel-and-compensation.md`
49. `TS-CMF-049-svre-aurore-and-asset-research-engine-routing.md`
50. `TS-CMF-050-evaluation-receipt-generation.md`
51. `TS-CMF-051-evidence-rich-review-surface.md`
52. `TS-CMF-052-review-commands-and-voice-dna-boost-requests.md`
53. `TS-CMF-053-approval-blockers.md`
54. `TS-CMF-054-publishing-intent-and-publer-adapter.md`
55. `TS-CMF-055-telegram-quick-review-with-evidence.md`
56. `TS-CMF-056-evidence-backed-memory-admission.md`
57. `TS-CMF-057-memory-review-correction-expiry-and-quarantine.md`
58. `TS-CMF-058-neo4j-relationship-projection.md`
59. `TS-CMF-059-operations-board.md`
60. `TS-CMF-060-workflow-recovery-actions.md`
61. `TS-CMF-061-operational-readiness-checks.md`
62. `TS-CMF-062-persona-code-registry-and-validation.md`
63. `TS-CMF-063-agentrolespec-and-departmentspec-runtime.md`
64. `TS-CMF-064-subagentrolespec-and-delegation-boundaries.md`
65. `TS-CMF-065-hookspec-and-extensionspec-lifecycle-contracts.md`
66. `TS-CMF-066-skillbinding-and-jit-skill-mode-binding.md`
67. `TS-CMF-067-agent-readiness-evals.md`
68. `TS-CMF-068-pi-harness-tool-registry.md`
69. `TS-CMF-069-adk-agents-cli-adapter-export-and-drift-gate.md`
70. `TS-CMF-070-ui-architecture-and-operator-experience.md`
71. `TS-CMF-071-reaction-editing-template-routing.md`
72. `TS-CMF-072-scene-template-runtime-binding-for-reaction-clips.md`
73. `TS-CMF-073-canonical-composition-json-registry-and-preview-approval.md`
74. `TS-CMF-074-reaction-clip-renderer-and-background-removal-compositing.md`
75. `TS-CMF-075-operator-composition-and-template-approval-workbench.md`
76. `TS-CMF-076-open-source-integration-adapter-evaluation-and-import-plan.md`
77. `TS-CMF-077-doctrine-driven-test-harness-and-primitive-eval-coverage.md`
78. `TS-CMF-078-four-video-format-runtime-and-doctrine-crosswalk.md`
79. `TS-CMF-079-route-specific-visual-feel-and-primitive-composition-gates.md`
80. `TS-CMF-080-composition-template-runtime-transcript-timing-and-brand-genesis-binding.md`
81. `TS-CMF-081-composition-template-family-registry-and-content-asset-codes.md`
82. `TS-CMF-082-brand-genesis-substrate-resolver-for-composition-runtime.md`
83. `TS-CMF-083-expression-lineage-and-interview-asset-contract-binding.md`
84. `TS-CMF-084-transcript-beat-map-and-timeline-cue-compiler.md`
85. `TS-CMF-085-64-state-acting-and-avatar-performance-selector.md`
86. `TS-CMF-086-papercut-rig-layer-motion-and-sfx-runtime.md`
87. `TS-CMF-087-micro-semiotic-anchor-selection-and-risk-gate.md`
88. `TS-CMF-088-ideogram-4-composition-director-to-production-template-bridge.md`
89. `TS-CMF-089-generative-asset-factory-layer-extraction-and-repair-queue.md`
90. `TS-CMF-090-renderer-prop-compiler-and-component-harness.md`
91. `TS-CMF-091-open-source-adapter-template-conversion-and-sandboxing.md`
92. `TS-CMF-092-composition-eval-fixtures-and-operator-approval-workbench.md`
93. `TS-CMF-093-animation-studio-migration-and-operator-rig-editor.md`
94. `TS-CMF-094-headless-2d-frame-renderer-and-avatar-export-worker.md`
95. `TS-CMF-095-geometrics-still-visual-composition-runtime-skia-sam3-pretext.md`
96. `TS-CMF-096-carousel-slide-composition-library-and-sequence-builder.md`
97. `TS-CMF-097-carousel-builder-engine-compiler-workflow-and-skia-export-runtime.md`
98. `TS-CMF-098-carousel-composition-atlas-registry-and-router-integration.md`
99. `TS-CMF-099-single-image-post-engine-supervisual-router-and-skia-runtime.md`
100. `TS-CMF-100-single-image-contracts-registry-loader-and-schema-parity.md`
101. `TS-CMF-101-single-image-router-format-family-and-archetype-selection.md`
102. `TS-CMF-102-supervisual-composition-families-and-primitive-triad-contracts.md`
103. `TS-CMF-103-single-image-provider-job-planner-and-layer-materialization.md`
104. `TS-CMF-104-single-image-skia-scene-compiler-and-render-binding.md`
105. `TS-CMF-105-single-image-eval-review-and-golden-fixture-runtime.md`
106. `TS-CMF-106-video-edit-program-compiler-otio-and-render-runtime.md`
110. `TS-CMF-110-two-d-character-engine-object-model-and-character-genesis.md`
111. `TS-CMF-111-two-d-character-provider-adapters-rig-authoring-and-asset-promotion.md`
112. `TS-CMF-112-two-d-character-scene-program-and-performance-compiler.md`
113. `TS-CMF-113-two-d-character-render-runtime-evals-approval-and-repair.md`
114. `TS-CMF-114-conscious-sequencing-contract-kernel-and-registries.md`
115. `TS-CMF-115-interview-brief-v2-sequence-hypothesis-and-expression-acquisition-plan.md`
116. `TS-CMF-116-live-ingredient-coverage-tracker-and-cue-suppression-policy.md`
117. `TS-CMF-117-expression-ingredient-inventory-and-relation-graph.md`
118. `TS-CMF-118-content-sequence-program-compiler-and-composition-handoff.md`
119. `TS-CMF-119-sequence-eval-gates-learning-and-package-sequencing.md`
120. `TS-CMF-120-openmontage-reference-adapter-governance.md`
121. `TS-CMF-121-production-pipeline-manifest-registry.md`
122. `TS-CMF-122-stage-director-skill-contract-binding.md`
123. `TS-CMF-123-capability-tool-registry-and-provider-menu.md`
124. `TS-CMF-124-scored-provider-selector-and-capability-router.md`
125. `TS-CMF-125-brand-scoped-project-workspace-and-checkpoint-runtime.md`
126. `TS-CMF-126-reference-video-and-existing-footage-intake-adapter.md`
127. `TS-CMF-127-real-footage-corpus-and-source-media-retrieval-adapter.md`
128. `TS-CMF-128-render-runtime-selection-and-locking.md`
129. `TS-CMF-129-pre-compose-delivery-promise-and-slideshow-risk-gate.md`
130. `TS-CMF-130-post-render-self-review-and-media-qa-gate.md`
131. `TS-CMF-131-budget-cost-and-resource-governance.md`
132. `TS-CMF-132-canonical-stage-artifacts-human-approval-and-reviewer-protocol.md`
133. `TS-CMF-133-still-visual-composition-program-manifest-and-stage-orchestration.md`
134. `TS-CMF-134-supervisual-visual-grammar-atlas-router-and-primitive-feel-matrix.md`
135. `TS-CMF-135-still-visual-runtime-api-review-read-model-and-approval-workbench.md`
136. `TS-CMF-136-operator-web-api-client-and-generated-contract-binding.md`
137. `TS-CMF-137-production-fastapi-composition-root-and-command-handler-wiring.md`
138. `TS-CMF-138-pi-harness-agent-command-routing-and-delegation-runtime.md`
139. `TS-CMF-139-operator-command-console-and-chat-to-command-proposal-runtime.md`
140. `TS-CMF-140-revision-update-and-repair-workflow-runtime.md`
141. `TS-CMF-141-telegram-bot-mini-app-and-pwa-handoff-integration.md`
142. `TS-CMF-142-live-operations-event-stream-and-read-model-sync.md`
143. `TS-CMF-143-operator-auth-scope-permission-and-contract-version-gates.md`
144. `TS-CMF-144-video-timeline-workbench-inside-operator-web.md`
145. `TS-CMF-145-supervisual-studio-operator-build-and-agentic-editing.md`

These foundation specs should be implemented before feature-specific specs because they define the command, orchestration, and spec-governance contracts used by the remaining stories.

Note: Story 3.5 is intentionally covered earlier by `TS-CMF-003-python-dspy-pi-bmad-spec-workflow.md` because the spec-governance workflow is a foundation dependency for all later specs.

Note: Story 11.1 through Story 11.8 extend the foundation with Agent Factory runtime contracts. TS-CMF-062 through TS-CMF-069 should be implemented before building production agent teams or generated ADK/Agents CLI adapters.

Note: `TS-CMF-070-ui-architecture-and-operator-experience.md` defines the operator-facing PWA, Telegram, generated-contract, command, receipt, guest workspace, content asset code, review, eval, Agent Factory, and operations UI architecture that should be used before implementing frontend surfaces.

Note: `TS-CMF-071-reaction-editing-template-routing.md` repairs the missing bridge between Conscious Reactions mechanics and live-filmed CMF production. It should be implemented before building Remotion/Motion Canvas templates for versus, tier list, ranking, elimination, mirror quiz, or authority quiz videos.

Note: `TS-CMF-072-scene-template-runtime-binding-for-reaction-clips.md` repairs the next dependency gap: reaction templates must bind to the migrated CMF scene-builder runtime asset before any production composition JSON or renderer template is approved.

Note: `TS-CMF-073-canonical-composition-json-registry-and-preview-approval.md` makes composition JSON the canonical source of truth. Preview PNGs, video previews, and renderer props are generated artifacts and cannot replace approved JSON.

Note: `TS-CMF-074-reaction-clip-renderer-and-background-removal-compositing.md` defines the actual video-editing/rendering build for stacked reaction clips: reaction UI above, upper-body interviewer/guest or guest-only subject cutouts below, beat-synced to the interview.

Note: `TS-CMF-075-operator-composition-and-template-approval-workbench.md` narrows the broad UI architecture into the immediate production workbench needed to review scene-template binding, composition JSON, previews, eval blockers, and approval receipts.

Note: `TS-CMF-076-open-source-integration-adapter-evaluation-and-import-plan.md` requires every open-source-inspired integration to pass license, architecture, security, reproducibility, guest-scope, doctrine, and primitive-fit evaluation before production import or adapter execution.

Note: `TS-CMF-077-doctrine-driven-test-harness-and-primitive-eval-coverage.md` makes testing doctrine-driven instead of random. It requires specs, contracts, workflows, UI, renderers, adapters, and approval paths to declare doctrine/primitive/eval obligations, negative fixtures, receipts, and approval blockers where relevant. Composition-bearing objects must load `registries/evals/composition/cmf_composition_primitive_triads.v1.json` and pass at least three registered primitives across meaning, delivery, and format/material roles.

Note: `TS-CMF-078-four-video-format-runtime-and-doctrine-crosswalk.md` canonically binds the Guest Asset Pack four short-video slots (`SV-CSC`, `SV-EDU`, `SV-FRB`, `SV-RRC`) to the nine CMF doctrines, source-backed routing, composition lineage, renderer dependencies, evaluation receipts, and Operator approval blockers. It should guide implementation before treating any of the four video categories as production-complete.

Note: `TS-CMF-079-route-specific-visual-feel-and-primitive-composition-gates.md` repairs the visual-previsualization failure mode where all formats collapse into the same generic premium social aesthetic. It requires every composition preview, prompt, JSON template, and renderer route to pass a route-specific `VisualFeelContract`, primitive obligations, and `CompositionPreflightReceipt` before preview generation or approval, with route triads enforced by `registries/evals/composition/cmf_composition_primitive_triads.v1.json`.

Note: `TS-CMF-080-composition-template-runtime-transcript-timing-and-brand-genesis-binding.md` repairs the source-trace gap between Brand Genesis V3, CCP V9/V9.1, open-source adapter planning, and executable composition templates. It requires every production composition to bind locked Brand Context substrate, 64-state acting or Paper-Cut rig assets, micro-semiotic anchors, Interview Asset Contract lineage, Expression Moment timestamps, transcript-to-frame beat maps, primitive triads, renderer props, eval receipts, and open-source adapter decision receipts before rendering or approval.

Note: `TS-CMF-081` through `TS-CMF-095` decompose TS-CMF-080 into buildable modules. They cover template family/code registry, Brand Genesis substrate resolution, expression lineage binding, transcript beat maps, acting/avatar performance selection, Paper-Cut rigged runtime, micro-semiotic anchor risk gates, Ideogram-to-production bridging, generative asset/layer extraction, renderer prop compilation, open-source adapter conversion, composition eval/operator approval, Animation Studio operator rig editing, headless 2D frame rendering, and the Skia/SAM3/PRETEXT Geometrics runtime for still visual content. These specs exist because TS-CMF-080 is a spine, not enough by itself to make the composition runtime functional at CMF standards.

Note: `TS-CMF-095-geometrics-still-visual-composition-runtime-skia-sam3-pretext.md` repairs the legacy CVE gap for carousels, visual polls, tweet-like quotes, memes, Super Visuals, and reaction stills. It preserves the old Ideogram 4 -> Qwen-Image-Layered -> SAM3 -> PRETEXT -> Geometrics -> Skia path, blocks browser-screenshot production fallbacks, and requires primitive triads before render.

Note: `TS-CMF-096-carousel-slide-composition-library-and-sequence-builder.md` adds the missing queryable carousel slide-atom layer. `CAR-LST` and `CAR-JUX` are no longer only broad format codes; they now resolve into slide atoms with composition meaning, primitive triads, sequence positions, visual grammar, and Geometrics handoff requirements.

Note: `TS-CMF-097-carousel-builder-engine-compiler-workflow-and-skia-export-runtime.md` binds the fragmented carousel specs into one executable compiler workflow. It owns `CreateCarouselRequest`, `CarouselSpec`, provider routing, Ideogram/Qwen/SAM3 materialization, rough annotation cue manifests, Geometrics/Skia handoff, export manifests, PWA/Telegram review evidence, and the final `CarouselBuilderReceipt`.

Note: `TS-CMF-098-carousel-composition-atlas-registry-and-router-integration.md` integrates the CCP Carousel Composition Atlas as the visual grammar layer between `CarouselSequencePlan` and `GeometricsLayoutPlan`. It keeps the 12 slide atoms as meaning-level contracts while adding 44 canonical visual composition specs, 12 sequence grammars, normalized zones, text budgets, tool routing policies, corpus evidence, and a scoring-based `CompositionRouterDecision`.

Note: `TS-CMF-099-single-image-post-engine-supervisual-router-and-skia-runtime.md` integrates the CCP Single Image Post Engine V2 as the single-frame and SuperVisual sibling to the carousel builder. It promotes the 28 canonical single-image composition contracts, router policy, provider responsibility policy, Ideogram prompt contracts, Skia component catalog, source evidence, and eval rubrics into canonical registries, and makes `SPV-CON`, `SPV-SYM`, `SPV-PRM`, visual polls, tweet-like quotes, memes, documentary social cards, promo cards, and reaction stills route through a deterministic Skia final render path instead of loose image prompting.

Note: `TS-CMF-100` through `TS-CMF-105` decompose the Single Image and SuperVisual umbrella into buildable modules: contracts/registry loader, output-family-aware router, SuperVisual primitive and visual-feel contracts, provider job planning, Skia scene compilation, and eval/review/golden fixtures. The Single Image or SuperVisual runtime is not implementation-complete until these child specs pass.

Note: `TS-CMF-106-video-edit-program-compiler-otio-and-render-runtime.md` creates the missing parent video editing compiler identified by `docs/audits/CMF_VIDEO_EDITING_ENGINE_MCDA_2026-06-24.md`. It defines `VideoEditProgram` as the canonical source of truth above `SceneSpec`, reaction routes, PaperCut and 2D character subscenes, provider jobs, transcript clocks, caption/audio plans, deterministic render contracts, OTIO audit manifests, eval gates, approval blockers, and final render receipts. `TS-CMF-110` through `TS-CMF-113` transform the CCP 2D Character Animation Engine V1 bundle into canonical CMF/ERA3 specs and feed character scenes into the broader video edit program. `TS-CMF-107` through `TS-CMF-109` remain intentionally unused in the current ledger.

Note: `TS-CMF-114` through `TS-CMF-119` transform the CCP Conscious Sequencing and Expression Acquisition Engine V1 bundle into canonical CMF/ERA3 specs. They add the missing procurement and sequencing brain between interview intelligence and composition: normalized sequencing registries, Interview Brief V2 procurement, live ingredient coverage, source-grounded expression inventory, `ContentSequenceProgram` compilation, composition handoff, sequence eval gates, package sequencing, and receipt-backed learning. These specs preserve the bundle's core law that final content may only use captured, approved, sourced, retrieved, pickup-requested, or non-human contextual ingredients; the compiler may not fabricate missing human truth to complete a content recipe.

Note: `TS-CMF-120` through `TS-CMF-132` adapt the OpenMontage architectural reference into CMF-native orchestration specs: reference governance, production manifests, stage director skill binding, tool and provider registries, scored provider selection, brand-scoped workspaces, reference media intake, real footage retrieval, render runtime locks, pre-compose QA, post-render QA, budget governance, and canonical stage artifact review. They provide the general production orchestration pattern that later video and still visual builders should reuse.

Note: `TS-CMF-133` through `TS-CMF-135` apply the same stage-manifest, provider-boundary, primitive-eval, deterministic-render, and human-approval architecture to still visual composition. They add a parent `StillVisualCompositionProgram` for carousels, SuperVisuals, visual polls, tweet-like quotes, memes, and reaction stills; a SuperVisual grammar atlas and primitive feel matrix; and a program-centered API/review workbench so still visuals can be routed, rendered, evaluated, revised, approved, and exported without collapsing into generic image prompting.

Note: `TS-CMF-136` through `TS-CMF-143` close the gap between the built React operator web app and a real CMF factory runtime. They bind the frontend to generated backend contracts, create a production FastAPI composition root, route Pi/Agent Factory actions through authority-checked command proposals, add a governed chat command console, make revisions first-class repair workflows, complete Telegram Bot/Mini App/PWA handoff, stream live receipt-linked operations events, and enforce auth, scope, permission, consent, and contract-version gates across PWA, Telegram, Pi, and Command Bus entry points.

Note: `TS-CMF-144-video-timeline-workbench-inside-operator-web.md` adds the missing dedicated Video Timeline Workbench to the React operator app. It requires a frame-accurate, transcript-bound, receipt-backed UI over `VideoEditProgram`, `CompositionBeatMap`, timeline cues, captions, audio, subject cutouts, reaction UI, PaperCut/2D character lanes, proxy renders, eval blockers, repair commands, and OTIO status. The browser remains an operator surface only: edits become drafts, drafts become commands, and accepted state is proven by receipts.

Note: `TS-CMF-145-supervisual-studio-operator-build-and-agentic-editing.md` adds the missing product component for SuperVisual creation and editing inside operator-web. It binds Interview Brief plus transcript or transcript-only context, Content Planning Agents Team, JIT Skill Compiler, SuperVisual routing, editable copy/family/composition/layer/prompt/asset/text/primitive/export state, agent quick-edit command proposals, primitive blockers, approval, download, export, and scheduling handoff into one receipt-backed workbench.
