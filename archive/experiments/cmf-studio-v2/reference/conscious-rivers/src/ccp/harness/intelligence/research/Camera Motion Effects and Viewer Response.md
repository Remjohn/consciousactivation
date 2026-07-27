# **Kinetic Cinematography and Neural Engagement: A Framework for Quantified Arousal and Presence Scoring in Mobile-First Video Environments**

The evolution of digital video consumption has shifted primarily toward mobile-first platforms, characterized by vertical aspect ratios, high-density small-format displays, and environments rife with external sensory distractions. In this landscape, the traditional cinematic grammar of camera movement must be re-evaluated through the lens of media psychology and neurobiology. The efficacy of automated video editing systems depends on their ability to predict and manipulate viewer physiological states. By establishing a quantified scoring model for motion effects based on the dual axes of Arousal and Presence—distinct from the established metric of Cognitive Load—systemic content optimization can reach levels of precision previously reserved for high-budget manual cinematography.

## **The Physiological Foundations of Motion Perception**

The human brain does not process camera movement as a mere sequence of shifting pixels; rather, it engages in a complex process of embodied simulation. This mechanism, rooted in the activation of the mirror neuron system (MNS), allows viewers to internally "feel" the movement displayed on screen, effectively mapping the camera’s path onto their own motor repertoire.1 The physiological consequence of this simulation is a measurable change in the autonomic nervous system, primarily observed through heart rate (HR), galvanic skin response (GSR), and electroencephalography (EEG).

## **Autonomic Activation and Arousal Metrics**

Physiological arousal refers to the degree of sympathetic nervous system activation, often termed the "fight or flight" response. Empirical research utilizing GSR (also known as electrodermal activity or EDA) indicates that high-frequency, unpredictable camera movements, such as the "Anxiety Camera Shake" (M-03) or "Speed Ramp Chaos" (M-02), trigger significant spikes in skin conductance.3 These spikes correlate with an increase in perceived stress and emotional intensity. For example, handheld camera movements mirror the physiological unsteadiness of a human observer under duress, thereby inducing a sympathetic mirror response in the viewer.3

In contrast, heart rate variability (HRV) and heart rate deceleration are often used to measure sustained attention and cognitive engagement. A slow, purposeful "Push-In" or "Dolly Forward" (M-09) typically results in heart rate deceleration, a marker of orienting responses as the viewer is drawn into a state of heightened focus and intimacy with the subject.5 These physiological markers allow for the categorization of motion effects along a spectrum of arousal.

| Effect Category | Primary Movement | Metric | Arousal Level | Neural Mechanism |
| :---- | :---- | :---- | :---- | :---- |
| High Arousal | Camera Shake / Rapid Pan | GSR Spike / HRV Drop | 8–10 | Amygdala/Sympathetic Activation 3 |
| Moderate Arousal | Rapid Push-In / Speed Ramp | GSR Elevation | 5–7 | Orienting Response 7 |
| Low Arousal | Slow Zoom / Subtle Drift | HR Deceleration | 2–4 | Parasympathetic Engagement 8 |
| Minimal Arousal | Static / Fixed Shot | Baseline | 1 | Cognitive Maintenance 9 |

## **EEG and Cognitive Load Interactions**

The relationship between motion and cognitive load is governed by the brain's ability to resolve visual information without exhausting its working memory. High-arousal effects like the "Speed Ramp Chaos" (M-02) impose significant extraneous cognitive load, as the brain must rapidly re-orient itself to changing temporal and spatial parameters.10 EEG studies show that when motion becomes too erratic, there is a shift from beta-wave dominance (focused attention) to theta-wave spikes, indicating a breakdown in the viewer's "narrative transportation" as they struggle to process the stimulus.8

For an automated editing system, the CLS (Cognitive Load Score) must be balanced against Arousal. An effect can be high-arousal (M-03: Anxiety Shake) without being high-presence, primarily because the disorientation it causes forces the viewer's brain to focus on the medium itself rather than the story world.3

