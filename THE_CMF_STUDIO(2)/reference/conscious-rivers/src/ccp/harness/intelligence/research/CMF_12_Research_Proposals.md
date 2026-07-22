# CMF Foundation Research Proposals
## 12 Deep Research Briefs for the Cognitive Science of Automated Video Editing

**Context for all proposals:** We are building an automated video production pipeline (The Conscious Movie Factory) that produces short-form social media content (60–180 seconds) for YouTube Shorts, TikTok, and Instagram Reels. The content is coaching/transformation content: a coach delivers a narrative arc through direct-to-camera A-Roll, supported by B-Roll (cinematic stock footage, AI-generated animated images, authentic behind-the-scenes footage), Found Clips (cultural reference clips used for ironic juxtaposition), and C-Roll (graphic compositions: text cards, animated charts, collages). The pipeline uses programmatic editing via Remotion (React-based video framework) and FFmpeg. We need to encode empirically validated cognitive and perceptual science into the system's editing intelligence so that every effect, color grade, transition, and scene sequence is chosen with research-backed intentionality rather than intuition.

---

## Research Proposal 1: Limited Capacity Model of Mediated Message Processing (LC4MP)

**Research Question:** How does Annie Lang's Limited Capacity Model of Motivated Mediated Message Processing (LC4MP) apply to short-form social media video content, and how can its three sub-processes (encoding, storage, retrieval) be used to quantify the cognitive load of specific video editing effects and scene compositions?

**Background & Scope:** We currently assign a "Cognitive Load Score" (CLS, 1–5 scale) to each visual effect and scene template in our library. This score is based on editorial intuition. We need to replace it with a research-grounded framework. Lang's LC4MP model (2000, Journal of Communication) proposes that processing mediated messages uses three concurrent limited-capacity sub-processes: encoding (taking sensory information in), storage (creating meaning and linking to existing knowledge), and retrieval (accessing previously stored information). When capacity is exceeded in any one channel, the others degrade.

**What we need from this research:**
1. A comprehensive summary of the LC4MP model and its key experiments, specifically those measuring cognitive load via secondary task reaction time (STRT), heart rate deceleration, and skin conductance in response to video content.
2. How specific production techniques — fast cuts, camera movement, on-screen text, graphic overlays, split-screen compositions, speed ramps — map to each of the three sub-processes. Which techniques load encoding? Which demand storage? Which trigger retrieval?
3. Any studies that have applied LC4MP specifically to short-form mobile-first video content (TikTok, YouTube Shorts, Instagram Reels) or to advertising content under 3 minutes.
4. Practical thresholds: at what point does cognitive overload occur in terms of cuts-per-second, simultaneous on-screen information elements, or combined audio-visual complexity? Are there published guidelines?
5. How structural features (cuts, movement, visual complexity) interact with content features (emotional valence, novelty, relevance) to impact total processing load.
6. Any criticism or updates to the LC4MP model in the 2010s–2020s that would affect its application to modern mobile-first short-form content.

---

## Research Proposal 2: Mayer's Cognitive Theory of Multimedia Learning (CTML) — The 12 Principles

**Research Question:** Which of Richard Mayer's 12 Multimedia Learning Principles are directly applicable to short-form social media video editing for coaching and educational content, and how do they translate into concrete editing rules for an automated video production system?

**Background & Scope:** Richard Mayer's Cognitive Theory of Multimedia Learning (CTML), developed across multiple publications starting from 2001 (Cambridge University Press), identifies 12 evidence-based principles for effective multimedia instruction. Our system produces coaching videos that are simultaneously educational and emotionally persuasive. We build C-Roll graphic compositions (animated text, charts, flowcharts, quote cards) that overlay or intercut with the coach's A-Roll narration. We need to know which Mayer principles directly govern how these compositions should be built, timed, and sequenced to maximize both comprehension and retention on social media platforms where attention is extremely scarce.

