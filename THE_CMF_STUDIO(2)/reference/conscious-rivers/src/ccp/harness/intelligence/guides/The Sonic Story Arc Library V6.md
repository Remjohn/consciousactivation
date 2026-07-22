# **The Sonic Story Arc Library (V7 — CMF 2.0 + Suno AI Edition)**

### **Introduction: The Emotional Blueprints**

This library contains the 12 master "Sonic Story Arc" templates that form the emotional foundation of every video produced by the **CONSCIOUS MOVIE FACTORY 2.0**. This V7 revision updates the library for integration with:

- **Suno AI** for music stem generation
- **MoviePy** for assembly (Stage 6)
- **`audio_effects_library/`** for programmatic audio processing

> **🔄 System Change (V7):** Music stems are now generated via **Suno AI API** rather than sourced from Epidemic Sound. The `sonic_arc_engine.py` module provides prompts and per-phase configurations. All audio assembly happens in MoviePy during Stage 6.

---

### **The Professional Audio Track Layout**

This is the standard 10-track audio layout for all Sonic Arc timeline templates. It prioritizes dialogue, then sound effects, then atmospheric layers, and finally the full musical score broken down into stems.

| Track | Role | Priority | Source |
|-------|------|----------|--------|
| **A1** | VO | 1 (highest) | DeepFilterNet processed |
| **A2** | Diegetic | 5 | B-Roll natural sounds |
| **A3** | Hits & Impacts | 2 | `SFX_Library/Hits_And_Impacts/` |
| **A4** | Risers & Swells | 4 | `SFX_Library/Risers_And_Swells/` |
| **A5** | Ambience & Drones | 6 | `SFX_Library/Drones_And_Ambience/` |
| **A6** | Music - BASS | 7 | Suno AI stem (Demucs separated) |
| **A7** | Music - DRUMS | 7 | Suno AI stem (Demucs separated) |
| **A8** | Music - MELODY/PADS | 7 | Suno AI stem (Demucs separated) |
| **A9** | Music - INSTRUMENT 1 | 7 | Suno AI stem |
| **A10** | Music - INSTRUMENT 2 / VOCALS | 7 | Suno AI stem |

**MoviePy Processing Rules:**
- A1 (VO) triggers **auto-ducking** of tracks A6-A10
- A3 (Hits) get **sidechain priority** over A5-A10
- Micro-fades (10ms) applied at all cut points via Semantic Slicing

---

### **Music Generation via Suno AI**

Instead of sourcing from Epidemic Sound, music is now generated per-project using Suno AI:

```python
from audio_effects_library.suno_integration import SunoStemManager

suno = SunoStemManager(api_key="your-key")
stems = suno.get_stems_for_phase(
    sonic_arc="breakthrough",
    phase="resolution",
    duration=30
)
```

**Suno Prompt Generation:**
Each arc phase maps to a Suno prompt combining:
- Emotional keywords from the arc
- Instrumentation hints (stems to include)
- Duration and style modifiers

---

### **The Final 12 Sonic Arcs**

---

#### **1. The Core Transformation**

* **Core Emotional Journey:** Intrigue → Vulnerability → Struggle/Realization → Empowerment
* **Best For:** The quintessential coaching story: Hook → Personal Low → Challenge/Shift → Insight.
* **Suno Keywords:** Pop, Acoustic, Cinematic, Pensive, Hopeful, Determined

| Story Phase | Music Stems (A6-A10) | Ambience & Drones (A5) | SFX (A3-A4) |
|-------------|----------------------|------------------------|-------------|
| **Intrigue (Hook)** | A sparse, questioning INSTRUMENT 1 (piano/guitar melody) | Neutral `SFX_Ambience_EmptyRoom` or soft ambient pad | Subtle `Reversed_Whoosh` leading into hook |
| **Vulnerability (Personal Low)** | Low, solitary BASS line or soft PADS. Melody drops out. | Cold `SFX_Drone_Hollow` for isolation feeling | None. Emptiness is intentional. |
| **Struggle/Realization (Shift)** | DRUMS enter with focused rhythm. BASS becomes determined. | Neutral ambience, drone clears | `Riser` into section + clean `SFX_Click` for "aha!" |
| **Empowerment (Insight)** | Full arrangement: MELODY returns over full band | Warm `SFX_Ambient_Pad` for confidence | `SFX_Sparkle` or `SFX_Chime_Bright` accents |

---

#### **2. The Breakthrough**

