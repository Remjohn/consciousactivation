# Tech-Spec: FR-ERA3-06 â€” Primitive Registry Query Service
**Created:** 2026-05-11
**Status:** Ready for Development
**Version:** 1.1 (SDA Boundary Update) <!-- UPDATED: version bump for SDA boundary update -->
**Phase:** 1 â€” Infrastructure
**Architecture Reference:** ERA3_Tech_Spec_Writing_Protocol.md Â§7

---

## Pre-Work Log

```
1. PROTOCOL LOADED:   Â§2.4 PRD-08 row confirms "No query service yet â€” THIS IS WHAT FR-ERA3-06 BUILDS"
2. PRD LOADED:        PRD-08 Â§1: "Primitives are that languageâ€¦ stable transformation operators that can be activated, measured, combined, suppressed, and validated in context." Â§3.3 defines Experience Primitive Schema with `experience_primitive_id`, `canonical_name`, `conflicts_with`, `synergizes_with` fields. Brownfield Â§1.1 confirms Meaning/Experience Plane Separation needs to be built; Â§2 confirms FR-APR-08 Primitive Matrix Engine exists but no runtime query service.
3. EPIC LOADED:       Phase1 Epic2 Story 2.1 AC: "Given the FastAPI application starts or a primitive is updated in the database, When lifespan initialization occurs or a targeted invalidation event is received, Then the service caches or hot-reloads the specific YAML primitives into Redis, And serves all runtime queries from in-memory cache without disk I/O."
4. CBAR AUDIT LOADED: Phase1-M04 (The Hot-Reload Rule) and Phase1-M05 (The Deterministic Override Rule) confirmed. Hallucination Purge: EXP-TRB-004 does NOT exist â€” corrected to EXP-TRS-001.
5. PRIMITIVES LOADED:
   - EXP-FBK-001: "RIM Feedback Discipline" (feedback_scoring family)
   - EXP-TRG-002: "Hook Cycle Velocity" (trigger_timing family)
   - EXP-SAF-003: "Hypnosedation Reframing" (safe_failure_recovery family)
   - EXP-FRC-002: "System 1 to System 2 Escalation" (friction_ability family)
   - EXP-TRS-001: "Visceral Hooking (Premium Authority Aesthetic)" (trust_branding family)
<!-- UPDATED: Added SDA source reads to pre-work log -->
8. SDA SOURCES READ:  `semantic_discernment_architecture_content_engine_v_1.md`, `semantic_discernment_architecture_artifact_taxonomy_v_1.md`, `Perceptual_Primitives_Architecture.md`, `Matrix of Edging.md`
9. SDA SPECS READ:    `FR-ERA3-21_SDA_Query_And_Crosswalk_Service_Tech_Spec.md`
6. BACKEND FILES READ:
   - src/ccp/api/telegram_webhook.py â€” `async def telegram_webhook(request: Request)`; uses in-memory dedup set with `_is_duplicate(chat_id, message_id)` (Redis pattern reference)
   - src/ccp/api/main.py â€” `app.include_router(router, prefix="/api", tags=[...])` pattern for route registration
   - src/ccp/services/dpa_engine.py â€” `async def resolve(self, coach_id, content_archetype, ...)` â†’ `DPAResult`
   - src/ccp/services/cpr_query_service.py â€” `class CPRQueryService` with `def query_registry(self, moment_id, regulatory_frame, selection_rationale, ...) -> CPRQueryResult`
   - src/ccp/core/circuit_breaker.py â€” `class CircuitBreaker` with `scan_for_crisis(self, text) -> bool` and `async def activate(self, client_telegram_id, trigger_message)`
7. TEST PATTERN:      test_ca11_fr19_trivianar_engine.py + test_ca11_fr15_dpa_engine.py â€” Pattern: `_run()` helper for async (no pytest-asyncio), class-per-AC grouping (e.g., `class TestQuestionDelivery`), fixture helpers (`_make_question(**overrides)`), constants imported from models, SQL schema string assertions.
```

---

## 1. Files Read

| # | File | Date/Version | Purpose |
|---|------|-------------|---------|
| 1 | `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md` | 2026-05-08 | Master protocol, backend architecture reference |
| 2 | `reference/conscious-rivers/docs/prd/modules/PRD_08_Conscious_Primitives.md` | v6.0, 2026-05-06 | Source PRD â€” registry schema, coalition theory, orchestration contracts |
| 3 | `docs/architecture/april_updates/Phase1_Infrastructure_Epics.md` | 2026-05-08, CBAR 2026-05-10 | Epic 2 stories + 7 CBAR mandates |
| 4 | `docs/architecture/cbar_audits/CBAR_Audit_Phase1_Infrastructure.md` | 2026-05-10 | Adversarial audit â€” M04/M05 verdicts, hallucination purge |
| 5 | `primitives/experience/feedback_scoring/EXP-FBK-001.yaml` | â€” | RIM Feedback Discipline â€” `conflicts_with: [EXP-FBK-004]` |
| 6 | `primitives/experience/trigger_timing/EXP-TRG-002.yaml` | â€” | Hook Cycle Velocity â€” `conflicts_with: [EXP-TRG-007]` |
| 7 | `primitives/experience/safe_failure_recovery/EXP-SAF-003.yaml` | â€” | Hypnosedation Reframing â€” `conflicts_with: [EXP-SOC-002]` |
| 8 | `src/ccp/api/telegram_webhook.py` | â€” | Redis dedup pattern, FastAPI router pattern |
| 9 | `src/ccp/api/main.py` | â€” | Route registration via `app.include_router()` |
| 10 | `src/ccp/services/dpa_engine.py` | â€” | DPAEngine.resolve() â€” existing service pattern |
| 11 | `src/ccp/services/cpr_query_service.py` | â€” | CPRQueryService â€” existing query service pattern with receipt chain |
| 12 | `src/ccp/core/circuit_breaker.py` | â€” | CircuitBreaker â€” fallback/degradation pattern |
| 13 | `tests/integration/test_ca11_fr19_trivianar_engine.py` | â€” | Pytest integration test pattern |
| 14 | `tests/integration/test_ca11_fr15_dpa_engine.py` | â€” | DPA engine test pattern with `_run()` async helper |
<!-- UPDATED: Added SDA sources to Files Read -->
| 15 | `lab/semantic_discernment_architecture_content_engine_v_1.md` | â€” | Deep SDA doctrine |
| 16 | `lab/semantic_discernment_architecture_artifact_taxonomy_v_1.md` | â€” | SDA taxonomy and crosswalk definitions |
| 17 | `docs/architecture/april_updates/FR-ERA3-21_SDA_Query_And_Crosswalk_Service_Tech_Spec.md` | â€” | Sibling SDA query service defining the crosswalk seam |