**What we need from this research:**
1. A clear summary of all 12 Multimedia Principles with their experimental evidence base, effect sizes where available, and boundary conditions.
2. Specific focus on: the Coherence Principle (removing extraneous material), the Signaling Principle (highlighting essential material), the Redundancy Principle (when NOT to use text + narration simultaneously), the Temporal Contiguity Principle (presenting narration and corresponding visuals simultaneously rather than sequentially), and the Modality Principle (using narration rather than on-screen text for complex explanations).
3. How these principles apply when the content is NOT purely instructional but also emotionally persuasive — does emotional engagement (music, color grading, testimonial clips) violate the Coherence Principle or enhance learning through emotional arousal?
4. Whether the 12 Principles have been validated in the context of mobile-first vertical video and social media platforms where viewing sessions are extremely short (under 3 minutes) and viewers can scroll away at any moment.
5. Any studies on the interaction between Mayer's Principles and viewer retention metrics (watch time, completion rate, replay rate) on YouTube, TikTok, or Instagram.
6. Concrete, implementable guidelines: e.g., "do not display more than X words of on-screen text simultaneously with narration," "animated elements should appear within X milliseconds of the corresponding narration," etc.

---

## Research Proposal 3: Neurocinematics — How Structured Editing Synchronizes Viewer Brains

**Research Question:** What does the field of neurocinematics (fMRI and EEG studies of viewers watching edited film) reveal about how editing structure, scene sequencing, and visual storytelling techniques synchronize neural activity across viewers, and how can these findings be applied to maximize engagement in short-form social media video?

**Background & Scope:** Uri Hasson and colleagues at Princeton pioneered "neurocinematics" (2008, Projections journal), using fMRI to measure Inter-Subject Correlation (ISC) — the degree to which different viewers' brains activate in the same regions at the same time while watching the same content. Their landmark finding: well-edited, structured films (like Hitchcock's work) produced 65% ISC, while unstructured real-life footage produced only 5%. Our automated pipeline constructs videos from pre-designed scene templates (72 templates across 18 scene types), each with specific emotional functions, pacing signatures, and effect assignments. We need to understand whether template-based, structured editing can achieve high ISC even in short-form social media content, and which structural techniques drive the highest neural synchrony.

**What we need from this research:**
1. A comprehensive review of Hasson's original neurocinematics findings and all subsequent studies in this field through 2025, including ISC measurements across different genres, editing styles, and content lengths.
2. Which specific editing techniques produce the highest ISC? Do cuts, camera movement, close-ups on faces, emotional music, or narrative tension drive the most neural synchrony?
3. Is there a minimum content length required for ISC to emerge, or can short-form content (60–180 seconds) achieve meaningful neural synchrony?
4. How does ISC relate to measurable engagement metrics that matter on social media: watch time, completion rate, share rate, comment rate? Has anyone correlated ISC with platform analytics?
5. The role of "attention attractors" — faces, moving objects, high-contrast elements — in driving ISC at the scene level.
6. Any findings on how narrative structure (setup → conflict → resolution) versus non-narrative montage affects ISC.
7. Practical implications: if our system sequences scenes using a pre-designed emotional arc (e.g., Intrigue → Vulnerability → Struggle → Empowerment), does the research suggest this will produce higher engagement than ad-hoc assembly?

---

## Research Proposal 4: Shot Duration, Cut Rhythm, and the 1/f Pattern in Film Editing

**Research Question:** What does James Cutting's research on shot duration patterns in successful films reveal about optimal cut rhythm and pacing, and how should these findings inform the automated sequencing and timing of cuts in short-form social media video (60–180 seconds)?

**Background & Scope:** James Cutting and colleagues at Cornell have conducted extensive computational analyses of shot duration in Hollywood films spanning nearly a century. Their key finding: shot durations in the most successful and engaging films approximate a "1/f" or "pink noise" pattern — a fractal, self-similar structure where temporal variation exists at every timescale, neither too predictable (boring) nor too random (chaotic). They also documented that average shot length (ASL) in Hollywood films has decreased from ~12 seconds in the 1930s to ~4 seconds in the 2010s. Our system creates short-form videos where the total runtime is 60–180 seconds and each scene template specifies a pacing characteristic (e.g., "fast staccato cuts at 15–20 frames" or "one long held shot for 3–4 seconds"). We need to understand how to apply 1/f timing principles at the micro-scale of short-form content.

