# Era 3 Tech Spec Writing Protocol — Implementation Documentation

> [!CAUTION]
> **This document is the MANDATORY protocol for writing ALL Era 3 Tech Specs. No spec may be written without following every step.**

---

## 1. Completed File Operations

### ✅ FR Files Merged into PRD Modules
All 9 functional requirements files have been **appended** to their corresponding full PRD modules under `## ERA 3 BROWNFIELD ANALYSIS`. Single source of truth per module.

| Merged Into | Location |
|---|---|
| PRD-01 through PRD-09 | `docs/prd/modules/PRD_XX_*.md` |

**Deleted:** `docs/prd/functional_requirements/FR_*.md` (9 files removed — content preserved in modules)

### ✅ Invalid Specs Deleted
All 4 specs written without proper PRD module loading have been deleted. **Zero specs exist.** Clean slate.

---

## 2. Existing Backend Architecture (MUST BE REFERENCED)

> [!IMPORTANT]
> **Before writing ANY spec, you MUST understand what already exists.** The CCP has a fully built Python/FastAPI backend with 201 services, 45 model files, 17 pipelines, 17 agents, 88 integration tests, and existing database schemas. New specs EXTEND this — they don't reinvent it.

### 2.1 Stack Summary

| Layer | Technology | Location |
|---|---|---|
| **API Gateway** | FastAPI (Python) | `src/ccp/api/main.py` |
| **Primary Database** | Supabase (PostgreSQL) with RLS | `src/ccp/scripts/setup_supabase.py` |
| **Graph Database** | Neo4j (Context Premises) | `src/ccp/scripts/setup_neo4j.py`, `src/ccp/services/neo4j_graph_manager.py` |
| **Cache / Dedup** | Redis (in-memory, planned migration) | Used in `telegram_webhook.py`, `finding_source_cache.py`, etc. |
| **Message Router** | Telegram Webhook → VidyeRouter | `src/ccp/api/telegram_webhook.py` → `src/ccp/agents/vidye_router.py` |
| **Orchestration** | Pi Extension Harness (11 extensions) | `src/ccp/services/pi_extension_harness.py` |
| **Pipeline Framework** | Custom Python pipelines | `src/ccp/pipelines/` (17 pipelines) |
| **Agent Framework** | Custom Python agents | `src/ccp/agents/` (17 agents) |
| **Visual Rendering** | Skia Renderer (sidecar) | `src/ccp/sidecars/skia-renderer/` |
| **Branding** | DPA Engine (FR-CA11-15) | `src/ccp/services/dpa_engine.py` |
| **Model Validation** | Pydantic v2 | `src/ccp/models/` (45 model files) |
| **Testing** | pytest (88 integration tests) | `tests/integration/` |
| **Frontend (Tierlist)** | Vite + React (JSX) | `tools/tierlist-app/` |
| **Telegram Bot (Tierlist)** | Python bot | `tools/telegram-tierlist-bot/` |
| **Coach Scaffolding** | CLI script | `src/ccp/scripts/scaffold_coach.py` |

### 2.2 Existing API Routes

| Route | Handler | Purpose |
|---|---|---|
| `POST /api/telegram/webhook` | `telegram_webhook.py` | All Telegram messages → VidyeRouter |
| `POST /api/sacred-audio/upload` | `sacred_audio.py` | Coach voice recording ingestion |
| `POST /api/notion/webhook` | `notion_webhook.py` | Notion status change triggers |
| `GET/POST /api/canvas/*` | `canvas_api.py` | Canva visual composition |
| `GET /health` | `main.py` | Health check + coach ID |

### 2.3 Existing Database Schema (PostgreSQL/Supabase)

| Table | Purpose | Key Fields |
|---|---|---|
| `receipt_chain` | Immutable audit log (ADR compliance) | `receipt_id`, `agent_id`, `action`, `asset_id`, `person_id` |
| `asset_registry` | Universal Asset IDs | `asset_id`, `asset_type`, `coach_acronym` |
| `person_registry` | Person IDs (coach + client) | `person_id`, `telegram_user_id`, `person_type` |
| `cultural_memory_map` | 7-layer CMM (DEP-ENG-023) | `cmm_id`, `coach_id`, `entries` (JSONB) |
| `coach_story_archive` | Hartian 5-element stories (DEP-ENG-024) | `story_id`, `hartian_schema` (JSONB) |
| `humor_mechanism_registry` | Boredom Ban compliance | `registry_id`, `entries` (JSONB) |
| `context_performance_registry` | Context vs performance (DEP-ENG-045) | `registry_id`, `context_selections` (JSONB) |
| `standing_trigger_library` | Research findings (quality ≥0.65) | `entry_id`, `trigger_category_id`, `quality_score` |
| `content_performance` | Script humor tagging + validation verdicts | `content_id`, `humor_mechanism_tag` (JSONB) |
| `resolved_palettes` | DPA palette audit trail | `resolved_palette_id`, `bhcs`, `brand_hue_used` |

**Storage Buckets:** `sacred-audio` (private), `voice-notes` (public), `coach-photos` (public), `visual-assets` (public)

### 2.4 Key Existing Services (by PRD Module)

#### PRD-01: Platform Strategy
| Service | File | What It Does |
|---|---|---|
| `single_tenant_deployment_service.py` | services/ | ADR-01 tenant isolation |
| `affine_sync.py` | services/ | AFFiNE ↔ CCP sync |
| `affine_workspace_provisioner.py` | services/ | Coach workspace creation |
| `affine_client_workspace.py` | services/ | Client workspace management |
| `coach_soul_adapter.py` | services/ | Voice DNA Core loading |
| `dpa_engine.py` | services/ | DPA branding engine (FR-CA11-15) |