---

## 2. Overview

### 2.1 Problem Statement â€” What breaks without this spec?

Without the Primitive Registry Query Service, every downstream system that needs primitive rules (orchestration engine, scoring pipelines, content factories, experience Mini Apps) must independently parse 243+ YAML files from disk at runtime. This creates:
- **Latency violations:** Disk I/O during user sessions breaks the 3-second RIM feedback SLA (`EXP-FBK-001`).
- **Stale rules:** No cache invalidation mechanism means updated primitives are never reflected until full application restart.
- **Contradictory payloads:** No conflict resolution means the orchestration engine can request two mutually exclusive primitives (e.g., `EXP-SAF-003` + `EXP-SOC-002`) and receive both, producing schizophrenic generation prompts.
- **No query layer:** PRD-08 Â§2.4 explicitly states "No query service yet."

### 2.2 Solution

This spec builds a new FastAPI service (`PrimitiveRegistryQueryService`) that loads all 243+ YAML primitives into a Redis-backed in-memory cache on application startup via the FastAPI `lifespan` context manager, serves sub-millisecond queries by primitive ID, family, plane, or tag, implements targeted Redis key invalidation for hot-reload on primitive updates, and provides a `Conflict_Resolver` middleware that parses `conflicts_with` fields and applies a deterministic precedence hierarchy before returning any multi-primitive payload. The service exposes REST endpoints under `/api/primitives/` and is consumed by the orchestration engine and all downstream generation systems.

<!-- UPDATED: Added SDA boundary clarification to solution -->
Crucially, this service exclusively manages **primitives as transformation operators**, leaving deep semantic ontology and crosswalk resolution to its sibling infrastructure, the SDA Query and Crosswalk Service (FR-ERA3-21).

### 2.3 Scope

**In scope:**
- YAML parsing engine for `primitives/experience/**/*.yaml` (51 files, 8 families) and `primitives/meaning/**/*.yaml` (192+ files, 10 families)
- Redis-backed in-memory cache with targeted key invalidation
- FastAPI REST endpoints for primitive queries (by ID, family, plane, tags)
- `Conflict_Resolver` middleware for `conflicts_with` field resolution
- Pydantic v2 response models extending `src/ccp/models/`
- Receipt chain logging for all query operations
- Hot-reload endpoint for CI/CD-triggered cache invalidation

**Out of scope:**
- Coalition formation logic (PRD-08 Â§5 â€” future spec)
- Primitive codification/authoring UI
- Meaning primitive candidate generation or scoring
- Vector embedding or similarity search of primitives
- Cross-coach primitive customization
- Experience primitive telemetry event tracking
<!-- UPDATED: Added explicit SDA exclusions to out of scope -->
- SDA ontology parsing or canonical grammar resolution
- Crosswalk-mediated lookups mapping primitives to Existential Invariants (owned by FR-ERA3-21)

---

## 3. Context for Development

### 3.1 Architecture Traceability

| DEP-ID | Component | Source FR | What It Does |
|--------|-----------|-----------|-------------|
| DEP-REG-001 | `PrimitiveRegistryQueryService` | FR-ERA3-06 | Main service class â€” loads, caches, queries, resolves primitives |
| DEP-REG-002 | `YAMLRegistryLoader` | FR-ERA3-06 | Parses all YAML files from `primitives/` into typed Pydantic models |
| DEP-REG-003 | `ConflictResolver` | FR-ERA3-06 | Middleware that filters mutually exclusive primitives from query results |
| DEP-REG-004 | `RegistryCacheManager` | FR-ERA3-06 | Redis cache layer with targeted key invalidation |
| DEP-REG-005 | `PrimitiveRegistryRouter` | FR-ERA3-06 | FastAPI router exposing `/api/primitives/*` endpoints |

### 3.2 Existing Backend Integration

| File | Path | How This Spec Uses It |
|------|------|-----------------------|
| `telegram_webhook.py` | `src/ccp/api/telegram_webhook.py` | **Redis dedup pattern reference** â€” uses `_is_duplicate()` with in-memory set + Redis TTL. This spec follows the same Redis connection pattern but uses structured key namespaces (`prim:exp:{id}`, `prim:mng:{id}`). |
| `main.py` | `src/ccp/api/main.py` | **Route registration** â€” new router registered via `app.include_router(primitive_router, prefix="/api", tags=["Primitives"])`. |
| `dpa_engine.py` | `src/ccp/services/dpa_engine.py` | **Consumer** â€” `DPAEngine.resolve()` will query this service for experience primitives governing visual branding constraints. Method signature: `async def resolve(self, coach_id: str, content_archetype: str, ...) -> DPAResult`. |
| `cpr_query_service.py` | `src/ccp/services/cpr_query_service.py` | **Architectural pattern** â€” `CPRQueryService.__init__()` loads registry on init, uses receipt chain logging. This spec follows the same staged-init + receipt pattern. Method: `def query_registry(self, moment_id, regulatory_frame, selection_rationale, ...) -> CPRQueryResult`. |
| `circuit_breaker.py` | `src/ccp/core/circuit_breaker.py` | **Fallback pattern** â€” `CircuitBreaker.scan_for_crisis()` returns `bool`. This spec's backward compatibility fallback uses a similar fail-closed pattern when Redis is unavailable. |
| `receipt_chain.py` | `src/ccp/core/receipt_chain.py` | **Audit trail** â€” `ReceiptChain.log(agent_id, action, input_summary, output_summary, metadata)` used for all query operations. |
<!-- UPDATED: Added FR-ERA3-21 interop reference -->
| `FR-ERA3-21` | `docs/architecture/april_updates/FR-ERA3-21_SDA_Query_And_Crosswalk_Service_Tech_Spec.md` | **Sibling Service** â€” Acts as a consumer of this service's primitive verification capabilities during its own primitive-to-invariant crosswalk resolutions. |

