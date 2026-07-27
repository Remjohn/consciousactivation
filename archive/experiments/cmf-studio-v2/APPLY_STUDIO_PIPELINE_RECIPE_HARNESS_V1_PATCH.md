# CCP Studio Pipeline Recipe Harness V1 Integration Bundle

Purpose: generalize the Format 02 Golden Path into reusable studio recipes while reusing the existing orchestration spine.

Recipes:
- format02_golden_path
- avatar_library_generation
- supervisual_from_expression_moment
- carousel_from_expression_moment
- format01_story_video

Critical boundary: this is a recipe/read-model/control layer over the existing orchestration spine. It must not create a parallel workflow engine. If `src/ccp_studio/contracts/orchestration.py` exists, map recipe steps to existing OrchestrationRun / StageExecutionPlan / ValidationContract / StageExecutionReceipt concepts through the adapter service.

Do not call providers, renderers, local workers, or background jobs. Do not replace orchestration.py.