#### PRD-02: CCF Content Factory
| Service | File | What It Does |
|---|---|---|
| `content_machine.py` | services/ | Content generation orchestration |
| `research_synthesis_protocol.py` | services/ | CRAL research pipeline |
| `psych_routing_engine.py` | services/ | Mood/archetype routing |
| `tiar_adapter.py` | services/ | Archetype adapter |
| `semantic_affinity_guard.py` | services/ | Blocks unsafe content combos |
| `boredom_ban_enforcer.py` | services/ | Humor uniqueness enforcement |

#### PRD-03: CMF Media Factory
| Service | File | What It Does |
|---|---|---|
| `abel_vcb_generator.py` | services/ | Visual prompt generation |
| `canvas_composition_service.py` | services/ | Visual layout engine |
| `course_video_cmf.py` | services/ | Video CMF pipeline |
| `format_governance_engine.py` | services/ | Format selection |
| `saliency_analysis_service.py` | services/ | Visual attention analysis |
| Skia Renderer | sidecars/ | Hardware-accelerated rendering |

#### PRD-04: CVE Experience Design
| Service | File | What It Does |
|---|---|---|
| `tii_calculator.py` | services/ | Telegram Intimacy Index (6-component) |
| `dormancy_recovery_service.py` | services/ | Comeback logic |
| `soundboard_service.py` | services/ | Sonic palette |
| `habit_architecture.py` | services/ | Habit loop management |
| `engagement_feedback.py` | services/ | Feedback engine |

#### PRD-05: CBCS Law28
| Service | File | What It Does |
|---|---|---|
| `trait_scoring_engine.py` (47KB!) | services/ | Biometric scoring (FR61) |
| `scorecard_emitter.py` | services/ | Score card generation |
| `change_talk_vault.py` | services/ | DARN-CAT commitment tracking |
| `spt_stage_engine.py` | services/ | Social Penetration stage |
| `identity_anchor_protocol.py` | services/ | 72-hour identity anchor |
| `counterfactual_activation.py` | services/ | Counterfactual window |
| `learning_path_builder.py` | services/ | Challenge path construction |
| `dynamic_journaling_engine.py` | services/ | Journaling prompts |

#### PRD-06: Conscious Reactions
| Service | File | What It Does |
|---|---|---|
| `trivianar_engine_service.py` | services/ | **EXISTING** reaction engine (legacy Trivianar name) |
| Tierlist App | `tools/tierlist-app/` | **EXISTING** Vite+React tierlist frontend |
| Tierlist Bot | `tools/telegram-tierlist-bot/` | **EXISTING** Telegram bot for tierlist |

#### PRD-07: V2WS Webinar
| Service | File | What It Does |
|---|---|---|
| `v2ws_interactive_service.py` | services/ | Interactive webinar logic |
| `v2ws_yolo_service.py` | services/ | Automated webinar mode |
| `webinar_brief_generator.py` | services/ | Webinar brief creation |
| `session_to_course.py` | services/ | Webinar → course conversion |

#### PRD-08: Conscious Primitives
| Service | File | What It Does |
|---|---|---|
| `primitives/` directory | workspace root | **201 YAML primitives already codified** |
| No query service yet | — | **THIS IS WHAT FR-ERA3-06 BUILDS** |

#### PRD-09: CPSC Silent Referral
| Service | File | What It Does |
|---|---|---|
| `conversion_sequence_router.py` | services/ | Conversion routing |
| `lead_capture_service.py` | services/ | Lead capture |
| `offer_tier_governor.py` | services/ | Tier access control |
| `challenge_funnel_builder.py` | services/ | Challenge → conversion path |
| `coping_invitation_engine.py` | services/ | Invitation timing |

#### Cross-System (PRD-01 §7)
| Service | File | What It Does |
|---|---|---|
| `receipt_chain.py` | core/ | Immutable audit trail |
| `asset_id.py` | core/ | Universal Asset ID generation |
| `circuit_breaker.py` | core/ | Failure protection |
| `cross_system_intelligence_service.py` | services/ | Cross-module data flow |
| `memory_tier_promotion_service.py` | services/ | Memory tier management |
| `scheduled_monitor_service.py` | services/ | FR15 cron monitoring |
| `guardian_agent.py` | agents/ | CA-0 pre-production intelligence |
| `morgan_orchestrator.py` (37KB) | agents/ | Main content orchestration agent |
| `vidye_router.py` | agents/ | Telegram message → agent router |

### 2.5 Existing Frontend Infrastructure

| App | Technology | Location | Status |
|---|---|---|---|
| Tierlist App | Vite + React (JSX) | `tools/tierlist-app/` | Built, has `dist/` |
| Tierlist Bot | Python + python-telegram-bot | `tools/telegram-tierlist-bot/` | Built |
| **No Mini App shell** | — | — | **Does not exist yet** |

---

## 3. Mandatory Pre-Flight Checklist (Before Writing ANY Spec)

### Step 1: Load the PRD Module
- Read `docs/prd/modules/PRD_XX_*.md` — the FULL file including the brownfield analysis
- Extract: ALL modes, ALL schemas, ALL integration flows, ALL quality gates
- From the brownfield section: What's NEW, What's EXISTING, What's OBSOLETE

### Step 2: Load Referenced Existing Specs
- Every spec mentioned in the brownfield Section 2 must be read
- Understand what already exists so the new spec extends, not duplicates

