# **Architectural Heuristics in Short-Form Video: A Theoretical and Empirical Analysis of the Peak-End Rule and Asymmetrical Production Strategies**

The subjective evaluation of a temporal experience is rarely an objective summation of its constituent parts. Instead, human memory operates through a series of filtered snapshots, prioritizing specific moments of high intensity and the concluding sensations of an episode over its total duration or its median state.1 This psychological phenomenon, formally conceptualized as the Peak-End Rule by Daniel Kahneman and Barbara Fredrickson, posits that the "remembering self" constructs narratives based on the average of the most affectively intense point (the peak) and the final moment (the end) of an event.1 As the digital landscape migrates toward short-form video (SFV) formats—typically under 180 seconds—on platforms such as TikTok, Instagram Reels, and YouTube Shorts, the relevance of these cognitive heuristics becomes acute.4 For content producers, understanding the interplay between the Peak-End Rule and the unique attentional constraints of mobile-first consumption is essential for optimizing engagement metrics and brand recall.6

## **Theoretical Foundations and the Snapshot Model of Memory**

The Peak-End Rule emerged from early investigations into "experienced utility" versus "remembered utility," identifying a fundamental disconnect in how individuals perceive time and discomfort.2 The foundational experiments conducted by Kahneman, Fredrickson, Schreiber, and Redelmeier in 1993 utilized aversively cold water to demonstrate that participants would choose a longer period of discomfort if it concluded with a relative improvement in sensation.1 This violation of temporal monotonicity—the logical assumption that more pain is worse—confirmed that the brain ignores the total duration of an experience in favor of its "snapshots".1

| Foundational Experiment | Trial Condition A | Trial Condition B | Behavioral Outcome | Psychological Mechanism |
| :---- | :---- | :---- | :---- | :---- |
| Cold Water Hand Immersion (1993) | 60s at 14°C | 60s at 14°C \+ 30s at 15°C | 80% preferred Trial B | Duration Neglect and End-State Bias.1 |
| Clinical Colonoscopy Ratings (1996) | Standard procedure (Variable length) | Extended procedure with scope stationary | Longer procedure rated as less painful | Peak-End Average dominating duration.1 |
| Horror Movie Anxiety (2019) | Finished at frightening peak | Finished with lower-intensity end | End-group reported lower anxiety | Resolution affecting retrospective emotion.11 |
| Student Performance Feedback | Short negative summary | Long summary ending on mild improvement | Long version perceived as easier | Narrative trajectory bias.2 |

The "snapshot model" dictates that the brain does not store a continuous, video-like record of events but rather a collection of prototypical moments.1 These moments are selected via the representativeness heuristic, where the peak and the end serve as the most "representative" indicators of the entire experience.1 In the context of visual media, this implies that a video’s 60-second duration is mentally compressed into two or three salient frames, which the viewer then uses to decide whether to interact with the "Like," "Share," or "Save" functions.2

## **The Short-Form Video Cognitive Paradigm: Memory, Attention, and the Neuralyzer Effect**

The application of the Peak-End Rule to short-form video must account for the rapid-fire, algorithmic environment in which these "snapshots" are formed. Research indicates that the consumption of TikTok, Reels, and Shorts creates a unique cognitive state characterized by "reduced inhibitory control" and "attentional disruption".4 This environment places extreme pressure on the Peak-End Rule, as the "end" of one experience is immediately superseded by the "hook" of the next.

Recent experimental data from Ludwig Maximilian University suggests that TikTok acts as a form of "memory-wiping Neuralyzer," significantly impairing prospective memory.14 When users engage in frictionless, high-speed task switching, the brain’s ability to hold onto intentions—such as a specific call to action (CTA) found in a video—is obliterated.14 This suggests a second-order insight for video architecture: the "End" of a video is not merely a psychological anchor for satisfaction but a functional bridge to behavioral decision-making that must occur before the next algorithmic wipe.7

| Cognitive Network | Impact of Intense SFV Use | Behavioral Manifestation | Significance for Video Design |
| :---- | :---- | :---- | :---- |
| Alerting Network | Efficiency reduction | Decreased readiness for incoming info | Hooks must be more visceral.4 |
| P300 Event-Related Potential | Amplitude reduction | Sign of weakened attention | Peak must be highly salient.13 |
| Prefrontal-Cingulate Connectivity | Altered patterns | Trade-off between social/attentional states | Narrative must be simplified.4 |
| Precuneus Activity | Decreased sensitivity to loss | Reduced self-reflection/risk assessment | Impulsive "Sharing" is more likely.4 |

