# CMF Creative Subsystems Definitions

**Version:** 1.0  
**Date:** 2026-03-23  
**Status:** Canonical first-pass definitions for CS-001 through CS-032  
**Purpose:** Convert the 30 research insights plus the 2 architecture-native additions into build-ready subsystem definitions that can later be split into `intelligence/subsystems/CS-{NNN}/` packages.

---

## How To Read This Document

Each creative subsystem is defined as a runtime decision library, not as abstract doctrine. Every subsystem therefore answers six implementation questions:

1. What problem in human perception, memory, or narrative processing does it solve?
2. Which research domain justifies its existence?
3. What inputs must the subsystem inspect?
4. What output, score, or pass/fail judgment must it produce?
5. What concrete thresholds or defaults should CMF use now?
6. What does success or failure look like inside the actual pipeline?

This document is intentionally more technical than [intelligence/CMF_Master_Scene_Intelligence.md](d:/Work/The%20Conscious%20Movie%20Factory%20December/intelligence/CMF_Master_Scene_Intelligence.md). The master intelligence file remains the synthesis layer. This file is the subsystem-definition layer that future `SKILL.md`, `config.json`, and `rules.yaml` files should inherit from.

---

## CS-001 - First Frame Imprint

CS-001 governs the first 400 milliseconds of exposure, where the viewer's nervous system decides whether the frame is worth encoding or should be rejected as clutter. The subsystem exists because the orienting response fires before reflective judgment: in mobile feed conditions, the visual system sorts for a clear high-contrast signal before the viewer has consciously decided to watch. In CMF, this means the first frame cannot be treated as branding space, decorative atmosphere, or an editor's flourish. It is a biological admission ticket. The subsystem inspects frame-one saliency, focal-element count, contrast separation, vertical position, and initial CLS. It then returns a binary or scored judgment: does the first frame create one dominant perceptual anchor fast enough to survive scroll conditions? The current CMF threshold is one focal object, upper-central placement, CLS less than or equal to 2 for the first 400 ms, and no competing text stack. A valid frame might open with a coach's face or a single striking object framed in the upper third against clean negative space. An invalid frame might open on a logo animation, a low-contrast room, subtitles plus emoji plus lower thirds, or a multi-object montage that forces search behavior. In runtime, CS-001 should be one of the earliest gates in HOOK selection because failure here makes downstream excellence irrelevant. If the video is never admitted into attention, nothing later in the system can recover the lost opportunity.

**Research basis:** Attention Capture, LC4MP  
**Primary inputs:** first-frame image, saliency map, CLS estimate, object count, UI safe-zone overlap  
**Primary output:** `PASS | REVISE | BLOCK` plus focal-confidence score  
**Current CMF default:** one focal element, upper-central third, CLS <= 2, no decorative clutter  
**Failure mode:** viewer searches instead of locks; scroll risk spikes before recognition begins  
**CMF example:** reject a HOOK template that starts on wide environmental B-roll with captions already visible

---

## CS-002 - Face Recognition Window

CS-002 defines how CMF exploits the 1.5 to 2.5 second recognition window in which faces disproportionately capture and hold gaze. The subsystem exists because human face processing is not just another compositional preference; it is a specialized neural pathway involving rapid fusiform and amygdala engagement. In short-form coaching video, a single well-framed face can outperform almost any synthetic design trick for holding attention long enough to transition from raw capture into semantic processing. CS-002 inspects whether a scene uses a face, how many faces appear, the shot scale, the eye and mouth visibility, top-of-frame placement, and whether the face is introduced early enough to matter. The subsystem should prefer medium close-up framing because it collapses the search cost for social information: the eyes, mouth, and emotional signal sit inside one glance. Its output is not merely “face present” but whether the face is usable as a recognition anchor. In CMF, vulnerability, recognition, confession, and direct teaching scenes should default to a single coach face positioned about 15 to 25 percent from the top of the frame. Multiple simultaneous faces should be penalized unless the scene intentionally requires comparison or testimony, because every additional face creates individuation cost and weakens the single-anchor effect. The subsystem fails when the face is too small, too low, too delayed, visually obscured, or multiplied. When CS-002 passes, the face becomes the primary social lock that buys time for captions, graphics, or emotional transfer to work.

**Research basis:** Attention Capture, Eye Tracking  
**Primary inputs:** face count, shot scale, bounding boxes, face position, time-to-face  
**Primary output:** recognition-anchor score and framing recommendation  
**Current CMF default:** single face, MCU, visible eyes and mouth, face introduced within first 2 seconds  
**Failure mode:** no social lock; the viewer treats the scene as generic media instead of human communication  
**CMF example:** prefer talking-head HOOK over abstract cinematic foreshadowing when early retention is weak

---

## CS-003 - Gaze Direction Transfer

CS-003 controls whether the coach's face competes with the message or transfers attention to it. The subsystem exists because faces can either monopolize visual attention or act as social pointers. Mutual gaze intensifies connection, but it also traps attention on the face itself. Averted gaze, by contrast, creates joint attention: the viewer reflexively follows where the person on screen is looking. In CMF this distinction is operational, not aesthetic. Whenever the purpose of the moment is emotional bonding, direct eye contact is valid. Whenever the purpose is to route the viewer into a caption, diagram, product, or evidence panel, the face should point. CS-003 inspects eye-line direction, graphic position, timing of graphic entry, scene purpose, and whether the face-to-graphic routing is semantically coherent. It outputs a decision such as `DIRECT_GAZE`, `AVERTED_LEFT`, `AVERTED_RIGHT`, or `REVISE_LAYOUT`. The subsystem is especially useful in scenes where agents might otherwise pile explanatory text beside a full-intensity talking head and wonder why the words are ignored. In CMF terms, the coach should not ask the audience to split loyalty between the face and the overlay. The face should recruit attention, then hand it off. The subsystem fails when gaze direction contradicts the overlay position, when direct gaze is used during dense instructional graphics, or when the graphic appears in a location the face does not socially authorize. When it passes, the graphic inherits part of the face's capture power and comprehension rises because the viewer is not independently searching for relevance.

**Research basis:** Attention Capture, social cueing research  
**Primary inputs:** eye-line vector, overlay coordinates, scene intent, text density  
**Primary output:** gaze-routing instruction and transfer confidence  
**Current CMF default:** mutual gaze for vulnerability, averted gaze for instructional transfer  
**Failure mode:** face and overlay compete, reducing both memory and readability  
**CMF example:** move the coach's glance toward a keyword card appearing screen-right during a proof sequence

---

## CS-004 - ISC Structure Enforcer