## **Vection and Presence on Miniaturized Displays**

Presence, or the sensation of "being there" within a mediated environment, is a distinct psychological axis from arousal. It is heavily influenced by "vection"—the illusion of self-motion induced by visual stimuli in the absence of physical movement.12 While vection was historically thought to require large, peripheral field-of-view (FOV) displays, recent research has redefined its requirements for mobile devices.

## **The 10-Square-Degree Threshold**

Groundbreaking studies have demonstrated that vection can be induced by visual stimuli covering as little as 10 square degrees.13 This area is significantly smaller than a standard 6-inch smartphone screen viewed at a typical distance of 40 cm. In these experiments, 88% of participants reported linear vection (a sense of moving forward or upward) when viewing small patches of moving dots.13 This confirms that the "Z-Space Parallax Sandwich" (M-16) and "Dynamic Handheld Drift" (M-14) are capable of inducing a sense of presence even on vertical mobile screens.

The intensity of vection—and thus the Presence score—is a function of the speed of the moving stimuli. Increasing dot speed from 5°/sec to 25°/sec significantly enhances the reported sensation of self-motion.13 Furthermore, when the frontal vision is occluded (as is the case when a viewer is focused intently on a smartphone screen in a dark or distracted environment), the sensation of vection increases as the brain is forced to rely solely on the on-screen motion as a frame of reference.13

## **Visually Induced Motion Sickness (VIMS) and the Safe Zone**

Vection is a "double-edged sword" for engagement. While it enhances presence, it is also the primary driver of cybersickness, which manifests as nausea, dizziness, and eye strain when a sensory mismatch occurs between the visual and vestibular systems.14 This mismatch is particularly acute during rapid scrolling or erratic camera movements where the eyes report motion that the inner ear does not feel.16

However, vection and motion sickness are not linearly coupled. It is possible to experience high presence (compelling vection) without any adverse symptoms.12 To maximize Presence while minimizing VIMS, motion must be linear and predictable. Acceleration is a higher risk factor for nausea than velocity; instant changes in speed or direction are more likely to disrupt the user's "VR legs" or comfort than a sustained, high-speed movement.10

| Motion Parameter | Impact on Presence | Impact on VIMS (Nausea) | Recommended Scoring |
| :---- | :---- | :---- | :---- |
| High Linear Velocity | High Increase | Low/Moderate | High Presence 13 |
| High Acceleration | Moderate Increase | High Increase | Low Presence / High CLS 10 |
| Consistent Speed | Sustained Presence | Minimal Risk | Optimal for M-01, M-12 17 |
| Rotational Motion | High Disorientation | Extreme Risk | Avoid for mobile 17 |

## **Temporal Thresholds and Movement Speed Guidelines**

To prevent a transition from "immersive" to "nauseating," an automated system must adhere to specific temporal thresholds. These are defined by the rate at which subjects or the camera move across the frame.

## **The Seven-Second Rule and Judder**

A foundational rule in cinematography for 24fps or 30fps content is the "seven-second rule": a camera pan should take at least seven seconds for a given subject to cross from one edge of the frame to the other.18 Panning faster than this results in "judder" or "staccato" artifacts, which are visually jarring and break immersion.19 On mobile screens, where high-contrast edges are often sharper, this judder is even more detrimental.

For higher frame rates (60fps or 120fps), these thresholds can be pushed. Research indicates that 120fps is a critical threshold for reducing simulator sickness, as it provides the motion clarity required for the brain to accept the visual motion as a window into reality rather than a flickering image.22 Consequently, effects like "M-02: Speed Ramp Chaos" must be scored with a high CLS if the source material is low frame rate, as the temporal aliasing will trigger a physiological stress response.22

## **Quantitative Speed Thresholds for Mobile Video**

