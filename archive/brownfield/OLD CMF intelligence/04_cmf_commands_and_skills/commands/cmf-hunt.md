---
name: cmf-hunt
description: Quote Mining using arc-specific Hunter skill + Scoring Rubric
---

# /cmf-hunt {project_id}

// turbo-all

> **SKILLS_BASE:** `skills/cmf/`
> **SCORING_BASE:** `intelligence/frameworks/viral_scoring/`

**Objective:** Extract 24-32 verbatim quotes using arc-specific Hunter skill and scoring rubric.

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify files exist", status: "pending" },
    { id: "step-2", description: "STEP 2A: LOAD narrative_dna - Extract structural targeting", status: "pending" },
    { id: "step-2", description: "STEP 2B: LOAD spr_text - PRIME LATENT SPACE", status: "pending" },
    { id: "step-2", description: "STEP 2C: VALIDATE narrative_dna - 5-point checklist", status: "pending" },
    { id: "step-3", description: "STEP 3: LOAD HUNTER - Read arc-specific skill file", status: "pending" },
    { id: "step-4", description: "STEP 4: LOAD RUBRIC - Read scoring rubric file", status: "pending" },
    { id: "step-5", description: "STEP 5: EXECUTE PRIMED HUNT - Extract 24-32 targeted quotes", status: "pending" },
    { id: "step-6", description: "STEP 6: SCORE QUOTES - Apply S+E+Sp scoring", status: "pending" },
    { id: "step-7", description: "STEP 7: GENERATE OUTPUT - Create Quote_Manifest.md", status: "pending" },
    { id: "step-8", description: "STEP 8: VALIDATE - Confirm quality gates", status: "pending" }
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
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify files exist", status: "in_progress" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "pending" },
    { id: "step-3", description: "STEP 3: LOAD HUNTER - Read arc-specific skill file", status: "pending" },
    { id: "step-4", description: "STEP 4: LOAD RUBRIC - Read scoring rubric file", status: "pending" },
    { id: "step-5", description: "STEP 5: EXECUTE HUNT - Extract 24-32 verbatim quotes", status: "pending" },
    { id: "step-6", description: "STEP 6: SCORE QUOTES - Apply S+E+Sp scoring", status: "pending" },
    { id: "step-7", description: "STEP 7: GENERATE OUTPUT - Create Quote_Manifest.md", status: "pending" },
    { id: "step-8", description: "STEP 8: VALIDATE - Confirm quality gates", status: "pending" }
  ]
});
```

**ACTIONS:**

| # | Check | Path | If Missing |
|---|-------|------|------------|
| 1 | Project folder | `production/Coach Adele/{project_id}/` | STOP |
| 2 | Strategy brief | `{project_id}_strategy_brief.json` | STOP → Run `/cmf-diagnose` first |
| 3 | Transcript | `{project_id}_transcript.md` or `.srt` | STOP |

**OUTPUT (30-50 words):**
```
PRE-FLIGHT COMPLETE:
- Folder: ✅ Found
- Strategy Brief: ✅ Found (Arc: The [Name])
- Transcript: ✅ Found ({X} words)
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify files exist", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "pending" },
    { id: "step-3", description: "STEP 3: LOAD HUNTER - Read arc-specific skill file", status: "pending" },
    { id: "step-4", description: "STEP 4: LOAD RUBRIC - Read scoring rubric file", status: "pending" },
    { id: "step-5", description: "STEP 5: EXECUTE HUNT - Extract 24-32 verbatim quotes", status: "pending" },
    { id: "step-6", description: "STEP 6: SCORE QUOTES - Apply S+E+Sp scoring", status: "pending" },
    { id: "step-7", description: "STEP 7: GENERATE OUTPUT - Create Quote_Manifest.md", status: "pending" },
    { id: "step-8", description: "STEP 8: VALIDATE - Confirm quality gates", status: "pending" }
  ]
});
```

---

## STEP 2A: LOAD narrative_dna

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify files exist", status: "completed" },
    { id: "step-2", description: "STEP 2A: LOAD narrative_dna - Extract structural targeting", status: "in_progress" },
    { id: "step-2", description: "STEP 2B: LOAD spr_text - PRIME LATENT SPACE", status: "pending" },
    { id: "step-2", description: "STEP 2C: VALIDATE narrative_dna - 5-point checklist", status: "pending" },
    { id: "step-3", description: "STEP 3: LOAD HUNTER - Read arc-specific skill file", status: "pending" },
    { id: "step-4", description: "STEP 4: LOAD RUBRIC - Read scoring rubric file", status: "pending" },
    { id: "step-5", description: "STEP 5: EXECUTE PRIMED HUNT - Extract 24-32 targeted quotes", status: "pending" },
    { id: "step-6", description: "STEP 6: SCORE QUOTES - Apply S+E+Sp scoring", status: "pending" },
    { id: "step-7", description: "STEP 7: GENERATE OUTPUT - Create Quote_Manifest.md", status: "pending" },
    { id: "step-8", description: "STEP 8: VALIDATE - Confirm quality gates", status: "pending" }
  ]
});
```