* **Core Emotional Journey:** Anxiety → Struggle → Epiphany → Empowerment
* **Best For:** Overcoming oppressive problems (burnout, self-doubt, fear).
* **Suno Keywords:** Pop, Beats, Electronic, Hopeful, Uplifting, Dreamy

| Story Phase | Music Stems (A6-A10) | Ambience & Drones (A5) | SFX (A3-A4) |
|-------------|----------------------|------------------------|-------------|
| **Anxiety (Hook & Setup)** | BASS only: low, repetitive, oppressive heartbeat | Deep `SFX_DRONE_Tension_SubBass` for unease | Sharp `Impact_Thud` or glitch on hook |
| **Struggle (Challenge)** | DRUMS enter: tense, driving. BASS continues. No melody. | Drone increases volume, slight distortion | Frequent `Riser` builds + sharp hits |
| **Epiphany (Turning Point)** | **CRITICAL:** Complete SILENCE for 1-2 seconds | Silence creates vacuum for clarity | Single `Impact_BellChime` releases tension |
| **Empowerment (Resolution)** | Full, powerful arrangement enters | Oppressive drone GONE. Warm high-freq pad. | `SFX_Whoosh` + `SFX_Sparkle` celebration |

---

#### **3. The Quiet Reflection**

* **Core Emotional Journey:** Nostalgia → Confusion → Acceptance → Peace
* **Best For:** Imposter syndrome, self-worth, reframing the past.
* **Suno Keywords:** Acoustic, Ambient, Lofi, Pensive, Introspective, Nostalgic

| Story Phase | Music Stems (A6-A10) | Ambience & Drones (A5) | SFX (A3-A4) |
|-------------|----------------------|------------------------|-------------|
| **Nostalgia (Hook & Setup)** | MELODY (soft piano/guitar) + PADS. No drums. | Warm `SFX_Vinyl_Crackle` + gentle room tone | None. Soft audio crossfades. |
| **Confusion (Challenge)** | Main MELODY fades. Dissonant INSTRUMENT 2 enters. | Cold `SFX_Drone_Hollow` or wind noise | Slow, subtle low-freq risers |
| **Acceptance (Turning Point)** | MELODY returns clean over PADS | Clean silence for lesson to land | Soft `Piano Chord Hit` or reversed cymbal |
| **Peace (Resolution)** | Full gentle arrangement with breathing room | Warm `SFX_Vinyl_Crackle` or high-end pad | None. Uncluttered, peaceful. |

---

#### **4. The Confrontation**

* **Core Emotional Journey:** Frustration → Debate → Clarity → Confidence
* **Best For:** Guru takedowns, contrarian points of view.
* **Suno Keywords:** Hip Hop, Electronic, Beats, Confident, Bold, Edgy

| Story Phase | Music Stems (A6-A10) | Ambience & Drones (A5) | SFX (A3-A4) |
|-------------|----------------------|------------------------|-------------|
| **Frustration (Hook & Setup)** | BASS only: distorted, aggressive, sputtering | `SFX_Drone_ElectricalHum` for irritation | Sharp glitch or static burst |
| **Debate (Challenge)** | DRUMS enter: "call and response" rhythm | Pulsing drone matching debate pace | `SFX_Whoosh_Fast` on every edit cut |
| **Clarity (Turning Point)** | BASS becomes clean, less distorted | Clean, confident silence | `SFX_Click` or `Impact_Smash` dismissal |
| **Confidence (Resolution)** | Cool, sparse: clean BASS, simple DRUMS, INSTRUMENT 1 | Clean, powerful, uncluttered | None. Confidence from lack of noise. |

---

#### **5. The Comedic Reframe**

* **Core Emotional Journey:** Normalcy → Absurd Twist → Ironic Laugh → Relief
* **Best For:** Busting myths, humor-based connection.
* **Suno Keywords:** Comedy, Pop, Acoustic, Quirky, Playful, Mischievous

| Story Phase | Music Stems (A6-A10) | Ambience & Drones (A5) | SFX (A3-A4) |
|-------------|----------------------|------------------------|-------------|
| **Normalcy (Hook & Setup)** | Full "corporate" stock music feel | Clean, standard room tone | None. |
| **Absurd Twist (Challenge)** | Music continues unchanged (dramatic irony) | Normal ambience continues | None. Humor from sound mismatch. |
| **Ironic Laugh (Turning Point)** | **CRITICAL:** Music stops with RECORD SCRATCH | Awkward silence after scratch | `Record_Scratch` + cartoon `SFX_Boink` |
| **Relief (Resolution)** | Quirky track: pizzicato + tuba/upright bass | Light, airy ambience | Subtle chimes or pops |

---

#### **6. The Divine Spark**

