# **Neuro-Computational Dynamics of Film Editing: 1/f Shot Patterns, Attentional Synchrony, and the Optimization of Short-Form Video Pacing**

The convergence of cinematic language and human neurobiology suggests that film editing is not merely a creative endeavor but an evolutionary process that has gradually aligned with the endogenous rhythms of human attention.1 Research conducted by James Cutting and his colleagues at Cornell University reveals that successful Hollywood films have increasingly adopted a specific temporal structure known as a 1/f or "pink noise" pattern.3 This fractal arrangement, characterized by self-similarity across multiple timescales, appears to reflect the optimal state of engagement for the human brain, balancing the monotony of predictable repetition with the disorientation of random sequences.1 As digital consumption shifts toward short-form social media video—typically ranging from 60 to 180 seconds—it is necessary to deconstruct these feature-length principles and apply them to the micro-scale timing of automated video generation systems.6

## **The Evolution of the Cinematic Mind: 1/f Patterns and Shot Duration**

The 1/f pattern, or pink noise, is a hallmark of complexity found throughout the natural and social worlds, from the pulsing of pulsars and human heartbeats to the fluctuations of the stock market.1 In the context of film, this pattern describes the serial relationship between the lengths of successive shots.5 James Cutting’s longitudinal analysis of 150 popular Hollywood films released between 1935 and 2005 demonstrates a definitive trend toward this pattern, suggesting that filmmakers have intuitively discovered a mathematical structure that effectively "harnesses" viewer attention.3

## **Methodology of the Cornell Shot Duration Studies**

The methodology employed by Cutting and his team involved a massive computational and manual parsing of shot transitions across 70 years of cinema.1 Using a mixture of algorithmic cut detection and human confirmation, the researchers recorded every individual cut and deduced the true shot lengths for 150 films.9 These films were selected based on high box-office performance across five major genres: action, adventure, animation, comedy, and drama.2

To identify the 1/f pattern, the sequence of shot lengths for each film was treated as a time-series vector.1 This vector was decomposed using Fourier analysis to identify constituent sine waves.1 The power spectral density (![][image1]) of these waves was then analyzed according to the frequency (![][image2]):

![][image3]  
In this formula, ![][image4] is a constant and ![][image5] (alpha) represents the slope of the power spectrum.4 A value of ![][image6] corresponds to white noise, where shot lengths are independent and random, while ![][image7] corresponds to brown noise (Brownian motion), where shot lengths are highly predictable and drifting.13 The 1/f pattern occurs when ![][image5] approaches 1.0, creating a "pink noise" signature where temporal variation exists at every scale—from clusters of rapid cuts to longer, lingering takes—in a way that mimics the fluctuations of human reaction times and neural firing rates.5

| Genre | Closeness to 1/f Pattern (Rank) | Representative Film Example |
| :---- | :---- | :---- |
| Action | 1 | *The Perfect Storm* (2000) 2 |
| Adventure | 2 | *Back to the Future* (1985) 1 |
| Animation | 3 | *The Lion King* (1994) 4 |
| Comedy | 4 | *Rebel Without a Cause* (1955) 11 |
| Drama | 5 | *Asphalt Jungle* (1955) 4 |

The analysis revealed that while early films showed considerable variation, movies produced after 1980 were significantly more likely to approach the 1/f universal constant.2 This shift suggests a "natural selection" in filmmaking, where edited rhythms that failed to align with human attentional waves were less successful in producing coherent, gripping narratives.1

## **The Longitudinal Decline of Average Shot Length (ASL)**

Parallel to the convergence toward 1/f patterns is a radical acceleration in the pace of editing. Historically, average shot length (ASL) in Hollywood has seen a steady and essentially linear decrease over the last 75 years.5

| Decade | Average Shot Length (ASL) | Perceptual Context |
| :---- | :---- | :---- |
| 1930s | \~10.0 \- 12.0 Seconds | Early sound era, static camera 1 |
| 1950s | \~8.0 \- 10.0 Seconds | Wider screens, complex blocking 16 |
| 1970s | \~5.0 \- 7.0 Seconds | New Hollywood, increased mobility 17 |
| 2010s | \~3.0 \- 4.0 Seconds | High visual activity, digital editing 1 |

This decrease is often attributed to technological shifts, such as the introduction of lightweight cameras and digital non-linear editing (NLE) systems, which allow for a greater volume of cuts and more precise timing.4 However, the research emphasizes that shorter shots are not inherently "better." Instead, it is the *pattern* of these shots—their autocorrelation with neighboring shots—that determines engagement.1 Modern films are not just faster; they are more "fractal," meaning they maintain long-range dependencies where the duration of a shot is statistically related to shots that occurred much earlier in the sequence.8

## **Fractal Dynamics at the Micro-Scale: Short-Form Social Video**

A central challenge for automated editing systems is determining whether 1/f principles, derived from feature-length films, remain valid for short-form content (60–180 seconds). The evidence suggests that the 1/f structure is fundamentally scale-invariant.16 Because it is a fractal pattern, the same proportional relationship between short and long durations exists whether the window of observation is two hours or two minutes.4

## **Scale Invariance and Event Perception**