### 3.3 ADR-05 Primitives

| Primitive ID | Name | Family | Constraint Applied |
|-------------|------|--------|-------------------|
| `EXP-FBK-001` | RIM Feedback Discipline | feedback_scoring | All cache queries must resolve in <3ms to protect the 3-second feedback SLA. `conflicts_with: [EXP-FBK-004]` â€” the `Conflict_Resolver` must parse this field and strip `EXP-FBK-004` when both are requested. |
| `EXP-TRG-002` | Hook Cycle Velocity | trigger_timing | Rapid hook cycle completion requires sub-millisecond primitive resolution. `conflicts_with: [EXP-TRG-007]` â€” resolver must handle this pair. |
| `EXP-SAF-003` | Hypnosedation Reframing | safe_failure_recovery | `conflicts_with: [EXP-SOC-002]` â€” the CBAR audit (Story 2.2) uses this exact pair as the failure example for contradictory payloads. |
| `EXP-FRC-002` | System 1 to System 2 Escalation | friction_ability | `conflicts_with: ["None"]` â€” foundational sequencing law, no conflicts. Validates that the resolver correctly handles empty/none conflict fields. |
| `EXP-TRS-001` | Visceral Hooking (Premium Authority Aesthetic) | trust_branding | `conflicts_with: [EXP-TRG-003]` â€” resolver must enforce. Corrected from hallucinated `EXP-TRB-004` per CBAR audit. |

### 3.4 CBAR Mandate Enforcement

| Mandate | Phase-M# | Story Origin | Implementation Mechanism |
|---------|----------|-------------|------------------------|
| **The Hot-Reload Rule** | Phase1-M04 | Story 2.1 (Registry Parsing & Caching) | The `RegistryCacheManager` implements targeted Redis key invalidation via `invalidate_primitive(primitive_id)`. When a YAML file is updated, only the affected key (`prim:{plane}:{id}`) is deleted from Redis, forcing the next query to reload that single YAML from disk and re-cache it. Full cache flushes are banned. TTL-only expiry is banned as sole freshness mechanism â€” event-driven invalidation is mandatory. The `/api/primitives/invalidate` endpoint accepts a `POST` with `primitive_id` for CI/CD integration. |
| **The Deterministic Override Rule** | Phase1-M05 | Story 2.2 (Context-Aware Primitive Resolution) | The `ConflictResolver` middleware intercepts every multi-primitive query. It reads the `conflicts_with` field from each requested primitive's cached YAML. When mutual conflicts are detected (A conflicts with B AND B conflicts with A, or A unilaterally conflicts with B), the resolver applies a strict precedence hierarchy: (1) primitives with higher `experience_stage_fit.scoring` values win in scoring contexts, (2) primitives explicitly requested by the orchestration engine's primary intent take precedence over secondary enrichment primitives, (3) if precedence is tied, the primitive with the lower family-sort-order wins (TRG > FRC > TRS > FBK > PRG > SOC > SAF > PER). The losing primitive is stripped from the payload and logged to receipt chain. Contradictory primitive payloads reaching downstream systems are strictly banned. |

### 3.5 Technical Decisions

| Decision | Rationale | Alternative Rejected | Why Rejected |
|----------|-----------|---------------------|-------------|
| Redis-backed cache with in-process dict mirror | Sub-ms query latency for hot path; Redis provides cross-worker consistency for invalidation | SQLite/PostgreSQL cache table | Database queries add 5-15ms latency, violating the 3-second RIM SLA chain |
| YAML parsed to Pydantic models at load time | Type safety, schema validation, `conflicts_with` field guaranteed to be a `list[str]` | Raw dict storage | No type safety; `conflicts_with` could be missing/malformed without detection |
| Deterministic family-sort-order tiebreaker | Reproducible, auditable conflict resolution without AI involvement | LLM-based conflict resolution | Non-deterministic; violates Phase1-M05 mandate; adds latency |
| FastAPI `lifespan` context manager for init | Ensures all primitives are loaded before any request is served | Lazy loading on first request | First request would take 2-5 seconds parsing 243+ YAMLs, violating RIM SLA |
| Separate endpoints for experience vs meaning planes | Enforces PRD-08 Â§2.1 Plane Separation at the API level | Single `/primitives/` endpoint with plane filter | Risks plane confusion; violates PRD-08 architectural claim |
<!-- UPDATED: Added SDA boundary decision -->
| Strict read-through boundary for SDA | Prevents the primitive registry from absorbing semantic ontology | Merge SDA schemas into primitive YAMLs | Violates PRD-08 Â§3.6; creates a false registry and collapses the architecture |

---


<!-- UPDATED: Added boundary law to prevent primitive registry from absorbing SDA ontology -->
### 3.6 Primitive Registry Boundary Law

This service owns primitive records, but it **does not own deep semantic ontology**. Following the Wave-0 PRD updates and SDA artifact taxonomy:

- **Primitives remain transformation operators.** They are not deep ontology. They encode meaning-spaces and transformation labs.
- **SDA artifacts are sibling infrastructure.** `Existential Invariants`, `Representation Geometries`, and `Archetypal Geometries` are canonical ontology layers managed by `FR-ERA3-20`, not new primitive families.
- **No SDA merging.** The primitive registry schemas must not be expanded to absorb SDA structural grammar or ontology logic.
- **Separation of concerns:** The Primitive Registry answers "What transformation operators exist and conflict?" while the SDA Query Service answers "What deep human pressures and directional topologies do those operators map to?"

