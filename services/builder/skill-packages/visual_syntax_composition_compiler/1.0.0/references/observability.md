# Observability — Visual Syntax Composition Compiler

## Telemetry & Audit Receipts

The compiler emits a `VisualSyntaxCompilerReceipt` containing:
- `spec_id`: Content hash of the compiled specification
- `harness_definition_id`: Input harness ID
- `category_id`: `carousels` or `supervisuals`
- `slide_count`: Number of slide roles compiled
- `primitive_count`: Total primitives instantiated across all zones
- `lock_translation_count`: Number of wrong-reading locks mapped to spatial rules
- `cross_slide_anchor_count`: Number of cross-slide locked anchors verified
- `deduplication_hash`: Content hash for spec sharing across identical harnesses
