# Phase 1 — Architecture Decision Record: Pi / Eve Package / StateM / OKF / Supabase / Redis

**Mandate ID:** `CAE-M11`  
**Status:** `RATIFIED_INVENTORY_AND_CONTRACTS_BASELINE`  
**Governing Authority:** `docs/CANONICAL_SKILL_AUTHORING_CONSTITUTION.md`, `docs/PRD/CURRENT.md` (v0.3.0), `00_CONTROL/01_BASELINE_AUTHORITY_READ_SET.md`, `00_CONTROL/02_EXTERNAL_RESEARCH_REGISTER.md`, `00_CONTROL/05_PROGRAM_PACKAGE_AND_AGENT_CONVENTION.md`, `00_CONTROL/06_STATE_AND_HOOKS_MODEL.md`  
**Repository Revision:** `1b65889723e0eda405543e74a43304703307abca`  
**Execution Date:** `2026-08-31`  

---

## 1. Executive Summary & Purpose

This Architecture Decision Record (ADR) establishes the binding architectural boundaries, subsystem ownership matrix, adopted implementation patterns, rejected abstractions, and fail-closed no-go conditions across all external frameworks, design references, and runtime engines integrated into the Conscious Activation Engine (CAE).

It formally resolves the technical posture of six core components:
1. **Pi**: Execution Substrate (Adopted for runtime graph scheduling & tool dispatch).
2. **Eve**: Package Composition Reference (Adopted for developer authoring filesystem conventions).
3. **CAE**: Authoritative Domain Layer (Sole system of record, typed mutation boundary, 4 Authority Lanes).
4. **StateM**: Runtime Context & Hook Lifecycle Pattern (Adopted for explicit context-and-contract boundaries, state entry/exit hooks, transition gating, and recovery runbooks).
5. **Supabase / PostgreSQL**: Operational & Security Authority (Sole authority for multi-tenant RLS, state aggregates, transition ledgers, and cryptographic receipts).
6. **Open Knowledge Format (OKF)**: Curated Knowledge Representation (Adopted as portable markdown/YAML exchange format for static/semi-static knowledge).
7. **Redis / Redis Iris**: Optional Performance Cache (Explicitly rejected as state/knowledge authority; relegated to optional, ephemeral caching and pub/sub transport).

---

## 2. Subsystem Ownership and Authority Matrix

| Subsystem / Technology | Primary Role in CAE | Authority Posture | Canonical Storage Model | Adopted Patterns | Rejected Patterns / No-Go Invariants |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CAE Domain & Operations** | System of Record & Domain Invariants | **AUTHORITATIVE** | PostgreSQL schema `cae` | Typed operations, 4 Authority Lanes (`HUNTER`, `ANALYST`, `COMPOSER`, `COMMANDER`), Pydantic domain models, optimistic CAS concurrency. | Framework concepts becoming domain ontology; untyped LLM hallucinations mutating state. |
| **Supabase / PostgreSQL** | Operational Database & Security Anchor | **AUTHORITATIVE** | Relational tables with Row-Level Security (RLS) | Tenancy isolation (`workspace_id`), immutable state transition ledgers, cryptographic receipt verification. | Direct unauthenticated SQL access, bypass of RLS policies, untracked mutations. |
| **Pi Engine** | Workflow & Graph Execution Substrate | **SUBSTRATE ONLY** | None (Ephemerally mounts state from CAE) | DAG traversal, async step runner, tool invocation dispatch, runtime hook firing. | Pi defining new state ontology, creating parallel receipt records, or redefining authority lanes. |
| **Eve Layout** | Package & Directory Authoring Reference | **REFERENCE ONLY** | Filesystem files (`manifest.yaml`, `instructions.md`) | Structured package folders (`programs/`, `agents/`, `skills/`, `evals/`). | Filesystem packages acting as runtime database; disk files overriding database state. |
| **StateM** | Runtime Context Boundary & Gating Pattern | **PATTERN ONLY** | None (Executes against PostgreSQL state) | States as context-and-contract boundaries, `in_hook` $\to$ work $\to$ `out_hook` $\to$ `before_transfer` $\to$ repair lifecycle. | Local `.statem` disk state directory; standalone CLI tool replacing CAE database. |
| **Open Knowledge Format (OKF)** | Curated Knowledge Representation & Exchange | **EXCHANGE FORMAT** | Portable Markdown/YAML files & static corpus | Progressive disclosure, structured concept/entity/source schema, portable domain exchange. | OKF acting as operational execution database or mutable transaction ledger. |
| **Redis / Redis Iris** | Optional Cache & Pub/Sub Transport | **OPTIONAL ADAPTER** | Ephemeral in-memory key-value | Short-term token bucket caching, distributed locking, WebSocket fan-out. | Redis storing authoritative state, knowledge graph truth, or required core dependency. |

---

## 3. Detailed Architecture Decisions

### 3.1 Decision 1: Pi as Pure Execution Substrate
- **Context:** The system requires an async execution runtime to traverse workflow DAGs, schedule concurrent agent tasks, invoke external tools, and fire extension hooks.
- **Decision:** Pi is adopted as the underlying execution substrate.
- **Adopted Elements:**
  - Runtime workflow graph traversal (`RuntimeWorkflowGraph`).
  - Async task dispatcher and tool adapter execution.
  - Runtime extension and hook invocation machinery.
- **Rejected Elements & Boundaries:**
  - Pi is **not** a domain authority.
  - Pi sessions, internal memory dumps, or runtime representations do **not** become CAE state.
  - Pi cannot introduce an alternative receipt or event logging standard.

---