**PURPOSE:** Load structural transformation framework for quote targeting.

**ACTIONS:**

1. Read `{project_id}_strategy_brief.json`
2. Extract these structural components:

| Field | Value | Purpose |
|-------|-------|---------|
| `selected_arc` | | Determines which Hunter skill to load |
| `narrative_dna.root_concept` | | Core transformation theme |
| `narrative_dna.state_alpha.sensory_anchor` | | Target for W2 (PROBLEM) quotes |
| `narrative_dna.the_spark.insight_quote` | | MUST appear in W3 (MECHANISM) |
| `narrative_dna.state_omega.result` | | Target for W4 (PROOF) quotes |
| `narrative_dna.coach_role.method_named` | | Look for technique mentions |

**OUTPUT:** List the extracted values.

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify files exist", status: "completed" },
    { id: "step-2", description: "STEP 2A: LOAD narrative_dna - Extract structural targeting", status: "completed" },
    { id: "step-2", description: "STEP 2B: LOAD spr_text - PRIME LATENT SPACE", status: "pending" },
    { id: "step-2", description: "STEP 2C: VALIDATE narrative_dna - 5-point checklist", status: "pending" },
    { id: "step-3", description: "STEP 3: LOAD HUNTER - Read arc-specific skill file", status: "pending" },
    { id: "step-4", description: "STEP 4: LOAD RUBRIC - Read scoring rubric file", status: "pending" },
    { id: "step-5", description: "STEP 5: EXECUTE PRIMED HUNT - Extract 24-32 targeted quotes", status: "pending" },
    { id: "step-6", description: "STEP 6: SCORE QUOTES - Apply S+E+Sp scoring", status: "pending" },
    { id: "step-7", description: "STEP 7: GENERATE OUTPUT - Create Quote_Manifest.md", status: "pending" },
    { id: "step-8", description: "STEP 8: VALIDATE - Confirm quality gates", status: "pending" }
  ]
});
```

---

## STEP 2B: LOAD spr_text (PRIME LATENT SPACE)

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify files exist", status: "completed" },
    { id: "step-2", description: "STEP 2A: LOAD narrative_dna - Extract structural targeting", status: "completed" },
    { id: "step-2", description: "STEP 2B: LOAD spr_text - PRIME LATENT SPACE", status: "in_progress" },
    { id: "step-2", description: "STEP 2C: VALIDATE narrative_dna - 5-point checklist", status: "pending" },
    { id: "step-3", description: "STEP 3: LOAD HUNTER - Read arc-specific skill file", status: "pending" },
    { id: "step-4", description: "STEP 4: LOAD RUBRIC - Read scoring rubric file", status: "pending" },
    { id: "step-5", description: "STEP 5: EXECUTE PRIMED HUNT - Extract 24-32 targeted quotes", status: "pending" },
    { id: "step-6", description: "STEP 6: SCORE QUOTES - Apply S+E+Sp scoring", status: "pending" },
    { id: "step-7", description: "STEP 7: GENERATE OUTPUT - Create Quote_Manifest.md", status: "pending" },
    { id: "step-8", description: "STEP 8: VALIDATE - Confirm quality gates", status: "pending" }
  ]
});
```

**PURPOSE:** Load the SPR text to prime your latent space for targeted quote extraction.

**⚠️ CRITICAL PRIMING INSTRUCTION:**

The `spr_text` field contains a 48-60 word Sparse Priming Representation. By reading this text, your latent space is now PRIMED to recognize quotes matching this transformation narrative.

**READ THIS SPR TEXT ALOUD IN YOUR CONTEXT:**

```
spr_text: "[Copy the spr_text value here]"
```

