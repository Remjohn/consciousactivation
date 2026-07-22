# Sovereign CRAL Research Engine — System Architecture Brief

**Status:** Pre-Tech-Spec — Specialized Textual Research Architecture  
**Context:** CRAL V1.0 (Conscious Research Alchemy Lab), CCP Research Orchestrator  
**Feeds Into:** CRAL V2.0 Specification, DEP-ENG-021/022 Implementation  
**Companion Document:** Sovereign Visual Research Engine (separate brief)

---

## 1. The Problem Statement: CRAL's Invisible Dependency

CRAL V1.0 is the most architecturally sophisticated research system in the CCP. Its seven JIT Moments — RELEVANT, BELIEVABLE, UNDENIABLE, RESONANT, SURPRISING, IRREFUTABLE, RELATABLE — each fire a categorically distinct research discipline at a precisely timed dependency resolution point. The Research Planner compiles 40-60 word directives with four constraints per firing. The Moment Executors return 240 words of pure signal. The diagonal research method produces compound emotional authority that no horizontal or vertical research architecture can match.

But CRAL V1.0 has a silent architectural flaw: **it does not specify how the Moment Executors access the internet.**

The specification defines cognitive states, source hierarchies, distillation constraints, human evidence specifications, and quality gates — everything except the actual search infrastructure. The Moment Executors are implicitly dependent on whatever search capability the host LLM provides. If the LLM has web access, the Executor searches. If it does not, the Executor hallucinates. If the LLM's browsing is filtered, rate-limited, or biased toward SEO-optimized content, the Executor's source hierarchy is structurally violated at the infrastructure level regardless of how perfectly the Planner compiled its directive.

This is not a design oversight. CRAL V1.0 was written before the Sovereign Search Harness was conceived. Now that SearXNG provides a deterministic, sovereign, discipline-configurable search substrate, we can close this gap permanently.

---

## 2. The Core Innovation: Moment-to-Category Mapping

The deepest insight from integrating SearXNG with CRAL is that SearXNG's custom category system maps directly onto CRAL's discipline-specific source hierarchies. Each CRAL Moment demands a specific type of source from a specific tier of the internet. SearXNG allows us to pre-configure exactly which search engines are active, at what weight, for each category name. When the Research Planner fires a directive for M6 IRREFUTABLE, it appends `&categories=institutional_prosecution` to the SearXNG JSON endpoint, and the meta-search engine physically cannot return Reddit opinion threads — because the `institutional_prosecution` category does not include Reddit in its engine list.

This is the difference between instructing an agent to "prioritize institutional documents" (which the agent may or may not obey) and physically routing the search traffic through infrastructure that only indexes institutional documents. The constraint moves from the prompt layer to the infrastructure layer, which makes it deterministic.

### 2.1 The Seven Source Categories

| CRAL Moment | SearXNG Category | Active Engines (Weight) | Excluded Engines | Discipline Rationale |
|:---|:---|:---|:---|:---|
| **M1 RELEVANT** | `cultural_now` | Reddit (3.5), Twitter/Nitter (3.0), HackerNews (2.5), Google News (2.0) | Google Scholar, Wikipedia, Wikimedia | Digital Ethnography requires living community discourse, not archival or academic sources. Recency is the primary constraint. |
| **M2 BELIEVABLE** | `precision_journalism` | Google Scholar (3.0), Wikipedia (2.5), Google News (2.0), Bing (1.5) | Reddit, Forums, Twitter | Precision Journalism requires primary documents, named sources, verifiable dates. Social media opinion is inadmissible as M2 evidence. |
| **M3 UNDENIABLE** | `behavioral_science` | Google Scholar (3.5), PubMed (3.0), Semantic Scholar (2.5) | Reddit, Twitter, Forums, General Google | Behavioral Science requires peer-reviewed studies and documented cohort data. The mood-specific prediction gap must be grounded in measured, published research. |
| **M4 RESONANT** | `narrative_journalism` | Google News (3.0), Bing News (2.5), DuckDuckGo (2.0), Google (1.5) | Google Scholar, Reddit | Narrative Non-Fiction requires long-form profile journalism, documented human stories, and testimonial sources. Not academic papers, not social threads. |
| **M5 SURPRISING** | `anomaly_science` | Google Scholar (3.0), ArXiv (2.5), HackerNews (2.0), Google (1.5) | Reddit, Forums | Science Journalism requires counter-intuitive primary research. The anomaly must be grounded in published studies, not anecdotal claims. |
| **M6 IRREFUTABLE** | `institutional_prosecution` | Google (3.0), Bing (3.0), DuckDuckGo (2.5), Google News (2.0) | Reddit, Twitter, Forums, PubMed | Investigative Journalism at maximum source proximity. The agent searches for internal institutional documents, regulatory filings, audit trails, and whistleblower testimony. Social media and academic research are irrelevant to M6's prosecutorial standard. |
| **M7 RELATABLE** | `tribal_vernacular` | Reddit (3.5), Forums (3.0), Twitter/Nitter (2.5), Quora (2.0) | Google Scholar, Wikipedia, PubMed, ArXiv | Oral History requires vernacular testimony from community members. The quality gate is tribal recognition, not factual accuracy. Academic and institutional sources are explicitly excluded because their language is never the tribe's own. |