Duration neglect remains a robust feature of SFV consumption, even as attention spans shrink. Users consistently underestimate the time spent in the "scroll" while overestimating the duration of individual videos when they are unengaging.16 This distortion means that if a video contains a sufficiently powerful peak and a satisfying end, the difference between a 45-second and a 90-second runtime becomes negligible in terms of user sentiment.1 Therefore, optimization efforts should prioritize the intensity of the "Peak" over the reduction of the "Duration" to its absolute minimum.9

## **Taxonomy of the "Peak": Defining Climax in Digital Content**

The "peak" in short-form video is not a monolithic event but a convergence of narrative, visual, and emotional dimensions.17 Affective Video Content Analysis (AVCA) identifies the "climax" as the point where emotional intensity reaches its zenith and the core message is most powerfully conveyed.17 Defining the "peak" for production purposes requires a nuanced understanding of which dimensions drive retrospective utility.

### **Emotional Arousal and the Tunnel Effect**

High-arousal emotions such as anger, fear, excitement, or extreme joy are the primary drivers of memory salience.8 These emotions trigger a "tunnel effect," where the brain focuses cognitive resources on the source of the arousal (the peak) while neglecting peripheral details (the setup).18 In a 4-7 scene narrative, the "Turning Point" serves as the architectural location for this emotional peak.17

### **Visual and Auditory Complexity**

Empirical evidence suggests a nonlinear, inverted U-shaped relationship between technical features and user engagement.19 Pixel-level image complexity and the number of shots (cutting rate) can manufacture a sense of intensity.19 However, if the visual "peak" is too complex, it leads to cognitive overload and "advertisement fatigue," causing the user to swipe away before reaching the conclusion.19

| Peak Feature | Technical Execution | Psychological Goal | Second-Order Insight |
| :---- | :---- | :---- | :---- |
| Narrative Surprise | Sudden "But..." transitions | Breaking pattern recognition | Triggers dopamine-driven curiosity loops.7 |
| Visual Scaling | Zooming/Distancing patterns | Enhancing emotional scope | Pulling away creates a sense of loneliness/sadness.17 |
| Auditory Climax | Data Point Loops/Alarms | Suggesting urgency/severity | Sound design often leads the emotional appraisal.17 |
| Spectral Intensity | High Spectral Centroid | Signaling brightness/clarity | Higher frequencies can improve recall but lower "Likes".19 |

## **The Hook and the Lead Factor: Reimagining the Peak-End-Start Model**

While Kahneman’s original rule focused on the retrospective evaluation of completed events, short-form video requires a model that incorporates the "Start" or "Hook." In a environment of instant rejection, the Hook acts as a cognitive gatekeeper.21 Some researchers argue for a "Peak-End-Start" heuristic, where the first impression establishes the reference frame for the subsequent peak.2

The "Lead Factor" posits that expectations set at the beginning of an experience fundamentally alter the perception of the peak.8 If a video opens with a "Secret Hook" (e.g., "Nobody is talking about this...") or a "Controversial Hook," it creates a curiosity gap that the brain demands be filled.7 If the peak (the Turning Point) meets or exceeds the expectation set by the hook, the video is rated exceptionally high.8 However, if the hook over-promises and the peak is underwhelming, the end is perceived as "outrageous" and the entire experience is devalued.8 This suggests that the Hook and the Peak must be architecturally synchronized; the Hook creates the "demand" for the Peak, and the Peak provides the "supply."

### **Hook Archetypes and Memory Framing**

1. **The POV Hook:** Establishes a relatability frame, making the peak more personally significant.22  
2. **The Result Hook:** Teases a transformation, making the end (the "Vision") the primary focus.21  
3. **The Visual Hook:** Uses fast-paced shots or unusual angles to trigger the "alerting" network before words are spoken.7

## **Metric-Heuristic Mapping: Correlating Behavior with Psychology**

In social media, the subjective evaluation of a video is expressed through discrete behavioral metrics: Likes, Shares, Saves, and Comments.24 These metrics are not interchangeable; they correlate with different moments in the Peak-End narrative arc.

### **The Share: Peak Intensity and Moral Contagion**

Sharing is a high-cost, public act of "electronic word-of-mouth" (eWOM).26 Research consistently shows that sharing is driven by high-arousal emotions at the "Peak".28 The "Moral Contagion" effect demonstrates that the presence of moral-emotional language in a post increases its sharing rate by 19%.30 High-arousal negative emotions like anger and disgust spread rapidly and create "bursty" engagement patterns—short, intense flurries of activity.31 If a video has a powerful turning point, the user is likely to share it before they even reach the end, as the peak triggers the "tunnel effect" focus on the core message.18

