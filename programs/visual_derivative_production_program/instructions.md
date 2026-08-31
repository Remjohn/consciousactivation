# Visual Derivative Production Program — Operational Instructions

## Lifecycle Stages
1. **Admission (`INITIAL` -> `DERIVATIVE_ADMITTED`)**:
   - Lane: `COMMANDER`
   - Validates workspace active status, program registration, and upstream `SemanticProgram` integrity.
2. **Source Extraction (`DERIVATIVE_ADMITTED` -> `SOURCES_EXTRACTED`)**:
   - Lane: `HUNTER`
   - Skill: `derivative_source_extractor`
   - Extracts verbatim quotes and timing spans from authentic evidence records. Computes quote SHA-256 hashes.
3. **Composition Compilation (`SOURCES_EXTRACTED` -> `COMPOSITIONS_COMPILED`)**:
   - Lane: `COMPOSER`
   - Skill: `derivative_composition_compiler`
   - Compiles layout, typography, element bounding boxes, negative space regions, and wrong-reading lock constraints into `CompositionIR`.
4. **Render Realization (`COMPOSITIONS_COMPILED` -> `RENDERS_REALIZED`)**:
   - Lane: `COMPOSER`
   - Realizes physical derivative files:
     - `CAROUSEL`: Generates slide PNGs and compiled PDF via `CarouselService`.
     - `SUPERVISUAL`: Generates high-impact image PNG via `SuperVisualService`.
     - `ANIMATION_SCENE_PACKAGE`: Renders discrete animation frames and encodes MP4 via `AnimationSceneRealizer`.
5. **Dual-Axis QA Evaluation (`RENDERS_REALIZED` -> `QA_EVALUATED`)**:
   - Lane: `ANALYST`
   - Skill: `derivative_qa_evaluator`
   - Evaluates Semantic QA (verbatim quote matches, wrong-reading locks) and Render QA (file validation, byte count > 0, frame integrity).
6. **Release Authorization (`QA_EVALUATED` -> `RELEASE_AUTHORIZED`)**:
   - Lane: `COMMANDER`
   - Verifies dual-axis QA pass and commits state with signed `DerivativeReleaseReceipt`.