**What we need from this research:**
1. A detailed summary of Cutting's methodology and findings on 1/f patterns, auto-correlation in shot durations, and the evolution of ASL across decades.
2. Does the 1/f pattern apply at the scale of 60–180 second videos, or is it only observable in feature-length films? Are there studies that have examined shot duration patterns in short-form content, YouTube videos, TikTok content, or advertising?
3. What is the relationship between cut rate (cuts per minute) and viewer engagement metrics (watch time, drop-off rate, retention curve) specifically on YouTube, TikTok, and Instagram? Are there published benchmarks?
4. The concept of "attentional synchrony" — do viewers synchronize their eye movements and attention more effectively when cuts follow a 1/f pattern versus random or metronomic patterns?
5. How does music tempo (BPM) interact with cut rhythm? Our system uses "Sonic Story Arcs" with specific BPM ranges (60–140 BPM). Should cuts be synchronized to beats? To sub-beats? To musical phrase boundaries?
6. Any research on the "first 3 seconds" rule for social media: what cut rate and visual complexity in the opening hook maximizes the probability that a scroller stops and watches?

---

## Research Proposal 5: Excitation Transfer Theory and Emotional Scene Sequencing

**Research Question:** How does Dolf Zillmann's Excitation Transfer Theory apply to the sequencing of emotionally varied scenes in short-form social media video, and what are the optimal patterns for alternating high-arousal and low-arousal scenes to maximize emotional impact and viewer retention?

**Background & Scope:** Dolf Zillmann's Excitation Transfer Theory (1971, reprinted widely) posits that residual physiological arousal from one stimulus transfers to and intensifies the emotional response to a subsequent stimulus. In video editing terms: a high-energy, fast-cut "Challenge" scene followed immediately by a quiet, still "Turning Point" scene should make the quiet moment feel MORE emotionally intense, not less, because the viewer's residual arousal from the preceding chaos amplifies the new emotion. Our system sequences 4–7 scenes per video, each drawn from 18 scene types with different emotional functions (Shock, Vulnerability, Tension, Ironic Release, Realization, Empowerment, etc.). We currently use a "Rhythmic Contrast Mandate" that says to juxtapose fast + slow, but we lack specific scientific rules for optimal emotional sequencing.

**What we need from this research:**
1. A comprehensive review of Excitation Transfer Theory: the original experiments, the physiological mechanisms (heart rate, galvanic skin response, cortisol), and the temporal decay curve of residual arousal in adults.
2. How long does residual excitation persist? If a 15-second high-CLS scene ends, how much arousal transfers to the next scene after 2 seconds? After 5 seconds? After 10 seconds? This temporal decay is critical for our editing timing.
3. Studies that have applied Excitation Transfer specifically to video editing sequences, advertising, or short-form content (not just laboratory paradigms with isolated stimuli).
4. Is there an optimal number of arousal "peaks" per minute of video content for social media? Too many peaks → habituation. Too few peaks → boredom. What does the research say?
5. How does the contrast between scenes matter? Is a jump from CLS 4 → CLS 1 more effective than CLS 4 → CLS 2? Does extreme contrast always beat moderate contrast?
6. The relationship between excitation transfer and the "hook" — does starting a video at high arousal (our HOOK scene type) create transfer that amplifies the subsequent SETUP scene, or does it create a "crash" if the drop is too severe?
7. Any findings specific to mobile viewing where the viewer has the option to scroll away — does excitation transfer play a role in retention decisions?

---

## Research Proposal 6: The Peak-End Rule and Its Application to Short-Form Video Structure

**Research Question:** How does Kahneman's Peak-End Rule apply to the subjective evaluation of short-form social media videos, and how should this bias inform the allocation of production effort, effect intensity, and asset quality across a video's scene sequence?

**Background & Scope:** Daniel Kahneman's Peak-End Rule (1993, Psychological Science; 2000, with Fredrickson) demonstrates that people evaluate past experiences based primarily on two moments: the peak intensity moment and the final moment, with "duration neglect" causing the overall length to have minimal impact on the retrospective evaluation. Our system produces videos with 4–7 scenes following a narrative arc. We need to understand whether this bias applies to short-form video evaluation (e.g., like/share/save/comment decisions, which happen AFTER viewing), and if so, which specific scenes should receive disproportionate production investment. Our scene types include HOOK (opening), SETUP, CHALLENGE, TURNING POINT, RESOLUTION, and VISION (closing). If the Peak-End Rule holds, CHALLENGE or TURNING POINT (the emotional peak) and VISION/RESOLUTION (the end) would be the primary drivers of viewer perception.