CS-004 exists to protect the conditions that maximize inter-subject correlation, the measurable synchronization of viewers' brains during structured media. Its role is to prevent CMF from drifting into improvisational assembly that may feel creatively free but weakens collective audience control. Neurocinematic research shows that highly structured editing, not merely strong content, is what elevates ISC. In practical terms, the subsystem asks whether the composition obeys the biologically justified arc, whether focal cues are clear, whether the sequence creates coherent anticipatory tension, and whether the scene order supports shared interpretation instead of idiosyncratic wandering. It reads container sequence, component assignment, arc compliance, emotional vector continuity, and focal consistency. It outputs a structural validity score and can raise a `BLOCK` when a composition breaks the architecture that produces synchrony. In CMF, this means HOOK, SETUP, CHALLENGE, TURNING_POINT, RESOLUTION, and VISION are not optional storytelling ornaments. They are synchronization infrastructure. CS-004 should therefore run above local stylistic preferences: a clever cold open or a fashionable montage is irrelevant if it destroys the shared scaffold the audience needs to track meaning together. The subsystem fails when beat order is arbitrary, when a scene behaves like an emotional outlier with no arc function, or when too many free-form exceptions erode the shape of the experience. It passes when the assembly gives different viewers the same attentional journey, which is the precondition for virality, recall, and communal response rather than isolated subjective interpretation.

**Research basis:** Neurocinematics, Eye Tracking  
**Primary inputs:** container order, component map, focal continuity, emotional arc metadata  
**Primary output:** ISC structural score and compliance verdict  
**Current CMF default:** fixed six-position arc with explicit function per beat  
**Failure mode:** low synchrony, fragmented interpretation, reduced shareability  
**CMF example:** reject a regeneration patch that inserts a hype montage between TURNING_POINT and RESOLUTION without arc justification

---

## CS-005 - Safe Zone Enforcer

CS-005 turns mobile viewing geometry into a hard execution rule. It exists because attention on 9:16 mobile screens is not evenly distributed: the upper-central region is privileged, the vertical midline is dominant, and the bottom zone is partially dead due to platform UI, thumb occlusion, and reduced perceptual priority. In many editing pipelines, safe zones are treated as export polish. In CMF, they are structural because misplacement directly increases search cost and decreases comprehension. The subsystem reads coordinates for faces, captions, graphics, logos, buttons, and essential emotional cues, then judges whether each element occupies biologically viable territory. Its output is a placement audit with violations such as `FACE_TOO_LOW`, `CAPTION_IN_UI_ZONE`, or `KEYWORD_TOO_RIGHT`. Current defaults place the face roughly 15 to 25 percent from the top, critical captions between 30 and 60 percent, and forbid important semantic elements in the bottom 20 percent or far-right margin. CS-005 is especially important when templates are adapted across platforms or when editors attempt to import desktop habits into mobile-first storytelling. A visually beautiful composition can still fail if the viewer must fight the device to access its meaning. The subsystem fails when crucial information overlaps platform chrome, sits too low to be foveally convenient, or disperses across the frame in a way that exceeds mobile scan comfort. It passes when the visual layout respects the body's default viewing strategy and makes the meaning feel immediate rather than laborious.

**Research basis:** Eye Tracking, mobile center-bias studies  
**Primary inputs:** element bounding boxes, platform template, aspect ratio, UI exclusion zones  
**Primary output:** placement compliance report  
**Current CMF default:** no critical content in bottom 20 percent; prioritize upper-central third  
**Failure mode:** avoidable search, subtitle loss, reduced comprehension under feed conditions  
**CMF example:** shift captions upward when platform buttons would otherwise occlude the final CTA phrase

---

## CS-006 - Gaze Continuity Checker

CS-006 ensures that cuts preserve attentional momentum instead of forcing needless reorientation. It exists because viewers do not consciously admire most cuts; they experience continuity when the focal point survives the transition and disorientation when the edit forces an unexpected jump. Attentional Theory of Cinematic Continuity frames good cutting not as visual smoothness but as perceptual economy. In CMF, that means cut quality is measured by where the eyes land after the cut, not by whether a transition effect is fashionable. The subsystem inspects outgoing focal coordinates, incoming focal coordinates, shot scale change, motion direction, and whether the cut occurs on attention-compatible action or shift. It outputs a delta score and can trigger a layout correction when the new focal point moves too far from the previous one. The current working threshold is a focal position delta of about 15 percent of frame width. Larger jumps are allowed only when the cut intentionally re-centers attention and supplies a strong reorientation cue. The subsystem is especially valuable in alternating A-roll and B-roll, where editors often accidentally place the outgoing point center-left and the incoming point bottom-right, making the viewer do unnecessary work. Failure occurs when the cut itself becomes the most salient event, stealing processing resources from the message. Success occurs when meaning appears to continue naturally across the edit, allowing the brain to stitch scenes together without noticing the mechanism.

**Research basis:** Eye Tracking, ATCC, edit blindness  
**Primary inputs:** pre-cut and post-cut focal coordinates, cut type, motion cues  
**Primary output:** gaze-delta score and continuity pass/fail  
**Current CMF default:** keep focal shift within roughly 15 percent of frame width unless justified  
**Failure mode:** edit draws attention to itself instead of routing attention through content  
**CMF example:** reframe incoming reaction shot so the coach's eyes land near the same screen position as the previous proof graphic

---

## CS-007 - Theta Reset Validator

CS-007 formalizes the idea that cuts are not interruptions but cognitive resets. The subsystem exists because EEG research shows an early theta-band synchronization burst after cuts, indicating active encoding and integration of the new shot. In short-form video this is precious. Every cut either buys a reset with a clear informational purpose or wastes a reset on empty change. CS-007 therefore asks whether the incoming shot justifies the neural reset it triggers. It reads cut timing, information introduced, semantic novelty, motion change, perspective change, and whether the new shot gives the viewer a concrete reason to re-engage. It outputs a reset quality score and flags wasteful edits. In CMF, a valid reset introduces a new emotional angle, object, proof, or social cue. An invalid reset simply changes the framing while saying nothing new, or cuts so frequently that the viewer expends encoding resources on update mechanics instead of narrative meaning. The subsystem is particularly useful in regeneration workflows where editors may add pace without adding value. CS-007 should not be interpreted as “more cuts equals more engagement.” Its job is the opposite: to make each cut earn the theta event it consumes. Failure produces a hollow high-energy feel where the video seems active but leaves little memory trace. Success creates forward pull because each reset rewards the brain with real progress rather than jitter.

