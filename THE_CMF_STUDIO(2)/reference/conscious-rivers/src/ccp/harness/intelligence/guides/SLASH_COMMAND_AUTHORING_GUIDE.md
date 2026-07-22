# ⚡ Slash Command Authoring Guide — How to Write CMF Commands with `write_todos`

> **Purpose:** This guide documents the established patterns and conventions for writing slash command files in the `commands/` directory. These commands orchestrate the CMF pipeline by loading skills, managing step progression via `write_todos`, and enforcing quality gates at every transition.

---

## 1. What Is a Slash Command?

A **slash command** is a markdown file in the `commands/` directory that tells an LLM agent exactly how to execute a multi-step workflow. Unlike a skill (which defines *what* an agent is), a command defines *what an agent does*, step by step, in a single session.

Commands are **orchestrators**. They:
1. Initialize a todo checklist (progress tracking)
2. Verify pre-conditions (pre-flight checks)
3. Load the correct skill files based on routing logic
4. Execute the skill's algorithm in structured steps
5. Generate output files in specified locations
6. Validate all outputs before declaring success
7. Point to the next command in the pipeline

The critical innovation is the `write_todos` system, which forces the LLM to maintain its own progress tracker — preventing it from skipping steps, losing context, or hallucinating completion.

---

## 2. File System Convention

```
commands/{command-name}.md
```

| Element | Convention | Example |
|---------|-----------|---------|
| **Folder** | `commands/` at workspace root | `commands/cmf-hunt.md` |
| **Filename** | `cmf-{verb}.md` (kebab-case) | `cmf-diagnose.md`, `cmf-sonic.md` |
| **Naming pattern** | `cmf-{action}` or `cmf-{action}-{target}` | `cmf-compose-gmg-01.md` |

### Command Families

Commands map to pipeline phases:

| Phase | Commands | Skills Loaded |
|-------|----------|---------------|
| Initialization | `cmf-init` | Project setup scripts |
| Diagnosis | `cmf-diagnose` | `story-doctor`, `arc-selection-guide` |
| Quote Mining | `cmf-hunt` | `{arc}-hunter` + scoring rubric |
| Analysis | `cmf-analyze` | `{arc}-analyst` |
| Composition | `cmf-compose` | `{arc}-composer` |
| Authorization | `cmf-authorize` | `{arc}-commander` |
| Sonic | `cmf-sonic` | `sonic-scribe` |
| Storyboard | `cmf-storyboard` | `storyboard-composer`, `visual-analyst` |
| Motion | `cmf-motion` | `gmg-composer`, `cac-composer` |
| E-Roll | `cmf-eroll` | `deep-researcher-{arc}` |
| Full Pipeline | `cmf-full` | Routes to all of the above |

---

## 3. YAML Frontmatter (Mandatory)

Every command file starts with YAML frontmatter:

```yaml
---
name: cmf-hunt
description: Quote Mining using arc-specific Hunter skill + Scoring Rubric
---
```

| Field | Required | Description |
|-------|----------|-------------|
| `name` | ✅ | The kebab-case command slug (matches filename without `.md`) |
| `description` | ✅ | One-line summary of what the command does |

---

## 4. Anatomy of a Slash Command

After the frontmatter, every command follows a rigid structure:

```
1. Title (H1) with parameter syntax
2. Turbo annotation
3. Base path declarations
4. Objective statement
5. STEP 0: INITIALIZE TODOS
6. Step Execution Protocol (mandatory boilerplate)
7. STEP 1: PRE-FLIGHT
8. STEP 2-N: Core workflow steps
9. STEP FINAL: VALIDATION
10. NEXT COMMAND link
11. Step Execution Protocol (repeated at bottom as reinforcement)
```

### 4.1 Title

The H1 heading shows the command syntax — how the user invokes it:

```markdown
# /cmf-hunt {project_id}
```

Parameters in curly braces (`{project_id}`) are user-supplied. Optional parameters use brackets:

```markdown
# /cmf-init {transcript_path} [--coach "Coach Name"]
```

### 4.2 Turbo Annotation

The comment `// turbo-all` tells the hosting agent platform to auto-approve all tool calls:

```markdown
// turbo-all
```

This is **mandatory** for headless batch execution. Without it, the agent will pause and wait for human approval at every file read/write.

### 4.3 Base Path Declarations

A blockquote section that anchors all relative references:

