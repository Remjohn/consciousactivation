# CMF Visual Pipeline Re-Architecture Proposal
## Session Separation Strategy: Preparation vs. Composition

**Date:** 2026-02-02
**Subject:** Systems Analysis of Decoupled Visual Generation Pipeline
**Hypothesis:** Separating "Ingredient Preparation" from "Prompt Composition" into discrete sessions will eliminate AI complacency and produce richer visual outputs.

---

## 1. Executive Summary

This document analyzes a fundamental architectural change to the CMF visual pipeline. The core proposal is to **decouple the visual generation process into two distinct phases**, each executed in a **fresh AI session**:

| Phase | Name | Purpose | Output |
|-------|------|---------|--------|
| **Phase A** | Ingredient Preparation | Extract ALL cinematic reasoning, verbs, body truths, and visual schema ingredients | Enriched `beat_cluster.json` with PRIMAL data embedded |
| **Phase B** | Prompt Composition | Load prepared ingredients in a FRESH session; focus ONLY on prompt synthesis | Final `T2I` and `I2V` prompt files |

The hypothesis is that AI models suffer from **context fatigue** and **cognitive complacency** when asked to both *think deeply about ingredients* AND *compose polished outputs* in the same session. By the time the model reaches composition, it has exhausted its "novelty budget" and defaults to safe, generic patterns.

This analysis applies Systems Thinking and SWOT methodology to evaluate whether this architectural change would solve the "Portrait Obsession" problem identified in the Audrey project.

---

## 2. Systems Thinking Analysis: The Cognitive Fatigue Hypothesis

### 2.1 The Current Monolithic Flow

In the existing pipeline, a single session performs the following sequence:

```
SESSION START (Context Window = Empty)
    │
    ├── Load final_script.json
    ├── Load strategy_brief.json
    ├── Load Brand Avatar
    ├── Load Visual Schema
    ├── Load beat_cluster.json
    │       ↓
    ├── [REASONING PHASE]
    │   ├── Run PRIMAL Analysis for each beat
    │   ├── Run VLSA Director's Treatment
    │   ├── Select T-Codes and V-Codes
    │   └── Validate Anti-Metaphor constraints
    │       ↓
    ├── [COMPOSITION PHASE]
    │   ├── Write T2I Prompt Block 1-7
    │   ├── Write I2V Motion Timeline
    │   └── Output SB_W{N}_*.txt files
    │
SESSION END (Context Window = Full, Attention Diluted)
```

**The Problem:** By the time the model reaches "Composition," it has:

1. **Consumed significant context window** with file loading and intermediate reasoning.
2. **Made dozens of micro-decisions** during the reasoning phase.
3. **Established cognitive anchors** (e.g., "this is a transformation story" → "show wholeness").
4. **Depleted its novelty-seeking behavior** — the model "settles" into a pattern.

This creates what we call **Contextual Entropy**: the degradation of creative specificity as the session progresses.

### 2.2 Evidence of Contextual Entropy in Audrey Outputs

Examining the Audrey storyboard files, we observe a pattern:

| Scene | PRIMAL Quality | Prompt Specificity | Observation |
|-------|----------------|-------------------|-------------|
| W1 | High ("shoulders drop two inches") | Medium ("coral batik strains as she breathes") | First scene has active verbs |
| W2 | Medium ("furrowed brow, hand pressing temple") | Low ("steadying herself against wall") | Action reduced to static pose |
| W3 | Medium ("hand resting on solar plexus") | Low ("listening to pulse beneath skin") | Still reasonable |
| W4 | Low ("softened features, warm gaze") | Low ("looking peaceful, holding toy") | Generic stock-photo language emerging |
| W5 | Low ("spine straight, eyes locked") | Very Low ("centered portrait, healed") | Full collapse into default |

**The Decay Curve:** Specificity degrades as the session progresses. The model "gives up" on finding unique compositions and reverts to templates.

### 2.3 The Proposed Decoupled Flow

The architectural change splits the workload:

```
═══════════════════════════════════════════════════════
SESSION A: INGREDIENT PREPARATION (Pure Reasoning)
═══════════════════════════════════════════════════════
    │
    ├── Load transcript, strategy_brief, Brand Avatar
    │       ↓
    ├── [DEEP REASONING — NO OUTPUT PRESSURE]
    │   ├── Run PRIMAL Analysis (Feeling, Body Truth, Environment, Timestamp, Uniqueness)
    │   ├── Run VLSA Director's Treatment (Subtext, Visual Irony, Texture Anchor, Director Ref)
    │   ├── Extract PHYSICAL VERBS from each quote ("shifts," "clenches," "exhales")
    │   ├── Identify MICRO-ACTIONS at each timestamp
    │   └── Select T-Codes and V-Codes with justification
    │       ↓
    ├── [OUTPUT: ENRICHED beat_cluster.json or PRIMAL_INGREDIENTS.json]
    │   Each beat now contains:
    │   {
    │     "beat": "W5",
    │     "primal": {
    │       "feeling": "The certainty of complete work",
    │       "body_truth": "Eyes shift left-to-right retracing each step; corner of mouth tightens; one definitive nod",
    │       "environment": "Same room as W1, now bathed in full morning light",
    │       "timestamp": "00:16:30",
    │       "uniqueness": "Only Audrey describes 'pas à pas' with this gratitude"
    │     },
    │     "vlsa": {
    │       "subtext": "She is the witness to her own healing",
    │       "visual_irony": "Direct address, but intimate not testimonial",
    │       "texture_anchor": "Light reflecting in the eyes — the spark of completion",
    │       "director_ref": "Barry Jenkins Moonlight direct address"
    │     },
    │     "t_codes": ["T1 (eyes/face)", "T4 (halfway vs full)"],
    │     "v_codes": ["V11 (Uncomfortable Lock)", "V3 (Invasive Macro)"],
    │     "physical_verbs": ["shifts", "tightens", "nods"]
    │   }
    │
SESSION A END
═══════════════════════════════════════════════════════

═══════════════════════════════════════════════════════
SESSION B: PROMPT COMPOSITION (Pure Synthesis)
═══════════════════════════════════════════════════════
    │
    ├── Load PRIMAL_INGREDIENTS.json (pre-computed reasoning)
    ├── Load visual_schema.json
    ├── Load Brand Avatar
    │       ↓
    ├── [FOCUSED COMPOSITION — NO REASONING REQUIRED]
    │   The model's ONLY job is to:
    │   ├── Translate already-defined body_truth into prose
    │   ├── Apply the pre-selected V-Code camera technique
    │   ├── Embed the pre-selected texture_anchor
    │   └── Format into the 7-block T2I structure
    │       ↓
    ├── [OUTPUT: SB_W{N}_T2I.txt, SB_W{N}_I2V.txt]
    │
SESSION B END
═══════════════════════════════════════════════════════
```

**The Key Insight:** Session B receives *pre-digested decisions*. It doesn't need to "think" about what the body is doing — that's already defined. Its only job is to *render those decisions into beautiful language*.

---

## 3. SWOT Analysis: Session Separation Architecture

### 3.1 STRENGTHS (Internal, Positive)

| Strength | Mechanism | Impact |
|----------|-----------|--------|
| **Eliminates Reasoning Fatigue** | Session B starts fresh with a clean context window. | Full attention on prose quality, not decision-making. |
| **Forces Explicit Reasoning Artifacts** | PRIMAL_INGREDIENTS.json becomes a auditable "contract." | Failures are traceable to Session A (bad reasoning) OR Session B (bad rendering). |
| **Enables Parallel Specialization** | Session A could use a "high-EQ" model (Pro); Session B could use a "fast-prose" model (Flash). | Optimal model selection per task. |
| **Prevents Cognitive Anchor Lock-In** | Session B has no memory of "I already decided this is a portrait." | Fresh eyes on the same data may find different compositions. |
| **Supports Human-in-the-Loop Review** | After Session A, a human could review PRIMAL_INGREDIENTS.json before Session B runs. | Quality gate between reasoning and output. |

### 3.2 WEAKNESSES (Internal, Negative)

| Weakness | Risk | Mitigation |
|----------|------|------------|
| **Increased Latency** | Two sessions = 2x startup time + file I/O overhead. | Batch projects to amortize overhead. |
| **Schema Drift Risk** | If PRIMAL_INGREDIENTS.json schema changes, Session B may fail silently. | Versioned schema + validation step at Session B start. |
| **Loss of Creative Serendipity** | Rigid pre-defined ingredients may prevent "happy accidents" in composition. | Allow Session B limited override authority with justification. |
| **Complexity Increase** | More moving parts = more failure points. | Clear handoff contracts; automated validation. |
| **Over-Engineering Risk** | This may be solving a symptom, not a root cause. | Pilot on 2-3 projects before full rollout. |

### 3.3 OPPORTUNITIES (External, Positive)

