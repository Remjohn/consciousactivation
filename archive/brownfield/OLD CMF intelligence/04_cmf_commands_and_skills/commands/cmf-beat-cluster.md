---
name: cmf-beat-cluster
description: Generate Beat Cluster JSON for concept-driven visual generation
---

# /cmf-beat-cluster {project_id}

// turbo-all

> **SKILLS_BASE:** `skills/cmf/narrative/beat-cluster-extractor/`

**Objective:** Generate `beat_cluster.json` — concept clusters for visual generation.

---

## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify premise_analysis.json and visual_schema.json exist", status: "pending" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read Beat Cluster Extractor SKILL.md completely", status: "pending" },
    { id: "step-3", description: "STEP 3: CLUSTER ANALYSIS - Group quotes into narrative beats", status: "pending" },
    { id: "step-4", description: "STEP 4: EXTRACT CONCEPTS - Derive concept, emotion per cluster", status: "pending" },
    { id: "step-5", description: "STEP 5: SELECT REPRESENTATIVE - Score and select representative quote per cluster", status: "pending" },
    { id: "step-6", description: "STEP 6: DERIVE VCP - Write Visual Cinematic Premise (mini-story) per cluster", status: "pending" },
    { id: "step-7", description: "STEP 7: OUTPUT - Generate beat_cluster.json with VCP", status: "pending" },
    { id: "step-8", description: "STEP 8: VALIDATE - Confirm all clusters have grounded VCP", status: "pending" }
  ]
});
```

---

## STEP 1: PRE-FLIGHT

**EXECUTE:** `write_todos` with STEP 1 as `in_progress`

**ACTIONS:**

| Check | Path | If Missing |
|-------|------|------------|
| 1 | `{project_id}_premise_analysis.json` | STOP → Run `/cmf-compose` |
| 2 | `{project_id}_Quote_Manifest_Enriched.md` | STOP → Run `/cmf-analyze` |
| 3 | `😎 {project_id} - The Brand Avatar 😎.md` | STOP → Run brand avatar script |
| 4 | `{project_id}_strategy_brief.json` | STOP → Run `/cmf-diagnose` |

**OUTPUT:**
```
PRE-FLIGHT COMPLETE:
- premise_analysis.json: ✅ Found
- Quote_Manifest_Enriched.md: ✅ Found ({N} quotes)
- Brand Avatar: ✅ Found
- strategy_brief.json: ✅ Found
```

**EXECUTE:** `write_todos` with STEP 1 as `completed`

---

## STEP 1.5: LOAD ENRICHED QUOTES (MANDATORY)

**EXECUTE:** `write_todos` with STEP 1.5 as `in_progress`

> [!CAUTION]
> **YOU MUST READ THE FULL QUOTE MANIFEST BEFORE PROCEEDING.**
> Do NOT summarize. Do NOT skip. Load EVERY quote.

**READ FILE:** `{project_id}_Quote_Manifest_Enriched.md`

**EXTRACT AND STORE:**

```markdown
=== LOADED QUOTES ===

W1/HOOK:
- Quote W1.1: "[exact text]"
- Quote W1.2: "[exact text]"
...

W2/PAIN:
- Quote W2.1: "[exact text]"
...

[Continue for all clusters]
```

> [!IMPORTANT]
> **VCPs MUST use EXACT PHRASES from these quotes.**
> Generic emotion words like "relief", "pain", "clarity" are FORBIDDEN.
> Use the protagonist's ACTUAL WORDS.

**OUTPUT:**
```
ENRICHED QUOTES LOADED:
- W1/HOOK: {N} quotes
- W2/PAIN: {N} quotes
- W3/SOLUTION: {N} quotes
- W4/PROOF: {N} quotes
- W5/CLOSE: {N} quotes
- TOTAL: {N} verbatim phrases available for VCPs
```

**EXECUTE:** `write_todos` with STEP 1.5 as `completed`

---

## STEP 2: LOAD BEAT CLUSTER EXTRACTOR SKILL

**EXECUTE:** `write_todos` with STEP 2 as `in_progress`

**📚 REQUIRED SKILL LOADING:**

Read this file **COMPLETELY** before proceeding:

```
skills/cmf/narrative/beat-cluster-extractor/SKILL.md
```

**YOU MUST FOLLOW:**
- **Cluster Analysis Algorithm** — Group quotes by narrative beat (W1-W5)
- **Representative Quote Selection** — Weighted scoring matrix (Directness, Economy, Physicality, Emotional Clarity)
- **Visual Intent Derivation** — What to show, what NOT to show, suggested physical noun
- **Output Schema** — Match `intelligence/schemas/beat_cluster_schema.json`

**OUTPUT:**
```
BEAT CLUSTER EXTRACTOR SKILL LOADED:
- Cluster Analysis Algorithm: ✅ Loaded
- Quote Selection Matrix: ✅ Loaded
- Visual Intent Derivation: ✅ Loaded
```

**EXECUTE:** `write_todos` with STEP 2 as `completed`

---

## STEP 3: CLUSTER ANALYSIS

**EXECUTE:** `write_todos` with STEP 3 as `in_progress`

**DETECT BEAT CODES FROM premise_analysis.json:**

> [!IMPORTANT]
> Do NOT assume W1-W5. The beat codes depend on the arc type.
> Read `strategy_brief.selected_arc` to understand the arc, then extract actual scene codes from `premise_analysis.json`.

**DYNAMICALLY BUILD THIS TABLE:**

| Cluster | Narrative Function | Scenes |
|---------|-------------------|--------|
| {BEAT1}_CLUSTER | [First beat function] | [List scene_codes] |
| {BEAT2}_CLUSTER | [Second beat function] | [List scene_codes] |
| {BEAT3}_CLUSTER | [Third beat function] | [List scene_codes] |
| {BEAT4}_CLUSTER | [Fourth beat function] | [List scene_codes] |
| ... | ... | ... |

**EXECUTE:** `write_todos` with STEP 3 as `completed`

---

## STEP 4: EXTRACT CONCEPTS

**EXECUTE:** `write_todos` with STEP 4 as `in_progress`

**FOR EACH CLUSTER, DERIVE:**

```markdown
=== CLUSTER {N}: {CLUSTER_NAME} ===