### Step 3: Map to Existing Backend (Section 2 of THIS document)
- Identify which existing services, models, pipelines, and agents are relevant
- The spec must reference existing code files it extends or integrates with
- New endpoints must be added to the existing FastAPI app (`src/ccp/api/main.py`)
- New models must follow the existing Pydantic pattern (`src/ccp/models/`)
- New services must follow the existing service pattern (`src/ccp/services/`)

### Step 4: Load Relevant Primitives (ADR-05)
- Check the PRD module's YAML frontmatter for `active_primitives`
- Load the PRIMARY primitives for each active family from `primitives/`
- The spec must reference specific primitive IDs and their constraints

### Step 5: Determine Mini App Separation
- If the feature surfaces in Telegram as a Mini App: each distinct mode/surface gets its own spec or clearly separated module section
- Mini Apps must be independently loadable via `startapp` parameter
- Agent must be able to call each Mini App surface independently

### Step 6: Cross-Reference PRD_INDEX.md
- Check which other PRD modules have secondary references to this feature

### Step 7: Load CBAR-Hardened Epic & Mandates
- Read the relevant Phase Epic file: `docs/architecture/april_updates/Phase{N}_*_Epics.md`
- Extract ALL Canonical CBAR Mandates that apply to stories mapped to this spec
- Identify the specific Story IDs and their Acceptance Criteria that this spec must enforce
- Cross-reference the Primitive ID Correction Log (if present) to ensure no hallucinated primitive IDs enter the spec
- The spec MUST declare which CBAR Mandates it enforces in Section 3

> [!CAUTION]
> **33 binding CBAR Mandates exist across 5 Phases (7+7+7+7+5).** A spec that ignores its applicable mandates will be rejected at QA. Mandates are codified in the Phase Epic files — they are NOT optional guidelines.

---

## 4. The 10-Section Spec Format

```
## 1. Files Read (PRD modules + existing code files + primitives + Phase Epic file)
## 2. Overview (Problem / Solution / Scope)
## 3. Context for Development
     - Architecture Traceability (DEP-ID table)
     - Existing Backend Integration (which services/models/pipelines this extends)
     - ADR-05 Primitives (specific YAML IDs + constraints)
     - CBAR Mandate Enforcement (which mandates apply + how each is enforced)
     - Technical Decisions (with rationale)
## 4. Implementation Plan (Staged — references existing code paths)
## 5. Primary Output Schema (JSON/Pydantic — extends existing models)
## 6. Backward Compatibility Fallback
## 7. Tasks
## 8. Acceptance Criteria (each with FAILURE EXAMPLE + CBAR mandate reference)
## 9. Dependencies (internal services + external)
## 10. Testing Strategy (follows existing pytest pattern in tests/integration/)
```

> [!IMPORTANT]
> **Section 3 must include an "Existing Backend Integration" subsection** listing the exact Python files, database tables, and API routes that the new spec extends or integrates with. This prevents specs from being written in a vacuum.

> [!IMPORTANT]
> **Section 3 must include a "CBAR Mandate Enforcement" subsection** listing each applicable CBAR Mandate by Phase and number (e.g., `Phase1-M1: The Optimistic Render Rule`), the Story ID it originates from, and the specific implementation mechanism in this spec that enforces it. Section 8 Acceptance Criteria must reference the mandate being tested. A spec without this subsection will be rejected.

---

## 5. Mini App Separation Doctrine

> [!IMPORTANT]
> The Conscious Reactions family contains **4 architectural categories**: Reaction Modes (standalone Mini Apps), User Roles (entry paths within CORE), Options/Mechanics (features within CORE), and Content Creation Experiences (standalone Mini Apps with unique interactive formats). Each category has different spec and deployment implications.

### 5.1 Conscious Reactions Architecture (PRD-06)

> [!IMPORTANT]
> The 14 items in the Conscious Reactions family are NOT all the same type of thing. They fall into **4 distinct architectural categories** that determine how they are built, specced, and deployed.

#### Category A — Reaction Modes (Standalone Mini App Experiences)

These are the core reaction formats where users react to hot topics. Each is a distinct Mini App with its own UI, flow, and scoring logic.

| # | Mode | `startapp` ID | Spec | What It Is | Primary Primitives |
|---|---|---|---|---|---|
| 1 | **Solo Reaction** | `react_solo` | FR-ERA3-05a | User receives a topic briefing + 15-20s voice brief, records a constrained 2-5 min take. Scored on conviction, pacing, authority. The foundational format — requires only one person. | TRG, FRC, FBK |
| 2 | **Debate with Jury** | `react_debate` | FR-ERA3-05b | Hot topic dropped into ecosystem lane. User records a take → opens For/Against voting → peers counter-react. Creates side-taking, social identity, compilation content. Strongest silent referral mechanic. | SOC, TRG, FBK, PER |
| 3 | **Reaction Duel** | `react_duel` | FR-ERA3-05c | Two coaches react to the same topic → compared side-by-side. Async first, sync later. Sharpens performance contrast and score relevance. Strongest competitive format without needing a large group. | SOC, FBK, SFR |

#### Category B — User Roles (Entry Paths — Part of CORE Engine)

These are NOT separate Mini Apps. They are different ways users ENTER and PARTICIPATE within the reaction modes above. They are features of the **CORE engine** (FR-ERA3-05-CORE).