**PRIMING EFFECT:**

After loading spr_text, your quote extraction will be "aimed" at:
- Quotes matching the STATE_BEFORE feelings/sensations
- Quotes matching the ABYSS breaking point
- Quotes matching the SPARK insight (especially coach moments)
- Quotes matching the STATE_AFTER transformation
- Quotes with measurable PROOF metrics

**The spr_text is now in your context. Your quote extraction is PRIMED to find quotes matching these associations.**

**OUTPUT:** Confirm spr_text loaded (48-60 words).

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify files exist", status: "completed" },
    { id: "step-2", description: "STEP 2A: LOAD narrative_dna - Extract structural targeting", status: "completed" },
    { id: "step-2", description: "STEP 2B: LOAD spr_text - PRIME LATENT SPACE", status: "completed" },
    { id: "step-2", description: "STEP 2C: VALIDATE narrative_dna - 5-point checklist", status: "pending" },
    { id: "step-3", description: "STEP 3: LOAD HUNTER - Read arc-specific skill file", status: "pending" },
    { id: "step-4", description: "STEP 4: LOAD RUBRIC - Read scoring rubric file", status: "pending" },
    { id: "step-5", description: "STEP 5: EXECUTE PRIMED HUNT - Extract 24-32 targeted quotes", status: "pending" },
    { id: "step-6", description: "STEP 6: SCORE QUOTES - Apply S+E+Sp scoring", status: "pending" },
    { id: "step-7", description: "STEP 7: GENERATE OUTPUT - Create Quote_Manifest.md", status: "pending" },
    { id: "step-8", description: "STEP 8: VALIDATE - Confirm quality gates", status: "pending" }
  ]
});
```

---

## STEP 2C: VALIDATE narrative_dna

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify files exist", status: "completed" },
    { id: "step-2", description: "STEP 2A: LOAD narrative_dna - Extract structural targeting", status: "completed" },
    { id: "step-2", description: "STEP 2B: LOAD spr_text - PRIME LATENT SPACE", status: "completed" },
    { id: "step-2", description: "STEP 2C: VALIDATE narrative_dna - 5-point checklist", status: "in_progress" },
    { id: "step-3", description: "STEP 3: LOAD HUNTER - Read arc-specific skill file", status: "pending" },
    { id: "step-4", description: "STEP 4: LOAD RUBRIC - Read scoring rubric file", status: "pending" },
    { id: "step-5", description: "STEP 5: EXECUTE PRIMED HUNT - Extract 24-32 targeted quotes", status: "pending" },
    { id: "step-6", description: "STEP 6: SCORE QUOTES - Apply S+E+Sp scoring", status: "pending" },
    { id: "step-7", description: "STEP 7: GENERATE OUTPUT - Create Quote_Manifest.md", status: "pending" },
    { id: "step-8", description: "STEP 8: VALIDATE - Confirm quality gates", status: "pending" }
  ]
});
```

**PURPOSE:** Validate narrative_dna structure before hunting.

**5-POINT VALIDATION CHECKLIST:**

```markdown
## NARRATIVE DNA VALIDATION
- [ ] 1. `state_alpha.identity` format: (Self == X) → [✅/❌]
- [ ] 2. `state_alpha.loop` format: {A -> B -> C -> Repeat} → [✅/❌]
- [ ] 3. `state_omega.result` has NUMBER → [✅/❌]
- [ ] 4. `sensory_anchors` has 3 items → [✅/❌]
- [ ] 5. `spr_text` is 48-60 words → [✅/❌]
```

**IF ANY VALIDATION FAILS:** STOP → Report → Run `/cmf-diagnose` again to fix

