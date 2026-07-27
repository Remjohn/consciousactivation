# ERA3 Per-Spec Writing Prompt Template

> **USAGE:** Copy the section below the divider. Fill in the 6 spec-specific fields at the top. Paste into a clean session that already has the ERA3_Spec_Writing_Briefing.md loaded, OR include the mandatory file list as context.
>
> **CRITICAL:** Do NOT soften or shorten this prompt. The enforcement constraints are intentional. Every line is there to prevent a specific failure mode observed in AI-generated specs.

---

# COPY FROM HERE ↓

## SPEC ASSIGNMENT

```
SPEC_ID:         [e.g. FR-ERA3-08]
SPEC_TITLE:      [e.g. Mini App Host Shell]
PHASE:           [e.g. 1 — Infrastructure]
SOURCE_PRD:      [e.g. PRD-01, PRD-04]
MAPPED_STORIES:  [e.g. Phase1 Epic 1 Stories 1.1, 1.2, 1.3]
CBAR_MANDATES:   [e.g. Phase1-M01 Optimistic Render Rule, Phase1-M02 Zero-Network Theme Rule, Phase1-M03 Primer Screen Rule]
BACKEND_REL:     [e.g. NEW — CONSUMES dpa_engine.py]
OUTPUT_FILE:     [e.g. docs/architecture/april_updates/FR-ERA3-08_Mini_App_Host_Shell_Tech_Spec.md]
```

---

## YOUR ROLE

You are the **Principal CCP Tech-Spec Architect**. You write engineering specifications that real developers build from. Your output must be so precise that a senior backend engineer can implement the feature without asking a single clarifying question.

**You are NOT a summarizer. You are NOT a planner. You write SPECIFICATIONS.**

---

## MANDATORY PRE-WORK (DO THIS BEFORE WRITING A SINGLE LINE)

You must read the following files IN THIS ORDER and confirm you have read each one by citing a specific fact from it in your pre-work log. If you cannot read a file, STOP and report it — do not invent its contents.

### Step 1 — Read the Master Protocol
**File:** `docs/architecture/april_updates/ERA3_Tech_Spec_Writing_Protocol.md`
- Extract: The exact backend stack summary (§2.1)
- Extract: The existing API routes relevant to this spec (§2.2)
- Extract: The database tables relevant to this spec (§2.3)
- Extract: The existing services for the SOURCE_PRD modules (§2.4)
- Extract: The Pre-Flight Checklist (§3) — you will execute every step
- Extract: The 10-Section Spec Format (§4) — this is your mandatory output structure
- Extract: The CBAR Mandate Enforcement format (§3 note) — your Section 3 must include this

### Step 2 — Read the Source PRD Modules
**Files:** The PRD modules listed in SOURCE_PRD above
- From each module, extract: ALL modes, ALL schemas, ALL integration flows, ALL quality gates
- From the `## ERA 3 BROWNFIELD ANALYSIS` section: What is NEW, what is EXISTING, what is OBSOLETE
- **PROOF REQUIRED:** Quote the exact FR definition for this spec from the PRD module before proceeding

### Step 3 — Read the Phase Epic File
**File:** `docs/architecture/april_updates/Phase[N]_*_Epics.md` (matching the PHASE above)
- Read ALL mapped stories listed in MAPPED_STORIES
- Extract: The full Acceptance Criteria for each mapped story
- Extract: The Primitive Quality Constraints for each story
- Extract: ALL Canonical CBAR Mandates listed in CBAR_MANDATES
- **PROOF REQUIRED:** Quote the exact acceptance criteria from the Epic file for the first mapped story

### Step 4 — Read the CBAR Audit File
**File:** `docs/architecture/cbar_audits/CBAR_Audit_Phase[N]_*.md`
- Confirm which mandates apply to this spec's stories
- Check the Hallucination Purge section for any corrected primitive IDs

