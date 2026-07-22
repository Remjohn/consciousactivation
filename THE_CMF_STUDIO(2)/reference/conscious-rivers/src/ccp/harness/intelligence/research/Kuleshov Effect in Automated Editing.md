# **The Kuleshov Effect: Neurobiological Mechanisms, Behavioral Validations, and Algorithmic Heuristics for Automated Narrative Assembly**

The Kuleshov Effect represents the foundational cornerstone of cinematic montage, asserting that the primary unit of filmic meaning is not the individual shot, but rather the emergent property created through the sequential juxtaposition of images.1 Originally articulated in the 1920s by Soviet filmmaker and theorist Lev Kuleshov, this phenomenon suggests that the viewer’s mind is an active participant in narrative construction, subconsciously bridging the "liminal space" between cuts to derive emotions and intentions that may not exist in the source footage.4 As digital media shifts toward hyper-compressed, short-form content characterized by rapid editing and automated assembly, the Kuleshov Effect has transitioned from an aesthetic theory to a critical framework for computational creativity.6 Modern empirical research—ranging from functional magnetic resonance imaging (fMRI) to sophisticated behavioral eye-tracking—has validated Kuleshov’s early intuitions, providing a granular look at how the human brain processes cinematic sequences and how these processes can be codified for automated video generation.9

## **Historical Context and Modern Empirical Validations**

The genesis of the Kuleshov Effect is rooted in the early Soviet Montage movement, where filmmakers sought to differentiate cinema from theater by emphasizing the "art of the cut".12 Kuleshov’s original experiment involved a single, neutral close-up of the actor Ivan Mosjoukine, which was intercut with three different images: a bowl of soup, a girl in a coffin, and a woman on a divan.1 Although the actor’s expression remained constant, audiences reportedly attributed vastly different emotional states—hunger, grief, and lust—to the performer, praising his "subtle acting".12 While the original film footage was lost, the theoretical weight of this experiment catalyzed the development of "pure cinema," where the editor, rather than the actor, becomes the primary architect of the audience's emotional journey.1

Recent scientific inquiries have moved beyond the anecdotal, providing robust evidence for the effect using controlled experimental designs. Research conducted by Mobbs et al. (2006) and replicated through 2024 has utilized fMRI to identify the neural architecture that supports these contextual attributions.9 Behavioral studies by Barratt et al. (2016) further established that viewers consistently categorize neutral faces in alignment with the preceding emotional context, particularly across categories of happiness, sadness, hunger, fear, and desire.1

### **Validated Neural Mechanisms of Contextual Interpretation**

The processing of a Kuleshov sequence engages a distributed network of brain regions involved in social perception, emotion regulation, and contextual memory.9 When a viewer encounters an emotional scene followed by a neutral face, the brain does not merely register two distinct stimuli; it performs a complex integration task known as "contextual framing".9

| Brain Region | Primary Functional Contribution to Kuleshov Effect | Source Evidence |
| :---- | :---- | :---- |
| **Amygdala** | Primes affective value; "tags" neutral faces with the emotional valence of the context. | 9 |
| **Bilateral Temporal Pole** | Facilitates mental-state attributions; integrates social signals with situational context. | 9 |
| **Anterior Cingulate Cortex** | Monitors for conflict between expected and observed emotional signals. | 9 |
| **Superior Temporal Sulcus** | Processes biological motion and the "social meaning" of facial orientations. | 9 |
| **Insula** | Generates interoceptive awareness; internalizes the emotion seen in the context. | 11 |
| **Hippocampus / Parahippocampal Gyrus** | Bridges temporal gaps; maintains context in working memory during the cut. | 11 |
| **Cuneus / Precuneus** | Facilitates mental imagery and the construction of the narrative "event model." | 11 |
| **Orbitofrontal Cortex** | Evaluates the "correctness" of the emotional attribution in a decision-making context. | 9 |

The right amygdala, in particular, plays a pivotal role in "priming" the viewer.9 When a subtle happy or fearful face is preceded by a congruent emotional movie, the amygdala shows enhanced BOLD (Blood-Oxygen-Level-Dependent) responses.9 This suggests that the brain pre-activates emotional circuitry based on the context, effectively "expecting" to see a specific emotion on the subsequent face.9 Furthermore, research has identified a dissociation between the ventrolateral prefrontal cortex (vlPFC) and the ventromedial prefrontal cortex (vmPFC), where the former is more active during negative contextually-evoked attributions and the latter during positive ones.9

