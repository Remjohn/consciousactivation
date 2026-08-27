---
name: cmf-diagnose
description: Story Doctor - Arc diagnosis and strategy brief generation
---

# /cmf-diagnose {project_id}

// turbo-all

> **SKILLS_BASE:** `skills/cmf/`
> **GUIDES_BASE:** `intelligence/guides/`

**Objective:** Diagnose the arc type and establish story foundation.

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify project folder exists", status: "pending" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Arc Selection Guide", status: "pending" },
    { id: "step-3", description: "STEP 3: SCAN - Answer 5 diagnosis questions", status: "pending" },
    { id: "step-4", description: "STEP 4: DETECT - Apply arc decision tree", status: "pending" },
    { id: "step-5", description: "STEP 5A: BUILD narrative_dna - Extract structural framework", status: "pending" },
    { id: "step-5", description: "STEP 5B: DISTILL spr_text - Compress to 48-60 word priming", status: "pending" },
    { id: "step-5", description: "STEP 5C: WRITE strategy_brief.json - Save output file", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm 13 quality gates", status: "pending" }
  ]
});
```

**DO NOT PROCEED until you have called `write_todos` above.**


---

## 📋 Step Execution Protocol (MANDATORY)

> [!CAUTION]
> **You MUST call `write_todos` at EVERY step transition.**
> This is not optional. Skipping todo updates = workflow failure.

**For EACH step, follow this pattern:**

1. **START STEP:** Update todo status to `in_progress`
2. **EXECUTE:** Perform the step actions
3. **VALIDATE:** Verify outputs exist
4. **COMPLETE STEP:** Update todo status to `completed`

**Status Update Template:**
```javascript
// When STARTING Step N:
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: ...", status: "completed" },
    { id: "step-2", description: "STEP 2: ...", status: "in_progress" },  // <- Current
    { id: "step-3", description: "STEP 3: ...", status: "pending" },
  ]
});
```

> [!IMPORTANT]
> **Validation Gate:** Before marking a step `completed`, verify:
> - Output file exists (if applicable)
> - Output matches expected schema
> - No error messages encountered



---

## STEP 1: PRE-FLIGHT

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify project folder exists", status: "in_progress" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Arc Selection Guide", status: "pending" },
    { id: "step-3", description: "STEP 3: SCAN - Answer 5 diagnosis questions", status: "pending" },
    { id: "step-4", description: "STEP 4: DETECT - Apply arc decision tree", status: "pending" },
    { id: "step-5", description: "STEP 5: GENERATE - Create strategy_brief.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm quality gates", status: "pending" }
  ]
});
```

**ACTIONS:**

1. Navigate to `production/Coach Adele/{project_id}/`
   - If folder missing → STOP → Report: "ERROR: Project folder not found"

2. Find transcript file: `*_transcript.md` or `*_transcript.srt`
   - If missing → STOP → Report: "ERROR: Transcript not found"

3. Read `PROJECT_CONTEXT.md` if it exists (optional)

**OUTPUT (20-30 words):**
```
PRE-FLIGHT COMPLETE:
- Folder: ✅ production/Coach Adele/{project_id}/
- Transcript: ✅ {filename} ({X} words)
- Context: ✅ Found / ⚠️ Not found
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify project folder exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Arc Selection Guide", status: "pending" },
    { id: "step-3", description: "STEP 3: SCAN - Answer 5 diagnosis questions", status: "pending" },
    { id: "step-4", description: "STEP 4: DETECT - Apply arc decision tree", status: "pending" },
    { id: "step-5", description: "STEP 5: GENERATE - Create strategy_brief.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm quality gates", status: "pending" }
  ]
});
```

---

