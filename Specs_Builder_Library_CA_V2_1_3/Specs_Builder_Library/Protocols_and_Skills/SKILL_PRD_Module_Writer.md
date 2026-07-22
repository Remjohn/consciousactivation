# SKILL: PRD Module Writer
# Version: 1.0
# Date: 2026-05-06
# Status: Source of Truth
# Purpose: Governs the writing of all CCP modular PRD documents (PRD-01 through PRD-09)

---

## 1. Task Definition

You are writing a **modular PRD module** for the Conscious Coaching Platform (CCP). Each module is a standalone document that covers one environment or capability area. It must be architecturally precise, free of superseded concepts, and within strict word count boundaries.

**Output:** One `.md` file saved to `docs/prd/modules/PRD_0X_[Name].md`

---

## 2. Mandatory Pre-Write Loading Sequence

Before writing any word of the PRD module, you MUST load and read the following files in this exact order. Do not skip or summarize. Actually read them.

### Step 1: Load the Router
- `docs/prd/modules/PRD_INDEX.md` — identify the module's scope, cross-references, and source documents

### Step 2: Load the Evolution Timeline (The Discernment Map)
- `docs/prd/evolution_timeline.md` — read the FULL "What Went Up," "What Went Down," and "PRD Writing Rules" sections. You will be checked against all 10 rules.

### Step 3: Load the Source Documents
- Load EVERY source document listed in the PRD_INDEX cross-reference table for this module
- For each source document, read at minimum the first 200 lines (purpose, core claims, key architecture)
- If the module involves primitives, also load `Perceptual_Primitives_Architecture.md` and `Primitive_Conscious_Orchestration_Architecture.md`

### Step 4: Load PRD-01 for Constants
- `docs/prd/modules/PRD_01_CCP_Platform_Strategy.md` — read Section 6 (Invisible App Doctrine) and Section 7 (Platform Architecture Principles). Every module must be compatible with these.

### Step 5: Load CAU Registry (if applicable)
- `Conscious Architect University/cau_master_curriculum_registry.md` — check if this module maps to any CAU track or course

---

## 3. Hard Constraints

### 3.1 Word Count Boundaries

| Metric | Value |
|---|---|
| **Floor** | 4,800 words |
| **Ceiling** | 5,400 words |
| **Target** | 5,100 words |
| **Measurement** | PowerShell: `($content -split '\s+' \| Where-Object { $_.Length -gt 0 }).Count` |
| **YAML frontmatter** | Included in count |
| **Verification** | MUST run word count script BEFORE declaring module complete |

If the first draft is under 4,800: you have failed to provide sufficient architectural depth. Expand the weakest sections with content from the source documents you were supposed to read.

If the first draft is over 5,400: you have been verbose. Cut filler, merge redundant sections, tighten prose.

### 3.2 Evolution Timeline Compliance (11 Rules)

The following rules are NON-NEGOTIABLE. Violation of any single rule invalidates the entire module:

1. **NEVER reference Trivianar as a standalone feature.** It is absorbed. Say "Conscious Reactions (which absorbed Trivianar game mechanics)" if needed.
2. **NEVER reference the $16.95/$39.95/$49.95 pricing.** Current pricing: $0 → $29/mo → $99/mo.
3. **NEVER center live roleplay.** De-centered. Center = async Skill Ladder.
4. **NEVER reference calendar-gated progression.** It is biometric-gated.
5. **ALWAYS distinguish Meaning Plane from Experience Plane** when discussing primitives.
6. **ALWAYS reference the 4 Skill Surfaces** (Law28, Webinar, Networking OFAP, Social Co-Creations).
7. **Advocate Ledger, Whale Slider, Crucible Filter** → backlogged. Reference only as deferred/future.
8. **When citing MCDA features**, always note Era 3 status (Active, Absorbed, Deferred, Retained).
9. **Two client touchpoints ONLY**: AFFiNE Dashboard + Telegram. No separate portals/apps/studios.
10. **Every coaching session self-translates** into content assets and Brand DNA/RNA refinement. Never describe content creation as a separate workflow.
11. **NEVER reference JV, Joint Venture, or partner-driven distribution.** Growth is through Silent Referral (participation-driven). Founding Partners are early adopters, not distributors.

### 3.3 Structural Constraints

- **YAML frontmatter is mandatory** — must include: type, module, title, author, date, status, version, dependencies, source_documents, active_primitives (if applicable), capability_areas
- **Section numbering is mandatory** — `## 1.` through `## N.`
- **Tables are preferred** over bullet lists for structured data (family maps, workflow maps, risk matrices)
- **Code blocks** for schemas, pipeline sequences, and YAML examples
- **Footer line is mandatory**: `*This document is one of 9 modular PRD modules. Consult PRD_INDEX.md for the complete module registry, cross-reference tables, and agent loading protocol.*`