### **Mechanisms of Meaning: Emotional Contagion vs. Cognitive Inference**

A fundamental question for the design of automated editing systems is whether the Kuleshov Effect relies on "emotional contagion" (an automatic, bottom-up feeling) or "cognitive inference" (a deliberate, top-down deduction).24 The "affective prediction hypothesis" posits that the brain uses the context to generate a prediction of the character's internal state.25 If the subsequent face is neutral, the brain fills in the blank to resolve the prediction error.24

Recent studies indicate that the effect involves a blend of both processes. Emotional contagion occurs as the viewer "catches" the emotion of the scene through the mirror neuron system (MNS), creating a shared emotional experience.26 However, cognitive inference is required to project that internal feeling onto the actor.24 Electroencephalography (EEG) data shows a high-amplitude Late Positive Potential (LPP) when faces are preceded by emotional contexts, signaling a complex process of expectation attribution.21 For automated editing, this means that the system must not only match emotional valence but also ensure that the sequence follows a logical narrative structure that permits this "expectation" to form.28

## **Temporal Constraints: Shot Duration in the Era of Short-Form Media**

The Kuleshov Effect was established during an era when the Average Shot Length (ASL) was significantly longer than it is in modern social media.1 In traditional cinema, shots were often held for 5 to 12 seconds to allow the audience to fully absorb the context and the reaction.1 However, the modern media landscape, characterized by attention spans that have reportedly dropped from 12 seconds to approximately 8 seconds, necessitates a much faster editing rhythm.6

### **The 1–3 Second Window and Narrative Efficiency**

Research into high-paced action films and social media content suggests that the Kuleshov Effect remains potent even at extremely short durations.6 In contemporary action climaxes, the ASL frequently falls below 2 seconds.7

| Content Category / Film | Average Shot Length (ASL) | Impact on Narrative Inference |
| :---- | :---- | :---- |
| **Traditional Cinema** | 5.0 \- 12.0 seconds | High cognitive deliberation; deep emotional resonance.1 |
| **Modern Drama (*Marriage Story*)** | 4.12 seconds | Balanced pacing for emotional depth and narrative clarity.7 |
| **Modern Horror (*Get Out*)** | 3.04 seconds | Mix of suspense and abrupt transitions for tension.7 |
| **Modern Action (*Top Gun: Maverick*)** | 1.76 seconds | Relies on "automatic" priming and rapid meaning creation.7 |
| **Short-Form Content (Social Media)** | 1.0 \- 3.0 seconds | Exploits high-density saccadic attention to maintain engagement.6 |

The "minimum shot duration" for narrative inference is surprisingly low. Experimental paradigms have successfully induced the Kuleshov Effect using facial presentations as short as 750 milliseconds, provided they were preceded by a clear 2–4 second contextual stimulus.18 For an automated system, this implies that while the "Context" clip (e.g., the B-Roll or Found Clip) needs sufficient time to establish valence (typically 2-4 seconds), the "Reaction" or "Punchline" can be as short as 1 second without losing its narrative impact.6

### **Bridging Inferences and Saccadic Attention**

The brain handles rapid cutting by treating the "shot change" as an articulation axis.33 Neural patterns in theta synchronization and delta desynchronization are triggered at the cut, facilitating narrative segmentation and memory encoding.33 Even in fast-paced edits, the viewer performs "bridging inferences," where they connect information from the previous shot to the new one to maintain a coherent "event model".33 The higher frequency of cuts in short-form media drives "saccadic attention," keeping the viewer’s brain constantly engaged in the process of making sense of the next image.6

## **Directionality and Asymmetry in Meaning Transfer**

A critical requirement for automated video assembly is understanding the "asymmetry of pairing".15 The order of Shot A and Shot B is not interchangeable; meaning transfer is predominantly unidirectional, flowing from the stimulus to the reaction.15

### **The Stimulus-Response Logic of Point-of-View (POV)**

The most effective Kuleshov sequences follow a specific directional logic:

1. **Shot A (Onlooker):** Establishes the character looking at something.12  
2. **Shot B (Object):** Shows what the character sees (the affective prime).12  
3. **Shot C (Reaction):** Shows the character’s emotional response to the object.12

In this structure, meaning is generated in the "liminal space" between B and C.4 Research has shown that in "Face-Scene-Face" sequences, the second face is interpreted significantly differently than the first, even when the clips are identical.18 The scene "contaminates" the interpretation of the subsequent face.17 For automated systems, this dictates that the "Punchline" or "Found Clip" must be positioned *after* the initial A-Roll setup but *before* the A-Roll reaction to maximize the effect.15

