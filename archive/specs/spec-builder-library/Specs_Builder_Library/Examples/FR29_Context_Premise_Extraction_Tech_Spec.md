# Tech-Spec: FR29 — 12-Dimension Context Premise Extraction (DEP-ENG-006)

**Created:** 2026-03-13
**Status:** Ready for Development
**Version:** 1.0 (Aligned to CCP Architecture v4.0 / Unified PRD v3.1)
**Architecture Reference:** PRD §8.2.3, Context_Premise_Trigger_Matching_Layer
**Skill Implementation:** `CBCS/backend/core/aria.py`, `CBCS/backend/core/transcription.py`
**Role Executing:** Principal CCP Tech-Spec Architect

---

## 1. Files Read

The following files were mandatory prerequisite reading before the architectural design of this component:
- `d:\Work\The Conscious Coaching Factory\docs\prd\prd.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\prd TO UPDATE.md`
- `d:\Work\The Conscious Coaching Factory\lab\CCP update\Context_Premise_Trigger_Matching_Layer.md`

---

## 2. Overview

### Problem Statement
Static user profiles (e.g., "35-year-old male entrepreneur") degrade the coaching illusion because they lack emotional reality. When a user leaves a voice note describing an acute moment of anxiety, and the automated AI responds with generic coaching advice, the session fails. To achieve "neural coupling," the system must understand exactly *who* the user is blaming (Enemies), *what* they secretly believe (Hidden Beliefs), and *how* they are adapting (Coping Mechanisms) in real-time. If taking this snapshot takes 15 seconds, the conversation stalls. 

### Solution
FR29 formally defines the **12-Dimension Context Premise Extraction Engine (DEP-ENG-006)**. Upon receipt of an unstructured voice note in Telegram, the system utilizes Whisper (local or ultra-fast cloud) to transcribe the audio, immediately passes the text to Agent Aria (The Synthesizer) to parse the 12 psychological vectors, and writes the state changes to the user's isolated Neo4j graph database. The entire cycle—transcription, extraction, and DB write—is architecturally bounded to execute in under **5 seconds**, guaranteeing the very next interaction is instantly informed by the updated state.

### Scope
**In scope:**
- Stage 1: Whisper-based audio transcription.
- Stage 2: Aria's 12-dimension semantic extraction.
- Stage 3: Neo4j relationship updates (`FIGHTS_AGAINST`, `FEARS`, `CRAVES`).
- The <5s target latency budget across these three operations.

**Out of scope:**
- Generating the actual coaching response (handled by Artisan + Vidye in FR27).
- Generating the Voice DNA (this is Context Premise, not Voice DNA).

---

## 3. Context for Development

### Architecture Traceability

| DEP-ID / Component | Name | Role in This Pipeline |
|---|---|---|
| `DEP-ENG-006` | Context Premise Map | OUTPUT — The 12-dimension JSON payload structuring the user's current psychological reality. |
| Aria | The Synthesizer | AGENT — The intelligence responsible for reading the transcript and extracting the 12 vectors. |
| `transcription.py` | Audio Processor | LOGIC — The Whisper API execution block converting Telegram .ogg blobs to text. |
| Neo4j | Knowledge Graph | DB — The storage layer tracking the temporal changes in the user's Context Premise over time. |

### Academic Grounding

| Algorithm / Framework | Author | Year | Mechanism / Concept Taught |
|---|---|---|---|
| **Common Ground Theory (L3 Depth)** | Clark & Brennan | 1991 | Outlines that deep coupling only occurs when two entities share *Structural Ground* (moral foundation, coping mechanisms). Aria explicitly hunts for this L3 (Level 3) depth (hidden beliefs over surface wants) so the matching engine has valid structural anchor points to pair with the coach's DNA. |

### Technical Decisions
1. **Zero-Shot LLM Extraction (Fast Model):** The 12-dimension extraction is a massive prompt. To maintain the <2500ms budget, Aria *must* be routed via `ModelRouter` to a high-speed inference tier (e.g., Gemini 1.5 Flash or Groq). If it hits a slow reasoning model, the pipeline will breach the Service Level Agreement (SLA).

Aria's 2500ms extraction budget is architecturally compatible with FR27's <2s felt latency SLA via Ghost Typing activation at T=0ms. These specs are deliberately coordinated. Do not modify Aria's latency budget without updating FR27 simultaneously. # REVISED: Added architectural coordination note for Decision 1.
2. **Deterministic Graph Merges:** Aria does not blindly append new nodes to Neo4j. It uses an `UPSERT` match algorithm. If the user previously feared "running out of money" and today states they fear "going bankrupt," the system merges the semantic similarity rather than creating 50 redundant fear nodes.