---

## 4. Section Template

Every PRD module MUST contain the following sections. Minimum word guidance is per-section to prevent front-loading all depth into Section 1 and leaving later sections skeletal.

| Section | Title Pattern | Min Words | Purpose |
|---|---|---|---|
| **§1** | The Architectural Claim / Purpose | 300 | What this module governs. Why it exists. What problem it solves. |
| **§2** | Core Architecture / Model | 600 | The primary model, framework, or pipeline this module introduces. Diagrams, tables, schemas. |
| **§3** | Schema / Registry / Data Contracts | 500 | The data structures, YAML schemas, API contracts, or configuration schemas that govern this module's domain. |
| **§4** | Key Architectural Correction | 400 | What changed from Era 1/2 to Era 3. What the old assumption was. What the current truth is. Prevents drift. |
| **§5** | Deep Mechanism / Theory | 500 | The deeper theory that justifies the architecture. Not just "what" but "why this way and not another way." |
| **§6** | Implementation / Biology / Stack | 400 | How this connects to the actual tech stack (FastAPI, DSPy, Pydantic, Redis, PostgreSQL, NIM, Skia, Telegram). |
| **§7** | Workflow Integration | 400 | How this module connects to other modules. The handoffs. The pipeline stages. |
| **§8** | Orchestration / Self-Translation | 400 | How this module serves the Invisible App Doctrine. What the coach sees vs. what runs behind. |
| **§9** | Validation & Quality Gates | 400 | Pydantic gates, metrics, fatality conditions, receipt architecture. |
| **§10** | Risk Mitigation | 300 | Module-specific risks and mitigations. Not generic. |

**Total minimum from section floors: ~4,200 words.** The remaining ~600-1,200 words should be distributed across sections that need more depth for this specific module.

**Sections may be renamed** to fit the module's domain (e.g., §5 in PRD-03 might be "The CMF Pipeline Phases" instead of "Deep Mechanism"). But the *function* of each section must be preserved.

---

## 5. Anti-Laziness Enforcement

### ⚠️ THIS MODULE IS CONSIDERED FAILED IF:

1. **You did not read the source documents.** If your module contains claims that contradict the source documents listed in PRD_INDEX, you have failed.
2. **Word count is outside 4,800–5,400.** No exceptions. Verify before declaring complete.
3. **Any Evolution Timeline rule is violated.** Grep the output for: "Trivianar" (standalone), "$16.95", "$39.95", "$49.95", "tripwire", "Crucible Onboarding Filter" (as active), "calendar-gated", "roleplay" (as center). Any hit = failure.
4. **Section 9 or 10 contains generic content.** Quality gates and risks must be specific to THIS module's domain, not copy-pasted from PRD-01.
5. **The Invisible App Doctrine is absent.** Every module must explicitly address how its domain serves the two-touchpoint architecture (AFFiNE + Telegram).
6. **Self-Translation is absent.** Every module must explain how coaching sessions in its domain auto-produce content assets and Brand DNA refinement.
7. **Any section is under its minimum word floor.** Each section must carry its own weight.
8. **Tables are missing where structured data exists.** Family maps, workflow stages, risk matrices, schema fields — these must be tables, not prose.

### Anti-Drift Protocol

- After writing §5, re-read the Evolution Timeline "PRD Writing Rules" section before continuing.
- After writing §8, run a mental grep for all 10 Evolution Timeline rules against what you've written so far. Fix violations before continuing.
- After the full draft, run the word count script. If under 4,800, identify which sections are under their floor and expand from source documents.

---

## 6. Post-Write Verification Checklist

Run this checklist BEFORE declaring the module complete. Every box must pass.

```
STRUCTURAL CHECKS
[ ] YAML frontmatter present with all mandatory fields
[ ] All 10 sections present (renamed is OK, function preserved)
[ ] Footer line present
[ ] Section numbering is sequential (## 1. through ## 10.)

WORD COUNT
[ ] Total word count: _____ (must be 4,800–5,400)
[ ] Word count verified via PowerShell script

EVOLUTION TIMELINE COMPLIANCE
[ ] Grep for "Trivianar" — zero standalone references (absorbed references OK)
[ ] Grep for "$16.95" / "$39.95" / "$49.95" / "tripwire" — zero hits
[ ] Grep for "Crucible Onboarding Filter" as active — zero hits
[ ] Grep for "calendar-gated" — zero hits
[ ] Grep for "roleplay" as center/primary/flagship — zero hits
[ ] Pricing references use $0 → $29/mo → $99/mo only
[ ] 4 Skill Surfaces referenced where applicable
[ ] Meaning/Experience plane distinction maintained

INVISIBLE APP DOCTRINE
[ ] Two-touchpoint architecture (AFFiNE + Telegram) referenced
[ ] Backend sophistication described as invisible to coach
[ ] Self-Translation Principle addressed

ANTI-SLOP
[ ] No section is under its minimum word floor
[ ] Tables used for all structured data
[ ] Risk mitigations are module-specific, not generic
[ ] Quality gates are measurable, not aspirational
```

