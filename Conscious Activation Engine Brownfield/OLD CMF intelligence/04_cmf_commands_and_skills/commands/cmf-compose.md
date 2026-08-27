---
name: cmf-compose
description: Premise assembly using arc-specific Composer skill
---

# /cmf-compose {project_id}

// turbo-all

> **SKILLS_BASE:** `skills/cmf/`

**Objective:** Assemble best quotes into 60-90 second premise narrative (800-1200 words output).

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify Quote_Manifest_Enriched.md exists", status: "pending" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "pending" },
    { id: "step-3", description: "STEP 3: LOAD COMPOSER - Read arc-specific composer skill", status: "pending" },
    { id: "step-4", description: "STEP 4: SELECT QUOTES - Choose best quotes using V3 tags", status: "pending" },
    { id: "step-5", description: "STEP 5: EXECUTE COMPOSITION - Assemble 60-90s premise", status: "pending" },
    { id: "step-6", description: "STEP 6: GENERATE OUTPUT - Create premise_analysis.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm duration and arc rules", status: "pending" }
  ]
});
```

---

## STEP 1: PRE-FLIGHT

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify Quote_Manifest_Enriched.md exists", status: "in_progress" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "pending" },
    { id: "step-3", description: "STEP 3: LOAD COMPOSER - Read arc-specific composer skill", status: "pending" },
    { id: "step-4", description: "STEP 4: SELECT QUOTES - Choose best quotes using V3 tags", status: "pending" },
    { id: "step-5", description: "STEP 5: EXECUTE COMPOSITION - Assemble 60-90s premise", status: "pending" },
    { id: "step-6", description: "STEP 6: GENERATE OUTPUT - Create premise_analysis.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm duration and arc rules", status: "pending" }
  ]
});
```

**ACTIONS:**

| Check | Path | If Missing |
|-------|------|------------|
| 1 | `{project_id}_Quote_Manifest_Enriched.md` | STOP → Run `/cmf-analyze` |
| 2 | `{project_id}_strategy_brief.json` | STOP → Run `/cmf-diagnose` |

**OUTPUT (20-30 words):**
```
PRE-FLIGHT COMPLETE:
- Enriched Manifest: ✅ Found ([X] quotes with V3 tags)
- Strategy Brief: ✅ Found (Arc: The [Name])
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify Quote_Manifest_Enriched.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "pending" },
    { id: "step-3", description: "STEP 3: LOAD COMPOSER - Read arc-specific composer skill", status: "pending" },
    { id: "step-4", description: "STEP 4: SELECT QUOTES - Choose best quotes using V3 tags", status: "pending" },
    { id: "step-5", description: "STEP 5: EXECUTE COMPOSITION - Assemble 60-90s premise", status: "pending" },
    { id: "step-6", description: "STEP 6: GENERATE OUTPUT - Create premise_analysis.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm duration and arc rules", status: "pending" }
  ]
});
```

---

## STEP 2: IDENTIFY ARC

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify Quote_Manifest_Enriched.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "in_progress" },
    { id: "step-3", description: "STEP 3: LOAD COMPOSER - Read arc-specific composer skill", status: "pending" },
    { id: "step-4", description: "STEP 4: SELECT QUOTES - Choose best quotes using V3 tags", status: "pending" },
    { id: "step-5", description: "STEP 5: EXECUTE COMPOSITION - Assemble 60-90s premise", status: "pending" },
    { id: "step-6", description: "STEP 6: GENERATE OUTPUT - Create premise_analysis.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm duration and arc rules", status: "pending" }
  ]
});
```

**ACTIONS:**
1. Read `{project_id}_strategy_brief.json`
2. Extract `selected_arc` and `spr`

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify Quote_Manifest_Enriched.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD COMPOSER - Read arc-specific composer skill", status: "pending" },
    { id: "step-4", description: "STEP 4: SELECT QUOTES - Choose best quotes using V3 tags", status: "pending" },
    { id: "step-5", description: "STEP 5: EXECUTE COMPOSITION - Assemble 60-90s premise", status: "pending" },
    { id: "step-6", description: "STEP 6: GENERATE OUTPUT - Create premise_analysis.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm duration and arc rules", status: "pending" }
  ]
});
```

---