<!-- UPDATED: Defined integration seam with FR-ERA3-21 SDA Query and Crosswalk Service -->
### 3.7 SDA Integration Seam

The service interfaces with the **SDA Query and Crosswalk Service (FR-ERA3-21)** via a strict read-through boundary:

| Operation | Owned By | Responsibility |
|-----------|----------|----------------|
| **Primitive Native Lookups** | `FR-ERA3-06` (This Service) | Returns the primitive YAML contents, resolves conflicts, and queries by primitive ID, family, or plane. |
| **Crosswalk-Mediated Lookups** | `FR-ERA3-21` (SDA Service) | Resolves the mapping between a primitive ID and its corresponding `Existential Invariant` or other SDA objects. |
| **Verification Handshake** | `FR-ERA3-06` (This Service) | Exposes primitive existence and metadata so `FR-ERA3-21` can verify primitive IDs before returning crosswalk lineage. |

The `ExperiencePrimitiveRecord.crosswalk_id` field serves as the anchor point for this integration. Downstream consumers requiring semantic invariants will ask the SDA service to resolve the primitive, and the SDA service will verify the primitive here before returning the crosswalk bundle.

## 4. Implementation Plan

### Phase A: Models & Schema (Tasks 1-3)

- [ ] **Task 1:** Create `src/ccp/models/primitive_registry_models.py` â€” Define `ExperiencePrimitiveRecord`, `MeaningPrimitiveRecord`, `PrimitiveQueryRequest`, `PrimitiveQueryResponse`, `ConflictResolutionResult`, `CacheHealthStatus` Pydantic v2 models.
- [ ] **Task 2:** Define `PRIMITIVE_QUERY_AUDIT_SQL` in the models file â€” `primitive_query_audit` table for receipt logging.
- [ ] **Task 3:** Add `FAMILY_SORT_ORDER` constant dict mapping family codes to precedence integers (TRG=0, FRC=1, TRS=2, FBK=3, PRG=4, SOC=5, SAF=6, PER=7).

### Phase B: Core Service (Tasks 4-7)

- [ ] **Task 4:** Create `src/ccp/services/primitive_registry_service.py` â€” Implement `YAMLRegistryLoader` class with `load_all(base_path: str) -> dict[str, ExperiencePrimitiveRecord | MeaningPrimitiveRecord]` that recursively walks `primitives/` and parses each YAML into the appropriate Pydantic model.
- [ ] **Task 5:** Implement `RegistryCacheManager` class with `warm_cache()`, `get(primitive_id) -> PrimitiveRecord | None`, `invalidate_primitive(primitive_id)`, `health() -> CacheHealthStatus` methods. Uses Redis with key pattern `prim:{plane}:{id}` and in-process dict mirror.
- [ ] **Task 6:** Implement `ConflictResolver` class with `resolve(requested_ids: list[str], context: str) -> ConflictResolutionResult` that parses `conflicts_with` fields, detects mutual conflicts, applies precedence hierarchy, returns clean payload with resolution log.
- [ ] **Task 7:** Implement `PrimitiveRegistryQueryService` orchestrator class with `query_by_id(id)`, `query_by_family(family)`, `query_by_plane(plane)`, `query_batch(ids, context)` methods. Integrates loader, cache, resolver, and receipt chain.

### Phase C: API Layer (Tasks 8-10)

- [ ] **Task 8:** Create `src/ccp/api/primitive_registry_api.py` â€” FastAPI router with endpoints: `GET /api/primitives/experience/{id}`, `GET /api/primitives/meaning/{id}`, `POST /api/primitives/query` (batch), `GET /api/primitives/family/{family_code}`, `GET /api/primitives/plane/{plane}`, and `GET /api/primitives/health`.
- [ ] **Task 9:** Add `POST /api/primitives/invalidate` endpoint accepting `{"primitive_id": "EXP-FBK-001"}` for targeted cache invalidation. Secured via internal API key.
- [ ] **Task 10:** Register router in `src/ccp/api/main.py` via `app.include_router(primitive_router, prefix="/api", tags=["Primitives"])`. Add lifespan init for cache warming and extend `/health` to expose `CacheHealthStatus`.

### Phase D: Integration & Testing (Tasks 11-14)

- [ ] **Task 11:** Add Redis connection factory to `src/ccp/services/primitive_registry_service.py` following `telegram_webhook.py` dedup pattern.
- [ ] **Task 12:** Create `tests/integration/test_era3_fr06_primitive_registry.py` â€” integration tests following `test_ca11_fr19_trivianar_engine.py` pattern.
- [ ] **Task 13:** Create `tests/integration/test_era3_fr06_conflict_resolver.py` â€” conflict resolution tests with real YAML `conflicts_with` data.
- [ ] **Task 14:** Wire receipt chain logging for all query, invalidation, and conflict resolution operations using `ReceiptChain.log()` pattern from `cpr_query_service.py`.

---

## 5. Primary Output Schema

