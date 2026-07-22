---
title: "TS-CMF-091 Build Receipt"
status: "implemented"
implemented_at: "2026-06-25"
batch: "Batch 1"
spec: "THE CMF STUDIO/docs/tech-specs/TS-CMF-091-open-source-adapter-template-conversion-and-sandboxing.md"
---

# TS-CMF-091 Build Receipt

Implemented sandboxed open-source template conversion through `OpenSourceTemplateConversion` and `convert_open_source_template`. Conversions always produce CMF-owned adapter refs and keep `direct_import_allowed` false.

Verification: `test_batch1_open_source_adapters_eval_conversion_and_operator_approval_are_sandboxed`.