## STEP 3: LOAD COMPOSER SKILL

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify Quote_Manifest_Enriched.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD COMPOSER - Read arc-specific composer skill", status: "in_progress" },
    { id: "step-4", description: "STEP 4: SELECT QUOTES - Choose best quotes using V3 tags", status: "pending" },
    { id: "step-5", description: "STEP 5: EXECUTE COMPOSITION - Assemble 60-90s premise", status: "pending" },
    { id: "step-6", description: "STEP 6: GENERATE OUTPUT - Create premise_analysis.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm duration and arc rules", status: "pending" }
  ]
});
```

**ROUTING TABLE:**

| Arc | Skill Path |
|-----|------------|
| The Witness | `skills/cmf/composers/witness-composer/SKILL.md` |
| The Breakthrough | `skills/cmf/composers/breakthrough-composer/SKILL.md` |
| [etc...] | |

**ACTIONS:**
1. Read the FULL composer skill file
2. Extract the VAE Decoder Protocol rules
3. Understand the cluster sequencing rules

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify Quote_Manifest_Enriched.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD COMPOSER - Read arc-specific composer skill", status: "completed" },
    { id: "step-4", description: "STEP 4: SELECT QUOTES - Choose best quotes using V3 tags", status: "pending" },
    { id: "step-5", description: "STEP 5: EXECUTE COMPOSITION - Assemble 60-90s premise", status: "pending" },
    { id: "step-6", description: "STEP 6: GENERATE OUTPUT - Create premise_analysis.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm duration and arc rules", status: "pending" }
  ]
});
```

---

## STEP 4: SELECT QUOTES

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify Quote_Manifest_Enriched.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD COMPOSER - Read arc-specific composer skill", status: "completed" },
    { id: "step-4", description: "STEP 4: SELECT QUOTES - Choose best quotes using V3 tags", status: "in_progress" },
    { id: "step-5", description: "STEP 5: EXECUTE COMPOSITION - Assemble 60-90s premise", status: "pending" },
    { id: "step-6", description: "STEP 6: GENERATE OUTPUT - Create premise_analysis.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm duration and arc rules", status: "pending" }
  ]
});
```

**SELECTION ALGORITHM:**

1. **START:** Select quote with highest THEMATIC_FIT for HOOK cluster
2. **FOLLOW:** Use HIGH_AFFINITY_SEQUENCES to find next quote
3. **CHECK:** Running total duration after each addition
4. **GLUE:** Insert highest GLUE_SCORE quotes as transitions
5. **END:** Select quote with highest THEMATIC_FIT for CLOSE cluster

**CONSTRAINTS:**
- Total duration: 60-90 seconds
- Max 3 quotes per cluster
- Prefer 3-5s fragments over 12s blocks
- Strong bookends (first and last quotes must score ≥22/30)

**OUTPUT (100-150 words):**
```
QUOTE SELECTION:
- SC01: [Quote W1.2] - 8s - Hook
- SC02: [Quote W2.3] - 6s - Pain
- SC03: [Quote W3.1] - 7s - Solution
- SC04: [Quote W4.2] - 9s - Proof
- SC05: [Quote W5.1] - 7s - Close
TOTAL: 67 seconds (5 scenes)
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify Quote_Manifest_Enriched.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD COMPOSER - Read arc-specific composer skill", status: "completed" },
    { id: "step-4", description: "STEP 4: SELECT QUOTES - Choose best quotes using V3 tags", status: "completed" },
    { id: "step-5", description: "STEP 5: EXECUTE COMPOSITION - Assemble 60-90s premise", status: "pending" },
    { id: "step-6", description: "STEP 6: GENERATE OUTPUT - Create premise_analysis.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm duration and arc rules", status: "pending" }
  ]
});
```

---

## STEP 5: EXECUTE COMPOSITION

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify Quote_Manifest_Enriched.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD COMPOSER - Read arc-specific composer skill", status: "completed" },
    { id: "step-4", description: "STEP 4: SELECT QUOTES - Choose best quotes using V3 tags", status: "completed" },
    { id: "step-5", description: "STEP 5: EXECUTE COMPOSITION - Assemble 60-90s premise", status: "in_progress" },
    { id: "step-6", description: "STEP 6: GENERATE OUTPUT - Create premise_analysis.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm duration and arc rules", status: "pending" }
  ]
});
```

**VAE DECODER PROTOCOL (Run for each scene):**

For each selected quote, execute:

1. **[SEMANTIC_CHECK]** — What is the exact emotional frequency? (10-15 words)
2. **[SHADOW_FILTER]** — How do we show, not tell? (10-15 words)
3. **[ANTI-CLICHÉ_GATE]** — What is the stock version? How subvert? (15-20 words)
4. **[EXECUTE]** — Write the visual_direction for this scene (20-30 words)