| Opportunity | How to Exploit |
|-------------|----------------|
| **Ingredient Caching** | PRIMAL_INGREDIENTS.json can be reused for multiple composition styles (e.g., "cinematic" vs. "editorial"). |
| **A/B Testing Compositions** | Run Session B multiple times with different models or prompts; compare outputs without re-running expensive Session A. |
| **Specialized Composer Agents** | Create multiple Session B variants: "The Intimate Composer," "The Epic Composer," "The Kinetic Composer." |
| **Human Co-Authorship** | A human editor could refine PRIMAL_INGREDIENTS.json before Session B, injecting creative direction. |
| **Async Scaling** | Session A for all 5 beats can run first; Session B can process each beat in parallel. |

### 3.4 THREATS (External, Negative)

| Threat | Likelihood | Impact | Mitigation |
|--------|------------|--------|------------|
| **Session B still defaults to generics** | Medium | High | Embed "Anti-Portrait" constraints directly in the Composer skill. |
| **PRIMAL_INGREDIENTS.json is still too abstract** | Medium | High | Enforce VERB mandates in Session A output schema. |
| **Model updates break Session B** | Low | Medium | Pin model versions; test after updates. |
| **Increased operational complexity** | Medium | Medium | Document workflow clearly; automate with RUN_PIPELINE.ps1. |

---

## 4. Systems Dynamics: Why This Should Work

### 4.1 The "Fresh Session" Effect

LLMs exhibit a well-documented behavior: **early tokens in a session receive disproportionate attention weight**. This is why:

- The first paragraph of a document is usually higher quality than the fifth.
- The first scene in a storyboard is more specific than the last.
- A model asked to "continue" an existing document produces blander output than one asked to "create" a new document.

By starting Session B with a fresh context, we reset the attention mechanism. The PRIMAL_INGREDIENTS.json data is "new information" to the model, not "old decisions I already made."

### 4.2 The "Constraint Liberation" Paradox

Counter-intuitively, **pre-defining the reasoning liberates the composer**. In the current system:

```
Architect: "What should the body truth be? Let me think... probably something about certainty... spine straight, eyes locked?"
Architect: "Now compose a prompt using that." → [Generic portrait]
```

In the new system:

```
Preparer (Session A): "The body truth is: Eyes shift left-to-right retracing each step; corner of mouth tightens; one definitive nod."

Composer (Session B): "I receive: 'eyes shift left-to-right, mouth tightens, definitive nod.' My job is to describe this beautifully."
→ "Her gaze tracks an invisible path—left to right, right to left—mentally walking back through each step. The corner of her lip tightens imperceptibly. Then, one nod. Not for the camera. For herself."
```

The Composer is freed from the burden of *deciding what happens* and can focus entirely on *how to say it*.

### 4.3 Feedback Loop Isolation

In the current monolithic session, errors compound:

```
[Bad Reasoning] → feeds into → [Bad Composition] → no way to trace which caused the failure
```

In the decoupled system:

```
[Session A Output] → auditable artifact → [Session B Output]
     ↓ Review                              ↓ Review
If bad: Fix Session A skill            If bad: Fix Session B skill
```

This enables **root cause isolation**. If the PRIMAL_INGREDIENTS are rich but the prompts are bland, we know the Composer skill needs work. If the PRIMAL_INGREDIENTS are generic ("centered portrait"), we know the Preparer skill needs work.

---

## 5. Implementation Sketch

### 5.1 Phase A: Ingredient Preparation Session

**Command:** `/cmf-prepare-visuals {project_id}`

**Inputs:**
- `final_script.json`
- `strategy_brief.json`
- `Brand Avatar 😎.md`
- `beat_cluster.json` (basic version from cmf-beat-cluster)

**Process:**
1. For each beat in beat_cluster.json:
   - Run PRIMAL Analysis (Feeling, Body Truth, Environment, Timestamp, Uniqueness)
   - Run VLSA Director's Treatment
   - Extract physical verbs from the representative quote
   - Select T-Codes and V-Codes with justification
2. Write enriched output

**Output:** `{project_id}_PRIMAL_INGREDIENTS.json`

### 5.2 Phase B: Prompt Composition Session (Per-Beat or Batched)

**Command:** `/cmf-compose-prompts {project_id}` (runs in fresh session)

**Inputs:**
- `{project_id}_PRIMAL_INGREDIENTS.json`
- `{project_id}_visual_schema.json`
- `Brand Avatar 😎.md`

**Process:**
For each beat:
1. Load pre-computed PRIMAL and VLSA data
2. NO REASONING — only prose synthesis
3. Render into 7-block T2I prompt
4. Render into I2V motion timeline

