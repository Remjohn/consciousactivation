# **🔶🎬 Conscious Movie Factory (CMF) \- Master Manual 🎬🔶**

## **1\. System Overview**

### **1.1 The Mission: The Sonic-First Generative Engine**

Welcome to the **Conscious Movie Factory (CMF)**.

To understand the CMF, one must first understand its lineage. It is the direct evolutionary descendant of the Conscious Content Factory (CCF). If the CCF is the "Brain" of our operation—architecting ideas, worldviews, and strategic narratives—the CMF is its "Heart." It is the kinetic engine designed to translate static intellectual property into visceral emotional experience.

The CMF is not merely a video production workflow; it is a **Sonic-First Generative Engine** designed to industrialize the creation of emotional resonance. It represents a fundamental paradigm shift in how we conceive of, construct, and deploy short-form video content in the digital age.

For decades, video production has operated on a "Visual-First" hierarchy: shoot footage, write a script, edit the visuals, and then layer music underneath as a background element or an afterthought. The CMF fundamentally inverts this hierarchy. We operate on the conviction that in the hyper-accelerated economy of short-form attention (40–60 seconds), **audio is the primary driver of emotion, and visuals are the validation of that emotion.**

The mission of the CMF is to transition from a manual, labor-intensive "editing" process to an **AI-Architected Construction Process**. We do not "edit" videos in the traditional sense; we **build** experiences. We utilize a sophisticated stack of autonomous agents, generative AI models (Z-Image Turbo for image generation, Wan 2.2 for video interpolation, and Wan 2.1 One-to-All for performance-driven animation), and forensic asset procurement systems to transmute a raw transcript into a cinematic artifact that feels less like a marketing video and more like a memory the viewer didn’t know they had.

This system moves beyond the "hybrid" model of human-AI collaboration into a new era of **Generative Direction**. The majority of our bespoke visual assets—from the character models (Brand Avatars) to the multi-shot cinematic scenes and abstract metaphors—are now generated on-demand, tailored to the exact emotional frequency of the script. We are no longer limited by stock footage libraries or the constraints of physical filming. If the script demands a "hyper-realistic close-up of a hand snapping a pencil in frustration," we generate it. If it requires a "surreal, dreamlike vision of a golden future," we architect it.

The CMF exists to solve the "Gap of Authenticity" inherent in current AI content generation. While most AI video feels sterile, random, or uncanny ("hallucinated visuals"), the CMF uses a strict **Script-to-Reality** translation protocol. We anchor every generative choice in deep human psychology—specifically the **Viral Trinity of Surprise, Emotion, and Specificity**. By rigorously enforcing continuity, character consistency, and "Sonic-First" pacing, we create content that bypasses the viewer's skepticism and speaks directly to their subconscious.

---

### **1.1a Official CMF 2.0 Tech Stack**

> **⚠️ This is the canonical technology specification for CMF 2.0.**

| Function | Tool | Platform | Reference |
|----------|------|----------|-----------|
| **Image Genesis (Generic)** | Z-Image Turbo (S3-DiT) | Running Hub (RTX 4090) | `Z_Image_Turbo_Hero.json` |
| **Image Genesis (Coach)** | SDXL/Flux + **Coach Identity LoRA** | Running Hub | Custom `.safetensors` |
| **Image Editing** | Qwen-Edit-2509 | Running Hub | `ComfyUi_Qwen-Edit-2509.json` |
| **Atmosphere/Relighting** | Qwen-Edit + SeedVR2 LoRA | Running Hub | `ComfyUi_Light Transfer Qwen-Edit-2509.json` |
| **Video (I2V B-Roll)** | **Wan 2.2** | Running Hub | `comfyUI-Wan-2.2.json` |
| **Video (Performance)** | **Wan 2.1 One-to-All** | Running Hub | `Wan21_OneToAllAnimation_simplified.json` |
| **Compositing** | Natron (.ntp templates) | **Runpod** (RTX 4090/5090) | `natron_effects_library/` |
| **Assembly** | MoviePy | Local | `audio_effects_library/` |
| **Music Generation** | Suno AI API | Cloud | `suno_integration.py` |
| **Orchestration** | Python + Streamlit | Local | N/A |

**Image Genesis Decision Logic:**

- **Use Coach Identity LoRA** when: Coach is the scene's protagonist ("Icon" scenes), need consistent likeness
- **Use Z-Image Turbo** when: Generic characters, archetypes, "Witness" characters, non-Coach scenes
- **Use Pre-Provided Image** when: Real photos, existing brand assets, pre-shot footage

**Motion Generation Decision Logic:**

- **Use Wan 2.2** when: You have Start Frame + End Frame, motion is ambient (head turn, subtle gesture), controlled via text Kinetic Prompts.
- **Use Wan 2.1 One-to-All** when: You have Artgrid/stock footage with motion, need human-quality performance (dancing, walking), mapping skeleton onto Avatar.

---

### **1.1b Canonical Glossary**

> **⚠️ Use these exact terms across all CMF documentation for consistency.**

**Asset Naming Convention:**

| Conceptual Term | Technical Artifact | Stage | File Pattern |
|-----------------|-------------------|-------|--------------|
| Hero Frame | Scene image (I2I output) | 3.1 | `*_HERO.png` |
| Lit Frame | Relit atmospheric image | 3.2 | `*_HERO_LIT.png` |
| Icon B-Roll | Animated clip (I2V output) | 4 | `*_ICON_RAW_v##.mp4` |
| Composited Scene | VFX-applied output | 5 | `*_ICON_FX.mov` |
| D-Roll | Authentic "dirty" footage | 4.3 | `*_DROLL_*.mp4` |
| E-Roll | Cultural/memetic clips | 4.3 | `*_EROLL_*.mp4` |
| C-Roll | Kinetic typography | 5 | `*_CROLL_*.mov` |

**LoRA Types (NOT Interchangeable):**

| Type | Name | Purpose | Training | Used In |
|------|------|---------|----------|---------|
| **Character LoRA** | Coach Identity | Face/body consistency | Custom (Coach photos) | Stage 3.1, 4 |
| **Lighting LoRA** | SeedVR2, etc. | Atmospheric effects | Pre-trained (generic) | Stage 3.2 only |

**Platform Definitions:**

| Name | Service Type | Purpose | Hardware |
|------|-------------|---------|----------|
| **Running Hub** | Cloud GPU nodes | ComfyUI inference (Z-Image, Wan, Qwen-Edit) | RTX 4090 |
| **Runpod** | Cloud GPU pods | Natron compositing/rendering only | RTX 4090/5090 |
| **Local** | Workstation | MoviePy assembly, Streamlit console | Any |

---

### **1.2 The Guiding Philosophy: The Narrative Core, Sonic Soul, & Visual Trinity**

The architecture of the CMF is built upon three immutable laws of physics that govern engagement: **The Narrative Core** provides the truth, **The Sonic Soul** determines the rhythm, and **The Visual Trinity** provides the proof.

#### **A. The Narrative Core (The Truth)**

Before a pixel is generated or a note is played, the story must be mined. The CMF rejects the notion of AI as a "writer." In our philosophy, AI is a curator, an analyst, and an architect, but it is not the author of human truth.

This is codified in **The Verbatim Constraint**. We do not ask the AI to "write a script about success." Instead, we deploy a sophisticated extraction engine—**The Narrative Core**—to mine the raw ore of human conversation (transcripts, interviews, coaching sessions) for "Gold Nuggets."

This philosophy asserts that the most viral content is not created; it is **found**. The CMF hunts for the **Viral Trinity** within the client's own words:

1. **Surprise:** Does this statement challenge a fundamental assumption?  
2. **Emotion:** Does it carry a visceral charge (shame, pride, relief)?  
3. **Specificity:** Is it grounded in a tangible, sensory reality (not "I was sad," but "I was crying on the kitchen floor at 3 AM")?

The resulting script is not a fabrication; it is an assembly of verbatim reality, structured by the **Script Composer** into a perfect narrative arc. This ensures that the "Soul" of the video remains authentically human, even as the execution becomes increasingly synthetic.

#### **B. The Sonic Soul (The Anchor)**

In the CMF, music is not an accessory; it is the **Director**.

The "Sonic-First" philosophy posits that human emotion is rhythmically entrained. The brain processes audio faster than visual information. We feel anxiety because of a chaotic, dissonant beat before we see the threat; we feel relief because of a resolving harmonic chord before we see the smile. Therefore, before a single image is generated or a single frame is cut, the **Sonic Soul** of the piece must be established.

This is achieved through our proprietary **12 Sonic Story Arcs**. These are not just "genres"; they are emotional blueprints that dictate the pacing, energy, and structure of the entire video.

* **The Arc Dictates the Edit:** If the chosen arc is *"The Ticking Clock"*, the editor knows—before seeing any footage—that the pacing must accelerate, the cuts must be on the beat of a rising synth, and the visual density must increase until a sudden drop.  
* **The Frequency of Truth:** We recognize that the human voice is the primary instrument. The sonic bed must support, not compete with, the vocal frequencies. We engineer a "Sonic Vacuum" at critical turning points—silencing the music to force the audience to lean in for the revelation.

By establishing the Sonic Soul first, we ensure that the video has a heartbeat. The visuals then become the skin and muscle that move to that beat.

#### **C. The Visual Trinity (The Body)**

To achieve maximum retention and persuasion, the CMF moves beyond simple "B-Roll." We categorize all visual inputs into a **Visual Trinity**, a strategic ecosystem designed to stimulate different parts of the viewer's brain simultaneously.

Layer 1: Generative Semiotics (The Story)

This is the domain of A-Roll and Generated B-Roll. It creates the narrative "spine" of the video and represents the "Dream" or the "Internal State."

* **Function:** To tell the specific, allegorical story of the script using a consistent **Brand Avatar**. We do not rely on random actors; we generate a consistent digital protagonist who ages, evolves, and reacts throughout the video.  
* **Mechanism:** We use **Cinematic Metaphors**. Instead of showing a generic "sad person," we generate a specific, visceral moment: a hand trembling while holding a coffee cup, or a "Cinematic Trinity" sequence of Environment, Behavior, and Detail. These images are engineered for **Low Cognitive Load** but **High Emotional Impact**—they are instantly readable symbols of human experience.

Layer 2: Authentic D-Roll (The Truth)

This is the domain of "Dirty" Realism. In an era of polished AI and synthetic perfection, gloss creates distrust. Authenticity creates connection.

* **Function:** To trigger the "That’s Me" pattern match. We validate the polished narrative with raw, unpolished glimpses of reality.  
* **Mechanism:** The **D-Roll Curator** hunts for "found footage" vibes—shaky iPhone camera movements, bad lighting, genuine unscripted reactions. When the script talks about "morning anxiety," we don't show a movie star; we show a grainy clip of a real person staring at a ceiling fan at 3 AM. This layer proves that the coach understands the *actual* lived experience of the audience, not just the theoretical one.

Layer 3: Cultural E-Roll (The Status)

This is the domain of Borrowed Authority and Pattern Interruption.

* **Function:** To leverage the pre-existing emotional capital of pop culture to disrupt the scroll and lend weight to the argument.  
* **Mechanism:** The **E-Roll Curator** injects iconic moments—a clip from *The Matrix*, a snippet of a famous speech, a viral meme. These act as "cognitive shortcuts." Instead of spending 30 seconds explaining "defiance," we insert a 2-second clip of a movie hero standing their ground. The audience instantly downloads the emotional context. This layer serves as the "Pattern Interrupt," snapping the viewer out of a trance with a jolt of familiarity.

### **1.3 The Operational Lifecycle: The 8-Stage Pipeline**

The CMF operates as a linear, high-velocity assembly line. It transforms a raw input (Transcript) into a final output (Production Bible & Asset Pack) through a strict sequence of **8 Deterministic Stages**. Unlike creative chaos, this lifecycle is deterministic: the output of one stage becomes the immutable input of the next.

> **⚠️ This 8-Stage Pipeline is the canonical production structure for CMF 2.0.**

---

**Stage 1: Narrative Core (The Truth)**

The process begins with the Strategic Intent Identifier (The Premise Hunter). We analyze the raw transcript not just for "content," but for viral potential. We categorize the content into one of four strategic lanes: **Heart** (Emotional Resonance), **Mind** (Intellectual Authority), **Community** (Social Connection), or **Proof** (Inspirational Testimonial).

Once the lane is selected, the **Script Composer** activates. Adhering to the "Verbatim Constraint," it assembles the raw quotes into a coherent 60-second narrative. Finally, the **Blueprint Architect** maps this script to a specific visual and sonic plan, creating the `production_blueprint.json`—the "God Object" that controls the rest of the factory.

**Stage 2: Sonic Foundation (The Heartbeat)**

Before visuals are considered, the **Sonic Sommelier** analyzes the target audience's "Tribe Profile" to select a specific musical vintage. The **Sonic Scribe** then translates the emotional beats of the script into a precise Suno.ai Prompt, effectively "scoring" the video before it exists. The **Ad-Lib Amplifier** generates subliminal audio layers. This stage creates the rhythm that the visual editors will cut to.

**Stage 3: Visual Genesis (The Hero Frame)**

This is where the **Digital Cinematographer** creates the foundational visual assets using the **I2I → I2V workflow**:

1. **Stage 3.1 (I2I):** Generate HERO FRAME from character reference images using **Qwen-Image-Edit-2509** with Aesthetic Control vocabulary
2. **Stage 3.2 (Optional):** Apply atmospheric lighting via **Qwen-Edit** with Lighting LoRAs

> **📚 Prompting Reference:** See `AI Video Creation Guide.md` for emotion, lighting, and composition vocabulary.

*Key Output:* `PROJ_XX_SC_XX_HERO.png` and (optional) `PROJ_XX_SC_XX_HERO_LIT.png`

**Stage 4: Motion Harvest (The Kinetic Engine)**

This stage translates the *Potential Energy* of the Hero Frame into *Kinetic Energy* using **two distinct pipelines**:

* **Pipeline A (Wan 2.2 I2V):** For standard B-rolls using HERO FRAME + Kinetic Prompt (motion + camera movement)
* **Pipeline B (Wan 2.1 One-to-All):** For Artgrid/driving video scenes requiring human motion (performance-driven)

> **📚 Prompting Reference:** See `AI Video Creation Guide.md` for camera movement patterns (push in, pull back, pan, arc shot, etc.)

The **Motion Harvester** determines which pipeline to use based on scene requirements and dispatches to Running Hub.

*Key Output:* `PROJ_XX_SC_XX_ICON_RAW_v01.mp4`

**Stage 5: C-Roll & VFX Fabrication (The Natron Factory)**

The **Natron Fabricator** applies C-Roll (Kinetic Typography) and VFX (Glitch transitions, CRT overlays, Glow effects) using pre-built `.ntp` template files. A Python script (`natron_injector.py`) injects file paths into templates and dispatches rendering to **Runpod** GPU pods.