**Research basis:** Neurocinematics, EEG cut-response studies  
**Primary inputs:** cut map, per-cut information delta, semantic function, shot purpose  
**Primary output:** reset-value score and redundant-cut warnings  
**Current CMF default:** every cut must introduce clear new information, angle, or emotional function  
**Failure mode:** wasted encoding pulses; pacing feels busy but mentally empty  
**CMF example:** remove three punch-in cuts during a monologue that add no new semantic content

---

## CS-008 - Excitation Transfer Timer

CS-008 governs one of CMF's most important emotional mechanisms: the timed conversion of residual physiological arousal into deeper feeling during the next beat. It exists because arousal decays slower than appraisal. After a high-intensity moment, the body remains activated while the mind is ready to re-label the energy. That short delay creates the “golden zone” in which a quiet or vulnerable follow-up feels disproportionately meaningful. The subsystem reads CLS sequence, beat order, duration since peak arousal, the arousal delta between adjacent beats, and whether a true low-intensity container exists after the spike. It outputs `PASS`, `FAIL`, or `BLOCK`, along with the measured transfer window. CMF's current rule is explicit: after a CLS 4 beat, the next beat must fall to CLS 1 or 2 within roughly 2 to 5 seconds. A CLS 4 followed by another CLS 4 is not escalation; it is transfer failure because the viewer never gets a space in which to misattribute the residual charge. Likewise, a 10-second delay is too late because the charge has decayed. The subsystem is central to scene ordering, pause insertion, and resolution design. Failure produces emotional bluntness, where intense scenes feel loud but not moving. Success produces the sensation that the quiet beat “lands harder than it should,” which is exactly the engineered effect CMF wants.

**Research basis:** Excitation Transfer Theory  
**Primary inputs:** CLS timeline, beat durations, transition timestamps, arousal tags  
**Primary output:** golden-zone validity and recommended follow-up beat  
**Current CMF default:** CLS 4 -> CLS 1-2 within 2-5 seconds; never CLS 4 -> CLS 4  
**Failure mode:** no misattribution window; intensity stays external instead of becoming feeling  
**CMF example:** force a pause or vulnerable close-up immediately after a dramatic revelation instead of another hype montage

---

## CS-009 - Emotional Contamination

CS-009 formalizes the Kuleshov-based principle that neutral images inherit emotional meaning from surrounding context. It exists so CMF can stop over-demanding literal B-roll. In many pipelines, editors search for footage that explicitly depicts the spoken idea, which is expensive and often less effective than using semantically neutral but emotionally absorptive material. CS-009 reads the emotional valence and intensity of the leading A-roll, the neutrality and contradiction risk of the B-roll, the duration of the contamination window, and whether the inserted image fights or supports the affective field. It outputs a contamination fitness score. In CMF, “good” B-roll is often not the clip that literally illustrates the transcript, but the clip neutral enough to receive the emotion already established by the coach's words, face, and score. A city street after a confession can feel lonely; the same city street after a triumph can feel expansive. The subsystem therefore penalizes B-roll that is too semantically loaded in a conflicting direction and rewards compositionally strong, emotionally permeable inserts. A practical working assumption from the earlier audit is that contamination can persist across roughly three to five short B-roll shots before the B-roll's own semantic identity starts dominating. Failure occurs when a “clever” visual overrides the emotional field and breaks the viewer's inferred meaning. Success occurs when the inserted image feels uncannily right even though its literal content is simple.

**Research basis:** Kuleshov Effect, affective priming  
**Primary inputs:** preceding emotional vector, B-roll neutrality score, contradiction score, sequence length  
**Primary output:** contamination suitability score  
**Current CMF default:** prefer neutral, compositionally strong B-roll over overly literal but emotionally noisy inserts  
**Failure mode:** B-roll hijacks emotion instead of absorbing it  
**CMF example:** use quiet architectural footage after grief-laden A-roll rather than a generic “sad person” stock shot

---

## CS-010 - Cross-Modal Audio Primer

CS-010 governs the affective priority of sound over picture in emotional framing. It exists because music, ambience, and leading audio can prime how the next image is interpreted before the eye has finished evaluating it. In CMF this is decisive: the audio layer should not be chosen after the visuals as if it were garnish. It should establish the emotional field into which the visuals arrive. The subsystem inspects the intended emotional arc, key and mode, timbral register, tempo, audio onset timing, transition type, and the congruence between sound and upcoming scene function. It outputs an audio-priming recommendation such as `J_CUT_REQUIRED`, `MUSIC_PRELOAD`, or `AVOID_MODE_CONFLICT`. J-cuts are the default use case because they let emotion arrive first and thereby reduce the work the picture must do to establish tone. The subsystem fails when neutral or contradictory sound arrives late, when the score changes after the visual already asked for interpretation, or when emotionally incoherent sound makes a scene feel false. It passes when the next beat is already emotionally intelligible the moment it appears. In CMF's pipeline, this subsystem should run before final visual assembly for emotionally sensitive transitions, especially around vulnerability, recognition, and turning points. If CS-010 is ignored, the editor often compensates with excessive visual signaling, which raises cognitive load and still delivers a weaker emotional lock than a properly primed audio entry.

**Research basis:** Kuleshov, Audio-Visual Congruence  
**Primary inputs:** audio key/mode, timbre, beat map, scene intent, transition timing  
**Primary output:** audio-first priming plan and congruence rating  
**Current CMF default:** music selection precedes visual finalization for emotional transitions; J-cuts are standard  
**Failure mode:** image lands emotionally late or ambiguously, forcing extra visual labor  
**CMF example:** start the low-register swell before revealing the coach's silent reaction shot

---

## CS-011 - Peak-End Budget Allocator

CS-011 allocates disproportionate production resources to the moments memory actually keeps. The subsystem exists because retrospective evaluation is dominated by the peak moment and the ending, not by the average quality of the whole sequence. In CMF, this means equal treatment across all scenes is wasteful. SETUP, CHALLENGE, and even RESOLUTION matter, but they are support beams. TURNING_POINT and VISION determine what survives in memory and what gets associated with the coach or brand. CS-011 reads scene role, predicted peak location, ending strength, available VFX and graphics budget, score intensity, and CTA timing. It outputs a resource allocation plan that privileges peak and end. That plan can govern C-roll density, effect complexity, motion budget, sound design emphasis, and revision attention. The subsystem fails when the middle of the video receives premium treatment while the ending dissolves into a generic callout or the turning point lacks enough perceptual force to register as the remembered peak. It passes when the audience could compress the entire video into two remembered snapshots and those snapshots contain the message CMF wanted to preserve. This subsystem is especially important for teams that instinctively polish every scene equally. Research says memory is not democratic. CMF should not pretend otherwise.