### **The Like/Save: End Satisfaction and Perceived Utility**

"Likes" and "Saves" are post-consumption signals of satisfaction and utility.26 While the peak captures attention, the "End" (the Vision/Resolution) secures the endorsement.6 The "recency bias" ensures that the final feeling—the "high note"—dominates the decision to "Like" the post.2 For brands, a strong ending that provides a "free granola" moment (a low-cost, high-value insight or feeling) is essential for converting a viewer into a follower.10

| Social Metric | Cognitive Trigger | Narrative Correlation | Platform Value |
| :---- | :---- | :---- | :---- |
| **Share** | High Arousal (Anger/Awe) | Turning Point (The Peak) | Increases reach and virality.26 |
| **Like** | General Satisfaction | Vision (The End) | Indicator of audience approval.24 |
| **Save** | Perceived Value/Utility | Turning Point/Resolution | High-intent engagement; algorithmic signal.33 |
| **Comment** | Moral Conflict/Empathy | Challenge/Turning Point | Deeper cognitive engagement.24 |

## **Asymmetrical Production Strategy: Resource Reallocation Framework**

If the Peak-End Rule holds that 80% of an experience's value is derived from 20% of its duration, production budgets must reflect this asymmetry.1 A "uniform quality" approach to a 6-scene video is inefficient, as resources are wasted on middle scenes that the brain will eventually "level" or forget.3

### **The 4-7 Scene Resource Distribution**

The narrative arc of the system (HOOK, SETUP, CHALLENGE, TURNING POINT, RESOLUTION, VISION) should be treated as a prioritized hierarchy rather than a linear sequence of equal parts.

1. **The Peak (Turning Point):** This is the moment of maximum emotional and visual intensity.17 It should receive **2x the visual effects (VFX) budget**, the most complex C-Roll compositions, and the highest-quality cinematic B-Roll.6 Branding must be heavily integrated into this peak, as brand recall is 3x higher when associated with an emotional high point.10  
2. **The End (Vision):** The final scene must be polished to provide a clean, upbeat resolution.8 High "Spectral Centroid" audio (bright, crisp sound) and high-contrast visuals should be used to leave a lasting impression.19 This is the "End" snapshot that secures the "Like".26  
3. **The Gatekeeper (Hook):** While not part of the Peak-End calculation of *pleasure*, it is the filter for *retention*.21 The Hook requires "experimental" creativity—testing multiple variations to see which "Lead Factor" creates the highest engagement for the peak.8  
4. **The "Middle" (Setup/Challenge/Resolution):** These scenes are functional. They provide the necessary context to make the peak meaningful, but they do not require premium asset quality.3 Simple execution and standard B-Roll are sufficient, as duration neglect will cause the viewer to overlook their relative brevity or lack of complexity.1

| Scene Category | Architectural Goal | Production Effort | VFX/C-Roll Complexity | Metric Impact |
| :---- | :---- | :---- | :---- | :---- |
| **HOOK** | Retention/Filter | High (Creativity) | High (Visual Hook) | CTR/Watch Time.21 |
| **SETUP** | Contextual baseline | Low (Functional) | Basic | Duration Buffer. |
| **CHALLENGE** | Tension/Stakes | Moderate | Standard | Comment Activity. |
| **TURNING POINT** | **The Peak** | **Maximum** | **Complex/Layered** | **Shares/Recall**.6 |
| **RESOLUTION** | Relief/Clarity | Low (Functional) | Basic | Retention Stability. |
| **VISION** | **The End** | **Maximum** | **Ultra-Premium** | **Likes/Saves**.26 |

### **Second-Order Implications of Asymmetrical Production**

This strategy creates a "Creative Magnifier" effect, where the viewer's memory of the brand is disproportionately tied to the most impressive frames of the video.6 By using "Distancing by Pulling Away" or "Sadness Echo" patterns only at the peak, these techniques become more impactful through contrast with the simpler setup scenes.17 This also mitigates "advertisement fatigue" 19; by not overwhelming the viewer with 60 seconds of high-intensity visuals, the specific peak moment remains a distinct, memorable snapshot.6

## **Duration Neglect and Platform Optimization**

A critical strategic dilemma for SFV producers is the trade-off between video length and engagement quality. Platform algorithms often reward high completion rates, which favors shorter (15-30s) videos. However, the Peak-End Rule suggests that "duration" is not a primary factor in the viewer’s *subjective* evaluation.1