CONCEPT TITLE: [A poetic 3-7 word title capturing the essence]
CONCEPT DESCRIPTION: [40-60 word description of what this beat represents narratively]
CORE EMOTION: [Single word: The primary emotion beneath the surface]
PHYSICAL MANIFESTATION: [How this emotion shows in the body - from visual_schema.micro_expressions]
```

**EXECUTE:** `write_todos` with STEP 4 as `completed`

---

## STEP 5: SELECT REPRESENTATIVE QUOTE

**EXECUTE:** `write_todos` with STEP 5 as `in_progress`

**FOR EACH CLUSTER, SCORE ALL QUOTES:**

| Quote | Directness (0-10) | Economy (0-10) | Physicality (0-10) | Emotional Clarity (0-10) | TOTAL |
|-------|-------------------|----------------|--------------------| --------------------------|-------|
| "{quote 1}" | X | X | X | X | /40 |
| "{quote 2}" | X | X | X | X | /40 |

**SELECT:** The quote with highest total score.

**WHY REPRESENTATIVE:** [1-2 sentences explaining why this quote best captures the beat's essence]

**EXECUTE:** `write_todos` with STEP 5 as `completed`

---

## STEP 6: DERIVE VISUAL CINEMATIC PREMISE (VCP)

**EXECUTE:** `write_todos` with STEP 6 as `in_progress`

> [!IMPORTANT]
> **VCP PRINCIPLE:**
> A Visual Cinematic Premise is a MINI-STORY, not a shot prescription.
> It contains BEFORE → TURNING POINT → AFTER structure.
> It is SPECIFIC to this person's actual words, not generic emotion labels.

### 6.1 VCP Writing Rules

> [!CAUTION]
> **VCPs are PURE MINI-STORIES. NO VISUAL DIRECTION.**
> The composer will interpret the story through their own lens.

| Rule | Description |
|------|-------------|
| **GROUNDED** | Use EXACT PHRASES from the enriched quotes (not generic labels) |
| **STORY ARC** | Include BEFORE (what was), TURNING POINT (what changed), AFTER (implication) |
| **SPECIFIC** | Must be unique to THIS person — embed their actual words |
| **NO PRESCRIPTION** | Do NOT specify shot_type, body_part, camera angle |
| **NO "SHOW..."** | Do NOT end with visual direction — let composers interpret |
| **60-80 WORDS** | Dense narrative, not a brief caption |

### 6.2 VCP Template

**FOR EACH CLUSTER:**

```markdown
=== VISUAL CINEMATIC PREMISE: {CLUSTER_NAME} ===

QUOTE: "{exact representative quote from transcript}"
TIMESTAMP: {HH:MM:SS}

ARC CONTEXT:
  - BEFORE: [The state before — use transcript phrases]
  - TURNING POINT: [What this quote reveals — use transcript phrases]
  - AFTER: [The implication — use transcript phrases]