| Movement | Immersive (Safe) | Disorienting | Nauseating (Failure) |
| :---- | :---- | :---- | :---- |
| Pan (Full Width) | \> 7.0 s | 3.0 – 5.0 s | \< 2.0 s 20 |
| Tilt (Full Height) | \> 5.0 s | 2.0 – 4.0 s | \< 1.0 s 24 |
| Zoom (2x Scale) | \> 3.0 s | 1.0 – 2.0 s | \< 0.5 s 25 |
| Drift (Periodic) | 0.5 – 1.0 Hz | \> 2.0 Hz | Arhythmic 8 |

## **The Semantic Lexicon of Directional Motion**

Directional semantics in cinematography are not merely stylistic choices; they are grounded in evolutionary psychology and the brain's processing of spatial orientation.

## **Vertical Dynamics: The Power Axis**

Research confirms that the vertical axis serves as a subconscious proxy for social and physical power. Low-angle shots (looking up) activate the amygdala and are associated with perceptions of strength, heroism, and threat.26 High-angle shots (looking down) evoke empathy but also signal vulnerability, weakness, and submission.26

Moving the camera *along* this axis—Tilting or Pedestaling—triggers directional emotions. Upward motion (M-06: Heroic Tilt Up) is universally associated with aspiration, growth, and hope.5 Downward motion (M-07: Vulnerable Tilt Down) signals descent, sadness, or a "falling into" the narrative.5 For an automated editor, an upward drift should be prioritized for "success" or "climax" beats, while a downward drift should accompany "loss" or "revelation" beats.

## **Horizontal Dynamics: The Progress vs. Resistance Axis**

Horizontal motion is governed by the brain's "laterality bias," which is heavily influenced by reading direction. For Western viewers, left-to-right (L-R) movement is perceived as natural and represents progress and completion.30 This is termed the "Super Mario Setup," where the hero moves right into new territory.30

Movement from right-to-left (R-L) is perceived as more "difficult," "negative," or "regressive".31 Empirical tests show that viewers rate R-L motion as having higher "Negative Affect".32 Furthermore, L-R movement is perceived as faster and easier to process, whereas R-L movement causes the eyes to "jump" back and forth, increasing cognitive effort and creating a sense of resistance.30

| Axis | Direction | Semantic Association | Scoring Implication |
| :---- | :---- | :---- | :---- |
| Vertical | Up | Aspiration / Power | \+Arousal / \+Presence 5 |
| Vertical | Down | Loss / Submission | \-Arousal / \+Presence 7 |
| Horizontal | L-R | Progress / Normalcy | \-Arousal / \++Presence 31 |
| Horizontal | R-L | Conflict / Resistance | \++Arousal / \-Presence 32 |

## **Animating the Static: Ken Burns and Multi-Layer Parallax**

A core requirement for many video systems is the animation of static, often AI-generated, images. This is primarily achieved through the "Ken Burns Effect" (slow zoom and pan) or the more advanced "Z-Space Parallax Sandwich" (M-16).

## **Engagement: Static vs. Dynamic Content**

Eye-tracking studies consistently demonstrate the superiority of dynamic content in capturing and holding attention. Videos (such as trailers) receive 5.7x more fixations and significantly longer fixation durations than static designs (such as posters).33 Dynamic media reduces extraneous cognitive load by guiding the viewer's gaze through motion cues, facilitating "germane load" which helps in processing narrative information.33

However, the effectiveness of the animation depends on its "biological" quality. The "Human Movement Effect" suggests that learners and viewers respond more strongly to motion that mimics the movement of a person or a natural observer.1 This supports the use of "M-12: Breathing Effect" over a perfectly linear mechanical zoom, as the subtle unsteadiness provides a "social signal" that increases presence and empathy.4

## **The 0.6 Scaling Rule for Parallax Realism**

The "Z-Space Parallax Sandwich" (M-16) relies on the principle that foreground objects move faster than background objects across the retina. For this to feel "real" on a flat mobile screen, a specific mathematical relationship must be maintained. Research found that in the absence of binocular stereopsis (the depth seen with two eyes in VR), the mapping between motion and viewpoint change should be approximately 0.6.35