| Role | What It Is | Where It Lives |
|---|---|---|
| **Audience Jury** | Users enter as judges, not speakers. They vote for strongest / most convincing / most leader-like take. Lowest friction entry — eventually prompts the judge to record their own take. | CORE engine feature, activated within Debate and Duel modes |
| **Supervisor Pairing** | Users enter as accountability witness / supporter / friend supervisor. Soft pathway — observe the ecosystem value before being invited to react. Creates paired accountability dynamics. | CORE engine feature, available across all modes |
| **Vote Then React** | Receiver watches a shared reaction → votes first (low friction) → invited to record own take (deeper entry). Staircase of commitment maximizes silent referral. | CORE engine sharing/entry mechanic, triggered by any mode's share action |

#### Category C — Options / Mechanics (Features Within CORE)

These are NOT separate Mini Apps. They are behavioral mechanics that layer ON TOP of reaction modes. They are features of the **CORE engine** (FR-ERA3-05-CORE).

| Option | What It Is | Where It Lives |
|---|---|---|
| **Redemption Round** | After a poor score or debate loss, user receives guided coaching cues + a second attempt. The delta between attempts is the highest-value developmental content. Makes the system feel like a coach, not a judge. | CORE engine feature, triggered by low score in any mode |

#### Category D — Content Creation Experiences (Standalone Mini Apps)

These are completely different interactive formats — NOT reaction-to-topic experiences. Each is its own standalone Mini App with a unique content creation mechanic.

| # | Experience | `startapp` ID | Spec | What It Is | Primary Primitives |
|---|---|---|---|---|---|
| 4 | **Tierlist Authority** | `react_tierlist` | FR-ERA3-05d | Coach is presented with elements to rank, speaks choices verbally, UI dynamically updates ranking state by timestamp + category shift. Strong authority display, TikTok-native familiarity, clean benchmarking on conviction + clarity. | FBK, FRC, PRG |
| 5 | **Audience Mirror Quiz** | `react_mirror_quiz` | FR-ERA3-05e | Coach answers questions reflecting the actual concerns/beliefs/tensions of their OWN audience. Not entertainment — authority validation + audience empathy proof. Proves the system understands the coach's market, driving $99.99 Coach OS conversion. | PER, TRB, FBK |
| 6 | **Blind Rank Reveal** | `react_blind_rank` | FR-ERA3-05f | Coach makes a ranking/preference judgment BEFORE the full context is revealed, then defends it. Creates tension, unpredictability, humor, authenticity. Makes real instincts visible before overthinking. | SFR, FBK, TRG |
| 7 | **Alphabet Challenge** | `react_alphabet` | FR-ERA3-05g | Timed, letter-based recall under pressure. Coach must respond with constraint (e.g., industry concepts starting with specific letters). High energy, visible pressure, strong pacing practice. Easy scoring. | PRG, FRC, FBK |
| 8 | **Last One Standing** | `react_elimination` | FR-ERA3-05h | Elimination format — multiple options narrowed one by one. Strong side-taking, strong comment behavior, intuitive audience participation, natural tension escalation. Excellent for industry hot takes + ranking disagreements. | SOC, PRG, SFR |
| 9 | **Authority Quiz** | `react_authority_quiz` | FR-ERA3-05i | Escalating-stakes question format inspired by high-stakes quiz mechanics. Visible pressure + urgency + dramatic answer moments. Fast authority proof + answer-under-pressure speaking practice. | PRG, FBK, TRB |
| 10 | **Ranking Quiz Co-Creation** | `react_ranking_quiz` | FR-ERA3-05j | Two people or one person + audience rank, defend, challenge, and reorder items. Creates contrast + speaking pressure + opinion visibility. Very easy content extraction. | SOC, FBK, PRG |

### 5.2 Experience Primitive Family Keys

Every Mini App spec MUST declare which families govern its experience design. The 8 families (51 codified YAMLs in `primitives/experience/`):

| Key | Family | What It Governs | Example Primitives |
|---|---|---|---|
| **TRG** | Trigger & Timing | When the system speaks / stays silent / sends the topic | `Context-Aware System Triggers`, `Kairos`, `Urgent Optimism Hooks` |
| **FRC** | Friction & Ability | Reducing cost of the main action (topic → mic → done) | `B=MAP Friction Audit`, `Zero-Thought Onboarding`, `Poka-Yoke` |
| **TRS** | Trust & Status | Creating permission to engage / premium authority feel | `Visceral Hooking`, `Reflective Social Proof`, `Epic Meaning Framing` |
| **FBK** | Feedback & Scoring | Emotional + practical quality of score reveals | `RIM Feedback`, `Bring the Data Forward`, `Reflective Scoring` |
| **PRG** | Progression & Replay | Turning repeat use into visible advancement | `Discover→Master→Replay`, `Long Loops for Habit Formation`, `Hook Cycle Velocity` |
| **SOC** | Social & Referral | Converting participation into spread (vote/jury/recruit) | `Social Treasures`, `Rewards of the Tribe`, `Default to Public` |
| **SFR** | Safe Failure & Recovery | Making pressure survivable — pressure without identity damage | `Behavioral Forgiveness`, `Richter Rescue`, `Possible-Win Scarcity` |
| **PER** | Personalization & Identity | Long-term stickiness, stored value, identity accretion | `Cumulative Investment`, `Monitor Attachment`, `Reputation Graph` |

### 5.3 Other Platform Mini Apps

