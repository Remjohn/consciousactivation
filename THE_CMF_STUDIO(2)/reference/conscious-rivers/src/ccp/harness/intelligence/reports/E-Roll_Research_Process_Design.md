# E-Roll Deep Research: Process Failure Analysis & Agentic Solution

**Date:** January 30, 2026
**Purpose:** Diagnose why Deep Research is never delivered and design an enforceable agentic process

---

## 1. The Diagnosis: Why Deep Research is Skipped

### 1.1 No Architectural Enforcement

The current `🔮 E-Roll Research Planning Generator.md` says "MANDATORY" but provides **no enforcement mechanism**.

| What the Guide Says | What Actually Happens |
|---|---|
| "Phase 3: Deep Research (Browser) ★ MANDATORY ★" | Agent skips directly to query generation |
| "DO NOT GENERATE SEARCH QUERIES WITHOUT A DEEP RESEARCH REPORT" | Agent generates queries without report |
| "2-3 NAMED references per angle with source URLs" | Agent invents generic descriptions |

**The Problem:** "Mandatory" is a suggestion without architectural enforcement.

### 1.2 Agent Optimization for Speed

Agents naturally optimize for:
1. **Speed** — Browser research is slow, query generation is fast
2. **Completion** — Producing output feels like progress
3. **Path of Least Resistance** — If skipping is possible, it will be skipped

**The Fix:** Make skipping **architecturally impossible**.

### 1.3 No Validation Checkpoint

The E-Roll Commander only checks:
- [ ] Does the file header contain the correct project ID?
- [ ] Does it cross-reference the final_script.json scenes?

It does NOT check:
- [ ] Does a Deep Research Report exist?
- [ ] Does it contain NAMED references with URLs?
- [ ] Is it 2400-3000 words?

**The Fix:** Add structural validation before query generation is allowed.

---

## 2. The Solution: Agentic Research Process (Enforced)

### 2.1 Critical Design Principle: Coach-Agnostic

This process must work for **48+ coaches**, each with their own `tribe_soul.json`.

```
production/
├── Coach Adele/
│   └── tribe_soul.json
├── Coach Bernard/
│   └── tribe_soul.json
├── Coach Celine/
│   └── tribe_soul.json
...
```

**All inputs are dynamic:**
- `{COACH_PATH}` = `production/{Coach Name}/`
- `{TRIBE_SOUL}` = `{COACH_PATH}/tribe_soul.json`
- `{PROJECT_PATH}` = `{COACH_PATH}/{project_id}/`

### 2.2 Architecture: 5-Phase Sequential Gating with Introspection

```
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 1: CONTEXT LOADING                                        │
│ ─────────────────────────                                       │
│ INPUT: {TRIBE_SOUL}, final_script.json, Brand Avatar            │
│ PROCESS: Load and parse tribe_soul.json for this coach          │
│ OUTPUT: Extracted cultural data (slang, heroes, enemies, jokes) │
│ GATE: Cannot proceed if tribe_soul.json missing or malformed    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 2: 12 INTROSPECTION QUESTIONS ★ CRITICAL ★                │
│ ─────────────────────────────────────                           │
│ INPUT: tribe_soul.json data                                     │
│ PROCESS: Answer 12 questions about THE CULTURE (not the script) │
│ OUTPUT: [project]_cultural_introspection.md                     │
│ GATE: All 12 questions must have specific, named answers        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 3: BROWSER RESEARCH (5 SPECIALIST MODES)                  │
│ ─────────────────────────────────────                           │
│ INPUT: Cultural introspection answers                           │
│ PROCESS: For each mode, use browser to find NAMED sources:      │
│          Mode 1: Influencer Scout (6+ recognizable faces)       │
│          Mode 2: Ethnographer (6+ cultural objects/rituals)     │
│          Mode 3: Journalist (4+ media articles/documentation)   │
│          Mode 4: Archivist (4+ historical/nostalgic images)     │
│          Mode 5: Symbol Hunter (4+ textiles/patterns/icons)     │
│ OUTPUT: [project]_ERoll_Deep_Research_Report.md                 │
│ VALIDATION: 2400-3000 words, 24+ named sources with URLs        │
│ GATE: Cannot proceed until validation passes                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 4: RESEARCH COMMANDER VALIDATION                          │
│ ─────────────────────────────────────                           │
│ INPUT: Deep Research Report                                     │
│ PROCESS: Verify each reference is:                              │
│          - NAMED (not generic)                                  │
│          - SOURCED (URL provided)                               │
│          - TRACEABLE to tribe_soul.json                         │
│ OUTPUT: AUTHORIZED or REJECTED                                  │
│ GATE: If REJECTED, return to Phase 3                            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ PHASE 5: QUERY GENERATION (LOCKED UNTIL PHASE 4 PASSES)         │
│ ─────────────────────────────────────                           │
│ INPUT: AUTHORIZED Deep Research Report                          │
│ PROCESS: For each NAMED reference, create search query          │
│ OUTPUT: [project]_ERoll_Search_Queries.json                     │
│ RULE: Every query MUST cite a specific reference from report    │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 Phase 2: The 12 Introspection Questions (Detailed)

These questions are answered **from the tribe_soul.json**, not invented.

#### Language & Codes (Questions 1-2)
1. **What insider slang identifies "us"?**
   → Extract from `tribe_soul.cultural_artifacts.tribe_slang`
   
2. **What visual signals or gestures do only insiders recognize?**
   → Infer from slang + inside_jokes

#### Aesthetics & Symbols (Questions 3-4)
3. **What colors, textures, or styles define this tribe's visual identity?**
   → Extract from tribe descriptions (e.g., "Batik," "Bogolan," "Kente")
   
4. **What sacred symbols, adornments, or objects carry deep meaning?**
   → Extract from cultural_artifacts + shared_heroes descriptions

#### Rituals & Behaviors (Questions 5-6)
5. **What daily or ceremonial practices define this community?**
   → Extract from tribe_slang (e.g., "Kinkeliba," "bain de feuilles")
   
6. **What preparation or cleansing rituals are sacred?**
   → Extract from tribe_slang + common_enemies (what they protect against)

#### Heroes, Elders & Icons (Questions 7-8)
7. **Who are the living figures this audience reveres? (NAMED)**
   → Extract from `tribe_soul.cultural_artifacts.shared_heroes`
   
8. **What archetypes resonate? (Healer, warrior, mother, elder)**
   → Extract from shared_heroes descriptions

#### Opposition, Wounds & Enemy (Questions 9-10)
9. **What systems or forces threatened this culture?**
   → Extract from `tribe_soul.cultural_artifacts.common_enemies`
   
10. **What shared wounds or traumas bind this community?**
    → Extract from common_enemies + core_anxieties

#### Shared Emotional Truths (Questions 11-12)
11. **What collective emotions (pride, grief, longing) define this tribe?**
    → Extract from `tribe_soul.emotional_resonance`
    
12. **What future vision or aspiration unites this community?**
    → Extract from `primary_aspirations`

**OUTPUT FORMAT:**
```markdown
# Cultural Introspection: {project_id}