**Research basis:** Peak-End Rule  
**Primary inputs:** arc position, predicted climax strength, ending design, available asset budget  
**Primary output:** prioritized budget map for scenes and effects  
**Current CMF default:** allocate roughly 2x complexity budget to TURNING_POINT and VISION  
**Failure mode:** polished middle, forgettable ending, weak retrospective value  
**CMF example:** spend the strongest graphic build and score lift on the revelation and the final future-self image, not on the exposition scene

---

## CS-012 - CTA Fusion Timer

CS-012 exists to protect action against the feed's memory-wiping momentum. The subsystem is based on the observation that in fast-scroll platforms, the interval between emotional resolution and behavioral request cannot be treated as dead air. If the end feeling and the CTA are separated by too much time, the next stimulus begins erasing intention before behavior can fire. CS-012 inspects the end beat, CTA onset, gap duration, fade behavior, silence use, and whether the CTA inherits the same emotional field as the ending. It outputs a fusion verdict and a maximum allowed gap. In CMF's current model, the CTA should live inside the same two to three second window as the end-state image or verbal resolution. No black-frame exhale, no ornamental tag, and no detached outro. The CTA should feel like the natural next movement of the same emotional wave, not like a postscript. The subsystem fails when the CTA feels administratively attached after the story has already ended. It passes when the audience reaches a peak or resolution and the desired action is presented before cognitive context switches. This is one of the clearest places where platform psychology overrides old media habits: a theatrical denouement can breathe; a feed-native CTA must fuse.

**Research basis:** Peak-End Rule, LC4MP, feed-switching behavior  
**Primary inputs:** end timestamp, CTA timestamp, gap duration, audio continuity, scene role  
**Primary output:** CTA-fusion compliance and timing adjustment  
**Current CMF default:** VISION and CTA share the same 2-3 second window  
**Failure mode:** the emotional end lands but behavior does not transfer  
**CMF example:** overlay “Follow for part 2” on the final resolved image instead of after a separate branded tail

---

## CS-013 - Variation Engine

CS-013 exists to prevent neurological habituation across a creator's body of work. The subsystem is not randomization for its own sake. It is controlled deviation that preserves the biological arc while changing the cinematic vehicle enough to prevent pattern fatigue. Variable reward logic suggests that audiences stay alert when they cannot fully predict the exact form the next payoff will take. In CMF, this means repeating the same HOOK vehicle, same scene type, same pacing pattern, and same temperature arc across consecutive videos will eventually collapse attention even if each video is locally competent. CS-013 reads recent campaign history, scene component usage, timing signatures, emotional vector patterns, motion palettes, and tribe preferences. It outputs a novelty score and recommends swaps at the component, template, or parameter level. The subsystem should prefer changing the vehicle rather than violating the arc. For example, the same SETUP function can be delivered by vulnerability, archetypal imagery, evidence, or voice of truth, provided the container contract still passes. Failure occurs when CMF optimizes itself into a technically correct but predictable house style. Success occurs when the audience experiences continuity of intelligence but novelty of execution. This subsystem is one of the main defenses against the “AI slop” failure mode, because repetition is often felt before it is consciously named.

**Research basis:** Excitation Transfer, Film Editing rhythm research, habituation logic  
**Primary inputs:** last-N videos, component history, timing signatures, effect history, tribe response  
**Primary output:** novelty score and substitution recommendations  
**Current CMF default:** no identical beat-timing or component pattern in consecutive campaign videos  
**Failure mode:** structurally correct repetition produces deadened engagement over time  
**CMF example:** swap SETUP from personal confession to archetypal visual setup while keeping the same biological function

---

## CS-014 - Emotional Beat Limiter

CS-014 protects the viewer from emotional over-segmentation. The subsystem exists because too many distinct emotional turns in a short video increase interpretation cost and reduce the strength of each individual beat. Kuleshov-style meaning and affective transfer work best under constraint: one dominant emotional direction, possibly one meaningful reversal, and then resolution. In CMF, a 60-second video that moves through fear, anger, irony, sadness, triumph, and serenity is not rich. It is diluted. CS-014 reads declared emotional vectors, scene-level affect labels, transition count, and the valence/arousal distance between beats. It outputs an emotion-complexity judgment and can require simplification. The current default is a primary and secondary emotional vector per video, with a hard ceiling of two to three emotional beats. Binary patterns such as tension to empowerment or grief to hope tend to outperform multi-step affect mosaics because the viewer can actually carry them through the arc. The subsystem fails when each scene introduces a new feeling identity without enough time for consolidation. It passes when emotional direction is legible, accumulative, and memory-friendly. This subsystem is particularly important in collaborative environments where each agent or editor wants to add “just one more feeling” to increase nuance. The research implication is clear: nuance without containment becomes noise.

**Research basis:** Kuleshov, affective sequencing, memory constraints  
**Primary inputs:** per-scene emotional tags, valence transitions, beat count, duration  
**Primary output:** emotional complexity score and allowed vector map  
**Current CMF default:** one primary and one secondary emotional vector; max 2-3 emotional beats  
**Failure mode:** emotional stalling, reduced recall, incoherent mood architecture  
**CMF example:** collapse a fear -> anger -> sadness -> hope plan into fear -> empowerment

---

## CS-015 - Shot Duration Enforcer

CS-015 governs minimum and context-appropriate shot duration so inference remains possible. The subsystem exists because the brain cannot extract narrative meaning from arbitrarily brief shots unless prior context has already prepared interpretation. The Kuleshov research suggests roughly 750 ms as a lower bound for meaningful narrative inference when preceded by about 2 to 4 seconds of context. Without that context, the floor rises substantially. In CMF this means ultra-short cuts are tools, not defaults. CS-015 reads shot durations, preceding context stability, shot scale, semantic load, and whether the shot is expected to introduce meaning or merely intensify tempo. It outputs duration validity and can force hold extensions. A rapid montage in the HOOK may pass because context is simple and the function is capture. The same micro-duration during vulnerability or proof often fails because the viewer has insufficient time to decode social and semantic detail. The subsystem also helps resist the common mistake of equating fast with modern. Modern short-form media still obeys perceptual floors. Failure occurs when a shot intended to carry emotional or narrative meaning is too short to be processed. Success occurs when every shot's duration matches its interpretive demand rather than the editor's impulse for activity.

**Research basis:** Kuleshov Effect, event perception  
**Primary inputs:** shot length, prior-context duration, shot role, complexity, scale  
**Primary output:** duration pass/fail and recommended minimum hold  
**Current CMF default:** >= 750 ms after stable context; closer to 2 s without prior orientation  
**Failure mode:** shots are seen but not understood  
**CMF example:** extend a reaction insert from 12 frames to 30 frames so the audience can actually infer the emotional shift