```markdown
> **SKILLS_BASE:** `skills/cmf/`
> **SCORING_BASE:** `intelligence/frameworks/viral_scoring/`
```

This tells the LLM where to find the files it needs to load.

### 4.4 Objective Statement

A single bold sentence stating the purpose of the command:

```markdown
**Objective:** Extract 24-32 verbatim quotes using arc-specific Hunter skill and scoring rubric.
```

---

## 5. The `write_todos` System (Core Innovation)

The `write_todos` function is the backbone of every command. It creates and updates a progress checklist that the LLM must maintain throughout execution. This is the mechanism that prevents the LLM from skipping steps, losing context mid-session, or falsely claiming completion.

### 5.1 Structure of a `write_todos` Call

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify files exist", status: "pending" },
    { id: "step-2", description: "STEP 2: LOAD SKILL - Read arc-specific skill file", status: "pending" },
    { id: "step-3", description: "STEP 3: EXECUTE - Extract quotes", status: "pending" },
    { id: "step-4", description: "STEP 4: VALIDATE - Confirm quality gates", status: "pending" }
  ]
});
```

### 5.2 The Three Status Values

| Status | Meaning | When to Set |
|--------|---------|-------------|
| `"pending"` | Not yet started | Initial state for all steps |
| `"in_progress"` | Currently executing | Set at the START of each step |
| `"completed"` | Successfully finished | Set AFTER outputs are verified |

### 5.3 The Mandatory Update Pattern

Every step in a command follows this exact four-phase lifecycle:

```
1. BEFORE THE STEP → Call write_todos setting this step to "in_progress"
2. EXECUTE → Perform the actual work
3. VERIFY → Check that outputs exist and match schema
4. AFTER THE STEP → Call write_todos setting this step to "completed"
```

This means **every step has TWO `write_todos` calls** — one at the start and one at the end.

### 5.4 Step 0: Initialize Todos

Every command starts with a dedicated "STEP 0" that calls `write_todos` to set up the entire checklist before any work begins:

```markdown
## 🎯 STEP 0: INITIALIZE TODOS

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - Verify files exist", status: "pending" },
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

**DO NOT PROCEED until you have called `write_todos` above.**
```

The explicit directive "DO NOT PROCEED" is important — it enforces sequencing.

### 5.5 Sub-Steps

When a step has multiple stages, use letter suffixes for the ids:

```javascript
{ id: "step-5", description: "STEP 5A: BUILD narrative_dna - Extract structural framework", status: "pending" },
{ id: "step-5", description: "STEP 5B: DISTILL spr_text - Compress to 48-60 word priming", status: "pending" },
{ id: "step-5", description: "STEP 5C: WRITE strategy_brief.json - Save output file", status: "pending" },
```

Note that sub-steps share the same `id` (e.g., `"step-5"`) and differentiate by description.

### 5.6 The Full `write_todos` at Every Transition

Here is the critical pattern: at every step transition, the **entire** todo list is rewritten, showing the full state of all steps. This is NOT incremental — it is a full snapshot:

```javascript
// When STARTING Step 3:
write_todos({
  todos: [
    { id: "step-1", description: "STEP 1: PRE-FLIGHT - ...", status: "completed" },
    { id: "step-2", description: "STEP 2: IDENTIFY ARC - ...", status: "completed" },
    { id: "step-3", description: "STEP 3: LOAD HUNTER - ...", status: "in_progress" },  // ← Current
    { id: "step-4", description: "STEP 4: LOAD RUBRIC - ...", status: "pending" },
    { id: "step-5", description: "STEP 5: EXECUTE HUNT - ...", status: "pending" },
    { id: "step-6", description: "STEP 6: SCORE QUOTES - ...", status: "pending" },
    { id: "step-7", description: "STEP 7: GENERATE OUTPUT - ...", status: "pending" },
    { id: "step-8", description: "STEP 8: VALIDATE - ...", status: "pending" }
  ]
});
```

The rationale: LLMs can lose track of state during long sessions. By writing the complete snapshot every time, the agent "re-anchors" its understanding of where it is in the workflow.

---

## 6. Step Execution Protocol (Boilerplate)

Every command includes a mandatory boilerplate section that reinforces the `write_todos` contract. This section appears twice — once near the top (after Step 0) and once at the very bottom of the file:

```markdown
## 📋 Step Execution Protocol (MANDATORY)

> [!CAUTION]
> **You MUST call `write_todos` at EVERY step transition.**
> This is not optional. Skipping todo updates = workflow failure.