### 2.2 What This Mapping Enforces

The diagonal research method requires that each moment arrives at a coordinate unreachable without the previous moment. The Moment-to-Category mapping enforces this at the infrastructure level:

- **M2's precision journalism evidence can never contaminate M7's tribal vernacular** — they search different engines entirely.
- **M3's behavioral science findings can never drift into M4's narrative journalism** — Scholar and PubMed do not return profile stories.
- **M1's cultural NOW can never anchor itself in last year's academic paper** — the `cultural_now` category excludes Google Scholar and applies `&time_range=month` by default.

The diagonal is no longer a prompting instruction that the LLM may or may not follow. It is a physical property of the search infrastructure.

---

## 3. The Autocomplete Intelligence Layer: Proactive M1

CRAL V1.0 specifies that M1 RELEVANT fires at session intake, before trigger authentication. The Executor reads "community-native forum discourse" to identify "what tension is currently active in the coach's tribe that was not active six months ago." But M1 fires reactively — after the coach has already opened a session.

The Sovereign CRAL Research Engine adds a proactive layer: the **Autocomplete Polling Engine**. This is a Python service running continuously on the SearXNG EC2 host that monitors the tribal information landscape between sessions.

### 3.1 How It Works

1. **Seed Phrase Generation:** For each active coach in the CCP, the system maintains a `tribe_seed_phrases` registry derived from the coach's `tribe_profile`, active tribal nouns from the TIAR (Tribal Imagen Activation Registry), and the most recent M1 findings stored in the CRAL Finding Registry.
2. **15-Minute Polling Cycle:** Every 15 minutes, the service pings the SearXNG autocomplete endpoint with each seed phrase: `http://searxng:8080/autocomplete?q={{seed_phrase}}`. SearXNG aggregates autocomplete suggestions from Google, Bing, DuckDuckGo, and YouTube simultaneously.
3. **Delta Detection:** The service compares the current autocomplete results against the previous cycle's snapshot stored in Redis. New phrases that appear — the "Zero-to-One Spike" — are flagged as emerging tribal signals.
4. **M1 Pre-Computation:** When a coach opens a new session, the Telegram bot's intake question generator does not wait for M1 to fire from scratch. It reads the pre-computed autocomplete delta from the last 24 hours and immediately references the most significant tribal shift: "I'm seeing a lot of conversation in your space about {{emerging_topic}} this week — is that connected to what you're bringing today?"

This transforms M1 from a reactive cultural scan into a proactive cultural intelligence system that monitors the tribe's information metabolism 24/7 and primes every coaching session with pre-computed relevance.

### 3.2 The Compound Effect on CRAL's Diagonal

Pre-computed M1 intelligence does not merely speed up the pipeline. It deepens the entire diagonal. When M1 arrives richer, the Research Planner compiles a sharper M2 directive. A sharper M2 finding produces a more precisely targeted M3 prediction gap. A more precise M3 produces a better-calibrated M5 surprise. The quality of the entire seven-moment sequence is a function of M1's richness — and the Autocomplete Polling Engine makes M1 maximally rich before the session even begins.