---

## CS-016 - PAD Color Vector Mapper

CS-016 translates color from taste language into measurable affective coordinates. It exists because hue alone is too imprecise for a machine-guided emotional system. The PAD model gives CMF a way to map scene feeling into Pleasure, Arousal, and Dominance values derived mainly from brightness and saturation, modulated by hue. The subsystem reads scene function, emotional target, brightness distribution, saturation distribution, hue family, and desired archetype. It outputs a PAD vector and a recommended grade profile. In practice, this means “warm and cinematic” is not enough. A hopeful scene and a gritty-determined scene may both contain warm notes, but their Pleasure, Arousal, and Dominance targets differ dramatically. CS-016 makes those differences explicit. It also gives downstream subsystems something to reason over: excitation transfer, temperature arc, and motion selection can all respond to PAD targets instead of vague mood labels. The subsystem fails when grading choices contradict the intended scene function, such as a low-brightness high-dominance look being applied to a tender recognition beat. It passes when the grade operates as emotional calibration, not decoration. Within CMF, this subsystem should become one of the main bridges between art direction and runtime logic because it allows emotional design to be specified, tested, and revised without reducing it to arbitrary presets.

**Research basis:** Color Psychology, PAD model  
**Primary inputs:** brightness, saturation, hue, lighting key, target emotion, scene role  
**Primary output:** PAD vector and grade archetype recommendation  
**Current CMF default:** use archetype palette tied to scene metadata, not editor taste alone  
**Failure mode:** color grade feels stylish but emotionally false  
**CMF example:** map a resilience beat to higher Dominance and moderate Arousal rather than generic “warm inspiration”

---

## CS-017 - Temperature Arc

CS-017 governs the progression of color temperature across the video as part of the emotional arc. It exists because temperature is not only a local scene attribute; it is also a temporal signal of movement from intimacy, uncertainty, authority, threat, release, or transcendence. Warmth tends to increase Pleasure and human closeness; cooler temperatures tend to increase Dominance, distance, and analytical authority. In CMF, this makes temperature one of the cleanest longitudinal emotional levers. CS-017 reads scene order, current temperature, prior scene temperature, target arc function, brand constraints, and required unpredictability. It outputs a temperature sequence, not just a per-scene recommendation. For example, a vulnerability-led arc may begin warm, cool into confrontation or evidence, then resolve into a more balanced or renewed warmth. The subsystem fails when adjacent scenes are too thermally similar to mark emotional change or when the chosen temperature contradicts the scene's social meaning. It also fails when brand palette dogma overrides emotional truth. It passes when the temperature journey quietly reinforces the narrative trajectory and creates perceptible but not cartoonish progression. CS-017 should work hand-in-hand with CS-016: PAD handles dimensional affect; temperature arc handles longitudinal thermal storytelling.

**Research basis:** Color Psychology, affective lighting research  
**Primary inputs:** scene order, Kelvin targets, prior scene temperatures, arc role, brand constraints  
**Primary output:** scene-by-scene temperature trajectory  
**Current CMF default:** vulnerability warm, confrontation cooler, empowerment cooler or balanced, resolve based on target affect  
**Failure mode:** no visible emotional shift or wrong shift at the wrong beat  
**CMF example:** cool the CHALLENGE evidence sequence to 5600 K after a 3600 K confession beat, then re-warm the resolution

---

## CS-018 - Presence/Arousal

CS-018 scores motion choices by the ratio of presence to arousal rather than by raw excitement. The subsystem exists because high-energy camera effects do not necessarily create immersion. Some increase stress and cognitive cost while actually weakening felt participation in the scene. Presence, especially on mobile, often comes from stable embodied movement cues such as subtle drift, breathing motion, or well-scaled parallax rather than whip-driven chaos. CS-018 reads motion effect identity, predicted arousal, predicted presence, CLS burden, scene function, and display context. It outputs a ranked motion recommendation. In CMF, high-presence low-arousal effects should be the default for vulnerability, explanation, and recognition. Higher-arousal motion can be reserved for turning points or intentionally destabilizing moments. The subsystem fails when editors chase energy and accidentally produce agitation without transportation. It passes when the viewer feels inside the scene rather than merely stimulated by it. This distinction matters because presence supports memory and trust, whereas cheap arousal often just burns attention. CS-018 therefore functions as a guardrail against over-editing and as a bridge from camera-motion research into asset selection logic.

**Research basis:** Camera Motion, vection and presence studies  
**Primary inputs:** effect ID, predicted presence score, arousal score, CLS cost, scene role  
**Primary output:** ranked motion selection and safe-use guidance  
**Current CMF default:** optimize for presence/arousal ratio; reserve high arousal for key peaks  
**Failure mode:** the video feels hectic rather than immersive  
**CMF example:** choose a breathing micro-drift for a confession instead of a restless handheld shake

---

## CS-019 - Directional Semantics

CS-019 converts movement direction into narrative meaning. It exists because vertical and horizontal motion directions are not neutral. Upward movement tends to imply aspiration, lift, or power; downward movement suggests descent, weight, or submission. For left-to-right readers, left-to-right motion typically feels progressive, while right-to-left often feels resistant or adversarial. In CMF, movement direction should therefore be treated as semantic metadata, not as random visual activity. CS-019 reads scene intent, emotional vector, planned motion path, cultural reading assumptions, and shot role. It outputs a directional recommendation or contradiction warning. The subsystem is especially useful in automated effect selection where a technically acceptable motion might still be narratively wrong. A triumphant line delivered under a right-to-left drag or downward tilt may feel subtly conflicted even if the editor cannot verbalize why. Failure occurs when motion encodes the opposite of the scene's intended story. Success occurs when movement reinforces the spoken and visual meaning at a low level, making the whole scene feel “right” without overt explanation. CS-019 should also interact with CS-020 and CS-021, since semantic direction and safe movement mechanics must agree.

**Research basis:** Camera Motion, embodied directionality research  
**Primary inputs:** motion vector, narrative function, cultural profile, scene role  
**Primary output:** semantic direction pass/fail and preferred path  
**Current CMF default:** empowerment = up / left-to-right; challenge = right-to-left or downward  
**Failure mode:** subtle semantic contradiction reduces emotional coherence  
**CMF example:** route a success reveal with a slight upward push instead of a descending tilt

---

## CS-020 - Parallax Scaler