**For EACH step, follow this pattern:**

1. **START STEP:** Update todo status to `in_progress`
2. **EXECUTE:** Perform the step actions
3. **VALIDATE:** Verify outputs exist
4. **COMPLETE STEP:** Update todo status to `completed`

> [!IMPORTANT]
> **Validation Gate:** Before marking a step `completed`, verify:
> - Output file exists (if applicable)
> - Output matches expected schema
> - No error messages encountered
```

The repetition is deliberate — it reinforces the protocol at both the beginning and end of the context window.

---

## 7. The Standard Step Template

Every step in a command follows this structure:

```markdown
## STEP N: ACTION_NAME

**EXECUTE THIS NOW:**

```javascript
write_todos({
  todos: [
    // Full snapshot with this step set to "in_progress"
  ]
});
```

**ACTIONS:**

| # | Action | Details |
|---|--------|---------|
| 1 | Read file X | Path: `...` |
| 2 | Extract data | Fields: ... |
| 3 | Process | Logic: ... |

**OUTPUT (XX-XX words):**
```
STEP N COMPLETE:
- Result: ✅ [summary]
- File: [filename] created
```

**WHEN COMPLETE, EXECUTE:**

```javascript
write_todos({
  todos: [
    // Full snapshot with this step set to "completed"
  ]
});
```
```

### Key Elements

| Element | Purpose |
|---------|---------|
| `**EXECUTE THIS NOW:**` | Tells the LLM to immediately run the `write_todos` call |
| `**ACTIONS:**` | Lists exactly what to do in this step (often as a table) |
| `**OUTPUT (XX-XX words):**` | Constrains the response length to prevent verbosity |
| `**WHEN COMPLETE, EXECUTE:**` | Marks the transition out of this step |

### Word Count Constraints

Every step specifies an expected output length in parentheses. This prevents the LLM from producing excessively long or short responses:

```markdown
**OUTPUT (30-50 words):**
```

Typical ranges: 20-40 words for pre-flight checks, 50-80 words for analysis steps, 2500-3500 words for full document generation.

---

## 8. PRE-FLIGHT Step (Always Step 1)

Every command starts with a PRE-FLIGHT check that verifies required input files exist:

```markdown
## STEP 1: PRE-FLIGHT

**ACTIONS:**

| # | Check | Path | If Missing |
|---|-------|------|------------|
| 1 | Project folder | `production/Coach Adele/{project_id}/` | STOP |
| 2 | Strategy brief | `{project_id}_strategy_brief.json` | STOP → Run `/cmf-diagnose` first |
| 3 | Transcript | `{project_id}_transcript.md` or `.srt` | STOP |
```

The "If Missing" column always specifies what to do: either `STOP` entirely, or redirect to a prerequisite command.

---

## 9. Routing Tables (Skill Loading)

When a command needs to load a skill dynamically (e.g., selecting the correct Hunter for a given arc), it uses a **routing table**:

```markdown
## STEP 3: LOAD HUNTER SKILL

**ROUTING TABLE:**

| Arc | Skill Path |
|-----|------------|
| The Witness | `skills/cmf/hunters/witness-hunter/SKILL.md` |
| The Breakthrough | `skills/cmf/hunters/breakthrough-hunter/SKILL.md` |
| The Shared Struggle | `skills/cmf/hunters/shared-struggle-hunter/SKILL.md` |
...
```

The LLM reads `selected_arc` from `strategy_brief.json` and looks up the corresponding skill path. The command always includes:

```markdown
**ACTIONS:**
1. Based on `selected_arc`, find the correct skill path from table above
2. Read the FULL skill file (do NOT summarize, do NOT skip sections)
3. Extract the cluster definitions for this arc
```

The instruction "do NOT summarize, do NOT skip sections" is critical — without it, the LLM will try to summarize long skill files to save context.

---

## 10. Validation Steps (Always the Final Step)

Every command ends with a validation step that runs a checklist of quality gates:

```markdown
## STEP N: VALIDATION

**RUN THESE X VALIDATION CHECKS:**

| # | Check | Requirement | Result |
|---|-------|-------------|--------|
| 1 | Quote Count | 24-32 quotes | ✅/❌ |
| 2 | All Timestamps | Every quote has start/end | ✅/❌ |
| 3 | Word Count | Each quote ≥15 words | ✅/❌ |
| 4 | Duration | Each quote ≥5 seconds | ✅/❌ |
| 5 | Scoring | All quotes have S/E/Sp | ✅/❌ |
| 6 | Thresholds | All clusters meet minimums | ✅/❌ |