## Tribe: {tribe_name} (from {coach_name})

### Q1: Insider Slang
- "S'enjailler" - [extracted from tribe_soul.tribe_slang[0]]
- "Kinkeliba" - [extracted from tribe_soul.tribe_slang[3]]
...

### Q7: Named Heroes
- [Name from shared_heroes[0].hero]
- [Name from shared_heroes[1].hero]
...

[Continue for all 12 questions]
```

### 2.4 The Deep Research Report Template (Coach-Agnostic)

The template uses dynamic variables that are populated from each coach's `tribe_soul.json`:

```markdown
# E-Roll Deep Research Report: {PROJECT_ID}

**Coach:** {COACH_NAME}
**Tribe:** {TRIBE_NAME} (from {TRIBE_SOUL} path)
**Word Count:** [MUST BE 2400-3000]
**Total Named References:** [MUST BE 24+]

---

## 1. CELEBRITIES & INFLUENCERS (Priority 1)

The audience recognizes these faces. AI cannot generate them.

### 1.1 Health & Wellness Influencers
| Name | Platform | URL | Why Tribe Knows Them |
|---|---|---|---|
| {from tribe_soul.shared_heroes} | {platform} | [URL] | {from hero.evidence} |
| [NAMED PERSON] | [PLATFORM] | [URL] | [CONNECTION TO TRIBE] |

### 1.2 Fashion & Culture Icons
| Name | Brand/Platform | URL | Why Tribe Knows Them |
|---|---|---|---|
| [NAMED PERSON] | [BRAND] | [URL] | [REASON] |

### 1.3 "Grande Sœur" / Trusted Figures
| Name | Platform | URL | Why Tribe Knows Them |
|---|---|---|---|
| [NAMED PERSON] | [PLATFORM] | [URL] | [REASON] |

---

## 2. REAL-LIFE CONTEXTUAL OBJECTS (Priority 2)

AI approximates these. E-Roll sources the REAL thing.

### 2.1 Traditional Pharmacopeia / Rituals
| Object | Search Terms | Source Image URL | Cultural Significance |
|---|---|---|---|
| {from tribe_soul.tribe_slang where object is mentioned} | [SEARCH TERM] | [URL] | {from slang.example_quote} |

### 2.2 Textiles & Patterns
| Object | Search Terms | Source Image URL | Cultural Significance |
|---|---|---|---|
| {extracted from tribe descriptions} | [SEARCH TERM] | [URL] | [MEANING] |

---

## 3. DOCUMENTARY / ARCHIVAL SOURCES (Priority 3)

These provide social proof and legitimacy.

### 3.1 Documentation of Shared Enemies
| Topic | Source | URL | Key Quote/Image |
|---|---|---|---|
| {from tribe_soul.common_enemies} | [PUBLICATION] | [URL] | {from enemy.evidence} |