### **The Direction of Contextual Backdrop**

The first shot in a pair serves as a "contextual backdrop" for the second, narrowing the spectrum of potential meanings.34 If a neutral face (Shot A) is followed by a coffin (Shot B), the viewer may infer that the person is *experiencing* loss.15 However, if the coffin (Shot A) is followed by a neutral face (Shot B), the viewer is more likely to infer that the person is *reacting* to the loss with specific emotional labels (e.g., "sadness").15 This directional transfer is the "master key" for manipulating audience perception in the edit.14

## **Emotional Contamination and Affective Priming of B-Roll**

One of the most revolutionary findings for automated B-Roll selection is the concept of "emotional contamination".38 Research into affective priming demonstrates that a highly emotional "prime" (e.g., a passionate A-Roll statement) can alter the perceived valence of a subsequent neutral "probe" (e.g., a generic B-Roll cityscape).38

### **Valence Transfer without Semantic Alignment**

This effect is remarkably robust and does not require semantic similarity between the shots.39

* **Congruency Facilitation:** When a positive voiceover (prime) is paired with a pleasant B-Roll image (probe), response latencies for emotional categorization are shortened.38  
* **Neutral Absorption:** When a neutral B-Roll clip is placed between two emotionally charged A-Roll segments, it "absorbs" the surrounding valence.2 A cityscape clip becomes "misery" when paired with a cold filter and sad music, or "romance" when paired with a warm filter and happy music.15

For an automated editing system, this implies that B-Roll selection can be simplified.5 Instead of searching for a clip that perfectly illustrates the *literal* words of a speaker, the system can prioritize clips that are "semantically neutral" but "compositionally strong," relying on the Kuleshov Effect to provide the necessary emotional color.2 This "writerly text" approach invites the audience to actively participate in creating the connection, leading to a more immersive experience.4

### **Cognitive Load and Contextual Continuity**

To ensure successful contamination, the system must maintain "cinematic continuity".28 Continuity editing aims to make the cuts "invisible" to the viewer, ensuring that the story flows naturally across different spaces and times.13

* **180-Degree Rule:** Preserving spatial clarity to ensure the viewer knows who is looking at what.13  
* **Eyeline Match:** Using the direction of a character's gaze to "cue" the viewer to anticipate the next shot.13  
* **Match-on-Action:** Using a single continuous action to bridge separate shots, making the edit feel seamless.36

## **Cross-Modal Kuleshov: The Role of Audio-Visual Juxtaposition**

The original Kuleshov experiments were silent, but modern research has extended the principle to the auditory domain, discovering a "Cross-modal Kuleshov Effect".1 This is particularly relevant for automated social media videos, which often feature a voiceover (A-Roll) layered over diverse footage (B-Roll).5

### **The Auditory Kuleshov Effect**

Nondiegetic sound, such as music or a speaker's voice, serves as an "affective primer" that influences evaluations of visual stimuli.37 Research by Baranowski and Hecht (2017) demonstrated that happy or sad music could significantly alter the perceived expression of a neutral face, even when the visual context was held constant.1

| Auditory Context | Impact on Visual Stimulus | Neural/Behavioral Result |
| :---- | :---- | :---- |
| **Congruent Music** | Enhances the intensity of the perceived emotion (e.g., Happy Music \+ Happy Face). | Increased heart rate and skin conductance; activation in Amygdala and Fusiform Gyrus.37 |
| **Incongruent Music** | Creates a "paradox result" where the auditory valence can override the visual expression. | Higher activation in regions involved in processing incongruent facial info.37 |
| **Neutral B-Roll \+ Music** | Gives specific meaning to ambiguous visual situations. | The "intersensory cross-talk" creates a new, emergent emotional state.37 |

In automated editing, a "coach’s voice" over B-Roll acts as the primary narrative anchor.45 The voiceover establishes the emotional "ground truth," and the B-Roll serves as a "visual metaphor".45 The audience automatically seeks to create a logical link between the voice and the images, meaning that even "generic" nature footage can feel profound when paired with the right words.5

### **L-Cuts and J-Cuts: Smoothing the Cross-Modal Cut**