**OUTPUT (50-80 words):**
```
PRIMING COMPLETE:
- Arc: The [Name]
- Root Concept: [underscored_phrase]
- State Alpha Loop: {[A] -> [B] -> [C] -> Repeat}
- Target Metrics: [state_omega.result value]
- spr_text: [X] words loaded ✅

LATENT SPACE PRIMED:
- Sensory Anchors: 3/3 loaded
- Insight Quote: "[quote]" → Target for W3 cluster
- All 5 validations passed ✅
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify files exist", status: "completed" },
    { id: "step-2", description: "STEP 2A: LOAD narrative_dna - Extract structural targeting", status: "completed" },
    { id: "step-2", description: "STEP 2B: LOAD spr_text - PRIME LATENT SPACE", status: "completed" },
    { id: "step-2", description: "STEP 2C: VALIDATE narrative_dna - 5-point checklist", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD HUNTER - Read arc-specific skill file", status: "pending" },
    { id: "step-4", description: "STEP 4: LOAD RUBRIC - Read scoring rubric file", status: "pending" },
    { id: "step-5", description: "STEP 5: EXECUTE PRIMED HUNT - Extract 24-32 targeted quotes", status: "pending" },
    { id: "step-6", description: "STEP 6: SCORE QUOTES - Apply S+E+Sp scoring", status: "pending" },
    { id: "step-7", description: "STEP 7: GENERATE OUTPUT - Create Quote_Manifest.md", status: "pending" },
    { id: "step-8", description: "STEP 8: VALIDATE - Confirm quality gates", status: "pending" }
  ]
});
```

---

## STEP 3: LOAD HUNTER SKILL

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify files exist", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD HUNTER - Read arc-specific skill file", status: "in_progress" },
    { id: "step-4", description: "STEP 4: LOAD RUBRIC - Read scoring rubric file", status: "pending" },
    { id: "step-5", description: "STEP 5: EXECUTE HUNT - Extract 24-32 verbatim quotes", status: "pending" },
    { id: "step-6", description: "STEP 6: SCORE QUOTES - Apply S+E+Sp scoring", status: "pending" },
    { id: "step-7", description: "STEP 7: GENERATE OUTPUT - Create Quote_Manifest.md", status: "pending" },
    { id: "step-8", description: "STEP 8: VALIDATE - Confirm quality gates", status: "pending" }
  ]
});
```

**ROUTING TABLE:**

| Arc | Skill Path |
|-----|------------|
| The Witness | `skills/cmf/hunters/witness-hunter/SKILL.md` |
| The Breakthrough | `skills/cmf/hunters/breakthrough-hunter/SKILL.md` |
| The Shared Struggle | `skills/cmf/hunters/shared-struggle-hunter/SKILL.md` |
| The Confrontation | `skills/cmf/hunters/confrontation-hunter/SKILL.md` |
| The Core Transformation | `skills/cmf/hunters/core-transformation-hunter/SKILL.md` |
| The Warning | `skills/cmf/hunters/warning-hunter/SKILL.md` |
| The Rally | `skills/cmf/hunters/rally-hunter/SKILL.md` |
| The Divine Spark | `skills/cmf/hunters/divine-spark-hunter/SKILL.md` |
| The Call to Adventure | `skills/cmf/hunters/call-to-adventure-hunter/SKILL.md` |
| The Ticking Clock | `skills/cmf/hunters/ticking-clock-hunter/SKILL.md` |
| The Comedic Reframe | `skills/cmf/hunters/comedic-reframe-hunter/SKILL.md` |
| The Sacred Return | `skills/cmf/hunters/sacred-return-hunter/SKILL.md` |
| The Quiet Reflection | `skills/cmf/hunters/quiet-reflection-hunter/SKILL.md` |

**ACTIONS:**

1. Based on `selected_arc`, find the correct skill path from table above
2. Read the FULL skill file (do NOT summarize, do NOT skip sections)
3. Extract the cluster definitions for this arc

**OUTPUT (40-60 words):**
```
HUNTER SKILL LOADED:
- File: skills/cmf/hunters/[arc]-hunter/SKILL.md
- Clusters: [List the cluster names, e.g., W1_HOOK, W2_PAIN, W3_SOLUTION, W4_PROOF, W5_CLOSE]
- Quote targets per cluster: [X-Y quotes each]
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify files exist", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD HUNTER - Read arc-specific skill file", status: "completed" },
    { id: "step-4", description: "STEP 4: LOAD RUBRIC - Read scoring rubric file", status: "pending" },
    { id: "step-5", description: "STEP 5: EXECUTE HUNT - Extract 24-32 verbatim quotes", status: "pending" },
    { id: "step-6", description: "STEP 6: SCORE QUOTES - Apply S+E+Sp scoring", status: "pending" },
    { id: "step-7", description: "STEP 7: GENERATE OUTPUT - Create Quote_Manifest.md", status: "pending" },
    { id: "step-8", description: "STEP 8: VALIDATE - Confirm quality gates", status: "pending" }
  ]
});
```

---

## STEP 4: LOAD SCORING RUBRIC

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify files exist", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD HUNTER - Read arc-specific skill file", status: "completed" },
    { id: "step-4", description: "STEP 4: LOAD RUBRIC - Read scoring rubric file", status: "in_progress" },
    { id: "step-5", description: "STEP 5: EXECUTE HUNT - Extract 24-32 verbatim quotes", status: "pending" },
    { id: "step-6", description: "STEP 6: SCORE QUOTES - Apply S+E+Sp scoring", status: "pending" },
    { id: "step-7", description: "STEP 7: GENERATE OUTPUT - Create Quote_Manifest.md", status: "pending" },
    { id: "step-8", description: "STEP 8: VALIDATE - Confirm quality gates", status: "pending" }
  ]
});
```