## STEP 2: LOAD SKILL

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify project folder exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Arc Selection Guide", status: "in_progress" },
    { id: "step-3", description: "STEP 3: SCAN - Answer 5 diagnosis questions", status: "pending" },
    { id: "step-4", description: "STEP 4: DETECT - Apply arc decision tree", status: "pending" },
    { id: "step-5", description: "STEP 5: GENERATE - Create strategy_brief.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm quality gates", status: "pending" }
  ]
});
```

**ACTIONS:**

1. Read this file COMPLETELY: `skills/cmf/hunters/🎯-arc-selection-guide/SKILL.md`
2. Load the 13-arc routing table into your context

**CRITICAL:** Read the FULL file. Do NOT summarize. Do NOT skip sections.

**OUTPUT (30-50 words):**
```
SKILL LOADED:
- File: skills/cmf/hunters/🎯-arc-selection-guide/SKILL.md
- Arcs available: 13 (Witness, Breakthrough, Shared Struggle, ...)
- Decision tree: Loaded
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify project folder exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Arc Selection Guide", status: "completed" },
    { id: "step-3", description: "STEP 3: SCAN - Answer 5 diagnosis questions", status: "pending" },
    { id: "step-4", description: "STEP 4: DETECT - Apply arc decision tree", status: "pending" },
    { id: "step-5", description: "STEP 5: GENERATE - Create strategy_brief.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm quality gates", status: "pending" }
  ]
});
```

---

## STEP 3: CONTENT SCAN

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify project folder exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Arc Selection Guide", status: "completed" },
    { id: "step-3", description: "STEP 3: SCAN - Answer 5 diagnosis questions", status: "in_progress" },
    { id: "step-4", description: "STEP 4: DETECT - Apply arc decision tree", status: "pending" },
    { id: "step-5", description: "STEP 5: GENERATE - Create strategy_brief.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm quality gates", status: "pending" }
  ]
});
```

**ACTIONS:**

Read the transcript and answer these 5 questions. **Each answer MUST be 20-40 words.**

| # | Question | Word Count |
|---|----------|------------|
| 1 | Who is speaking? (Client/Coach/Both) | 20-40 words |
| 2 | What is the emotional journey? (Before → After) | 20-40 words |
| 3 | Is there a clear transformation? (Yes/No + Evidence) | 20-40 words |
| 4 | What proof points exist? (Numbers, testimonials) | 20-40 words |
| 5 | What's the call to action? (Implicit/Explicit) | 20-40 words |

**OUTPUT (100-200 words total):**
```markdown
## CONTENT SCAN RESULTS

| # | Question | Answer |
|---|----------|--------|
| 1 | Who is speaking? | [20-40 words] |
| 2 | Emotional journey? | [20-40 words] |
| 3 | Clear transformation? | [20-40 words] |
| 4 | Proof points? | [20-40 words] |
| 5 | Call to action? | [20-40 words] |

Total words: [100-200]
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify project folder exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Arc Selection Guide", status: "completed" },
    { id: "step-3", description: "STEP 3: SCAN - Answer 5 diagnosis questions", status: "completed" },
    { id: "step-4", description: "STEP 4: DETECT - Apply arc decision tree", status: "pending" },
    { id: "step-5", description: "STEP 5: GENERATE - Create strategy_brief.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm quality gates", status: "pending" }
  ]
});
```

---

## STEP 4: ARC DETECTION

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify project folder exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Arc Selection Guide", status: "completed" },
    { id: "step-3", description: "STEP 3: SCAN - Answer 5 diagnosis questions", status: "completed" },
    { id: "step-4", description: "STEP 4: DETECT - Apply arc decision tree", status: "in_progress" },
    { id: "step-5", description: "STEP 5: GENERATE - Create strategy_brief.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm quality gates", status: "pending" }
  ]
});
```

**ACTIONS:**

Apply the decision tree from the Arc Selection Guide:

```
IF emotional breakdown present → The Witness
IF sudden insight/epiphany → The Breakthrough  
IF community/shared experience → The Shared Struggle
IF confrontation/callout → The Confrontation
IF origin story/how began → The Core Transformation
IF cautionary tale/warning → The Warning
IF comeback from setback → The Rally
IF spiritual awakening → The Divine Spark
IF hero's journey call → The Call to Adventure
IF deadline/urgency → The Ticking Clock
IF humor for insight → The Comedic Reframe
IF return home/full circle → The Sacred Return
IF quiet wisdom/reflection → The Quiet Reflection
```

**OUTPUT (50-80 words):**
```markdown
## ARC DETECTION RESULT

