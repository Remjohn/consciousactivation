---
name: cmf-script
description: Final script assembly and authorization
---

# /cmf-script {project_id}

// turbo-all

> **SKILLS_BASE:** `skills/cmf/`

**Objective:** Assemble final production-ready script (500-800 words output).

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify AUTHORIZED.md exists", status: "pending" },
    { id: "step-2", description: "STEP 2: LOAD FILES - Read premise_analysis.json and Brand Avatar", status: "pending" },
    { id: "step-3", description: "STEP 3: ADD SCENE IDS - Number all scenes (SC01, SC02...)", status: "pending" },
    { id: "step-4", description: "STEP 4: ADD VISUAL DIRECTION - Expand each scene", status: "pending" },
    { id: "step-5", description: "STEP 5: GENERATE OUTPUT - Create final_script.json", status: "pending" },
    { id: "step-6", description: "STEP 6: CREATE MARKER - Create SCRIPT_AUTHORIZED.md", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm JSON valid, all scenes numbered", status: "pending" }
  ]
});
```

---

## STEP 1: PRE-FLIGHT

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify AUTHORIZED.md exists", status: "in_progress" },
    { id: "step-2", description: "STEP 2: LOAD FILES - Read premise_analysis.json and Brand Avatar", status: "pending" },
    { id: "step-3", description: "STEP 3: ADD SCENE IDS - Number all scenes (SC01, SC02...)", status: "pending" },
    { id: "step-4", description: "STEP 4: ADD VISUAL DIRECTION - Expand each scene", status: "pending" },
    { id: "step-5", description: "STEP 5: GENERATE OUTPUT - Create final_script.json", status: "pending" },
    { id: "step-6", description: "STEP 6: CREATE MARKER - Create SCRIPT_AUTHORIZED.md", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm JSON valid, all scenes numbered", status: "pending" }
  ]
});
```

**ACTIONS:**

| Check | Path | If Missing |
|-------|------|------------|
| 1 | `{project_id}_[ARC]_AUTHORIZED.md` (score ≥75) | STOP → Run `/cmf-authorize` |
| 2 | `{project_id}_premise_analysis.json` | STOP → Run `/cmf-compose` |
| 3 | `😎 {project_id} - The Brand Avatar 😎.md` | STOP → Run brand avatar script |

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify AUTHORIZED.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD FILES - Read premise_analysis.json and Brand Avatar", status: "pending" },
    { id: "step-3", description: "STEP 3: ADD SCENE IDS - Number all scenes (SC01, SC02...)", status: "pending" },
    { id: "step-4", description: "STEP 4: ADD VISUAL DIRECTION - Expand each scene", status: "pending" },
    { id: "step-5", description: "STEP 5: GENERATE OUTPUT - Create final_script.json", status: "pending" },
    { id: "step-6", description: "STEP 6: CREATE MARKER - Create SCRIPT_AUTHORIZED.md", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm JSON valid, all scenes numbered", status: "pending" }
  ]
});
```

---

## STEP 2: LOAD FILES

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify AUTHORIZED.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD FILES - Read premise_analysis.json and Brand Avatar", status: "in_progress" },
    { id: "step-3", description: "STEP 3: ADD SCENE IDS - Number all scenes (SC01, SC02...)", status: "pending" },
    { id: "step-4", description: "STEP 4: ADD VISUAL DIRECTION - Expand each scene", status: "pending" },
    { id: "step-5", description: "STEP 5: GENERATE OUTPUT - Create final_script.json", status: "pending" },
    { id: "step-6", description: "STEP 6: CREATE MARKER - Create SCRIPT_AUTHORIZED.md", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm JSON valid, all scenes numbered", status: "pending" }
  ]
});
```

**ACTIONS:**

1. Read `{project_id}_premise_analysis.json`
2. Read `😎 {project_id} - The Brand Avatar 😎.md`
3. Extract the Character Anchor for visual consistency

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify AUTHORIZED.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD FILES - Read premise_analysis.json and Brand Avatar", status: "completed" },
    { id: "step-3", description: "STEP 3: ADD SCENE IDS - Number all scenes (SC01, SC02...)", status: "pending" },
    { id: "step-4", description: "STEP 4: ADD VISUAL DIRECTION - Expand each scene", status: "pending" },
    { id: "step-5", description: "STEP 5: GENERATE OUTPUT - Create final_script.json", status: "pending" },
    { id: "step-6", description: "STEP 6: CREATE MARKER - Create SCRIPT_AUTHORIZED.md", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm JSON valid, all scenes numbered", status: "pending" }
  ]
});
```

---

## STEP 3: ADD SCENE IDS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify AUTHORIZED.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD FILES - Read premise_analysis.json and Brand Avatar", status: "completed" },
    { id: "step-3", description: "STEP 3: ADD SCENE IDS - Number all scenes (SC01, SC02...)", status: "in_progress" },
    { id: "step-4", description: "STEP 4: ADD VISUAL DIRECTION - Expand each scene", status: "pending" },
    { id: "step-5", description: "STEP 5: GENERATE OUTPUT - Create final_script.json", status: "pending" },
    { id: "step-6", description: "STEP 6: CREATE MARKER - Create SCRIPT_AUTHORIZED.md", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm JSON valid, all scenes numbered", status: "pending" }
  ]
});
```