### 3.2 Decision 2: Eve-Inspired Package Composition Surface
- **Context:** Developers and prompt engineers need standard, modular directory structures for authoring Programs, Agents, and Skills.
- **Decision:** Adopt Eve-style package conventions as human/developer authoring surfaces:
  ```
  programs/<program-id>/
      program.md
      manifest.yaml
      harness/
      agents/
      operations/
      evals/
      references/
  ```
- **Adopted Elements:**
  - Clear structural separation: `CAE.md` (governance/context constraints), `instructions.md` (role behavior), `skills/` (passive canonical skill capsules), `subagents/` (local specialist configs).
- **Rejected Elements & Boundaries:**
  - The filesystem is an **authoring/composition surface**, not canonical state.
  - Canonical artifacts and state never live only on disk as Markdown.
  - Packaging files on disk cannot override or bypass PostgreSQL state.

---

### 3.3 Decision 3: StateM-Inspired Context & Hook Execution Semantics
- **Context:** Long-running agents require clean phase boundaries, context refreshing, and deterministic verification before transferring control.
- **Decision:** Adopt the StateM procedural control pattern:
  $$\text{Plan} \longrightarrow \text{State Entry (\texttt{in\_hook})} \longrightarrow \text{Agent Work} \longrightarrow \text{Exit (\texttt{out\_hook})} \longrightarrow \text{Gating (\texttt{before\_transfer})} \longrightarrow \text{Verify / Repair}$$
- **Adopted Elements:**
  - States as explicit context-and-contract boundaries.
  - `in_hook`: Prepares state-local context and loads required domain invariants.
  - `out_hook`: Persists intermediate checkpoints and stages candidate outputs.
  - `before_transfer`: Deterministic blocking validation checks before advancing state.
  - Dynamic failure-driven recovery runbooks executed outside the primary model context.
- **Rejected Elements & Boundaries:**
  - StateM's local `.statem` directory is **explicitly rejected**.
  - CAE's authoritative PostgreSQL tables (`cae.state_aggregate`, `cae.state_transition`) are the sole state store.

---

### 3.4 Decision 4: PostgreSQL / Supabase as Sole Operational & Receipt Authority
- **Context:** Multi-tenant production operations require ACID transactions, strict tenant Row-Level Security (RLS), optimistic concurrency controls, and tamper-evident audit trails.
- **Decision:** PostgreSQL (via Supabase) is the sole authoritative system of record.
- **Adopted Elements:**
  - Row-Level Security (RLS) keyed on `workspace_id` enforcing zero cross-tenant leakage.
  - Optimistic concurrency control via `state_version` and `expected_state_sha256` Compare-And-Swap (CAS) headers.
  - Cryptographic receipt tables (`cae.receipt`) storing immutable, signed hashes of all gate decisions, evaluations, and releases.
- **Rejected Elements & Boundaries:**
  - No client, agent, or microservice may mutate state outside of typed backend operations.
  - Agent completion text is never accepted as completion proof without verified database receipts.

---

### 3.5 Decision 5: OKF as Curated Knowledge Exchange Layer
- **Context:** Editorial intelligence, brand guidelines, guest biographical profiles, and domain taxonomies require structured, human-readable representations.
- **Decision:** Google Open Knowledge Format (OKF) is adopted as the curated knowledge representation and exchange format.
- **Adopted Elements:**
  - Portable Markdown files with structured YAML frontmatter.
  - Progressive disclosure linking (`concepts/`, `entities/`, `sources/`).
  - Standardized knowledge ingestion into RAG and JIT execution capsules.
- **Rejected Elements & Boundaries:**
  - OKF is **not** an operational transactional database.
  - Ephemeral execution state, candidate pools, and mutable program states must not be written as OKF files.

---

### 3.6 Decision 6: Rejection of Redis as Canonical State/Knowledge Authority
- **Context:** Redis Iris provides in-memory vector indexing and context engine capabilities.
- **Decision:** Explicitly **REJECT** Redis as a canonical state, receipt, or knowledge authority.
- **Adopted Elements:**
  - Redis is relegated to an **optional, ephemeral cache** (rate limiting token buckets, transient session caches, WebSocket pub/sub fan-out).
- **Rejected Elements & Boundaries:**
  - Redis cannot be a hard runtime dependency for core CAE execution.
  - No durable state, candidate pool, or receipt may reside exclusively in Redis.
  - If Redis is unavailable or unconfigured, CAE must operate fully and correctly against PostgreSQL.

---

## 4. Cross-Cutting Invariants & Anti-Framework Collapse Rules

1. **Four Authority Lanes**: `HUNTER`, `ANALYST`, `COMPOSER`, and `COMMANDER` remain strictly separated. No framework adapter may collapse these lanes into a single prompt or monolithic loop.
2. **Passive, Flat Canonical Skills**: Zero skill-to-skill invocation. Skills remain flat transformations invoked exclusively by the orchestrator.
3. **Typed CAE Operations as Mutation Boundary**: All state mutations and receipt emissions must occur through typed Python/SQL operations.
4. **Substrate Independence**: CAE domain logic and invariants must remain decoupled from Pi or any specific runtime engine, allowing runtime substrate replacement without domain model changes.

---

## 5. Verification & Acceptance Standard

This ADR is satisfied and proven in the codebase by:
1. `tests/cae` and `tests/pipeline` verifying that domain models and workflow graphs execute independently of external framework storage.
2. `tests/relational_intelligence` verifying that workspace isolation is enforced by PostgreSQL RLS, not local folder conventions.
3. `tests/collision_intelligence` verifying that candidate evaluation, falsification, and portfolio synthesis follow four-lane separation and emit verifiable receipts.