Psychological research into event perception indicates that the "working human mind" processes experiences as a sequence of units.18 Most experiments in cognitive psychology focus on events that are only a few minutes in length, aligning perfectly with the temporal scope of short-form social media videos.3 Cutting notes that scenes—the fundamental building blocks of films—typically last between a few seconds and a few minutes, and it is within these scenes that the 1/f fluctuations are most effectively utilized to maintain narrative grip.3

For a 60-second TikTok or Instagram Reel, applying 1/f timing requires moving away from "metronomic" pacing (e.g., cutting every 2 seconds) or "random" pacing.19 Instead, the sequence of shot durations should be generated using a pink noise algorithm, ensuring that:

1. **Short-Range Correlation:** A very short shot is more likely to be surrounded by other relatively short shots (creating a "staccato" cluster).8  
2. **Long-Range Variation:** These clusters are punctuated by longer "anchor" shots that allow for cognitive "resetting" and deeper processing of complex visual information.19

## **Cut Rate and Engagement Benchmarks in Social Media**

In contemporary social media environments, the "cut rate" (cuts per minute) is a primary driver of retention.22 High-energy formats like TikTok and YouTube Shorts favor rapid visual change to prevent the viewer's attention from drifting during the "infinite scroll".23

| Platform | Avg. Engagement Rate (2025-2026) | Optimal Video Length | Target Completion Rate |
| :---- | :---- | :---- | :---- |
| TikTok | 3.70% \- 4.90% | 60 \- 90 Seconds | 75%+ for Virality 25 |
| Instagram Reels | 0.48% \- 1.48% | 60 \- 90 Seconds | 30% \- 40% 26 |
| YouTube Shorts | 5.91% | \~60 Seconds | 50% \- 70% 26 |
| Facebook Reels | 0.15% \- 2.18% | \< 30 Seconds | N/A 26 |

The relationship between cut density and virality is evidenced by the fact that using jump cuts—which remove pauses or redundant frames—increases completion rates by an average of 26%.22 Furthermore, videos that maintain a high visual activity index (VAI), incorporating both actor motion and camera movement, are more likely to achieve sustained exposure on the "For You Page" (FYP).5

## **Attentional Synchrony and the "Tyranny of Film"**

The primary mechanism by which 1/f editing influences behavior is "attentional synchrony"—the phenomenon where multiple viewers look at the same place on the screen at the same time.30 Professionally edited content, particularly Hollywood trailers, elicits a significantly higher degree of synchrony than natural dynamic scenes or static images.30

## **Exogenous Control of Gaze**

Cuts act as exogenous triggers that reset the viewer's gaze, typically centering it on the screen to search for new information.32 This effect is so pronounced it has been termed the "Tyranny of Film Hypothesis," proposing that editing techniques exert almost total control over the viewer's oculomotor behavior.30 When cuts follow a 1/f pattern, the timing of these resets aligns with the brain's internal attentional refresh rate, reducing the cognitive load required to "follow" the narrative.1

Research using eye-tracking data shows that:

1. **Cluster Tightness:** Fixations are most tightly clustered immediately following a cut and gradually disperse as the shot continues.32  
2. **Narrative Comprehension:** In adults, attentional synchrony is driven by both bottom-up perceptual features (motion, contrast) and top-down understanding of the montage.33  
3. **Subtitle Impact:** The presence of on-screen text or subtitles alters eye movement patterns, forcing a gaze shift from the center to the bottom and back, which can disrupt synchrony if not timed with shot changes.22

## **Clutter Cost and the Scale-Duration Rule**

James Cutting’s research on "clutter cost" provides a quantitative guideline for how long a shot *needs* to be based on its visual complexity.35 In a study of 31,000 shots from movies made between 1940 and 2010, the researchers found a strict relationship between shot scale and duration: the larger the subject in the frame (e.g., a close-up), the shorter the shot can be.35

| Shot Scale | Subject Size in Frame | Processing Time (Cognitive Load) | Editing Implication |
| :---- | :---- | :---- | :---- |
| Extreme Close-Up (ECU) | Tiny detail (eye/mouth) | Very Low | Can be ultra-brief (\< 15 frames) 35 |
| Close-Up (CU) | Full face | Low | Fast staccato cuts work well 35 |
| Medium Shot (MS) | Waist up | Moderate | Needs 1.5x \- 2x duration of CU 35 |
| Long Shot (LS) | Full body | High | Requires longer holding time 35 |
| Extreme Long Shot (ELS) | Small subject / Landscape | Very High | Must be held for context 35 |

Visual clutter—defined as distracting objects, shadows, or textures surrounding the subject—increases the time required for a viewer to recognize emotions or key actions.35 For automated systems, a "pacing characteristic" must not be applied blindly. A "fast staccato" template applied to an extreme long shot with high clutter will lead to "perceptual failure," where the viewer skips the content because they literally could not "see" the point of the shot before it ended.35

## **The First 3 Seconds: The Neuro-Cognitive Triage**

In the high-velocity environment of social media, the 1/f pattern is subject to a "front-loading" requirement.24 The first 3 seconds of a video are the most critical, serving as a triage window where the viewer's brain decides whether to invest attention or scroll.39

## **The 1.7-Second Threshold**