**ACTIONS:**

1. Read rubric file: `intelligence/frameworks/viral_scoring/{arc}_scoring.md`
2. Extract:
   - Minimum thresholds per cluster
   - Scoring weights (Surprise/Emotion/Specificity)
   - Arc-specific ladders (e.g., Proof Specificity Ladder)

**OUTPUT (50-70 words):**
```
SCORING RUBRIC LOADED:
- File: intelligence/frameworks/viral_scoring/[arc]_scoring.md
- Cluster thresholds:
  - W1_HOOK: ≥22/30
  - W2_PAIN: ≥20/30
  - W3_SOLUTION: ≥18/30
  - W4_PROOF: ≥24/30
  - W5_CLOSE: ≥20/30
- Special rules: [Arc-specific requirements]
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify files exist", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD HUNTER - Read arc-specific skill file", status: "completed" },
    { id: "step-4", description: "STEP 4: LOAD RUBRIC - Read scoring rubric file", status: "completed" },
    { id: "step-5", description: "STEP 5: EXECUTE HUNT - Extract 24-32 verbatim quotes", status: "pending" },
    { id: "step-6", description: "STEP 6: SCORE QUOTES - Apply S+E+Sp scoring", status: "pending" },
    { id: "step-7", description: "STEP 7: GENERATE OUTPUT - Create Quote_Manifest.md", status: "pending" },
    { id: "step-8", description: "STEP 8: VALIDATE - Confirm quality gates", status: "pending" }
  ]
});
```

---

## STEP 5: EXECUTE HUNT

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify files exist", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD HUNTER - Read arc-specific skill file", status: "completed" },
    { id: "step-4", description: "STEP 4: LOAD RUBRIC - Read scoring rubric file", status: "completed" },
    { id: "step-5", description: "STEP 5: EXECUTE HUNT - Extract 24-32 verbatim quotes", status: "in_progress" },
    { id: "step-6", description: "STEP 6: SCORE QUOTES - Apply S+E+Sp scoring", status: "pending" },
    { id: "step-7", description: "STEP 7: GENERATE OUTPUT - Create Quote_Manifest.md", status: "pending" },
    { id: "step-8", description: "STEP 8: VALIDATE - Confirm quality gates", status: "pending" }
  ]
});
```

**VERBATIM MODE RULES:**

> ⚠️ **"If it is not in the timecode, it does not exist."**

| Rule | Requirement |
|------|-------------|
| 1 | **EXACT QUOTES ONLY** — Copy character-for-character from transcript |
| 2 | **TIMESTAMP REQUIRED** — Every quote must have `start_time` and `end_time` |
| 3 | **MINIMUM LENGTH** — Each quote ≥15 words AND ≥5 seconds |
| 4 | **NO HALLUCINATION** — If cluster empty, report `[MISSING_DATA]` |

**QUOTA:**
- Minimum: 24 quotes
- Target: 28 quotes  
- Maximum: 32 quotes

**FOR EACH QUOTE, EXTRACT (60-100 words per quote):**

```markdown
### Quote [CLUSTER].[NUMBER]

- **Text:** "[Exact verbatim quote, 15-40 words, character-for-character from transcript]"
- **Start:** 00:04:15
- **End:** 00:04:22
- **Duration:** 7s
- **Words:** 23
```

**OUTPUT:** 24-32 quotes extracted in the format above

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify files exist", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD HUNTER - Read arc-specific skill file", status: "completed" },
    { id: "step-4", description: "STEP 4: LOAD RUBRIC - Read scoring rubric file", status: "completed" },
    { id: "step-5", description: "STEP 5: EXECUTE HUNT - Extract 24-32 verbatim quotes", status: "completed" },
    { id: "step-6", description: "STEP 6: SCORE QUOTES - Apply S+E+Sp scoring", status: "pending" },
    { id: "step-7", description: "STEP 7: GENERATE OUTPUT - Create Quote_Manifest.md", status: "pending" },
    { id: "step-8", description: "STEP 8: VALIDATE - Confirm quality gates", status: "pending" }
  ]
});
```