```python
# src/ccp/models/primitive_registry_models.py
from __future__ import annotations
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator

# â”€â”€ Constants â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

FAMILY_SORT_ORDER: dict[str, int] = {
    "TRG": 0, "FRC": 1, "TRS": 2, "FBK": 3,
    "PRG": 4, "SOC": 5, "SAF": 6, "PER": 7,
}

EXPERIENCE_PLANE = "experience"
MEANING_PLANE = "meaning"

CACHE_KEY_PREFIX_EXP = "prim:exp"
CACHE_KEY_PREFIX_MNG = "prim:mng"

REGISTRY_AGENT_NAME = "Athena"

PRIMITIVE_QUERY_AUDIT_SQL = """
CREATE TABLE IF NOT EXISTS primitive_query_audit (
    audit_id        TEXT PRIMARY KEY,
    query_type      TEXT NOT NULL,
    requested_ids   JSONB NOT NULL,
    resolved_ids    JSONB NOT NULL,
    conflicts_found JSONB NOT NULL DEFAULT '[]',
    resolution_log  JSONB NOT NULL DEFAULT '[]',
    latency_ms      REAL NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""


# â”€â”€ Enums â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class PrimitivePlane(str, Enum):
    EXPERIENCE = "experience"
    MEANING = "meaning"


class ConflictPrecedenceReason(str, Enum):
    SCORING_FIT = "higher_scoring_stage_fit"
    PRIMARY_INTENT = "primary_intent_priority"
    FAMILY_ORDER = "family_sort_order_tiebreak"


# â”€â”€ Primitive Records â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class ExperienceStageFit(BaseModel):
    entry: float = Field(ge=0.0, le=1.0)
    activation: float = Field(ge=0.0, le=1.0)
    recording: float = Field(ge=0.0, le=1.0)
    scoring: float = Field(ge=0.0, le=1.0)
    social_spread: float = Field(ge=0.0, le=1.0)
    recovery: float = Field(ge=0.0, le=1.0)
    retention: float = Field(ge=0.0, le=1.0)
    conversion: float = Field(ge=0.0, le=1.0)


class ExperiencePrimitiveRecord(BaseModel):
    """Typed representation of a single experience primitive YAML."""
    experience_primitive_id: str = Field(pattern=r"^EXP-[A-Z]{3}-\d{3}$")
    canonical_name: str = Field(min_length=1)
    aliases: list[str] = Field(default_factory=list)
    experience_family: str = Field(min_length=1)
    mechanic_role: str = Field(min_length=1)
    moment_role: str = Field(min_length=1)
    implementation_role: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    core_move: str = Field(min_length=1)
    why_it_works: str = Field(min_length=1)
    synergizes_with: list[str] = Field(default_factory=list)
    conflicts_with: list[str] = Field(default_factory=list)
    experience_stage_fit: ExperienceStageFit
    # <!-- UPDATED: Documented crosswalk_id field as the anchor for FR-ERA3-21 -->
    crosswalk_id: str = Field(default="", description="The crosswalk anchor ID used by FR-ERA3-21 to map this primitive to canonical SDA ontology like Existential Invariants.")

    @field_validator("conflicts_with", mode="before")
    @classmethod
    def normalize_conflicts(cls, v: list[str]) -> list[str]:
        """Strip 'None' strings and empty entries from conflicts_with."""
        if not v:
            return []
        return [c for c in v if c and c.lower() != "none" and c.strip()]


class MeaningPrimitiveRecord(BaseModel):
    """Typed representation of a single meaning primitive YAML."""
    primitive_id: str = Field(pattern=r"^PRM-[A-Z]{3}-\d{3}$")
    primitive_name: str = Field(min_length=1)
    family: str = Field(min_length=1)
    version: str = Field(default="2.0")
    definition: str = Field(min_length=1)
    coalition_partners_synergistic: list[str] = Field(default_factory=list)
    coalition_partners_antagonistic: list[str] = Field(default_factory=list)


# â”€â”€ Query/Response Models â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

class PrimitiveQueryRequest(BaseModel):
    """Batch query request for multiple primitives."""
    requested_ids: list[str] = Field(min_length=1)
    context: str = Field(default="general", description="Scoring context for conflict precedence")
    include_conflicts_log: bool = Field(default=True)


class ConflictEntry(BaseModel):
    """A single detected conflict between two primitives."""
    primitive_a: str
    primitive_b: str
    winner: str
    loser: str
    reason: ConflictPrecedenceReason


class ConflictResolutionResult(BaseModel):
    """Result of conflict resolution across a set of primitives."""
    clean_ids: list[str] = Field(description="IDs after conflict stripping")
    removed_ids: list[str] = Field(default_factory=list)
    conflicts: list[ConflictEntry] = Field(default_factory=list)
    resolution_applied: bool = Field(default=False)


class PrimitiveQueryResponse(BaseModel):
    """Response from a batch primitive query."""
    query_id: str
    requested_ids: list[str]
    resolved_primitives: list[ExperiencePrimitiveRecord | MeaningPrimitiveRecord]
    conflict_resolution: ConflictResolutionResult
    cache_hit: bool = Field(default=True)
    latency_ms: float = Field(ge=0.0)


class CacheHealthStatus(BaseModel):
    """Health check for the primitive cache."""
    experience_count: int = Field(ge=0)
    meaning_count: int = Field(ge=0)
    total_cached: int = Field(ge=0)
    redis_connected: bool
    last_warm_at: str
    stale_keys: int = Field(default=0, ge=0)
```

---

## 6. Backward Compatibility Fallback

Following the `circuit_breaker.py` fail-closed pattern:

1. **Redis Unavailable:** If Redis connection fails during `lifespan` init, the service falls back to an in-process `dict` cache loaded directly from YAML disk reads. A `WARNING` receipt is logged. All queries continue to function but without cross-worker invalidation consistency. The `/health` endpoint reports `redis_connected: false`.

2. **YAML Parse Failure:** If a single YAML file fails Pydantic validation during loading, the service logs the error to receipt chain, skips the malformed file, and continues loading remaining primitives. The `CacheHealthStatus.stale_keys` counter increments. The service does NOT halt â€” partial registry is better than no registry.

3. **Conflict Resolver Failure:** If the `ConflictResolver` encounters an unknown primitive ID in a `conflicts_with` field (referencing a primitive not in the registry), it logs a warning and treats the conflict as non-applicable. The requesting primitive is NOT stripped. This prevents cascading failures from incomplete registry states.

4. **Hot-Reload Failure:** If targeted invalidation fails (Redis key deletion error), the service falls back to serving the existing cached version and schedules a retry. It does NOT perform a full cache flush, preserving the Phase1-M04 mandate.