**Selected Arc:** The [Name]
**Confidence:** [0.75-1.00]
**Reasoning:** [30-50 words explaining why this arc was selected based on transcript evidence]
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify project folder exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Arc Selection Guide", status: "completed" },
    { id: "step-3", description: "STEP 3: SCAN - Answer 5 diagnosis questions", status: "completed" },
    { id: "step-4", description: "STEP 4: DETECT - Apply arc decision tree", status: "completed" },
    { id: "step-5", description: "STEP 5: GENERATE - Create strategy_brief.json", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm quality gates", status: "pending" }
  ]
});
```

---

## STEP 5A: BUILD narrative_dna

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify project folder exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Arc Selection Guide", status: "completed" },
    { id: "step-3", description: "STEP 3: SCAN - Answer 5 diagnosis questions", status: "completed" },
    { id: "step-4", description: "STEP 4: DETECT - Apply arc decision tree", status: "completed" },
    { id: "step-5", description: "STEP 5A: BUILD narrative_dna - Extract structural framework", status: "in_progress" },
    { id: "step-5", description: "STEP 5B: DISTILL spr_text - Compress to 48-60 word priming", status: "pending" },
    { id: "step-5", description: "STEP 5C: WRITE strategy_brief.json - Save output file", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm 13 quality gates", status: "pending" }
  ]
});
```

**PURPOSE:** Extract structural transformation framework from transcript.

**ACTIONS:**

Re-read the transcript and extract VERBATIM quotes/details for each field:

| Field | Source in Transcript | What to Extract |
|-------|---------------------|-----------------|
| `state_alpha.identity` | How client describes themselves BEFORE | Identity code `(Self == X)` |
| `state_alpha.loop` | Recurring pattern described | `{A -> B -> C -> Repeat}` |
| `state_alpha.internal_monologue` | EXACT quote of limiting belief | 5-12 words verbatim |
| `state_alpha.sensory_anchor` | Physical description of suffering | 5-10 words |
| `the_abyss.event` | The breaking point moment | CAPSLOCK event name |
| `the_abyss.sensation` | Physical feelings at rock bottom | `(Physical1, Physical2)` |
| `the_abyss.realization` | EXACT quote of insight | 5-15 words verbatim |
| `the_spark.trigger` | Coach-related moment | Coach action |
| `the_spark.insight_quote` | EXACT quote WITH TIMESTAMP | Quote + `(HH:MM)` |
| `state_omega.identity` | New self-concept | `(Self == X)` |
| `state_omega.action` | What they do differently | 5-10 words |
| `state_omega.result` | MEASURABLE outcome | Must contain NUMBER |
| `sensory_anchors` | 3 physical details | BEFORE, TURNING, NOW |
| `coach_role` | Coach's function | From enums |

**OUTPUT:** Write out the narrative_dna JSON object (do not save yet).

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify project folder exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Arc Selection Guide", status: "completed" },
    { id: "step-3", description: "STEP 3: SCAN - Answer 5 diagnosis questions", status: "completed" },
    { id: "step-4", description: "STEP 4: DETECT - Apply arc decision tree", status: "completed" },
    { id: "step-5", description: "STEP 5A: BUILD narrative_dna - Extract structural framework", status: "completed" },
    { id: "step-5", description: "STEP 5B: DISTILL spr_text - Compress to 48-60 word priming", status: "pending" },
    { id: "step-5", description: "STEP 5C: WRITE strategy_brief.json - Save output file", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm 13 quality gates", status: "pending" }
  ]
});
```

---

## STEP 5B: DISTILL spr_text

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify project folder exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Arc Selection Guide", status: "completed" },
    { id: "step-3", description: "STEP 3: SCAN - Answer 5 diagnosis questions", status: "completed" },
    { id: "step-4", description: "STEP 4: DETECT - Apply arc decision tree", status: "completed" },
    { id: "step-5", description: "STEP 5A: BUILD narrative_dna - Extract structural framework", status: "completed" },
    { id: "step-5", description: "STEP 5B: DISTILL spr_text - Compress to 48-60 word priming", status: "in_progress" },
    { id: "step-5", description: "STEP 5C: WRITE strategy_brief.json - Save output file", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm 13 quality gates", status: "pending" }
  ]
});
```