**ACTIONS:**

Number each scene sequentially:
- SC01, SC02, SC03, SC04, SC05, etc.

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify AUTHORIZED.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD FILES - Read premise_analysis.json and Brand Avatar", status: "completed" },
    { id: "step-3", description: "STEP 3: ADD SCENE IDS - Number all scenes (SC01, SC02...)", status: "completed" },
    { id: "step-4", description: "STEP 4: ADD VISUAL DIRECTION - Expand each scene", status: "pending" },
    { id: "step-5", description: "STEP 5: GENERATE OUTPUT - Create final_script.json", status: "pending" },
    { id: "step-6", description: "STEP 6: CREATE MARKER - Create SCRIPT_AUTHORIZED.md", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm JSON valid, all scenes numbered", status: "pending" }
  ]
});
```

---

## STEP 4: ADD VISUAL DIRECTION

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify AUTHORIZED.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD FILES - Read premise_analysis.json and Brand Avatar", status: "completed" },
    { id: "step-3", description: "STEP 3: ADD SCENE IDS - Number all scenes (SC01, SC02...)", status: "completed" },
    { id: "step-4", description: "STEP 4: ADD VISUAL DIRECTION - Expand each scene", status: "in_progress" },
    { id: "step-5", description: "STEP 5: GENERATE OUTPUT - Create final_script.json", status: "pending" },
    { id: "step-6", description: "STEP 6: CREATE MARKER - Create SCRIPT_AUTHORIZED.md", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm JSON valid, all scenes numbered", status: "pending" }
  ]
});
```

**FOR EACH SCENE (20-30 words per visual_direction):**

```
visual_direction: "[Describe the visual in 20-30 words. Include emotional tone, composition, and any key visual elements from Brand Avatar.]"
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify AUTHORIZED.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD FILES - Read premise_analysis.json and Brand Avatar", status: "completed" },
    { id: "step-3", description: "STEP 3: ADD SCENE IDS - Number all scenes (SC01, SC02...)", status: "completed" },
    { id: "step-4", description: "STEP 4: ADD VISUAL DIRECTION - Expand each scene", status: "completed" },
    { id: "step-5", description: "STEP 5: GENERATE OUTPUT - Create final_script.json", status: "pending" },
    { id: "step-6", description: "STEP 6: CREATE MARKER - Create SCRIPT_AUTHORIZED.md", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm JSON valid, all scenes numbered", status: "pending" }
  ]
});
```

---

## STEP 5: GENERATE OUTPUT

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify AUTHORIZED.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD FILES - Read premise_analysis.json and Brand Avatar", status: "completed" },
    { id: "step-3", description: "STEP 3: ADD SCENE IDS - Number all scenes (SC01, SC02...)", status: "completed" },
    { id: "step-4", description: "STEP 4: ADD VISUAL DIRECTION - Expand each scene", status: "completed" },
    { id: "step-5", description: "STEP 5: GENERATE OUTPUT - Create final_script.json", status: "in_progress" },
    { id: "step-6", description: "STEP 6: CREATE MARKER - Create SCRIPT_AUTHORIZED.md", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm JSON valid, all scenes numbered", status: "pending" }
  ]
});
```

**CREATE FILE:** `{project_id}_final_script.json`

```json
{
  "project_id": "{project_id}",
  "arc": "The [Name]",
  "total_duration": 67,
  "character_anchor": "[From Brand Avatar]",
  "scenes": [
    {
      "id": "SC01",
      "cluster": "W1_HOOK",
      "quote": "Exact verbatim text",
      "start": "00:07:11",
      "end": "00:07:20",
      "duration": 9,
      "visual_direction": "20-30 word description"
    }
  ]
}
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify AUTHORIZED.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD FILES - Read premise_analysis.json and Brand Avatar", status: "completed" },
    { id: "step-3", description: "STEP 3: ADD SCENE IDS - Number all scenes (SC01, SC02...)", status: "completed" },
    { id: "step-4", description: "STEP 4: ADD VISUAL DIRECTION - Expand each scene", status: "completed" },
    { id: "step-5", description: "STEP 5: GENERATE OUTPUT - Create final_script.json", status: "completed" },
    { id: "step-6", description: "STEP 6: CREATE MARKER - Create SCRIPT_AUTHORIZED.md", status: "pending" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm JSON valid, all scenes numbered", status: "pending" }
  ]
});
```

---

## STEP 6: CREATE MARKER

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify AUTHORIZED.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD FILES - Read premise_analysis.json and Brand Avatar", status: "completed" },
    { id: "step-3", description: "STEP 3: ADD SCENE IDS - Number all scenes (SC01, SC02...)", status: "completed" },
    { id: "step-4", description: "STEP 4: ADD VISUAL DIRECTION - Expand each scene", status: "completed" },
    { id: "step-5", description: "STEP 5: GENERATE OUTPUT - Create final_script.json", status: "completed" },
    { id: "step-6", description: "STEP 6: CREATE MARKER - Create SCRIPT_AUTHORIZED.md", status: "in_progress" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm JSON valid, all scenes numbered", status: "pending" }
  ]
});
```