**What we need from this research:**
1. Summary of the Peak-End Rule experiments and their replication across domains (pain, pleasure, entertainment, advertising).
2. Has the Peak-End Rule been studied specifically for short-form video content (under 3 minutes)? For social media content? For content where the "end" is immediately followed by a behavioral decision (like, share, comment, follow)?
3. Does the "peak" in video content correspond to the highest emotional intensity moment, the most visually complex moment, or the most surprising moment? Which dimension defines "peak" for video evaluation?
4. How does "duration neglect" interact with platform metrics? If a 90-second video with a strong peak+end is rated equally to a 60-second video with the same peak+end, should we optimize for shorter videos?
5. Does the "first impression" (our HOOK) function independently of the Peak-End Rule, or does a strong hook CREATE the peak by establishing the reference frame? Some researchers argue for a "Peak-End-Start" model.
6. Practical implications: should we allocate 2x the visual effects budget, higher-quality B-Roll, and more complex C-Roll compositions to the peak and final scenes while using simpler execution for middle scenes?
7. Any interaction between the Peak-End Rule and social sharing behavior — is a strong ending more predictive of shares than a strong peak?

---

## Research Proposal 7: Color Psychology and Emotional Response in Video — Quantified PAD Models

**Research Question:** What does empirical research on color-emotion associations reveal about the quantifiable relationship between video color grading parameters (hue, saturation, brightness, temperature) and viewer emotional responses, specifically using the PAD (Pleasure-Arousal-Dominance) model, and how can these mappings be used to automate color grade selection in social media video?

**Background & Scope:** Our effects library contains 22 color grading presets, each designed to trigger specific emotions: "Personal Low" (cool, desaturated = sadness), "Hopeful" (warm, golden = inspiration), "Gritty Determination" (high contrast, desaturated, steel-blue = resilience), "Playful Pop" (high saturation, bright = joy), etc. These assignments are currently based on Patti Bellantoni's qualitative color theory and editorial intuition. We need to replace intuitive emotion labels with quantified emotional vectors that our system can compute and match against the target emotional state of each narrative beat. The PAD model (Pleasure, Arousal, Dominance — Mehrabian & Russell, 1974) provides three continuous dimensions that can describe any emotional state. We need the research that maps color parameters to PAD coordinates.

**What we need from this research:**
1. A comprehensive review of Patricia Valdez & Albert Mehrabian (1994) and Lauren Labrecque & George Milne (2012) on color-emotion quantification using the PAD model. What are the experimentally validated mappings from hue, saturation, and brightness to Pleasure, Arousal, and Dominance scores?
2. How do these mappings change when colors are applied as video color grades rather than isolated color swatches? Is there research on the emotional impact of color grading specifically (LUTs, curves adjustments, tint/temperature shifts) in motion picture or video advertisement contexts?
3. The warm-cool spectrum: how do warm color temperatures (orange/golden tones, 3200K–4500K) versus cool temperatures (blue/cyan tones, 6500K–9000K) affect Pleasure and Arousal specifically in social media video? Are there studies using video content rather than static images?
4. Saturation levels: does the relationship between saturation and emotional response differ on mobile screens (phone displays, OLED vs LCD, typical viewing brightness in various environments)?
5. The specific emotional impact of desaturation (our "Personal Low" and "Graphic Novel" grades use significant desaturation). Does desaturation reliably reduce Pleasure and Arousal? Does it increase perceive seriousness or authority?
6. Any cultural variation in color-emotion associations that would matter for a global social media audience (YouTube, TikTok, Instagram have global reach).
7. Practical deliverable: can you produce a mapping table of common color grade archetypes (warm/golden, cool/desaturated, high-contrast, soft/pastel, monochrome) to their approximate PAD coordinates based on the available empirical evidence?

---

## Research Proposal 8: Camera Movement, Motion Effects, and Physiological Arousal/Presence

**Research Question:** What does empirical research reveal about the relationship between camera movement speed, direction, and type (zoom, pan, tilt, shake, dolly, drift) and viewer physiological responses (arousal, sense of presence, emotional engagement), and how can these findings be used to assign quantified arousal and presence scores to motion effects in an automated video editing system?

