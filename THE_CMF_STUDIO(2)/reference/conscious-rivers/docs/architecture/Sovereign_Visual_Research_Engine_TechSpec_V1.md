# Sovereign Visual Research Engine (SVRE) — Technical Specification V1.0

**Author:** CCP Engineering Division
**Date:** 2026-04-07
**Version:** 1.0
**Status:** Technical Specification — Build Ready
**Supersedes:** CVE Documentation V3.0 Sections 4.1–4.4 (Aurore + Image Research Skills)
**Feeds Into:** CVE V4.0 Integration, CMF Agentic Architecture PRD Update, AWS Infrastructure Provisioning
**Architecture Brief:** Sovereign Visual Research Engine Architecture Brief V1.0
**External References:**
- [SearXNG Repository](https://github.com/searxng/searxng) — Meta-search engine, self-hosted
- [Gen-Searcher Paper](https://gen-searcher.vercel.app/) — Reinforcing Agentic Search for Image Generation (Feng et al., MMLab CUHK)
- [SearXNG Documentation](https://docs.searxng.org/) — Configuration reference for `settings.yml`
- CVE Documentation V3.0 — Sections 2.4 (Four-Tier Hierarchy), 4.1–4.4 (Aurore + 9 Skills)
- MCDA: E-Roll vs Gen-Searcher — Quantity-First Hybrid Architecture recommendation

---

## Document Purpose

This specification defines the complete buildable architecture for the Sovereign Visual Research Engine — the upgrade to Aurore's image research pipeline that replaces Serper API dependencies with a self-hosted SearXNG meta-search node, adds Pinterest and five new sovereign source categories, introduces the Gen-Searcher RL multi-hop search agent for query decomposition, and implements the T-Score tribal reward function for autonomous image selection via NIM-hosted vision models.

Every section resolves to a buildable system component: a Docker container, a `settings.yml` configuration block, a composable SKILL definition, an API contract, a data schema, or a validation gate.

**What this spec changes from CVE V3.0:**
- SKILL-IMG-005 (Serper General Image Search) — eliminated, replaced by SearXNG sovereign categories
- SKILL-IMG-006 (Serper Known Persons Search) — eliminated, replaced by SearXNG `known_persons` category
- Aurore's skill routing table — rewritten for flood-all-score-best strategy
- Four new SKILL-IMG definitions added (Pinterest, Tribal Voice, Editorial News, Institutional Archive)
- New dependency: DEP-VIS-019 (Source Win-Rate Matrix)
- New dependency: DEP-VIS-020 (T-Score Configuration)
- New agent component: NIM Vision Scoring Pipeline

**What this spec does NOT change:**
- SKILL-IMG-001 (Unsplash) — retained, queried for every image search
- SKILL-IMG-002 (Pexels) — retained, queried for every image search
- SKILL-IMG-003 (Pixabay) — retained, queried for every image search
- SKILL-IMG-004 (GIPHY) — retained, exclusive for motion content
- SKILL-IMG-007 (RunningHub Realistic) — retained unchanged
- SKILL-IMG-008 (RunningHub Ghibli) — retained unchanged
- SKILL-IMG-009 (Photo Deck Query) — retained unchanged
- Abel's VCB schema — untouched
- The Four-Tier Image Sourcing Hierarchy — untouched
- Paradoxe's prompt compilation — untouched

---

## Section 1 — Infrastructure: SearXNG Deployment

### 1.1 Docker Container Specification

The SearXNG instance runs as a Docker container on the CCP AWS VPC. It is not public-facing. It accepts queries exclusively from agents running within the same VPC.

```yaml
# docker-compose.searxng.yml
version: "3.9"

services:
  searxng:
    image: searxng/searxng:latest
    container_name: ccp-searxng
    restart: unless-stopped
    ports:
      - "127.0.0.1:8080:8080"
    volumes:
      - ./searxng/settings.yml:/etc/searxng/settings.yml:ro
      - ./searxng/limiter.toml:/etc/searxng/limiter.toml:ro
    environment:
      - SEARXNG_BASE_URL=http://localhost:8080/
      - SEARXNG_SECRET=GENERATE_SECRET_HERE
    networks:
      - ccp-internal
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    container_name: ccp-searxng-redis
    restart: unless-stopped
    command: redis-server --save 60 1 --loglevel warning
    volumes:
      - redis-data:/data
    networks:
      - ccp-internal

  pinterest-scraper:
    build:
      context: ./pinterest-scraper
      dockerfile: Dockerfile
    container_name: ccp-pinterest-scraper
    restart: unless-stopped
    environment:
      - PROXY_POOL_URL=http://proxy-mesh:8888
      - MAX_CONCURRENT_SCRAPES=5
      - SCROLL_DEPTH=3
      - RESULT_LIMIT=30
    ports:
      - "127.0.0.1:8081:8081"
    networks:
      - ccp-internal
    depends_on:
      - proxy-mesh

  proxy-mesh:
    image: serjs/go-socks5-proxy:latest
    container_name: ccp-proxy-mesh
    restart: unless-stopped
    environment:
      - PROXY_LIST=/etc/proxies/residential.txt
    volumes:
      - ./proxies/residential.txt:/etc/proxies/residential.txt:ro
    ports:
      - "127.0.0.1:8888:1080"
    networks:
      - ccp-internal

volumes:
  redis-data:

networks:
  ccp-internal:
    driver: bridge
```

### 1.2 SearXNG `settings.yml` — Complete CCP Configuration

> [!NOTE]
> Boundary Dispute Resolution: This `settings.yml` block contains configuration for textual CRAL Research Engines. In production, this shared infrastructure logic will be extracted to an independent `SPEC-INFRA` blueprint. It remains here temporarily for documentation completeness.

```yaml
use_default_settings: true

general:
  instance_name: "CCP Sovereign Search"
  debug: false

server:
  bind_address: "0.0.0.0"
  port: 8080
  secret_key: "${SEARXNG_SECRET}"
  image_proxy: true
  limiter: false

search:
  safe_search: 0
  autocomplete: "google"
  default_lang: "en"
  formats:
    - json
  max_ban_time_on_fail: 120
  default_page_results: 50

redis:
  url: "redis://redis:6379/0"

outgoing:
  proxies:
    all://:
      - socks5://proxy-mesh:1080
  using_tor_proxy: false
  pool_maxsize: 100
  useragent_suffix: ""
  request_timeout: 4.0

# CCP Custom Categories — mapped to CRAL Moments and Visual Research Zones
categories_as_tabs:
  editorial_news:
    name: "Editorial News"
  tribal_voice_visual:
    name: "Tribal Voice Visual"
  institutional_archive:
    name: "Institutional Archive"
  documentary_photo:
    name: "Documentary Photo"
  known_persons:
    name: "Known Persons"
  cultural_now:
    name: "Cultural Now"
  precision_journalism:
    name: "Precision Journalism"
  behavioral_science:
    name: "Behavioral Science"
  narrative_journalism:
    name: "Narrative Journalism"
  anomaly_science:
    name: "Anomaly Science"
  institutional_prosecution:
    name: "Institutional Prosecution"
  tribal_vernacular:
    name: "Tribal Vernacular"

engines:
  # --- Image Research Engines ---
  - name: google images
    categories: editorial_news, documentary_photo, known_persons
    weight: 2.0
    disabled: false
    shortcut: gimg

  - name: bing images
    categories: editorial_news, known_persons
    weight: 2.5
    disabled: false
    shortcut: bimg

  - name: duckduckgo images
    categories: documentary_photo
    weight: 2.0
    disabled: false
    shortcut: ddgimg

  - name: flickr
    categories: documentary_photo
    weight: 3.0
    disabled: false
    shortcut: fl

  - name: wikimedia commons
    categories: editorial_news, institutional_archive, known_persons
    weight: 3.0
    disabled: false
    shortcut: wmc

  - name: reddit
    categories: tribal_voice_visual, cultural_now, tribal_vernacular
    weight: 3.5
    disabled: false
    shortcut: rd

  - name: imgur
    categories: tribal_voice_visual
    weight: 2.0
    disabled: false
    shortcut: img

  # --- CRAL Textual Research Engines ---
  - name: google
    categories: institutional_prosecution, narrative_journalism
    weight: 3.0
    disabled: false

  - name: bing
    categories: institutional_prosecution, precision_journalism
    weight: 2.5
    disabled: false

  - name: duckduckgo
    categories: institutional_prosecution
    weight: 2.5
    disabled: false

  - name: google scholar
    categories: precision_journalism, behavioral_science, anomaly_science
    weight: 3.0
    disabled: false
    shortcut: gs

  - name: pubmed
    categories: behavioral_science
    weight: 3.0
    disabled: false
    shortcut: pm

  - name: arxiv
    categories: anomaly_science
    weight: 2.5
    disabled: false
    shortcut: ax

  - name: wikipedia
    categories: precision_journalism
    weight: 2.5
    disabled: false
    shortcut: wp

  - name: google news
    categories: editorial_news, cultural_now, narrative_journalism
    weight: 2.5
    disabled: false
    shortcut: gn

  - name: bing news
    categories: editorial_news, narrative_journalism
    weight: 2.5
    disabled: false
    shortcut: bn

  - name: hackernews
    categories: cultural_now, anomaly_science
    weight: 2.0
    disabled: false
    shortcut: hn

  - name: pinterest
    categories: documentary_photo
    weight: 1.5
    disabled: false
    shortcut: pin

  - name: quora
    categories: tribal_vernacular
    weight: 2.0
    disabled: false
    shortcut: qr
```

### 1.3 SearXNG JSON API Contract

All agents query SearXNG via HTTP GET to the JSON endpoint:

```
GET http://ccp-searxng:8080/search?q={query}&format=json&categories={category}&time_range={range}
```

**Response Schema (relevant fields):**

```json
{
  "query": "string — the submitted query",
  "number_of_results": 50,
  "results": [
    {
      "url": "string — page URL",
      "title": "string — page title",
      "content": "string — snippet text",
      "engine": "string — which engine returned this result",
      "score": 1.0,
      "category": "string — matched category",
      "publishedDate": "string — ISO 8601 if available",
      "img_src": "string — proxied image URL (when image_proxy: true)",
      "thumbnail_src": "string — thumbnail URL",
      "source": "string — domain name"
    }
  ],
  "suggestions": ["string"],
  "infoboxes": []
}
```

**Autocomplete Endpoint:**

```
GET http://ccp-searxng:8080/autocomplete?q={partial_query}
```

Returns: `["suggestion_1", "suggestion_2", ...]`

---

## Section 2 — Pinterest Headless Scraper

### 2.1 Service Specification

The Pinterest Scraper is a dedicated FastAPI service running in a Docker container. It exposes a single JSON endpoint that the Gen-Searcher RL Agent calls when Pinterest is part of the source flood.

**Endpoint:**

```
POST http://ccp-pinterest-scraper:8081/search
Content-Type: application/json

{
  "query": "string — the image search query",
  "max_results": 30,
  "scroll_depth": 3
}
```

**Response Schema:**

```json
{
  "query": "string",
  "results": [
    {
      "pin_id": "string",
      "image_url": "string — highest resolution available",
      "thumbnail_url": "string",
      "title": "string — pin title/description",
      "source_url": "string — original source the pin links to",
      "board_name": "string — name of the board the pin was found in",
      "pinner": "string — username who pinned it",
      "dominant_colors": ["#hex1", "#hex2", "#hex3"]
    }
  ],
  "total_results": 30,
  "scrape_duration_ms": 2400
}
```

### 2.2 Scraper Implementation Architecture

```python
# pinterest_scraper/main.py — core architecture (pseudocode)

from fastapi import FastAPI
from playwright.async_api import async_playwright
import asyncio

app = FastAPI()

class PinterestScraper:
    """
    Headless Playwright scraper for Pinterest search results.
    
    Design Decisions:
    - Uses residential proxy rotation via the proxy-mesh container
    - Emulates realistic scroll behavior (random delays 800-2400ms)
    - Extracts high-res image URLs from Pinterest's React DOM
    - Rotates user agents across a pool of 50+ browser fingerprints
    
    Reference: Pinterest's DOM structure uses data-test-id attributes
    for pin containers. The scraper targets [data-test-id="pin"] elements.
    """
    
    async def search(self, query: str, max_results: int = 30, scroll_depth: int = 3):
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                proxy={"server": "socks5://proxy-mesh:1080"},
                headless=True
            )
            context = await browser.new_context(
                user_agent=self._random_user_agent(),
                viewport={"width": 1920, "height": 1080}
            )
            page = await context.new_page()
            
            url = f"https://www.pinterest.com/search/pins/?q={quote(query)}"
            await page.goto(url, wait_until="networkidle")
            
            pins = []
            for scroll in range(scroll_depth):
                await page.evaluate("window.scrollBy(0, window.innerHeight)")
                await asyncio.sleep(random.uniform(0.8, 2.4))
                
                new_pins = await page.query_selector_all('[data-test-id="pin"]')
                for pin in new_pins:
                    pin_data = await self._extract_pin_data(pin)
                    if pin_data and pin_data not in pins:
                        pins.append(pin_data)
                
                if len(pins) >= max_results:
                    break
            
            await browser.close()
            return pins[:max_results]
    
    async def _extract_pin_data(self, pin_element):
        """Extract image URL, title, source from a pin DOM element."""
        img = await pin_element.query_selector("img")
        if not img:
            return None
        
        src = await img.get_attribute("src")
        # Pinterest serves thumbnails by default; replace size token for high-res
        high_res_url = src.replace("/236x/", "/originals/") if src else None
        
        return {
            "image_url": high_res_url,
            "thumbnail_url": src,
            "title": await img.get_attribute("alt") or "",
            "source_url": await self._get_pin_source_link(pin_element),
            "dominant_colors": []  # computed post-download by NIM pipeline
        }
```

### 2.3 Licensing Strategy for Pinterest Images

Pinterest images are not directly licensed through Pinterest. Each pin links to a source URL. The licensing strategy operates in three tiers:

1. **Source URL traceable to CC-licensed platform** (Flickr CC, Wikimedia, personal blog with CC notice) → Direct use permitted with attribution
2. **Source URL traceable to commercial stock** (Shutterstock preview, Getty watermarked) → Image used as **composition reference only** — color palette, spatial density, and environmental grammar extracted for ComfyUI constrained synthesis
3. **Source URL untraceable or dead** → Image used as composition reference only

The NIM Vision Pipeline's Stage 3 (Source Attribution) automated this classification by following the `source_url` and checking for CC metadata.

---

## Section 3 — The Upgraded Aurore: Flood-All-Score-Best

### 3.1 Agent Specification (Upgraded)

**Agent Name:** Aurore (V2.0)
**Previous Role:** Image Research Planner (CVE V3.0)
**New Role:** Sovereign Image Research Orchestrator
**Department:** Perception Department
**Reads From:** DEP-VIS-005 (VCB), DEP-VIS-006 (Known Persons Registry), DEP-VIS-019 (Source Win-Rate Matrix), DEP-VIS-020 (T-Score Configuration)
**Writes To:** `image_resolution_map` (upgraded schema — see Section 3.4)
**Infrastructure:** SearXNG (port 8080), Pinterest Scraper (port 8081), Unsplash API, Pexels API, Pixabay API, GIPHY API, NIM Vision Pipeline

### 3.2 Flood-All Query Execution

For every slide where `image_type` is `environment_scene`, Aurore fires the VCB-derived query to **all retrieval sources simultaneously:**

```yaml
# Aurore V2.0 — Flood-All execution per slide
flood_all_execution:
  parallel_api_queries:
    - skill: "SKILL-IMG-001"  # Unsplash
      query_source: "vcb.image_search_query"
      results_per_query: 10
    - skill: "SKILL-IMG-002"  # Pexels
      query_source: "vcb.image_search_query"
      results_per_query: 10
    - skill: "SKILL-IMG-003"  # Pixabay
      query_source: "vcb.image_search_query"
      results_per_query: 10
    - skill: "SKILL-IMG-S01"  # SearXNG Editorial News
      endpoint: "http://ccp-searxng:8080/search"
      params:
        q: "{{vcb.image_search_query}}"
        format: json
        categories: editorial_news
      results_per_query: 15
    - skill: "SKILL-IMG-S02"  # SearXNG Tribal Voice
      endpoint: "http://ccp-searxng:8080/search"
      params:
        q: "{{vcb.image_search_query}}"
        format: json
        categories: tribal_voice_visual
      results_per_query: 15
    - skill: "SKILL-IMG-S03"  # SearXNG Documentary Photo
      endpoint: "http://ccp-searxng:8080/search"
      params:
        q: "{{vcb.image_search_query}}"
        format: json
        categories: documentary_photo
      results_per_query: 15
    - skill: "SKILL-IMG-S04"  # SearXNG Institutional Archive
      endpoint: "http://ccp-searxng:8080/search"
      params:
        q: "{{vcb.image_search_query}}"
        format: json
        categories: institutional_archive
      results_per_query: 10
    - skill: "SKILL-IMG-P01"  # Pinterest Headless Scraper
      endpoint: "http://ccp-pinterest-scraper:8081/search"
      params:
        query: "{{vcb.tribal_noun_visual_congruent.visual_congruent}}"
        max_results: 20
      results_per_query: 20

  total_expected_candidates: 80-120
  
  hard_routed_exceptions:
    character_brand_avatar: "SKILL-IMG-007 direct"
    character_specific_emotion: "SKILL-IMG-007 direct"
    conceptual_contrast_illustration: "SKILL-IMG-008 direct"
    supervisual_abstract: "SKILL-IMG-008 direct"
    named_person_coach: "SKILL-IMG-009 direct"
    motion_content: "SKILL-IMG-004 exclusive"
  
  named_person_public_figure:
    searxng_category: "known_persons"
    also_floods: ["SKILL-IMG-001", "SKILL-IMG-002", "SKILL-IMG-003"]
    note: "All curated APIs also queried — winner in any source is valid"
```

### 3.3 Gen-Searcher RL Multi-Hop Fallback

When the flood-all query returns fewer than 10 viable candidates after NIM Vision Pipeline Stage 1 sieve, the Gen-Searcher RL multi-hop agent activates. This agent uses learned search strategies from the Gen-Searcher paper to decompose the query and search deeper.

**Implementation Strategy — Phase 1 (Prompt-Based):**

The Gen-Searcher RL agent's multi-hop capability is initially replicated through prompt-based behavioral alignment, not full RL fine-tuning. A Qwen3-VL or equivalent multimodal model receives a structured system prompt that encodes the three Gen-Searcher tools:

```json
{
  "gen_searcher_fallback": {
    "activation_condition": "viable_candidates < 10 after Stage 1 sieve",
    "model": "qwen3-vl-8b (NIM container)",
    "tools": [
      {
        "name": "search",
        "description": "Web text search via SearXNG. Returns top-k URLs with snippets.",
        "endpoint": "http://ccp-searxng:8080/search?q={query}&format=json"
      },
      {
        "name": "image_search",
        "description": "Web image search via SearXNG. Returns image URLs with thumbnails.",
        "endpoint": "http://ccp-searxng:8080/search?q={query}&format=json&categories={dynamic_inherit_from_failed_request}"
      },
      {
        "name": "browse",
        "description": "Read and summarize a webpage to extract deeper evidence.",
        "implementation": "requests.get(url) → html_to_markdown → summarize with qwen3-vl"
      }
    ],
    "max_hops": 5,
    "max_turns": 10,
    "termination": "viable_candidates >= 10 OR max_hops reached",
    "phase_2_note": "Full RL fine-tuning against T-Score rewards when GPU capacity available (Gen-Searcher trains on 8x H800 for SFT + 16x H800 for RL rollouts)"
  }
}
```

**Reference:** Gen-Searcher paper Section 3.3 — Training Scheme. The SFT stage teaches multi-turn tool use (search → browse → image_search → reason → repeat). The RL stage (GRPO with dual reward) optimizes tool-calling trajectories. Phase 1 of our implementation uses prompt engineering to replicate SFT-level behavior without requiring the full training pipeline.

### 3.4 Image Resolution Map V2.0 (Upgraded Schema)

Aurore's output now includes the T-Score, source origin, and ranked alternatives per slide:

```json
{
  "vcb_id": "VCB-20260317-0042",
  "resolution_map": [
    {
      "slide_number": 1,
      "image_type": "environment_scene",
      "resolution_tier": 2,
      "resolution_source": "SKILL-IMG-S02",
      "source_platform": "reddit",
      "resolved_image_url": "http://ccp-searxng:8080/image_proxy?url=...",
      "t_score": {
        "overall": 0.82,
        "emotional_mode_match": 0.90,
        "tribal_authenticity": 0.85,
        "pssl_alignment": 0.78,
        "anti_ai_score": 0.95,
        "compositional_usability": 0.62
      },
      "attribution": "u/startup_burnout on r/antiwork — CC unspecified",
      "licensing_status": "composition_reference_only",
      "licensing_routing_action": "Reroute direct placement to SKILL-IMG-008 (ComfyUI Image-to-Image / ControlNet) to generate safe final asset mapping to this tribal structure.",
      "runninghub_required": true,
      "alternatives": [
        {
          "rank": 2,
          "source_platform": "unsplash",
          "resolved_image_url": "https://images.unsplash.com/photo-xyz.jpg",
          "t_score_overall": 0.79,
          "attribution": "Photo by Jane Doe on Unsplash"
        },
        {
          "rank": 3,
          "source_platform": "pinterest",
          "resolved_image_url": "http://ccp-pinterest-scraper:8081/cached/pin-abc.jpg",
          "t_score_overall": 0.76,
          "attribution": "Pin by @morning_ritual_aesthetic — source: flickr CC-BY"
        }
      ]
    }
  ]
}
```

---

## Section 4 — The T-Score: Tribal Reward Function

### 4.1 Why K-Score Is Wrong for the CCP

Gen-Searcher's K-Score (from the KnowGen benchmark) weights Visual Correctness at 0.4 and Text Accuracy at 0.4, with Faithfulness and Aesthetics at 0.1 each. This reward function optimizes for factual grounding — "does the image of the Nobel Prize podium match the real podium?" The CCP does not need factual accuracy. It needs emotional precision.

**Reference:** Gen-Searcher paper Section 3.2 — K-Score formula: `K = 0.1 × Faithfulness + 0.4 × Visual_Correctness + 0.4 × Text_Accuracy + 0.1 × Aesthetics`

### 4.2 T-Score Definition

```
T-Score = 0.30 × Emotional_Mode_Match
        + 0.25 × Tribal_Authenticity
        + 0.20 × PSSL_Parameter_Alignment
        + 0.15 × Anti_AI_Artifact_Score
        + 0.10 × Compositional_Usability
```

### 4.3 T-Score Dimension Specifications

**DEP-VIS-020 — T-Score Configuration:**

```json
{
  "dependency_id": "DEP-VIS-020",
  "name": "T-Score Configuration",
  "version": "1.0",
  "dimensions": [
    {
      "name": "emotional_mode_match",
      "weight": 0.30,
      "scoring_scale": [0.0, 0.5, 1.0],
      "vlm_prompt_instruction": "Evaluate the dominant emotional register of this image. The VCB specifies arc_stage='{{arc_stage}}'. Score 1.0 if the image clearly evokes {{arc_stage}} (tension = constriction/unease, vulnerability = exposure/softness, recognition = warmth/familiarity). Score 0.5 if the emotional register is ambiguous but compatible. Score 0.0 if the image evokes a contradictory emotion.",
      "inputs": ["vcb.slide.arc_stage", "vcb.slide.somatic_target"]
    },
    {
      "name": "tribal_authenticity",
      "weight": 0.25,
      "scoring_scale": [0.0, 0.5, 1.0],
      "vlm_prompt_instruction": "Evaluate whether this image feels like it belongs to the specific tribal reality described. The tribal noun is '{{tribal_noun}}' and the visual congruent is '{{visual_congruent}}'. Score 1.0 if the image contains environment-specific, culturally-grounded elements that match this tribe's world. Score 0.5 if the image is generic but not contradictory. Score 0.0 if the image is clearly staged, corporate, or culturally misaligned.",
      "inputs": ["vcb.slide.tribal_noun_visual_congruent"]
    },
    {
      "name": "pssl_alignment",
      "weight": 0.20,
      "scoring_scale": [0.0, 0.5, 1.0],
      "vlm_prompt_instruction": "Evaluate the image against these PSSL parameters — Color temperature: {{world_color_temp_kelvin}}K, Spatial density: {{spatial_density}}/10, Temporal signal: {{temporal_signal}}, PAD scores: P={{pleasure}} A={{arousal}} D={{dominance}}. Score 1.0 if the image aligns within acceptable range on 3+ parameters. Score 0.5 if 2 parameters align. Score 0.0 if fewer than 2 align.",
      "inputs": ["vcb.slide.environmental_grammar", "vcb.slide.chromatic_spec"]
    },
    {
      "name": "anti_ai_artifact",
      "weight": 0.15,
      "scoring_scale": [0.0, 0.5, 1.0],
      "vlm_prompt_instruction": "Scan this image for signs of AI generation: unnaturally smooth skin, perfect bilateral symmetry, impossible geometry, cinematic rim lighting without a visible source, plastic-looking textures, repeated patterns, text artifacts, extra fingers or limbs. Score 1.0 if the image appears to be an unedited real photograph. Score 0.5 if minor AI-like artifacts are present but not obvious. Score 0.0 if the image is clearly AI-generated.",
      "inputs": []
    },
    {
      "name": "compositional_usability",
      "weight": 0.10,
      "scoring_scale": [0.0, 0.5, 1.0],
      "vlm_prompt_instruction": "Evaluate whether this image can be directly placed into a {{aspect_ratio}} canvas with typography overlay. Score 1.0 if the subject is positioned with adequate negative space for text, the image is at least 1080px on the shortest edge, and the subject does not collide with typical text placement zones. Score 0.5 if minor cropping or repositioning is needed. Score 0.0 if the image requires significant manipulation.",
      "inputs": ["vcb.aspect_ratio", "vcb.slide.typography"]
    }
  ],
  "passing_threshold": 0.65,
  "top_selection_count": 3,
  "alternatives_count": 5
}
```

---

## Section 5 — NIM Vision Scoring Pipeline

### 5.1 Pipeline Architecture

All images from all sources converge into a two-stage NIM Vision Pipeline:

```
Stage 1: Gemma 4 Sieve (High Throughput)
  Input:  80-120 raw candidates per slide
  Output: 15 viable candidates
  Model:  Gemma 4 (or equivalent high-throughput VLM on NIM)
  Latency: ~500ms per batch of 50

Stage 2: Heavy VLM Deep Ranker (T-Score)
  Input:  15 viable candidates
  Output: Top 3 + 5 alternatives with full T-Score
  Model:  Qwen2-VL-72B (or equivalent heavy VLM on NIM)
  Latency: ~2s per batch of 15
```

### 5.2 Stage 1 — Gemma 4 Sieve Specification

The sieve performs five binary elimination checks:

```yaml
sieve_checks:
  - name: "resolution_check"
    rule: "image width >= 1080px AND height >= 1080px (WAIVED IF category == 'tribal_voice_visual' or source == 'reddit' or source == 'imgur')"
    method: "metadata_read — no VLM needed"
    
  - name: "watermark_detection"
    rule: "no visible stock watermark text"
    method: "VLM binary classification"
    prompt: "Does this image contain a visible watermark or stock photo overlay text? Answer YES or NO."
    
  - name: "ai_artifact_rapid"
    rule: "no obvious AI generation markers"
    method: "VLM binary classification"
    prompt: "Is this image obviously AI-generated (smooth plastic skin, impossible geometry, repeated patterns, extra fingers)? Answer YES or NO."
    
  - name: "relevance_check"
    rule: "image is topically related to the search query"
    method: "VLM binary classification"
    prompt: "The search was for '{{query}}'. Is this image topically related? Answer YES or NO."
    
  - name: "content_safety"
    rule: "no explicit, violent, or disturbing content"
    method: "VLM binary classification"
    prompt: "Does this image contain explicit, violent, or disturbing content? Answer YES or NO."

elimination_logic: "ANY check returns positive elimination → image removed from pool"
```

### 5.3 Stage 2 — Heavy VLM Deep Ranker Specification

The deep ranker computes full T-Score for each surviving candidate:

```yaml
deep_ranker:
  model: "qwen2-vl-72b (NIM container — high VRAM queue)"
  
  per_candidate_evaluation:
    system_prompt: |
      You are the CCP Visual Evaluation Agent. You score images for use in 
      coaching content carousels. You evaluate each image across five dimensions.
      Return a JSON object with scores for each dimension (0.0, 0.5, or 1.0).
    
    user_prompt_template: |
      Evaluate this image for the following visual composition slot:
      
      Arc Stage: {{arc_stage}}
      Tribal Noun: {{tribal_noun}}
      Visual Congruent: {{visual_congruent}}
      Color Temperature Target: {{world_color_temp_kelvin}}K
      Spatial Density Target: {{spatial_density}}/10
      Temporal Signal: {{temporal_signal}}
      PAD Scores: P={{pleasure}} A={{arousal}} D={{dominance}}
      Aspect Ratio: {{aspect_ratio}}
      
      Score each dimension (0.0, 0.5, or 1.0):
      1. emotional_mode_match — Does the image evoke {{arc_stage}}?
      2. tribal_authenticity — Does it feel specific to this tribe's world?
      3. pssl_alignment — Do lighting, color, density match the targets?
      4. anti_ai_artifact — Does it look like a real photograph?
      5. compositional_usability — Can it be placed in a {{aspect_ratio}} canvas?
      
      Return JSON: {"emotional_mode_match": X, "tribal_authenticity": X, 
                     "pssl_alignment": X, "anti_ai_artifact": X, 
                     "compositional_usability": X}
    
    output_processing: "compute weighted T-Score from 5 dimension scores. EXCEPTION: If asset originated from generative source (e.g. SKILL-IMG-007), skip anti_ai_artifact constraint proportionally."
    
  ranking_logic:
    - "Sort all candidates by T-Score descending"
    - "Select top 3 as primary selections"
    - "Select next 5 as ranked alternatives"
    - "Record source_platform for each selection"
    - "Log to DEP-VIS-019 Source Win-Rate Matrix"
    - "Receipt Write: Per FR47 DEP-ENG-041 schema — { stage_name: 'Visual_Candidate_Ranking', agent_name: 'Deep_Ranker' }"
```

---

## Section 6 — New Composable Image Search Skills

### 6.1 SKILL-IMG-S01: SearXNG Editorial News Image Search

```yaml
skill_id: "SKILL-IMG-S01"
skill_name: "searxng_editorial_news_image"
skill_family: "image_research"
composable: true
replaces: "Partial function of SKILL-IMG-005 (Serper general)"

api_endpoint: "http://ccp-searxng:8080/search"
infrastructure: "Self-hosted SearXNG Docker container"

block_a_invariants:
  - "Query derives from VCB image_search_query field"
  - "Category locked to editorial_news — routes to Google News, Bing News, Wikimedia Commons"
  - "Results are real editorial photographs — not stock, not AI"
  - "SearXNG image_proxy must be enabled — images downloaded through proxy to avoid tracking"
  - "Results scored against PSSL parameters via NIM Vision Pipeline"

block_b_runtime_injections:
  q: "{{vcb.image_search_query}} real photo documentary"
  format: "json"
  categories: "editorial_news"
  time_range: "{{derived_from_content_recency_requirement}}"
  pageno: 1

scoring_against_pssl:
  - "Documentary authenticity — visible environmental grain, non-staged composition"
  - "Color temperature match"
  - "Temporal signal presence"
  - "PAD rough match"

block_c_validation:
  - "Results must contain img_src field (image proxy URL)"
  - "Results without img_src are text-only results — excluded from image pool"
  - "Minimum 1 result must have viable image after Stage 1 sieve"

output:
  format: "ranked_image_candidates_list"
  fields: ["img_src", "url", "title", "engine", "score", "publishedDate", "source"]
```

### 6.2 SKILL-IMG-S02: SearXNG Tribal Voice Visual Search

```yaml
skill_id: "SKILL-IMG-S02"
skill_name: "searxng_tribal_voice_visual"
skill_family: "image_research"
composable: true
new_source: true

api_endpoint: "http://ccp-searxng:8080/search"
infrastructure: "Self-hosted SearXNG Docker container"

block_a_invariants:
  - "Query derives from VCB tribal_noun_visual_congruent — uses tribal language, not formal search syntax"
  - "Category locked to tribal_voice_visual — routes exclusively to Reddit, Imgur, forums"
  - "Images from these sources are user-submitted, unposed, raw — maximum tribal authenticity"
  - "Licensing is typically unclear — flag all results as composition_reference_only unless CC metadata found"

block_b_runtime_injections:
  q: "{{vcb.tribal_noun_visual_congruent.visual_congruent}}"
  format: "json"
  categories: "tribal_voice_visual"

block_c_validation:
  - "Results with img_src extracted from Reddit/Imgur posts"
  - "Sub-1080px images accepted as composition references (not direct use)"
  - "Emotional register alignment checked against arc_stage"

output:
  format: "ranked_image_candidates_list"
  fields: ["img_src", "url", "title", "engine", "source", "licensing_status"]
```

### 6.3 SKILL-IMG-S03: SearXNG Documentary Photo Search

```yaml
skill_id: "SKILL-IMG-S03"
skill_name: "searxng_documentary_photo"
skill_family: "image_research"
composable: true

api_endpoint: "http://ccp-searxng:8080/search"

block_a_invariants:
  - "Category locked to documentary_photo — routes to Flickr CC, Google Images, DuckDuckGo Images, Pinterest"
  - "Prioritizes CC-licensed content (Flickr weight: 3.0)"
  - "This is the broadest image search category — catches what curated APIs miss"

block_b_runtime_injections:
  q: "{{vcb.image_search_query}}"
  format: "json"
  categories: "documentary_photo"

block_c_validation:
  - "Flickr results: check for CC license metadata in result fields"
  - "Google/Bing image results: licensing status set to requires_verification"

output:
  format: "ranked_image_candidates_list"
  fields: ["img_src", "url", "title", "engine", "score", "source"]
```

### 6.4 SKILL-IMG-S04: SearXNG Institutional Archive Search

```yaml
skill_id: "SKILL-IMG-S04"
skill_name: "searxng_institutional_archive"
skill_family: "image_research"
composable: true

api_endpoint: "http://ccp-searxng:8080/search"

block_a_invariants:
  - "Category locked to institutional_archive — routes to Wikimedia Commons and Google"
  - "Wikimedia Commons weight: 3.5 — highest of any engine"
  - "All Wikimedia results are CC or public domain — zero licensing risk"
  - "Use for juxtaposition elements, symbolic artifacts, and institutional credibility imagery"

block_b_runtime_injections:
  q: "{{vcb.image_search_query}} site:commons.wikimedia.org OR official photo"
  format: "json"
  categories: "institutional_archive"

block_c_validation:
  - "Wikimedia results: licensing confirmed automatically (CC metadata in Wikimedia API)"
  - "Google results: licensing status set to requires_verification"

output:
  format: "ranked_image_candidates_list"
  fields: ["img_src", "url", "title", "engine", "score", "source", "license"]
```

### 6.5 SKILL-IMG-P01: Pinterest Headless Scraper Search

```yaml
skill_id: "SKILL-IMG-P01"
skill_name: "pinterest_headless_search"
skill_family: "image_research"
composable: true
new_source: true

api_endpoint: "http://ccp-pinterest-scraper:8081/search"
infrastructure: "Dedicated Playwright Docker container with residential proxy rotation"

block_a_invariants:
  - "Query derives from VCB tribal_noun_visual_congruent — Pinterest searches work best with aesthetic/lifestyle language"
  - "Results are curated by human emotional intelligence — the pin survived a human authenticity filter"
  - "All results initially flagged composition_reference_only until source_url licensing verified"
  - "Source URL tracing required: if source is Flickr CC → upgrade to direct_use"

block_b_runtime_injections:
  query: "{{vcb.tribal_noun_visual_congruent.visual_congruent}} aesthetic"
  max_results: 20
  scroll_depth: 3

block_c_validation:
  - "Minimum 5 results returned (Pinterest search rarely fails for coaching-adjacent queries)"
  - "Source URL traced for each pin — licensing classified"
  - "Images scored against PSSL parameters via NIM Vision Pipeline"

output:
  format: "ranked_image_candidates_list"
  fields: ["image_url", "thumbnail_url", "title", "source_url", "board_name", "licensing_status", "dominant_colors"]
```

### 6.6 SKILL-IMG-S05: SearXNG Known Persons Search

```yaml
skill_id: "SKILL-IMG-S05"
skill_name: "searxng_known_persons"
skill_family: "image_research"
composable: true
replaces: "SKILL-IMG-006 (Serper Known Persons)"

api_endpoint: "http://ccp-searxng:8080/search"
prerequisite: "Person must exist in DEP-VIS-006 Known Persons Registry"

block_a_invariants:
  - "Only invoked when image_type = named_person_public_figure"
  - "Person must be in DEP-VIS-006 before this skill fires"
  - "Category locked to known_persons — Google Images (3.0), Bing Images (3.0), Wikimedia (2.0)"
  - "Multi-engine concordance provides higher confidence than single-engine Serper"

block_b_runtime_injections:
  person_name: "{{dep_vis_006.person.full_name}}"
  context: "{{script_reference_context}}"
  q: "{{person_name}} {{context}} photo"
  format: "json"
  categories: "known_persons"

block_c_validation:
  - "Person correctly identified in returned images (VLM face-context check)"
  - "Multi-engine concordance: same person appearing in 2+ engine results increases confidence"
  - "If person not identifiable: escalate to RunningHub Tier 3"

output:
  format: "ranked_person_image_candidates"
  fields: ["img_src", "url", "title", "engine", "source", "person_confirmed", "concordance_score"]
```

---

## Section 7 — Source Win-Rate Matrix (DEP-VIS-019)

### 7.1 Dependency Specification

```json
{
  "dependency_id": "DEP-VIS-019",
  "name": "Source Win-Rate Matrix",
  "version": "1.0",
  "description": "Tracks which image sources produce winning images per image_type. Updated after each project. Drives adaptive weight allocation.",
  "schema": {
    "matrix": {
      "{{image_type}}": {
        "{{source_platform}}": {
          "total_selections": 0,
          "total_wins": 0,
          "win_rate": 0.0,
          "current_weight": 1.0,
          "last_updated": "ISO 8601 timestamp"
        }
      }
    }
  },
  "weight_update_formula": "new_weight = (1 - 0.2) × current_weight + 0.2 × recent_win_rate",
  "update_frequency": "After every 10 completed projects",
  "minimum_weight": 0.1,
  "maximum_weight": 3.0,
  "note": "No source is ever fully excluded. Even at minimum weight (0.1), the source still participates with reduced candidate count."
}
```

### 7.2 Weight Application to Candidate Count

```yaml
weight_to_candidate_count:
  weight_3.0: "request 15 results per query"
  weight_2.0: "request 10 results per query"
  weight_1.0: "request 10 results per query (default)"
  weight_0.5: "request 5 results per query"
  weight_0.1: "request 3 results per query"
```

---

## Section 8 — Aurore V2.0 Skill Routing Table (Updated)

```yaml
# Aurore V2.0 — Skill Routing Table
# REPLACES: CVE V3.0 Section 4.3 skill routing table

image_type_to_skills:
  environment_scene:
    flood_all:
      - "SKILL-IMG-001"  # Unsplash
      - "SKILL-IMG-002"  # Pexels
      - "SKILL-IMG-003"  # Pixabay
      - "SKILL-IMG-S01"  # SearXNG Editorial News
      - "SKILL-IMG-S02"  # SearXNG Tribal Voice
      - "SKILL-IMG-S03"  # SearXNG Documentary Photo
      - "SKILL-IMG-S04"  # SearXNG Institutional Archive
      - "SKILL-IMG-P01"  # Pinterest
    execution: "parallel_flood_all"
    scoring: "nim_vision_pipeline_t_score"
    fallback: "gen_searcher_multi_hop → SKILL-IMG-007"

  motion_content:
    primary: ["SKILL-IMG-004"]  # GIPHY exclusive
    fallback: ["SKILL-IMG-001", "SKILL-IMG-002"]
    execution: "sequential"

  named_person_coach:
    primary: ["SKILL-IMG-009"]  # Photo Deck
    fallback: "photo_session_recommendation"
    execution: "direct"

  named_person_public_figure:
    flood_all:
      - "SKILL-IMG-S05"  # SearXNG Known Persons
      - "SKILL-IMG-001"  # Unsplash
      - "SKILL-IMG-002"  # Pexels
      - "SKILL-IMG-003"  # Pixabay
      - "SKILL-IMG-S04"  # SearXNG Institutional (Wikimedia)
    prerequisite: "DEP-VIS-006 registry check"
    execution: "parallel_flood_all"
    scoring: "nim_vision_pipeline_t_score"
    fallback: "SKILL-IMG-007"

  character_specific_emotion:
    primary: ["SKILL-IMG-007"]  # RunningHub Realistic
    no_retrieval_search: true
    execution: "direct"

  character_brand_avatar:
    primary: ["SKILL-IMG-007"]  # RunningHub Realistic + DEP-VIS-004
    no_retrieval_search: true
    execution: "direct"

  conceptual_contrast_illustration:
    primary: ["SKILL-IMG-008"]  # RunningHub Ghibli
    no_retrieval_search: true
    execution: "direct"

  supervisual_abstract:
    primary: ["SKILL-IMG-008"]  # RunningHub Ghibli
    no_retrieval_search: true
    execution: "direct"
```

---

## Section 9 — Implementation Roadmap

### Phase 1 — Infrastructure Deployment
- Provision AWS EC2 instance (t3.medium minimum) within CCP VPC
- Deploy `docker-compose.searxng.yml` with SearXNG + Redis + Pinterest Scraper + Proxy Mesh
- Configure `settings.yml` with all 12 custom categories and engine weights
- Validate SearXNG JSON endpoint returns correctly for test queries across all categories
- Set up residential proxy rotation (BrightData or equivalent)

### Phase 2 — Skill Development
- Implement SKILL-IMG-S01 through S05 and P01 as JIT-compiled SKILL.md files
- Update Aurore V2.0 agent with flood-all execution logic
- Build the NIM Vision Pipeline (Stage 1 Gemma 4 sieve + Stage 2 Heavy VLM ranker)
- Encode T-Score evaluation prompts in DEP-VIS-020
- Initialize DEP-VIS-019 Source Win-Rate Matrix with uniform weights

### Phase 3 — Integration Testing
- Run 5 complete carousel projects through the full pipeline
- Validate flood-all returns 80-120 candidates per slide
- Verify T-Score rankings correlate with human operator preference (minimum r=0.7)
- Calibrate T-Score dimension weights based on operator feedback
- Stress-test Pinterest scraper under production query volume

### Phase 4 — Gen-Searcher Multi-Hop Activation
- Deploy Qwen3-VL-8B on NIM container for prompt-based multi-hop agent
- Configure tool bindings to SearXNG endpoints
- Test multi-hop decomposition on 20 queries that failed single-shot retrieval
- Measure improvement in viable candidate count after multi-hop

### Phase 5 — Adaptive Weight System
- After 10 completed projects: run first weight update cycle
- Validate weight changes are directionally correct (high-performing sources gain weight)
- Monitor for edge cases: a source that wins rarely but wins big (don't over-penalize)

---

## Appendix A — Dependency Registry Updates

| Dependency ID | Name | Status |
|:---|:---|:---|
| DEP-VIS-019 | Source Win-Rate Matrix | NEW — initialized with uniform weights |
| DEP-VIS-020 | T-Score Configuration | NEW — five-dimension tribal reward function |
| SKILL-IMG-005 | Serper General Image Search | DEPRECATED — replaced by SKILL-IMG-S01/S02/S03/S04 |
| SKILL-IMG-006 | Serper Known Persons Search | DEPRECATED — replaced by SKILL-IMG-S05 |
| SKILL-IMG-S01 | SearXNG Editorial News Image Search | NEW |
| SKILL-IMG-S02 | SearXNG Tribal Voice Visual Search | NEW |
| SKILL-IMG-S03 | SearXNG Documentary Photo Search | NEW |
| SKILL-IMG-S04 | SearXNG Institutional Archive Search | NEW |
| SKILL-IMG-S05 | SearXNG Known Persons Search | NEW |
| SKILL-IMG-P01 | Pinterest Headless Scraper Search | NEW |