| Mini App | `startapp` ID | Source PRD | Spec | User Experience |
|---|---|---|---|---|
| Webinar Companion | `webinar` | PRD-07 | FR-ERA3-01 | Audience-facing webinar viewer: consumes assembled V2WS modules, syncs with coach's live/recorded presentation |
| Payment Sheet | `pay` | PRD-09 | FR-ERA3-02 | In-chat payment surface: checks tier eligibility via `offer_tier_governor`, processes Telegram/Stripe payments |
| Challenge Arena | `challenge` | PRD-05 | FR-ERA3-11 | 30-day challenge progression: streak tracking, daily prompts, XP, leaderboards, habit verification |
| Conscious Editor | `editor` | PRD-02/03 | FR-ERA3-09 | Coach reviews/edits micro-content extracted by ContentMachinePipeline before publishing |
| Score Card | `score` | PRD-04/05 | Extension | Coach's Leadership Scorecard visualization: 12-trait radar, evidence citations, developmental insights |
| Testimonial Recorder | `testimonial` | PRD-05 | FR-ERA3-19 | Client records voice/video transformation story → auto-packaged as branded social proof asset |

---

## 6. Dynamic Whitelabel Branding

Every Mini App uses the **existing** `dpa_engine.py` (FR-CA11-15):
- `DPAEngine.resolve(coach_id, content_archetype, audience_mood_state)` → `DPAResult`
- Identity tokens (locked): typography, logo, spacing from `branding.json`
- Mood tokens (dynamic): colors, gradients per archetype from PAD vectors
- **Existing model:** `src/ccp/models/ca11_models.py` — `ResolvedPalette`, `MoodPaletteColors`, `PADVector`
- **Existing table:** `resolved_palettes` in Supabase

## 7. Execution Order

> [!IMPORTANT]
> **Relationship verbs:** `NEW` = no existing backend service. `CONSUMES` = calls existing service as a client. `REPLACES` = supersedes an obsolete service. `READS` = reads existing data/files.
>
> **Pre-Flight** = what the spec writer MUST load before writing (Step 1-5 of §3).

### Phase 1 — Infrastructure (Specs 1-3)

> **CBAR Source:** [`Phase1_Infrastructure_Epics.md`](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/april_updates/Phase1_Infrastructure_Epics.md) — **7 Mandates** (Optimistic Render, Zero-Network Theme, Primer Screen, Hot-Reload, Deterministic Override, Stored Value, Payment Masking). Spec writers MUST load this file per §3 Step 7.

| # | Spec | Source PRD | Pre-Flight | Backend Relationship |
|---|---|---|---|---|
| 1 | FR-ERA3-08 — Mini App Host Shell | PRD-01, PRD-04 | Load both full modules + FR-APR-04 (existing TMA spec) + FR-CA11-15 (DPA branding) | **NEW** frontend. **CONSUMES** `dpa_engine.py` for whitelabel theming via `DPAEngine.resolve()` → `ResolvedPalette`. Mini Apps use `Telegram.WebApp` SDK — NOT `telegram_webhook.py`. |
| 2 | FR-ERA3-06 — Primitive Registry Query Service | PRD-08 | Load full module + sample YAMLs from each of the 8 experience families + meaning families | **NEW** FastAPI service. **READS** `primitives/**/*.yaml` (243+ files). No query layer exists today. |
| 3 | FR-ERA3-02 — In-Chat Telegram Payments | PRD-09 | Load full module + FR58 (Offer Tier Architecture) + FR-COM-01 (Pricing) | **NEW** payment integration. **CONSUMES** `offer_tier_governor.py` for tier eligibility checks. Stripe/Telegram Payments API is net new. |

### Phase 2 — Conscious Reactions (Specs 4-14)

> **CBAR Source:** [`Phase2_Conscious_Reactions_Epics.md`](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/april_updates/Phase2_Conscious_Reactions_Epics.md) — **7 Mandates** (Ephemeral Decay, Background Upload, Streaming Audio SLA, Earned Export Gate, Visual Adversary, Bracket Matchmaking, Client-Side Timing). Spec writers MUST load this file per §3 Step 7.

> [!IMPORTANT]
> **Spec 4 (CORE)** defines the shared engine: topic intake, biometric scoring pipeline, reaction event schema, content extraction hooks, DPA branding injection, PLUS the User Roles (Audience Jury, Supervisor Pairing, Vote Then React) and Options (Redemption Round) as built-in features.
>
> **Specs 5-7** are the 3 Reaction Mode Mini Apps. **Specs 8-14** are the 7 Content Creation Experience Mini Apps.

| # | Spec | Pre-Flight | Backend Relationship | Primary Primitives |
|---|---|---|---|---|
| 4 | FR-ERA3-05-CORE — Core Engine | Load FULL PRD-06 + Source of Truth + Viral Thresholds + FR61 (biometric scoring) + FR3 (Voice DNA) | **NEW** engine. **REPLACES** `trivianar_engine_service.py` (marked `[OBSOLETE]` in PRD-01 §3). Includes: Audience Jury role, Supervisor Pairing role, Vote Then React mechanic, Redemption Round mechanic. | All 8 families |

**Reaction Modes** (each is a standalone Mini App for reacting to hot topics):

| # | Spec | Pre-Flight | Backend Relationship | Primary Primitives |
|---|---|---|---|---|
| 5 | FR-ERA3-05a — Solo Reaction | PRD-06 §2.2.1 + CORE spec + TRG/FRC/FBK primitives | **NEW** Mini App. **CONSUMES** CORE engine. Foundational format — requires only one person. | TRG, FRC, FBK |
| 6 | FR-ERA3-05b — Debate with Jury | PRD-06 §2.2.2 + CORE spec + SOC/TRG/FBK/PER primitives | **NEW** Mini App. **CONSUMES** CORE engine. For/Against voting + counter-takes. Strongest silent referral mechanic. | SOC, TRG, FBK, PER |
| 7 | FR-ERA3-05c — Reaction Duel | PRD-06 §5.6.3 (Source of Truth) + CORE spec + SOC/FBK/SFR primitives | **NEW** Mini App. **CONSUMES** CORE engine. Two coaches react to same topic → side-by-side comparison. Async first, sync later. | SOC, FBK, SFR |