---

## 4. Implementation Plan

### Stage 1: Fast Audio Transcription (Target: <1.5s)
*Agent Task:* Background system pipeline
*Inputs:* Telegram Voice Note (`.ogg` payload)
*Outputs:* Raw Text Transcript
*Failure Condition:* Whisper API timeout > 2 seconds.
*Receipt Write:* Per FR47 DEP-ENG-041 schema — # REVISED: Standardized receipt format.
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'FAST-AUDIO-TRANSCRIPTION',
  agent_name: 'Background-Pipeline',
  timestamp }

**Steps:**
1. Pipeline receives the voice payload from Telegram.
2. In-memory buffer passes the audio directly to the Whisper Cloud API (or local instance).
3. Transcript is immediately forwarded to Aria.

### Stage 2: 12-Dimension Extraction (Target: <2500ms) # REVISED: Aligned extraction target
*Agent Name:* Aria (The Synthesizer)
*Inputs:* Raw Text Transcript
*Outputs:* `DEP-ENG-006` Context Premise JSON payload
*Failure Condition:* Aria hallucinates an entity not present in the audio transcript text (e.g., hallucinating an "Enemy" when the user only expressed a "Fear").
*Receipt Write:* Per FR47 DEP-ENG-041 schema — # REVISED: Standardized receipt format.
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: '12-DIMENSION-EXTRACTION',
  agent_name: 'Aria',
  timestamp }

**Steps:**
1. Aria runs the 12-dimensional parsing map over the text. The dimensions are:
   `Wants`, `Frustrations`, `Dreams`, `Fears`, `Suspicions`, `Insecurities`, `Envy Feelings`, `Enemies`, `Coping Mechanism`, `Hidden Beliefs`, `Emotional Triggers`, `Success Markers`.
2. Aria executes the **Hallucination Gate**: Every extracted dimension must quote the exact 3-4 word phrase from the transcript that supports it. If an extraction lacks a direct quote, it is dropped as `<null>`.
3. Aria classifies the depth of the insight (L1 Surface, L2 Private, L3 Structural).

### Stage 3: Neo4j Graph Ontology Update (Target: <1.0s)
*Agent Name:* Azaria (Memory Curator background sync)
*Inputs:* `DEP-ENG-006` JSON
*Outputs:* Confirmed Neo4j Graph Write
*Failure Condition:* Deadlock attempting to write to the graph while CBCS is simultaneously reading it for the actual response.
*Receipt Write:* Per FR47 DEP-ENG-041 schema — # REVISED: Standardized receipt format.
{ receipt_id, previous_receipt_hash,
  input_payload_hash, output_payload_hash,
  stage_name: 'NEO4J-ONTOLOGY-UPDATE',
  agent_name: 'Azaria',
  timestamp }

**Steps:**
1. The JSON vectors are translated into Neo4j Cypher queries.
2. The user entity (`Person`) is updated with new timestamped relationships:
   - `(Person)-[:FEARS {depth: "L3", quote: "..."}]->(Concept)`
   - `(Person)-[:FIGHTS_AGAINST {depth: "L2"}]->(Enemy)`
3. For latency protection, if the Neo4j write transaction pool is saturated, the `DEP-ENG-006` JSON serves as the temporary local working memory for the response generation, and the database write degrades to an asynchronous background task.

---

## 5. Primary Output Schema (DEP-ENG-006 Context Premise)

**Schema Name:** `context_premise_extraction.json`

```json
{
  "user_id": "USR-99X2",
  "transcription_time_ms": 840,
  "extraction_time_ms": 1420,
  "total_latency_ms": 2260,
  "context_premise": {
    "fears": [
      {
        "entity": "public failure",
        "depth_level": "L3",
        "exact_quote": "I'm terrified they'll see I'm faking it"
      }
    ],
    "enemies": [
      {
        "entity": "corporate hierarchy",
        "depth_level": "L1",
        "exact_quote": "my boss won't authorize the budget"
      }
    ],
    "dreams": [],
    "hidden_beliefs": [
      {
        "entity": "imposter syndrome inevitability",
        "depth_level": "L3",
        "exact_quote": "I guess I don't really belong at this level"
      }
    ],
    "coping_mechanism": "workaholic avoidance",
    "emotional_triggers": ["being micromanaged", "email alerts"]
    // Note: Dimensions not detected in the current audio note are returned as empty arrays/null, never hallucinated.
  }
}
```

---