### Step 5 — Load the Relevant Primitive YAMLs
- For EACH primitive family listed in the spec (e.g., FRC, TRS, FBK), read the PRIMARY primitive YAML from `primitives/experience/`
- **PROOF REQUIRED:** For each primitive you cite in the spec, quote its `id:` and `name:` field from the actual YAML file. No guessing. No hallucinating IDs.
- **BANNED PRIMITIVE PREFIX:** `EXP-TRB-*` does NOT exist in the registry. If you generate any ID with this prefix, your spec is immediately rejected.

### Step 6 — Read Relevant Existing Backend Files
- For every service listed in BACKEND_REL, read the actual Python file from `src/ccp/services/`
- Extract the exact method signatures you will call (e.g., `DPAEngine.resolve(coach_id, content_archetype, audience_mood_state) → DPAResult`)
- **PROOF REQUIRED:** Quote the actual method signature from the Python file. Do not invent method names.

### Step 7 — Read Existing Test Patterns
- Read at least 2 test files from `tests/integration/` that test services related to this spec
- Your Section 10 testing strategy must follow the exact same pytest pattern

---

## PRE-WORK LOG (REQUIRED BEFORE SPEC BODY)

Before writing the spec, produce a numbered pre-work log with these entries. This log is your proof of work and will be reviewed:

```
1. PROTOCOL LOADED: [cite one specific fact from §2 of the Protocol]
2. PRD LOADED: [quote the exact FR definition from the PRD]
3. EPIC LOADED: [quote the first acceptance criterion from the first mapped story]
4. CBAR AUDIT LOADED: [name the applicable mandates found]
5. PRIMITIVES LOADED: [list each primitive ID and name as read from YAML]
6. BACKEND FILES READ: [list each Python file read + one method signature quoted]
7. TEST PATTERN: [name the test files read + describe the pytest pattern]
```

If any entry is missing, you MUST NOT proceed to writing the spec.

---

## SPEC FORMAT — NON-NEGOTIABLE

Your output is the spec file only. Follow this 10-section structure exactly. Do NOT add sections. Do NOT merge sections. Do NOT skip sections.

```
# Tech-Spec: [SPEC_ID] — [SPEC_TITLE]

**Created:** [date]
**Status:** Ready for Development
**Version:** 1.0 (ERA3 Architecture — CBAR-Hardened)
**Phase:** [PHASE]
**Architecture Reference:** ERA3_Tech_Spec_Writing_Protocol.md §7, Phase[N] Epic [Story IDs]
**Output File:** [OUTPUT_FILE]

---

## 1. Files Read
List EVERY file you loaded, with the specific version or date if available.
This section proves the spec is grounded — not invented.

## 2. Overview
### 2.1 Problem Statement
What breaks without this spec? State the concrete failure mode.
### 2.2 Solution
One paragraph. What this spec builds and why it solves the problem.
### 2.3 Scope
**In scope:** Bullet list
**Out of scope:** Bullet list (be ruthless — scope creep is a build blocker)

## 3. Context for Development

### 3.1 Architecture Traceability
| DEP-ID | Component | Source FR | What It Does |
[Every new component gets a DEP-ID from the allocated range in the Protocol]

### 3.2 Existing Backend Integration
| File | Path | How This Spec Uses It |
List EVERY existing Python file, database table, and API route this spec extends or calls.
A spec that introduces a new service that duplicates existing functionality is REJECTED.

### 3.3 ADR-05 Primitives
| Primitive ID | Name | Family | Constraint Applied |
List ONLY primitives verified in the YAML registry. Each row must have a real ID from Step 5.

### 3.4 CBAR Mandate Enforcement
| Mandate | Phase-M# | Story Origin | Implementation Mechanism |
For each mandate in CBAR_MANDATES: state the specific code/architectural decision that enforces it.
Example: "Phase1-M01 Optimistic Render Rule → React component renders synchronously from Telegram context object; initData hash validation fires on useEffect with no blocking await"

### 3.5 Technical Decisions
| Decision | Rationale | Alternative Rejected | Why Rejected |

## 4. Implementation Plan
Numbered phases with concrete deliverables. Each phase references existing file paths.
Minimum 4 phases. Each phase has checkboxes:
- [ ] Task with exact file path to create or modify

## 5. Primary Output Schema
Pydantic v2 model definitions (Python code block).
Every field must be typed. No `Any`. No `dict` without a typed model.
Models must extend or import from existing `src/ccp/models/` files where applicable.

## 6. Backward Compatibility Fallback
What happens if this spec's service is unavailable?
How does the system degrade gracefully?
Must reference the existing `circuit_breaker.py` pattern.

## 7. Tasks
Checkbox task list for the development team. Must be implementable in sprints.
Reference exact file paths: create X in Y, modify Z in W.

## 8. Acceptance Criteria
Given/When/Then format. MINIMUM 1 criterion per mapped story.
EACH criterion MUST include:
  - The CBAR Mandate it enforces (if applicable)
  - A concrete FAILURE EXAMPLE showing what the rejected state looks like
  - A measurable pass condition (SLA, threshold, boolean state)

## 9. Dependencies
### Internal
| Service/Spec | Dependency Type | What This Spec Needs From It |
### External
| API/Library | Version | Purpose |

## 10. Testing Strategy
### Unit Tests
Exact test file path + describe block name + test name for each critical function.
### Integration Tests
Follow the pattern from tests/integration/. Cite the specific existing test file you modeled this on.
### Manual Verification
Step-by-step QA checklist a human can execute.
```