If the parallax layers are moved at a 1:1 ratio based on their supposed depth, the effect feels "too fast" or distorted because the brain's stereoscopic system is still reporting a flat screen surface. By scaling the motion mapping down to 0.6, the brain can resolve the monocular depth cues (parallax and occlusion) in a way that feels like a "window" into three-dimensional space, maximizing the Presence score.35

## **Contextual Application: Talking Heads and Short-Form Social Media**

The application of motion to "Talking Head" A-Roll (standard interview or vlog footage) is a balancing act between engagement and distraction.

## **The Arousal-Presence Tradeoff in Content Delivery**

In social media contexts like TikTok or Reels, where users are often viewing in "unenclosed environments" (public spaces with distractions), they are highly susceptible to external stimuli.37 Subtle motion—like a "Slow Zoom" (M-01) or "Breathing Effect" (M-12)—is essential for "masking" these distractors and maintaining a focused state of immersion.38

However, studies comparing animated vs. talking-head videos for science communication found no significant difference in knowledge transfer, suggesting that for high-information content, movement should be kept "subtle" (Low Arousal / High Presence) to avoid overloading the working memory.11 "M-14: Dynamic Handheld Drift" may be too aggressive for educational A-roll, while "M-12: Breathing Effect" provides the necessary dynamism to prevent "boredom" without disrupting comprehension.4

## **Millennial Adaptability to Small Screens**

An important demographic finding is that "Millennials" (and by extension Gen Z) are highly adapted to smartphone viewing. For these users, screen size and external distractions have less of an impact on immersion than they do for older generations.37 They compensate for the small screen by adjusting their physical position and are capable of achieving "cinema-like" states of empathy and comprehension on a 6-inch display, provided the motion effects are "loyal to cinematic formulae".37 This suggests that high Presence scores can be reliably assigned to complex effects like the "Z-Space Parallax Sandwich" for these target audiences.

## **Quantified Scoring Framework for the Motion Effects Library**

Integrating the aforementioned findings, we can assign precise Arousal and Presence scores to the 16 effects. These scores are calibrated for vertical mobile viewing, assuming a 60–120Hz display and a millennial/Gen Z target audience.

| Effect ID | Effect Name | Arousal (1–10) | Presence (1–10) | CLS (1–5) | Psychological Trigger |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **M-01** | Slow Zoom In | 3 | 8 | 1 | Intimacy / Looming Effect 41 |
| **M-02** | Speed Ramp Chaos | 9 | 2 | 5 | Startle / Temporal Disorientation 22 |
| **M-03** | Anxiety Camera Shake | 9 | 3 | 4 | Sympathetic Stress Response 3 |
| **M-04** | Standard Pan (L-R) | 2 | 6 | 1 | Flow / Narrative Progress 31 |
| **M-05** | Resistance Pan (R-L) | 4 | 5 | 2 | Conflict / Search Effort 30 |
| **M-06** | Heroic Tilt Up | 5 | 7 | 2 | Power / Aspiration / Awe 26 |
| **M-07** | Vulnerable Tilt Down | 3 | 6 | 2 | Submission / Sadness / Descent 5 |
| **M-08** | Whip Pan Transition | 7 | 1 | 3 | Jolt / Energy / Spatial Reveal 3 |
| \*\***M-09** | Dolly Push-In | 4 | 9 | 1 | Walking Toward / Intimacy 42 |
| **M-10** | Dolly Pull-Out | 2 | 5 | 1 | Detachment / Isolation 6 |
| **M-11** | Vertigo Dolly Zoom | 8 | 4 | 4 | Depth Distortion / Conflict 41 |
| **M-12** | Breathing Effect | 4 | 9 | 1 | Biological Signal / Empathy 8 |
| **M-13** | Subtle Handheld Drift | 5 | 7 | 2 | Realism / Documentary Feel 3 |
| **M-14** | Dynamic Handheld Drift | 7 | 6 | 3 | Urgency / High Kinetic Energy 7 |
| **M-15** | Vertical Drift (Slow) | 3 | 7 | 2 | Atmospheric / Contemplative 9 |
| **M-16** | Z-Space Sandwich | 3 | 10 | 3 | Optimal Parallax / Realism 35 |