On mobile devices, users spend an average of only 1.7 seconds on a piece of content before deciding to skip.41 Therefore, the "hook" must be delivered in "second zero".24 Data from Facebook reveals a clear retention hierarchy: if a viewer passes the 3-second mark, they have a 65% chance of watching for 10 seconds, and a 45% chance of reaching 30 seconds.39

Successful 3-second hooks typically employ:

1. **Visual Pattern Interrupts:** Bold colors, high contrast, or unexpected motion that breaks the visual routine of the feed.40  
2. **Immediate Value Proposition:** Showing the "result" or "payoff" first, then explaining the process (e.g., showing a finished meal before the cooking tutorial).43  
3. **Low Clutter / High Scale:** Starting with a clean close-up or a "hero shot" reduces processing time and increases the probability of an immediate emotional connection.35

| Retention Metric | Benchmark for Well-Optimized Content |
| :---- | :---- |
| 3-Second View Rate | 70% \- 80% 45 |
| 60-Second Retention | High Comment Rates / Algorithmic Promotion 29 |
| Video Completion Rate (VCR) | 40% \- 60% 26 |

A common pitfall is the use of extended logos or slow-motion intros, which viewers perceive as "dead time" or "filler," triggering an immediate scroll response.43

## **Audio-Visual Synchronization and Sonic Story Arcs**

The interaction between music and visual rhythm is mediated by "auditory driving," where the tempo and arousal level of the music dictate the viewer's perception of time.47 Higher arousal music (high BPM, high volume) is associated with "time flying faster," but it also leads to duration overestimations in memory.47

## **Beat vs. Phrase Synchronization**

For automated sequencing, the choice between cutting on the "beat" (the metronomic pulse) and the "musical phrase" (the narrative structure of the song) is pivotal.48

* **Beat Synchronization:** Aligning cuts with the rhythmic pulse (e.g., every 1/4 or 1/8 note) creates a high-energy, "staccato" feel. This is ideal for the first 3-15 seconds to establish momentum.20  
* **Phrase Synchronization:** Aligning transitions with musical section boundaries (e.g., the transition from a verse to a chorus) creates a sense of resolution and story progression.48

Automated systems should utilize a "hierarchical video parsing" approach.7 This involves:

1. **Micro-Timing:** Synchronizing "hit points" (impactful visual events like a high-five or a jump) precisely with the beat.7  
2. **Macro-Timing:** Using the 1/f pattern to determine the *probability* of a cut on any given beat, ensuring that the rhythm is not "cookie-cutter" or overly predictable.1

## **BPM and Cut Frequency Relationship**

The "Sonic Story Arc" should guide the intensity of the edit. As BPM increases (e.g., 60 to 140 BPM), the cut frequency should generally increase to maintain "rhythmic consistency".7 However, cutting on every single beat of a fast 140 BPM track for 60 seconds is fatiguing; instead, the 1/f principle suggests "syncopation"—clusters of fast cuts followed by longer holds that align with musical phrase boundaries.20

| Music Tempo (BPM) | Ideal "Base" Cut Frequency | Editing Characteristic |
| :---- | :---- | :---- |
| 60 \- 80 (Chill/Lo-fi) | 1 cut every 4 \- 6 seconds | Narrative, atmospheric 19 |
| 90 \- 110 (Pop/Standard) | 1 cut every 2 \- 4 seconds | Engaging, balanced 19 |
| 120 \- 140+ (High Energy) | 1 cut every 0.5 \- 2 seconds | Intense, action-driven 7 |

## **Quantitative Synthesis: Insights for Automated Sequencing**

The research by James Cutting and the subsequent analysis of social media engagement provides a robust framework for the automated sequencing of short-form video. The "optimal" cut rhythm is not a static number but a dynamic, self-similar structure that adapts to visual and auditory context.

## **The 1/f Algorithmic Framework**

To implement a 1/f timing principle in a 60-180 second video, the system should follow these second-order logic steps:

1. **Generate the Duration Vector:** Use a Voss-McCartney or inverse-FFT algorithm to produce a series of durations where the power spectrum slope ![][image8]. This ensures the "natural" feel of the edit.13  
2. **Modulate by Visual Complexity:** Adjust each generated duration based on the "clutter" and "scale" of the selected shot. If the 1/f algorithm proposes a 15-frame shot, but the template is a cluttered "Extreme Long Shot," the system should override the duration or select a "Close-Up" shot to match the brief window.35  
3. **Front-Load the Hook:** Ensure the first 3 seconds contain at least one major "pattern interrupt" and a high VAI. Avoid logos or slow-build intros in this window.41  
4. **Align with the Sonic Story Arc:** Snap the 1/f durations to the nearest musical beat or sub-beat, but prioritize "phrase boundaries" for major scene changes.7  
5. **Calculate the Visual Activity Index (VAI):** Ensure that the median correlation across frames is low, indicating sufficient motion and movement to maintain high "attentional synchrony".5

## **Summary of Engagement Thresholds**

| Metric | Target Value | Strategic Goal |
| :---- | :---- | :---- |
| Average Shot Length (ASL) | 2.5 \- 4.5 Seconds | Maintain modern viewer expectations 1 |
| Cut Rate (Cuts/Min) | 15 \- 25 (Niche dependent) | Maximize TikTok/Reels retention 22 |
| 3-Second Retention | \> 70% | Secure algorithmic distribution 45 |
| Attentional Synchrony | High (Clustered Gaze) | Induce the "Tyranny of Film" 30 |