*Key Output:* `PROJ_XX_SC_XX_ICON_FX.mov`

**Stage 6: Assembly & Engineering (The MoviePy Assembler)**

**MoviePy** stitches the Scene Modules onto a timeline based on the Sonic Arc. It uses the Voice Over as the "Master Clock" and applies logic-based audio mixing (ducking, sidechain compression). Time remapping ensures clips fit their slots without gaps.

*Key Output:* `PROJ_XX_DRAFT.mp4`

**Stage 7: Captioning Engine (The WhisperX Layer)**

The **Caption Engine** applies synchronized subtitles using WhisperX for transcription and FFmpeg for burn-in. Captions follow the brand's typography guidelines extracted from the Blueprint.

*Key Output:* `PROJ_XX_CAPTIONED.mp4`

**Stage 8: Hybrid Output (The Final Delivery)**

The final stage produces two outputs:
* **MP4 Render:** The finished video ready for distribution.
* **DaVinci Resolve XML:** An editable timeline for human polish (color grading, audio mastering).

*Key Output:* `PROJ_XX_FINAL.mp4` + `PROJ_XX_timeline.xml`

---

This lifecycle ensures that "Creativity" is not a random act, but a predictable, repeatable, and scalable output of the factory. We do not hope for a good video; we engineer it.

---

### **1.3a Complete Asset Flow Diagram**

> **Visual representation of the complete CMF pipeline from Hero Frame to Final Output.**

```
STAGE 3.1: Z-Image Turbo (Running Hub)
    │
    ▼
HERO.png ──────────────────────────────────────────────────
    │                                                      │
    ▼                                                      │
STAGE 3.2: Qwen-Edit + Lighting LoRA (Running Hub)         │
    │       ├── Workflow: Light Transfer Qwen-Edit-2509    │
    │       └── Uses: SeedVR2 Lighting LoRA                │
    ▼                                                      │
HERO_LIT.png (This IS the End Frame)                       │
    │                                                      │
    ▼                                                      │
STAGE 3.3: Qwen-Edit (NO LoRA) (Running Hub)               │
    │       ├── Workflow: Qwen-Edit-2509 (standard)        │
    │       └── Purpose: Reverse Engineering               │
    ▼                                                      │
HERO_START.png (Start Frame) ──────────────────────────────┤
    │                                                      │
    ▼                                                      │
STAGE 4: Motion Generation (Decision Point)               │
    ├── IF text-driven B-roll ──► Wan 2.2 ─────────────────┤
    │                             (Kinetic Prompts)        │
    └── IF driving video ───────► Wan 2.1 One-to-All ──────┤
                                  (Artgrid/Performance)    │
                                                           │
    ▼                                                      │
ICON_RAW_v01.mp4 ──────────────────────────────────────────┘
    │
    ▼
STAGE 5: Natron Fabricator (Runpod)
    │       ├── VFX Templates (.ntp)
    │       └── C-Roll (Kinetic Typography)
    ▼
ICON_FX.mov
    │
    ▼
STAGE 6: MoviePy Assembler (Local)
    ▼
DRAFT.mp4
    │
    ▼
STAGE 7: WhisperX Caption Engine (Local)
    ▼
CAPTIONED.mp4
    │
    ▼
STAGE 8: Final Output
    ├── FINAL.mp4 (Distribution Ready)
    └── timeline.xml (DaVinci Resolve)
```

**Key Insight:** Stages 3.2 and 3.3 use the SAME model (Qwen-Edit) but DIFFERENT workflows and settings. See Deterministic Manual §3.2-3.3 for detailed specifications.

---

### **1.4 The Human-in-the-Loop Paradigm**

While the CMF is an automation engine, it is not a "black box" that excludes human oversight. It is designed as a **"Director-Driven"** system.

The human operator functions as the **Executive Producer**. The system presents options (e.g., "Here are the Top 8 Viral Premises"), and the human makes the critical strategic decision ("Proceed with Premise \#3"). Once the decision is made, the system executes the labor-intensive work of writing, searching, prompting, and organizing.

This relationship frees the human creator from the tyranny of the "Blank Page" and the drudgery of "Asset Hunting," allowing them to focus entirely on **Taste, Strategy, and Soul.** The CMF handles the "How"; the human handles the "Why."

---

## 

## **2\. Architecture Design & The 4 Pillars**

### **The Intelligence Stack: From Static Truth to Kinetic Experience**

The Conscious Movie Factory (CMF) represents a radical departure from traditional AI video generation methods. It is not a standalone tool, nor is it a simple "text-to-video" prompter. It is a hierarchical intelligence stack designed to solve the single most pervasive failure mode in generative media: **The Hallucination of Context.**

Most AI video workflows fail because they operate in a vacuum. When a user prompts a model to "create a video about success," the AI hallucinates a generic definition of success—usually a man in a suit walking toward a sunset. It does not know who the client is, it does not know the specific cultural language of their audience, and it does not understand the nuanced psychological journey required to build trust. The result is content that looks expensive but feels hollow—technically impressive "slop" that registers as spam to the human brain.

The CMF architecture solves this by acting as the kinetic engine attached to the static intelligence of the Conscious Content Factory (CCF). If the CCF is the "Brain" that defines the worldview, values, and voice, the CMF is the "Nervous System" that translates that worldview into sensory experience.

We do not simply "generate video." We sequentially layer **Meaning**, **Rhythm**, and **Reality** to construct a final artifact that feels inevitable. This architecture enforces a one-way flow of truth: Strategy dictates Narrative; Narrative dictates Sound; Sound dictates Vision. At no point does a downstream agent make a decision that contradicts an upstream truth.

This section details the **Unified Intelligence Architecture**, mapping how the "Soul" of the text becomes the "Beat" of the video, and defining the four immutable pillars that govern this transformation.

---

### **The Integration Bridge: CCF → CMF Data Flow**

The CMF does not guess; it inherits. Before a single frame is rendered or a single note of music is selected, the CMF ingests the **"Source Code"** of the brand directly from the CCF’s output directory. This is a hard-coded dependency. The CMF cannot function without the intelligence assets created during the CCF Setup Phase. This ensures that the video content is not just "cool footage," but a mathematically precise extension of the client’s psychological profile.

This data inheritance occurs through four critical pathways, which we call the **Context Injection Loop**:

#### **1\. The Cultural Inheritance (Tribe Soul → Sonic/Visual Filters)**

The first injection comes from the **Tribe Soul**. In video, "quality" is subjective; "resonance" is objective. What looks like "high production value" to a Baby Boomer (clean lighting, steady cam, orchestral music) looks like "fake corporate advertising" to a Gen Z viewer who values raw, chaotic, lo-fi authenticity.

The CMF reads the tribe\_soul.json file to calibrate its aesthetic sensors.

* **Sonic Calibration:** The **Sonic Sommelier** agent reads the generational\_markers field (e.g., "Gen X, grew up on 90s Hip Hop, values grit") to determine the **Sonic Vintage**. It ensures the system never places a hyper-pop track over a video targeting a stoic, masculine audience, nor a classical score over a video meant for a high-energy, disruptive startup culture. It aligns the BPM and instrumentation with the tribe’s nostalgia centers.  
* **Cultural Calibration:** The **E-Roll Hunter** reads the cultural\_heroes and shared\_enemies fields. If the Tribe Soul lists "The Matrix" or "The Office" as core metaphors, the CMF automatically prioritizes sci-fi dystopia clips or awkward workplace humor for its pattern interrupts. It speaks the tribe's visual language.  
* **Visual Calibration:** The **D-Roll Hunter** reads the demographic\_reality field (e.g., "Overworked corporate moms, late nights, messy kitchens"). This defines the **Authenticity Markers** for the computer vision filter. It tells the AI to reject polished stock photos of models in pristine studios and instead hunt for grainy, imperfect footage that mirrors the messy reality of the audience's actual lives.

#### **2\. The Identity Inheritance (Client Soul → Brand Avatar)**

In text, a "voice" can be consistent even if the writer changes. In video, a "face" must be immutable. One of the greatest challenges in AI video is **Character Consistency**—the tendency for generative models to "morph" the protagonist’s face, weight, or age from shot to shot.

The CMF solves this through the **Identity Inheritance** pathway.

* **The Digital Twin:** The **Brand Avatar Architect** ingests the physical description and style rules defined in the CCF (client\_soul.json). It evolves these text descriptions into **4-Dimensional Consistency Prompts**. While the CCF needs a static image description, the CMF needs a character rigged for motion.  
* **Temporal Consistency:** The system generates "Anchor Prompts" for the client at four key life stages: **Child** (for backstory), **Adolescent** (for formative struggle), **Young Adult** (for the "before" state), and **Current** (for the authority state). Every subsequent visual agent calls upon this master file. This ensures that "Valerie the Struggler" in Scene 2 looks exactly like "Valerie the Mentor" in Scene 5, simply younger and more tired, rather than like a different person entirely.  
* **Subconscious Voice:** The **Ad-Lib Amplifier** uses the voice\_baseline (TTT Temperature) to generate subliminal "Dog Whispers"—internal monologue audio layers that match the client's cadence. If the client is a "Truth-Teller" (TTT-05), these whispers will be sharp and aggressive. If they are a "Compassionate Companion" (TTT-02), the whispers will be soft and fearful.

#### **3\. The Strategic Inheritance (Strategy → Narrative Lane)**

Content without purpose is waste. The CMF inherits the **Strategic Intent** directly from the content\_strategy.md file.

* **The Trust Framework:** The **Strategic Intent Identifier** uses the 7-11-4 Trust Framework to categorize the video's mission. Is this video meant to build intimacy (Heart), establish authority (Mind), or create tribal belonging (Community)?  
* **Lane Locking:** This decision locks the "Strategic Lane" for the entire production. It prevents the common failure of trying to do too much—trying to be funny, smart, sad, and authoritative all at once. The architecture forces a choice, ensuring the video creates a singular, piercing emotional effect.

#### **4\. The Proof Inheritance (Witness Soul → Visual Evidence)**

In the age of skepticism, claims require receipts. The CMF integrates the **Witness Soul** database (\_index.json) to automate the creation of proof.

* **Data Visualization:** When building "Proof" or "Mind" videos, the **Testimonial Architect** pulls specific metrics (e.g., "$10k/month," "30lbs lost") and emotional "Before" states directly from the validated Witness database.  
* **Fact-Checking:** This ensures that the **Data Visualization C-Rolls** (charts, graphs, "savage stats") are factually accurate to the client's track record. The AI is forbidden from hallucinating numbers; it must cite the Witness Soul.

---

### **Pillar 1: The Narrative Soul (Identity & Story)**

The first pillar of the CMF architecture is **The Narrative Soul**. This is the "Why." A video is a vehicle for a story, and if the story is weak, no amount of 4K rendering or Dolby Atmos sound will save it.

The CMF architecture enforces a strict categorization of narrative purpose. We do not "write scripts" in the traditional sense. We extract **Strategic Assets** based on the **Viral Trinity** (Surprise × Emotion × Specificity). The architecture mandates that every video must occupy one of four distinct **"Strategic Lanes."** Each lane has its own architectural rules for pacing, visual selection, and sonic texture.

#### **Lane 1: Heart (Emotional Resonance)**

* **Objective:** To generate deep empathy, psychological safety, and a feeling of "being seen."  
* **Architectural Rules:**  
  * **Pacing:** Slow, deliberate, and breathable. High use of pauses and silence. The rhythm allows the viewer to sit with the emotion.  
  * **Visuals:** Prioritizes **"Cinematic Trinity"** shots (Environment \-\> Behavior \-\> Detail). High use of extreme close-ups (ECU) to show micro-expressions, tears, and subtle shifts in gaze. Generative imagery focuses on isolation and atmosphere.  
  * **Sonic:** Acoustic textures, stripped-back arrangements (piano, cello), and "Sonic Vacuums" where all sound cuts out to highlight a vulnerable confession.

#### **Lane 2: Mind (Intellectual Authority)**

* **Objective:** To disrupt the viewer's worldview, challenge conventional wisdom, and establish high status/authority.  
* **Architectural Rules:**  
  * **Pacing:** Fast, staccato, aggressive. "Ping-pong" editing that keeps the brain engaged.  
  * **Visuals:** Prioritizes **C-Roll** (Kinetic Typography, Data Visualization, Split-Screens) and fast-cut "Debate" montages. Visuals are used to "prove" the argument visually.  
  * **Sonic:** Driving beats, "The Confrontation" arcs, and sharp Sound Effects (glitches, hits, whooshes) that act as cognitive punctuation marks.

#### **Lane 3: Community (Social Connection)**

* **Objective:** To create a "Me Too" moment of shared struggle, validating the audience's hidden pains.  
* **Architectural Rules:**  
  * **Pacing:** Rhythmic and collective.  
  * **Visuals:** Heavy reliance on **Authentic D-Roll**. The goal is to show "the many," not just "the one." We want the viewer to see a montage of people who look like them, experiencing the same struggle.  
  * **Sonic:** "The Shared Struggle" arcs, layered voices, and ambient textures that sound like real environments (coffee shops, city streets).

#### **Lane 4: Testimonial (Inspirational Proof)**

* **Objective:** To provide irrefutable evidence of transformation, moving the viewer from skepticism to belief.  
* **Architectural Rules:**  
  * **Pacing:** "The Rally" structure (Low Energy \-\> High Energy). A clear acceleration from the slow "Before" to the dynamic "After."  
  * **Visuals:** Explicit **"Before & After"** contrasts. Split-screen compositions showing the "Hell" state vs. the "Heaven" state.  
  * **Sonic:** Swelling orchestral scores or driving anthems that build to a euphoric crescendo.

---

### **Pillar 2: The Sonic-First Foundation (The Heartbeat)**

This is the single most important architectural differentiator of the CMF. In traditional video production workflows, audio is the final layer—something added in post-production to "sweeten" the cut. In the CMF, audio is the **foundation**. It is pre-production.

We operate on the neurological truth that **Emotion is Rhythm.** The brain processes audio information faster than visual information. We feel anxiety because of a chaotic, dissonant beat before we visually identify the threat; we feel relief because of a resolving harmonic chord before we see the smile. Therefore, the CMF architecture mandates that the **Sonic Bible** be created before a single image is generated.

#### **1\. The Sonic Story Arc System**

We have codified the entire spectrum of human emotion into **12 Master Sonic Arcs** (e.g., "The Divine Spark," "The Ticking Clock," "The Patient Growth"). These are not vibes; they are rigid timeline instruction sets.