---

## 7. Execution Protocol

### For Each Module:

1. **Load** — Follow §2 (Mandatory Pre-Write Loading Sequence) exactly
2. **Draft** — Write the full module following §4 (Section Template), targeting 5,100 words
3. **Verify Word Count** — Run the PowerShell count script
4. **Verify Compliance** — Run §6 (Post-Write Verification Checklist)
5. **Fix** — Address any failures found in verification
6. **Re-verify** — Run word count and checklist again
7. **Declare Complete** — Only after all checks pass

### Word Count Script

Save to `docs/prd/modules/count.ps1` and run after each module:

```powershell
$files = Get-ChildItem "d:\Work\The Conscious Coaching Factory\docs\prd\modules\PRD_*.md"
foreach ($f in $files) {
    $c = [IO.File]::ReadAllText($f.FullName)
    $w = ($c -split '\s+' | Where-Object { $_.Length -gt 0 }).Count
    $status = if ($w -ge 4800 -and $w -le 5400) { "PASS" } elseif ($w -lt 4800) { "UNDER" } else { "OVER" }
    Write-Host "$($f.BaseName) : $w words [$status]"
}
```

---

## 8. Module-Specific Guidance

### PRD-01: Platform Strategy
- Heaviest on §1 (identity), §2 (Voice DNA), §6 (Invisible App Doctrine)
- Must include CAU integration and Founding Partner JV

### PRD-02: CCF Content Factory  
- Heaviest on §2 (Trigger-First pipeline), §3 (Content Trinity schema), §5 (edge extraction theory)
- Self-Translation: coaching voice notes → CCF scripts → Content Trinity assets

### PRD-03: CMF Media Factory
- Heaviest on §2 (narrative → cinematic → sonic pipeline), §3 (VDP/VCP schemas), §6 (Skia/SAM3 stack)
- Self-Translation: scripts → visual compositions → sonic phases → export-ready media

### PRD-04: CVE Experience Design
- Heaviest on §2 (Communication Skill Ladder), §3 (Experience Primitive schemas), §5 (Voice-First doctrine)
- Must cover all 4 async skill surfaces with equal depth

### PRD-05: CBCS Law28
- Heaviest on §2 (4-Engine coaching system), §3 (28-Command suite), §4 (biometric-gated progression)
- Must cover Sunday Postcard, accountability architecture, seasonal challenge recursion

### PRD-06: Conscious Reactions
- Heaviest on §2 (Solo/Debate/Jury/Tier List modes), §5 (viral thresholds), §7 (Trivianar absorption)
- §4 MUST explicitly document Trivianar absorption — this is the module where the old concept lives as absorbed mechanics

### PRD-07: V2WS Webinar
- Heaviest on §2 (YOLO/Interactive modes), §3 (slide generation schema), §5 (teaching-while-selling theory)
- Self-Translation: webinar recordings → CMF clips → coaching content

### PRD-08: Conscious Primitives
- Heaviest on §2 (Meaning/Experience planes), §3 (YAML registry schemas), §5 (coalition formation theory)
- Must include basis definitions, vector operations, biological hierarchy

### PRD-09: CPSC Silent Referral
- Heaviest on §2 ($29/$99 pricing architecture), §5 (Silent Referral theory), §7 (OFAP, Church vertical)
- §4 MUST explicitly document the tripwire pricing replacement and Advocate Ledger deferral

---

## 9. Fatality Conditions

The module is declared FATAL and must be rewritten from scratch if:

- Word count is below 4,000 (indicates fundamental scope failure)
- More than 2 Evolution Timeline rules are violated (indicates source documents were not read)
- Any section is completely absent (indicates structural failure)
- The Invisible App Doctrine is not referenced anywhere (indicates architectural disconnection)

---

## 10. Completion Receipt

After finishing a module, produce this receipt:

```
MODULE: PRD-0X [Name]
WORD COUNT: [number] [PASS/UNDER/OVER]
SECTIONS: [count]/10
EVOLUTION TIMELINE VIOLATIONS: [count] [list if any]
INVISIBLE APP DOCTRINE: [PRESENT/ABSENT]
SELF-TRANSLATION: [PRESENT/ABSENT]
SOURCE DOCUMENTS READ: [count]/[total listed in PRD_INDEX]
STATUS: COMPLETE / NEEDS REVISION
```
