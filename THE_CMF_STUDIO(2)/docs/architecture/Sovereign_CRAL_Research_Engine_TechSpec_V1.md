# Sovereign CRAL Research Engine (SCRE) — Technical Specification V1.0

**Author:** CCP Engineering Division
**Date:** 2026-04-07
**Version:** 1.0
**Status:** Technical Specification — Build Ready
**Supersedes:** CRAL Documentation V1.0 Section 03 (System Architecture — implicit search infrastructure)
**Feeds Into:** CRAL V2.0 Specification, CMF Agentic Architecture PRD Update, AWS Infrastructure Provisioning
**Architecture Brief:** Sovereign CRAL Research Engine Architecture Brief V1.0
**External References:**
- [SearXNG Repository](https://github.com/searxng/searxng) — Meta-search engine, self-hosted
- [SearXNG Documentation](https://docs.searxng.org/) — Configuration reference for `settings.yml`
- CRAL Documentation V1.0 — Sections 03–07 (System Architecture, Seven JIT Moments, Nine Skills)
- Sovereign Visual Research Engine TechSpec V1.0 — Shared SearXNG infrastructure (same Docker deployment)

---

## Document Purpose

This specification defines the complete buildable architecture for the Sovereign CRAL Research Engine — the upgrade to the CRAL's Moment Executor search infrastructure that replaces implicit LLM browsing dependence with explicit SearXNG category routing, adds proactive M1 intelligence via the Autocomplete Polling Engine, implements the Epistemic Friction Swarm for inter-moment conflict resolution, and introduces the Finding-Linked Source Cache for compound acceleration on repeat trigger categories.

Every section resolves to a buildable system component: a SearXNG category configuration, a FastAPI service, a Redis cache schema, a composable SKILL update, an agent component, or a validation gate.

**CRITICAL: Shared Infrastructure.** This specification shares the SearXNG Docker deployment with the Sovereign Visual Research Engine TechSpec V1.0. The `settings.yml` defined in SVRE TechSpec Section 1.2 already contains all CRAL-specific category and engine configurations. This document specifies only the CRAL-specific components that layer on top of the shared infrastructure.

**What this spec changes from CRAL V1.0:**
- All seven Moment Executors receive explicit SearXNG category routing — no longer dependent on host LLM browsing
- New service: Autocomplete Polling Engine for proactive M1 pre-computation
- New agent layer: Epistemic Friction Swarm for inter-moment conflict resolution
- New dependency: DEP-ENG-060 (Finding-Linked Source Cache)
- New dependency: DEP-ENG-061 (Tribe Seed Phrases Registry)
- New dependency: DEP-ENG-062 (Viral Signal Configuration)
- Research Planner directive compilation gains `&categories={{moment_category}}` parameter

**What this spec does NOT change:**
- The seven JIT Moments — definitions, firing conditions, dependency maps unchanged
- The Research Planner — directive compilation logic unchanged (40-60 word question generation)
- The Research Orchestrator — OODA loop monitoring unchanged
- The 240-word signal output contract — unchanged
- The diagonal research progression — unchanged (enforcement is strengthened, not altered)
- The human evidence bias — unchanged
- The Archetype Assembler integration — unchanged

---

## Section 1 — Moment-to-Category SearXNG Routing

### 1.1 The Architectural Principle

CRAL V1.0 specifies seven discipline-specific source hierarchies — one per Moment Executor. Digital ethnography for M1, precision journalism for M2, behavioral science for M3, etc. But V1.0 does not specify *how* these source hierarchies are enforced at the infrastructure level. The Moment Executors implicitly use whatever search access the host LLM provides, which means a single incorrectly configured browsing tool can route M7's oral history search through Google Scholar, violating the source hierarchy.

The Sovereign CRAL Engine enforces each source hierarchy **at the SearXNG category level.** When the Research Planner fires a directive for M6 IRREFUTABLE, it appends `&categories=institutional_prosecution` to the SearXNG JSON endpoint. This category is configured to route exclusively to Google (3.0), Bing (3.0), DuckDuckGo (2.5), and Google News (2.0) — with Reddit, Twitter, forums, and academic engines completely excluded from the engine list. The M6 Executor physically cannot receive a Reddit opinion thread because the infrastructure does not query Reddit for that category.

### 1.2 Category Routing Table

The seven SearXNG categories for CRAL are already defined in the shared `settings.yml` (SVRE TechSpec Section 1.2). This table specifies how each CRAL Moment maps to its category:

| CRAL Moment | SearXNG Category | Active Engines (Weight) | Excluded Engines | CRAL V1.0 Discipline |
|:---|:---|:---|:---|:---|
| **M1 RELEVANT** | `cultural_now` | Reddit (3.5), HackerNews (2.0), Google News (2.5) | Google Scholar, Wikipedia, PubMed, ArXiv | Digital Ethnography / Netnography |
| **M2 BELIEVABLE** | `precision_journalism` | Google Scholar (3.0), Wikipedia (2.5), Bing (2.5) | Reddit, Forums, Twitter | Precision Journalism |
| **M3 UNDENIABLE** | `behavioral_science` | Google Scholar (3.5), PubMed (3.0) | Reddit, Twitter, Forums, General Search | Cognitive Bias Research |
| **M4 RESONANT** | `narrative_journalism` | Google News (3.0), Bing News (2.5), DuckDuckGo (2.0), Google (1.5) | Google Scholar, Reddit | Narrative Non-Fiction |
| **M5 SURPRISING** | `anomaly_science` | Google Scholar (3.0), ArXiv (2.5), HackerNews (2.0), Google (1.5) | Reddit, Forums | Philosophy of Productive Surprise |
| **M6 IRREFUTABLE** | `institutional_prosecution` | Google (3.0), Bing (3.0), DuckDuckGo (2.5), Google News (2.0) | Reddit, Twitter, Forums, PubMed | Investigative Journalism |
| **M7 RELATABLE** | `tribal_vernacular` | Reddit (3.5), Forums (3.0), Quora (2.0) | Google Scholar, Wikipedia, PubMed, ArXiv | Oral History Methodology |

### 1.3 Research Planner Directive Upgrade

The Research Planner's directive compilation logic (CRAL V1.0 Section 05) is unchanged in its cognitive process. The single change is in how the compiled directive is delivered to the Moment Executor.

**CRAL V1.0 (Current):**
```
Planner compiles 40-60 word directive → passes to Moment Executor → Executor uses host LLM browsing
```

**CRAL V2.0 (Sovereign):**
```
Planner compiles 40-60 word directive → appends category routing → passes to Moment Executor
Executor queries: http://ccp-searxng:8080/search?q={{directive_as_query}}&format=json&categories={{moment_category}}&time_range={{moment_time_range}}
```

**Directive Routing Schema:**

```json
{
  "moment_routing": {
    "M1_RELEVANT": {
      "category": "cultural_now",
      "time_range": "month",
      "default_results": 30,
      "rationale": "M1 needs recency — cultural NOW means last 30 days maximum"
    },
    "M2_BELIEVABLE": {
      "category": "precision_journalism",
      "time_range": null,
      "default_results": 20,
      "rationale": "M2 needs precision — no time constraint, best documented instance regardless of date"
    },
    "M3_UNDENIABLE": {
      "category": "behavioral_science",
      "time_range": null,
      "default_results": 15,
      "rationale": "M3 needs peer-reviewed — academic research is timeless, no recency filter"
    },
    "M4_RESONANT": {
      "category": "narrative_journalism",
      "time_range": "year",
      "default_results": 20,
      "rationale": "M4 needs long-form profiles — within last year keeps stories culturally current"
    },
    "M5_SURPRISING": {
      "category": "anomaly_science",
      "time_range": null,
      "default_results": 15,
      "rationale": "M5 needs counter-intuitive research — the best anomalies may be decades old"
    },
    "M6_IRREFUTABLE": {
      "category": "institutional_prosecution",
      "time_range": null,
      "default_results": 20,
      "rationale": "M6 needs internal documents — regulatory filings and audit trails are undated"
    },
    "M7_RELATABLE": {
      "category": "tribal_vernacular",
      "time_range": "year",
      "default_results": 30,
      "rationale": "M7 needs vernacular testimony — recent forum posts capture current tribal language"
    }
  }
}
```

### 1.4 Moment Executor Search Skill Upgrade

Each Moment Executor's search capability is formalized as a composable SKILL with the three-block schema:

```yaml
skill_id: "SKILL-RES-SEARCH"
skill_name: "cral_moment_sovereign_search"
skill_family: "research"
composable: true
replaces: "Implicit host LLM browsing"

api_endpoint: "http://ccp-searxng:8080/search"
infrastructure: "Shared SearXNG Docker container (see SVRE TechSpec Section 1)"

block_a_invariants:
  - "Query is the Research Planner's compiled 40-60 word directive — passed verbatim"
  - "Category is determined by moment_routing table — never overridden by the Executor"
  - "Time range is determined by moment_routing table — moment-specific"
  - "Results are raw JSON from SearXNG — Executor performs discipline-specific distillation"
  - "The Executor NEVER queries outside its assigned category"

block_b_runtime_injections:
  q: "{{planner_directive}}"
  format: "json"
  categories: "{{moment_routing[moment_id].category}}"
  time_range: "{{moment_routing[moment_id].time_range}}"
  pageno: 1

block_c_validation:
  - "SearXNG returns >= 5 results with non-empty content fields"
  - "If < 5 results: Executor refines query using SearXNG autocomplete suggestions"
  - "If refined query also < 5 results: Executor flags sparse_evidence to Orchestrator"
  - "Orchestrator may authorize cross-category search in exceptional cases (logged)"

output:
  format: "raw_searxng_json"
  processing: "Executor performs discipline-specific distillation to 240-word finding"
```

---

## Section 2 — Autocomplete Polling Engine

### 2.1 Service Overview

The Autocomplete Polling Engine is a FastAPI service running on the SearXNG EC2 host. It monitors the tribal information landscape between coaching sessions, pre-computing M1 RELEVANT intelligence so that CRAL's first moment arrives rich before the coach even opens a session.

### 2.2 FastAPI Service Specification

```python
# autocomplete_polling/main.py — architecture specification

from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import httpx
import json

app = FastAPI(title="CCP Autocomplete Polling Engine", version="1.0")

SEARXNG_URL = "http://ccp-searxng:8080/autocomplete"
REDIS_URL = "redis://ccp-searxng-redis:6379/1"  # DB 1 (DB 0 used by SearXNG cache)
POLL_INTERVAL_MINUTES = 15

class AutocompletePoller:
    """
    Polls SearXNG autocomplete endpoint with tribe seed phrases every 15 minutes.
    Detects Zero-to-One Spikes by comparing current results against previous snapshot.
    Pre-computes M1 RELEVANT intelligence for proactive session priming.
    """
    
    async def poll_tribe(self, coach_id: str, seed_phrases: list[str]):
        """
        For each seed phrase, query SearXNG autocomplete, store snapshot,
        compute delta against previous snapshot, flag emerging signals.
        """
        current_snapshot = {}
        
        for phrase in seed_phrases:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    SEARXNG_URL,
                    params={"q": phrase}
                )
                suggestions = response.json()  # list of strings
                current_snapshot[phrase] = suggestions
        
        # Load previous snapshot from Redis
        previous_snapshot = await self.redis.get(f"autocomplete:{coach_id}")
        previous_snapshot = json.loads(previous_snapshot) if previous_snapshot else {}
        
        # Compute delta
        emerging_signals = []
        for phrase, current_suggestions in current_snapshot.items():
            previous_suggestions = previous_snapshot.get(phrase, [])
            new_suggestions = [s for s in current_suggestions if s not in previous_suggestions]
            
            if new_suggestions:
                emerging_signals.append({
                    "seed_phrase": phrase,
                    "new_autocomplete": new_suggestions,
                    "signal_type": "zero_to_one_spike",
                    "detected_at": datetime.utcnow().isoformat(),
                    "coach_id": coach_id
                })
        
        # Store current snapshot
        await self.redis.set(
            f"autocomplete:{coach_id}",
            json.dumps(current_snapshot),
            ex=86400  # 24h TTL
        )
        
        # Store emerging signals
        if emerging_signals:
            await self.redis.lpush(
                f"signals:{coach_id}",
                json.dumps(emerging_signals)
            )
            # Receipt Write: Per FR47 DEP-ENG-041 schema — { stage_name: 'Signal_Emergence', agent_name: 'Autocomplete_Poller' }
        
        return emerging_signals
    
    async def compute_viral_parameters(self, signal: dict) -> dict:
        """
        Compute the 14 viral signal parameters for an emerging signal.
        Uses SearXNG full search to gather structural data.
        """
        query = signal["new_autocomplete"][0]
        
        # Full search to gather structural data
        async with httpx.AsyncClient() as client:
            # Search last 24 hours
            day_results = await client.get(
                "http://ccp-searxng:8080/search",
                params={"q": query, "format": "json", "time_range": "day"}
            )
            # Search last week
            week_results = await client.get(
                "http://ccp-searxng:8080/search",
                params={"q": query, "format": "json", "time_range": "week"}
            )
        
        day_data = day_results.json()
        week_data = week_results.json()
        
        return {
            "autocomplete_emergence_rank": signal.get("rank", 0),
            "zero_to_one_spike": True,
            "cross_engine_concordance": self._compute_concordance(day_data),
            "engine_divergence_score": self._compute_divergence(day_data),
            "temporal_velocity": len(day_data["results"]) / max(len(week_data["results"]), 1),
            "platform_dispersion_ratio": self._compute_dispersion(day_data),
            "result_freshness_clustering": self._compute_freshness_variance(day_data),
            "entity_co_occurrence": self._extract_entities(day_data),
            "query_mutation_rate": self._count_mutations(day_data),
            "headline_pattern_clustering": self._cluster_headlines(day_data),
            "snippet_sentiment_shift": self._analyze_sentiment(day_data),
            "content_volume_spike": len(day_data["results"]),
            "niche_engine_triggering": self._check_niche_engines(day_data),
            "geographic_variance": 0.0  # requires multi-region proxy — Phase 2
        }

# API Endpoints

@app.get("/api/tribe_signals/{coach_id}")
async def get_tribe_signals(coach_id: str):
    """
    Called by the Telegram bot at session start.
    Returns pre-computed M1 RELEVANT intelligence.
    """
    signals = await redis.lrange(f"signals:{coach_id}", 0, -1)
    return {
        "coach_id": coach_id,
        "emerging_signals": [json.loads(s) for s in signals],
        "last_polled": await redis.get(f"last_poll:{coach_id}")
    }

@app.get("/api/viral_trends/{coach_id}")
async def get_viral_trends(coach_id: str):
    """
    Called by the Content Strategy Dashboard.
    Returns validated tribal trends specifically mapped to the active coach's ecosystem.
    ADR-01 Enforced: Aggregates signals exclusively from the coach's allowed intelligence pool.
    """
    # Aggregate valid signals restricted to the specific coach's scope
    pass

@app.post("/api/seed_phrases/{coach_id}")
async def update_seed_phrases(coach_id: str, phrases: list[str]):
    """
    Called when a coach's tribe_profile or TIAR is updated.
    Updates the seed phrases used for autocomplete polling.
    """
    await redis.set(f"seeds:{coach_id}", json.dumps(phrases))
    return {"status": "updated", "phrase_count": len(phrases)}
```

### 2.3 Dependency: Tribe Seed Phrases Registry (DEP-ENG-061)

```json
{
  "dependency_id": "DEP-ENG-061",
  "name": "Tribe Seed Phrases Registry",
  "version": "1.0",
  "description": "Per-coach seed phrases derived from tribe_profile, active tribal nouns (TIAR), and recent M1 findings. Updated when tribe_profile changes or after each CRAL session.",
  "schema": {
    "coach_id": "string",
    "seed_phrases": [
      "string — derived from tribe_profile.coaching_segment",
      "string — derived from TIAR active tribal nouns",
      "string — derived from most recent M1 finding keywords"
    ],
    "last_updated": "ISO 8601 timestamp",
    "source_dependencies": [
      "tribe_profile",
      "DEP-VIS-001 (TIAR)",
      "CRAL Finding Registry (M1 most recent)"
    ]
  },
  "generation_rules": [
    "Each coach has 10-20 seed phrases",
    "Phrases are 2-4 words each — optimized for autocomplete query length",
    "Phrases combine coaching segment + tribal noun: e.g., 'coaching burnout', 'conscious business integrity'",
    "Updated automatically after each CRAL session and when tribe_profile changes"
  ]
}
```

---

## Section 3 — Finding-Linked Source Cache (DEP-ENG-060)

### 3.1 Architecture

Every time a Moment Executor queries SearXNG, the raw JSON response is stored alongside the distilled 240-word finding in the CRAL Finding Registry. This creates a compound intelligence effect: the more sessions CRAL runs, the faster repeat trigger categories resolve.

### 3.2 Redis Cache Schema

```json
{
  "dependency_id": "DEP-ENG-060",
  "name": "Finding-Linked Source Cache",
  "version": "1.0",
  "storage": "Redis DB 2 (DB 0 = SearXNG cache, DB 1 = autocomplete snapshots)",
  "schema": {
    "cache_key": "finding_cache:{{trigger_category}}:{{moment_id}}",
    "value": {
      "trigger_category": "string — from DEP-ENG-007 trigger map",
      "moment_id": "M1|M2|M3|M4|M5|M6|M7",
      "searxng_raw_json": "complete SearXNG JSON response (stored as gzip)",
      "finding_text": "240-word distilled finding",
      "emotional_register": "string — T|V|R",
      "source_urls_used": ["url1", "url2", "url3"],
      "convergence_count": 0,
      "first_cached": "ISO 8601 timestamp",
      "last_confirmed": "ISO 8601 timestamp",
      "ttl_days": 90,
      "tier": 0
    }
  },
  "tier_promotion_rules": {
    "tier_0_threshold": "convergence_count >= 3",
    "tier_0_behavior": "Executor receives cached source URLs directly — SearXNG query skipped",
    "tier_1_default": "Standard SearXNG query flow",
    "demotion_rule": "If last_confirmed > 90 days, demote from Tier 0 to Tier 1",
    "m1_bypass_rule": "M1_RELEVANT queries must bypass Tier 0 completely to preserve the 30-day Cultural Now constraint. M1 queries generate standalone 24-hour micro-caches that never promote to Tier 0."
  },
  "convergence_logic": {
    "description": "When a new CRAL session fires M2 for the same trigger category, the raw JSON response is compared against existing cache entries. If 2+ source URLs from the new response match URLs in the cached response, convergence_count is incremented.",
    "matching_threshold": "2+ shared source URLs = convergence"
  }
}
```

### 3.3 Executor Cache Integration

```yaml
# Moment Executor cache-aware execution flow

executor_cache_flow:
  step_1_cache_check:
    action: "Query Redis for finding_cache:{{trigger_category}}:{{moment_id}}"
    if_tier_0_hit:
      - "Load cached source_urls_used"
      - "Pass directly to discipline-specific distillation"
      - "Skip SearXNG query entirely"
      - "Update last_confirmed timestamp"
    if_tier_1_or_miss:
      - "Execute standard SearXNG query via SKILL-RES-SEARCH"
      - "After distillation: store raw JSON + finding in cache"
      - "Receipt Write: Per FR47 DEP-ENG-041 schema — { stage_name: 'Cache_Update', agent_name: 'Moment_Executor' }"
      - "Compute convergence against existing cache entries"
      - "If convergence_count reaches 3: promote to Tier 0"
  
  step_2_distillation:
    action: "Standard CRAL discipline-specific distillation"
    input: "SearXNG raw JSON OR cached source URLs"
    output: "240-word finding with emotional register tag and verifiability citation"
    constraint: "Distillation quality must be identical regardless of cache/live source"
```

---

## Section 4 — Epistemic Friction Swarm

### 4.1 Activation Condition

The Epistemic Friction Swarm activates when the Research Orchestrator detects inter-moment tension — specifically, when findings from two or more moments contain contradictory mechanism evidence. Currently (CRAL V1.0), this triggers a Builder Engine Step 3.5 flag for coach review. The Swarm replaces this human rescue point with autonomous adversarial resolution.

### 4.2 The Six Agents

```json
{
  "epistemic_friction_swarm": {
    "activation_condition": "Orchestrator detects contradiction between M2/M6 findings OR M3/M5 findings",
    "agents": [
      {
        "name": "Signal Extractor",
        "role": "Raw data analysis — no interpretation",
        "action": "Read SearXNG JSON responses for both conflicting moments. Compute cross-engine concordance. Compute semantic similarity between contradictory findings.",
        "output": "Structured conflict report: which sources agree, which disagree, confidence per side"
      },
      {
        "name": "Pattern Builder",
        "role": "Structural interpretation",
        "action": "Cluster the contradictory findings. Determine: genuine mechanism complexity (multiple documented aspects) vs. research noise (one finding from low-quality source).",
        "output": "Conflict classification: GENUINE_COMPLEXITY | SOURCE_QUALITY_MISMATCH | TEMPORAL_SHIFT"
      },
      {
        "name": "Contrarian Agent",
        "role": "Adversarial attack on the stronger finding",
        "action": "Take the finding with higher concordance score. Search SearXNG for counter-evidence, retractions, legal challenges. Must reduce confidence score before Synthesizer can accept the finding.",
        "tool_access": "SKILL-RES-SEARCH with category matching the stronger finding's moment AND parameter cache_bypass_ttl=0",
        "mandatory_behavior": "MUST produce at least one counter-argument using LIVE search (bypassing any Tier 0 cache to break epistemological echo chambers). If no genuine counter-evidence found, must explicitly state why the finding is robust."
      },
      {
        "name": "Contextualizer",
        "role": "Historical pattern matching",
        "action": "Cross-reference both findings against Finding-Linked Source Cache (DEP-ENG-060). Has this trigger category produced similar conflicts before? How were they resolved?",
        "output": "Historical precedent report OR 'no_precedent_found'"
      },
      {
        "name": "Speculator",
        "role": "Second-order implication analysis",
        "action": "Ask: if both findings are simultaneously true, what does that imply? Sometimes the contradiction IS the insight — the mechanism operates differently at different scales or in different contexts.",
        "output": "Compound hypothesis: a single statement that reconciles both findings"
      },
      {
        "name": "Synthesizer",
        "role": "Final judge — Bayesian weighted combination",
        "action": "Receive all five agent outputs. Produce resolved finding with confidence score. The resolved finding must be usable by the Assembler in the content pipeline.",
        "output_schema": {
          "resolved_finding": "string — 240 words maximum, same contract as standard CRAL finding",
          "confidence_score": 0.85,
          "resolution_type": "GENUINE_COMPLEXITY | STRONGER_FINDING_CONFIRMED | COMPOUND_TRUTH",
          "rationale": "string — how the contradiction was resolved",
          "source_citations": ["url1", "url2"],
          "receipt_log": "Receipt Write: Per FR47 DEP-ENG-041 schema — { stage_name: 'Epistemic_Friction_Resolution', agent_name: 'Synthesizer' }"
        },
        "constraint": "Synthesizer CANNOT accept a finding until the Contrarian Agent has evaluated it"
      }
    ]
  }
}
```

### 4.3 Integration with Research Orchestrator

```yaml
# Research Orchestrator — Epistemic Friction integration

orchestrator_conflict_detection:
  trigger: "Orchestrator receives findings from M2 and M6 (or M3 and M5)"
  
  conflict_check:
    method: "Semantic similarity between mechanism descriptions in both findings"
    threshold: "If similarity < 0.4 AND both findings reference the same mechanism → CONFLICT"
  
  if_conflict_detected:
    action: "Activate Epistemic Friction Swarm"
    input: "Both conflicting findings + their raw SearXNG JSON responses"
    output: "Resolved finding from Synthesizer"
    routing: "Resolved finding replaces the weaker original finding in the Output Index"
  
  if_no_conflict:
    action: "Standard CRAL pipeline continues"
    note: "Swarm is never activated unnecessarily — only on detected contradictions"
```

---

## Section 5 — The 14-Parameter Viral Signal Engine

### 5.1 Dependency: Viral Signal Configuration (DEP-ENG-062)

```json
{
  "dependency_id": "DEP-ENG-062",
  "name": "Viral Signal Configuration",
  "version": "1.0",
  "description": "Configuration for the 14 viral signal parameters computed from SearXNG JSON responses. Used by the Autocomplete Polling Engine to detect and validate tribal trends.",
  "parameters": [
    {
      "id": 1,
      "name": "autocomplete_emergence_rank",
      "type": "integer",
      "description": "Position of the new term in aggregated autocomplete results (lower = more prominent)",
      "computed_from": "SearXNG autocomplete response ordering"
    },
    {
      "id": 2,
      "name": "zero_to_one_spike",
      "type": "boolean",
      "description": "True if query returned 0 results previously and 5+ results now",
      "computed_from": "Delta between current and previous autocomplete snapshots"
    },
    {
      "id": 3,
      "name": "cross_engine_concordance",
      "type": "float (0.0-1.0)",
      "description": "Proportion of active engines that return the topic in top-10 results. High concordance = established. Low concordance = emerging only in specific contexts.",
      "computed_from": "SearXNG JSON 'engine' field across all results"
    },
    {
      "id": 4,
      "name": "engine_divergence_score",
      "type": "float (0.0-1.0)",
      "description": "When engines disagree, one has indexed something others haven't — this is the alpha signal. High divergence = one engine found something novel.",
      "computed_from": "Variance in engine-specific result counts"
    },
    {
      "id": 5,
      "name": "temporal_velocity",
      "type": "float",
      "description": "Ratio of content indexed in last 24 hours vs. last 7 days. High ratio = rapid acceleration.",
      "computed_from": "SearXNG time_range=day vs time_range=week result counts"
    },
    {
      "id": 6,
      "name": "platform_dispersion_ratio",
      "type": "float (0.0-1.0)",
      "description": "Ratio of social (Reddit/Twitter) to institutional (Google News) results. High social, low institutional = early trend not yet mainstream.",
      "computed_from": "SearXNG 'engine' field categorization"
    },
    {
      "id": 7,
      "name": "result_freshness_clustering",
      "type": "float (hours)",
      "description": "Standard deviation of publication timestamps. Tight clustering (< 3 hours) = viral spike event.",
      "computed_from": "SearXNG 'publishedDate' field analysis"
    },
    {
      "id": 8,
      "name": "entity_co_occurrence",
      "type": "list[string]",
      "description": "Named entities appearing alongside the tribal seed phrase in search snippets.",
      "computed_from": "Basic NER on SearXNG 'content' fields"
    },
    {
      "id": 9,
      "name": "query_mutation_rate",
      "type": "integer",
      "description": "Count of autocomplete variants appearing for the seed phrase. High mutation = expanding discourse.",
      "computed_from": "SearXNG autocomplete response count"
    },
    {
      "id": 10,
      "name": "headline_pattern_clustering",
      "type": "float (0.0-1.0)",
      "description": "Similarity score across result titles. High similarity = media amplification phase (many outlets covering the same angle).",
      "computed_from": "TF-IDF cosine similarity across SearXNG 'title' fields"
    },
    {
      "id": 11,
      "name": "snippet_sentiment_shift",
      "type": "string (positive|negative|mixed)",
      "description": "Dominant sentiment polarity in result snippets. Detects outrage vs. hype.",
      "computed_from": "Basic sentiment analysis on SearXNG 'content' fields"
    },
    {
      "id": 12,
      "name": "content_volume_spike",
      "type": "integer",
      "description": "Raw number of indexed pages across all engines for this query.",
      "computed_from": "SearXNG 'number_of_results' field"
    },
    {
      "id": 13,
      "name": "niche_engine_triggering",
      "type": "boolean",
      "description": "True if the topic appears in specialized engines (Google Scholar, HackerNews). Indicates the topic has crossed from social chatter to substantive discourse.",
      "computed_from": "SearXNG 'engine' field check for scholarly/niche engines"
    },
    {
      "id": 14,
      "name": "geographic_localization_variance",
      "type": "float (0.0-1.0)",
      "description": "Difference in result volume when querying through proxies in different geographical regions. High variance = localized trend, not global.",
      "computed_from": "Multi-region SearXNG queries via proxy rotation — Phase 2 implementation"
    }
  ],
  "trend_validation_threshold": {
    "minimum_velocity_parameters": 3,
    "description": "A signal must cross configurable magnitude on 3+ velocity parameters simultaneously to be promoted to Validated Tribal Trend"
  }
}
```

---

## Section 6 — Implementation Roadmap

### Phase 1 — SearXNG Category Validation
- Deploy shared SearXNG infrastructure (from SVRE TechSpec Phase 1)
- Run 5 test directives per CRAL category against real trigger categories
- Verify exclusive engine routing: M7 returns zero Google Scholar results
- Verify M2 returns zero Reddit results
- Document any category weight adjustments needed

### Phase 2 — Research Planner + Executor Integration
- Update Research Planner to append `&categories={{moment_category}}` to directives
- Update all seven Moment Executors to use SKILL-RES-SEARCH instead of host LLM browsing
- Run 3 complete 7-moment CRAL sessions through the sovereign pipeline
- Compare finding quality against baseline (CRAL V1.0 with LLM browsing)
- Validate 240-word output contract is maintained

### Phase 3 — Autocomplete Polling Engine
- Deploy FastAPI service on SearXNG EC2 host
- Configure Redis DB 1 for autocomplete snapshot storage
- Generate initial DEP-ENG-061 seed phrases for all active coaches
- Run 48-hour burn-in test validating 15-minute polling cycle stability
- Connect `/api/tribe_signals/{coach_id}` to Telegram bot intake flow

### Phase 4 — Finding-Linked Source Cache
- Configure Redis DB 2 for finding cache storage
- Implement cache-aware execution flow in Moment Executors
- Run 10 sessions across 3 trigger categories to build initial convergence data
- Validate Tier 0 promotion when convergence_count reaches 3
- Verify cache hit reduces M2/M6 execution from ~45s to ~5-8s

### Phase 5 — Epistemic Friction Swarm
- Implement six swarm agents as LLM-based tool-calling agents
- Configure activation condition in Research Orchestrator conflict detection
- Test with 5 artificially constructed inter-moment contradictions
- Validate Synthesizer output conforms to 240-word finding contract
- Confirm Contrarian Agent mandatory evaluation prevents premature consensus

---

## Appendix A — Dependency Registry Updates

| Dependency ID | Name | Status |
|:---|:---|:---|
| DEP-ENG-060 | Finding-Linked Source Cache | NEW — Redis DB 2, Tier 0 promotion at convergence 3 |
| DEP-ENG-061 | Tribe Seed Phrases Registry | NEW — per-coach seed phrases for autocomplete polling |
| DEP-ENG-062 | Viral Signal Configuration | NEW — 14 parameters computed from SearXNG JSON |
| SKILL-RES-SEARCH | CRAL Moment Sovereign Search | NEW — replaces implicit host LLM browsing |

## Appendix B — Cross-References

| This Spec Component | References |
|:---|:---|
| SearXNG Docker deployment | SVRE TechSpec V1.0 Section 1.1 |
| `settings.yml` with CRAL categories | SVRE TechSpec V1.0 Section 1.2 |
| SearXNG JSON API contract | SVRE TechSpec V1.0 Section 1.3 |
| Redis infrastructure | SVRE TechSpec V1.0 Section 1.1 (shared redis container) |
| Proxy mesh | SVRE TechSpec V1.0 Section 1.1 (shared proxy-mesh container) |
| Seven JIT Moments definitions | CRAL Documentation V1.0 Section 04 |
| Research Planner compilation | CRAL Documentation V1.0 Section 05 |
| Dependency firing map | CRAL Documentation V1.0 Section 03 |
| Gen-Searcher multi-hop tools | Gen-Searcher Paper Section 3.3 |
| GRPO optimization | Gen-Searcher Paper Section 3.3, Equation 3 |