**PURPOSE:** Compress narrative_dna into 48-60 word latent space primer.

**📚 REQUIRED READING:** `intelligence/guides/SPR_DISTILLATION_GUIDE.md`

**SPR DISTILLATION ALGORITHM:**

```
INPUT: narrative_dna object from STEP 5A
OUTPUT: 48-60 word prose (spr_text)

SENTENCE 1: state_alpha.sensory_anchor → felt suffering (8-12 words)
SENTENCE 2: the_abyss.sensation → breaking point (8-12 words)
SENTENCE 3: the_spark.insight_quote → coach insight (8-12 words)
SENTENCE 4: state_omega.action → new behavior (8-12 words)
SENTENCE 5: state_omega.result → measurable proof (8-12 words)
SENTENCE 6: gift → what they offer (8-12 words)

RULES:
- Use EXACT words from internal_monologue, insight_quote
- Use sensory/physical language
- Include transcript metaphors
- Count words BEFORE finalizing
```

**EXAMPLE DISTILLATION:**

From this narrative_dna:
```json
{
  "state_alpha": { "sensory_anchor": "weight of eyelids every afternoon" },
  "the_abyss": { "sensation": "(Frustration_Burning, Tears_Behind_Smile)" },
  "the_spark": { "insight_quote": "gut not absorbing nutrients (08:23)" },
  "state_omega": { "result": "Energy from 3/10 to 8/10" }
}
```

To this spr_text (56 words):
> "She dragged through days like a zombie, weight pressing her eyelids by afternoon. The doctor's 'nothing wrong' broke her—frustration burning behind forced smiles. Dr. Maria saw what medicine missed: gut not absorbing nutrients properly. Now she listens to her body first. Energy climbed from 3 to 8 within six weeks. She helps other mothers trust their bodies."

**OUTPUT:** Write out the spr_text string (48-60 words, count them).

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify project folder exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Arc Selection Guide", status: "completed" },
    { id: "step-3", description: "STEP 3: SCAN - Answer 5 diagnosis questions", status: "completed" },
    { id: "step-4", description: "STEP 4: DETECT - Apply arc decision tree", status: "completed" },
    { id: "step-5", description: "STEP 5A: BUILD narrative_dna - Extract structural framework", status: "completed" },
    { id: "step-5", description: "STEP 5B: DISTILL spr_text - Compress to 48-60 word priming", status: "completed" },
    { id: "step-5", description: "STEP 5C: WRITE strategy_brief.json - Save output file", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm 13 quality gates", status: "pending" }
  ]
});
```

---

## STEP 5C: WRITE strategy_brief.json

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify project folder exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Arc Selection Guide", status: "completed" },
    { id: "step-3", description: "STEP 3: SCAN - Answer 5 diagnosis questions", status: "completed" },
    { id: "step-4", description: "STEP 4: DETECT - Apply arc decision tree", status: "completed" },
    { id: "step-5", description: "STEP 5A: BUILD narrative_dna - Extract structural framework", status: "completed" },
    { id: "step-5", description: "STEP 5B: DISTILL spr_text - Compress to 48-60 word priming", status: "completed" },
    { id: "step-5", description: "STEP 5C: WRITE strategy_brief.json - Save output file", status: "in_progress" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm 13 quality gates", status: "pending" }
  ]
});
```

**PURPOSE:** Combine all components and save the strategy_brief.json file.

**ACTIONS:**

Create this file: `production/Coach Adele/{project_id}/{project_id}_strategy_brief.json`

**⚠️ CRITICAL: COPY THIS EXACT TEMPLATE AND FILL IN EVERY FIELD:**