If a 90-second video allows for a more intense Turning Point and a more satisfying Vision than a 60-second video, the Peak-End Rule indicates that the 90-second version will be remembered as superior.1 The "remembering self" is indifferent to the extra 30 seconds.1 Therefore, optimization should not be for "shortest possible length" but for "maximum peak-end intensity".11 A 90-second video with a strong peak and end is a more effective brand asset than a 60-second video with a diluted peak and end.6

Furthermore, the "Neuralyzer" effect of rapid scrolling means that the "End" of a video must be placed in extremely close temporal proximity to the behavioral call to action.14 In long-form media, a slow fade to black may be acceptable; in SFV, the "End" snapshot and the "CTA" must be almost simultaneous to capitalize on the recency bias before the user swiping into the next memory-erasing cycle.7

## **Conclusions and Practical Synthesis**

The integration of the Peak-End Rule into short-form video production is not merely a creative choice but a requirement for operating within the constraints of the human memory system. The analysis leads to several definitive conclusions for video architecture:

1. **Peak-End Primacy:** The retrospective value of a video—and thus its likelihood of being liked, shared, or saved—is determined by the Turning Point (Peak) and the Vision (End). The middle scenes (Setup, Challenge, Resolution) function solely as narrative scaffolding and should be produced with minimal resource intensity.1  
2. **Metric-Driven Architecture:** To maximize "Shares" and virality, producers must engineer a high-arousal Turning Point, potentially utilizing "Moral Contagion" or narrative surprise.28 To maximize "Likes" and brand sentiment, producers must ensure a high-quality Vision scene that concludes the experience on a positive high note.8  
3. **Asymmetrical Resource Allocation:** Production budgets should be reallocated to provide a **2x multiplier on VFX and C-Roll assets** for the Turning Point and Vision scenes.6 This ensures that the "snapshots" retained by the viewer are of the highest possible quality, leveraging the "Creative Magnifier" effect.6  
4. **The Hook-Peak-End Triad:** The Hook acts as the filter for the experience, establishing a "Lead Factor" expectation that the Peak must then fulfill.8 A strong hook is useless if it does not lead to an equally intense Turning Point, as the "Peak-End" judgment will ultimately devalue the content if expectations are unfulfilled.8  
5. **Strategic Duration Neglect:** Producers should prioritize narrative impact and peak intensity over the reduction of duration.1 A longer video with a superior peak-end profile is more valuable for brand memory and behavioral conversion than a shorter, less intense clip.6

By engineering short-form videos as a series of deliberate snapshots rather than a continuous stream of information, content creators can navigate the "Neuralyzer" effect of modern social media and build lasting brand recall through the psychological shortcuts of the remembering self.

#### **Works cited**

