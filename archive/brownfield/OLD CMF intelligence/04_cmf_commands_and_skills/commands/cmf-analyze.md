---
name: cmf-analyze
description: V3 Enrichment using arc-specific Analyst skill
---

# /cmf-analyze {project_id}

// turbo-all

> **SKILLS_BASE:** `skills/cmf/`

**Objective:** Enrich quotes with V3 narrative coherence tags (400-600 words output).

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify Quote_Manifest.md exists", status: "pending" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "pending" },
    { id: "step-3", description: "STEP 3: LOAD ANALYST - Read arc-specific analyst skill", status: "pending" },
    { id: "step-4", description: "STEP 4: EXECUTE ANALYSIS - Apply V3 tags to each quote", status: "pending" },
    { id: "step-5", description: "STEP 5: GENERATE OUTPUT - Create Quote_Manifest_Enriched.md", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm all quotes tagged", status: "pending" }
  ]
});
```

---

## STEP 1: PRE-FLIGHT

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify Quote_Manifest.md exists", status: "in_progress" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "pending" },
    { id: "step-3", description: "STEP 3: LOAD ANALYST - Read arc-specific analyst skill", status: "pending" },
    { id: "step-4", description: "STEP 4: EXECUTE ANALYSIS - Apply V3 tags to each quote", status: "pending" },
    { id: "step-5", description: "STEP 5: GENERATE OUTPUT - Create Quote_Manifest_Enriched.md", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm all quotes tagged", status: "pending" }
  ]
});
```

**ACTIONS:**

| Check | Path | If Missing |
|-------|------|------------|
| 1 | `{project_id}_Quote_Manifest.md` | STOP → Run `/cmf-hunt` first |
| 2 | `{project_id}_strategy_brief.json` | STOP → Run `/cmf-diagnose` first |

**OUTPUT (20-30 words):**
```
PRE-FLIGHT COMPLETE:
- Quote Manifest: ✅ Found ([X] quotes)
- Strategy Brief: ✅ Found (Arc: The [Name])
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify Quote_Manifest.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "pending" },
    { id: "step-3", description: "STEP 3: LOAD ANALYST - Read arc-specific analyst skill", status: "pending" },
    { id: "step-4", description: "STEP 4: EXECUTE ANALYSIS - Apply V3 tags to each quote", status: "pending" },
    { id: "step-5", description: "STEP 5: GENERATE OUTPUT - Create Quote_Manifest_Enriched.md", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm all quotes tagged", status: "pending" }
  ]
});
```

---

## STEP 2: IDENTIFY ARC

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify Quote_Manifest.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "in_progress" },
    { id: "step-3", description: "STEP 3: LOAD ANALYST - Read arc-specific analyst skill", status: "pending" },
    { id: "step-4", description: "STEP 4: EXECUTE ANALYSIS - Apply V3 tags to each quote", status: "pending" },
    { id: "step-5", description: "STEP 5: GENERATE OUTPUT - Create Quote_Manifest_Enriched.md", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm all quotes tagged", status: "pending" }
  ]
});
```

**ACTIONS:**
1. Read `{project_id}_strategy_brief.json`
2. Extract `selected_arc`

**OUTPUT (15-25 words):**
```
ARC: The [Name]
Next: Loading [arc]-analyst skill
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify Quote_Manifest.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD ANALYST - Read arc-specific analyst skill", status: "pending" },
    { id: "step-4", description: "STEP 4: EXECUTE ANALYSIS - Apply V3 tags to each quote", status: "pending" },
    { id: "step-5", description: "STEP 5: GENERATE OUTPUT - Create Quote_Manifest_Enriched.md", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm all quotes tagged", status: "pending" }
  ]
});
```

---

## STEP 3: LOAD ANALYST SKILL

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify Quote_Manifest.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD ANALYST - Read arc-specific analyst skill", status: "in_progress" },
    { id: "step-4", description: "STEP 4: EXECUTE ANALYSIS - Apply V3 tags to each quote", status: "pending" },
    { id: "step-5", description: "STEP 5: GENERATE OUTPUT - Create Quote_Manifest_Enriched.md", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm all quotes tagged", status: "pending" }
  ]
});
```

**ROUTING TABLE:**

| Arc | Skill Path |
|-----|------------|
| The Witness | `skills/cmf/analysts/witness-analyst/SKILL.md` |
| The Breakthrough | `skills/cmf/analysts/breakthrough-analyst/SKILL.md` |
| The Shared Struggle | `skills/cmf/analysts/shared-struggle-analyst/SKILL.md` |
| [etc...] | |