```json
{
  "project_id": "{project_id}",
  "selected_arc": "The [Arc Name]",
  "arc_confidence": 0.85,
  "unified_frame_statement": "[EXACTLY 20-25 WORDS - Count them. Must include: PROTAGONIST + COACH + MECHANISM + PROBLEM + RESULT]",
  "protagonist_voice": {
    "name": "[Client Name from transcript]",
    "role": "client"
  },
  "narrative_dna": {
    "mission": "DECODE_[ARC_TYPE]_TRANSFORMATION",
    "root_concept": "[2-4 words with underscores, e.g., Caregiver_Burnout_to_Sovereignty]",
    "state_alpha": {
      "identity": "(Self == [3-5 word identity code, e.g., Exhausted_Caregiver])",
      "loop": "{[Stage1] -> [Stage2] -> [Stage3] -> Repeat}",
      "internal_monologue": "[VERBATIM quote from transcript, 5-12 words, in quotes]",
      "sensory_anchor": "[Specific physical detail from BEFORE period, 5-10 words]"
    },
    "the_abyss": {
      "event": "[CAPSLOCK_Event_Name, e.g., Medical_System_Failure]",
      "sensation": "([Physical1], [Physical2])",
      "realization": "[VERBATIM insight quote from transcript, 5-15 words]"
    },
    "the_spark": {
      "trigger": "[Coach-related moment, e.g., Maman_Adele_First_Session]",
      "shift_type": "[One of: Logic_Collapse | Permission_Granted | Mirror_Moment | Root_Cause_Reveal | Framework_Gift]",
      "insight_quote": "[VERBATIM from transcript with timestamp, e.g., 'J'ai appris à m'écouter' (12:34)]"
    },
    "state_omega": {
      "identity": "(Self == [New identity, 3-5 words, e.g., Holistic_Healer_of_Self])",
      "action": "[What they do differently now, 5-10 words]",
      "result": "[MEASURABLE outcome with NUMBER, e.g., 'Anger from -5 to +3 on emotional scale']"
    },
    "sensory_anchors": [
      "[Physical detail from BEFORE, 5-10 words]",
      "[Physical detail from TURNING POINT, 5-10 words]",
      "[Physical detail from NOW, 5-10 words]"
    ],
    "coach_role": {
      "function": "[One of: Framework | Permission | Mirror | Challenge | Witness | Safe_Harbor]",
      "method_named": "[Specific technique from transcript, or 'NULL' if not mentioned]",
      "presence_type": "[One of: Guide | Challenger | Witness | Safe_Harbor | Teacher | Healer]"
    }
  },
  "spr_text": "[EXACTLY 48-60 WORDS - See SPR Generation Rules below]"
}
```

---

### 🧠 SPR TEXT GENERATION (LATENT SPACE PRIMING)

**Purpose:** The `spr_text` field is a Sparse Priming Representation — a distilled 48-60 word text that activates the LLM's latent space to extract relevant quotes.

**Theory:** LLMs embed knowledge in latent space. The right words *prime* the model to think in a certain way. This SPR text primes the Hunter to find quotes matching the transformation narrative.

**SPR Generation Rules:**

| Rule | Requirement |
|------|-------------|
| **Word Count** | EXACTLY 48-60 words (count before writing) |
| **Sentences** | 4-6 complete sentences |
| **Emotional Grounding** | Show how the speaker FEELS, not just thinks |
| **Verbatim Language** | Use words/phrases from the transcript itself |
| **Associations** | Include metaphors, analogies from the transcript |
| **Compression** | Capture maximum meaning with minimum words |

**SPR Structure Template:**

```
[STATE_BEFORE: 1 sentence describing the felt experience of suffering]
[ABYSS: 1 sentence capturing the breaking point sensation]
[SPARK: 1 sentence with the coach-triggered insight]
[STATE_AFTER: 1 sentence describing the new felt experience]
[PROOF: 1 sentence with measurable transformation]
[GIFT: 1 sentence about what they now offer/share]
```

**Example SPR (The Witness Arc):**

> "She dragged through days like a zombie, coffee crashing by noon, exhaustion her only companion. The moment the doctor said 'nothing wrong,' she broke—body screaming what tests couldn't measure. Maman Adele saw what medicine missed: the liver holding years of suppressed anger. Now she listens to her body first. Energy climbed from 3 to 8. She teaches her children to feel before they fix."