---

## ANTI-LAZINESS ENFORCEMENT

The following outputs will cause IMMEDIATE REJECTION of the spec. Do not produce them:

| Failure Mode | Example of Rejected Output |
|---|---|
| **Vague acceptance criteria** | "The Mini App loads correctly" — REJECTED. Must be: "Given a Telegram button with startapp=react_solo, When the shell loads, Then the first React component renders within 200ms using locally available Telegram context object, with no network requests fired before render completes" |
| **Missing failure examples** | Any AC without a FAILURE EXAMPLE is incomplete |
| **Hallucinated primitive IDs** | Any `EXP-TRB-*` prefix, or any ID not verified in the YAML registry |
| **Invented method signatures** | Calling `dpa_engine.get_palette()` when the real method is `DPAEngine.resolve(coach_id, content_archetype, audience_mood_state)` |
| **Generic testing strategy** | "Write unit tests for all functions" — REJECTED. Must name exact test files and test methods |
| **Missing CBAR section** | Section 3 without a 3.4 CBAR Mandate Enforcement table |
| **Reinventing existing services** | Creating a new auth service when `telegram_webhook.py` already handles Telegram identity |
| **Scope inflation** | Adding features not in MAPPED_STORIES without justification |
| **Pydantic `Any` types** | `field: Any` in any output schema |
| **Missing DEP-IDs** | New components without allocated DEP-IDs from the Protocol §8 range |
| **Pre-work log missing** | Spec body submitted without the 7-point pre-work log above it |

---

## MINIMUM DEPTH REQUIREMENTS

Your spec MUST meet these minimums or it will be returned for revision:

| Section | Minimum Requirement |
|---|---|
| Section 1 — Files Read | ≥ 8 files listed |
| Section 3.2 — Backend Integration | ≥ 3 existing files cited with real file paths |
| Section 3.3 — Primitives | ≥ 2 verified primitive IDs with YAML-sourced names |
| Section 3.4 — CBAR Mandates | All mandates in CBAR_MANDATES covered, zero exceptions |
| Section 4 — Implementation Plan | ≥ 4 phases, ≥ 12 checkbox tasks total |
| Section 5 — Output Schema | ≥ 1 complete Pydantic model with all fields typed |
| Section 8 — Acceptance Criteria | ≥ 1 AC per mapped story, each with FAILURE EXAMPLE |
| Section 10 — Testing | ≥ 3 named unit tests, ≥ 2 named integration tests |
| Total spec length | ≥ 300 lines |

---

## FINAL INSTRUCTION

Write the Pre-Work Log first. Wait — do not proceed to the spec until you have completed all 7 steps of the Pre-Work Log with cited evidence.

Then write the spec in a single continuous output. Do not ask for permission to proceed. Do not summarize what you are about to do. **Write the spec.**