---

## 4. The Epistemic Friction Swarm: Trend Validation for CRAL

CRAL's Research Orchestrator runs an OODA loop monitoring dependency resolution events. But the Orchestrator currently lacks the ability to evaluate conflicting signals — when M2 and M6 produce contradictory mechanism evidence, the Builder Engine Step 3.5 flags for coach review. This is a human rescue point.

Drawing from the ChatGPT epistemic engine analysis, we integrate a **6-Agent Epistemic Friction Swarm** into the CRAL pipeline. This swarm operates specifically at the conflict detection layer, not as a replacement for the Moment Executors, but as an adversarial validation layer that runs whenever the Research Orchestrator detects inter-moment tension.

### 4.1 The Six Agents Applied to CRAL

1. **Signal Extractor** — Reads the raw SearXNG JSON responses for the conflicting moments. Computes cross-engine concordance and semantic similarity scores between the contradictory findings.
2. **Pattern Builder** — Clusters the contradictory findings to determine whether they represent genuine mechanism complexity (the mechanism has multiple documented aspects) or research noise (one finding is from a low-quality source).
3. **Contrarian Agent** — Structurally attacks the stronger finding. If M6's institutional document appears irrefutable, the Contrarian searches SearXNG for counter-evidence, retractions, legal challenges to the document's validity.
4. **Contextualizer** — Cross-references both findings against the Standing Trigger Intelligence library. Has this trigger category produced similar conflicts in previous sessions? If so, how were they resolved?
5. **Speculator** — Asks: "If both findings are true simultaneously, what does that imply about the mechanism?" Sometimes the contradiction is the insight — the mechanism operates differently at different scales.
6. **Synthesizer (Judge)** — Produces a resolved finding with a confidence score and a rationale that the Assembler can embed into the content. The audience receives not a contradiction but a compound truth.

The critical design principle: **the Contrarian Agent must reduce the confidence score of every finding it evaluates before the Synthesizer can accept it.** This prevents the hallucination cascades that occur when multi-agent systems converge too quickly into agreement.

---

## 5. The Standing Trigger Intelligence Accelerator

CRAL V1.0's implementation roadmap specifies that Phase 5 (Weeks 15-20) will build a Standing Trigger Intelligence library — pre-researched mechanism evidence indexed to the Trigger Map that reduces M2 and M6 execution time on repeat trigger categories. SearXNG transforms the economics of this library.

### 5.1 The Compound Caching Strategy

When M2 BELIEVABLE fires and the Research Planner routes the directive through the `precision_journalism` SearXNG category, the JSON response includes 50 results with full metadata (titles, snippets, URLs, publication dates, engine sources). Currently, this data is consumed by the Executor, distilled into a 240-word finding, and the raw JSON is discarded.

With the Sovereign CRAL Engine, we implement a **Finding-Linked Source Cache:**

1. **Raw JSON Persistence:** Every SearXNG JSON response is stored in the CRAL Finding Registry alongside the moment's finding, linked to the trigger category and the coach's `tribe_profile`.
2. **Cross-Session Pattern Detection:** When M2 fires for the same trigger category in a future session (different coach, different mood state), the Research Planner first queries the Finding Registry for cached JSON from previous M2 executions on this trigger.
3. **Cached Source Prioritization:** If 3+ previous M2 sessions for this trigger category converge on the same institutional source document, that document is promoted to Tier 0 — the Executor receives it directly without querying SearXNG at all.
4. **Freshness Decay:** Cached sources decay over time. After 90 days with no reconfirmation, a cached source drops from Tier 0 back to the standard SearXNG query flow.

This creates a compound intelligence effect: the more sessions CRAL runs, the faster and more precise its M2 and M6 Executors become for known trigger categories. Novel triggers still run the full SearXNG query loop. But repeat triggers — which constitute the majority of production sessions — execute in a fraction of the time with higher confidence.

### 5.2 The Scale Economics

