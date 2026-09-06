# CAE Mandate Bundle — Wave 02

**Bundle ID:** `CAE_MANDATE_BUNDLE_WAVE_02`  
**Scope:** Canonical Questions Q09–Q16  
**Status:** `EXECUTION READY — bounded mandate bundle`  
**Prepared:** `2026-09-06`

## 1. Authority chain

1. `docs/cae/cae_mandate_bundle/01_CA_MANDATE_AUTHORING_PROTOCOL.md`
2. Master 57-Question Decision & Convergence Canon
3. CAE Product Brief / PRDs / Functional Requirements
4. `docs/cae/UI.md`
5. `docs/cae/Architecture.md`
6. Wave 01 mandates and their recorded Operator decisions
7. Individual Wave 02 mandates
8. Repository implementation and executable evidence

The protocol is normative for mandate grammar, scope, evidence classes, collision procedure, activation prompts, parallelism, completion, and stop behavior. Runtime authority remains the canonical CAE runtime. Planning documents and mandate prose do not become runtime authority.

## 2. Wave 02 objective

Wave 02 turns the Q01–Q08 foundation into an evidence-grounded pre-production substrate:

```text
Wave 01 canonical inputs
        ↓
structured research
        ↓
revisioned preparation graph
        ↓
sealed pre-production snapshot
        ↓
sovereign source media
        ↓
temporally anchored evidence
        ↓
continuity-protected evidence
        ↓
verbatim evidence
        ↓
grounded Collision
```

The project readiness assessment explicitly defines Wave 02 as Q09–Q16 and identifies Q09 as primarily control-plane work, Q10–Q16 as primarily causal/data/runtime work, with Q11 acting as the mutable-to-immutable execution boundary.

## 3. Mandate map

| File | Mandate ID | Canon | Mandate | Primary surface | Dependency |
|---|---|---:|---|---|---|
| `01_CA_MANDATE_009.md` | `CA-M009` | Q09 | Interactive Parameter-Sensitive Preparation Graph | graph/UI/API/runtime | Q04, Q08 |
| `02_CA_MANDATE_010.md` | `CA-M010` | Q10 | Structured, Digest-Pinned Research Brief | research/program surfaces | Q01–Q02 |
| `03_CA_MANDATE_011.md` | `CA-M011` | Q11 | Cryptographically Sealed Pre-Production Snapshot | compiler/runtime/state | Q06–Q10 |
| `04_CA_MANDATE_012.md` | `CA-M012` | Q12 | Sovereign Source Media Byte Supremacy | media/evidence pipeline | Q11 |
| `05_CA_MANDATE_013.md` | `CA-M013` | Q13 | Temporal Evidence Anchoring | evidence domain | Q12 |
| `06_CA_MANDATE_014.md` | `CA-M014` | Q14 | Cross-Window Continuity and Chunking Protection | evidence ingestion | Q12–Q13 |
| `07_CA_MANDATE_015.md` | `CA-M015` | Q15 | Verbatim Spoken Capture Integrity | evidence/composer boundary | Q12–Q14 |
| `08_CA_MANDATE_016.md` | `CA-M016` | Q16 | Grounded Collision Tension Matrix | collision intelligence | Q01, Q02, Q07, Q08, Q15 |

## 4. Dependency and parallelism

```text
CA-M009 ───────┐
               ├──→ CA-M011 → CA-M012 → CA-M013 ──┐
CA-M010 ───────┘                                  ├→ CA-M015 → CA-M016
                                      CA-M014 ─────┘
```

CA-M009 and CA-M010 may be investigated or implemented in parallel only where their outputs are independently mergeable and they do not establish conflicting shared authority. CA-M011 is the integration owner for the mutable-to-immutable pre-production boundary. Q12–Q15 form a sequential evidence provenance chain because each establishes an input contract consumed by the next. CA-M016 closes the wave at grounded Collision admission.

Shared registries, shared state, migrations, receipts, and Operator decisions have one integration owner. Parallel read-only inspection is allowed; parallel conflicting writes are not.

## 5. Inherited Wave 01 evidence

Executors must verify, not assume, the relevant Wave 01 outputs:
- three-layer audience context;
- audience/guest convergence;
- Subject Constitution lifecycle;
- canonical causal ordering;
- format/archetype feasibility;
- Activative↔Elicitation linkage;
- Activative derivation lineage;
- frozen Content Portfolio contract.

A Wave 01 document saying “complete” is a `DOCUMENT` claim until executable evidence supports it.

## 6. Wave-level false-proof suite

Wave 02 should collectively reject:
1. mutation of an execution-bound preparation revision;
2. stale/forged pre-production snapshot admission;
3. research claims without required provenance;
4. source-media digest mismatch;
5. floating evidence without a source-resolvable anchor;
6. chunk-boundary corruption or unsupported reconstruction;
7. paraphrased “verbatim” quote;
8. single-pole Collision;
9. unfalsifiable or evidence-free Collision;
10. UI-only or score-only authority.

These are deliberate anti-centroid controls and must be treated as proof obligations.

## 7. Execution/control rule

Each mandate follows:

`LOAD AUTHORITY → VERIFY PRECONDITIONS → BUILD PLAN → EXECUTE WITHIN FILE BOUNDARY → VERIFY → RECORD EVIDENCE → UPDATE CONTROL STATE → COMMIT → REQUEST OPERATOR DECISION → STOP`

Every mandate contains a 200–300 word activation prompt. The activation prompt is an execution key, not an expansion of authority.

## 8. Completion

Wave 02 is complete only when all eight mandates independently pass their proof standards, limitations are recorded, control state is updated, exact commit SHAs are captured by the executors, and the Operator explicitly closes the wave.

Wave 02 does not authorize Q17–Q23. Those remain a separately governed bundle.

## 9. Naming note

The repository already contains an older/editorial mandate series using identifiers such as `M08`, `M09`, `M10`, `M11`, and `M12`. This Wave 02 intentionally uses `CA-M009` through `CA-M016` and `CA_MANDATE_009` through `CA_MANDATE_016` to avoid colliding semantically with those legacy/editorial documents. No existing legacy mandate is overwritten by this bundle.