## 6. Backward Compatibility Fallback
If the Telegram client sends an corrupted `.ogg` file, or the Whisper transcription API outright fails, the transcription block throws `[TRANSCRIPT_FAIL]`. Aria is bypassed entirely, the `DEP-ENG-006` object is instantiated as `null`, and the Neo4j database uses the *previous* session's Context Premise map to inform generation. The downstream generation agent is silently appended with the prompt modifier: *"The user sent a voice note that was unintelligible. Acknowledge this politely and ask them to type it or re-send."*

---

## 7. Tasks

- [ ] **Task 1:** Build the `core/transcription.py` module wrapping the Whisper API with an uncompromising 2-second timeout parameter.
- [ ] **Task 2:** Refine Aria's prompt template. Implement the Evidence Grounding rule (must output `exact_quote` for every entity) and map her to `Gemini 1.5 Flash` to secure the 2500ms maximum inference boundary. # REVISED: Aligned extraction boundary
- [ ] **Task 3:** Write the Cypher `MERGE` query factory in `graph_db.py`. It must translate Aria's 12 dimensions into corresponding Neo4j Edge properties without duplicating existing nodes of high similarity.
- [ ] **Task 4:** Wrap the execution sequence in an `asyncio` loop where the Whisper block passes the string to Aria the millisecond it streams in, tracking the aggregate latency threshold.
- [ ] **Task 5:** Implement ADR-01 multi-tenancy constraints on the Neo4j graph ensuring Coach A's clients never share a graph instance with Coach B's clients.

---

## 8. Acceptance Criteria

- [ ] **AC1 (The Extraction Latency Barrier):** A 15-second voice note is submitted. Transcription (1.1s), Extraction (2.2s), and Graph Write (0.4s) complete in exactly 3.7 seconds. *Failure Example:* Aria is routed to a slow reasoning model and takes 6.5 seconds to parse the 12 vectors, breaching the <2500ms SLA for extraction. <2500ms for 12-dimension Context Extraction on transcribed text input. Ghost Typing UX masking active during this window (see FR27). # REVISED: Aligned SLA condition.
- [ ] **AC2 (Anti-Hallucination Gate):** A user submits the voice note: "I am super tired of my commute." Aria returns a `Context Premise` with "Enemies" left `null`. *Failure Example:* Aria hallucinates an "Enemy" of "Public Transportation," despite the user never stating it, polluting the psychological map with false assumptions.
- [ ] **AC3 (Evidence Grounding):** Aria identifies a Hidden Belief. The JSON output includes the exact 4-word quote `"I can't do this"` from the audio. *Failure Example:* Aria outputs the belief but the `exact_quote` field is missing, causing the system to reject the extraction layer.
- [ ] **AC4 (ADR-01 Strict Isolation):** When Aria writes the Context Premise edge for User 123 (a client of Coach Dan), the system specifically mounts the connection pool for Dan's Neo4j schema, completely bypassing Maria's graph DB. *Failure Example:* Dan's client expresses a fear, and Maria's database accidentally imports it because the Cypher query was sent to a shared tenant graph.

---

## 9. Dependencies

| Dependency | Type | Notes |
|---|---|---|
| Whisper API | External | The fast audio transcription engine. |
| ModelRouter | Internal | Required to route Aria to Gemini Flash. |
| Neo4j Driver | Infrastructure | The graph database connection pool. |
| Receipt Chain Guard | Infrastructure | Non-negotiable sequence auditing. |

---

## 10. Testing Strategy

### Unit Tests
- **Hallucination Test:** Feed Aria a transcript containing only L1 factual data ("I bought a coffee today"). Assert that the 12 psychological array returns entirely empty/null.
- **Evidence Extraction Test:** Feed Aria a known trigger phrase ("My mother always said I was lazy"). Assert she correctly maps `Enemies: Mother` and attaches the exact quote to the JSON payload.

### Integration Tests
- **Performance Benchmarking:** Feed a 30-second audio clip through the pipeline locally. Time the exact delta between the ingress trigger and the `CTX-GRAPH` receipt. Assert total execution time `<5.0s`. 
- **Graph State Verification:** Submit a Context Premise JSON payload. Execute the Neo4j write. Run a mock graph read query 1 second later. Assert the correct `(Person)-[:FIGHTS_AGAINST]->(Enemy)` node relationship was successfully committed.

### Safety Tests (ADR-01 Quarantine Security)
- **Tenant Segregation Test:** Instantiate two mock environments (Coach A, Coach B). Send an extraction payload into the pipeline specifically targeting Coach B's user. Run a Cypher query on Coach A's DB. Assert zero side-effects.