* **The Blueprint:** Each Arc dictates the editing rhythm.  
  * **BPM Curve:** It maps the heart rate of the video. *The Ticking Clock* accelerates from 90 BPM to 140 BPM. *The Quiet Reflection* decelerates to a standstill.  
  * **The Sonic Vacuum:** A hard-coded timestamp in the arc where *all sound must die*. This architectural constraint forces the editor to build visual tension that resolves in absolute silence, creating a "lean-in" moment for the most important line of the script.  
* **The Synergy:** The **Virtual Director** agent reads the Arc metadata. If the Arc is "The Rally," the Director knows Scene 3 must be a chaotic, fast-cut montage to match the rising drum beat. If the Arc is "The Quiet Reflection," Scene 3 must be a single long take to match the sustained pad.

#### **2\. The Sonic Sommelier & Scribe**

These two agents bridge the gap between the abstract "Soul" and the concrete "File."

* **The Sommelier:** Analyzes the Tribe Soul to select a **Sonic Vintage**. It doesn't just pick "Happy Music." It picks "1980s Synth-Wave Nostalgia" for a Gen X Tech Tribe, or "Acoustic Coffee House" for a Millennial Mom Tribe. It ensures the music signals "I am one of you."  
* **The X-Factor Filter:** It applies a frequency mask to ensure the chosen music has "frequency gaps" in the vocal range (1kHz \- 4kHz), ensuring the coach’s voice never fights the melody for dominance.  
* **The Scribe:** Translates the Script’s emotional beats into a **Suno.ai V5 Prompt**. It "scores" the video, mapping the script's "Verse" to the "Setup," the "Pre-Chorus" to the "Challenge," and the "Chorus" to the "Resolution."

#### **3\. The Subconscious Audio Layer**

The architecture includes a dedicated "Invisible Track" for psychological immersion.

* **Dog Whispers:** We use voice cloning technology to generate whispered, subliminal affirmations or fears in the coach's own voice. These are layered at \-25dB—felt rather than heard—triggering deep subconscious associations.  
* **Diegetic Texture:** The architecture mandates: **"If you see it, you must hear it."** If the visual is a "Looking out the window" shot, the system automatically retrieves "Rain on Glass" SFX, even if the video is otherwise silent. This creates a 3D immersive reality that flat video cannot achieve.

---

### **Pillar 3: The Visual Trinity (The Body)**

Once the Soul is defined and the Heartbeat is set, the architecture moves to visual construction. We reject the flat, mono-layered approach of generic AI video which simply "slaps B-roll" over audio. Instead, we architect a **Visual Trinity**—three distinct types of imagery that serve three distinct psychological functions.

#### **Layer A: Generative Semiotics (The Cinema)**

* **Source:** AI Generation (**Z-Image Turbo** for images, **Wan 2.2** for video interpolation).  
* **Function:** Storytelling & Metaphor. This layer visualizes the internal state, the dream, or the nightmare.  
* **The Innovation: Paired Keyframe Architecture.** To solve the "jittery AI" problem where characters morph and backgrounds shift, the **Virtual Director** does not ask for a video. It architects a **Start Frame** and an **End Frame**.  
  * *Start:* "Valerie (35, tired) sitting at a desk, head in hands, blue moonlight, tight framing."  
  * *End:* "Valerie (35, tired) looking up at the screen, eyes wide in shock, blue moonlight, medium framing."  
* **The Execution:** By defining the start and end states with photographic precision, we allow video interpolation models to "tween" the motion perfectly. This creates intentional, directed camera movement (e.g., "Slow Dolly In") rather than random, hallucinogenic AI motion.

#### **Layer B: Authentic D-Roll (The Reality)**

* **Source:** Forensic Search (Asset Hunter).  
* **Function:** Trust & Validation. This layer proves the coach lives in the real world.  
* **Mechanism: The "Dirty" Protocol.** The architecture explicitly forbids polish here. The **D-Roll Hunter** actively searches for imperfection. It uses Gemini Vision to scan search results for **Authenticity Markers**: grain, bad lighting, vertical aspect ratios, cluttered backgrounds, messy hair.  
  * *Logic:* If the script says "I was drowning in laundry," a stock photo of a smiling mom holding a basket destroys trust. A shaky, low-res clip of a toddler screaming while a mom sighs builds trust. This layer grounds the AI visuals in gritty reality.

#### **Layer C: Cultural E-Roll (The Status)**

* **Source:** Cultural Archives (YouTube/Movies).  
* **Function:** Pattern Interrupt & Authority. This layer borrows emotional capital from the culture.  
* **Mechanism: The Memetic Index.** The system scans the script for concepts that have "Cultural Shortcuts."  
  * *Logic:* Instead of spending 30 seconds explaining "a difficult choice," the system inserts the "Red Pill/Blue Pill" clip from *The Matrix*. This borrows the emotional weight of the movie and transfers it to the coach's message instantly. It acts as a rhythmic grenade, snapping the viewer out of a trance.

---

### **Pillar 4: The Automated Procurement Engine (The Hands)**

This is the most technologically advanced pillar of the CMF. It solves the biggest bottleneck in video production: **Asset Hunting**. In a manual workflow, a human editor spends 80% of their time scrolling through stock sites or Google Images. The CMF automates this using a sophisticated **Search-Vision-Select** loop driven by the CLI.

#### **1\. The Search-Vision Loop**

This engine does not just "search text"; it "sees results."

* **Step 1: Translation.** The **Scene Builder** translates a script beat (e.g., "The overwhelming noise of the city") into an "Observable Scenario" (e.g., "Crowded Tokyo crosswalk sound audio visual chaos").  
* **Step 2: Multi-Vector Search.** The agent generates 5-10 search queries across multiple APIs (Google Images, Pexels, YouTube). It searches for literal matches, aesthetic matches, and platform-specific matches.  
* **Step 3: The Vision Filter (The Breakthrough).** This is the core innovation. The agent creates a temporary database of thumbnails. It passes these thumbnails to **Gemini Pro Vision** with a strict scoring rubric:  
  * *Prompt:* "Does this image look STAGED (stock photo lighting, fake smiles) or AUTHENTIC (grainy, messy background, candid)? Rate Authenticity 0-10. Does it contain the demographic markers defined in the Tribe Soul?"  
* **Step 4: Selection & Acquisition.** The system acts as a strict gatekeeper. It discards 90% of the noise and downloads only the top 10% of assets that pass the Vision Filter with a score \> 8\.

#### **2\. The Dual-Track Output**

The Procurement Engine simultaneously manages two tracks, ensuring the "Visual Trinity" is satisfied:

* **Track A (Generative):** Sends precise, consistency-checked prompts to the Image Gen API for the "Cinema" layer.  
* **Track B (Sourced):** Scours the web for the "Reality" and "Status" layers (D-Roll and E-Roll).

This architecture allows the CMF to "instantiate" a video project folder that is fully populated with bespoke, verified, and sorted assets—custom generated characters AND real-world clips—in minutes rather than days.

---

### **System Architecture: The Directory Map**

To implement this philosophy, the CMF uses a strict, standardized file system structure. This structure is not just organization; it is the "physical body" of the factory, defining how data flows from abstract thought to concrete file.

**Root Directory:** \~/cmf/

#### **1\. The Brain (/intelligence/)**

This folder contains the static knowledge base—the "Laws of Physics" for the system.

* frameworks/sonic\_story\_arcs.yaml: The 12 emotional blueprints with BPM/Instrument rules.  
* frameworks/visual\_hooks\_recipes.yaml: The library of visual metaphors (e.g., "The Heavy Backpack Drop").  
* frameworks/master\_effects.yaml: The CapCut effect codes and transition logic.  
* frameworks/viral\_trinity\_scoring.yaml: The rubric for judging script potential.  
* lexicons/brand\_avatar\_dna.json: The master file defining the client's physical appearance.

#### **2\. The Workforce (/agents/)**

This contains the executable prompts for every AI agent.

* \_master/: The orchestrators (Producer, Blueprint Architect, Post-Super).  
* extraction/: The story miners (Premise Hunter, Script Composer, Extractors).  
* sonic/: The audio engineers (Sommelier, Scribe, Ad-Libber).  
* visual/: The directors (Virtual Director, Scene Builder, Metaphor Director).  
* procurement/: The automated hunters (Asset Hunter D-Roll/E-Roll, Cutter).  
* validation/: The quality control (Critic, Audiophile, Continuity Supervisor).

#### **3\. The Factory Floor (/output/)**

This is where projects live. Every video gets a unique ID.

* project\_\[ID\]/:  
  * 01\_narrative/: Final extracted script, premise analysis, and strategic brief.  
  * 02\_sonic/: Sonic Bible, Suno prompts, Ad-Lib brief, and audio manifest.  
  * 03\_storyboard/: The cinematic storyboard (text), production config (JSON), and scene maps.  
  * 04\_assets/:  
    * generative/: AI-created images (Start/End frames) for Track A.  
    * d\_roll/: Downloaded authentic clips for Track B.  
    * e\_roll/: Downloaded pop-culture clips/links for Track C.  
    * a\_roll/: Sliced clips from the original source video (if applicable).  
    * audio/: Generated music, voiceovers, and SFX files.  
  * 05\_assembly/: The final JSON handoff file for the editor.

#### **4\. The Safety Layer**

* cmf\_helpers.sh: The Bash script that manages context loading (so agents don't hallucinate) and atomic file writing (so data isn't corrupted).  
* config.yaml: The session truth. Stores client details, API keys, and project paths.

---

## **3\. The Official Production Workflow**

### **3.1 The Generative Hybrid Operating System**

The CMF Production Workflow is not a linear checklist; it is a **Generative Hybrid Operating System**. It is "Generative" because it creates assets from scratch (images, music, scripts) rather than just editing existing ones. It is "Hybrid" because it merges the precision of code (JSON schemas, CLI automation) with the nuance of creative direction (Director Agents, Sonic Sommeliers).

This workflow transforms the abstract "Client Soul" into concrete "Digital Reality." It operates on a strict **Input/Process/Output (IPO)** model. Every phase is a black box that accepts specific files (Inputs), processes them through an Agent or CLI Tool, and produces a validated asset (Output) that triggers the next phase.

The Golden Rule of CMF Production:

No pixel is generated until the Sound is locked. No Sound is generated until the Blueprint is locked. No Blueprint is locked until the Truth is mined.

---

### **Phase 1: The Narrative Architecture (The Truth)**

**Objective:** To transmute raw, unstructured transcripts into a production-ready "God Object" (The Blueprint) using a precision three-step refinement process. We do not "write" scripts; we excavate them.

#### **Step 1.1: Premise Mining (The Hunt)**

Before writing, we must define the *weapon*. We do not simply "summarize" a transcript; we hunt for the specific psychological trigger it contains.

* **Agent:** The Premise Hunter V2.0  
* **Input:** Raw Transcript (inputs/transcripts/raw\_interview.txt) \+ Tribe Soul Profile \+ Witness Blueprint (if applicable).  
* **The Protocol:** The agent scans the text against the **Viral Trinity Formula** (Surprise × Emotion × Specificity). It creates a structured analysis of the raw material, identifying 8 potential "Viral Premises" and ranking them by a **60-Point Viral Score**.  
  * It categorizes each premise into a **Strategic Lane**:  
    * **Heart:** Emotional vulnerability and connection.  
    * **Mind:** Intellectual authority and contrarian insight.  
    * **Community:** Shared struggle and validation.  
    * **Proof:** Empirical evidence and transformation.  
  * Crucially, it extracts **16-24 Verbatim Quotes** for each premise. These are the building blocks of the script.  
* **Output:** 01\_narrative/premise\_analysis.json (A ranked menu of 8 strategic options).  
* **Human Action:** The Director reviews the menu and selects the "Winning Premise" (e.g., "Premise \#3: The Hidden Cost of Silence").

#### **Step 1.2: Verbatim Script Assembly (The Composition)**

Once the premise is selected, the system moves from analysis to construction.

* **Agent:** The Script Composer V1.0  
* **Input:** premise\_analysis.json \+ Selected Premise ID.  
* **The Protocol:** This agent operates under the **Verbatim Mandate**. It is strictly forbidden from inventing text or using AI "filler" words. It acts as a "Narrative Architect," arranging the raw quotes extracted in Step 1.1 into a perfect 60-second narrative flow.  
  * **Structure:** It organizes quotes into the Conscious Arc: Hook \-\> Setup \-\> Challenge \-\> Turning Point \-\> Resolution \-\> Close.  
  * **Scoring:** It grades its own work on "Script Viability" (Flow, Clarity, Arc), ensuring the collage of quotes feels like a cohesive story.  
* **Output:** 01\_narrative/final\_script.json (A sequence of timed, verbatim quotes).

#### **Step 1.3: Production Blueprinting (The Plan)**

The script is text; the blueprint is executable code. This step translates the "What" into the "How."

* **Agent:** The Blueprint Architect V3.0  
* **Input:** final\_script.json \+ Sonic Story Arc Library \+ Conscious Scene Builder.  
* **The Protocol:** The agent deconstructs the script into a dynamic sequence of 4-8 scenes. It is the bridge between the writer and the director.  
  * **Sonic Mapping:** It assigns the specific **Sonic Arc** (e.g., "The Rally" or "The Divine Spark") that matches the emotional journey of the text.  
  * **Visual Mapping:** It assigns a specific **Scene Template** to every beat (e.g., "Line 1 \= HOOK-4 Found Clip Reframe," "Line 2 \= SETUP-1 Personal Low Visualization").  
  * **Context Inheritance:** It ensures the visual choices align with the *Premise Hunter's* original "Visual Trinity" recommendations (e.g., ensuring a "Proof" script gets "Data Viz" scenes).  
* **Output:** 01\_narrative/production\_blueprint.json (The Master Instruction Set for the rest of the factory).

---

### **Phase 2: The Sonic Foundation (The Heartbeat)**

**Objective:** To generate the auditory landscape (Music, Voice, Texture) that dictates the rhythm of the edit. **This phase creates the timeline before visuals exist.**

#### **Step 2.1: Sonic Sommelier Analysis**

* **Agent:** The Sonic Sommelier  
* **Input:** production\_blueprint.json \+ Tribe Soul Profile \+ Genre Library.txt.  
* **The Protocol:** The agent acts as a Cultural Resonance Strategist. It analyzes the target audience to determine the **Sonic Vintage**. It asks: *"What does this Tribe listen to?"* and *"What is the musical texture of this specific emotion?"*  
  * *Example:* For a Gen X Entrepreneur target, it might select "90s Boom Bap" mixed with "Cinematic Strings."  
  * *Example:* For a Wellness Tribe, it might select "432Hz Ambient" mixed with "Lo-Fi beats."  
* **Output:** 02\_sonic/sonic\_sourcing\_brief.json containing specific genre tags, BPM targets, and "X-Factor" filters.

#### **Step 2.2: The Sonic Scribe (Generation)**