**Word count: 56 words ✅**

**Another Example (The Breakthrough Arc):**

> "He performed perfection while dying inside, chest tight in every meeting, panic his silent partner. The boardroom attack stripped the armor—vulnerability exposed, control lost. His daughter's question pierced the facade: 'Daddy, are you sad?' Permission to stop performing arrived like relief. Panic attacks dissolved from weekly to zero. He now models presence, not perfection, for his team."

**Word count: 54 words ✅**

---

**FIELD REQUIREMENTS (MANDATORY):**

| Field | Word Count | Format | Example |
|-------|------------|--------|---------|
| `unified_frame_statement` | EXACTLY 20-25 words | Full sentence | "Audrey shares her transformation with Maman Adele, showing how holistic healing helped her overcome chronic anger and achieve inner peace." |
| `root_concept` | 2-4 words | Underscored | `Anger_to_Peace` |
| `identity` (both) | 3-5 words | `(Self == X)` | `(Self == Exhausted_Caregiver)` |
| `loop` | 4 stages | `{A -> B -> C -> Repeat}` | `{Hide_Pain -> Push_Through -> Flare -> Repeat}` |
| `internal_monologue` | 5-12 words | VERBATIM in quotes | `"My body is failing me."` |
| `sensory_anchor` (all 4) | 5-10 words each | Physical detail | `"The weight in her shoulders every morning"` |
| `result` | MUST contain NUMBER | Measurable | `"Energy from 3/10 to 8/10"` |
| **`spr_text`** | **EXACTLY 48-60 words** | 4-6 complete sentences | See examples above |

**VERBATIM RULES:**
- `internal_monologue`: MUST be exact quote from transcript
- `realization`: MUST be exact quote from transcript
- `insight_quote`: MUST be exact quote WITH TIMESTAMP
- `spr_text`: Use transcript language/metaphors when possible
- If quote not found, write: `"[INSUFFICIENT_DATA]"`

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify project folder exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Arc Selection Guide", status: "completed" },
    { id: "step-3", description: "STEP 3: SCAN - Answer 5 diagnosis questions", status: "completed" },
    { id: "step-4", description: "STEP 4: DETECT - Apply arc decision tree", status: "completed" },
    { id: "step-5", description: "STEP 5: GENERATE - Create strategy_brief.json", status: "completed" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm quality gates", status: "pending" }
  ]
});
```

---

## STEP 6: VALIDATION

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify project folder exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Arc Selection Guide", status: "completed" },
    { id: "step-3", description: "STEP 3: SCAN - Answer 5 diagnosis questions", status: "completed" },
    { id: "step-4", description: "STEP 4: DETECT - Apply arc decision tree", status: "completed" },
    { id: "step-5", description: "STEP 5: GENERATE - Create strategy_brief.json", status: "completed" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm quality gates", status: "in_progress" }
  ]
});
```

**ACTIONS:**

Run these **12 validation checks** (ALL MUST PASS):

### Core Checks
| # | Check | Requirement | Regex/Pattern | Result |
|---|-------|-------------|---------------|--------|
| 1 | `selected_arc` | One of 13 valid arcs | `The (Witness\|Breakthrough\|...)` | ✅/❌ |
| 2 | `arc_confidence` | ≥ 0.75 | Number check | ✅/❌ |
| 3 | `unified_frame_statement` | 20-25 words | Word count | ✅/❌ |
| 4 | JSON syntax | Valid, no errors | Parse test | ✅/❌ |

### Narrative DNA Structure Checks
| # | Check | Requirement | Pattern | Result |
|---|-------|-------------|---------|--------|
| 5 | `narrative_dna.state_alpha.identity` | Format: `(Self == X)` | `\(Self == .+\)` | ✅/❌ |
| 6 | `narrative_dna.state_alpha.loop` | Format: `{A -> B -> C -> Repeat}` | `\{.+ -> .+ -> .+ -> Repeat\}` | ✅/❌ |
| 7 | `narrative_dna.state_omega.result` | Contains a NUMBER | `\d+` | ✅/❌ |
| 8 | `narrative_dna.sensory_anchors` | Array with 3 items | Length check | ✅/❌ |
| 9 | `narrative_dna.coach_role.function` | Valid enum value | One of 6 allowed | ✅/❌ |