CS-020 calibrates parallax depth for mobile reality rather than desktop spectacle. The subsystem exists because vection can be achieved on small screens, but depth cues that feel persuasive on large displays can feel artificial or game-like on a phone if they are not scaled down. In CMF, parallax is powerful precisely because it can create embodied presence on a small device, but only when used with restraint. CS-020 reads delivery format, screen assumptions, effect depth settings, motion velocity, and scene role. It outputs a scale coefficient and safety note. The current CMF default is approximately 0.6 of desktop depth values for mobile-first renders, with room for controlled exceptions when a stylized effect is intentional. The subsystem fails when depth cues become the subject rather than the support, making the scene feel synthetic. It passes when parallax quietly enhances layered realism or narrative movement without being consciously noticed. This is a classic CMF pattern: the best execution often disappears into the felt experience. CS-020 therefore prevents one of the most common automation mistakes, where a measurable effect parameter is pushed simply because it can be. Biological calibration matters more than numerical intensity.

**Research basis:** Camera Motion, mobile vection studies  
**Primary inputs:** target platform, depth values, motion profile, scene type  
**Primary output:** parallax coefficient and use authorization  
**Current CMF default:** 0.6 for mobile, 1.0 max only for desktop-specific output  
**Failure mode:** artificial “video game” depth breaks trust and immersion  
**CMF example:** reduce layered text-background parallax on Shorts export while keeping full value in desktop previews

---

## CS-021 - Pan Speed Limiter

CS-021 prevents lateral camera movement from crossing the threshold where motion clarity collapses into judder and discomfort. The subsystem exists because immersion depends not only on what moves but on how fast it traverses the frame relative to the display. Traditional cinematography rules remain relevant on mobile, often more so because smaller screens and sharp edges make temporal artifacts obvious. CS-021 reads pan distance, intended duration, frame rate, display assumptions, and whether a cut could achieve the goal more cleanly. It outputs a safe speed verdict. The working CMF rule is that a full-width horizontal traverse should not occur in less than about seven seconds under normal frame-rate conditions. Faster movement may require either a different effect, a shorter traversal, or a compositional cut. The subsystem fails when motion is fast enough to produce staccato perception, visual stress, or needless attention to the camera move itself. It passes when motion remains legible, comfortable, and narratively useful. CS-021 is a polish subsystem, but it becomes structural the moment motion artifacts begin consuming attention that should have gone to meaning.

**Research basis:** Camera Motion, judder and mobile comfort research  
**Primary inputs:** pan duration, frame width, frame rate, movement amplitude  
**Primary output:** safe/unsafe motion verdict and alternative suggestion  
**Current CMF default:** no full-frame horizontal pan under ~7 s unless explicitly stylized  
**Failure mode:** judder, broken immersion, viewer discomfort  
**CMF example:** replace a rushed sideways reveal with a cut to a new framing instead of speeding up the pan

---

## CS-022 - AV Sync Enforcer

CS-022 protects recall and fluency by keeping audiovisual events inside a biologically plausible synchrony window. The subsystem exists because congruent audiovisual presentation improves recall and reduces integration cost, while drift forces the brain to decide whether two events belong together. In CMF, this is especially relevant for hits, text pops, gesture accents, and semantic reveals. CS-022 reads audio event timestamps, visual onset timestamps, event class, and whether the moment is speech-linked or impact-linked. It outputs a timing deviation and compliance verdict. The current operational window is roughly -20 ms to +100 ms as the preferred zone, with slightly different tolerance depending on whether the event is speech or a percussive hit. Failure occurs when the picture trails or leads enough that the event splits into two processing problems. Success occurs when sound and picture feel like one bound event, strengthening recall and reducing unnecessary effort. CS-022 should also coordinate with CS-027: sync is the coarse enforcement layer, while temporal binding handles the stricter word-to-graphic memory coupling. If CS-022 is lax, the video may still “look fine” in an editor but will feel subtly off in the body.

**Research basis:** Audio-Visual Congruence  
**Primary inputs:** audio onset, visual onset, event type, scene function  
**Primary output:** timing error, compliance verdict, correction target  
**Current CMF default:** preferred sync window -20 ms to +100 ms  
**Failure mode:** broken binding, reduced recall, lowered perceived polish  
**CMF example:** nudge a proof-word card 80 ms earlier so it lands with the spoken keyword rather than after it

---

## CS-023 - Rhythm Generator

CS-023 creates shot-duration rhythm using a pink-noise or 1/f logic rather than equal spacing or random cuts. The subsystem exists because human attention responds well to temporal structures that combine local bursts with long-range variation, mirroring complexity patterns found in natural systems. In CMF, rhythm should therefore feel alive rather than metronomic or arbitrary. CS-023 reads total runtime, target ASL, scene roles, BPM range, and pacing constraints from other subsystems. It outputs a timing vector with both clustered acceleration and reset spaces. The subsystem fails when cuts fall into robotic sameness or chaotic unpredictability. It passes when pacing feels intuitively natural and narratively aligned, even if the viewer cannot articulate why. CS-023 must not be used in isolation; its rhythm should still be modulated by content arousal, retention needs, and shot duration minima. But it provides the baseline temporal field from which those adaptations can depart. In practical CMF terms, this subsystem should drive default beat grids for Scene Builder and then allow CS-024, CS-025, and CS-015 to shape them according to cognitive constraints.

**Research basis:** Film Editing, 1/f temporal pattern research  
**Primary inputs:** runtime, target ASL, BPM, scene sequence, pacing constraints  
**Primary output:** shot-duration vector and tempo clusters  
**Current CMF default:** 1/f-inspired duration distribution centered on mobile-appropriate ASL  
**Failure mode:** robotic sameness or random disorder  
**CMF example:** generate a timing map with short HOOK bursts, a steadier setup hold, and a tighter turning-point cluster

---

## CS-024 - Arousal-Pacing Gate

CS-024 enforces the counterintuitive rule that emotionally hot content often needs cooler editing. It exists because LC4MP shows that overload arrives sooner when arousing content is also cut too aggressively. This means the editorial instinct to speed up the most emotional moments can backfire by pushing the viewer from engagement into processing collapse. CS-024 reads content arousal, scene CLS, current shot durations, rhythm profile, and the semantic burden of the moment. It outputs either approval or a pacing slowdown requirement. In CMF, high-arousal moments like turning points or raw confessions often need longer holds than informational setup scenes, because the viewer must absorb emotion and meaning at once. Conversely, calm or explanatory sections can tolerate somewhat faster pacing provided informational density per cut remains reasonable. The subsystem fails when editing speed and content arousal multiply each other into overload. It passes when pacing counterbalances emotional heat so the viewer remains inside the narrative rather than defending against it. This is one of CMF's most important anti-instinct rules and should be encoded explicitly, because human editors frequently violate it in the name of intensity.

