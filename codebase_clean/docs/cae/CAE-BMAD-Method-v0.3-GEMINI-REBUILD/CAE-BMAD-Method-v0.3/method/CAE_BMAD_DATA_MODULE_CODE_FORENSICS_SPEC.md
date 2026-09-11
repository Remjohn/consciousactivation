# CAE-BMAD Data, Module, and Code Forensics Specification

**Version:** 0.3.0-rebuild  
**Status:** CANONICAL SPECIFICATION  
**Authority:** CAE Rebuild Program / Operator Mandate M08  
**Scope:** Deep forensics standards, entity relationship auditing, package namespace verification, AST class/method inspection, and line-level proof extraction across Operating Levels 09, 10, 11, 12, and 13.

---

## 1. Operating Levels 09 through 13 in the CAE Hierarchy

```text
Level 09: DATABASE / TABLE        [Entity models, canonical state schemas, storage engines]
         ↕
Level 10: MODULE / DIRECTORY      [Package namespaces, import graphs, internal cohesion]
         ↕
Level 11: FILE / TYPE / CLASS     [AST class models, pydantic/dataclass types, fields]
         ↕
Level 12: FUNCTION                [Signatures, handlers, coroutines, return types]
         ↕
Level 13: LINE / BLOCK            [Exact statement proof, verifiers, exception blocks]
```

---

## 2. Responsibilities by Operating Level

### 2.1 Level 09: DATABASE / TABLE (`cae-data-analyst`)
- Audits entity models across `services/world-intelligence`, `services/pipeline`, and `packages/ca_runtime`.
- Verifies alignment with canonical state aggregate constitutions (`docs/cae/constitutions/CA-CAN-02_STATE_AGGREGATE.yaml`).
- Enforces storage engine classification (`IN_MEMORY_CAS`, `FILESYSTEM_YAML`, `SQLITE`, `POSTGRES`, `REDIS`).

### 2.2 Level 10: MODULE / DIRECTORY (`cae-module-analyst`)
- Maps internal Python module hierarchies across `packages/ca_runtime` and `services/*/src/`.
- Verifies public API symbols in `__init__.py` files and audits circular dependencies.
- Enforces strict encapsulation boundaries between microservices.

### 2.3 Levels 11–13: FILE / CLASS / FUNCTION / LINE (`cae-code-forensics-analyst`)
- Performs static AST and line-by-line inspection of Python implementation files.
- Extracts exact code citations (file path + line number range + verbatim code snippet).
- Executes unit and integration test verifications (`pytest`) to validate functional reality.

---

## 3. The Ground Truth Standard

1. **No Assertion Without Lineage:** An agent cannot claim a function handles an edge case without citing the exact line numbers and condition blocks.
2. **Verbatim Snippet Requirement:** Every line proof in `CODE_FORENSICS_REPORT.json` must contain the exact code snippet from disk.
3. **AST Symbol Validation:** Classes and functions listed must match the Python AST parsed directly from the target file.