**CREATE FILE:** `{project_id}_SCRIPT_AUTHORIZED.md`

```markdown
# ✅ SCRIPT AUTHORIZED: {project_id}

**Arc:** The [Name]
**Duration:** [X] seconds
**Scenes:** [X]
**Date:** [Date]

## PHASE 1A COMPLETE ✅

Ready for Phase 1B:
- `/cmf-storyboard {project_id}`
- `/cmf-sonic {project_id}`
- `/cmf-motion {project_id}`
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify AUTHORIZED.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD FILES - Read premise_analysis.json and Brand Avatar", status: "completed" },
    { id: "step-3", description: "STEP 3: ADD SCENE IDS - Number all scenes (SC01, SC02...)", status: "completed" },
    { id: "step-4", description: "STEP 4: ADD VISUAL DIRECTION - Expand each scene", status: "completed" },
    { id: "step-5", description: "STEP 5: GENERATE OUTPUT - Create final_script.json", status: "completed" },
    { id: "step-6", description: "STEP 6: CREATE MARKER - Create SCRIPT_AUTHORIZED.md", status: "completed" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm JSON valid, all scenes numbered", status: "pending" }
  ]
});
```

---

## STEP 7: VALIDATION

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify AUTHORIZED.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD FILES - Read premise_analysis.json and Brand Avatar", status: "completed" },
    { id: "step-3", description: "STEP 3: ADD SCENE IDS - Number all scenes (SC01, SC02...)", status: "completed" },
    { id: "step-4", description: "STEP 4: ADD VISUAL DIRECTION - Expand each scene", status: "completed" },
    { id: "step-5", description: "STEP 5: GENERATE OUTPUT - Create final_script.json", status: "completed" },
    { id: "step-6", description: "STEP 6: CREATE MARKER - Create SCRIPT_AUTHORIZED.md", status: "completed" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm JSON valid, all scenes numbered", status: "in_progress" }
  ]
});
```

**CHECKS:**

| # | Check | Requirement | Result |
|---|-------|-------------|--------|
| 1 | All scenes have IDs | SC01, SC02, SC03... | ✅/❌ |
| 2 | All visual_direction present | 20-30 words each | ✅/❌ |
| 3 | JSON valid | No syntax errors | ✅/❌ |
| 4 | SCRIPT_AUTHORIZED.md created | File exists | ✅/❌ |

**OUTPUT (25-35 words):**
```
✅ SCRIPT ASSEMBLY COMPLETE
- Scenes: [X]
- Duration: [X] seconds
- Files created: final_script.json, SCRIPT_AUTHORIZED.md
- PHASE 1A COMPLETE ✅
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify AUTHORIZED.md exists", status: "completed" },
    { id: "step-2", description: "STEP 2: LOAD FILES - Read premise_analysis.json and Brand Avatar", status: "completed" },
    { id: "step-3", description: "STEP 3: ADD SCENE IDS - Number all scenes (SC01, SC02...)", status: "completed" },
    { id: "step-4", description: "STEP 4: ADD VISUAL DIRECTION - Expand each scene", status: "completed" },
    { id: "step-5", description: "STEP 5: GENERATE OUTPUT - Create final_script.json", status: "completed" },
    { id: "step-6", description: "STEP 6: CREATE MARKER - Create SCRIPT_AUTHORIZED.md", status: "completed" },
    { id: "step-7", description: "STEP 7: VALIDATE - Confirm JSON valid, all scenes numbered", status: "completed" }
  ]
});
```

---

## 🔗 PHASE 1A COMPLETE

Proceed to Phase 1B:
- `/cmf-storyboard {project_id}`
- `/cmf-sonic {project_id}`
- `/cmf-motion {project_id}`