**Content Creation Experiences** (each is a standalone Mini App with a unique interactive format):

| # | Spec | Pre-Flight | Backend Relationship | Primary Primitives |
|---|---|---|---|---|
| 8 | FR-ERA3-05d — Tierlist Authority | PRD-06 §5.6.2 (Source of Truth) + CORE spec + FBK/FRC/PRG primitives | **NEW** Mini App. **CONSUMES** CORE engine. Coach ranks elements verbally → UI updates ranking state. Strong authority display. | FBK, FRC, PRG |
| 9 | FR-ERA3-05e — Audience Mirror Quiz | PRD-06 §5.6.4 (Source of Truth) + CORE spec + PER/TRB/FBK primitives | **NEW** Mini App. **CONSUMES** CORE engine. **READS** tribe_soul data. Authority validation + audience empathy proof. Drives $99.99 Coach OS conversion. | PER, TRB, FBK |
| 10 | FR-ERA3-05f — Blind Rank Reveal | PRD-06 §5.6.5 (Source of Truth) + CORE spec + SFR/FBK/TRG primitives | **NEW** Mini App. **CONSUMES** CORE engine. Judgment before context → then defend. Tension, humor, authenticity. | SFR, FBK, TRG |
| 11 | FR-ERA3-05g — Alphabet Challenge | PRD-06 §5.6.6 (Source of Truth) + CORE spec + PRG/FRC/FBK primitives | **NEW** Mini App. **CONSUMES** CORE engine. Timed letter-based recall under pressure. High energy, easy scoring. | PRG, FRC, FBK |
| 12 | FR-ERA3-05h — Last One Standing | PRD-06 §5.6.7 (Source of Truth) + CORE spec + SOC/PRG/SFR primitives | **NEW** Mini App. **CONSUMES** CORE engine. Elimination format — options narrowed one by one. Audience participation + tension escalation. | SOC, PRG, SFR |
| 13 | FR-ERA3-05i — Authority Quiz | PRD-06 §5.6.8 (Source of Truth) + CORE spec + PRG/FBK/TRB primitives | **NEW** Mini App. **CONSUMES** CORE engine. Escalating-stakes pressure ladder. Answer-under-pressure speaking practice. | PRG, FBK, TRB |
| 14 | FR-ERA3-05j — Ranking Quiz Co-Creation | PRD-06 §5.6.10 (Source of Truth) + CORE spec + SOC/FBK/PRG primitives | **NEW** Mini App. **CONSUMES** CORE engine. Person + audience rank, defend, challenge, reorder. Easy content extraction. | SOC, FBK, PRG |

### Phase 3 — Experience Mini Apps (Specs 15-20)

> **CBAR Source:** [`Phase3_Experience_Mini_Apps_Epics.md`](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/april_updates/Phase3_Experience_Mini_Apps_Epics.md) — **7 Mandates** (Ambient Prompt, Per-Slide Feedback, Lateral Progression, Telemetry Surfacing, Modular CMF Recovery, Peer-Gated Apex, Auth-Free Benchmark). Spec writers MUST load this file per §3 Step 7.

| # | Spec | Source PRD | Pre-Flight | Backend Relationship |
|---|---|---|---|---|
| 15 | FR-ERA3-01 — Webinar Companion | PRD-07 | Load full PRD-07 + FR-CA11-16 (AFFiNE) + FR33 (V2WS session) | **NEW** audience-facing Mini App. **READS** data produced by `v2ws_interactive_service.py`. The V2WS is the coach's creation tool; this is the audience's consumption surface. |
| 16 | FR-ERA3-11 — Challenge Arena | PRD-05 | Load full PRD-05 + PRG/SFR/FBK primitives | **NEW** Mini App. **CONSUMES** `learning_path_builder.py` `recommend_next()`. **CONSUMES** `habit_architecture.py` `parse_and_verify()`. Streak tracking + gamification are net new. |
| 17 | FR-ERA3-09 — Conscious Editor | PRD-02, PRD-03 | Load both + OmniShotCut paper | **NEW** Mini App. **CONSUMES** `content_machine.py` output. Editor UI is net new. |
| 18 | FR-ERA3-19 — Testimonial Builder & User Cards | PRD-05, PRD-09 | Load both + Silent Referral Source of Truth | **NEW** Mini App. Entirely new — voice/video recording of client transformation stories. `scorecard_emitter.py` is NOT relevant. |
| 19 | Score Card Viewer | PRD-04, PRD-05 | Load both + FR7 (Leadership Scorecard) | **NEW** Mini App. **READS** `leadership_scorecard.json` produced by `scorecard_emitter.py`. Visualization UI is net new. |
| 20 | FR-ERA3-10 — Onboarding Flow | PRD-01, PRD-04 | Load both + Source of Truth §5.4 (Supervisor Pairing as entry) + TRB/FRC primitives | **NEW** Mini App. First-touch experience before any reaction mode. |

### Phase 4 — Pipelines & Engines (Specs 21-27)