**OUTPUT per scene (60-80 words):**
```
SC01: W1_HOOK
- Quote: "[Exact text]"
- SEMANTIC_CHECK: [10-15 words]
- SHADOW_FILTER: [10-15 words]
- ANTI-CLICHÉ_GATE: [15-20 words]
- visual_direction: [20-30 words describing the visual]
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify Quote_Manifest_Enriched.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD COMPOSER - Read arc-specific composer skill", status: "completed" },
    { id: "step-4", description: "STEP 4: SELECT QUOTES - Choose best quotes using V3 tags", status: "completed" },
    { id: "step-5", description: "STEP 5: EXECUTE COMPOSITION - Assemble 60-90s premise", status: "completed" },
    { id: "step-6", description: "STEP 6: GENERATE OUTPUT - Create premise_analysis.json", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm duration and arc rules", status: "pending" }
  ]
});
```

---

## STEP 6: GENERATE OUTPUT

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify Quote_Manifest_Enriched.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD COMPOSER - Read arc-specific composer skill", status: "completed" },
    { id: "step-4", description: "STEP 4: SELECT QUOTES - Choose best quotes using V3 tags", status: "completed" },
    { id: "step-5", description: "STEP 5: EXECUTE COMPOSITION - Assemble 60-90s premise", status: "completed" },
    { id: "step-6", description: "STEP 6: GENERATE OUTPUT - Create premise_analysis.json", status: "in_progress" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm duration and arc rules", status: "pending" }
  ]
});
```

**CREATE FILE:** `{project_id}_premise_analysis.json`

**USE THIS EXACT TEMPLATE:**

```json
{
  "project_id": "{project_id}",
  "arc": "The [Name]",
  "total_duration": 67,
  "scenes": [
    {
      "id": "SC01",
      "cluster": "W1_HOOK",
      "quote": "Exact verbatim text from transcript",
      "start": "00:07:11",
      "end": "00:07:20",
      "duration": 9,
      "visual_direction": "20-30 word description of the visual"
    },
    {
      "id": "SC02",
      "cluster": "W2_PAIN",
      "quote": "...",
      "start": "...",
      "end": "...",
      "duration": 7,
      "visual_direction": "..."
    }
  ]
}
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify Quote_Manifest_Enriched.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD COMPOSER - Read arc-specific composer skill", status: "completed" },
    { id: "step-4", description: "STEP 4: SELECT QUOTES - Choose best quotes using V3 tags", status: "completed" },
    { id: "step-5", description: "STEP 5: EXECUTE COMPOSITION - Assemble 60-90s premise", status: "completed" },
    { id: "step-6", description: "STEP 6: GENERATE OUTPUT - Create premise_analysis.json", status: "completed" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm duration and arc rules", status: "pending" }
  ]
});
```

---

## STEP 7: VALIDATION

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify Quote_Manifest_Enriched.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD COMPOSER - Read arc-specific composer skill", status: "completed" },
    { id: "step-4", description: "STEP 4: SELECT QUOTES - Choose best quotes using V3 tags", status: "completed" },
    { id: "step-5", description: "STEP 5: EXECUTE COMPOSITION - Assemble 60-90s premise", status: "completed" },
    { id: "step-6", description: "STEP 6: GENERATE OUTPUT - Create premise_analysis.json", status: "completed" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm duration and arc rules", status: "in_progress" }
  ]
});
```

**CHECKS:**

| # | Check | Requirement | Result |
|---|-------|-------------|--------|
| 1 | Total duration | 60-90 seconds | ✅/❌ |
| 2 | Scene count | 5-8 scenes | ✅/❌ |
| 3 | All clusters | At least 1 quote from each cluster | ✅/❌ |
| 4 | No quote >15s | Each quote ≤15 seconds | ✅/❌ |
| 5 | JSON valid | No syntax errors | ✅/❌ |

**OUTPUT (25-35 words):**
```
✅ COMPOSITION COMPLETE
- Duration: [X] seconds
- Scenes: [X]
- Arc: The [Name]
- File: {project_id}_premise_analysis.json created
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify Quote_Manifest_Enriched.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD COMPOSER - Read arc-specific composer skill", status: "completed" },
    { id: "step-4", description: "STEP 4: SELECT QUOTES - Choose best quotes using V3 tags", status: "completed" },
    { id: "step-5", description: "STEP 5: EXECUTE COMPOSITION - Assemble 60-90s premise", status: "completed" },
    { id: "step-6", description: "STEP 6: GENERATE OUTPUT - Create premise_analysis.json", status: "completed" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm duration and arc rules", status: "completed" }
  ]
});
```

---

## 🔗 NEXT COMMAND

`/cmf-authorize {project_id}`
