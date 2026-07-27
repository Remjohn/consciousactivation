# Lane E — Existing Interview Expression Product and Story Campaign

## Governing correction

The Interview Expression product already exists.

The integrator must locate and use its live local product root. This lane must not
create another Interview repository, another Interview product identity, or a GNM
subsystem.

## Exclusive target paths

The integrator assigns the existing Interview Expression product paths before source
writes. The lane may also migrate approved predecessor material from
`THE_CMF_STUDIO(2).zip`.

Migration candidates:

```text
05_PRD_CMF_STUDIO_INTERVIEW_FIRST.md
CCP V9  Interview-First Expression Engine.md
CCP V9.1 Expression Capture & Archetype Routing Update.md
CCP_CONSCIOUS_SEQUENCING_AND_EXPRESSION_ACQUISITION_ENGINE_V1_BUNDLE/**
docs/prd/modules/PRD_CMF_06_Interview_Expression_Routing.md
docs/stories/story-5-4-interviewer-pre-induction.md
docs/stories/story-5-5-interview-asset-contract-and-quality-gate.md
docs/tech-specs/TS-CMF-026-interviewer-pre-induction.md
docs/tech-specs/TS-CMF-027-interview-asset-contract-and-quality-gate.md
docs/tech-specs/TS-CMF-083-expression-lineage-and-interview-asset-contract-binding.md
docs/tech-specs/TS-CMF-115-interview-brief-v2-sequence-hypothesis-and-expression-acquisition-plan.md
src/ccp_studio/contracts/interview_contracts.py
src/ccp_studio/services/interview_contract_service.py
src/ccp_studio/services/interview_brief_binding_service.py
src/ccp_studio/workflows/interview_preparation.py
src/ccp_studio/dspy_programs/interview_contract_compiler.py
```

## Deliver

- Execute all existing READY Interview Stories in dependency order.
- Complete Expression Session.
- Guest dossier, Audience Reality, and Interviewer Resonance Context.
- Narrative-state map, Matrix of Edging brief, First-Line Anchors, and Depth Anchors.
- Interview Asset Contracts.
- Transcript and timestamped anchor hits.
- Expression Moments and Expression Ingredient Inventory.
- Asset Package Spec routing to edited video, Carousel, SuperVisual, meme, poll, quote,
  and other governed downstream jobs.
- Post-session learning and evaluation receipts.
- Local CLI or operator flow for one real interview session.

## GNM boundary

This product does not implement or depend on GNM.

An `ExpressionMoment` or `AssetPackageSpec` may later be included in a Pipeline-created
Visual Asset Demand. The Visual Asset Editor independently decides whether its approved
production plan uses GNM.

No GNM imports, coefficient generation, model loading, or ComfyUI workflows are permitted
inside this lane.