* **Agent:** The Sonic Scribe  
* **Input:** production\_blueprint.json \+ sonic\_sourcing\_brief.json.  
* **The Protocol:** The agent translates the Script and Blueprint into a **Suno.ai V5 Prompt**. This is a "musical score in text form."  
  * It maps the **Blueprint Scenes** to **Song Structures** (Scene 1/Hook \= Intro, Scene 3/Challenge \= Pre-Chorus Build, Scene 5/Resolution \= Chorus).  
  * It embeds **Directorial Notes** (e.g., *"\[Break\] Silence. Sonic Vacuum."*) to ensure the music respects the dialogue gaps defined in the Blueprint.  
* **Action:** The system generates the music via Suno (or selects from the library if using stock).  
* **Output:** 02\_sonic/music\_track.mp3 and 02\_sonic/suno\_prompt.txt.

#### **Step 2.3: Subconscious Audio Layering**

* **Agent:** The Ad-Lib Amplifier  
* **Input:** production\_blueprint.json.  
* **The Protocol:** The agent generates the "invisible" audio layers defined in the Blueprint's emotional arc. These are the sounds that are felt rather than heard.  
  1. **Confirmation Bias Ad-Libs:** "Dog Whispers" (subliminal affirmations voice-cloned in the coach's voice).  
  2. **Cultural Echoes:** Quotes from external sources/documentaries that validate the message.  
  3. **Diegetic Texture:** Specific sounds implied by the script (e.g., *“The sound of a ticking clock”*, *“City traffic”*, *“Rain on glass”*).  
* **Output:** 02\_sonic/audio\_manifest.json (List of SFX and Ad-Libs to generate/find).

---

### **Phase 3: The Visual Architecture (The Execution)**

**Objective:** To translate the blueprint and sonic rhythm into a precise visual plan, ensuring character consistency and cinematic quality.

#### **Step 3.1: Brand Avatar Definition**

* **Agent:** Brand Avatar Generation Agent  
* **Input:** Client Profile (Photos/Description) \+ production\_blueprint.json.  
* **The Protocol:** The agent defines the **Visual DNA** of the protagonist. It solves the "AI Morphing" problem by creating a master prompt for the character at different life stages.  
  * *Consistency Anchors:* Defines the specific facial features, hair style, and clothing that must remain constant.  
  * *Timeline Mapping:* Creates variations for "Young Adult" (flashbacks) vs. "Current" (narrator).  
* **Output:** 03\_storyboard/brand\_avatar.json (The "Cast" file).

#### **Step 3.2: The Virtual Directing (Master Storyboard)**

* **Agent:** The Virtual Director  
* **Input:** production\_blueprint.json \+ brand\_avatar.json \+ Visual Hooks Recipes.  
* **The Protocol:** This is the core creative step. The agent writes the **Master Cinematic Storyboard** following the exact scene sequence defined by the *Blueprint Architect*.  
  * **For Generative Scenes (A-Roll):** It defines the **Start Frame** and **End Frame** prompts. This "Paired Keyframe" approach allows for seamless video interpolation.  
  * **For D-Roll/E-Roll Scenes:** It refines the "Observable Scenarios" into specific shot descriptions (e.g., "Close up of hands wringing in anxiety" vs. "Wide shot of lonely office").  
  * **Technical Specs:** Defines Lens (85mm vs 35mm), Lighting (Rembrandt vs Soft), and Color Grade (Teal/Orange vs B\&W) for every shot to ensure visual continuity.  
* **Output:** 03\_storyboard/master\_storyboard.md (Human readable) & 03\_storyboard/production\_config.json (Machine readable asset list).

---

### **Phase 4: Asset Procurement (The Automated Hunt)**

**Objective:** To execute the storyboard. This phase uses the **CLI Automation** to procure assets. Unlike previous versions, this phase focuses on the *external* and *generative* assets—the B-Roll, the E-Roll, and the Dream Layer.

#### **Track A: Generative Semiotics (The Dream)**

* **Agent:** The Prompt Engineer (Automated)  
* **Action:**  
  1. Reads production\_config.json.  
  2. Extracts all scenes tagged as "Generative" (A-Roll Visualization).  
  3. Injects the correct brand\_avatar string into the scene\_prompt to ensure the character looks like the client.  
  4. Sends prompts to the Image Generation API (e.g., Midjourney via Discord connector or Flux API).  
  5. **Consistency Loop:** Generates both the Start Frame and End Frame for interpolation.  
* **Output:** High-res images saved to 04\_assets/generative/.

#### **Track B: The Asset Hunter (The Reality \- D-Roll & E-Roll)**

* **Agent:** The Asset Hunter (Vision-Enhanced CLI)  
* **Action:** This is the "Search & Vision" loop.  
  * **Query Generation:** Reads the "Observable Scenario" from the storyboard (e.g., *"A tired mom looking at a laptop in a messy kitchen"*). Converts this into search queries for Google Images, Pexels, or YouTube.  
  * **Search Execution:** Runs the search via API.  
  * **The Vision Filter:** This is the quality control. The system passes search result thumbnails to **Gemini Pro Vision** with a specific rubric:  
    * *"Rate authenticity 0-10. Does this look staged (stock photo) or authentic (real life)? Does it match the demographic profile?"*  
  * **Selection & Download:** Images/Videos with an Authenticity Score \> 8 are automatically downloaded.  
  * **E-Roll Specifics:** For cultural clips, it searches YouTube for specific scenes and logs the URL and timestamp.  
* **Output:**  
  * Authentic clips saved to 04\_assets/d\_roll/.  
  * Cultural clips/links saved to 04\_assets/e\_roll/.

---

### **Phase 4.5: A-Roll Extraction (The Cutter)**

**Objective:** To physically create the base layer of the video. This is the "Raw-to-Edit" pipeline that processes the original source video file.

Why is this separate?

While Phase 4 hunts for supplementary assets (B-Roll), Phase 4.5 handles the primary asset (A-Roll). This phase requires access to the large source video file and uses FFmpeg for precise temporal slicing. It happens after the script is locked but before the final assembly, ensuring the A-Roll is ready to serve as the foundation for the B-Roll layering.

#### **Step 4.5.1: Timestamp Parsing**

* **Agent:** The Cutter  
* **Input:** 01\_narrative/final\_script.json \+ Raw Source Video (inputs/raw\_video.mp4).  
* **The Protocol:** The agent reads the final script and extracts the exact start and end timestamps for every quote.  
  * It verifies the integrity of the timecodes (e.g., Start Time \< End Time).  
  * It checks for overlaps or gaps.  
  * It maps each clip to its narrative function (e.g., "Clip 1 \= Hook," "Clip 2 \= Setup").

#### **Step 4.5.2: The Cut Manifest**

* **Action:** The agent generates a machine-readable cut\_jobs.json file. This file is a precise instruction set for the slicing engine.  
  * *Example Entry:* {"id": "clip\_01\_hook", "start": "00:04:23.000", "end": "00:04:35.000", "source": "raw\_interview.mp4"}

#### **Step 4.5.3: FFmpeg Execution**

* **Action:** The system triggers the local Python script (tools/execute\_cuts.py).  
* **The Process:** This script wraps FFmpeg to physically slice the source video file.  
  * **Precision:** It uses high-precision seeking to ensure the cut happens exactly on the requested frame, not the nearest keyframe.  
  * **Encoding:** It re-encodes the audio to a standard format (AAC 48kHz) to prevent sync issues in the editing software.  
  * **Output:** It saves the individual MP4 clips into the 04\_assets/a\_roll/ directory (e.g., clip\_001\_hook.mp4, clip\_002\_setup.mp4).

#### **Step 4.5.4: XML Timeline Generation**

* **Action:** The agent generates an .xml file (FCPXML format) compatible with DaVinci Resolve.  
* **The Result:** This file contains the timeline data. When the editor imports this file, the A-Roll clips are already placed in order on Track 1, with the correct spacing and gaps left for transitions. The timeline is pre-built.

---

### **Phase 5: Assembly & Validation (The Handoff)**

**Objective:** To package the chaos of raw assets into a structured, verified format for the human editor (or automated editing pipeline).

#### **Step 5.1: The Continuity Check**

* **Agent:** The Continuity Supervisor  
* **Input:** 04\_assets/generative/ \+ brand\_avatar.json.  
* **The Protocol:** The agent uses Gemini Vision to compare the generated images against the Brand Avatar definition.  
  * *Vision Check:* "Is the person in Scene 1 the same as the person in Scene 4? Are they wearing the same clothes? Is the lighting consistent?"  
  * *Result:* It flags any inconsistencies (e.g., "Avatar changed shirt color in Scene 3") and triggers a regeneration request if necessary.

#### **Step 5.2: The Production Handoff**

* **Agent:** The Asset Taskmaster (Production Coordinator)  
* **Input:** All 04\_assets subfolders \+ production\_blueprint.json.  
* **The Protocol:** The agent compiles the **Final JSON Handoff**. This is the master inventory file.  
  * **Timeline Structure:** It links the Script Audio to the Music Track.  
  * **Visual Track:** It maps every timestamp in the audio to a specific file path in /04\_assets/ (linking the A-Roll, B-Roll, and Generative assets to their timeline positions).  
  * **Effect Track:** It reads the *Scene Builder* map and appends the specific **CapCut Effect Codes** (e.g., EFFECT-C-04 Modern Grade, EFFECT-TR-01 Glitch) to each scene metadata, giving the editor explicit technical instructions.  
* **Output:** 05\_assembly/project\_handoff.json.

### **Summary of Workflow Logic**

The CMF workflow is a **Dependency Cascade**.

1. **Truth (Narrative):** We mine the raw ore for the story.  
2. **Rhythm (Sonic):** We build the musical track to carry the story.  
3. **Plan (Visual):** We map the imagery to the rhythm.  
4. **Reality (Procurement):** We hunt/generate the imagery.  
5. **Foundation (Cutter):** We carve the base video layer.  
6. **Package (Assembly):** We bundle it for the finish.

This structure ensures that "Creativity" is not a bottleneck, but a flow state. The machine handles the logic, the search, and the assembly, leaving the human to handle the final polish and the "Go/No-Go" strategic decisions. \[citation: 5330-5344\] \[citation: 8499-8551\] \[citation: 12837-12840\]

---

## 

## **4\. Agent Registry (The Workforce)**

### **The CMF Workforce: 20+ Specialized Intelligence Units**

The Conscious Movie Factory does not rely on a single, monolithic AI model. It is a synchronized orchestra of **20+ Specialized Intelligence Units**, each possessing a distinct persona, expertise domain, and operational protocol.

Unlike generic tools that attempt to be "all-in-one" creators, CMF agents are **Role-Locked Specialists**. The *Sonic Sommelier* does not write scripts. The *Virtual Director* does not choose music. This division of labor ensures that every layer of the video—Narrative, Sonic, Visual, and Procurement—is executed with expert-level depth rather than generalist mediocrity.

### **Agent Design Philosophy**

Every CMF agent is built on three foundational principles:

1. **Persona-Driven Execution:** Each agent simulates a specific human expert (e.g., a "Viral Strategist," a "Musicologist," a "Director of Photography"). This shapes their decision-making patterns.  
2. **Protocol-Based Operation:** Agents do not improvise. They execute explicit .md protocol files containing their "Laws of Physics" (e.g., *The Viral Trinity*, *The Sonic Story Arcs*).  
3. **State-Aware Handover:** Agents do not communicate directly. They save their work to specific JSON files (e.g., premise\_analysis.json) which serve as the immutable input for the next agent in the chain.

---

## **Group I: The Narrative Core (The Brain)**

These agents form the new **Strategic Intelligence Layer**. They are responsible for mining the "Truth" from the raw source material and architecting the story before any production begins.

### **1\. The Premise Hunter (Strategic Analyst) 🔎**

* **File:** agents/extraction/premise\_hunter.md  
* **Protocol:** prompts/extraction/premise\_hunter\_protocol.md  
* **Source Reference:** 🔎 THE PREMISE HUNTER AGENT

Role: The Viral Archaeologist

Identity: An elite narrative intelligence agent who bridges the gap between raw human expression and viral potential. They do not create; they hunt. They scan transcripts not for information, but for "Singular Moments of Truth" that score high on the Viral Trinity (Surprise × Emotion × Specificity).

Core Function:

* **Mining:** Scans raw transcripts to identify 8 potential "Viral Premises."  
* **Scoring:** Ranks each premise using a **60-Point Viral Score** (Surprise, Emotion, Specificity, Universal Appeal).  
* **Lane Assignment:** Categorizes each premise into a Strategic Lane: **Heart** (Vulnerability), **Mind** (Authority), **Community** (Connection), or **Proof** (Testimonial).  
* Quote Extraction: Pulls 16-24 verbatim quotes for each premise to serve as raw material.  
  Key Output: 01\_narrative/premise\_analysis.json (A ranked menu of strategic options).

### **2\. The Script Composer (Verbatim Architect) ✍️**

* **File:** agents/extraction/script\_composer.md  
* **Protocol:** prompts/extraction/script\_composer\_protocol.md  
* **Source Reference:** ✍️ THE SCRIPT COMPOSER AGENT V1

Role: The Narrative Assembler

Identity: A master editor who operates under a strict "Zero New Text" mandate. They do not write; they assemble. They believe that the most powerful scripts are built from the speaker's own words, not AI-generated filler.

Core Function:

* **Selection:** Takes the "Winning Premise" selected by the human director.  
* **Assembly:** Arranges the raw quotes extracted by the *Premise Hunter* into a perfect 60-second narrative arc (Hook → Setup → Challenge → Turning Point → Resolution → Close).  
* Validation: Checks its own work to ensure every word is traceable to a timestamped source.  
  Key Output: 01\_narrative/final\_script.json (A sequence of timed, verbatim quotes).

### **3\. The Blueprint Architect (Production Planner) 🎬**

* **File:** agents/\_master/blueprint\_architect.md  
* **Protocol:** prompts/\_master/blueprint\_architect\_protocol.md  
* **Source Reference:** 🎬 The Blueprint Architect

Role: The Bridge Between Story & System

Identity: A production genius who speaks both "Emotion" and "JSON." They translate the text script into a machine-readable instruction set for the rest of the factory.

Core Function:

* **Scene Deconstruction:** Breaks the 60-second script into a dynamic sequence of 4-8 scenes.  
* **Mapping:** Assigns a specific **Scene Template** (from the *Scene Builder Library*) to every beat (e.g., "Line 1 \= HOOK-4 Found Clip Reframe").  
* **Sonic Tagging:** Assigns the definitive **Sonic Arc** (e.g., "The Rally") that matches the emotional journey.  
* Context Inheritance: Ensures that the Premise Hunter’s "Visual Trinity" recommendations are baked into the plan.  
  Key Output: 01\_narrative/production\_blueprint.json (The Master Instruction Set).

---

## **Group II: Sonic Intelligence Team (The Audio Engineers)**

These agents take the Blueprint and build the "Sonic Soul"—the rhythm and atmosphere that dictates the visual edit.

### **4\. The Sonic Sommelier (Musicologist) 🍷**

* **File:** agents/sonic/sommelier.md  
* **Protocol:** prompts/sonic/sommelier\_protocol.md

Role: The Cultural Resonance Strategist

Identity: An elite music supervisor who thinks in "Tribal Vintages." They know exactly what a 45-year-old CEO listens to versus a 22-year-old creator.

Core Function:

* **Tribe Analysis:** Reads the *Tribe Soul Profile* to identify the target audience's musical nostalgia.  
* Vintage Selection: Selects a precise genre blend (e.g., "Cinematic Lo-Fi with 90s Boom-Bap Drums") that fits the Sonic Arc defined in the Blueprint.  
  Key Output: 02\_sonic/sonic\_sourcing\_brief.json.

### **5\. The Sonic Scribe (Lyricist & Composer) 🎼**

* **File:** agents/sonic/scribe.md  
* **Protocol:** prompts/sonic/scribe\_protocol.md

Role: The AI Composer

Identity: A master prompt engineer for Suno.ai. They translate narrative beats into musical instructions.

Core Function:

* **Translation:** Converts the Blueprint Scenes into a musical structure (Scene 1/Hook \= Intro, Scene 3/Challenge \= Pre-Chorus).  
* Directorial Notes: Embeds dynamic instructions (e.g., "\[Break\] Silence. Sonic Vacuum.") to ensure the music breathes with the story.  
  Key Output: 02\_sonic/suno\_prompt.txt.

### **6\. The Ad-Lib Amplifier (Subconscious Architect) 🔊**

* **File:** agents/sonic/ad\_lib\_amplifier.md  
* **Protocol:** prompts/sonic/ad\_lib\_protocol.md

Role: The Sound Designer

Identity: A psychologist of sound. They understand that what you hear in the background determines what you feel.

Core Function:

* **Layering:** Generates scripts for subliminal "Dog Whispers" (internal thoughts) and "Cultural Echoes" (external quotes).  
* Diegetic Manifest: Lists the specific sound effects (SFX) required by the Blueprint scenes (e.g., "Ticking Clock," "City Traffic").  
  Key Output: 02\_sonic/audio\_manifest.json.

---

## **Group III: Visual Architecture Team (The Directors)**

These agents execute the visual plan defined in the Blueprint.

### **7\. The Brand Avatar Architect (Casting Director) 🔮**

* **File:** agents/visual/avatar\_architect.md  
* **Protocol:** prompts/visual/brand\_avatar\_protocol.md

Role: The Identity Guardian

Identity: A character designer who solves the "AI Consistency Problem."

Core Function:

* **DNA Definition:** Defines the subject's physical "Seed" (Age, Ethnicity, Hair, Style).  
* Timeline Mapping: Creates 4 distinct prompts for the character at different life stages (Child, Adolescent, Young Adult, Current) to support the Blueprint's timeline.  
  Key Output: 03\_storyboard/brand\_avatar.json.

### **8\. The Virtual Director (Storyboard Artist) 🎬**

* **File:** agents/visual/virtual\_director.md  
* **Protocol:** prompts/visual/virtual\_director\_protocol.md

Role: The Cinematographer

Identity: A master visual storyteller who translates the Blueprint's scene codes into "Paired Keyframes."

Core Function:

* **Shot Design:** Describes the **Start Frame** and **End Frame** for every Generative Scene (A-Roll).  
* **Technical Specs:** Defines Lens (35mm vs 85mm), Lighting (Rembrandt vs Soft), and Color Grade for every shot.  
* Observable Scenarios: Refines the descriptions for D-Roll and E-Roll searches.  
  Key Output: 03\_storyboard/master\_storyboard.md.

### **9\. The Scene Builder (The Specialist) 🏗️**

* **File:** agents/visual/scene\_builder.md  
* **Protocol:** prompts/visual/scene\_builder\_protocol.md

Role: The Recipe Master

Identity: A specialist in "Visual Recipes."

Core Function:

* Reference: Provides the specific ingredients for the 18 Scene Types (e.g., "To build HOOK-4, you need 1 Glitch Transition \+ 1 Record Scratch").  
  Used By: The Blueprint Architect and Virtual Director.

---

## **Group IV: Asset Procurement Team (The Automated Hunters)**

These agents execute the search, generation, and slicing commands via the CLI.

### **10\. The Prompt Engineer (Generative Specialist) 🖼️**

* **File:** agents/procurement/prompt\_engineer.md  
* **Protocol:** prompts/procurement/prompt\_engineer\_protocol.md

Role: The Midjourney Whisperer

Identity: An expert in AI image syntax.

Core Function:

* **Formatting:** Converts the *Virtual Director's* shot descriptions into optimized Midjourney/Flux prompts, injecting the *Brand Avatar* DNA.

### **11\. The Asset Hunter (D-Roll / Authentic) 📸**

* **File:** agents/procurement/asset\_hunter\_droll.md  
* **Protocol:** prompts/procurement/droll\_protocol.md

Role: The Documentary Researcher

Identity: A forensic search agent equipped with Computer Vision. They hate stock footage.

Core Function:

* **Search & Vision:** Scours the web for "Observable Scenarios" defined in the Blueprint. Uses Gemini Vision to filter for "Authenticity" (grain, bad lighting, real people).

### **12\. The Asset Hunter (E-Roll / Cultural) 🎞️**

* **File:** agents/procurement/asset\_hunter\_eroll.md  
* **Protocol:** prompts/procurement/eroll\_protocol.md

Role: The Pop Culture Historian

Identity: A meme archivist who knows every movie scene and viral clip.

Core Function:

* **Clip Hunting:** Finds the specific YouTube clips referenced in the Blueprint (e.g., "The Matrix Red Pill"). Returns URLs and timestamps.

### **13\. The Cutter (A-Roll Specialist) ✂️**

* **File:** agents/procurement/cutter.md  
* **Protocol:** prompts/procurement/cutter\_protocol.md  
* **Source Reference:** Gemini CLI \+ DaVinci Resolve: Execute Pre-Made Cut Decisions

Role: The Assembly Editor

Identity: A technical editor who operates with frame-level precision. They do not make creative decisions; they execute the "Cut List" generated by the narrative team. They speak the language of FFmpeg and XML.

Core Function:

* **Parsing:** Reads the final\_script.json to extract the timestamped "In" and "Out" points for every quote.  
* **Slicing:** Triggers the execute\_cuts.py tool to physically slice the raw source video file into individual MP4 clips for the A-Roll track.  
* XML Generation: Creates the DaVinci Resolve .xml timeline file, placing the sliced A-Roll clips in sequential order on Track 1\.  
  Key Output: 04\_assets/a\_roll/ (folder of clips) and 05\_assembly/timeline\_import.xml.

---

## **Group V: Master Orchestrators & QA**

### **14\. The Producer (System State Manager) 📢**

* **File:** agents/\_master/cmf\_producer.md  
* **Role:** Manages the workflow state and triggers the next agent.

### **15\. The Post-Super (Final Assembly) 🎞️**

* **File:** agents/\_master/post\_super.md  
* **Role:** Compiles all procured assets into the final production\_handoff.json.

### **16\. The Validators (QA Team)**

* **Critic:** Checks narrative flow and arc compliance.  
* **Audiophile:** Checks sonic texture and mix balance.  
* **Continuity Supervisor:** Checks visual consistency against the Brand Avatar.

---

## **5\. The Automated Procurement Protocols**

### **5.1 The "Search-Vision-Select" Architecture**

Section 5 defines the operational logic of the **Automated Procurement Engine**. This is the factory’s heavy lifting division, the system that replaces the human editor’s most exhausting and time-consuming task: asset hunting.

In the traditional video production workflow, the "search cost" is the single largest inefficiency. A human editor might spend four to six hours scouring stock footage sites, YouTube, and archival libraries to find a single three-second clip that feels "authentic." They are forced to wade through thousands of polished, soulless studio clips to find one diamond in the rough. This friction is the primary reason why high-quality, emotionally resonant content is difficult to scale.

The CMF solves this problem by automating the search process through a proprietary architecture we call **"Search-Vision-Select."** This protocol creates a closed-loop intelligence system that does not just search for keywords; it *sees*, *judges*, and *acquires* visual content with the discernment of a human director but the speed of a machine.

#### **The Logic of Automated Discernment**

The Procurement Engine operates on a fundamental rejection of the standard "Keyword Matching" algorithm used by stock sites. If you search for "stressed mother" on a stock site, the algorithm returns images tagged with those words—usually a model in a pristine kitchen feigning stress with perfect lighting. The algorithm validates the *metadata*, not the *aesthetic truth*.

The CMF’s "Search-Vision-Select" architecture adds a **Semantic Vision Layer** to the process. It inserts a multimodal AI eye (Gemini Pro Vision) between the search results and the final selection. The system does not trust the tags; it looks at the pixels.

The process functions as a deterministic loop:

1. **Translation (The Request):** The system converts narrative needs from the *Blueprint Architect* (e.g., "A moment of overwhelming parental chaos") into a set of visual search vectors (e.g., "tired mom messy kitchen candid grainy").  
2. **Acquisition (The Dragnet):** The CLI executes a massive, multi-platform sweep, fetching raw candidates from Google Images, YouTube, Pexels, Unsplash, and Storyblocks. It casts a wide net, knowing that 90% of what it catches will be unusable "slop."  
3. **Vision Filtering (The Intelligence):** This is the engine's brain. The system creates a temporary database of thumbnails and passes each one to the Vision Model with a specific interrogative prompt. It asks the AI to judge the image not on relevance, but on *authenticity*, *demographic alignment*, and *emotional weight*.  
4. **Selection (The Edit):** The system applies a strict numerical threshold. Only assets that score above an 8/10 on the "Authenticity Scale" are allowed into the project folder. The rest are discarded.

This architecture transforms the procurement process from a manual treasure hunt into a deterministic industrial process. The following protocols detail exactly how this engine executes its four primary mandates: Authenticity (D-Roll), Culture (E-Roll), Dream (Generative), and Foundation (A-Roll Cutting).

---

### **5.2 Protocol A: The D-Roll Hunter (Authenticity Engine)**

Agent: The Asset Hunter (D-Roll)

File: agents/procurement/asset\_hunter\_droll.md

Objective: To procure "Dirty Realism." To scour the web for footage that looks user-generated, authentic, imperfect, and deeply human, validating the viewer's struggle through visual empathy.

The D-Roll Hunter is the most critical component for building trust. Its mandate is to reject perfection. It is programmed to understand that in the current media landscape, high production value often signals "lie," while low production value signals "truth." It hunts for the "glitch," the grain, and the messy background that proves the footage is real.

#### **Step 1: Input Ingestion & Scenario Translation**

The protocol begins by ingesting the specific scene requirements from the production\_blueprint.json. The agent extracts three specific data points for every D-Roll scene:

* **The Observable Scenario:** A literal, physical description of the action (e.g., "A person sitting on the floor of a bedroom surrounded by unpaid bills, head in hands").  
* **The Demographic Filter:** The specific visual markers of the target tribe derived from the *Tribe Soul* (e.g., "Millennial, 30s, messy bun, apartment living, not a luxury home, casual attire").  
* **The Authenticity Markers:** The aesthetic qualities that define "real" for this audience (e.g., "Bad lighting, vertical orientation, clutter in background, no makeup, slight camera shake").

#### **Step 2: Query Vectorization (The Search Matrix)**

A human searcher typically tries one keyword, fails, and tries another. The D-Roll Hunter creates a **Search Matrix**—a simultaneous execution of 10-15 distinct search strategies designed to triangulate the perfect clip across the semantic web.

It generates queries across four vectors to maximize coverage:

1. **Literal Vectors:** Describes the subject directly.  
   * *"stressed woman looking at bills floor"*  
   * *"crying anxiety attack bedroom"*  
2. **Aesthetic Vectors:** Describes the "look" of the file.  
   * *"grainy iphone video sad night"*  
   * *"low light candid struggle vertical"*  
   * *"amateur footage stressed parent"*  
3. **Platform-Specific Vectors:** Uses the language of user-generated content platforms to find vlogs and confessions.  
   * *"my mental health journey vlog"*  
   * *"day in the life burnout tiktok"*  
   * *"real depression room tour"*  
4. **Negative Filtering:** Explicitly excludes the markers of stock footage to pre-filter the noise.  
   * *"-stock \-studio \-smiling \-corporate \-4k \-tripod"*

The system fires these queries against multiple APIs simultaneously, aggregating a pool of roughly 50-100 raw candidate images or video thumbnails.

#### **Step 3: The Vision Filter (The "Authenticity Score")**

This is where the CMF differentiates itself from a simple scraper. The raw candidates are often a mix of genuine photos and staged stock images that managed to slip through the keyword filters. To separate them, the system employs **Gemini Pro Vision**.

The agent passes each thumbnail to the Vision Model with a strict, multi-criteria scoring rubric. The prompt is engineered to force the AI to act as a cynical creative director who hates fake content:

Vision Prompt:

"Analyze this image for use in a gritty, documentary-style video about \[Topic\]. We are looking for Radical Authenticity.

**Criteria 1: The Stock Photo Test (Pass/Fail)**

* Does the subject have perfect skin, perfect teeth, or a 'frozen' smile?  
* Is the lighting professionally balanced (three-point lighting)?  
* Is the background blurry and nondescript (bokeh) or perfectly staged?  
* *IF YES TO ANY: Score 0\. Immediate Fail.*

**Criteria 2: The Reality Test (Score 1-10)**

* Is the lighting bad, harsh, or dim (e.g., overhead fluorescent, computer screen glow)? (+2 points)  
* Is the background cluttered, messy, or specific (e.g., laundry on the couch, dirty dishes, unmade bed)? (+3 points)  
* Does the subject look genuinely tired, unkempt, or unguarded? (+3 points)  
* Does the image quality have grain, noise, or compression artifacts consistent with a phone camera? (+2 points)

**Criteria 3: The Demographic Match (Yes/No)**

* Does this person match the description: \[Black woman, 30s, corporate attire\]?

**Output:** Return a JSON object with score and reasoning."

#### **Step 4: Selection & Acquisition**

The system processes the Vision scores. Any asset scoring below an 8.0 is instantly discarded. The remaining assets are ranked by score. The top 3 candidates are automatically downloaded to the project folder (04\_assets/d\_roll/). The system renames the files to match the scene code (e.g., CHALLENGE\_3\_option\_A.mp4), ensuring the editor knows exactly where to place them without having to preview the file.

---

### **5.3 Protocol B: The E-Roll Hunter (Cultural Engine)**

Agent: The Asset Hunter (E-Roll)

File: agents/procurement/asset\_hunter\_eroll.md

Objective: To procure "Cultural Echoes." To locate specific, iconic moments in pop culture history that act as pattern interrupts, borrowed authority, or shared language.

While the D-Roll Hunter looks for the *unknown* (authentic strangers), the E-Roll Hunter looks for the *known* (famous moments). Its challenge is not distinguishing reality from fake, but distinguishing the *specific clip* from the ocean of commentary, reaction videos, and parodies that clutter search results.

#### **Step 1: Narrative Function Analysis**

The protocol begins by analyzing the *Scene Builder* requirements. It identifies the specific "Memetic Hook" required for the scene.

* **Reference:** "The Matrix Red Pill Scene."  
* **Strategic Goal:** "Pattern Interrupt / Setup for Reframe."  
* **Key Dialogue:** "You take the blue pill, the story ends."

#### **Step 2: Targeted Retrieval (The YouTube Scraper)**

The agent must find a clean, high-quality clip of the scene, avoiding 20-minute video essays *about* the scene. It constructs high-specificity queries using Boolean operators and duration filters.

* *Query:* "The Matrix red pill blue pill scene clip 4k \-commentary \-reaction"  
* *Filter:* Duration \< 4 minutes.  
* *Filter:* Upload Date \> 1 year (favors established, stable uploads).

#### **Step 3: Metadata & Transcript Verification**

Since the agent cannot "watch" a 5-minute video in real-time during a fast batch process, it uses text-based verification to confirm the content matches the request.

1. **Title Check:** Does the video title contain "Scene," "Clip," "Moment," or "4K"?  
2. **Transcript Scan:** The agent pulls the auto-generated transcript of the YouTube video. It searches for the specific dialogue line ("You take the blue pill").  
   * *If found:* It records the exact timestamp of that line.  
   * *If not found:* It discards the video as a likely mislabeled clip or music video.

#### **Step 4: Output Generation**

The E-Roll Hunter generates a **Precision Link Manifest**. Unlike D-Roll, it often provides links and timestamps rather than raw downloads to respect copyright and bandwidth.

* It updates 04\_assets/e\_roll/manifest.json.  
* It logs the Scene Code (HOOK-4), the Source (The Matrix), the YouTube URL, and most importantly, the **Start/End Timestamps** derived from the transcript scan.  
* This allows the editor to instantly navigate to the exact second required without scrubbing through footage.

---

### **5.4 Protocol C: The Prompt Architect (Generative Prep)**

Agent: The Prompt Engineer

File: agents/procurement/prompt\_engineer.md

Objective: To automate the creation of high-fidelity generative prompts. This protocol manages Track A (Generative Semiotics), ensuring that the AI-generated imagery is consistent, cinematic, and strictly adherent to the Brand Avatar.

The Prompt Architect is the bridge between the *Virtual Director's* vision and the *Image Generation Model's* latent space. It solves the problem of "Prompt Drift," where an AI character slowly changes appearance over the course of a video.

#### **Step 1: Consistency Injection (The DNA Merge)**

The core mechanism of this protocol is the merging of static identity with dynamic action. It treats the prompt as a composite object.

* **Input A:** brand\_avatar.json. Contains the immutable physical description of the client (e.g., "A 45-year-old man, bald with a grey beard, thick black glasses, wearing a navy turtleneck").  
* **Input B:** master\_storyboard.md. Contains the specific action for the scene (e.g., "Sitting on a park bench, looking at a bird, feeling peaceful").

The agent merges these inputs using a rigid syntax structure designed to lock the character's features. It places the physical description at the very start of the prompt (the "Subject Anchor") to weight it heavily in the generation process.

* *Merged Prompt:* "**\[Subject Anchor\]** A cinematic wide shot of a 45-year-old man, bald with a grey beard, thick black glasses, wearing a navy turtleneck. **\[Action\]** He is sitting on a wooden park bench, looking at a bird with a gentle smile. **\[Environment\]** Central Park in autumn, falling leaves. **\[Tech Specs\]** Soft golden hour lighting, shallow depth of field, Canon 50mm, Kodak Portra 400 \--ar 16:9 \--v 6.0"

#### **Step 2: Technical Formatting & Optimization**

The agent applies model-specific optimizations based on the current config.yaml settings.

* **Midjourney Optimization:** Appends parameters like \--stylize 250 (for artistic flair) or \--raw (for photographic realism). It calculates the correct aspect ratio (\--ar 9:16 for Reels, \--ar 16:9 for YouTube) based on the project settings.  
* **Z-Image Turbo Optimization:** Formats the prompt into the specific JSON structure required by API-based generators, separating "Positive Prompts" from "Negative Prompts" (e.g., "blurry, deformed hands, cartoon, illustration").

#### **Step 3: The Interpolation Prep (Start/End Frames)**

For scenes requiring video generation (via **Wan 2.2** for I2V or **Wan 2.1 One-to-All** for performance-driven animation), the agent generates **Paired Prompts**.

* It takes the base scene and creates two variations: a **Start Frame** and an **End Frame**.  
* *Start Prompt:* "...He is looking down at his hands, expression sad..."  
* *End Prompt:* "...He is looking up at the sky, expression hopeful..."  
* It ensures that every other variable (lighting, clothing, background) remains *identical* between the two prompts. This allows the video generation model to interpolate the movement between the two states without hallucinating a costume change.

---

### **5.5 Protocol D: The Cutter (A-Roll Extraction)**

Agent: The Cutter

File: agents/procurement/cutter.md

Objective: To automate the physical editing of the primary footage. This protocol turns the timestamps identified by the Premise Hunter into actual video files.

This is the bridge between "AI Analysis" and "Non-Linear Editing." While the other protocols hunt for external assets, this protocol mines the internal source material. It requires access to the raw, long-form video file (e.g., the full 60-minute interview) and uses FFmpeg for precise temporal slicing.

#### **Step 1: Timestamp Parsing & Validation**

The agent reads the final\_script.json generated by the Script Composer. It extracts the precise start and end timestamps for every quote in the script.

* **Validation:** It verifies the integrity of the timecodes (e.g., checking that Start Time \< End Time and that the duration matches the script estimate).  
* **Mapping:** It maps each clip to its narrative function (e.g., "Clip 1 \= Hook," "Clip 2 \= Setup"). This metadata will be used to name the files, keeping the edit organized.

#### **Step 2: The Cut Manifest Generation**

The agent generates a machine-readable cut\_jobs.json file. This file is a precise instruction set for the slicing engine, independent of any video editor.

* *Example Entry:*

| JSON{  "id": "clip\_01\_hook",  "start": "00:04:23.000",  "end": "00:04:35.000",  "source\_file": "inputs/raw\_interview.mp4",  "description": "HOOK: The shocking statement about failure"} |
| :---- |

#### **Step 3: FFmpeg Execution**

The system triggers a local Python script (tools/execute\_cuts.py) which wraps **FFmpeg**. This tool physically slices the source video file.

* **Precision Seeking:** It uses high-precision seeking flags (\-ss before \-i) to ensure the cut happens exactly on the requested frame, avoiding the "drift" common in simpler cutting tools.  
* **Re-Encoding:** It re-encodes the audio to a standard format (AAC 48kHz) to prevent sync issues in the editing software. It creates a new, clean video file for every single sentence in the script.  
* **Output:** It saves the individual MP4 clips into the 04\_assets/a\_roll/ directory (e.g., clip\_001\_hook.mp4, clip\_002\_setup.mp4).

#### **Step 4: XML Timeline Generation**

Finally, the agent generates an .xml file (FCPXML format) compatible with DaVinci Resolve and Premiere Pro.

* **The Result:** This file contains the timeline data. When the editor imports this file, the A-Roll clips are already placed in sequential order on Track 1\.  
* **Spacing:** It leaves calculated gaps between clips if the script indicates a "Sonic Vacuum" or a pure B-Roll transition. This effectively "pre-edits" the rough cut before the human editor even opens the software.

---

### **5.6 Automation Result: The Asset Manifest**

The ultimate result of Section 5 is the **Asset Manifest**. This JSON file is the proof of work. It transforms a folder of ideas into a folder of files. It tells the *Post-Super* agent (and the human editor) exactly what has been procured, where it lives, and how authentic it is.

**Structure of 05\_assembly/project\_handoff.json:**

| JSON{  "project\_id": "CMF\_001",  "sonic\_arc": "The Rally",  "assets": {    "track\_a\_generative": \[      {        "scene": "SCENE\_02\_SETUP",        "status": "PROMPTS\_READY",        "prompt\_file": "04\_assets/generative/midjourney\_prompts.txt",        "description": "Brand Avatar in dark room looking at laptop"      }    \],    "track\_b\_droll": \[      {        "scene": "CHALLENGE\_3",        "status": "DOWNLOADED",        "file\_path": "04\_assets/d\_roll/tired\_mom\_kitchen.mp4",        "source": "Pexels",        "vision\_score": 9.2,        "authenticity\_notes": "Pass: Grainy, bad lighting, genuine expression."      }    \],    "track\_c\_eroll": \[      {        "scene": "HOOK\_4",        "status": "LINKED",        "url": "https://youtube.com/watch?v=xyz123",        "timestamp\_start": "00:45",        "timestamp\_end": "00:49",        "cultural\_reference": "The Matrix Red Pill"      }    \],    "track\_d\_aroll": \[      {        "scene": "FULL\_NARRATIVE",        "status": "CUT\_COMPLETE",        "folder\_path": "04\_assets/a\_roll/",        "xml\_path": "05\_assembly/timeline\_import.xml"      }    \]  }} |
| :---- |

This architecture ensures that the **Asset Research and Assembly**—historically the most subjective and labor-intensive parts of production—are handled by the machine with objective rigor. The human editor opens their project folder to find the timeline pre-built, the music pre-selected, the B-roll pre-downloaded and sorted by authenticity, and the generative prompts written and ready. The "blank page" problem is solved. The editor simply begins to edit.

## **6\. The Master Commands & CLI Operations**

### **6.1 The CLI Philosophy: Director-Driven Code**

The Conscious Movie Factory is not designed to be operated through a chat window or a drag-and-drop dashboard. While conversational AI is powerful for brainstorming, it is catastrophic for production. In a high-velocity creative environment, "chatting" with your tools introduces latency, ambiguity, and drift. You cannot build a skyscraper by having a conversation with the crane; you must operate the controls.

Therefore, the CMF operates exclusively via a **Command Line Interface (CLI)**. This interface treats the entire movie production process—from the initial spark of a premise to the final gathering of assets—as a series of deterministic, executable functions. We do not "ask" the AI to work; we "command" the factory to produce.

This architecture implements a **"Director-Driven" Paradigm**. In standard software engineering, CLI commands are technical instructions (e.g., git push, npm install). In the CMF, commands are **Directorial Intentions**. When you type a command, you are not just running a script; you are activating a specialized department of your virtual studio.

* Instead of manually prompting an LLM to "find good music," you execute cmf-sonic. This single command wakes up the Musicologist, reviews the cultural profile of your audience, cross-references it with the emotional arc of your script, and generates a music cue sheet.  
* Instead of scrubbing through an hour-long video to find a specific quote, you execute cmf-cut. This triggers the automated editor to parse the script timestamps and physically slice the raw video file into usable clips.

The CLI acts as the "Executive Producer's Console." It creates a layer of abstraction that hides the immense complexity of the underlying agents (The Premise Hunter, The Cutter, The Vision Filter) while giving the human operator absolute strategic control. You define the *What* and the *Why*; the CLI handles the *How*. This ensures precision, reproducibility, and speed—turning a multi-day pre-production process into a 20-minute workflow.

---

### **6.2 The Safety Layer (cmf\_helpers.sh)**

Video production involves a fragile ecosystem of dependencies. A single "hallucinated" file path, a mismatched timestamp, or a forgotten character description can cause the entire production chain to collapse. Generic Large Language Models (LLMs) have "Goldfish Memory"—they often forget the constraints set five minutes ago.

To solve this, the CMF operates inside a rigid **Bash Safety Layer** defined by the cmf\_helpers.sh script. This script is the immune system of the factory. It wraps every interaction with the AI models to ensure strict data hygiene and context management. You do not run the factory without the safety layer.

**The Three Core Functions:**

1\. Context Scoping (The Blinders)

The Safety Layer enforces strict "Need-to-Know" protocols. It prevents Context Window Overflow and Logic Drift by ensuring agents only see the files required for their specific task.

* When you run cmf-sonic, the Safety Layer loads the *Script* and the *Tribe Soul*. It deliberately hides the *Visual Storyboard* because visual information is irrelevant to musical selection and would only confuse the model.  
* When you run cmf-cut, it loads the *Final Script* timestamps and the *Raw Video Metadata*, but hides the *Tribe Soul*, because cultural nuance is irrelevant to the physical act of cutting video frames.

2\. Atomic Writes (The Vault)

The Safety Layer prevents data corruption through "Atomic Writes." When an agent generates a file (like final\_script.json), it does not write directly to your hard drive.

* First, it writes to a temporary location (.tmp).  
* Second, the Safety Layer performs a syntax check. Is it valid JSON? Are all required fields present?  
* Only if the validation passes does it move the file to the live directory. This ensures that a network glitch or a model error never corrupts your project files.

3\. Session Injection (The Memory)

The Safety Layer automatically injects the config.yaml file into every prompt. This file contains the "Session Truth"—the client’s name, the industry, and the file paths. This means the human operator never has to copy-paste context. You never have to say, "Remember, we are writing for Sarah Chen." The system knows.

Initialization:

Before running any session, the operator must activate the layer. This "boots up" the factory.

| Bashsource \~/cmf/cmf\_helpers.shecho "🎬 CMF Safety Layer Active. Director on set." |
| :---- |

---

### **6.3 Command 1: Project Initialization (cmf-init)**

**Purpose:** To spawn a new production entity. In the CMF, a "Project" is not just a folder; it is a standardized database structure that will house every thought, asset, and decision related to a specific video.

**Syntax:**

| Bashcmf-init \--name="project\_id" \--transcript="path/to/audio.mp3" |
| :---- |

**The Automated Chain:**

1. **Structure Generation:** The system carves out the physical space for the project. It creates the root directory /output/project\_id/ and the standard five-phase subfolder architecture: 01\_narrative, 02\_sonic, 03\_storyboard, 04\_assets, and 05\_assembly.  
2. **Transcript Processing:** The system passes the raw audio file to Gemini 1.5 Pro (Long Context). It transcribes the audio into a timestamped Markdown file (transcript\_raw.md). Crucially, it formats timestamps in \[HH:MM:SS\] format to ensure downstream compatibility with the *Cutter* agent.  
3. **Soul Injection:** The system copies the client\_soul.json and tribe\_soul.json files from the central /intelligence/ vault into the project's input folder. This "locks" the identity of the video. Even if the central files change later, this project now has a permanent record of the soul it was born from.

**Success State:**

✅ Project \[project\_id\] initialized. Transcript processed. Soul injected. Ready for Narrative Extraction.

---

### **6.4 Command 2: Premise Mining (cmf-premise)**

**Purpose:** To execute **Phase 1.1** of the Narrative Core. This command triggers the *Premise Hunter* to scan the raw transcript for viral potential. It is the "Discovery" phase of the wizard.

**Syntax:**

| Bashcmf\-premise |
| :---- |

**The Automated Chain:**

1. **Ingestion:** The agent loads the transcript\_raw.md, the tribe\_soul.json, and the viral\_trinity\_scoring.yaml rubric.  
2. **Analysis:** It scans the text for "Viral Vectors." It looks for moments of high Surprise, Emotion, and Specificity. It ignores generic advice and hunts for stories, confessions, and contrarian takes.  
3. **Ranking:** It identifies 8 potential premises. It scores each one out of 60 points based on the Viral Trinity.  
4. **Output Generation:** It generates 01\_narrative/premise\_analysis.json. This file contains the 8 premises, their scores, and—crucially—a list of 16-24 verbatim quotes associated with each one.  
5. **Human Presentation:** The CLI displays a formatted summary of the top 3 premises to the user, including their Titles, Strategic Lanes (Heart/Mind/Community/Proof), and Viral Scores.

Director's Note:

This command does not make a final decision. It presents the options. It transforms the transcript from a wall of text into a menu of strategic choices.

---

### **6.5 Command 3: Narrative Assembly (cmf-compose)**

**Purpose:** To execute **Phase 1.2** of the Narrative Core. This command allows the human director to select the "Winning Premise" and triggers the *Script Composer* to assemble the narrative.

**Syntax:**

| Bashcmf-compose \--id=\[1-8\] |
| :---- |

* \--id: The number of the premise you wish to develop (from the list generated by cmf-premise).

**The Automated Chain:**

1. **Selection:** The system isolates the chosen premise from the premise\_analysis.json. It discards the unused premises to keep the context window clean.  
2. **The Verbatim Lock:** The *Script Composer* agent activates. It is fed *only* the quotes associated with the selected premise. It operates under a hard constraint: **"Zero New Text."** It cannot write; it can only arrange.  
3. **Assembly:** The agent arranges the selected quotes into the "Conscious Structure": Hook \-\> Setup \-\> Challenge \-\> Turning Point \-\> Resolution \-\> Close. It ensures the timestamps are preserved for every sentence.  
4. **Validation:** The agent performs a self-check. "Is this quote from the source? Is the pacing approximately 60 seconds?"  
5. **Output Generation:** It saves the 01\_narrative/final\_script.json. This file is the "Locked Narrative." It contains the sequence of quotes, their timestamps, and their narrative function tags.

**Success State:**

✅ Narrative Assembled. Script locked for Premise \#\[ID\]. Ready for Blueprinting.

---

### **6.6 Command 4: Production Blueprinting (cmf-blueprint)**

**Purpose:** To execute **Phase 1.3** of the Narrative Core. This command translates the text script into a machine-readable production plan. It creates the "God Object" that controls the rest of the factory.

**Syntax:**

| Bashcmf\-blueprint |
| :---- |

**The Automated Chain:**

1. **Ingestion:** The *Blueprint Architect* loads the final\_script.json, the sonic\_story\_arcs.yaml, and the scene\_builder\_library.yaml.  
2. **Sonic Mapping:** The agent analyzes the emotional arc of the script. It assigns the definitive **Sonic Arc** (e.g., "The Rally") that matches the journey. This dictates the BPM and energy curve for the rest of production.  
3. **Visual Mapping:** The agent deconstructs the script into 4-8 scenes. For each scene, it assigns a specific **Scene Template** code (e.g., HOOK-4, CHALLENGE-3). It calculates the Cognitive Load Score (CLS) to ensure the visual rhythm isn't too overwhelming or too boring.  
4. **Output Generation:** It generates 01\_narrative/production\_blueprint.json. This file is the master instruction set. It tells the Sonic team what music to make, the Visual team what images to generate, and the Procurement team what clips to find.

Director's Note:

This is the pivot point of the system. Once this command is run, the "Creative" phase is largely complete. The subsequent commands are "Execution" phases that run autonomously based on the instructions in the Blueprint.

---

### **6.7 Command 5: Audio Architecture (cmf-sonic)**

**Purpose:** To generate the "Sonic Soul." This command builds the auditory landscape before a single visual asset is procured.

**Syntax:**

| Bashcmf\-sonic |
| :---- |

**The Automated Chain:**

1. **Genre Selection:** The *Sonic Sommelier* reads the Blueprint and the Tribe Soul. It selects a "Sonic Vintage" that matches the audience's taste (e.g., "Lo-Fi Chill" for a focus-oriented tribe, "Epic Orchestral" for a motivation-oriented tribe).  
2. **Composition:** The *Sonic Scribe* translates the Blueprint into a **Suno.ai Prompt**. It maps the script sections to song structures (Scene 1 \= Intro, Scene 3 \= Pre-Chorus). It embeds directorial notes to ensure the music swells and drops at the exact timestamps defined in the Blueprint.  
3. **Subconscious Layering:** The *Ad-Lib Amplifier* scans the script for opportunities to add "invisible audio." It generates manifests for "Dog Whispers" (internal thoughts) and "Cultural Echoes" (external quotes) to be layered into the mix.  
4. **Output Generation:** It creates 02\_sonic/sonic\_bible.json, containing the music prompts, SFX lists, and ad-lib scripts.

---

### **6.8 Command 6: The Cutter (cmf-cut)**

**Purpose:** To execute the **"Raw-to-Edit" Pipeline**. This command bridges the gap between the abstract script and the physical media file. It physically slices the raw source video into the A-Roll clips defined by the script timestamps.

**Syntax:**

| Bashcmf\-cut \--source="inputs/raw\_video.mp4" |
| :---- |

* \--source: The file path to the original, long-form video or audio recording from which the script was extracted.

**The Automated Chain:**

**1\. Script Parsing (The Logic)**

* The **Cutter Agent** activates. It reads the 01\_narrative/final\_script.json generated by the *Script Composer*.  
* It extracts the precise source\_timestamp start and end points for every quote in the script.  
* It verifies timestamp integrity (e.g., ensuring Start Time \< End Time and checking for overlap).  
* It maps each clip to its narrative function (e.g., "Clip 1 \= Hook," "Clip 2 \= Setup") to ensure the files are named meaningfully.

**2\. Manifest Generation (The Instruction)**

* The agent compiles a machine-readable cut\_jobs.json file. This serves as the "Cutting List" for the Python tool.  
* *Example Entry:*

| JSON{  "id": "clip\_01\_hook",  "start": "00:04:23.000",  "end": "00:04:35.000",  "source\_file": "inputs/raw\_video.mp4",  "description": "HOOK: The shocking statement about failure"} |
| :---- |

**3\. FFmpeg Execution (The Surgery)**

* The system triggers the local Python script (tools/execute\_cuts.py). This script wraps **FFmpeg**, the industry-standard multimedia framework.  
* **Precision Seeking:** It uses high-precision seeking flags (\-ss placed *before* \-i) to ensure the cut happens exactly on the requested frame, avoiding the "drift" common in simpler cutting tools.  
* **Audio Re-Encoding:** It re-encodes the audio to a standard format (AAC 48kHz) to prevent sync issues in the editing software, ensuring the timeline is rock-solid.  
* **Physical Output:** It saves the individual MP4 clips into the 04\_assets/a\_roll/ directory (e.g., clip\_001\_hook.mp4, clip\_002\_setup.mp4).

**4\. XML Timeline Generation (The Handoff)**

* Finally, the agent generates an .xml file (FCPXML format) compatible with DaVinci Resolve and Premiere Pro.  
* **The Result:** This file contains the timeline data. When the editor imports this file, the A-Roll clips are already placed in sequential order on Track 1\.  
* **Smart Spacing:** It leaves calculated gaps between clips if the script indicates a "Sonic Vacuum" or a pure B-Roll transition. This effectively "pre-edits" the rough cut before the human editor even opens the software.

**Success State:**

✅ Cuts Complete. 6 Clips extracted to 04\_assets/a\_roll/. XML Timeline generated.

---

### **6.9 Command 7: Visual Architecture (cmf-visual)**

**Purpose:** To generate the "Generative Semiotics" (Track A). This command creates the AI-generated imagery that represents the internal story or metaphor.

**Syntax:**

| Bashcmf\-visual |
| :---- |

**The Automated Chain:**

1. **Avatar Consistency:** The *Brand Avatar Architect* loads the client profile and generates 03\_storyboard/brand\_avatar.json. This file contains the "Anchor Prompts" for the client at various life stages, ensuring visual consistency.  
2. **Shot Construction:** The *Virtual Director* reads the production\_blueprint.json. For every scene tagged as "Generative," it writes a detailed shot description.  
3. **Paired Keyframing:** It generates two prompts for every shot: a **Start Frame** and an **End Frame**. This prepares the assets for video interpolation.  
4. **Prompt Engineering:** The *Prompt Engineer* formats these descriptions into optimized Midjourney/Flux prompts, injecting the Brand Avatar DNA into each one.  
5. **Output Generation:** It saves the ready-to-run prompts to 03\_storyboard/production\_config.json.

---

### **6.10 Command 8: The Automated Hunt (cmf-hunt)**

**Purpose:** To execute the **"Search-Vision-Select"** loop for Research Assets (Tracks B and C). This is the heavy lifting of the factory.

**Syntax:**

| Bashcmf-hunt \--track=\[all|droll|eroll\] \--strictness=\[high|med|low\] |
| :---- |

* \--track: Specifies whether to hunt for D-Roll (Authentic), E-Roll (Cultural), or both.  
* \--strictness: Controls the Vision Filter threshold. High \= \>8/10 score required. Low \= \>6/10.

**The Automated Chain:**

1. **Track B (D-Roll):**  
   * The agent reads the "Observable Scenarios" from the Blueprint.  
   * It generates multi-vector search queries.  
   * It fetches thumbnails from stock/web APIs.  
   * It passes thumbnails to **Gemini Vision** to score them on "Authenticity" and "Demographic Match."  
   * It downloads the winners to 04\_assets/d\_roll/.  
2. **Track C (E-Roll):**  
   * The agent reads the "Cultural References" from the Blueprint.  
   * It searches YouTube for the specific clips.  
   * It verifies the content using metadata and transcripts.  
   * It saves the URLs and timestamps to 04\_assets/e\_roll/manifest.json.

**Success State:**

✅ Hunt Complete. 12 Assets Procured. 84 Candidates Rejected.

---

### **6.11 Command 9: Final Assembly (cmf-assemble)**

**Purpose:** To package the chaos into order. This command executes the role of the *Post-Supervisor*, preparing the final handoff for the editor.

**Syntax:**

| Bashcmf\-assemble |
| :---- |

**The Automated Chain:**

1. **Asset Verification:** The system scans the /04\_assets/ directory. It verifies that every scene in the Blueprint has a corresponding file (A-Roll, D-Roll, or Generative) and that the Music file exists.  
2. **Effect Coding:** It reads the *Scene Builder* mapping in the Blueprint and appends the specific CapCut Effect Codes (e.g., EFFECT-TR-01) to the metadata.  
3. **XML Updates:** It updates the DaVinci Resolve XML to include tracks for B-Roll and Music (if locally available), synchronized to the A-Roll timeline.  
4. **Manifest Creation:** It compiles the 05\_assembly/project\_handoff.json, a master file linking every second of the video to its constituent parts.

**Success State:**

✅ Project Assembled. Handoff Package ready in 05\_assembly/.

---

### **6.12 Troubleshooting & Error Handling**

The CLI includes robust error handling to guide the operator through the complex dependency chain.

**Error: \[400\_NO\_PREMISE\_SELECTED\]**

* **Cause:** You tried to run cmf-compose without specifying an ID.  
* **Fix:** Run cmf-compose \--id=X with a valid premise number from the analysis file.

**Error: \[403\_VERBATIM\_VIOLATION\]**

* **Cause:** The *Script Composer* attempted to invent a sentence that did not exist in the source text.  
* **Fix:** The Safety Layer blocked the write. The system will auto-retry with a stricter prompt. If it fails twice, it will request human intervention to approve or reject the text.

**Error: \[404\_SONIC\_MISSING\]**

* **Cause:** You tried to run cmf-visual or cmf-hunt before the Blueprint was generated.  
* **Fix:** The workflow is linear. You must run cmf-blueprint first to define the scenes.

**Error: \[409\_TIMESTAMP\_MISMATCH\]**

* **Cause:** The *Cutter* detected that a start time is after the end time, or a timestamp does not exist in the source video duration.  
* **Fix:** Manually check the final\_script.json timestamps against the source video file and correct the error.

**Error: \[500\_VISION\_REJECT\]**

* **Cause:** The Asset Hunter could not find any images that met the "Authenticity Threshold" (usually \>8/10).  
* **Fix:** Run cmf-hunt \--track=droll \--strictness=low to lower the threshold to 6/10, or manually refine the "Observable Scenario" description in the Blueprint to be less specific.

This suite of commands transforms the role of the creator. You are no longer a laborer dragging clips onto a timeline. You are a Commander, issuing strategic orders to a fleet of specialized agents who execute your vision with speed, precision, and soul. 

## **7\. Installation & Implementation (The Physical Manifest)**

### **7.1 From Theory to Machinery: The "Raw-to-Edit" Upgrade**

We have defined the philosophy. We have mapped the architecture. We have registered the workforce. But the factory does not exist yet. It is currently just a concept, a ghost in the machine. To bring the Conscious Movie Factory (CMF) to life, we must move from architectural theory to physical construction.

This implementation guide is different from previous versions because it now includes the **Mechanical Room**—the set of Python tools and FFmpeg wrappers that allow the AI to reach out and physically touch your video files.

The CMF is no longer just a text generator; with the integration of the **Automated Cutter**, it is now a video processing engine. This introduces a new layer of complexity. You are not just managing prompts; you are managing binaries, file paths, and rendering engines. The system must be built with absolute precision, or the "Cutter" will slice the wrong frames, the "Hunter" will download the wrong assets, and the "Assembler" will fail to build the timeline.

This section provides the definitive, uncompromising **Implementation Guide**. It lists every directory you must carve out, every file you must populate, every script you must write, and the exact configuration required to bring this sophisticated machinery online. This is your blueprint for building the engine that turns raw transcripts into edited timelines.

---

### **7.2 Step 1: The Factory Floor (Directory Structure)**

The first step in physical construction is defining the space. We must carve out the digital territory where the factory lives. You cannot manage a complex production pipeline in a single folder; you need a rigid hierarchy that separates **Logic** (Agents), **Knowledge** (Intelligence), **Inputs** (Raw Material), **Tools** (Execution Scripts), and **Outputs** (Products).

The structure has been specifically updated to include the tools/ directory for our new Python scripts and the a\_roll/ asset folder for the sliced video clips.

Execution:

Run this block in your terminal to initialize the skeleton. Do not use a GUI; use the CLI to ensure permissions and hierarchy are perfect.

| Bash\# 1\. Create Root Directorymkdir \-p \~/cmf\# 2\. Create The Brain (Intelligence)\# Stores the static frameworks the agents referencemkdir \-p \~/cmf/intelligence/{frameworks,lexicons,recipes}mkdir \-p \~/cmf/intelligence/recipes/scene\_recipes\# 3\. Create The Workforce (Agents)mkdir \-p \~/cmf/agents/\_master              \# Orchestrators (Producer, Architect, Post-Super)mkdir \-p \~/cmf/agents/extraction           \# Hunter, Composer, Extractorsmkdir \-p \~/cmf/agents/sonic                \# Sommelier, Scribe, Ad-Libbermkdir \-p \~/cmf/agents/visual               \# Virtual Director, Scene Builder, Metaphor Directormkdir \-p \~/cmf/agents/procurement          \# Asset Hunters, Cutter, Prompt Engineermkdir \-p \~/cmf/agents/validation           \# Critic, Audiophile, Continuity Supervisor\# 4\. Create The Mechanical Room (NEW)\# Stores the Python scripts for physical file manipulationmkdir \-p \~/cmf/tools\# 5\. Create The Inputs (Raw Material)mkdir \-p \~/cmf/inputs/transcripts          \# Raw text filesmkdir \-p \~/cmf/inputs/raw\_video            \# Raw source video files for cuttingmkdir \-p \~/cmf/inputs/ccf\_import           \# The umbilical cord to the CCF Soul\# 6\. Create The Outputs (Production Floor)\# Organized by project IDsmkdir \-p \~/cmf/output\# 7\. Create The Logsmkdir \-p \~/cmf/logs |
| :---- |

---

### **7.3 Step 2: The "Laws of Physics" (Intelligence Assets)**

The agents are useless without knowledge. If you deploy the *Cutter Agent* without teaching it how to format a timestamp, it will fail. If you deploy the *Blueprint Architect* without a library of Scene Types, it will hallucinate impossible shots.

You must populate the /intelligence/ folder with the static frameworks that define *how* the CMF thinks. You need to create these **5 Critical Files**.

#### **File 1: intelligence/frameworks/viral\_trinity\_scoring.yaml**

* **Purpose:** This is the rubric used by the **Premise Hunter** to rank stories. It defines exactly what "Good" looks like.  
* **Action:** Extract the "60-Point Scoring System" from *The Premise Hunter* document.  
* **Content:** Detailed definitions for "Surprise Factor," "Emotional Intensity," "Specificity," and "Universal Appeal."

#### **File 2: intelligence/frameworks/sonic\_story\_arcs.yaml**

* **Purpose:** Defines the 12 Sonic Arcs. It is the bridge between emotion and rhythm.  
* **Action:** Copy the content from **Section 3 (The 12 Arcs)** of your *Sonic Story Arc Library* document.  
* **Crucial Detail:** Include the BPM curve and "Sonic Vacuum" timestamps. The *Cutter* uses this to know where to leave gaps in the A-Roll for dramatic silence.

#### **File 3: intelligence/frameworks/scene\_builder\_library.yaml**

* **Purpose:** The "Menu" of 18 Scene Types available to the *Blueprint Architect*.  
* **Action:** Copy the definitions from *The Conscious Scene Builder*.  
* **Crucial:** Include the **Cognitive Load Score (CLS)** for each scene.

#### **File 4: intelligence/frameworks/visual\_hooks\_recipes.yaml**

* **Purpose:** Defines the "Prop-Driven Metaphors" (e.g., "The Heavy Backpack Drop") used to visualize abstract concepts.  
* **Action:** Copy the recipes from your *Visual Hooks Recipes* document.

#### **File 5: intelligence/frameworks/master\_effects.yaml**

* **Purpose:** Defines the specific CapCut codes (e.g., EFFECT-C-04).  
* **Action:** Copy the effect codes from your *Master Effects Library*. This allows the *Post-Supervisor* to pass technical instructions to the human editor.

---

### **7.4 Step 3: The Session Truth (config.yaml)**

This is the single source of truth for the factory. It tells the agents who the client is, where the files are, and which AI models to use. With the new integration, we must add paths for the **Raw Video Inputs** and the **Tools Directory**.

**Create File:** \~/cmf/config.yaml

| YAML\# \============================================================================\# CMF MASTER CONFIGURATION (v3.0 \- Raw-to-Edit Edition)\# \============================================================================\# 1\. CLIENT IDENTITY (Inherited from CCF)client:  name: "Sarah Chen"                 industry: "Real Estate"  voice\_baseline: "TTT-03"         \# From CCF Soul\# 2\. FILE PATHS (The Nervous System)paths:  root: "\~/cmf"  \# Inputs  ccf\_client\_soul: "\~/ccf/output/setup/03\_client\_soul.json"  ccf\_tribe\_soul: "\~/ccf/output/setup/04\_tribe\_soul.json"  raw\_video\_source: "\~/cmf/inputs/raw\_video/source\_master.mp4" \# Default source    \# Tools (The Mechanical Room)  tools\_dir: "\~/cmf/tools"  cutter\_script: "\~/cmf/tools/execute\_cuts.py"  xml\_script: "\~/cmf/tools/xml\_generator.py"  \# Intelligence Assets  viral\_scoring: "intelligence/frameworks/viral\_trinity\_scoring.yaml"  sonic\_arcs: "intelligence/frameworks/sonic\_story\_arcs.yaml"  scene\_library: "intelligence/frameworks/scene\_builder\_library.yaml"\# 3\. AI MODELS (The Engines)models:  reasoning: "gemini-3-pro-preview" \# For Premise Hunter & Architect  creative: "gemini-3-pro-preview"  \# For Script Composer  vision: "gemini-pro-vision"       \# For Asset Filtering  generation: "midjourney-v6"       \# For A-Roll Prompts\# 4\. PROCUREMENT & CUTTING SETTINGSprocurement:  d\_roll\_threshold: 8.0            \# Min Authenticity Score (0-10)  max\_search\_results: 20           \# Images to scan per scenecutting:  ffmpeg\_path: "/usr/bin/ffmpeg"   \# Path to FFmpeg binary  audio\_sample\_rate: "48000"       \# Standard for video editing  video\_codec: "libx264"           \# Standard H.264\# 5\. FEATURE FLAGSfeatures:  enable\_vision\_filter: true         enable\_voice\_cloning: true         force\_verbatim\_mode: true        \# Forbids AI from inventing text  enable\_auto\_cut: true            \# Enables the FFmpeg slicing module |
| :---- |

---

### **7.5 Step 4: The Safety Layer (cmf\_helpers.sh)**

We must update the helper script to handle the new **Cutting Context**. The Cutter agent needs to see the script timestamps and the raw video metadata (duration, framerate), but it does not need to see the Tribe Soul or Sonic Arcs. This "Need-to-Know" scoping prevents the agent from getting confused by irrelevant data.

**Create/Update File:** \~/cmf/cmf\_helpers.sh

| Bash\#\!/bin/bash\# CMF CONTEXT LOADER\# Usage: build\_cmf\_context "phase\_name" "project\_id"build\_cmf\_context() {    local phase="$1"    local pid="$2"        echo "--- SYSTEM CONFIG \---"    cat \~/cmf/config.yaml        case "$phase" in        "hunter")            \# Context: Raw Data \+ Scoring Logic            echo "--- TRIBE SOUL \---"            cat $(yq '.paths.ccf\_tribe\_soul' \~/cmf/config.yaml)            echo "--- SCORING RUBRIC \---"            cat \~/cmf/intelligence/frameworks/viral\_trinity\_scoring.yaml            echo "--- RAW TRANSCRIPT \---"            cat \~/cmf/inputs/transcripts/"$pid".txt            ;;                    "composer")            \# Context: The Winning Idea            echo "--- PREMISE ANALYSIS \---"            cat \~/cmf/output/"$pid"/01\_narrative/premise\_analysis.json            ;;                    "architect")            \# Context: The Script \+ Production Constraints            echo "--- FINAL SCRIPT \---"            cat \~/cmf/output/"$pid"/01\_narrative/final\_script.json            echo "--- SCENE LIBRARY \---"            cat \~/cmf/intelligence/frameworks/scene\_builder\_library.yaml            echo "--- SONIC ARCS \---"            cat \~/cmf/intelligence/frameworks/sonic\_story\_arcs.yaml            ;;        "cutter")            \# Context: Script Timestamps \+ Video Specs            \# The Cutter only needs to know WHERE to cut and WHAT to cut.            echo "--- FINAL SCRIPT \---"            cat \~/cmf/output/"$pid"/01\_narrative/final\_script.json            echo "--- RAW VIDEO METADATA \---"            \# We assume ffprobe has run or metadata is manually logged            echo "Source File: inputs/raw\_video/source\_master.mp4"            ;;                    "visual")            \# Context: The Blueprint \+ Visual Recipes            echo "--- PRODUCTION BLUEPRINT \---"            cat \~/cmf/output/"$pid"/01\_narrative/production\_blueprint.json            echo "--- VISUAL RECIPES \---"            cat \~/cmf/intelligence/frameworks/visual\_hooks\_recipes.yaml            echo "--- BRAND AVATAR \---"            cat \~/cmf/output/"$pid"/03\_storyboard/brand\_avatar.json            ;;    esac} |
| :---- |

---

### **7.6 Step 5: The Mechanical Room (Tools & Scripts)**

This is the new addition. You must populate the \~/cmf/tools/ directory with the Python scripts that perform the actual file manipulation. These scripts are the hands of the factory.

#### **Tool 1: tools/execute\_cuts.py**

* **Purpose:** This script wraps FFmpeg to physically slice the raw video file based on the JSON manifest provided by the Cutter Agent.  
* **Action:** Create this file and paste the Python code derived from the "Gemini CLI \+ DaVinci Resolve" document (see Section 5.5). Ensure it includes the logic for subprocess.run calling FFmpeg with re-encoding parameters (\-c:v libx264, \-c:a aac).

#### **Tool 2: tools/xml\_generator.py**

* **Purpose:** This script takes the list of cut clips and generates an .xml file (FCP7 format) that can be imported into DaVinci Resolve or Premiere Pro.  
* **Action:** Create this file. It should contain the logic to write the \<sequence\>, \<media\>, and \<clipitem\> tags, placing the A-Roll clips sequentially on the timeline with the correct frame rates and duration.

---

### **7.7 Step 6: The Agent Workforce (Population)**

Now we populate the agents. We must ensure the **Cutter** is present in the Procurement team, alongside the Narrative Core and the Asset Hunters.

**Folder: agents/\_master/**

1. cmf\_producer.md (State Manager)  
2. blueprint\_architect.md (Production Planner)  
3. post\_super.md (Final Assembly)

| Folder: agents/extraction/4\. premise\_hunter.md (Strategic Analyst)5\. script\_composer.md (Verbatim Architect)6\. resonance\_extractor.md (Heart Specialist)7\. authority\_extractor.md (Mind Specialist)8\. connection\_extractor.md (Community Specialist)9\. testimonial\_architect.md (Proof Specialist)Folder: agents/sonic/10\. sommelier.md (Music Selection)11\. scribe.md (Suno Prompting)12\. ad*\_lib\_*amplifier.md (Subconscious Audio)Folder: agents/visual/13\. avatar\_architect.md (Character Design)14\. virtual\_director.md (Storyboard Design)15\. scene\_builder.md (Recipe Lookup)16\. metaphor\_director.md (Prop Design)Folder: agents/procurement/17\. prompt\_engineer.md (Midjourney Formatting)18\. asset*\_hunter\_*droll.md (Authentic Search)19\. asset*\_hunter\_*eroll.md (Cultural Search)20\. cutter.md (A-Roll Slicing) \[NEW\]\* Role: Technical Editor.\* Task: Parse final*\_script.json timestamps, generate cut\_*jobs.json, trigger execute\_cuts.py.Folder: agents/validation/21\. critic.md (Narrative QA)22\. audiophile.md (Sonic QA)23\. continuity\_supervisor.md (Visual QA) |
| :---- |

---

### **7.8 Step 7: The Execution Flow (The "First Light")**

You have built the factory. Now you turn it on. Here is the exact sequence to run your first automated production using the fully integrated **Raw-to-Edit** workflow.

**Phase A: Mining the Gold**

* **Command:** cmf-premise  
* **Action:** The *Premise Hunter* reads the transcript. It presents the Top 8 Premises.  
* **Human Decision:** "Premise \#3 is the one."

**Phase B: Assembling the Narrative**

* **Command:** cmf-compose \--id=3  
* **Action:** The *Script Composer* assembles the verbatim script. The text is locked.

**Phase C: Architecting the Production**

* **Command:** cmf-blueprint  
* **Action:** The *Blueprint Architect* maps the Sonic Arc and Scene Types.

**Phase D: The Physical Cut (The New Step)**

* **Command:** cmf-cut \--source="inputs/raw\_video.mp4"  
* **Action:** The *Cutter Agent* reads the script timestamps. It triggers FFmpeg. It slices the raw video into 6-8 clips in 04\_assets/a\_roll/. It generates the XML timeline.

**Phase E: The Asset Hunt (Parallel)**

* **Command:** cmf-sonic (Generates Music)  
* **Command:** cmf-visual (Generates Visual Prompts)  
* **Command:** cmf-hunt (Finds B-Roll)

**Phase F: Final Assembly**

* **Command:** cmf-assemble  
* **Action:** The *Post-Super* verifies all files and packages the project.

---

### **7.9 Final Verification Checklist**

To confirm your system is ready for the **Automated Cutter Integration**, verify these specific files exist in your structure:

* \[ \] **tools/execute\_cuts.py** contains the FFmpeg logic.  
* \[ \] **tools/xml\_generator.py** contains the XML logic.  
* \[ \] **agents/procurement/cutter.md** contains the agent persona.  
* \[ \] **config.yaml** has the cutting block and raw\_video\_source path defined.  
* \[ \] **cmf\_helpers.sh** includes the cutter context in the loader.  
* \[ \] **inputs/raw\_video/** contains a test video file to work with.

You have now successfully integrated the physical machinery of video editing into the intellectual architecture of the CMF. You are ready to produce.