## **Conclusion: Strategic Implementation for Automated Systems**

The research indicates that the most effective motion effects for mobile-first engagement are those that maximize the **Presence/Arousal ratio**. For an automated editing system to be successful on platforms like TikTok or YouTube Shorts, it must move away from simply adding "energy" (high arousal) and instead focus on "immersion" (high presence).

1. **High Presence, Low Arousal (The Engagement Core):** Effects like **M-01, M-09, M-12,** and **M-16** should be the "default" for narrative content. They leverage biological signals and the 0.6 parallax rule to keep viewers focused on the screen, effectively masking external distractions in mobile environments.8  
2. **High Arousal, Low Presence (The Pattern Interrupt):** Effects like **M-02, M-03,** and **M-08** are "shocks to the system." They should be used only at transition points or major narrative beats. Over-use will lead to high CLS and viewer fatigue, causing them to exit the content.3  
3. **Directional Semantics as Emotional Metadata:** The system should align **M-04/M-06** with positive sentiments and **M-05/M-07** with negative ones to reinforce the underlying narrative through low-level visual cues.31  
4. **Vection Management:** For fast-paced content, the system must monitor the "acceleration duration" of effects. By keeping movements linear and avoiding rapid oscillation, the system can induce vection (presence) without crossing the threshold into VIMS (nausea).10

By applying these quantified metrics, an automated editing system can produce content that is not only visually dynamic but also physiologically optimized for the modern mobile spectator.

#### **Works cited**