<!-- UPDATED: Added fallback behavior for SDA unavailability -->
5. **SDA Integration Unavailable:** If downstream systems query the SDA Query and Crosswalk Service (FR-ERA3-21) and it is unavailable, this Primitive Registry Query Service continues to function entirely normally. It is not dependent on SDA for its own primitive-native lookups. The `crosswalk_id` field will simply remain unresolvable by the sibling service until SDA recovers.

---

## 7. Tasks

### Sprint 1: Registry Models and Schema

- [ ] Create `src/ccp/models/primitive_registry_models.py` with `PrimitivePlane`, `ConflictPrecedenceReason`, `ExperiencePrimitiveRecord`, `MeaningPrimitiveRecord`, `PrimitiveQueryRequest`, `PrimitiveQueryResponse`, `ConflictResolutionResult`, and `CacheHealthStatus`.
- [ ] Add `FAMILY_SORT_ORDER`, cache key constants, agent constants, and `PRIMITIVE_QUERY_AUDIT_SQL` to `src/ccp/models/primitive_registry_models.py`.
- [ ] Extend `src/ccp/scripts/setup_supabase.py` to append `primitive_query_audit` table DDL and indexes into `SCHEMA_SQL`.
- [ ] Add exports for the new registry models in `src/ccp/models/__init__.py` if the package export surface is being maintained centrally.

### Sprint 2: Loader, Cache, and Resolver

- [ ] Create `src/ccp/services/primitive_registry_service.py` with `YAMLRegistryLoader` that walks `primitives/experience/**/*.yaml` and `primitives/meaning/**/*.yaml`.
- [ ] Implement `RegistryCacheManager` in `src/ccp/services/primitive_registry_service.py` with Redis-backed storage plus an in-process dict mirror keyed as `prim:{plane}:{id}`.
- [ ] Implement `ConflictResolver` in `src/ccp/services/primitive_registry_service.py` using `conflicts_with`, scoring-context precedence, primary-intent precedence, and `FAMILY_SORT_ORDER` tiebreaking.
- [ ] Implement `PrimitiveRegistryQueryService` in `src/ccp/services/primitive_registry_service.py` with `query_by_id()`, `query_by_family()`, `query_by_plane()`, `query_by_tag()`, `query_batch()`, `invalidate_primitive()`, and `health()`.
- [ ] Wire `ReceiptChain.log()` calls into `src/ccp/services/primitive_registry_service.py` for registry warm, cache hit/miss, conflict stripping, invalidation, and degraded fallback paths.

### Sprint 3: API and Application Wiring

- [ ] Create `src/ccp/api/primitive_registry_api.py` with `GET /api/primitives/experience/{primitive_id}` and `GET /api/primitives/meaning/{primitive_id}`.
- [ ] Create `POST /api/primitives/query`, `GET /api/primitives/family/{family_code}`, `GET /api/primitives/plane/{plane}`, and `GET /api/primitives/health` in `src/ccp/api/primitive_registry_api.py`.
- [ ] Create `POST /api/primitives/invalidate` in `src/ccp/api/primitive_registry_api.py`, guarded by an internal API key check matching the existing secret-header pattern in `src/ccp/api/telegram_webhook.py`.
- [ ] Modify `src/ccp/api/main.py` to register `primitive_router`, initialize the service during application startup, and extend `/health` with registry cache diagnostics.

### Sprint 4: Consumer Integration and Verification

- [ ] Update `src/ccp/services/dpa_engine.py` integration notes or consumer hooks so branding and experience systems can query primitive constraints through the service instead of direct YAML reads.
- [ ] Add `tests/integration/test_era3_fr06_primitive_registry.py` covering cache warm, by-id queries, plane/family queries, and invalidation behaviour.
- [ ] Add `tests/integration/test_era3_fr06_conflict_resolver.py` covering mutually exclusive primitives, unilateral conflicts, `"None"` conflict normalization, and deterministic tiebreaking.
- [ ] Add `tests/integration/test_era3_fr06_primitive_registry_api.py` covering route registration, auth rejection for invalidation, 404 for unknown primitive IDs, and health payload shape.
- [ ] Verify every new test file follows the existing `_run()` helper and class-per-AC organization used in `tests/integration/test_ca11_fr19_trivianar_engine.py` and `tests/integration/test_ca11_fr15_dpa_engine.py`.

---

## 8. Acceptance Criteria

### AC-2.1.1: Startup Registry Warm and In-Memory Serving

**CBAR Mandate Enforced:** Phase1-M04 - The Hot-Reload Rule

**Given** the FastAPI application starts with access to the `primitives/` registry,
**When** application startup initialization runs,
**Then** the service parses all valid primitive YAML files exactly once during startup,
**And** caches each parsed primitive in Redis plus the worker's in-process mirror,
**And** all subsequent runtime registry queries are served from cache without disk I/O.

**FAILURE EXAMPLE:** The worker starts successfully, but the first live request for `EXP-FBK-001` opens the YAML file from disk because startup skipped cache warming. A burst of concurrent requests causes repeated disk reads, pushing feedback latency above the allowed budget. This is a spec violation.

**Measurable pass condition:** `CacheHealthStatus.total_cached >= 243` after startup, and 100 consecutive hot-path queries execute with zero additional YAML file reads and P95 service lookup latency under 3ms.

---

### AC-2.1.2: Targeted Primitive Hot Reload

**CBAR Mandate Enforced:** Phase1-M04 - The Hot-Reload Rule

**Given** a single primitive YAML has been updated and the deployment pipeline posts `{"primitive_id": "EXP-TRG-002"}` to the invalidation endpoint,
**When** the invalidation handler runs,
**Then** it deletes only the affected cache key for that primitive,
**And** the next request for `EXP-TRG-002` reloads only that YAML file into Redis and the local mirror,
**And** all other cached primitives remain intact and immediately queryable.

**FAILURE EXAMPLE:** A one-line correction to `EXP-TRG-002.yaml` triggers a full Redis flush, wiping 242 unrelated primitive cache entries. The next wave of requests re-parses the full registry and causes avoidable latency spikes. This is a spec violation.