1. Peak–end rule \- Wikipedia, accessed on March 23, 2026, [https://en.wikipedia.org/wiki/Peak%E2%80%93end\_rule](https://en.wikipedia.org/wiki/Peak%E2%80%93end_rule)  
2. Peak-End Heuristic \- ModelThinkers, accessed on March 23, 2026, [https://modelthinkers.com/mental-model/peak-end-heuristic](https://modelthinkers.com/mental-model/peak-end-heuristic)  
3. Peak-end rule \- The Decision Lab, accessed on March 23, 2026, [https://thedecisionlab.com/biases/peak-end-rule](https://thedecisionlab.com/biases/peak-end-rule)  
4. Large meta-analysis links TikTok and Instagram Reels to poorer cognitive and mental health, accessed on March 23, 2026, [https://www.psypost.org/large-meta-analysis-links-tiktok-and-instagram-reels-to-poorer-cognitive-and-mental-health/](https://www.psypost.org/large-meta-analysis-links-tiktok-and-instagram-reels-to-poorer-cognitive-and-mental-health/)  
5. The Impact of Short-Form Video Use on Cognitive and Mental Health Outcomes: A Systematic Review | medRxiv, accessed on March 23, 2026, [https://www.medrxiv.org/content/10.1101/2025.08.27.25334540v2.full](https://www.medrxiv.org/content/10.1101/2025.08.27.25334540v2.full)  
6. The Peak-End Rule: Optimizing Advertising Effectiveness \- iMotions, accessed on March 23, 2026, [https://imotions.com/blog/learning/best-practice/the-peak-end-rule/](https://imotions.com/blog/learning/best-practice/the-peak-end-rule/)  
7. The Psychology of Short-Form Video: Why Hooks, Curiosity, and Creativity Drive Conversions \- Storybox, accessed on March 23, 2026, [https://www.storyboxhq.ca/post/the-psychology-of-short-form-video-why-hooks-curiosity-and-creativity-drive-conversions](https://www.storyboxhq.ca/post/the-psychology-of-short-form-video-why-hooks-curiosity-and-creativity-drive-conversions)  
8. The Peak-End Rule: 2 Things We Actually Remember \- Sprouts \- Learning Videos, accessed on March 23, 2026, [https://sproutsschools.com/peak-end-rule/](https://sproutsschools.com/peak-end-rule/)  
9. Duration Neglect in Retrospective Evaluations of Affective Episodes \- ResearchGate, accessed on March 23, 2026, [https://www.researchgate.net/publication/14844443\_Duration\_Neglect\_in\_Retrospective\_Evaluations\_of\_Affective\_Episodes](https://www.researchgate.net/publication/14844443_Duration_Neglect_in_Retrospective_Evaluations_of_Affective_Episodes)  
10. Peak End Rule | LinkedIn Marketing Solutions, accessed on March 23, 2026, [https://business.linkedin.com/advertise/resources/b2b-institute/b2b-research/trends/peak-end-rule](https://business.linkedin.com/advertise/resources/b2b-institute/b2b-research/trends/peak-end-rule)  
11. What Is the Peak End Rule and How to Use It Smartly, accessed on March 23, 2026, [https://positivepsychology.com/what-is-peak-end-theory/](https://positivepsychology.com/what-is-peak-end-theory/)  
12. Duration Neglect: Ignoring Duration in Retrospective Evaluations \- Renascence, accessed on March 23, 2026, [https://www.renascence.io/journal/duration-neglect-ignoring-duration-in-retrospective-evaluations](https://www.renascence.io/journal/duration-neglect-ignoring-duration-in-retrospective-evaluations)  
13. Intense Short-Video-Based Social Media Use reduces the P300 Event-Related Potential Component in a Visual Oddball Experiment: A Sign for Reduced Attention \- MDPI, accessed on March 23, 2026, [https://www.mdpi.com/2075-1729/14/3/290](https://www.mdpi.com/2075-1729/14/3/290)  
14. TikToks, Shorts, and Reels Are Melting Your Attention Span, Study Finds \- VICE, accessed on March 23, 2026, [https://www.vice.com/en/article/tiktoks-shorts-and-reels-are-melting-your-attention-span-study-finds/](https://www.vice.com/en/article/tiktoks-shorts-and-reels-are-melting-your-attention-span-study-finds/)  
15. The Impact of Short-Form Content \- Changing Tides, accessed on March 23, 2026, [https://thechangingtides.org/blog/2025/10/15/the-impact-of-short-form-content](https://thechangingtides.org/blog/2025/10/15/the-impact-of-short-form-content)  
16. Losing Track of Time on TikTok? An Experimental Study of Short Video Users' Time Distortion \- PMC, accessed on March 23, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12292152/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12292152/)  
17. At the Peak: Empirical Patterns for Creating Climaxes in Data Videos, accessed on March 23, 2026, [https://www.computer.org/csdl/journal/tg/2025/10/11023634/27gSRBkzn7G](https://www.computer.org/csdl/journal/tg/2025/10/11023634/27gSRBkzn7G)  
18. How Does Emotion Affect Information Communication \- arXiv, accessed on March 23, 2026, [https://arxiv.org/html/2502.16038v1](https://arxiv.org/html/2502.16038v1)  
19. Exploring user engagement behavior with short-form video ..., accessed on March 23, 2026, [https://www.researchgate.net/publication/386378356\_Exploring\_user\_engagement\_behavior\_with\_short-form\_video\_advertising\_on\_short-form\_video\_platforms\_a\_visual-audio\_perspective](https://www.researchgate.net/publication/386378356_Exploring_user_engagement_behavior_with_short-form_video_advertising_on_short-form_video_platforms_a_visual-audio_perspective)  
20. Exploring user engagement behavior with short-form video advertising on short-form video platforms: a visual-audio perspective | Internet Research | Emerald Publishing, accessed on March 23, 2026, [https://www.emerald.com/intr/article/36/1/154/1255369/Exploring-user-engagement-behavior-with-short-form](https://www.emerald.com/intr/article/36/1/154/1255369/Exploring-user-engagement-behavior-with-short-form)  
21. Viral Video Hooks: Strategies for Short-Form Success | Aiken House Blog, accessed on March 23, 2026, [https://www.aikenhouse.com/post/viral-video-hooks-strategies-for-short-form-success](https://www.aikenhouse.com/post/viral-video-hooks-strategies-for-short-form-success)  
22. How to Write Better Hooks for Short Form Video in 2025 \- Fresh Faced Marketing, accessed on March 23, 2026, [https://www.freshfacedmarketing.co.uk/marketing-blog/how-to-write-better-hooks-for-short-form-video-in-2025](https://www.freshfacedmarketing.co.uk/marketing-blog/how-to-write-better-hooks-for-short-form-video-in-2025)  
23. Short-Form Video Hooks That Will Get Your Videos Noticed \- AJI Media, accessed on March 23, 2026, [https://ajimedia.com/short-form-video-hooks-that-will-get-your-videos-noticed-aji-media/](https://ajimedia.com/short-form-video-hooks-that-will-get-your-videos-noticed-aji-media/)  
24. A Multimodal Analysis of Automotive Video Communication Effectiveness: The Impact of Visual Emotion, Spatiotemporal Cues, and Title Sentiment \- MDPI, accessed on March 23, 2026, [https://www.mdpi.com/2079-9292/14/21/4200](https://www.mdpi.com/2079-9292/14/21/4200)  
25. The Art of Analyzing Social Media Metrics \- Mitch Daniels School of Business, accessed on March 23, 2026, [https://business.purdue.edu/daniels-insights/posts/2026/analyzing-social-media-metrics.php](https://business.purdue.edu/daniels-insights/posts/2026/analyzing-social-media-metrics.php)  
26. (PDF) From Hearts to Carts: Understanding the Impact of Comments, Likes, and Share Functions on Consumer Purchase Intentions in a Social Media Landscape \- ResearchGate, accessed on March 23, 2026, [https://www.researchgate.net/publication/381445383\_From\_Hearts\_to\_Carts\_Understanding\_the\_Impact\_of\_Comments\_Likes\_and\_Share\_Functions\_on\_Consumer\_Purchase\_Intentions\_in\_a\_Social\_Media\_Landscape](https://www.researchgate.net/publication/381445383_From_Hearts_to_Carts_Understanding_the_Impact_of_Comments_Likes_and_Share_Functions_on_Consumer_Purchase_Intentions_in_a_Social_Media_Landscape)  
27. View of View, Like, Comment, Post: Analyzing User Engagement by Topic at 4 Levels across 5 Social Media Platforms for 53 News Organizations \- AAAI Publications, accessed on March 23, 2026, [https://ojs.aaai.org/index.php/ICWSM/article/view/3208/3076](https://ojs.aaai.org/index.php/ICWSM/article/view/3208/3076)  
28. 'Likes' and 'shares' teach people to express more outrage online | Yale News, accessed on March 23, 2026, [https://news.yale.edu/2021/08/13/likes-and-shares-teach-people-express-more-outrage-online](https://news.yale.edu/2021/08/13/likes-and-shares-teach-people-express-more-outrage-online)  
29. Emotional content and sharing on Facebook: A theory cage match ..., accessed on March 23, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC10541009/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10541009/)  
30. Emotion shapes the diffusion of moralized content in social networks \- PNAS, accessed on March 23, 2026, [https://www.pnas.org/doi/10.1073/pnas.1618923114](https://www.pnas.org/doi/10.1073/pnas.1618923114)  
31. Online propagation of emotions: A study of resharing dynamics on ..., accessed on March 23, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12694876/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12694876/)  
32. Emotional contagion on social media: pathways, effects, and insights for marketers, accessed on March 23, 2026, [https://www.tandfonline.com/doi/full/10.1080/0267257X.2025.2570739](https://www.tandfonline.com/doi/full/10.1080/0267257X.2025.2570739)  
33. How to Read Your Social Media Metrics | First Ascent Design \- Digital Marketing Agency, accessed on March 23, 2026, [https://firstascentdesign.com/social-media-metrics-explained/](https://firstascentdesign.com/social-media-metrics-explained/)  
34. I can't stress this enough \- The Hook of your Videos is so important\! : r/NewTubers \- Reddit, accessed on March 23, 2026, [https://www.reddit.com/r/NewTubers/comments/1o16ywu/i\_cant\_stress\_this\_enough\_the\_hook\_of\_your\_videos/](https://www.reddit.com/r/NewTubers/comments/1o16ywu/i_cant_stress_this_enough_the_hook_of_your_videos/)