**Background & Scope:** Our effects library contains 16 motion effects ranging from subtle (M-01: Slow Zoom, M-12: Breathing Effect, M-14: Dynamic Handheld Drift) to intense (M-02: Speed Ramp Chaos, M-03: Anxiety Camera Shake, M-16: Z-Space Parallax Sandwich). These effects are currently scored only by Cognitive Load (CLS 1–5). We need to add two additional axes: Arousal (does this effect activate the nervous system?) and Presence (does this effect make the viewer feel "in the scene"?). These are distinct: Camera Shake is high arousal but low presence (it's disorienting). Slow Zoom is low arousal but high presence (it's immersive). We produce content for mobile-first platforms (YouTube Shorts, TikTok, Instagram Reels) where videos are viewed vertically on small screens, often without headphones, in distracting environments.

**What we need from this research:**
1. Studies measuring physiological responses (heart rate, galvanic skin response, EEG) to specific camera movement types in film and video content. Separate findings by movement type: zoom in, zoom out, pan, tilt, dolly forward, dolly backward, handheld shake, speed ramp, static.
2. The concept of "vection" (illusory self-motion induced by visual motion) and how it applies to small mobile screens. Does vection still occur on a 6-inch phone screen? Does it contribute to engagement or to motion sickness/discomfort?
3. Movement speed thresholds: at what speed does camera movement transition from "immersive" to "disorienting" to "nauseating"? Are there published speed-of-movement guidelines for mobile content?
4. Directional semantics: does research confirm that upward motion universally signals hope/aspiration and downward motion signals descent/sadness? (We use vertical drift with these assumptions.) What about horizontal motion?
5. The "Ken Burns effect" (slow zoom + pan on still images) — is there research on its engagement effectiveness compared to static images? We extensively animate still AI-generated images into video using this technique.
6. Parallax and layered motion (our Z-Space Sandwich effect): does multi-layer parallax movement increase perceived depth and engagement on mobile screens, or is the effect lost at small screen sizes?
7. Any studies comparing the engagement impact of subtle motion effects versus no motion on otherwise static content (talking head A-Roll) in social media contexts.

---

## Research Proposal 9: Eye Tracking, Attention Direction, and Continuity Editing in Short-Form Video

**Research Question:** What does eye-tracking and attention research reveal about where viewers look during edited video, how attention is directed by cuts and visual composition, and how these findings should inform the placement and timing of effects, text overlays, and transitions in short-form social media video?

**Background & Scope:** Tim J. Smith's "Attentional Theory of Continuity Editing" (2012+) uses eye-tracking data to explain why certain cuts feel "invisible" (viewers don't notice the edit) while others feel jarring. Smith found that viewers converge their gaze to a small "attentional focus" region during engaging content, and cuts are most successful when they maintain this gaze position. Our system uses effects that direct attention: Punch-In zooms (M-04) to a specific point, Spotlight effects (C-07) that darken everything except a focal area, Match-Cuts (TR-07) that maintain subject position across cuts. We also place text overlays, subtitle captions, animated graphics, and C-Roll compositions that compete for the viewer's visual attention. We need to understand the science of where viewers actually look and how to guide that gaze programmatically.

**What we need from this research:**
1. A comprehensive review of Tim J. Smith's eye-tracking research on film editing (2010–2025), including the concepts of "edit blindness," "attentional synchrony," and the "center bias" in film viewing.
2. How does eye-tracking behavior differ on mobile screens (small, held close, often vertical) versus cinema/TV screens? Is the "center bias" stronger or weaker on mobile? Is attentional synchrony higher or lower?
3. Where do viewers look during talking-head content (A-Roll)? Eye-tracking studies on face perception in video: do viewers fixate on the eyes, mouth, or face center? Does this change when subtitles/captions are present?
4. The competition between on-screen text and visual imagery: when text (subtitles, quote cards, kinetic typography) is displayed simultaneously with moving B-Roll, where does the viewer's gaze go? What percentage of attention goes to text versus imagery? Does this change based on text position (top, center, bottom)?
5. "Safe cut" zones: is there research on when during a viewer's gaze pattern a cut is least disruptive? Should we time cuts to coincide with blinks, saccades, or fixation points?
6. How do motion effects (camera shake, zoom, speed ramp) affect the viewer's gaze pattern? Do they scatter or concentrate attention?
7. Implications for subtitle placement in vertical (9:16) video: where should captions be positioned for maximum readability without pulling attention from the primary visual content?