**Measurable pass condition:** After invalidating one primitive, exactly one cache key is deleted, the updated primitive is reloaded on first access, and cache hit counts for unrelated primitives remain unchanged.

---

### AC-2.2.1: Conflict Filtering Before Payload Return

**CBAR Mandate Enforced:** Phase1-M05 - The Deterministic Override Rule

**Given** an active Reaction Loop requests a primitive set containing a known conflict pair such as `["EXP-SAF-003", "EXP-SOC-002"]`,
**When** `POST /api/primitives/query` resolves the batch,
**Then** the service inspects each requested primitive's `conflicts_with` field,
**And** the `ConflictResolver` removes the losing primitive before returning the payload,
**And** the response includes an explicit conflict-resolution log describing which primitive was stripped and why.

**FAILURE EXAMPLE:** The orchestration layer requests `EXP-SAF-003` and `EXP-SOC-002`, and the API returns both records untouched. A downstream prompt engine receives contradictory recovery and social-pressure rules in the same payload and generates unstable instructions. This is a spec violation.

**Measurable pass condition:** For any request containing a verified conflict pair, `PrimitiveQueryResponse.conflict_resolution.resolution_applied == true`, `removed_ids` is non-empty, and the returned primitive list contains no conflicting pair.

---

### AC-2.2.2: Deterministic Tiebreaking Order

**CBAR Mandate Enforced:** Phase1-M05 - The Deterministic Override Rule

**Given** two requested primitives conflict and neither can be discarded by simple presence rules alone,
**When** the resolver evaluates precedence,
**Then** it applies the hierarchy in this exact order: scoring-context fit, primary-intent priority, family sort order,
**And** if family sort order is required, it uses `TRG > FRC > TRS > FBK > PRG > SOC > SAF > PER`,
**And** it logs the winning primitive and the exact precedence reason into the receipt chain and API response.

**FAILURE EXAMPLE:** The same pair of conflicting primitives is requested twice under identical context, but request one keeps `EXP-TRS-001` while request two keeps `EXP-FBK-001` because resolution depends on Python dict iteration order. This non-determinism makes audits impossible. This is a spec violation.

**Measurable pass condition:** Replaying the same conflicting request 1,000 times under identical context returns the same winning primitive every time, and the precedence reason is identical across all runs.

---

### AC-2.2.3: Query Surface Coverage Across ID, Family, and Plane

**CBAR Mandate Enforced:** None directly; inherits M04 freshness and M05 clean payload requirements

**Given** downstream systems need primitives by exact ID, by family, or by plane,
**When** they call the corresponding service or API query path,
**Then** the service returns typed Pydantic responses for the requested slice,
**And** experience-plane endpoints never return meaning-plane records,
**And** unknown IDs return a clean 404 or empty-result contract rather than a malformed payload.

**FAILURE EXAMPLE:** `GET /api/primitives/experience/EXP-FBK-001` returns a meaning-plane schema, or `GET /api/primitives/family/feedback_scoring` mixes experience and meaning records without a plane boundary. Downstream consumers now need custom cleanup logic. This is a spec violation.

**Measurable pass condition:** By-id, by-family, and by-plane endpoints all return schema-valid payloads; plane-specific endpoints return only records from the requested plane; unknown IDs return HTTP 404 with no partial record body.

---

<!-- UPDATED: Added AC for Primitive Registry boundary enforcement -->
### AC-2.2.4: SDA Boundary Preservation

**CBAR Mandate Enforced:** None directly; enforces PRD-08 Â§3.6 primitive/SDA separation law

**Given** the service loads primitives and serves query responses,
**When** a primitive contains a `crosswalk_id`,
**Then** the service returns the `crosswalk_id` as part of the `ExperiencePrimitiveRecord`,
**And** it does not attempt to resolve the crosswalk locally, load SDA ontology files, or merge SDA schemas into the primitive response.

**FAILURE EXAMPLE:** The Primitive Registry Query Service notices a `crosswalk_id`, reaches out to `FR-ERA3-21` (or reads SDA files directly), and injects the `Existential Invariant` payload into the primitive response. This collapses the architecture and turns the primitive registry into a generic semantic warehouse. This is a spec violation.

**Measurable pass condition:** The returned primitive record schema exactly matches the primitive YAML, and the service never initiates queries against the SDA registry.

---

## 9. Dependencies

### Internal

| Service/Spec | Dependency Type | What This Spec Needs From It |
|-------------|-----------------|------------------------------|
| `src/ccp/api/main.py` | Code extension | Router registration, startup initialization, and `/health` payload extension |
| `src/ccp/api/telegram_webhook.py` | Pattern reference | Secret-header verification pattern and lightweight request-guard style for internal invalidation endpoints |
| `src/ccp/services/cpr_query_service.py` | Pattern reference | Registry-style staged initialization and `ReceiptChain.log()` usage for query actions |
| `src/ccp/services/dpa_engine.py` | Runtime consumer | Downstream experience systems query primitive constraints without direct YAML reads |
| `src/ccp/core/receipt_chain.py` | Runtime dependency | Immutable logging of warm-cache, query, invalidation, conflict-resolution, and degraded-fallback events |
| `src/ccp/core/circuit_breaker.py` | Pattern reference | Fail-closed and graceful-degradation behaviour when Redis or YAML loading partially fails |
| `src/ccp/scripts/setup_supabase.py` | Code extension | Adds `primitive_query_audit` DDL and indexes into the canonical schema bootstrap |
| `primitives/experience/**/*.yaml` | Data contract | Canonical experience primitive source of truth, including `conflicts_with` and `experience_stage_fit` |
| `primitives/meaning/**/*.yaml` | Data contract | Canonical meaning primitive source of truth for plane-aware query support |
| `reference/conscious-rivers/docs/prd/modules/PRD_08_Conscious_Primitives.md` | Requirements dependency | Plane separation, primitive schema fields, and orchestration assumptions this service must enforce |
| `FR-ERA3-08` Mini App Host Shell | Downstream dependency | Future Mini App surfaces consume already-resolved primitive data rather than touching YAML directly |
<!-- UPDATED: Added SDA spec dependencies -->
| `FR-ERA3-20` SDA Ontology and Registry | Boundary enforcement | Defines what SDA canonical artifacts are, ensuring they are NOT loaded by this service |
| `FR-ERA3-21` SDA Query and Crosswalk Service | Downstream dependency | Consumes this service to verify primitive metadata during crosswalk mapping |