---

## STEP 6: SCORE QUOTES

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify files exist", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD HUNTER - Read arc-specific skill file", status: "completed" },
    { id: "step-4", description: "STEP 4: LOAD RUBRIC - Read scoring rubric file", status: "completed" },
    { id: "step-5", description: "STEP 5: EXECUTE HUNT - Extract 24-32 verbatim quotes", status: "completed" },
    { id: "step-6", description: "STEP 6: SCORE QUOTES - Apply S+E+Sp scoring", status: "in_progress" },
    { id: "step-7", description: "STEP 7: GENERATE OUTPUT - Create Quote_Manifest.md", status: "pending" },
    { id: "step-8", description: "STEP 8: VALIDATE - Confirm quality gates", status: "pending" }
  ]
});
```

**APPLY TO EACH QUOTE:**

| Dimension | Range | What to Evaluate |
|-----------|-------|------------------|
| **S (Surprise)** | 1-10 | Unexpectedness, revelation, flip |
| **E (Emotion)** | 1-10 | Vulnerability depth, visceral feeling |
| **Sp (Specificity)** | 1-10 | Concrete details, numbers, names |

**VIRAL SCORE = S + E + Sp (out of 30)**

**FOR EACH QUOTE, ADD (30-50 words per score):**

```markdown
- **Viral Score:** 24/30 (S:7 E:8 Sp:9)
  - Surprise: 7 — [10-15 word justification]
  - Emotion: 8 — [10-15 word justification]
  - Specificity: 9 — [10-15 word justification]
```

**MINIMUM THRESHOLDS (from rubric):**
- W1/HOOK: ≥22/30
- W4/PROOF: ≥24/30
- All others: ≥18/30

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify files exist", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD HUNTER - Read arc-specific skill file", status: "completed" },
    { id: "step-4", description: "STEP 4: LOAD RUBRIC - Read scoring rubric file", status: "completed" },
    { id: "step-5", description: "STEP 5: EXECUTE HUNT - Extract 24-32 verbatim quotes", status: "completed" },
    { id: "step-6", description: "STEP 6: SCORE QUOTES - Apply S+E+Sp scoring", status: "completed" },
    { id: "step-7", description: "STEP 7: GENERATE OUTPUT - Create Quote_Manifest.md", status: "pending" },
    { id: "step-8", description: "STEP 8: VALIDATE - Confirm quality gates", status: "pending" }
  ]
});
```

---

## STEP 7: GENERATE OUTPUT

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify files exist", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD HUNTER - Read arc-specific skill file", status: "completed" },
    { id: "step-4", description: "STEP 4: LOAD RUBRIC - Read scoring rubric file", status: "completed" },
    { id: "step-5", description: "STEP 5: EXECUTE HUNT - Extract 24-32 verbatim quotes", status: "completed" },
    { id: "step-6", description: "STEP 6: SCORE QUOTES - Apply S+E+Sp scoring", status: "completed" },
    { id: "step-7", description: "STEP 7: GENERATE OUTPUT - Create Quote_Manifest.md", status: "in_progress" },
    { id: "step-8", description: "STEP 8: VALIDATE - Confirm quality gates", status: "pending" }
  ]
});
```

**CREATE FILE:** `production/Coach Adele/{project_id}/{project_id}_Quote_Manifest.md`

**USE THIS EXACT TEMPLATE (2500-3500 words total):**

```markdown
# Quote Manifest: {project_id}

**Arc:** The [Name]
**Generated:** [Date]
**Total Quotes:** [24-32]
**Scoring Rubric:** {arc}_scoring.md

---

## CLUSTER W1: HOOK (Min: 22/30)

### Quote W1.1
- **Text:** "[Exact verbatim, 15-40 words]"
- **Start:** 00:07:11
- **End:** 00:07:20
- **Duration:** 9s
- **Words:** 28
- **Viral Score:** 24/30 (S:7 E:8 Sp:9)
  - Surprise: 7 — [justification]
  - Emotion: 8 — [justification]
  - Specificity: 9 — [justification]