> **CBAR Source:** [`Phase4_Pipelines_and_Engines_Epics.md`](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md) — **7 Mandates** (Intelligence-Gated Intercept, Cinematic Meaning, Inline Routing SLA, Frictionless Block, Actionable Rejection, Sonic Prestige, Long Loop Framing). Spec writers MUST load this file per §3 Step 7.

| # | Spec | Source PRD | Pre-Flight | Backend Relationship |
|---|---|---|---|---|
| 21 | FR-ERA3-07 — AFFiNE Broadcasting Pipeline | PRD-07, PRD-01 | Load both + FR-CA11-16 (AFFiNE sync) | **TBD** — must audit `affine_sync` services before writing. |
| 22 | FR-ERA3-12 — OmniShotCut CMF Shot Intelligence | PRD-03 | Load full + OmniShotCut paper | **NEW** pipeline. **CONSUMES** Skia Renderer sidecar (`src/ccp/sidecars/skia-renderer/`). |
| 23 | FR-ERA3-13 — Four-Surface Async Skill Ladder | PRD-04 | Load full + Communication Skill Ladder doc | **NEW** service. **CONSUMES** `learning_path_builder.py` journey DAGs. Gamification layer is net new. |
| 24 | FR-ERA3-15 — Trigger-First Execution Guard | PRD-02 | Load full + TRG primitives | **TBD** — must audit `psych_routing_engine.py` before writing. |
| 25 | FR-ERA3-16 — Archetype Container Runtime | PRD-02 | Load full | **TBD** — must audit content archetype services before writing. |
| 26 | FR-ERA3-17 — Voice Prompt Engine | PRD-04 | Load full + FR3 (Voice DNA) | **TBD** — must audit `voice_dna_service.py` before writing. |
| 27 | FR-ERA3-18 — CBCS Four-Engine Runtime | PRD-05 | Load full + all FR-CBCS specs | **TBD** — must audit all `cbcs_*.py` services before writing. |

### Phase 5 — Growth (Specs 28-30)

