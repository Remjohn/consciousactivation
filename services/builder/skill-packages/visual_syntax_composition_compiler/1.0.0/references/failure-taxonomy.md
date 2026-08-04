# Failure Taxonomy — Visual Syntax Composition Compiler

## Error Codes

| Error Code                    | Description                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| `UNSUPPORTED_CATEGORY`        | Input category_id is not `carousels` or `supervisuals`.                    |
| `NON_CANONICAL_PRIMITIVE`     | An observed primitive type does not exist in the canonical taxonomy.        |
| `EMPTY_WRONG_READING_LOCKS`   | Harness passed zero wrong-reading locks.                                    |
| `INVALID_SLIDE_SEQUENCE`      | Slide roles do not follow valid order (e.g. cover missing, closing missing).|
| `UNMAPPED_LOCK`               | A wrong-reading lock could not be translated to any spatial/semantic rule.  |
| `ANCHOR_DISCREPANCY`          | A cross-slide locked anchor has conflicting dimensions across slides.       |
| `INVALID_ATTRIBUTE_RANGE`     | Attribute range min exceeds max or falls outside canvas bounds.             |