### Verbatim Checks
| # | Check | Requirement | Verification | Result |
|---|-------|-------------|--------------|--------|
| 10 | `internal_monologue` | 5-12 words, in quotes | Word count | ✅/❌ |
| 11 | `insight_quote` | Contains timestamp `(HH:MM)` | `\(\d{1,2}:\d{2}\)` | ✅/❌ |
| 12 | No `[PLACEHOLDER]` text | All fields filled | No brackets except `[INSUFFICIENT_DATA]` | ✅/❌ |

### SPR Text Check
| # | Check | Requirement | Verification | Result |
|---|-------|-------------|--------------|--------|
| 13 | `spr_text` | EXACTLY 48-60 words | Word count | ✅/❌ |

**VALIDATION OUTPUT (copy and fill):**

```markdown
## VALIDATION RESULTS

### Core (4/4 required)
- [ ] 1. selected_arc: [✅/❌] [value]
- [ ] 2. arc_confidence: [✅/❌] [value]
- [ ] 3. unified_frame_statement: [✅/❌] [word count]
- [ ] 4. JSON syntax: [✅/❌]

### Narrative DNA (5/5 required)
- [ ] 5. state_alpha.identity format: [✅/❌]
- [ ] 6. state_alpha.loop format: [✅/❌]
- [ ] 7. state_omega.result has NUMBER: [✅/❌]
- [ ] 8. sensory_anchors has 3 items: [✅/❌]
- [ ] 9. coach_role.function valid: [✅/❌]

### Verbatim (3/3 required)
- [ ] 10. internal_monologue word count: [✅/❌] [count]
- [ ] 11. insight_quote has timestamp: [✅/❌]
- [ ] 12. No unfilled placeholders: [✅/❌]

**TOTAL: [X]/12 PASSED**
```

**IF ANY CHECK FAILS:** STOP → Report which check failed → Fix before proceeding

**IF ALL 12 CHECKS PASS:**

**OUTPUT (30-40 words):**
```
✅ DIAGNOSIS COMPLETE (12/12 validations passed)
- Arc: The [Name] (confidence: X.XX)
- Narrative DNA: ✅ Complete (all 5 blocks)
- Sensory Anchors: 3/3
- File: {project_id}_strategy_brief.json created
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify project folder exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Arc Selection Guide", status: "completed" },
    { id: "step-3", description: "STEP 3: SCAN - Answer 5 diagnosis questions", status: "completed" },
    { id: "step-4", description: "STEP 4: DETECT - Apply arc decision tree", status: "completed" },
    { id: "step-5", description: "STEP 5: GENERATE - Create strategy_brief.json", status: "completed" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm quality gates", status: "completed" }
  ]
});
```

---

## 🔗 NEXT STEPS

1. Run Brand Avatar: `python tools/generate_brand_avatar.py --path "{PROJECT_PATH}"`
2. Proceed to: `/cmf-hunt {project_id}`




---

## 📋 Step Execution Protocol (MANDATORY)

> [!CAUTION]
> **You MUST call `write_todos` at EVERY step transition.**
> This is not optional. Skipping todo updates = workflow failure.

**For EACH step, follow this pattern:**

1. **START STEP:** Update todo status to `in_progress`
2. **EXECUTE:** Perform the step actions
3. **VALIDATE:** Verify outputs exist
4. **COMPLETE STEP:** Update todo status to `completed`

**Status Update Template:**
```javascript
// When STARTING Step N:
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: ...", status: "completed" },
    { id: "step-2", description: "STEP 2: ...", status: "in_progress" },  // <- Current
    { id: "step-3", description: "STEP 3: ...", status: "pending" },
  ]
});
```

> [!IMPORTANT]
> **Validation Gate:** Before marking a step `completed`, verify:
> - Output file exists (if applicable)
> - Output matches expected schema
> - No error messages encountered