### 3.2 Diaspora Experience
| Topic | Source | URL | Key Quote/Image |
|---|---|---|---|
| [TOPIC] | [PUBLICATION] | [URL] | [KEY QUOTE] |

---

## 4. NOSTALGIC AESTHETICS (Priority 4)

AI cannot recreate authentic time-period photography.

### 4.1 Archival Photography
| Era/Location | Search Terms | Source Archive | What It Evokes |
|---|---|---|---|
| {inferred from tribe geographic origin} | [SEARCH TERM] | [ARCHIVE] | [NOSTALGIA TRIGGER] |

---

## 5. INSIDE JOKES / VIRAL FORMATS (Priority 5)

Screenshots and stills from content the tribe has already seen.

### 5.1 Viral Formats
| Format | Creator | URL | Why It Resonates |
|---|---|---|---|
| {from tribe_soul.inside_jokes} | [CREATOR] | [URL] | {from joke.description} |

---

## Research Sources Index

1. [URL 1]
2. [URL 2]
...
24. [URL 24]

---

**VALIDATION CHECKLIST:**
- [ ] Word count: 2400-3000
- [ ] Named celebrities: 6+ (from Section 1)
- [ ] Named cultural objects: 6+ (from Section 2)
- [ ] Named documents/articles: 4+ (from Section 3)
- [ ] Source URLs: 24+ (from all sections)
- [ ] Every reference traceable to tribe_soul.json
```

---

## 3. Enforcement Mechanisms

### 3.1 Word Count Validation

The Research Commander must verify:
```
if word_count < 2400:
    REJECT("Deep Research Report is too short. Minimum 2400 words.")
if word_count > 3000:
    REJECT("Deep Research Report is too long. Maximum 3000 words.")
```

### 3.2 Named Reference Validation

The Research Commander must verify:
```
for each reference in report:
    if reference is generic (e.g., "African woman", "herbal tea"):
        REJECT("Reference must be NAMED. 'African woman' is not a name.")
    if reference has no URL:
        REJECT("Reference must have source URL.")
```

### 3.3 Query-to-Research Traceability

Every query must cite a specific line from the Deep Research Report:
```json
{
    "query": "Tatiane Van Laethem naturopathe afro-holistique interview",
    "source_reference": "Section 1.1, Row 1 - Tatiane Van Laethem",
    "source_url": "https://instagram.com/tatiane.vanlaethem"
}
```

If a query cannot cite a specific reference, it is REJECTED.

---

## 4. Implementation Options

### Option A: SKILL + Commander (Manual Enforcement)

1. Create `E-ROLL DEEP RESEARCHER.md` SKILL with enforced template
2. Update `E-ROLL RESEARCH COMMANDER.md` with validation checklist
3. Workflow: Researcher → Commander → (Pass/Fail) → Query Generator

**Pros:** Works with current agent architecture
**Cons:** Still relies on agent discipline

### Option B: Python Script Validation (Automated Enforcement)

1. Create `validate_eroll_research.py` script
2. Script parses report, counts words, extracts URLs, validates structure
3. Script returns PASS/FAIL with specific failure reasons

```python
def validate_deep_research(report_path):
    report = read_markdown(report_path)
    
    # Word count
    word_count = len(report.split())
    if word_count < 2400:
        return FAIL("Word count: {word_count}/2400 minimum")
    
    # Named references
    references = extract_references(report)
    generic_refs = [r for r in references if is_generic(r)]
    if generic_refs:
        return FAIL(f"Generic references found: {generic_refs}")
    
    # URL count
    urls = extract_urls(report)
    if len(urls) < 24:
        return FAIL(f"URL count: {len(urls)}/24 minimum")
    
    return PASS
```

**Pros:** Cannot be bypassed, deterministic
**Cons:** Requires script development

### Option C: Workflow Gate (Recommended)

Add to `.agent/workflows/cmf-eroll.md`:

```markdown
## Phase 2: Deep Research (GATED)

// turbo
1. Run `python scripts/validate_eroll_research.py [project_path]`
2. IF FAIL: Stop workflow, display failure reason, return to research
3. IF PASS: Proceed to Query Generation

⛔ DO NOT PROCEED TO QUERY GENERATION IF VALIDATION FAILS
```

**Pros:** Integrates with existing workflow system, automated validation
**Cons:** Requires Python script

---

## 5. Recommended Path Forward

1. **Create** `scripts/validate_eroll_research.py` (automated validation)
2. **Create** `E-ROLL DEEP RESEARCHER.md` SKILL with enforced template
3. **Update** `cmf-eroll.md` workflow with validation gate
4. **Update** `E-ROLL RESEARCH COMMANDER.md` with new checklist

**The key insight:** The problem is not the methodology—it's the lack of enforcement. Adding a Python validation script makes the gate real, not suggested.

---

## 6. Next Steps

1. Do you want me to create the validation script (`validate_eroll_research.py`)?
2. Do you want me to create the Deep Researcher SKILL with the enforced template?
3. Do you want me to update the workflow with the validation gate?