| Metric | CRAL V1.0 (No Cache) | Sovereign CRAL V2.0 (Finding Cache) |
|:---|:---:|:---:|
| M2 execution time (novel trigger) | ~45 seconds | ~45 seconds |
| M2 execution time (repeat trigger) | ~45 seconds | ~5 seconds (cache hit) |
| M6 execution time (novel trigger) | ~60 seconds | ~60 seconds |
| M6 execution time (repeat trigger) | ~60 seconds | ~8 seconds (cache hit) |
| Total 7-moment research time (novel) | ~5 minutes | ~5 minutes |
| Total 7-moment research time (repeat) | ~5 minutes | ~1.5 minutes |
| Research quality on repeat triggers | Same as novel | Higher (converged source confidence) |

---

## 6. The Viral Memetic Feed: CRAL's Connection to the Content Calendar

CRAL is an upstream intelligence system for individual coaching sessions. But the CCP also needs strategic intelligence for the content calendar — deciding which topics to produce content about next week. The Sovereign CRAL Engine connects these two layers through the SearXNG viral signal pipeline.

### 6.1 The 14-Parameter Viral Signal Engine

Drawing from the Gemini analysis, we implement 14 measurable signal parameters computed from raw SearXNG JSON responses:

**Velocity Signals (4):** Autocomplete Emergence Rank, Zero-to-One Spike, Query Mutation Rate, Temporal Velocity (1h vs 24h content volume).

**Consensus Signals (3):** Cross-Engine Concordance, Engine Divergence Score, Result Rank Volatility across polling cycles.

**Content Signals (4):** Publication Timestamp Density, New Domain Emergence Rate, Entity Co-occurrence, Headline Pattern Clustering.

**Quality Signals (3):** Snippet Sentiment Shift, Niche Engine Triggering (does it appear in Scholar or HN?), Geographic Localization Variance.

These 14 parameters are computed by the Autocomplete Polling Engine as a secondary output alongside its M1 pre-computation work. When a tribal topic crosses a configurable signal magnitude on 3+ velocity parameters simultaneously, it is promoted to the Content Strategy Dashboard as a "Validated Tribal Trend" — ready for the content calendar to schedule a full coaching content production cycle around it.

### 6.2 The Feedback Loop to CRAL

When a Validated Tribal Trend becomes a scheduled content topic, CRAL's Research Orchestrator receives the trend's full signal profile as an additional dependency at session start. This means M1 RELEVANT does not merely scan the cultural NOW — it arrives with a pre-validated trend already identified, including its temporal velocity, sentiment polarity, and cross-engine concordance score. The Planner uses this data to compile an M1 directive that is sharper than any reactive cultural scan could produce.

---

## 7. Implementation Prerequisites

### 7.1 SearXNG Category Configuration

Seven custom categories must be created in `settings.yml`, each with precisely defined engine lists and weights as specified in Section 2.1. These configurations must be validated against real-world queries before production use:
- Run 5 test directives per category against real trigger categories from existing coaching sessions
- Verify that the returned JSON exclusively contains sources matching the moment's discipline hierarchy
- Confirm that excluded engines produce zero results in each category

### 7.2 Redis Cache Schema

The Finding-Linked Source Cache requires an extension to the existing Redis schema used for SearXNG query caching. The cache must support:
- Trigger-category-indexed storage of raw SearXNG JSON responses
- Cross-session linking (same trigger → same cache bucket regardless of coach)
- 90-day TTL with freshness decay scoring
- Automatic Tier 0 promotion when 3+ sessions converge on the same source document

### 7.3 Autocomplete Polling Service

A lightweight FastAPI service running on the SearXNG EC2 host:
- Polls SearXNG autocomplete every 15 minutes per active coach's seed phrases
- Stores snapshots in Redis with timestamp indexing
- Computes deltas and fires M1 pre-computation triggers to the CRAL Finding Registry
- Exposes a `/api/tribe_signals/{{coach_id}}` endpoint for the Telegram bot to query at session start

> [!CAUTION]
> **Validation Requirement:** The Moment-to-Category mapping must be empirically validated before PRD commitment. Run at least 3 complete 7-moment CRAL sessions through the category-weighted SearXNG configuration. If any Moment Executor receives sources that violate its discipline hierarchy (e.g., M7 receives an academic paper), the category engine weights must be recalibrated before deployment.