**ACTIONS:**
1. Read the FULL analyst skill file (do NOT skip sections)
2. Extract the V3 tagging rules

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify Quote_Manifest.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD ANALYST - Read arc-specific analyst skill", status: "completed" },
    { id: "step-4", description: "STEP 4: EXECUTE ANALYSIS - Apply V3 tags to each quote", status: "pending" },
    { id: "step-5", description: "STEP 5: GENERATE OUTPUT - Create Quote_Manifest_Enriched.md", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm all quotes tagged", status: "pending" }
  ]
});
```

---

## STEP 4: EXECUTE ANALYSIS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify Quote_Manifest.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD ANALYST - Read arc-specific analyst skill", status: "completed" },
    { id: "step-4", description: "STEP 4: EXECUTE ANALYSIS - Apply V3 tags to each quote", status: "in_progress" },
    { id: "step-5", description: "STEP 5: GENERATE OUTPUT - Create Quote_Manifest_Enriched.md", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm all quotes tagged", status: "pending" }
  ]
});
```

**FOR EACH QUOTE, ADD V3 TAGS (15-25 words per quote):**

```markdown
- **THEMATIC_FIT:** [0.0-1.0] — [5-10 word justification]
- **GLUE_SCORE:** [0.0-1.0] — [5-10 word justification]
- **HIGH_AFFINITY_SEQUENCES:** [List of cluster IDs this quote flows well into]
- **SUBTEXT:** [10-15 words describing deeper meaning]
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify Quote_Manifest.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD ANALYST - Read arc-specific analyst skill", status: "completed" },
    { id: "step-4", description: "STEP 4: EXECUTE ANALYSIS - Apply V3 tags to each quote", status: "completed" },
    { id: "step-5", description: "STEP 5: GENERATE OUTPUT - Create Quote_Manifest_Enriched.md", status: "pending" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm all quotes tagged", status: "pending" }
  ]
});
```

---

## STEP 5: GENERATE OUTPUT

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify Quote_Manifest.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD ANALYST - Read arc-specific analyst skill", status: "completed" },
    { id: "step-4", description: "STEP 4: EXECUTE ANALYSIS - Apply V3 tags to each quote", status: "completed" },
    { id: "step-5", description: "STEP 5: GENERATE OUTPUT - Create Quote_Manifest_Enriched.md", status: "in_progress" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm all quotes tagged", status: "pending" }
  ]
});
```

**CREATE FILE:** `{project_id}_Quote_Manifest_Enriched.md` (3000-4000 words)

**Same structure as Quote_Manifest.md, but each quote now includes V3 tags.**

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify Quote_Manifest.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD ANALYST - Read arc-specific analyst skill", status: "completed" },
    { id: "step-4", description: "STEP 4: EXECUTE ANALYSIS - Apply V3 tags to each quote", status: "completed" },
    { id: "step-5", description: "STEP 5: GENERATE OUTPUT - Create Quote_Manifest_Enriched.md", status: "completed" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm all quotes tagged", status: "pending" }
  ]
});
```

---

## STEP 6: VALIDATION

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify Quote_Manifest.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD ANALYST - Read arc-specific analyst skill", status: "completed" },
    { id: "step-4", description: "STEP 4: EXECUTE ANALYSIS - Apply V3 tags to each quote", status: "completed" },
    { id: "step-5", description: "STEP 5: GENERATE OUTPUT - Create Quote_Manifest_Enriched.md", status: "completed" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm all quotes tagged", status: "in_progress" }
  ]
});
```

**CHECKS:**

| # | Check | Requirement | Result |
|---|-------|-------------|--------|
| 1 | All quotes have THEMATIC_FIT | Required | ✅/❌ |
| 2 | All quotes have GLUE_SCORE | Required | ✅/❌ |
| 3 | All quotes have HIGH_AFFINITY_SEQUENCES | Required | ✅/❌ |
| 4 | All quotes have SUBTEXT | Required | ✅/❌ |

**OUTPUT (20-30 words):**
```
✅ ANALYSIS COMPLETE
- Quotes enriched: [X]
- File: {project_id}_Quote_Manifest_Enriched.md created
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify Quote_Manifest.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - Read strategy_brief.json", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD ANALYST - Read arc-specific analyst skill", status: "completed" },
    { id: "step-4", description: "STEP 4: EXECUTE ANALYSIS - Apply V3 tags to each quote", status: "completed" },
    { id: "step-5", description: "STEP 5: GENERATE OUTPUT - Create Quote_Manifest_Enriched.md", status: "completed" },
    { id: "step-6", description: "STEP 6: VALIDATE - Confirm all quotes tagged", status: "completed" }
  ]
});
```

---

## 🔗 NEXT COMMAND

`/cmf-compose {project_id}`