---

## Research Proposal 10: The Kuleshov Effect — How Juxtaposition Creates Meaning in Editing

**Research Question:** What does modern empirical research on the Kuleshov Effect reveal about how the sequential juxtaposition of shots creates meaning, emotion, and narrative interpretation in the viewer's mind, and how should these findings govern the ordering and pairing of clips in an automated video editing system for social media?

**Background & Scope:** The Kuleshov Effect (1920s, experimentally validated by Mobbs et al. 2006 using neuroimaging, and Barratt et al. 2016 in Frontiers in Psychology) demonstrates that the meaning of a shot is dramatically altered by the shot that precedes or follows it. A neutral face followed by food = hunger; the same face followed by a coffin = grief. Our system constructs every video from a sequence of 4–7 scene templates, where each scene uses different asset types (A-Roll, B-Roll, Found Clips, C-Roll). The order and pairing of these assets creates meaning beyond what any individual clip contains. Our "JUXTAPOSITION" scene type (4 templates) explicitly exploits this effect: Found Clip Punchline, Stylized Mismatch, Match Cut, Then vs. Now. But the Kuleshov Effect operates at EVERY cut, not just in dedicated juxtaposition scenes. We need to understand the full scope of this effect for automated editing.

**What we need from this research:**
1. The original Kuleshov experiments and their modern empirical validations (Mobbs et al. 2006 neuroimaging study, Barratt et al. 2016 behavioral study, and any others through 2025). What are the validated mechanisms — is it purely cognitive inference, or does juxtaposition produce genuine emotional contagion?
2. Does the Kuleshov Effect operate with equal strength in short-form content where individual shots may last only 1–3 seconds, compared to traditional cinema where shots are held for 5–12 seconds? Is there a minimum shot duration for the juxtaposition to generate meaning?
3. Asymmetry of pairing: does Shot A → Shot B create the same meaning as Shot B → Shot A? What does the research say about the direction of meaning transfer? This is critical for our system because the order of clips in a montage matters.
4. The "emotional contamination" of B-Roll: when a neutral B-Roll shot (e.g., a cityscape) is placed between two emotionally charged A-Roll statements, does the B-Roll inherit the emotional valence of the surrounding shots? This would mean our B-Roll clip selection can be simpler than we think.
5. Cross-modal Kuleshov: does the same meaning-creation happen when the juxtaposition is audio → visual (coach's voice over B-Roll) rather than visual → visual? This is critical because most of our scenes use A-Roll voiceover on B-Roll footage.
6. Cultural dependency: are the meanings created by juxtaposition universal or culturally bound? Does culture affect the interpretation of our Found Clip punchlines!
7. Practical implications for automated B-Roll ordering: given N candidate B-Roll clips for a scene, does the research suggest rules for which SEQUENCE of clips creates the strongest emotional impact?

---

## Research Proposal 11: Audio-Visual Congruence and Crossmodal Correspondence in Video

**Research Question:** What does research on audio-visual congruence and crossmodal correspondence reveal about how the alignment (or deliberate misalignment) of sonic properties (tempo, pitch, timbre, energy) with visual properties (motion speed, color temperature, cut rhythm, brightness) affects viewer comprehension, emotional response, recall, and engagement in short-form social media video?

**Background & Scope:** Our pipeline has a "Sonic Story Arc" system with 12 emotional blueprints, each specifying BPM range, keywords (e.g., "Pensive, Hopeful, Determined"), and a 4-phase sonic structure (instruments, ambience, drones per phase). Separately, we have a visual effects library with 78 effects (motion, color, texture, transitions). Currently, these two systems are NOT connected: the sonic arc is chosen based on the script's emotional journey, and the effects are chosen based on scene templates. There is no rule preventing a slow, contemplative Sonic Arc (60 BPM, Soft Piano, Vinyl Crackle) from being paired with high-energy visual effects (Speed Ramp Chaos, Camera Shake, Glitch Transitions). We need the cross-modal correspondence research to build congruence rules between sonic and visual parameters.

**What we need from this research:**
1. A comprehensive review of crossmodal correspondence research: Boltz, Schulkind & Kantra (1991) on background music and memory; Lipscomb & Kendall (1994) on music-image congruence; Charles Spence (2011) on crossmodal correspondences generally; and any subsequent studies through 2025.
2. The specific impact of audio-visual congruence on RECALL: studies show that congruent audio + visuals increase information recall by 20–40%. Is this effect consistent across content types? Does it hold for social media content where attention is divided?
3. Tempo-motion congruence: does visual cut rhythm or motion speed need to match audio BPM? If the music is 70 BPM, should the visual cuts also follow a 70-BPM rhythm, or can the visual rhythm be an independent layer? What happens when visual rhythm is at a harmonic of the audio BPM (double or half)?
4. Pitch-height/brightness correspondence: high-pitched sounds are associated with bright visuals and vertical height. Low-pitched sounds with dark visuals and low positions. How strong are these correspondences? Should our warm, bright color grades (Hopeful, Aspirational Bloom) only be paired with high-register music?
5. Deliberate incongruence: when audio and visual moods intentionally MISMATCH (calm voiceover over chaotic visuals — our "Stylized Mismatch" JUXTAPOSITION template), what is the psychological effect? Does incongruence increase surprise and attention at the cost of comprehension? How long can incongruence be sustained before it becomes confusing?
6. Sound effects and visual events: what does the research say about the timing precision required for synchronizing SFX hits (impact sounds, whooshes, risers) with visual events (cuts, zooms, text appearances)? What is the tolerance window for audio-visual synchrony perception?
7. Any studies on the impact of audio-visual congruence on social media engagement metrics (watch time, shares, comments) rather than just laboratory measures.

---

## Research Proposal 12: Attention Capture vs. Transfer in Video Advertising and Social Media Content

**Research Question:** What does the advertising effectiveness research of Rik Pieters, Michel Wedel, and related scholars reveal about the distinct mechanisms of attention capture versus attention transfer in video content, and how should these findings govern the design of visual elements (B-Roll imagery, text overlays, graphic compositions, coach face time) in short-form coaching content for social media?

**Background & Scope:** Rik Pieters and Michel Wedel's research (2004, Journal of Marketing; 2008 book chapter) demonstrated that in print advertising, pictorial elements CAPTURE attention (eyes are drawn to images first) while text and brand elements TRANSFER captured attention into memory (images alone do not create lasting brand recall without textual anchoring). Our system uses multiple visual element types: B-Roll footage (pictorial, captures attention), C-Roll graphic compositions (text-based, transfers ideas to memory), A-Roll talking head (face, captures attention through social cognition), Found Clips (cultural references, capture attention through recognition), and text overlays/subtitles (transfer spoken ideas to written memory). We need to understand how these elements work in a VIDEO context (not static print) and specifically in short mobile-first social media content where the "capture" function is existentially important (the viewer will scroll away in under 2 seconds if attention is not captured).

**What we need from this research:**
1. A comprehensive review of Pieters & Wedel (2004) and their subsequent work on attention to advertising elements, including the distinction between pictorial, text, and brand elements and their respective roles in capture vs. transfer.
2. Has this capture/transfer framework been validated in VIDEO advertising contexts, not just print/static? How does the framework change when visual elements are temporal (appearing and disappearing over time) rather than spatial (co-present on a page)?
3. The "first 2 seconds" problem on social media: what visual elements have the highest probability of capturing attention and stopping a scroller? Is it faces? Motion? Text? Color contrast? Novelty? What does eye-tracking and engagement research say about the opening frame of social media video content?
4. Competition for attention: when B-Roll imagery (capture) and on-screen text (transfer) are present simultaneously, does one suppress the other? What is the optimal timing — should text appear AFTER the visual has had time to capture attention, or should they co-appear?
5. Face-advantage in attention: our coaching content features a human face (A-Roll) prominently. What does face perception research (Theeuwes & Van der Stigchel, 2006; Langton et al., 2008) say about the face as an attention capture mechanism? Does the coach's face compete with or complement text overlays?
6. Motion effects and attention capture: do our Punch-In zoom, Camera Shake, and Speed Ramp effects function as attention CAPTURE mechanisms? If so, should they never be used simultaneously with text overlays (which require attention TRANSFER)?
7. Practical guidelines for our graphic compositions: should animated charts (EVIDENCE scenes) use minimal motion to preserve cognitive bandwidth for text transfer? Should emotional B-Roll scenes maximize motion and minimize text to preserve the capture function?