### Quote W1.2
[Same format...]

---

## CLUSTER W2: PAIN (Min: 20/30)

[Same format, 4-6 quotes...]

---

## CLUSTER W3: SOLUTION (Min: 18/30)

[Same format, 4-6 quotes...]

---

## CLUSTER W4: PROOF (Min: 24/30)

[Same format, 4-6 quotes...]

---

## CLUSTER W5: CLOSE (Min: 20/30)

[Same format, 4-6 quotes...]

---

## GAP ANALYSIS REPORT

| Cluster | Quotes | Avg Score | Meets Threshold |
|---------|--------|-----------|-----------------|
| W1 HOOK | 5 | 23.4/30 | ✅ |
| W2 PAIN | 6 | 21.2/30 | ✅ |
| W3 SOLUTION | 5 | 19.8/30 | ✅ |
| W4 PROOF | 6 | 25.1/30 | ✅ |
| W5 CLOSE | 4 | 22.0/30 | ✅ |
| **TOTAL** | **26** | **22.3/30** | — |

**Missing Data:** [List any clusters with insufficient quotes]
**Low Scores:** [List any quotes below threshold]
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify files exist", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD HUNTER - Read arc-specific skill file", status: "completed" },
    { id: "step-4", description: "STEP 4: LOAD RUBRIC - Read scoring rubric file", status: "completed" },
    { id: "step-5", description: "STEP 5: EXECUTE HUNT - Extract 24-32 verbatim quotes", status: "completed" },
    { id: "step-6", description: "STEP 6: SCORE QUOTES - Apply S+E+Sp scoring", status: "completed" },
    { id: "step-7", description: "STEP 7: GENERATE OUTPUT - Create Quote_Manifest.md", status: "completed" },
    { id: "step-8", description: "STEP 8: VALIDATE - Confirm quality gates", status: "pending" }
  ]
});
```

---

## STEP 8: VALIDATION

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify files exist", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD HUNTER - Read arc-specific skill file", status: "completed" },
    { id: "step-4", description: "STEP 4: LOAD RUBRIC - Read scoring rubric file", status: "completed" },
    { id: "step-5", description: "STEP 5: EXECUTE HUNT - Extract 24-32 verbatim quotes", status: "completed" },
    { id: "step-6", description: "STEP 6: SCORE QUOTES - Apply S+E+Sp scoring", status: "completed" },
    { id: "step-7", description: "STEP 7: GENERATE OUTPUT - Create Quote_Manifest.md", status: "completed" },
    { id: "step-8", description: "STEP 8: VALIDATE - Confirm quality gates", status: "in_progress" }
  ]
});
```

**RUN THESE 6 VALIDATION CHECKS:**

| # | Check | Requirement | Result |
|---|-------|-------------|--------|
| 1 | Quote Count | 24-32 quotes | ✅/❌ |
| 2 | All Timestamps | Every quote has start/end | ✅/❌ |
| 3 | Word Count | Each quote ≥15 words | ✅/❌ |
| 4 | Duration | Each quote ≥5 seconds | ✅/❌ |
| 5 | Scoring | All quotes have S/E/Sp | ✅/❌ |
| 6 | Thresholds | All clusters meet minimums | ✅/❌ |

**IF ANY CHECK FAILS:** STOP → Report failure → Suggest fix

**IF ALL PASS:**

**OUTPUT (30-40 words):**
```
✅ HUNT COMPLETE
- Quotes: [X] extracted
- Clusters: All 5 populated
- Thresholds: All met
- File: {project_id}_Quote_Manifest.md created (XXXX words)
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify files exist", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD HUNTER - Read arc-specific skill file", status: "completed" },
    { id: "step-4", description: "STEP 4: LOAD RUBRIC - Read scoring rubric file", status: "completed" },
    { id: "step-5", description: "STEP 5: EXECUTE HUNT - Extract 24-32 verbatim quotes", status: "completed" },
    { id: "step-6", description: "STEP 6: SCORE QUOTES - Apply S+E+Sp scoring", status: "completed" },
    { id: "step-7", description: "STEP 7: GENERATE OUTPUT - Create Quote_Manifest.md", status: "completed" },
    { id: "step-8", description: "STEP 8: VALIDATE - Confirm quality gates", status: "completed" }
  ]
});
```

---

## 🔗 NEXT COMMAND

`/cmf-analyze {project_id}`



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