VISUAL CINEMATIC PREMISE (60-80 words):
"[Write a narrative mini-story that:
- References the BEFORE state using protagonist's actual words
- Captures the TURNING POINT with specific details from transcript
- Implies the AFTER change with real phrases
- DO NOT end with 'Show...' — composers will interpret]"
```

### 6.3 VCP Examples (GOOD vs BAD)

| ❌ BAD (Generic/Prescriptive/"Show...") | ✅ GOOD (Story-Specific, Pure Narrative) |
|----------------------------------------|------------------------------------------|
| "Show relief through body language" | "For years, she felt 'larguée' — dropped by systems that should have held her. Then she encountered 'cette approche corps-à-corps où elle lâche pas.' An unrelenting grip that matched the intensity of her struggle. The collision she needed." |
| "Hand gripping sink, extreme macro. Show the violence of standing still." | "Her body screamed with 'beaucoup de vertiges, beaucoup de crises.' The doctors ran tests. The results returned blank: 'physiquement il ne constatait rien.' She stood perfectly still while her world tilted. No one believed the floor was moving." |
| "Show completion in golden hour." | "She could have stopped at 'le travail à moitié' — the half-done work. But she went 'pas à pas' into the personal sphere until nothing was left undone. Not for herself alone, but for the future she carries: 'je le vois en pleine face chez mon fils.'" |

### 6.4 VCP Quality Gate

Before proceeding, verify each VCP:

| Check | Requirement |
|-------|-------------|
| **Uses transcript phrases?** | Contains EXACT WORDS from enriched quotes (in quotes or French) |
| **Has BEFORE?** | Mentions the prior state using protagonist's words |
| **Has TURNING POINT?** | Captures what this specific quote reveals |
| **Has AFTER?** | Implies the change or consequence |
| **NO "Show..."?** | Does NOT end with visual direction |
| **60-80 words?** | Dense narrative, not a brief caption |
| **NO shot_type?** | Does NOT prescribe Macro/Wide/etc. |
| **NO body_part?** | Does NOT prescribe fingers/hands/feet/etc. |

**EXECUTE:** `write_todos` with STEP 6 as `completed`

---

## STEP 7: OUTPUT beat_cluster.json

**EXECUTE:** `write_todos` with STEP 7 as `in_progress`

**CREATE FILE:** `{project_id}_beat_cluster.json`

```json
{
  "project_id": "{project_id}",
  "arc": "The [Arc Name]",
  "generated_at": "[ISO timestamp]",
  "vcp_version": "2.0",
  "clusters": [
    {
      "cluster_id": "SC01",
      "beat_position": "HOOK",
      "concept": {
        "title": "[3-7 word poetic title]",
        "description": "[40-60 word description]",
        "core_emotion": "[Single word]"
      },
      "quotes": {
        "representative": {
          "text": "[Verbatim quote]",
          "timestamp": "[HH:MM:SS]",
          "why_representative": "[1-2 sentences]"
        },
        "supporting": [
          {
            "text": "[Other quote in cluster]",
            "timestamp": "[HH:MM:SS]",
            "function": "CONTEXT — [Why included]"
          }
        ]
      },
      "arc_context": {
        "before": "[The state before this moment]",
        "turning_point": "[What this quote reveals or changes]",
        "after": "[The implication or consequence]"
      },
      "visual_cinematic_premise": "[60-80 word PURE NARRATIVE using EXACT PHRASES from transcript. NO 'Show...', NO visual direction.]",
      "arc_position": {
        "beat": "HOOK",
        "narrative_function": "[What this beat does for the story]"
      }
    }
  ]
}
```

**EXECUTE:** `write_todos` with STEP 7 as `completed`

---

## STEP 8: VALIDATION

**EXECUTE:** `write_todos` with STEP 8 as `in_progress`

**CHECKS:**

| # | Check | Requirement | Result |
|---|-------|-------------|--------|
| 1 | All clusters have concept.title | Non-empty string | ✅/❌ |
| 2 | VCP word count | Each VCP is 60-80 words | ✅/❌ |
| 3 | VCPs use transcript phrases | Contains EXACT WORDS from enriched quotes | ✅/❌ |
| 4 | All VCPs have BEFORE | Mentions prior state with protagonist's words | ✅/❌ |
| 5 | All VCPs have TURNING POINT | Captures what quote reveals | ✅/❌ |
| 6 | All VCPs have AFTER | Implies consequence | ✅/❌ |
| 7 | NO "Show..." ending | VCPs are pure narrative, no visual direction | ✅/❌ |
| 8 | NO prescription in VCP | No shot_type, body_part, camera angle | ✅/❌ |
| 9 | JSON valid | No syntax errors | ✅/❌ |

**VCP QUALITY CHECK:**
> ❓ Is each VCP SPECIFIC to this person (not generic emotion labels)?
> ❓ Could this VCP ONLY describe this moment for THIS person?
> ❓ Does the VCP tell a MINI-STORY (not just describe an image)?

**OUTPUT:**
```
✅ BEAT CLUSTER EXTRACTION COMPLETE (VCP Enhanced)
- Clusters: 5 (SC01-SC05)
- File created: {project_id}_beat_cluster.json
- All clusters have visual_cinematic_premise
- All VCPs follow BEFORE/TURNING/AFTER structure
- Ready for storyboard-composer, cac-composer, gmg-composer
```

**EXECUTE:** `write_todos` with STEP 8 as `completed`

---

## 🔗 NEXT COMMANDS

Ready for Phase 1B:
- `/cmf-storyboard {project_id}`
- `/cmf-motion {project_id}`