* **Core Emotional Journey:** Emptiness → Surrender → Receiving Grace → Renewed Purpose
* **Best For:** Spiritual themes, hope after darkness, healing.
* **Suno Keywords:** Ambient, Spiritual, Cinematic, Ethereal, Peaceful, Healing

| Story Phase | Music Stems (A6-A10) | Ambience & Drones (A5) | SFX (A3-A4) |
|-------------|----------------------|------------------------|-------------|
| **Emptiness (Hook & Setup)** | Single low BASS note or none | Cold `SFX_Wind_Howl` or very low drone | Single distant scrape or melancholic piano |
| **Surrender (Challenge)** | All music remains out. Emptiness. | Static cold drone. No build. | None. Sonic minimalism. |
| **Receiving Grace (Turning Point)** | **CRITICAL:** Ethereal PADS + wordless VOCALS fade in | Warm shimmering pad replaces cold drone | Soft `Hit_Healing` or sparkle |
| **Renewed Purpose (Resolution)** | Simple hopeful MELODY (piano) over pads/vocals | Warm, supportive ambience | Gentle swells under voiceover |

---

#### **7. The Call to Adventure**

* **Core Emotional Journey:** Restlessness → Contemplation → The Spark → The First Step
* **Best For:** Leaving comfort zone, trying something new.
* **Suno Keywords:** Acoustic, Indie Pop, Lofi, Folk, Restless, Hopeful

| Story Phase | Music Stems (A6-A10) | Ambience & Drones (A5) | SFX (A3-A4) |
|-------------|----------------------|------------------------|-------------|
| **Restlessness (Hook & Setup)** | Repetitive INSTRUMENT 1 + laidback DRUMS | `SFX_Ambience_City` or distant train | Soft whoosh like passing thought |
| **Contemplation (Challenge)** | DRUMS/BASS fade. Solo guitar or questioning piano. | Intimate room tone or vinyl crackle | None. Space for internal conflict. |
| **The Spark (Turning Point)** | Warm PADS or soft vocal "ooh" swells gently | Ambience fades to near silence | Soft, hopeful `SFX_Chime_Bright` |
| **The First Step (Resolution)** | Laidback DRUMS + optimistic BASS return | Warm, sunny ambience | Gentle whooshes or pops |

---

#### **8. The Rally**

* **Core Emotional Journey:** Setback → Frustration → Renewed Focus → Determined Action
* **Best For:** Resilience stories, overcoming failure/burnout.
* **Suno Keywords:** Pop, Electronic, Beats, Determined, Empowering, Confident

| Story Phase | Music Stems (A6-A10) | Ambience & Drones (A5) | SFX (A3-A4) |
|-------------|----------------------|------------------------|-------------|
| **Setback (Hook & Setup)** | Sparse, lonely synth pluck. No drums/bass. | Cold `SFX_Drone_Hollow` | Sharp `Impact_Slam` for setback |
| **Frustration (Challenge)** | Frustrated, repetitive BASS. Stuck in loop. | Hollow drone continues. Claustrophobic. | Quick, sharp glitches |
| **Renewed Focus (Turning Point)** | Bass/synth cut. Single MELODY/PADS chord swells. | Silence. Drone cuts completely. | Clean `SFX_Click` or `Piano Chord Hit` |
| **Determined Action (Resolution)** | Full driving arrangement: BASS + powerful DRUMS + MELODY | Clean room tone. No emotional baggage. | None. Power from driving rhythm. |

---

#### **9. The Ticking Clock**

* **Core Emotional Journey:** Stagnation → Rising Urgency → Decisive Action → Momentum
* **Best For:** High stakes, procrastination, pivotal decisions.
* **Suno Keywords:** Electronic, Beats, Cinematic, Tense, Driving, Urgent

| Story Phase | Music Stems (A6-A10) | Ambience & Drones (A5) | SFX (A3-A4) |
|-------------|----------------------|------------------------|-------------|
| **Stagnation (Hook & Setup)** | Pulsing INSTRUMENT 1 (synth arpeggio) like clock | Low, steady `SFX_Drone_Anticipatory` | Persistent `SFX_Clock_Ticking` layer |
| **Rising Urgency (Challenge)** | DRUMS + BASS enter: urgent rhythm. Arpeggio speeds up. | Drone increases volume and pitch | Long, steady riser throughout |
| **Decisive Action (Turning Point)** | **CRITICAL:** All sound cuts → single `Impact_Slam` | Silence for decision moment | `Impact_Slam` or deep boom |
| **Momentum (Resolution)** | New, powerful forward-moving arrangement | Clean. Drone gone. | Energetic whooshes on cuts |