Ultimately, the goal of applying 1/f timing is to synchronize the film's rhythm with the "waves in our attention" that course through us at every timescale.1 By doing so, the automated system moves beyond mechanical cutting and enters a state of "cultural transmission," mimicking the intuitive, successful patterns developed by master film editors over the last century.1 This alignment is the key to creating content that is not just "seen," but truly "engrossing," leading to higher watch times, lower drop-off rates, and superior performance across all social media engagement metrics.2

#### **Works cited**

1. Pattern in movies mimics that found in our brain | Cornell Chronicle, accessed March 23, 2026, [https://news.cornell.edu/stories/2010/03/study-pattern-movies-mimics-found-our-brain](https://news.cornell.edu/stories/2010/03/study-pattern-movies-mimics-found-our-brain)  
2. Focusing on the Cinematic Mind \- Association for Psychological Science, accessed March 23, 2026, [https://www.psychologicalscience.org/news/were-only-human/focusing-on-the-cinematic-mind.html](https://www.psychologicalscience.org/news/were-only-human/focusing-on-the-cinematic-mind.html)  
3. James CUTTING | Susan Linn Sage Professor | PhD | Cornell University, Ithaca | CU | Department of Psychology | Research profile \- ResearchGate, accessed March 23, 2026, [https://www.researchgate.net/profile/James-Cutting](https://www.researchgate.net/profile/James-Cutting)  
4. Temporal fractals in movies and mind \- PMC \- NIH, accessed March 23, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC5849648/](https://pmc.ncbi.nlm.nih.gov/articles/PMC5849648/)  
5. Quicker, faster, darker: Changes in Hollywood film over 75 years ..., accessed March 23, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC3485803/](https://pmc.ncbi.nlm.nih.gov/articles/PMC3485803/)  
6. VideoGen-of-Thought: Step-by-step generating multi-shot video with minimal manual intervention, accessed March 23, 2026, [https://what-makes-good-video.github.io/assets/10\_VideoGen\_of\_Thought\_Step\_by.pdf](https://what-makes-good-video.github.io/assets/10_VideoGen_of_Thought_Step_by.pdf)  
7. Video Echoed in Music: Semantic, Temporal, and Rhythmic Alignment for Video-to-Music Generation \- arXiv, accessed March 23, 2026, [https://arxiv.org/html/2511.09585](https://arxiv.org/html/2511.09585)  
8. New Scientist and the 1/f structure in film editing \- Continuity Boy, accessed March 23, 2026, [http://continuityboy.blogspot.com/2010/02/new-scientist-and-1f-structure-in-film.html](http://continuityboy.blogspot.com/2010/02/new-scientist-and-1f-structure-in-film.html)  
9. Shot Structure and Visual Activity: The Evolution of Hollywood Film \- ResearchGate, accessed March 23, 2026, [https://www.researchgate.net/publication/245641122\_Shot\_Structure\_and\_Visual\_Activity\_The\_Evolution\_of\_Hollywood\_Film](https://www.researchgate.net/publication/245641122_Shot_Structure_and_Visual_Activity_The_Evolution_of_Hollywood_Film)  
10. A plot of shot lengths in seconds by how common shots of those lengths... | Download Scientific Diagram \- ResearchGate, accessed March 23, 2026, [https://www.researchgate.net/figure/A-plot-of-shot-lengths-in-seconds-by-how-common-shots-of-those-lengths-are-in-the-film-A\_fig3\_255484237](https://www.researchgate.net/figure/A-plot-of-shot-lengths-in-seconds-by-how-common-shots-of-those-lengths-are-in-the-film-A_fig3_255484237)  
11. Science of Hollywood blockbusters | ScienceDaily, accessed March 23, 2026, [https://www.sciencedaily.com/releases/2010/02/100223121435.htm](https://www.sciencedaily.com/releases/2010/02/100223121435.htm)  
12. (PDF) Attention and the Evolution of Hollywood Film \- ResearchGate, accessed March 23, 2026, [https://www.researchgate.net/publication/43348238\_Attention\_and\_the\_Evolution\_of\_Hollywood\_Film](https://www.researchgate.net/publication/43348238_Attention_and_the_Evolution_of_Hollywood_Film)  
13. Pink noise \- Wikipedia, accessed March 23, 2026, [https://en.wikipedia.org/wiki/Pink\_noise](https://en.wikipedia.org/wiki/Pink_noise)  
14. Algorithm for high quality 1/f noise? \- Computational Science Stack Exchange, accessed March 23, 2026, [https://scicomp.stackexchange.com/questions/18987/algorithm-for-high-quality-1-f-noise](https://scicomp.stackexchange.com/questions/18987/algorithm-for-high-quality-1-f-noise)  
15. PinkNoise.java \- a class for generating 1/f^alpha pink noise \- of Sampo Niskanen, accessed March 23, 2026, [https://sampo.kapsi.fi/PinkNoise/](https://sampo.kapsi.fi/PinkNoise/)  
16. Film through the Human Visual System: Finding Patterns and Limits \- ResearchGate, accessed March 23, 2026, [https://www.researchgate.net/publication/255484237\_Film\_through\_the\_Human\_Visual\_System\_Finding\_Patterns\_and\_Limits](https://www.researchgate.net/publication/255484237_Film_through_the_Human_Visual_System_Finding_Patterns_and_Limits)  
17. The Science of Hollywood Blockbusters, accessed March 23, 2026, [https://www.psychologicalscience.org/observer/the-science-of-hollywood-blockbusters-2](https://www.psychologicalscience.org/observer/the-science-of-hollywood-blockbusters-2)  
18. The Role of Event Number and Duration in Time-Compressed Memory Replay \- PMC, accessed March 23, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12768557/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12768557/)  
19. The importance of rhythm in video editing \- Highlights \- Solveig Multimedia, accessed March 23, 2026, [https://www.solveigmm.com/blog/en/the-importance-of-rhythm-in-video-editing/](https://www.solveigmm.com/blog/en/the-importance-of-rhythm-in-video-editing/)  
20. What's Your Go to Method for finding the rhythm when cutting video to music? \- Reddit, accessed March 23, 2026, [https://www.reddit.com/r/premiere/comments/1nomnj0/whats\_your\_go\_to\_method\_for\_finding\_the\_rhythm/](https://www.reddit.com/r/premiere/comments/1nomnj0/whats_your_go_to_method_for_finding_the_rhythm/)  
21. Mastering Pacing and Rhythm: Essential Editing Techniques for Engaging Videos (Full Transcript) \- GoTranscript, accessed March 23, 2026, [https://gotranscript.com/public/mastering-pacing-and-rhythm-essential-editing-techniques-for-engaging-videos](https://gotranscript.com/public/mastering-pacing-and-rhythm-essential-editing-techniques-for-engaging-videos)  
22. Tiktok Videos Statistics 2025: 93+ Stats & Insights \[Expert Analysis\] \- Marketing LTB, accessed March 23, 2026, [https://marketingltb.com/blog/statistics/tiktok-videos-statistics/](https://marketingltb.com/blog/statistics/tiktok-videos-statistics/)  
23. 2025 TikTok Benchmark Report \- Dash Social, accessed March 23, 2026, [https://www.dashsocial.com/social-media-benchmarks/tiktok](https://www.dashsocial.com/social-media-benchmarks/tiktok)  
24. \[What Data Says\] How Long Does It Take for a TikTok to Get Views?, accessed March 23, 2026, [https://www.socialinsider.io/blog/tiktok-virality-insights/](https://www.socialinsider.io/blog/tiktok-virality-insights/)  
25. Social Media Benchmarks For 2026 \- Socialinsider, accessed March 23, 2026, [https://www.socialinsider.io/social-media-benchmarks](https://www.socialinsider.io/social-media-benchmarks)  
26. Every Video Marketing Metric That Matters in 2026 and How to Report It \- Swydo, accessed March 23, 2026, [https://www.swydo.com/blog/video-marketing-metrics/](https://www.swydo.com/blog/video-marketing-metrics/)  
27. 2025 Social Media Video Performance Statistics \- Socialinsider, accessed March 23, 2026, [https://www.socialinsider.io/social-media-benchmarks/social-media-video-statistics](https://www.socialinsider.io/social-media-benchmarks/social-media-video-statistics)  
28. Benchmarks for Measuring Your Content's Social Media Performance in 2025, accessed March 23, 2026, [https://www.blinkjarmedia.com/blog/benchmarks-for-measuring-your-contents-social-media-performance-in-2025](https://www.blinkjarmedia.com/blog/benchmarks-for-measuring-your-contents-social-media-performance-in-2025)  
29. 2026 TikTok Marketing Benchmarks (Real Data \+ Strategies) \- WebFX, accessed March 23, 2026, [https://www.webfx.com/blog/social-media/tiktok-benchmarks/](https://www.webfx.com/blog/social-media/tiktok-benchmarks/)  
30. Attentional Synchrony and the Effects of Repetitive ... \- CEUR-WS.org, accessed March 23, 2026, [https://ceur-ws.org/Vol-1751/AICS\_2016\_paper\_57.pdf](https://ceur-ws.org/Vol-1751/AICS_2016_paper_57.pdf)  
31. 1 Gaze Data for the Analysis of A ention in Feature Films \- Stanford Computer Graphics Laboratory, accessed March 23, 2026, [https://graphics.stanford.edu/\~kbreeden/pub/dataset.pdf](https://graphics.stanford.edu/~kbreeden/pub/dataset.pdf)  
32. Eﬀect of Subtitles on Gaze Behavior during Shot Changes: An Eye-tracking Study \- PMC, accessed March 23, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC10723748/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10723748/)  
33. Effect of sequential video shot comprehensibility on attentional synchrony: A comparison of children and adults | PNAS, accessed March 23, 2026, [https://www.pnas.org/doi/10.1073/pnas.1611606114](https://www.pnas.org/doi/10.1073/pnas.1611606114)  
34. The neural impact of editing on viewer narrative cognition in virtual reality films \- PMC \- NIH, accessed March 23, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12425892/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12425892/)  
35. Here's looking at you, kid: Filmmakers know how we read emotions ..., accessed March 23, 2026, [https://news.cornell.edu/stories/2016/01/heres-looking-you-kid-filmmakers-know-how-we-read-emotions](https://news.cornell.edu/stories/2016/01/heres-looking-you-kid-filmmakers-know-how-we-read-emotions)  
36. Facial expression, size, and clutter: Inferences from movie structure to emotion judgments and back \- PMC, accessed March 23, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC4819543/](https://pmc.ncbi.nlm.nih.gov/articles/PMC4819543/)  
37. Guide to Camera Shots: Every Shot Size Explained (2026) \- StudioBinder, accessed March 23, 2026, [https://www.studiobinder.com/blog/types-of-camera-shots-sizes-in-film/](https://www.studiobinder.com/blog/types-of-camera-shots-sizes-in-film/)  
38. Exploring Shot Sizes: From Extreme Close-Ups to Extreme Long Shots \- Journalism University, accessed March 23, 2026, [https://journalism.university/electronic-media/exploring-shot-sizes-close-ups-long-shots/](https://journalism.university/electronic-media/exploring-shot-sizes-close-ups-long-shots/)  
39. The Three Second Social Media Rule \- Marketing Essentials Lab, accessed March 23, 2026, [https://marketingessentialslab.com/%E2%80%A8the-three-second-social-media-rule/](https://marketingessentialslab.com/%E2%80%A8the-three-second-social-media-rule/)  
40. Why Your First 3 Seconds Are All That Matter on Social Media \- Multipost Digital, accessed March 23, 2026, [https://www.multipostdigital.com/blog/10jnpbhqk90zkfoaav27jqyzaum8cg](https://www.multipostdigital.com/blog/10jnpbhqk90zkfoaav27jqyzaum8cg)  
41. Video Marketing Data Blog \#1: It's About The First 3 Seconds\! \- PURESIVE FILMS, accessed March 23, 2026, [https://www.puresivefilms.ch/blog/videomarketing-datablog-1-the-first-3-seconds](https://www.puresivefilms.ch/blog/videomarketing-datablog-1-the-first-3-seconds)  
42. The 3-Second Rule of Marketing: Win or Lose Attention Before They Blink, accessed March 23, 2026, [https://www.stardigitalmarketing.org/the-3-second-rule-of-marketing-win-or-lose-attention-before-they-blink/](https://www.stardigitalmarketing.org/the-3-second-rule-of-marketing-win-or-lose-attention-before-they-blink/)  
43. What viewers actually care about in the first 3 seconds \- based on our retention data : r/DigitalMarketing \- Reddit, accessed March 23, 2026, [https://www.reddit.com/r/DigitalMarketing/comments/1ps2x60/what\_viewers\_actually\_care\_about\_in\_the\_first\_3/](https://www.reddit.com/r/DigitalMarketing/comments/1ps2x60/what_viewers_actually_care_about_in_the_first_3/)  
44. TikTok 3 Second Rule: Mastering Rapid Engagement \- Teleprompter.com, accessed March 23, 2026, [https://www.teleprompter.com/blog/tiktok-3-second-rule](https://www.teleprompter.com/blog/tiktok-3-second-rule)  
45. Why The First 3 Seconds of Video Matter More Than the Next 30 \- Animoto, accessed March 23, 2026, [https://animoto.com/blog/video-marketing/why-first-3-seconds-matter](https://animoto.com/blog/video-marketing/why-first-3-seconds-matter)  
46. 12 TikTok metrics you should track to measure content performance & improve engagement, accessed March 23, 2026, [https://planable.io/blog/tiktok-metrics/](https://planable.io/blog/tiktok-metrics/)  
47. The Effect of Music and Editing Style on Subjective Perception of ..., accessed March 23, 2026, [https://labocinemedias.ca/wp-content/uploads/2024/10/The\_Effect\_of\_Music\_and\_Editin.pdf](https://labocinemedias.ca/wp-content/uploads/2024/10/The_Effect_of_Music_and_Editin.pdf)  
48. Audio‐visual concert performances synchronize audience's heart rates \- PMC, accessed March 23, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC11776452/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11776452/)  
49. Influence of musical context on sensorimotor synchronization in classical ballet solo dance | PLOS One \- Research journals, accessed March 23, 2026, [https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0284387](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0284387)  
50. Top 7 Metrics for Social Video Engagement \- Zight, accessed March 23, 2026, [https://zight.com/blog/top-7-metrics-for-social-video-engagement/](https://zight.com/blog/top-7-metrics-for-social-video-engagement/)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACoAAAAYCAYAAACMcW/9AAACPUlEQVR4Xu2VO2gVURCGR0ihJr4IKqIgkYgEQkACgiBqIRgRLbRUqxQ2kiYQIYUgISA2gRSCSggpbHyUFkqKEC1EwUJsAxdRREMsLmoRifr/O3Oys2fPcjFVhP3hg3vPnD0zO4+zIrVqZRo07lUwDPYYXvtE7QuOO+AwuAXa8q0tfdwE3UalWh2ybgLdbpwGP8GE5IEdFD3om3HEntkPXoJT9j/oLGiC69F67OO25D541g1bJ0zMBn0srUvgt5SdM3MfjcdgE3gIrvlNpi3gGTgWG0xVPqjLBoM9GtkKmhQNhoF59YMfBgPtBUvgnN9k6gDTYG9sMNFHQ9L2A8ZnMBrZMjEL5AV4CjYWzVnmVozzkgc+L9pTvkz8zbPi0rXyQflAZyJbph6DWfJvQmcs4aJo34TeYdaegz/Gd3DfiKsR5H3E/RtEX+SXaOZLumDQ6TswZ7wWLeOhsNFpq+ikNiQPmLwHu/Jtqwo+qvqTumrwHPZySYyeMOVM/b9qG5gymI3UIAUfDUn3J1uBLUE4J11Fs+q/CHQHeGPMgvaiuaQBSZcu9NcX0WHz8j6qBonPNI0RKQ/jaoOT8ciWEi/qE/GiaE+RV6IZ9vI+UoPE/UzSIyN+PhMPD4NwJrJ5+etlTIpvvFP0K0UuuvWgcMnHg8Qz+sBb0aFlNUsVZQk/gGXJA/0KHoDNbl9QuF6egLuiGeC3e0j0prhi+Beo8sE18kn0K3ZcEqVeq5g10mn/d4t+mU5Kuudq1apVaw36C8oCpynKnVPyAAAAAElFTkSuQmCC>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAYCAYAAADOMhxqAAAAyUlEQVR4XmNgGFKAH4hnAfFBKM5DlcYEJGvIAeK1QLwfircCMQeKCiTADcR7gLgYiK2gWB5FBRqQAeK7QOyCLoEMWKDYAYjLgfg9lHaGYla4SijghGJPIO4D4odAnMCARwMyaGUg4ElkAHLWGiCehC6BC5CsQRCITwNxNLoELqDJAPGwDboELgAKe1AcgOKCKFDEAIllUGwTBeYwEPCwGBCfA+IJULwdiC1RVKABkCefAHE/FM9mIBCrJGtgBGJ9IHaFYlB6GkAAALsiJCoUBrvdAAAAAElFTkSuQmCC>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAAAuCAYAAACVmkVrAAADBUlEQVR4Xu3dT4hVVRwH8CNlFP2BIFLRkLBNbVrNohAUJNCF/UNUchNEuK8ocdUiQRFahOCiFroQF7rVRbkIhYhooaIohDAbA91Euzaiv1/33bn3Hd5MML2ZuYyfD3zh3d95761/nHPPOaUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIM3Ezkd+aQeAABgGJ6O7IpsrQcAABiOg5GNdREAgGF4KXJz9PnZyM7Imm4YAICVlu+w3Y+8Fjka+TWyYewbAACsqDORfyIvjJ6f7I0BADAAuRz6beTvyO5qDACAAZgtzYaDnyNHSrMsapYNACC8P8pC3qsLS+BsaRq0zyM/Rd4cHwYAWL2+LM2BtCl3X94p3dEZr4xSy92Z30euleY36cfIprlvAAAwNb9F1vWez5duqfHrXr0vG7p9ke292onIV71nAACm5EFpDqRt5Y0CKW8UuN6rt3L581jk08iOXj1n1672ngEAmJJs2B5GbkT29uoHSvOCf21P5HLkozLesD0fudJ7bj0Rebk0Z6ZNytruqwAALGRb5K/SLYfm8mb7bltfLp/me26158rkBm+xbi8im//9JQDAKpEN1qHeczZq+f5aa76GLXdn/lkXy/Qbtvy/xQQAYNX4sIw3Xh+X5riMVh5OO2mJ83CZXM+Zt1t1EQCAxTse+aY0Gwj2Ry5G1vfGXy+TNxHkLNwPdbE0M2+/10UAAJZWzsK1mwJyxi1n5HLn6Ktz3+hkI/dWXZyiXyKnSndgbu5mdfk7APDYy2btndHnzyJ/lOamgUlyxi4P1F0K+b95+fsbo8/pZGRL5N3i1gMA4DGXTVt7m8F8/mv8/9hemjPfcum2vSIr36NrzUY+6D0DALDMdpWmWfuidA1bXv7eulCaM+AAAFhBucmhvYGh9WJplkdzBvCpagwAgGWUy62X6iIAAMMxE7lbFwEAGI6803TSVVgAAAzEd2X8yiwAAAYiz1a7FzlX3BEKADBIuQP07cgz9QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA0PMIZV1bk1ZfpasAAAAASUVORK5CYII=>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAsAAAAZCAYAAADnstS2AAAA2ElEQVR4Xu3SvQ7BUBwF8CtYfAwSidjEYrQwSMRkMRhswmjwAAZh8QQS8QI2E+8gMdlsBiQGi6fgnPY0zW0tbBIn+SXt/Z82vW2N+d3kYSFHaNpjO3FoyA2q1vRNeDc6QS4wC2UqG4gFZlY4ZIl4AcN9DCSrNScflfmMZ2lBBSawkpFfdXd/lZ6U4CFdv2pMH56yhqTW+XihzS5hKzO4Q9lqKGnYw1BSsIMxFKTuVo0pwkUL5JXb0JHaV2UeHIz7LikCc+O+Mu+r8t9xEoWEd6Lwgoxm9E8oLwGZKi4LR9U5AAAAAElFTkSuQmCC>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAaCAYAAACD+r1hAAAAu0lEQVR4Xu3RMQtBYRTG8WtQkkIGKWVRMlksdjJZZDcYlEkGVovBalXKRzDYrTIx2I1WH0D+p5739jIoRnnqV7dz7nnf27lB8M/PpIgBesi89MJEMZc1Cqhjr2djww17OYIxdpK0Iolhi6k00bFGCVf0xY/dtpEZslb8eKCNGyriZ4G7hIeNcEFO/ExwkLQr1nBGXlzKOAXPy4hbw63UfWsXKwxRxVGWaH014JIQ24Qd4mL/w6S82j9v8wAyaip2bbagMwAAAABJRU5ErkJggg==>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAXCAYAAABNq8wJAAABmUlEQVR4Xu3VPShFYRwG8L9QhBQiMlxRIjKYlLJQhCwGRRlJShYWRoOURDclJYMYLAYyGBSDQclsIimDRRnF85z3f+o9517dszjOyXnq1733/bid9/OIJEnyL1IJPaoO8rzV0U0hLMEJjKldSGtd5NMHd1BjlRXDGUxbZZFNrAfAfb4Hx1Dgq9uECyjxlTuHZUItQ4f83YEpgyvY91cgi/AItW4BH3JGTIdO1ShmlAtaz+VsdjtkCQ8Vl5p/GkQ15Ds9s4dt+JA/DeBdzAQ74X56gJRboBmHZ2iFDajyVntSASMwGtCgZNkCVnIN4EPMREuDmIdcsVtouuEV5sSsRJgJPIAB+IReu4WGDdjwHup9db+dwGdgCt6gxW6hcQfArZQrTXALTwFdS+aWtcNzx1voFIp8dXyZXUIpf3TBi+hyWOF9uwZfMCxmv4b99usXs/r+98A5zLoFHOk83MAkrKsDaIcdOIItKNc+YYUTtg2H0KZW9XfGs3CZuKf4aS8ZrzrePmHPvhtOcAqGFL+zLCOxH0CSJElimG8ZM0+7XrycdQAAAABJRU5ErkJggg==>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAXCAYAAABNq8wJAAABkklEQVR4Xu3VvytGURgH8EdShORHfpSBKBFRSikmDJIMbJSRLLLYjAZEZLOwkD/CQAyKlMFkk5RBShkM4vu95zn1vO99y32X932v7rc+761z7um959znnCuSJMm/TxG0wIiq17ZYpApOYMN4h1PtK/hsw6KkrvgwfMFuWntBJtYTqIBz+IBe014NN/AAdaY9SC3MqTVxA/M5y1lxdW/rvRIuJW0CfMgl7ehXbXAGq9o/Bh1+QIaUQAM0RcTTpDgYmV26xW3klBJinT2KO65suALP0CVuQOiVmdTAFMxENAHlwcho4QLRobgSavYdreIect03mAzBKyyLexP5Clea/08X0Gg7x+EbRm2jhqX0CfdiZpyHTMOx8vuBeyEowQV4g07tsPETYCn9lXa4haeIriRcspkyAHviys2XHB9+U68yCC/iHtamDLbgBybFDWYN5jJ9cAdHcGDwTfAabGL+rMA1zMOO4k09eiM/3fuS2883F4ynIBcwk9CeLRV3vPFKPqwznj65Xv2sE/sJJEmSJIb5BXQYUEytTazhAAAAAElFTkSuQmCC>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAD8AAAAYCAYAAABN9iVRAAACUElEQVR4Xu2WT0hVQRSHj2RgJJgYaChotAjTdGEFgcsSXLQJN2JQGGG4UIxQEVxKSBFRgeCuRSC4jiCCghYJrlpIgQQRkVTkIqhFIPr7vTnz3tw/7zkP5L0nzgcf9zkz917PzDkzVyQQCFQ4jfBovLEAh+Ap2KvWRrv3Fwcq+GPqBfgYbsCeyIj8NMEX8B4cUt/Bq+6gSuamOgrvwr/iF3wVfASf6m9LJ1yDHU7bnsLUYnrSw7E+lxrVlyviH3wz/CJmtV2Oiwn+Tqw9Q4N6Dc7CbonOXCEY6Dz8Cb+pP+CgmNpzqYbjqm8NFxP8efhPzD0uXJi38JnbyACZWqwJyhdwo3gNJ7X/Mjxtb0hhAN6SaKAM7AF8D7vEPIf9TOUZ1ZdigufYbb262OAZV3bSb8N12KZamDZcwTNiaohpk49+WB9vVHj/K/hHzIpw8+LLfVed7GXwNLPznxQT4Fx2SA4eD0xdpiczwAfuzuWu+RC8Xl0SwTNdt+Cl7JAcfBFf+AG2xPriMNAF+At+VTlxNyR9w2OpUd8JKCZ47w1vBP6G7bbBwQYfPzLS4IY3LNHTgTU9Dd9IcsPj5kh9KSZ4e9QxNhdm42c4ZRsuwu+SfOgReF9y6cNACqXxbhveSzHPonwun099yRc8M5J+hMtiMomTzA+ctI+cT3rNwM4JuAKvqw/hc3gWLsIl+ATW6T2lwpYGS+i/mInb1L9tmbrBs+xYUqQVrsIxMRNGeeLwSE98u3DGTqhuHTJNecQVWvVKhf/zOdinlnrxAoFAIFB2dgByGHn5D5sYHgAAAABJRU5ErkJggg==>