**Research basis:** LC4MP  
**Primary inputs:** scene arousal score, CLS, shot duration map, content density  
**Primary output:** pacing approval or slowdown mandate  
**Current CMF default:** higher arousal requires longer, cleaner holds than low-arousal explanation  
**Failure mode:** the peak becomes noisy instead of powerful  
**CMF example:** extend the emotional reaction beat after a hard truth instead of cutting three times inside it

---

## CS-025 - Retention Cascade

CS-025 exists to optimize the first few seconds as a survival gate for the rest of the video. The subsystem is based on the observation that if a viewer survives the earliest window, the probability of staying rises sharply. In CMF this turns the HOOK into a compression problem: maximum signal, minimum confusion, minimal cognitive burden per cut, and immediate relevance. CS-025 reads the first three seconds, time-to-face, time-to-stakes, ASL, focal clarity, CLS, and whether the opening telegraphs delay instead of payload. It outputs a retention risk score and can reject an opening that is technically polished but strategically slow. The current default is a HOOK ASL around 0.8 to 1.5 seconds with low per-cut information density and fast delivery of the most important signal. The subsystem fails when the opener wastes time on logos, framing statements like “today I want to talk about,” or high-CLS clutter that asks for effort before trust is earned. It passes when the viewer is admitted quickly and then handed a viable path into ten seconds. CS-025 should be considered a survival subsystem in the priority stack because nothing downstream matters if the opening leaks viewers immediately.

**Research basis:** Attention Capture, Film Editing retention benchmarks  
**Primary inputs:** first-3s timing, ASL, time-to-stake, time-to-face, opening CLS  
**Primary output:** retention survival score  
**Current CMF default:** front-load strongest signal; HOOK ASL 0.8-1.5 s; no delayed payload intros  
**Failure mode:** viewers leave before structure, emotion, or teaching can engage  
**CMF example:** replace “Hi guys, today...” with immediate problem statement plus face lock

---

## CS-026 - Identity Tracking

CS-026 protects limited cognitive resources by minimizing unnecessary face individuation. The subsystem exists because every new face introduced into a short-form sequence demands configural processing and identity bookkeeping. If multiple faces appear without narrative necessity, the viewer spends resources tracking who is who instead of understanding the message. In CMF, this makes the coach's face a privileged continuity anchor. CS-026 reads face changes across scenes, role necessity, B-roll face prominence, and whether secondary faces are decorative or functional. It outputs an identity-load score and can recommend reducing or subordinating additional faces. The subsystem fails when extra people are introduced for surface variety but impose nontrivial comprehension cost. It passes when the social field remains simple enough that attention stays on meaning. This is also an authenticity subsystem: processing fluency can increase perceived sincerity when the same recognisable human anchor carries the arc. CS-026 does not ban other faces; it requires justification. Testimony, contrast, or specific narrative evidence may warrant them. Decoration does not.

**Research basis:** LC4MP, Attention Capture  
**Primary inputs:** face count over time, role tags, shot prominence, narrative necessity  
**Primary output:** identity-load rating and reduction advice  
**Current CMF default:** one dominant coach face per video unless justified otherwise  
**Failure mode:** unnecessary individuation tax reduces message comprehension  
**CMF example:** reject a montage of random smiling faces in the middle of a teaching sequence

---

## CS-027 - Temporal Binding

CS-027 is the precise memory-binding subsystem for word-to-graphic alignment. It exists because temporal contiguity has unusually high instructional effect size: when a keyword and its visual counterpart arrive within the temporal binding window, the brain encodes them as one integrated event rather than two loosely related ones. In CMF, this is crucial for educational, proof, and coaching content where C-roll is supposed to strengthen, not merely decorate, the spoken message. CS-027 reads phonetic onset, waveform features, graphic first-frame timing, event salience, and whether the visual leads or lags speech. It outputs a binding confidence score. Current CMF logic prefers visual onset inside roughly -20 ms to +160 ms relative to the target word, with visual-leading slightly more tolerable than audio-leading when needed. The subsystem fails when the graphic arrives so late that the viewer has already processed the spoken word and must reopen working memory to connect it. It passes when the word and image feel fused. CS-027 is stricter than CS-022 because its concern is not general sync polish but memory trace construction. If this subsystem is tuned well, simple instructional graphics become disproportionately effective without adding load.

**Research basis:** Mayer's Principles, audiovisual temporal binding research  
**Primary inputs:** phonetic onset, graphic onset, event type, waveform peaks  
**Primary output:** temporal-binding score  
**Current CMF default:** first graphic frame within about -20 ms to +160 ms of keyword onset  
**Failure mode:** words and graphics are both present but weakly encoded together  
**CMF example:** pop a three-word framework card exactly as the coach begins saying the core term

---

## CS-028 - Element Counter

CS-028 enforces mobile working-memory limits by restricting the number of simultaneously meaningful visual elements on screen. The subsystem exists because the visual channel's effective capacity is narrow. Face, text, icon, diagram, product, subtitle, reaction sticker, lower third: each added element competes for selection and storage. In CMF, this capacity limit should be modeled, not negotiated ad hoc. CS-028 reads frame-level element count, semantic importance, redundancy, and whether multiple elements can be sequenced across cuts instead of stacked. It outputs a count violation report and can propose serialization. The current default is a maximum of three simultaneous meaningful elements, typically some combination of face, key text, and one support cue. Failure occurs when four or more competing items ask the viewer to integrate them at once. Success occurs when the composition chooses one thing to look at, one thing to read, and optionally one contextual support. This subsystem is especially valuable because automation pipelines tend to accumulate “helpful” overlays until help becomes overload.

**Research basis:** Mayer's Principles, split-attention research  
**Primary inputs:** per-frame object/overlay count, semantic weights, redundancy map  
**Primary output:** element-count compliance and reduction recommendation  
**Current CMF default:** max 3 simultaneous meaningful elements  
**Failure mode:** split attention, stalled encoding, degraded readability  
**CMF example:** remove decorative emoji and secondary label when face plus keyword plus icon already occupy the frame

---

## CS-029 - ISC Quality Scorer