**IF ANY CHECK FAILS:** STOP → Report failure → Suggest fix
**IF ALL PASS:** [Success output template]
```

### Graduated Validation

Some commands use graduated validation (from `cmf-diagnose`):

```markdown
### Core Checks (4/4 required)
### Narrative DNA Structure Checks (5/5 required)
### Verbatim Checks (3/3 required)
### SPR Text Check (1/1 required)

**TOTAL: [X]/13 PASSED**
```

---

## 11. The NEXT COMMAND Link

Every command ends by telling the agent (and user) what comes next:

```markdown
## 🔗 NEXT COMMAND

`/cmf-analyze {project_id}`
```

This creates the chain that makes the full pipeline self-documenting. The sequence is:

```
/cmf-init → /cmf-diagnose → /cmf-hunt → /cmf-analyze → /cmf-compose →
/cmf-authorize → /cmf-sonic → /cmf-storyboard → /cmf-motion → /cmf-eroll
```

---

## 12. Creating a New Command — Checklist

When creating a new slash command, follow this checklist:

- [ ] Create file: `commands/cmf-{verb}.md`
- [ ] Add YAML frontmatter (`name`, `description`)
- [ ] Write H1 title with parameter syntax: `# /cmf-{verb} {project_id}`
- [ ] Add `// turbo-all` annotation
- [ ] Declare base paths (`SKILLS_BASE`, etc.)
- [ ] Write objective statement
- [ ] Write STEP 0: INITIALIZE TODOS with full `write_todos` call
- [ ] Write Step Execution Protocol boilerplate (copy from existing command)
- [ ] Write STEP 1: PRE-FLIGHT with input file checks
- [ ] Write STEP 2: LOAD SKILL with routing table (if dynamic routing needed)
- [ ] Write STEP 3-N: Core workflow steps, each with:
  - Opening `write_todos` (status → `in_progress`)
  - ACTIONS table or numbered list
  - OUTPUT word count constraint
  - Closing `write_todos` (status → `completed`)
- [ ] Write FINAL STEP: VALIDATION with pass/fail checklist
- [ ] Add NEXT COMMAND link
- [ ] Copy Step Execution Protocol boilerplate at the bottom of the file
- [ ] Test by running in a fresh session

---

## 13. Design Principles

### Every Step is Self-Contained

Each step must contain ALL the information the LLM needs. Assume the LLM might have "forgotten" earlier steps by the time it reaches later ones. This is why:
- Routing tables are in the step that needs them (not at the top)
- Output templates are embedded in the generation step
- The full `write_todos` snapshot is rewritten at every transition

### Constraint Over Freedom

LLMs produce better results when constrained. Every command uses:
- **Word count limits** on outputs (`30-50 words`)
- **Explicit templates** for file content
- **Pass/fail gates** before progression
- **`STOP → Report`** directives for failures

### Redundancy is Intentional

The Step Execution Protocol appears twice. The `write_todos` pattern repeats at every step. This is not a mistake — it is a reliability pattern. LLMs operating on long documents benefit from periodic reinforcement of the rules.

### Session Isolation

Each command is designed for a **single, fresh session**. Commands do not assume any prior context. This enables:
- Parallel execution across different projects
- Failure isolation (retry one step, not the whole pipeline)
- Context window optimization (each session reads only what it needs)

---

## 14. Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Fix |
|-------------|-------------|-----|
| Skipping the initial `write_todos` | LLM has no progress anchor | Always start with STEP 0 |
| Incremental todo updates | LLM loses track of overall state | Always write the FULL snapshot |
| Missing word count constraints | LLM produces walls of text or too-brief responses | Add `(XX-XX words)` to every OUTPUT |
| No `IF MISSING → STOP` in pre-flight | LLM proceeds with missing files and hallucinates | Always define the failure path |
| Hard-coding skill paths | Cannot be reused across arcs | Use routing tables with dynamic `selected_arc` |
| Forgetting the bottom boilerplate | LLM ignores `write_todos` protocol in late steps | Copy the protocol block to the end of every command |
| Single-step validation | Catches errors too late | Add per-step verification before marking `completed` |

---

**END OF SLASH COMMAND AUTHORING GUIDE**