> **CBAR Source:** [`Phase5_Growth_Epics.md`](file:///d:/Work/The%20Conscious%20Coaching%20Factory/docs/architecture/april_updates/Phase5_Growth_Epics.md) — **5 Mandates** (Verifiable Artifact, Earned Escalation, OFO Ego-Defense, Inline Capture Hook, 1-Tap Paywall). Spec writers MUST load this file per §3 Step 7.

| # | Spec | Source PRD | Pre-Flight | Backend Relationship |
|---|---|---|---|---|
| 28 | FR-ERA3-03 — Silent Referral Architecture | PRD-09 | Load full + Silent Referral Source of Truth + SOC primitives | **NEW** referral mechanism. **CONSUMES** `conversion_sequence_router.py` (FR53) for timing calibration via dormancy gates. **READS** `lead_capture_service.py` (FR-CA11-20) cooldown state. |
| 29 | FR-ERA3-04 — OFO Engine | PRD-09 | Load full | **NEW** service. No existing backend handles OFO. |
| 30 | FR-ERA3-14 — CAU Knowledge Transfer | PRD-01 | Load full | **NEW** service. **READS** existing SKILL files. No transfer/export service exists. |

### Phase 6 — Existing Spec Updates (Specs 31-34)

| # | Spec | Source PRD | What Changes |
|---|---|---|---|
| 31 | FR-APR-08 — Add ADR-05 + Dual-Source | PRD-08 | Add primitive-loading mandate to existing spec |
| 32 | FR-CA11-16 — Add broadcast path | PRD-07 | Add AFFiNE broadcast routing |
| 33 | FR-COM-01 — Update pricing | PRD-09 | Update tier pricing to match $39.99/$99.99 structure |
| 34 | FR58 — Update tier definitions | PRD-09 | Align `OfferTierGovernor` tier ceilings with new pricing |

---

## 8. CBAR Mandate Summary (33 Total)

> [!IMPORTANT]
> Every CBAR Mandate below is a **binding engineering constraint** derived from adversarial audit. Specs MUST declare which mandates they enforce in Section 3.

| Phase | # | Mandate | Governing Story | Governing Primitive |
|---|---|---|---|---|
| **1** | M-01 | The Optimistic Render Rule | Story 1.1 | `EXP-FRC-002` |
| **1** | M-02 | The Zero-Network Theme Rule | Story 1.2 | `EXP-TRS-001` |
| **1** | M-03 | The Primer Screen Rule | Story 1.3 | `EXP-FRC-003` |
| **1** | M-04 | The Hot-Reload Rule | Story 2.1 | `EXP-FBK-001` |
| **1** | M-05 | The Deterministic Override Rule | Story 2.2 | Orchestration Engine |
| **1** | M-06 | The Stored Value Rule | Story 3.1 | `EXP-PER-003` |
| **1** | M-07 | The Payment Masking Rule | Story 3.3 | `EXP-FBK-001` |
| **2** | M-01 | The Ephemeral Decay Mandate | Story 1.1 | `EXP-TRG-002` |
| **2** | M-02 | The Background Upload Rule | Story 1.2 | `EXP-FRC-003` |
| **2** | M-03 | The Streaming Audio SLA | Story 1.3 | `EXP-FBK-001` |
| **2** | M-04 | The Earned Export Gate | Story 2.1 | `EXP-PRG-002` |
| **2** | M-05 | The Visual Adversary Rule | Story 2.2 | `EXP-SOC-002` |
| **2** | M-06 | The Bracket Matchmaking Rule | Story 2.3 | `EXP-SOC-004` |
| **2** | M-07 | The Client-Side Timing Rule | Story 6.1 | `EXP-FRC-006` |
| **3** | M-01 | Ambient Prompt Rule | Story 1.1 | `EXP-TRS-003` |
| **3** | M-02 | Per-Slide Feedback Rule | Story 1.2 | `EXP-FBK-001` |
| **3** | M-03 | Lateral Progression Rule | Story 2.1 | `EXP-PRG-002` |
| **3** | M-04 | Telemetry Surfacing Rule | Story 2.2 | `EXP-FBK-004` |
| **3** | M-05 | Modular CMF Recovery Rule | Story 3.2 | `EXP-SAF-002` |
| **3** | M-06 | Peer-Gated Apex Rule | Story 4.2 | `EXP-SOC-001` |
| **3** | M-07 | Auth-Free Benchmark Rule | Story 6.1 | `EXP-FRC-002` |
| **4** | M-01 | The Intelligence-Gated Intercept Rule | Story 1.1 | `EXP-PER-003` |
| **4** | M-02 | The Cinematic Meaning Rule | Story 2.1 | `EXP-TRS-004` |
| **4** | M-03 | The Inline Routing SLA | Story 3.1 | `EXP-PRG-001` |
| **4** | M-04 | The Frictionless Block Rule | Story 4.1 | `EXP-FRC-006` |
| **4** | M-05 | The Actionable Rejection Rule | Story 5.1 | `EXP-FBK-001` |
| **4** | M-06 | The Sonic Prestige Rule | Story 6.1 | `EXP-TRS-003` |
| **4** | M-07 | The Long Loop Framing Rule | Story 7.1 | `EXP-PRG-004` |
| **5** | M-01 | The Verifiable Artifact Rule | Story 1.1 | `EXP-SOC-001` |
| **5** | M-02 | The Earned Escalation Rule | Story 1.2 | `EXP-TRG-005` |
| **5** | M-03 | The OFO Ego-Defense Rule | Story 2.1 | `EXP-TRS-004` |
| **5** | M-04 | The Inline Capture Hook | Story 2.2 | `EXP-PRG-001` |
| **5** | M-05 | The 1-Tap Paywall Rule | Story 3.1 | `EXP-FRC-002` |

---

## 9. Key Reference Files

| File | Purpose |
|---|---|
| `docs/prd/modules/PRD_INDEX.md` | Master PRD router |
| `docs/prd/modules/PRD_01-09_*.md` | Full PRD modules (include brownfield analysis) |
| `docs/architecture/CCP_Technical_Architecture.md` | ADRs + 7-layer architecture |
| `docs/architecture/april_updates/Phase1_Infrastructure_Epics.md` | **CBAR-hardened** Phase 1 Epics — 7 mandates |
| `docs/architecture/april_updates/Phase2_Conscious_Reactions_Epics.md` | **CBAR-hardened** Phase 2 Epics — 7 mandates |
| `docs/architecture/april_updates/Phase3_Experience_Mini_Apps_Epics.md` | **CBAR-hardened** Phase 3 Epics — 7 mandates |
| `docs/architecture/april_updates/Phase4_Pipelines_and_Engines_Epics.md` | **CBAR-hardened** Phase 4 Epics — 7 mandates |
| `docs/architecture/april_updates/Phase5_Growth_Epics.md` | **CBAR-hardened** Phase 5 Epics — 5 mandates |
| `docs/architecture/cbar_audits/CBAR_Audit_Phase1_Infrastructure.md` | Phase 1 adversarial audit trail |
| `docs/architecture/cbar_audits/CBAR_Audit_Phase2_Conscious_Reactions.md` | Phase 2 adversarial audit trail |
| `docs/architecture/cbar_audits/CBAR_Audit_Phase3_Experience_Mini_Apps.md` | Phase 3 adversarial audit trail |
| `docs/architecture/cbar_audits/CBAR_Audit_Phase4_Pipelines_and_Engines.md` | Phase 4 adversarial audit trail |
| `docs/architecture/spec updates/CBAR_Constraint_Based_Adversarial_Reasoning.md` | CBAR engine protocol |
| `src/ccp/api/main.py` | FastAPI entry point (add new routes here) |
| `src/ccp/models/` | All Pydantic models (45+ files) |
| `src/ccp/services/` | All backend services (201+ files) |
| `src/ccp/pipelines/` | All pipelines (17 files) |
| `src/ccp/agents/` | All agents (17 files) |
| `src/ccp/scripts/setup_supabase.py` | Database schema (10 schemas, add tables here) |
| `src/ccp/scripts/setup_neo4j.py` | Graph schema (Neo4j manager) |
| `tests/integration/` | Test pattern — 88 existing tests (follow for new tests) |
| `primitives/experience/` | 51 experience primitive YAMLs across 8 families |
| `primitives/meaning/` | 192+ meaning primitive YAMLs |
| `lab/CCP APRIL Updates/05_Core_Experience/Conscious_Reactions_Source_of_Truth.md` | 14 reaction modes — definitive product description |
| `lab/CCP APRIL Updates/05_Core_Experience/Conscious_Reactions_Experience_Primitive_Orchestration_Architecture.md` | 8 experience primitive families + orchestration sequence |
| `lab/CCP APRIL Updates/05_Core_Experience/Conscious_Reactions_Viral_Thresholds.md` | Topic scoring thresholds |
| `tools/tierlist-app/` | Desktop Excalidraw+React recording studio (NOT a Telegram Mini App) |
| `tools/telegram-tierlist-bot/` | Existing Telegram bot |