---

#### **10. The Authentic Voice**

* **Core Emotional Journey:** Conforming → Self-Doubt → Acceptance → Confident Expression
* **Best For:** Overcoming imposter syndrome, being oneself.
* **Suno Keywords:** Pop, Acoustic, Soul, Singer-Songwriter, Heartfelt, Empowering

| Story Phase | Music Stems (A6-A10) | Ambience & Drones (A5) | SFX (A3-A4) |
|-------------|----------------------|------------------------|-------------|
| **Conforming (Hook & Setup)** | Simple, generic MELODY. Fine but lacks soul. | Neutral, clean room tone | None. Lack of texture is the point. |
| **Self-Doubt (Challenge)** | Sparse: BASS + hesitant INSTRUMENT 1 | Introspective `SFX_Drone_Hollow` | Subtle riser: "this isn't me" |
| **Acceptance (Turning Point)** | All music cuts → warm, authentic INSTRUMENT 1 enters | Silence for acceptance | Warm swell like cleansing exhale |
| **Confident Expression (Resolution)** | Organic DRUMS, warm BASS, soulful vocal chop | Warm, intimate (coffee shop feel) | None. Pure, unadorned authenticity. |

---

#### **11. The Patient Growth**

* **Core Emotional Journey:** Frustration → Small Steps → Glimmer of Progress → Hopeful Perseverance
* **Best For:** Honest transformation journeys.
* **Suno Keywords:** Ambient, Acoustic, Post-Rock, Folk, Hopeful, Pensive

| Story Phase | Music Stems (A6-A10) | Ambience & Drones (A5) | SFX (A3-A4) |
|-------------|----------------------|------------------------|-------------|
| **Frustration (Hook & Setup)** | Simple, slightly melancholic INSTRUMENT 1 loop | Neutral, slightly cold room tone | None. Quiet, repetitive frustration. |
| **Small Steps (Challenge)** | Same melody + simple supportive BASS | Neutral. Action is in subtle bass addition. | Small pops or clicks per "step" |
| **Glimmer of Progress (Turning Point)** | Melody resolves to major. Warm PADS swell. | Warmer `SFX_Ambient_Pad` | Single hopeful `SFX_Chime_Bright` |
| **Hopeful Perseverance (Resolution)** | Gentle minimalist DRUMS enter. Calm forward motion. | Warm pad continues as support bed | None. Calm, determined perseverance. |

---

#### **12. The Shared Struggle**

* **Core Emotional Journey:** Isolation → Recognition ("You too?") → Shared Understanding → Collective Strength
* **Best For:** Community building, social proof.
* **Suno Keywords:** Pop, Cinematic, Acoustic, Singer-Songwriter, Sentimental, Uplifting

| Story Phase | Music Stems (A6-A10) | Ambience & Drones (A5) | SFX (A3-A4) |
|-------------|----------------------|------------------------|-------------|
| **Isolation (Hook & Setup)** | Single, lonely INSTRUMENT 1 (solo piano/guitar) | Cold `SFX_Ambience_City` or wind howl | None. |
| **Recognition (Challenge)** | Second INSTRUMENT 2 joins, harmonizing | Warmer, more intimate ambience | None. Musical harmony is the action. |
| **Shared Understanding (Turning Point)** | Two instruments resolve to beautiful MELODY/PADS chord | All ambience fades for connection moment | Very soft, warm swell |
| **Collective Strength (Resolution)** | Full, warm orchestral/band arrangement | Warm, comforting `SFX_Ambient_Pad` | None. Complete, supportive sound. |

---

## **Implementation Reference**

### SFX Retrieval

```python
from audio_effects_library import SFXLibrary

sfx = SFXLibrary("D:/Work/The Conscious Movie Factory December/SFX_Library")

# Get a drone for the "Anxiety" phase
drones = sfx.search("Tension SubBass")
# Returns: [SFXEntry(path=..., category='Drones_And_Ambience', ...)]

# Get an impact for turning point
impacts = sfx.search("BellChime")
```

### Suno Prompt for Arc/Phase

```python
from audio_effects_library.sonic_arc_engine import SonicArcEngine, StoryPhase

engine = SonicArcEngine()
prompt = engine.get_suno_prompt("breakthrough", StoryPhase.RESOLUTION)
# "Empowerment, Pop, Beats, Electronic, featuring bass, drums, melody"
```

---

**Sonic Story Arc Library V7 — CMF 2.0 + Suno AI Edition**
*Conscious Movie Factory December 2024*