CS-029 gives CMF a quantitative proxy for how well a composition is likely to synchronize an audience. The subsystem exists because ISC itself is too expensive to measure directly at runtime, but the conditions that increase it are known: strong structure, clear focal guidance, coherent arc, controlled pacing, and meaningful cuts. CS-029 reads outputs from other subsystems rather than raw media alone. It aggregates structural compliance, gaze continuity, peak-end integrity, emotional clarity, rhythm quality, and retention viability into a synthetic synchrony score. The output is a numeric quality estimate and a ranked list of weak contributors. This subsystem is important because it prevents the team from optimizing isolated local metrics while ignoring the global audience-control objective. A video can have excellent color and sound yet still earn a mediocre synchrony forecast if its structure is loose or its cuts scatter attention. Failure occurs when the overall system cannot explain why a composition feels unlikely to travel or persuade. Success occurs when CMF has a defensible global measure that reflects the whole composition rather than a single craft dimension. CS-029 should become the final “quality north star” just before render and during regeneration review.

**Research basis:** Neurocinematics, predictive media-performance research  
**Primary inputs:** outputs of CS-001 through CS-028, plus arc metadata  
**Primary output:** 0-100 ISC quality score and contributor breakdown  
**Current CMF default:** use as final composite quality metric before publish  
**Failure mode:** local wins mask global audience-synchrony weakness  
**CMF example:** hold release when strong graphics and score cannot compensate for poor structural synchrony

---

## CS-030 - Neural Phase Router

CS-030 maps scene roles to the neural systems they are supposed to recruit. The subsystem exists because the narrative arc is not a loose storytelling tradition; it is a sequence of attentional and mnemonic jobs. Exposition and recognition often recruit self-referential and default-mode processing; surprise and incitement recruit orienting systems; high stakes recruit affective and executive systems; endings recruit memory consolidation mechanisms. In CMF, scene metadata should therefore determine parameter defaults according to neural phase, not merely according to genre conventions. CS-030 reads container identity, emotional task, desired network target, and currently chosen parameters. It outputs a consistency judgment: do the scene's motion, pacing, color, and saliency settings actually support the neural phase assigned to that beat? Failure occurs when a beat is tagged as vulnerability but behaves like a hype trailer, or when a turning point lacks the multimodal density required for peak integration. Success occurs when each scene's formal parameters help route the viewer through the right cognitive state in the right order. This subsystem is the high-level architecture link between neuroscience and composition logic.

**Research basis:** Neurocinematics, Peak-End, narrative processing research  
**Primary inputs:** container type, target neural phase, scene parameters, emotional function  
**Primary output:** neural-phase consistency verdict  
**Current CMF default:** parameters inherit from container-specific neural targets  
**Failure mode:** scenes are mislabeled or misbuilt relative to the brain state they should induce  
**CMF example:** downgrade motion and raise intimacy when a scene marked VULNERABILITY is currently built like a confrontation beat

---

## CS-031 - Scene Type Selector

CS-031 is the architecture-native subsystem that chooses which cinematic vehicle should fill a biologically fixed container. It exists because the arc positions are stable, but the creative vehicles that satisfy them must vary across tribe, asset availability, recent campaign history, and stylistic differentiation. In other words, the brain cares about function more than vehicle, but audiences still habituate to repeated vehicles. CS-031 reads container contracts, component compatibility, available assets, prior video history, tribe preferences, and outputs from high-priority subsystems such as retention, excitation transfer, and variation. It outputs the best-fitting component-template pair for each arc position. This subsystem is more than a lookup table because conflicts are common: a component may be emotionally ideal but fail face-recognition requirements, exceed HOOK CLS budget, or repeat a pattern used in the last three videos. CS-031 resolves those tensions by selecting the nearest viable alternative that still honors the container's biological job. Failure occurs when scene selection is driven by vibes, habit, or asset convenience instead of subsystem-aware reasoning. Success occurs when the same underlying arc can be rendered through different cinematic vocabularies without losing its neuroscientific validity. This subsystem is the practical hinge between reusable creative inventory and rigorous structural intelligence.

**Research basis:** Synthesized from Neurocinematics, Kuleshov, Peak-End, system architecture  
**Primary inputs:** container contracts, component library, asset inventory, variation history, subsystem constraints  
**Primary output:** selected scene component and template per container  
**Current CMF default:** choose by biological fit first, novelty second, preference third  
**Failure mode:** repetitive or invalid scene choices made without subsystem consultation  
**CMF example:** replace a no-face cinematic HOOK with an out-of-context talking-head HOOK because early retention requires CS-002 compliance

---

## CS-032 - Silence Container

CS-032 is the architecture-native subsystem that guarantees the existence of a true low-noise container after peak arousal moments. It exists because excitation transfer requires not only a timing window but a physical narrative vessel in which residual arousal can be re-labeled. Silence, stillness, or near-silence is therefore not emptiness in CMF. It is the engineered receiver of the previous beat's charge. CS-032 reads preceding CLS, timing since peak, ambient density, dialogue density, score intensity, and whether a clean pause exists. It outputs a mandatory pause requirement, duration guidance, and placement recommendation. The subsystem fails when the pipeline treats pauses as optional mood choices and immediately fills the post-peak interval with more speech, more motion, or more music. It passes when there is a real perceptual cavity in which the body is still activated but the scene has become quiet enough for emotional transfer and consolidation. CS-032 is especially important because teams often resist silence out of fear that it will lower retention, but the research logic suggests the opposite when used after a peak: the pause is what converts stimulus into feeling. Within CMF's priority hierarchy, this subsystem belongs near memory formation and should be allowed to override ornamental momentum.

**Research basis:** Synthesized from Excitation Transfer and LC4MP  
**Primary inputs:** prior beat CLS, gap duration, soundtrack density, dialogue density, scene order  
**Primary output:** pause mandate and silence-container spec  
**Current CMF default:** insert a clean low-CLS pause after major peaks when transfer is required  
**Failure mode:** no quiet vessel exists for residual arousal to become meaning  
**CMF example:** insert THE PAUSE after a revelation instead of jumping directly into explanatory narration

---

## Packaging Guidance

When this document is decomposed into the future subsystem library, each `intelligence/subsystems/CS-{NNN}/` package should inherit the same six-part logic used above:

- `purpose`: what cognitive or narrative problem the subsystem solves
- `research_basis`: source papers or synthesized domains
- `inputs`: the artifact fields or measurements it reads
- `outputs`: score, verdict, or routing decision it produces
- `thresholds`: current CMF defaults and hard constraints
- `examples`: one success case and one failure case in pipeline terms

The practical next step is not more conceptual expansion. It is to turn the highest-priority subsystems into real packages first:

1. `CS-001`, `CS-025` for survival
2. `CS-008`, `CS-024`, `CS-027`, `CS-032` for encoding and memory
3. `CS-011`, `CS-012`, `CS-029` for recall and quality control