**Output:** `SB_W{N}_T2I.txt`, `SB_W{N}_I2V.txt`

### 5.3 Optional: Per-Beat Composition Sessions

For maximum freshness, each beat could have its own Session B:

```
Session B-1: Compose W1 → SB_W1_*.txt
Session B-2: Compose W2 → SB_W2_*.txt
Session B-3: Compose W3 → SB_W3_*.txt
Session B-4: Compose W4 → SB_W4_*.txt
Session B-5: Compose W5 → SB_W5_*.txt
```

This prevents even the "first beat is better than the last beat" decay pattern.

---

## 6. Decision Matrix: Will This Solve the Portrait Obsession?

| Root Cause | Does Session Separation Address It? | Verdict |
|------------|-------------------------------------|---------|
| **Abstract visual_intent in beat_cluster** | ✅ Session A is now responsible for embedding VERBS and BODY TRUTH | ADDRESSED |
| **V-Code bias toward close-ups** | ⚠️ Partially — if Session A selects diverse V-Codes, Session B will use them | PARTIALLY ADDRESSED |
| **Cognitive fatigue causing generic outputs** | ✅ Session B starts fresh with full attention | ADDRESSED |
| **Lack of auditable reasoning chain** | ✅ PRIMAL_INGREDIENTS.json is the audit trail | ADDRESSED |
| **Complacency from re-using patterns** | ✅ Each fresh session has no memory of "what I did before" | ADDRESSED |

**Conclusion:** Session separation addresses **4 of 5 root causes** fully and **1 partially**. The partial issue (V-Code diversity) requires an additional constraint in Session A to mandate variety.

---

## 7. Recommendation

**PROCEED WITH THE SESSION SEPARATION ARCHITECTURE.**

The proposal is sound. The risks are manageable. The benefits align with observed failure patterns.

**Implementation Priority:**

1. **Create `cmf-prepare-visuals` command** — Defines the PRIMAL_INGREDIENTS.json schema and enforces VERB + BODY TRUTH extraction.
2. **Create `cmf-compose-prompts` command** — Loads prepared ingredients and synthesizes prompts with ZERO reasoning overhead.
3. **Update RUN_PIPELINE.ps1** — Insert the new preparation step before storyboard, and call composition as a separate session.
4. **Pilot on 2 projects** — Run Audrey AND one other project through the new pipeline; compare against old outputs.
5. **Iterate based on results** — If compositions are still generic, investigate Session B skill constraints.

---

## 8. Final Systems Diagram

```
┌────────────────────────────────────────────────────────────────────┐
│                        PHASE 1A: NARRATIVE                          │
│  (Diagnose → Hunt → Analyze → Compose → Authorize → Script → Beat)  │
└────────────────────────────────────┬───────────────────────────────┘
                                     │
                                     ▼
                          beat_cluster.json (basic)
                                     │
┌────────────────────────────────────┴───────────────────────────────┐
│                    SESSION A: INGREDIENT PREPARATION                │
│                        /cmf-prepare-visuals                         │
│                                                                     │
│  • PRIMAL Analysis (Feeling, Body Truth, Environment, Timestamp)    │
│  • VLSA Director's Treatment (Subtext, Irony, Texture, Director)    │
│  • Physical Verb Extraction                                         │
│  • T-Code / V-Code Selection with Justification                     │
│                                                                     │
│  OUTPUT: PRIMAL_INGREDIENTS.json                                    │
└────────────────────────────────────┬───────────────────────────────┘
                                     │
                          [QUALITY GATE / HUMAN REVIEW]
                                     │
┌────────────────────────────────────┴───────────────────────────────┐
│                    SESSION B: PROMPT COMPOSITION                    │
│                       /cmf-compose-prompts                          │
│                                                                     │
│  • Load PRIMAL_INGREDIENTS.json (pre-computed)                      │
│  • Load visual_schema.json                                          │
│  • Load Brand Avatar                                                │
│  • ZERO REASONING — Pure prose synthesis                            │
│                                                                     │
│  OUTPUT: SB_W{N}_T2I.txt, SB_W{N}_I2V.txt                           │
└────────────────────────────────────┬───────────────────────────────┘
                                     │
                                     ▼
┌────────────────────────────────────────────────────────────────────┐
│                   REMAINING PHASE 1B STEPS                          │
│           (Sonic → Motion → Visual Authorization)                   │
└────────────────────────────────────────────────────────────────────┘
```

---

**END OF ANALYSIS**