1. The effect of dynamic versus static visualizations on acquisition of basketball game actions: a diurnal study \- PMC, accessed March 23, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC10593838/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10593838/)  
2. An embodiment of the cinematographer: emotional and perceptual responses to different camera movement techniques \- PMC, accessed March 23, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC10352452/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10352452/)  
3. Essential Camera Movements in Cinematography to Know for Production I \- Fiveable, accessed March 23, 2026, [https://fiveable.me/lists/essential-camera-movements-in-cinematography](https://fiveable.me/lists/essential-camera-movements-in-cinematography)  
4. Smartphone Spectatorship in Unenclosed Environments: The Physiological Impacts of Visual and Sonic Distraction During Movie Watching on Mobile Devices | Request PDF \- ResearchGate, accessed March 23, 2026, [https://www.researchgate.net/publication/360229140\_Smartphone\_Spectatorship\_in\_Unenclosed\_Environments\_The\_Physiological\_Impacts\_of\_Visual\_and\_Sonic\_Distraction\_During\_Movie\_Watching\_on\_Mobile\_Devices](https://www.researchgate.net/publication/360229140_Smartphone_Spectatorship_in_Unenclosed_Environments_The_Physiological_Impacts_of_Visual_and_Sonic_Distraction_During_Movie_Watching_on_Mobile_Devices)  
5. Basics of Video Shooting: Understanding Camera Movements and Their Dramatic Impact, accessed March 23, 2026, [https://www.tamron.eu/da-DK/newsroom/blog/basics-of-video-shooting-understanding-camera-movements-and-their-dramatic-impact](https://www.tamron.eu/da-DK/newsroom/blog/basics-of-video-shooting-understanding-camera-movements-and-their-dramatic-impact)  
6. Types of Camera Movements in Film Explained: Definitive Guide \- StudioBinder, accessed March 23, 2026, [https://www.studiobinder.com/blog/different-types-of-camera-movements-in-film/](https://www.studiobinder.com/blog/different-types-of-camera-movements-in-film/)  
7. Camera Movement Tutorial: How To Create Emotion \- The Slanted Lens, accessed March 23, 2026, [https://theslantedlens.com/camera-movement-tutorial-how-to-create-emotion/](https://theslantedlens.com/camera-movement-tutorial-how-to-create-emotion/)  
8. (PDF) The “Breathing” Camera: Psychological Effects of Human-Like ..., accessed March 23, 2026, [https://www.researchgate.net/publication/365363126\_The\_Breathing\_Camera\_Psychological\_Effects\_of\_Human-Like\_Camera\_Flow\_in\_Visual\_Narratives\_Doctoral\_dissertation\_Indiana\_University](https://www.researchgate.net/publication/365363126_The_Breathing_Camera_Psychological_Effects_of_Human-Like_Camera_Flow_in_Visual_Narratives_Doctoral_dissertation_Indiana_University)  
9. Static vs. Dynamic Shots in Filmmaking and How to Edit With Them \- EditMentor, accessed March 23, 2026, [https://editmentor.com/blog/static-vs-dynamic-shots-skyrocketing-visual-impact/](https://editmentor.com/blog/static-vs-dynamic-shots-skyrocketing-visual-impact/)  
10. arXiv:1611.06292v1 \[cs.HC\] 19 Nov 2016, accessed March 23, 2026, [https://arxiv.org/pdf/1611.06292](https://arxiv.org/pdf/1611.06292)  
11. Comparing the effectiveness of animated videos and talking‐head videos in science communication \- PMC, accessed March 23, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC11840882/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11840882/)  
12. Vection and visually induced motion sickness: how are they related ..., accessed March 23, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC4403286/](https://pmc.ncbi.nlm.nih.gov/articles/PMC4403286/)  
13. Vection induced by a pair of patches of synchronized visual motion stimuli covering total field of views as small as 10 square-degrees \- PMC, accessed March 23, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC10521291/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10521291/)  
14. Motion and Cyber Sickness \- Balance & Dizziness Canada, accessed March 23, 2026, [https://balanceanddizziness.org/disorders/vestibular-disorders/motion-and-cyber-sickness/](https://balanceanddizziness.org/disorders/vestibular-disorders/motion-and-cyber-sickness/)  
15. What is Cybersickness? Why VR and scrolling can leave kids dizzy \- Gabb, accessed March 23, 2026, [https://gabb.com/blog/what-is-cybersickness/](https://gabb.com/blog/what-is-cybersickness/)  
16. Cybersickness: What It Is, Symptoms, Causes, and Treatments \- Healthline, accessed March 23, 2026, [https://www.healthline.com/health/cybersickness](https://www.healthline.com/health/cybersickness)  
17. To move or not to move… is that your question? | Blog \- Meta Quest for Creators, accessed March 23, 2026, [https://creator.oculus.com/blog/to-move-or-not-to-move-is-that-your-question/](https://creator.oculus.com/blog/to-move-or-not-to-move-is-that-your-question/)  
18. How can I eliminate this awful flickering/jitter when panning? (Please see the details in the comments.) : r/Filmmakers \- Reddit, accessed March 23, 2026, [https://www.reddit.com/r/Filmmakers/comments/13h0i6e/how\_can\_i\_eliminate\_this\_awful\_flickeringjitter/](https://www.reddit.com/r/Filmmakers/comments/13h0i6e/how_can_i_eliminate_this_awful_flickeringjitter/)  
19. panSpeedCalc \- PHFX.COM | tools, accessed March 23, 2026, [https://phfx.com/tools/panSpeedCalc/](https://phfx.com/tools/panSpeedCalc/)  
20. Pan speeds? \- Cinematography \- Creative COW, accessed March 23, 2026, [https://creativecow.net/forums/thread/pan-speedsae/](https://creativecow.net/forums/thread/pan-speedsae/)  
21. Why are my pans jittery ? : r/cinematography \- Reddit, accessed March 23, 2026, [https://www.reddit.com/r/cinematography/comments/1c03moh/why\_are\_my\_pans\_jittery/](https://www.reddit.com/r/cinematography/comments/1c03moh/why_are_my_pans_jittery/)  
22. Investigators in a scientific study find that "120 fps is an important threshold for VR" \- to reduce nausea and discomfort : r/ValveIndex \- Reddit, accessed March 23, 2026, [https://www.reddit.com/r/ValveIndex/comments/1atrwux/investigators\_in\_a\_scientific\_study\_find\_that\_120/](https://www.reddit.com/r/ValveIndex/comments/1atrwux/investigators_in_a_scientific_study_find_that_120/)  
23. Does Frame Rate in VR Cause Motion Sickness? \- Consensus: AI Search Engine for Research, accessed March 23, 2026, [https://consensus.app/home/blog/does-frame-rate-in-vr-cause-motion-sickness/](https://consensus.app/home/blog/does-frame-rate-in-vr-cause-motion-sickness/)  
24. Basics of Video Shooting: Understanding Camera Movements and Their Dramatic Impact, accessed March 23, 2026, [https://www.tamron.eu/de-CH/newsroom/blog/basics-of-video-shooting-understanding-camera-movements-and-their-dramatic-impact](https://www.tamron.eu/de-CH/newsroom/blog/basics-of-video-shooting-understanding-camera-movements-and-their-dramatic-impact)  
25. Content Quality Standards: Camera Stabilization / Movement | Shutterstock Contributor, accessed March 23, 2026, [https://submit.shutterstock.com/help/en/articles/10617466-content-quality-standards-camera-stabilization-movement](https://submit.shutterstock.com/help/en/articles/10617466-content-quality-standards-camera-stabilization-movement)  
26. Camera Angles Decoded: The Hidden Psychology Behind Character Perception \- FilmLocal, accessed March 23, 2026, [https://filmlocal.com/filmmaking/camera-angles-decoded/](https://filmlocal.com/filmmaking/camera-angles-decoded/)  
27. The effect of different vertical camera-angles on faceperception. \- Essay \- UT Student Theses, accessed March 23, 2026, [https://essay.utwente.nl/fileshare/file/60111/scriptie\_H\_S%C3%A4ttelli.pdf](https://essay.utwente.nl/fileshare/file/60111/scriptie_H_S%C3%A4ttelli.pdf)  
28. Effect of Camera Angle on Perception of Trust and Attractiveness, accessed March 23, 2026, [https://experimental.psychologie.uni-mainz.de/files/2024/06/2018BaranowskiHecht\_Camera\_Angle.pdf](https://experimental.psychologie.uni-mainz.de/files/2024/06/2018BaranowskiHecht_Camera_Angle.pdf)  
29. Bringing Scenes to Life: The Art of Camera Movements • Journalism ..., accessed March 23, 2026, [https://journalism.university/electronic-media/the-art-of-camera-movements-in-film/](https://journalism.university/electronic-media/the-art-of-camera-movements-in-film/)  
30. The Psychology of Camera Movement : r/Filmmakers \- Reddit, accessed March 23, 2026, [https://www.reddit.com/r/Filmmakers/comments/133sef/the\_psychology\_of\_camera\_movement/](https://www.reddit.com/r/Filmmakers/comments/133sef/the_psychology_of_camera_movement/)  
31. Why a Character's Left or Right Movement in Film Matters | No Film School, accessed March 23, 2026, [https://nofilmschool.com/left-to-right-movement-film](https://nofilmschool.com/left-to-right-movement-film)  
32. (PDF) Which Way Did He Go? Directionality of Film Character and Camera Movement and Subsequent Spectator Interpretation \- ResearchGate, accessed March 23, 2026, [https://www.researchgate.net/publication/228448619\_Which\_Way\_Did\_He\_Go\_Directionality\_of\_Film\_Character\_and\_Camera\_Movement\_and\_Subsequent\_Spectator\_Interpretation](https://www.researchgate.net/publication/228448619_Which_Way_Did_He_Go_Directionality_of_Film_Character_and_Camera_Movement_and_Subsequent_Spectator_Interpretation)  
33. Analyzing Audience Engagement in Static Versus Dynamic Media Content Using Eye-Tracking and Instagram Metrics Through the Lens of TPB and CLT \- Article (Preprint v1) by Kareem Mohamed Abdelhafeez Mahfouz Hussein et al. | Qeios, accessed March 23, 2026, [https://www.qeios.com/read/F16VXK](https://www.qeios.com/read/F16VXK)  
34. What Really Grabs People's Attention \- Static or Dynamic Content? \- RealEye.io, accessed March 23, 2026, [https://www.realeye.io/blog/post/what-really-grabs-peoples-attention--static-or-dynamic-content](https://www.realeye.io/blog/post/what-really-grabs-peoples-attention--static-or-dynamic-content)  
35. Perceptual Distortions Between Windows and Screens: Stereopsis ..., accessed March 23, 2026, [https://www.biomotionlab.ca/Text/WangEtAl\_IEEEVR2020.pdf](https://www.biomotionlab.ca/Text/WangEtAl_IEEEVR2020.pdf)  
36. (PDF) A Room with a Cue: The Efficacy of Movement Parallax, Occlusion, and Blur in Creating a Virtual Window \- ResearchGate, accessed March 23, 2026, [https://www.researchgate.net/publication/220089591\_A\_Room\_with\_a\_Cue\_The\_Efficacy\_of\_Movement\_Parallax\_Occlusion\_and\_Blur\_in\_Creating\_a\_Virtual\_Window](https://www.researchgate.net/publication/220089591_A_Room_with_a_Cue_The_Efficacy_of_Movement_Parallax_Occlusion_and_Blur_in_Creating_a_Virtual_Window)  
37. Watching films on a small screen has an impact on comprehension ..., accessed March 23, 2026, [https://www.gu.se/en/news/watching-films-on-a-small-screen-has-an-impact-on-comprehension-and-immersion](https://www.gu.se/en/news/watching-films-on-a-small-screen-has-an-impact-on-comprehension-and-immersion)  
38. The Effects of Smartphone Spectatorship on Attention, Arousal, Engagement, and Comprehension \- PMC, accessed March 23, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC7900791/](https://pmc.ncbi.nlm.nih.gov/articles/PMC7900791/)  
39. Smartphone spectatorship in unenclosed environments \- DORAS | DCU Research Repository, accessed March 23, 2026, [https://doras.dcu.ie/31830/1/2024\_Smartphone%20spectatorship%20in%20unenclosed%20environments\_Entertainment%20Computing.pdf](https://doras.dcu.ie/31830/1/2024_Smartphone%20spectatorship%20in%20unenclosed%20environments_Entertainment%20Computing.pdf)  
40. Long Room Hub (Scholarly Publications) \- TARA, accessed March 23, 2026, [https://www.tara.tcd.ie/collections/33da9241-86a1-4bd8-b309-bf9e897a900b/browse/dateissued](https://www.tara.tcd.ie/collections/33da9241-86a1-4bd8-b309-bf9e897a900b/browse/dateissued)  
41. What is a dolly zoom: How to film the Vertigo effect \- Adobe, accessed March 23, 2026, [https://www.adobe.com/creativecloud/video/production/cinematography/camera-shots-and-angles/dolly-zoom-shot.html](https://www.adobe.com/creativecloud/video/production/cinematography/camera-shots-and-angles/dolly-zoom-shot.html)  
42. The Visual and Emotional Effects of Using Dolly and Zoom Shots in Your Film, accessed March 23, 2026, [https://nofilmschool.com/2017/02/visual-and-emotional-effects-using-dolly-and-zoom-shots-your-film](https://nofilmschool.com/2017/02/visual-and-emotional-effects-using-dolly-and-zoom-shots-your-film)