### External

| API/Library | Version | Purpose |
|------------|---------|---------|
| `fastapi` | `>=0.110.0` | Route layer, startup lifecycle, and response models |
| `pydantic` | `>=2.6.0` | Strongly typed request/response and YAML record validation |
| `redis` | `>=5.0.0` | Shared cache and targeted invalidation across workers |
| `PyYAML` | `>=6.0.1` | YAML parsing for `primitives/experience/` and `primitives/meaning/` |
| `supabase` | `>=2.3.0` | Optional persistence of `primitive_query_audit` and consistency with existing schema tooling |
| PostgreSQL | Existing platform dependency | Backing store for audit rows if persisted beyond file-based receipt logs |

---

## 10. Testing Strategy

### Unit Tests

**File:** `tests/integration/test_era3_fr06_primitive_registry.py`

```python
def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


class TestYAMLRegistryLoader:
    def test_load_experience_primitive_by_verified_id()
    def test_load_meaning_primitive_by_verified_id()
    def test_normalize_none_conflicts_to_empty_list()
    def test_invalid_yaml_is_skipped_and_counted_stale()


class TestRegistryCacheManager:
    def test_warm_cache_loads_all_registry_files()
    def test_get_returns_cached_record_without_disk_reload()
    def test_invalidate_primitive_deletes_single_cache_key()
    def test_health_reports_redis_connectivity_and_counts()


class TestPrimitiveRegistryQueryService:
    def test_query_by_id_returns_typed_record()
    def test_query_by_family_returns_only_requested_family()
    def test_query_by_plane_preserves_plane_boundary()
    def test_query_logs_receipt_chain_entry()
```

**File:** `tests/integration/test_era3_fr06_conflict_resolver.py`

```python
class TestConflictResolver:
    def test_ac221_filters_exp_saf_003_vs_exp_soc_002()
    def test_unilateral_conflict_still_removes_loser()
    def test_family_sort_order_breaks_ties_deterministically()
    def test_primary_intent_beats_secondary_enrichment()
    def test_scoring_context_prefers_higher_stage_fit()
```

**File:** `tests/integration/test_era3_fr06_primitive_registry_api.py`

```python
class TestPrimitiveRegistryAPI:
    def test_get_experience_primitive_returns_200()
    def test_get_unknown_primitive_returns_404()
    def test_post_query_returns_conflict_resolution_block()
    def test_invalidate_requires_internal_api_key()
    def test_health_includes_total_cached_and_redis_connected()
```

### Integration Tests

Modeled on `tests/integration/test_ca11_fr19_trivianar_engine.py` and `tests/integration/test_ca11_fr15_dpa_engine.py`:
- use a local `_run()` helper instead of `pytest-asyncio`
- organize tests by acceptance-criterion class
- use small fixture builders for primitive records and cache state
- assert constants, SQL strings, and receipt-chain side effects directly

**File:** `tests/integration/test_era3_fr06_primitive_registry.py`

```python
class TestRegistryParsingAndCaching:
    def test_ac211_startup_warm_serves_queries_from_memory(self)
    def test_ac212_targeted_invalidation_reloads_only_one_primitive(self)
    def test_health_payload_matches_cache_state(self)


class TestPlaneQueries:
    def test_experience_endpoint_never_returns_meaning_record(self)
    def test_meaning_plane_query_returns_only_meaning_records(self)

<!-- UPDATED: Added boundary enforcement test -->
class TestSDABoundaryEnforcement:
    def test_ac224_service_does_not_resolve_crosswalk_ids_locally(self)
    def test_service_never_loads_sda_yaml_files(self)
```

**File:** `tests/integration/test_era3_fr06_conflict_resolver.py`

```python
class TestContextAwarePrimitiveResolution:
    def test_ac221_conflicting_batch_returns_clean_payload(self)
    def test_ac222_identical_request_replayed_100_times_is_stable(self)
    def test_conflict_resolution_receipt_logged(self)


class TestRealRegistryExamples:
    def test_exp_fbk_001_conflict_field_is_respected(self)
    def test_exp_trs_001_corrected_id_is_used_not_exp_trb_prefix(self)
```

**File:** `tests/integration/test_era3_fr06_primitive_registry_api.py`

```python
class TestRouteRegistration:
    def test_router_is_mounted_under_api_prefix(self)
    def test_family_query_endpoint_returns_schema_valid_payload(self)
    def test_invalidate_endpoint_rejects_missing_secret(self)
```

### Manual Verification

1. Start the FastAPI app and confirm startup completes with registry warm logs in the local receipt chain.
2. Call `GET /api/primitives/health` and verify `total_cached >= 243`, `experience_count > 0`, and `meaning_count > 0`.
3. Call `GET /api/primitives/experience/EXP-FBK-001` and verify the response is a typed experience primitive record with `conflicts_with` normalized as a list.
4. Call `POST /api/primitives/query` with `{"requested_ids": ["EXP-SAF-003", "EXP-SOC-002"], "context": "scoring"}` and verify one primitive is removed plus the conflict-resolution reason is returned.
5. Modify a test primitive YAML locally, call `POST /api/primitives/invalidate`, and verify only that primitive is reloaded on the next request while unrelated queries remain cache hits.
6. Stop Redis, restart the app, and verify the service degrades to in-process cache, still answers queries, and surfaces `redis_connected: false` in health output.
7. Replay the same conflicting batch request repeatedly and verify the same winner is returned every time.
8. Query a meaning-plane endpoint and verify no experience-plane schema fields leak into the payload.