Sophisticated editing techniques like L-cuts (audio from the next scene begins before the visual cut) and J-cuts (audio from the preceding scene continues after the visual cut) are essential for cross-modal integration.13 These transitions allow the auditory cues to guide the audience’s expectations before the visual transition occurs, making the Kuleshov link feel "natural" rather than forced.13

## **Cultural Dependency and the Universality of Juxtaposition**

A central concern for automated systems is whether the meanings generated by juxtaposition are universal or culturally bound.2 Research suggests that while the *capacity* for the Kuleshov Effect is universal, the *specific interpretation* can be influenced by cultural context and cinematic literacy.2

### **Universality of Basic Emotional Triggers**

Basic emotional links—such as the association between a **coffin and grief** or **food and hunger**—appear to be universally accepted.5 Qualitative studies conducted across four continents (Europe, North America, Asia, and Africa) found that consensus on the perceived emotion in Kuleshov-style sequences was remarkably stable.48 This suggests that the brain’s ability to use context for social attribution is a fundamental evolutionary trait rather than a learned cultural behavior.27

### **The Role of Cinematic Literacy and Experience**

However, "cinematic literacy" does affect the *strength* and *complexity* of the inferences made.22

* **Experienced Viewers:** Readily construct spatiotemporal links and accept "creative geography" (e.g., cutting from a Moscow street to the White House steps).16  
* **First-Time Viewers:** Struggle to perceive continuity between adjacent shots, often viewing them as independent, unrelated events.22  
* **Cultural Nuance:** While basic valence (positive/negative) is universal, the specific "labeling" of an emotion (e.g., "sarcasm" vs. "disgust") may vary based on cultural norms and social factors like group identity and relationship intimacy.27

For social media automation, this means that while "Found Clip" punchlines should rely on universal archetypes (e.g., someone falling, a cute animal, a clear visual metaphor), more subtle emotional nuances should be carefully tailored to the target demographic's "cinematic language".2

## **Practical Implications for Automated B-Roll Ordering**

Given a library of ![][image1] candidate B-Roll clips, how should an algorithm decide their sequence for maximum emotional impact? Research into "emotional sequencing" provides concrete heuristics for narrative assembly.49

### **Heuristics for Emotional Progression**

A 2025 study on disinformation and emotional manipulation on social networks identified specific "temporal orders" of emotions that drive engagement and virality.49 These findings can be adapted for positive narrative construction in automated editing.

| Sequencing Rule | Behavioral Pattern | Practical Application in Automated Editing |
| :---- | :---- | :---- |
| **The Rule of Three** | Reliable news/narratives rarely exceed 3 distinct emotional categories in a sequence. | Limit each 4–7 scene video to 2–3 core emotional "beats" to maintain coherence.49 |
| **Binary Transitioning** | Sequences like **Fear → Anger** or **Joy → Sadness** are highly engaging. | Use a "Stylized Mismatch" template to pivot between high-arousal emotions.4 |
| **Cyclic Progression** | Cyclic patterns (returning to a core emotion) sustain attention in short-form content. | Return to a consistent A-Roll "Reaction" shot after every 2–3 B-Roll clips.49 |
| **Density Heuristic** | High-arousal negative emotions (Fear/Anger) require faster cutting (1.5-2s ASL). | Speed up the edit during high-tension A-Roll segments; slow it down for "Calm" segments.7 |
| **Confidence in Clips** | Combinations of {Disgust, Fear, Anger} are statistically linked to high-engagement. | For a "JUXTAPOSITION" template, pair a "shocker" Found Clip with a "fearful" A-Roll reaction.49 |

### **Algorithmic Logic for Asset Pairing**

1. **Prioritize Affective Priming:** If the A-Roll is emotionally charged, follow it with a neutral B-Roll shot to allow "contamination" to occur.5  
2. **Use "Creative Geography":** If assets were filmed in different locations, use a consistent color filter and continuous voiceover to trick the audience into believing they exist in the same space.15  
3. **Exploit the "Writerly Text":** Do not make every connection literal. By presenting juxtaposed shots without explicit explanation, the algorithm invites the audience to "fill in the gaps," leading to higher mental engagement.4  
4. **Sequential Probabilistic Modeling:** Use "dynamic state occupancy probabilities" to ensure that the temporal dynamics of the brain (the BOLD signal trajectory) remain consistent across the video's duration.51

## **Strategic Conclusions for Automated Systems**

The Kuleshov Effect is not merely an editing trick; it is the neurobiological "operating system" through which humans consume and understand visual narratives.9 For an automated video editing system for social media, the implications are profound:

* **Relationship \> Content:** The meaning of a scene is determined by its *placement* in the sequence, not by its individual pixels.1 An automated system can generate high-value content using "generic" assets if the juxtaposition logic is sound.2  
* **The Power of the Prime:** The first shot in any pair (or the voiceover) sets the "affective expectation" for the second.9 Algorithms should be designed to prioritize the "Context" first to prime the interpretation of the "Reaction."  
* **Temporal Compression as a Feature:** Fast editing (1–3s ASL) is not a limitation; it is a tool for driving saccadic attention and maintaining narrative tension in a low-attention-span environment.6  
* **Universal Archetypes over Cultural Specifics:** To maximize global reach, automated assembly should rely on universal Kuleshov triggers (Hunger, Grief, Fear, Joy) that have been validated to transcend cultural boundaries.47

By codifying these cognitive mechanics into a sequential optimization problem, an automated system can transition from simple "video-making" to "narrative-crafting," creating content that feels as if it were meticulously assembled by a human master of the craft.4 The Kuleshov Effect remains the "magic" of cinema, now rendered as a set of actionable, empirical heuristics for the digital age.14

#### **Sources des citations**

1. Kuleshov effect \- Wikipedia, consulté le mars 23, 2026, [https://en.wikipedia.org/wiki/Kuleshov\_effect](https://en.wikipedia.org/wiki/Kuleshov_effect)  
2. Kuleshov effect | Film History and Form Class Notes |... \- Fiveable, consulté le mars 23, 2026, [https://fiveable.me/film-history-and-form/unit-10/kuleshov-effect/study-guide/bKORpwu3pl6rkfdo](https://fiveable.me/film-history-and-form/unit-10/kuleshov-effect/study-guide/bKORpwu3pl6rkfdo)  
3. Understanding the Kuleshov Effect \- A Filmmaker's Powerful Tool : r/directors \- Reddit, consulté le mars 23, 2026, [https://www.reddit.com/r/directors/comments/1i4zhih/understanding\_the\_kuleshov\_effect\_a\_filmmakers/](https://www.reddit.com/r/directors/comments/1i4zhih/understanding_the_kuleshov_effect_a_filmmakers/)  
4. Get Your Shots in Order With This Guide to the Kuleshov Effect \- Backstage, consulté le mars 23, 2026, [https://www.backstage.com/magazine/article/kuleshov-effect-guide-77088/](https://www.backstage.com/magazine/article/kuleshov-effect-guide-77088/)  
5. The Kuleshov Effect: A powerful tool in video makers' toolkit \- Storyblocks, consulté le mars 23, 2026, [https://www.storyblocks.com/resources/blog/kuleshov-effect](https://www.storyblocks.com/resources/blog/kuleshov-effect)  
6. Chase Adamek Clemson University World Cinema and Psychology Undergraduate Research 3 December 2021 The Kuleshov Affect: Emotion \- Squarespace, consulté le mars 23, 2026, [https://static1.squarespace.com/static/61dca6b26c1e45622d05fab7/t/61f0be6289444664fb82e203/1643167330984/The+Kuleshov+Affect+-+Emotional+Stimulation+in+Montage+Editing.pdf](https://static1.squarespace.com/static/61dca6b26c1e45622d05fab7/t/61f0be6289444664fb82e203/1643167330984/The+Kuleshov+Affect+-+Emotional+Stimulation+in+Montage+Editing.pdf)  
7. Fall 2025: Joey Fisher | The Elon Journal, consulté le mars 23, 2026, [https://www.elon.edu/u/academics/communications/journal/archive/fall-2025/fall-2025-joey-fisher/](https://www.elon.edu/u/academics/communications/journal/archive/fall-2025/fall-2025-joey-fisher/)  
8. EditIQ: Automated Cinematic Editing of Static Wide-Angle Videos via Dialogue Interpretation and Saliency Cues \- CVIT, IIIT, consulté le mars 23, 2026, [https://cvit.iiit.ac.in/images/ConferencePapers/2025/EditIQ.pdf](https://cvit.iiit.ac.in/images/ConferencePapers/2025/EditIQ.pdf)  
9. The Kuleshov Effect: the influence of contextual framing on emotional attributions \- PubMed, consulté le mars 23, 2026, [https://pubmed.ncbi.nlm.nih.gov/17339967](https://pubmed.ncbi.nlm.nih.gov/17339967)  
10. Does the Kuleshov effect really exist? Revisiting a classic film experiment on facial expressions and emotional contexts \- Lund University Research Portal, consulté le mars 23, 2026, [https://portal.research.lu.se/en/publications/does-the-kuleshov-effect-really-exist-revisiting-a-classic-film-e/](https://portal.research.lu.se/en/publications/does-the-kuleshov-effect-really-exist-revisiting-a-classic-film-e/)  
11. Reexamining the Kuleshov effect: Behavioral and neural evidence from authentic film experiments, consulté le mars 23, 2026, [https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0308295\&type=printable](https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0308295&type=printable)  
12. Kuleshov Effect: Everything You Need to Know \- NFI \- Nashville Film Institute, consulté le mars 23, 2026, [https://www.nfi.edu/kuleshov-effect/](https://www.nfi.edu/kuleshov-effect/)  
13. The Art of The Cut & Continuity (Kuleshov Effect) \- HUFOCW, consulté le mars 23, 2026, [https://www.hufocw.org/Download/file/30832](https://www.hufocw.org/Download/file/30832)  
14. What Is The Kuleshov Effect & Why Is It So Efficient? \- TheCollector, consulté le mars 23, 2026, [https://www.thecollector.com/what-is-the-kuleshov-effect/](https://www.thecollector.com/what-is-the-kuleshov-effect/)  
15. Kuleshov Effect \- Film School \- WeVideo, consulté le mars 23, 2026, [https://www.wevideo.com/blog/kuleshov-effect](https://www.wevideo.com/blog/kuleshov-effect)  
16. Kuleshov's Experimentations: How Did Film Transfer To Art Theory? \- Digital Converters, consulté le mars 23, 2026, [https://digitalconverters.co.uk/blog/kuleshovs-experimentations-how-did-film-transfer-to-art-theory](https://digitalconverters.co.uk/blog/kuleshovs-experimentations-how-did-film-transfer-to-art-theory)  
17. Revisiting the Kuleshov effect with authentic films: A behavioral and fMRI study, consulté le mars 23, 2026, [https://www.researchgate.net/publication/376246155\_Revisiting\_the\_Kuleshov\_effect\_with\_authentic\_films\_A\_behavioral\_and\_fMRI\_study](https://www.researchgate.net/publication/376246155_Revisiting_the_Kuleshov_effect_with_authentic_films_A_behavioral_and_fMRI_study)  
18. Reexamining the Kuleshov effect: Behavioral and neural evidence from authentic film experiments \- ResearchGate, consulté le mars 23, 2026, [https://www.researchgate.net/publication/382881080\_Reexamining\_the\_Kuleshov\_effect\_Behavioral\_and\_neural\_evidence\_from\_authentic\_film\_experiments](https://www.researchgate.net/publication/382881080_Reexamining_the_Kuleshov_effect_Behavioral_and_neural_evidence_from_authentic_film_experiments)  
19. Does the Kuleshov Effect Really Exist? Revisiting a Classic Film Experiment on Facial Expressions and Emotional Contexts \- PubMed, consulté le mars 23, 2026, [https://pubmed.ncbi.nlm.nih.gov/27056181/](https://pubmed.ncbi.nlm.nih.gov/27056181/)  
20. The Kuleshov Effect: the influence of contextual framing on emotional attributions \- PMC, consulté le mars 23, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC1810228/](https://pmc.ncbi.nlm.nih.gov/articles/PMC1810228/)  
21. Revisiting the Kuleshov effect with authentic films: A behavioral and fMRI study | bioRxiv, consulté le mars 23, 2026, [https://www.biorxiv.org/content/10.1101/2023.12.04.569135v1.full](https://www.biorxiv.org/content/10.1101/2023.12.04.569135v1.full)  
22. Reexamining the Kuleshov effect: Behavioral and neural evidence from authentic film experiments \- PMC, consulté le mars 23, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC11299807/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11299807/)  
23. Reexamining the Kuleshov effect: Behavioral and neural evidence from authentic film experiments \- PubMed, consulté le mars 23, 2026, [https://pubmed.ncbi.nlm.nih.gov/39102395/](https://pubmed.ncbi.nlm.nih.gov/39102395/)  
24. An examination of the Kuleshov effect using still photographs \- PMC, consulté le mars 23, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC6822748/](https://pmc.ncbi.nlm.nih.gov/articles/PMC6822748/)  
25. How Context Influences Our Perception of Emotional Faces: A Behavioral Study on the Kuleshov Effect \- Frontiers, consulté le mars 23, 2026, [https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2017.01684/full](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2017.01684/full)  
26. A scoping review of emotional contagion research with human subjects: identifying common trends of previous research and potential areas for future research \- Frontiers, consulté le mars 23, 2026, [https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2025.1573375/full](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2025.1573375/full)  
27. The role of self-representation in emotional contagion \- Frontiers, consulté le mars 23, 2026, [https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2024.1361368/full](https://www.frontiersin.org/journals/human-neuroscience/articles/10.3389/fnhum.2024.1361368/full)  
28. Context shapes evaluation of emotional valence, not emotional categorization: A fresh look at the Kuleshov effect \- PMC, consulté le mars 23, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12972553/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12972553/)  
29. Context shapes evaluation of emotional valence, not emotional categorization: A fresh look at the Kuleshov effect \- PubMed, consulté le mars 23, 2026, [https://pubmed.ncbi.nlm.nih.gov/41815739/](https://pubmed.ncbi.nlm.nih.gov/41815739/)  
30. On Shot Lengths and Film Acts: A Revised View \- ResearchGate, consulté le mars 23, 2026, [https://www.researchgate.net/publication/236964224\_On\_Shot\_Lengths\_and\_Film\_Acts\_A\_Revised\_View](https://www.researchgate.net/publication/236964224_On_Shot_Lengths_and_Film_Acts_A_Revised_View)  
31. Perceptual oddities: assessing the relationship between film editing ..., consulté le mars 23, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC10725757/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10725757/)  
32. Statistical Style Analysis of Hindi Biopics: Exploring the Genre Conventions in Recent Years, consulté le mars 23, 2026, [https://www.researchgate.net/publication/354824494\_Statistical\_Style\_Analysis\_of\_Hindi\_Biopics\_Exploring\_the\_Genre\_Conventions\_in\_Recent\_Years](https://www.researchgate.net/publication/354824494_Statistical_Style_Analysis_of_Hindi_Biopics_Exploring_the_Genre_Conventions_in_Recent_Years)  
33. An exploration of the editing cut as an articulator in film through frequency domain analysis of spectator EEGs \- PMC, consulté le mars 23, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12267235/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12267235/)  
34. Point-of-view Shots in Light of Cognitive Grammar \- Googleapis.com, consulté le mars 23, 2026, [https://padlet-uploads.storage.googleapis.com/2465321737/92588208fd0b44502362a25be36e4234/Point\_of\_view\_Shots\_in\_Light\_of\_Cognitive\_Grammar.pdf](https://padlet-uploads.storage.googleapis.com/2465321737/92588208fd0b44502362a25be36e4234/Point_of_view_Shots_in_Light_of_Cognitive_Grammar.pdf)  
35. An examination of the Kuleshov effect using still photographs | PLOS One, consulté le mars 23, 2026, [https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0224623](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0224623)  
36. Editing – Introduction to Film & TV \- OPEN OKSTATE, consulté le mars 23, 2026, [https://open.library.okstate.edu/introfilmtv/part/editing/](https://open.library.okstate.edu/introfilmtv/part/editing/)  
37. The Auditory Kuleshov Effect: Multisensory Integration in Movie Editing \- Uni Mainz, consulté le mars 23, 2026, [https://experimental.psychologie.uni-mainz.de/files/2024/06/2017baranowski-kuleshov.pdf](https://experimental.psychologie.uni-mainz.de/files/2024/06/2017baranowski-kuleshov.pdf)  
38. Affective Priming by Biological Motion | JOV \- Journal of Vision, consulté le mars 23, 2026, [https://jov.arvojournals.org/article.aspx?articleid=2144897](https://jov.arvojournals.org/article.aspx?articleid=2144897)  
39. Affective Priming with Pictures of Emotional Scenes: The Role of Perceptual Similarity and Category Relatedness, consulté le mars 23, 2026, [https://revistas.ucm.es/index.php/SJOP/article/download/SJOP0606120010A/29048](https://revistas.ucm.es/index.php/SJOP/article/download/SJOP0606120010A/29048)  
40. Affective Priming with Pictures of Emotional Scenes: The Role of Perceptual Similarity and Category Relatedness \- Redalyc.org, consulté le mars 23, 2026, [https://www.redalyc.org/pdf/172/17290102.pdf](https://www.redalyc.org/pdf/172/17290102.pdf)  
41. Positive affective priming decreases the middle late positive potential response to negative images \- PMC, consulté le mars 23, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC6346648/](https://pmc.ncbi.nlm.nih.gov/articles/PMC6346648/)  
42. Download \- HUFOCW, consulté le mars 23, 2026, [https://www.hufocw.org/Download/file/30812](https://www.hufocw.org/Download/file/30812)  
43. Bordwell, D & Thompson, K 2013, 'Chapter 6 The relation of shot and shot: editing', Film Art: An Introduction, 10th ed, McGraw Hill, New York, pp. 218-265 \- Media Factory, consulté le mars 23, 2026, [https://www.mediafactory.org.au/2016-cut-v-shot/2016/05/27/bordwell-d-thompson-k-2013-chapter-6-the-relation-of-shot-and-shot-editing-film-art-an-introduction-10th-ed-mcgraw-hill-new-york-pp-218-265/](https://www.mediafactory.org.au/2016-cut-v-shot/2016/05/27/bordwell-d-thompson-k-2013-chapter-6-the-relation-of-shot-and-shot-editing-film-art-an-introduction-10th-ed-mcgraw-hill-new-york-pp-218-265/)  
44. Kuleshov Effect – A video editor's most powerful tool \- YouTube, consulté le mars 23, 2026, [https://www.youtube.com/watch?v=MHcr19dejyw](https://www.youtube.com/watch?v=MHcr19dejyw)  
45. B-Roll with a Voiceover \- YouTube, consulté le mars 23, 2026, [https://www.youtube.com/watch?v=ZmV8YHVRyqY](https://www.youtube.com/watch?v=ZmV8YHVRyqY)  
46. Revisiting the Kuleshov Effect with First-Time Viewers \- SciSpace, consulté le mars 23, 2026, [https://scispace.com/pdf/revisiting-the-kuleshov-effect-with-first-time-viewers-3rnguwgxgo.pdf](https://scispace.com/pdf/revisiting-the-kuleshov-effect-with-first-time-viewers-3rnguwgxgo.pdf)  
47. BPhil Kuleshov Effect | PDF | Emotions | Perception \- Scribd, consulté le mars 23, 2026, [https://www.scribd.com/document/401599335/BPhil-Kuleshov-Effect](https://www.scribd.com/document/401599335/BPhil-Kuleshov-Effect)  
48. (PDF) Aesthetics and action: situations, emotional perception and the Kuleshov effect, consulté le mars 23, 2026, [https://www.researchgate.net/publication/330989335\_Aesthetics\_and\_action\_situations\_emotional\_perception\_and\_the\_Kuleshov\_effect](https://www.researchgate.net/publication/330989335_Aesthetics_and_action_situations_emotional_perception_and_the_Kuleshov_effect)  
49. Emotional Sequencing as a Marker of Manipulation in Social Media ..., consulté le mars 23, 2026, [https://www.mdpi.com/1999-5903/17/12/546](https://www.mdpi.com/1999-5903/17/12/546)  
50. Ratings for Emotion Film Clips \- PMC \- NIH, consulté le mars 23, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC6445277/](https://pmc.ncbi.nlm.nih.gov/articles/PMC6445277/)  
51. Variation is the Norm: Brain State Dynamics Evoked By Emotional Video Clips \- PMC, consulté le mars 23, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC8784974/](https://pmc.ncbi.nlm.nih.gov/articles/PMC8784974/)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABIAAAAXCAYAAAAGAx/kAAABGElEQVR4Xu3SMWoCURAG4AkmhWJQK7FTCyEQsPAMgmlSpAiKpa0kpVYStEkhiGkC6cUrpMgBAjlALmBlI9gpaPx/3yxO1pUtLPWHr3De+HZ33hM5mTTUh2pD1KxnYai8nldImp5tWKA7mMMKymb9CnLqC54gAxHT8y816MAMxnBp1q7VG6RMPTBHb3Sh+N0FcZtws1vTc6P64noDwyfQAOJQgTW8mJ4HVTe1vZRUS38n4Bt+Ia21rmLfwXA2dG9qTfiDquxmEzofzobyps6jnsCnuLfgbELnw9l48/HCP/RgIe4Ccjah8/G+3x+eGk+Pl7SoAsOnPsOj8of3iFfhR3Ynuxce5VTcQJdqBDHbJO4qvPtq55zDbAB7gDMYHgeMRgAAAABJRU5ErkJggg==>