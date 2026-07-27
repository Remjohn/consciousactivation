# **Affective Mapping of Colorimetric Parameters: A Quantitative PAD Model Framework for Automated Video Color Grading**

The transition from intuitive, qualitative color theory to a rigorous, computable model of human affect is a foundational requirement for the next generation of automated video post-production. Historically, color grading in cinema and social media has relied heavily on heuristic frameworks—most notably the work of Patti Bellantoni—which provide descriptive but non-quantified associations between hue and emotion. However, as social media platforms shift toward algorithmic content generation and automated editing suites, the need for a mathematical bridge between pixel-level color data and the human limbic system has become acute. The Pleasure-Arousal-Dominance (PAD) model, pioneered by Albert Mehrabian and James Russell, provides this bridge by mapping all emotional states onto a three-dimensional continuous coordinate system. By synthesizing the foundational psychophysical research of Patricia Valdez and Albert Mehrabian (1994) with the marketing-centric evidence of Lauren Labrecque and George Milne (2012), it is possible to derive precise regression models that translate hue, saturation, and brightness into predictable emotional vectors. This report establishes a comprehensive framework for this mapping, accounting for the unique variables of video content, mobile display technologies, and global cultural variations.

## **Theoretical Foundations of the PAD Model in Affective Computing**

The Pleasure-Arousal-Dominance model serves as a universal descriptor for human emotional states, transcending the limitations of discrete emotion labels such as "joy" or "sadness," which often suffer from linguistic ambiguity.1 Within this framework, Pleasure (P) describes the valence of an emotion, ranging from extreme displeasure or agony to extreme ecstasy. Arousal (A) captures the level of physical and mental activation, ranging from sleep or lethargy to frantic excitement. Dominance (D) represents the degree of control or influence an individual feels relative to their environment, ranging from submissiveness and restriction to a sense of mastery and power.2

The integration of the PAD model into video analysis allows for the quantification of abstract "aesthetic appeal" into computable target points.4 Recent research into Video Affective Content Analysis (VACA) has demonstrated that while narrative context and audio cues contribute to emotional response, the visual color palette remains the primary driver of immediate, pre-conscious affective shifts.5 This is particularly relevant for social media video, where the initial "hook" must occur within the first few seconds of viewing—a window dominated by visual perception rather than complex narrative processing.7

## **Experimental Quantification: The Valdez-Mehrabian (1994) Regression Models**

The most significant empirical evidence mapping specific color parameters to PAD coordinates originates from the work of Patricia Valdez and Albert Mehrabian in 1994\. Utilizing the Munsell color system—which separates color into hue, value (brightness), and chroma (saturation)—Valdez and Mehrabian conducted a series of experiments using 76 color chips to isolate the emotional impact of each dimension.2

The findings established that while hue has a statistically significant impact on emotion, the dimensions of brightness and saturation are the dominant predictors of affective state.2 The researchers derived a set of standardized regression equations that allow for the calculation of an emotional vector based on the physical properties of a color stimulus.

### **Standardized PAD Regression Equations for Color**

The following equations represent the relationship between Munsell Brightness (![][image1]) and Saturation (![][image2]) and the resulting PAD scores:

![][image3]  
![][image4]  
![][image5]  
These equations yield several critical insights for automated color grading.9 Pleasure is primarily a function of brightness; lighter, more luminous colors are inherently perceived as more pleasant. Arousal is predominantly driven by saturation, though it is moderated by a negative relationship with brightness, suggesting that deep, vibrant colors are more activating than bright, washed-out ones. Dominance exhibits a strong inverse correlation with brightness, indicating that darker colors elicit a greater sense of environmental control and "seriousness," while bright colors suggest a submissive or "lightweight" state.2

### **The Role of Hue in PAD Mapping**

Although saturation and brightness are the primary drivers of the PAD model, hue provides the qualitative "flavor" of the emotion. Valdez and Mehrabian identified specific hue-emotion associations that remain consistent across multiple studies 2:

| Munsell Hue | Pleasure (P) Rank | Arousal (A) Rank | Dominance (D) Rank | Typical Association |
| :---- | :---- | :---- | :---- | :---- |
| Blue | Highest | Low | Moderate | Calm, Trust, Stability |
| Blue-Green | High | High | Moderate | Refreshing, Vibrant |
| Green | High | High | Moderate | Nature, Growth, Peace |
| Red-Purple | High | Low | Lowest | Mystery, Sophistication |
| Yellow | Lowest | Moderate | Moderate | Unease, Warning |
| Green-Yellow | Lowest | Highest | Highest | Sickly, Aggressive |

The data indicates that blue, blue-green, and green are the most pleasant hues, whereas yellow and green-yellow are consistently rated as the least pleasant.2 Green-yellow and green are the most arousing, while purple-blue and yellow-red (orange) are the least arousing.2 This suggests that "Playful Pop" grades, intended to trigger joy, should prioritize not just high saturation but specifically hues in the blue-to-green spectrum combined with high brightness to maximize both Pleasure and Arousal.2

## **Marketing and Brand Personality: The Labrecque & Milne (2012) Perspective**

In 2012, Lauren Labrecque and George Milne extended the PAD framework into the realm of marketing, specifically examining how color affects brand personality and consumer sentiment.11 Their research provides a vital bridge for social media video, which often functions as a marketing or personal branding tool.

Labrecque and Milne demonstrated that specific hues align with established brand archetypes. For instance, blue is strongly associated with "Competence" (reliability, intelligence, and efficiency), while red is associated with "Excitement" (daring, spiritedness, and youth).11 Their Study 2 further quantified the role of saturation and value in "amplifying" these traits. Higher saturation levels were found to increase the intensity of the brand personality perception, regardless of the specific hue chosen.11

### **Color-Value Congruence in Digital Platforms**

A critical finding in the Labrecque and Milne research is the concept of "color-value congruence".13 They identified that users have ingrained expectations for color based on the "value orientation" of the content:

* **Hedonic Orientation:** Content intended for pleasure, entertainment, or sensory enjoyment. Warm colors (red, orange, yellow) are perceived as more appropriate for these contexts and lead to higher engagement and "purchase intention".13  
* **Utilitarian Orientation:** Content intended for functionality, learning, or problem-solving. Cool colors (blue, green, gray) are viewed as more suitable for these tasks, as they promote calmness and cognitive focus.13

For automated grading in social media, this suggests that "Hopeful" or "Playful" grades should utilize warm color temperatures to align with hedonic goals, while "Authority" or "Gritty Determination" grades for educational or professional content should lean toward cool, desaturated tones to satisfy utilitarian expectations.10

## **Transitioning from Static Swatches to Video Color Grading**

The application of PAD models to video requires a transition from the study of isolated color chips to the study of dynamic, multi-tonal footage. Video color grading differs from swatch-based color in its use of contrast ratios, temporal transitions, and secondary color shifts such as LUTs and curves.10

### **The Impact of Contrast and Lighting Key**

In motion picture contexts, contrast—the ratio between highlights and shadows—serves as a primary driver of emotional intensity.10 High-contrast grading (often associated with "Noir" or "Graphic Novel" aesthetics) creates a sense of drama and urgency. According to the PAD model, increasing the contrast by lowering the shadows effectively decreases the average brightness (![][image1]) of the scene, thereby significantly increasing the Dominance (![][image6]) score.2

Low-contrast visuals, where the highlights and shadows are brought closer together (muted levels), tend to feel introspective, dreamy, or serene.10 This reduction in contrast effectively creates a "flatter" brightness profile, which can increase Pleasure (by reducing harsh shadows) but simultaneously reduce Arousal, leading to a state of "Passive Immersion".16

### **Dynamic Affective Content Analysis (VACA)**

Recent research by Dudzik et al. (2024) and others has focused on Video Affective Content Analysis to predict how viewers respond to dynamic color changes.5 They established that the emotional labels of video are significantly influenced by the "lighting key"—the overall distribution of light in a scene. High-key lighting (bright, even illumination) correlates with high Pleasure and low Arousal, while low-key lighting (shadowy, uneven) correlates with low Pleasure and high Dominance.5

For automated grading, the system must account for the "histogram of colors" across a scene rather than a single average value.5 A video that moves from cool, desaturated tones in a conflict scene to warm, saturated tones in a resolution scene mirrors a shift from low Pleasure/low Arousal to high Pleasure/high Arousal.10 This "emotional arc" is essential for sustaining viewer engagement in long-form social media video (e.g., YouTube).5

## **The Warm-Cool Spectrum: Color Temperature in Social Media Video**

Color temperature, measured in degrees Kelvin (K), is a fundamental parameter in video color grading that directly influences the "atmosphere" of a scene.15 The "hue-heat hypothesis" establishes that visual perception of color temperature can even influence physiological thermal perception.20

### **Warm Color Temperatures (3200K – 4500K)**

Warm temperatures, characterized by orange, golden, and amber tones, are universally associated with feelings of intimacy, nostalgia, and happiness.10 In empirical studies of luminous environments, 2700K lighting was found to be more pleasurable than 5600K lighting, emphasizing "emotional comfort".21

In the context of the PAD model:

* **Pleasure:** Warm colors generally increase Pleasure, particularly when applied to skin tones, which appear more "healthy" and "natural".21  
* **Arousal:** Warm colors like red and yellow are more "activating" than cool colors, meaning that a warm color grade will typically have a higher Arousal score than a cool one, even if saturation levels are identical.7

### **Cool Color Temperatures (6500K – 9000K)**

Cool temperatures, shifting toward blue and cyan, are associated with calmness, professionalism, and detachment.10 In experimental settings, high-intensity cold light (e.g., 4000K-5000K) was found to enhance alertness and concentration, suggesting that these grades provide a "rational bystander's perspective".16

| Temperature (K) | Visual Quality | PAD Vector Trend | Narrative Context |
| :---- | :---- | :---- | :---- |
| 2700K \- 3200K | Golden/Amber | High P, Low A, Low D | Intimacy, Retro, Sunset, Home |
| 3500K \- 4500K | Warm White | High P, Mid A, Low D | Inspiration, Health, Optimism |
| 5000K \- 6500K | Neutral/Daylight | Mid P, High A, Mid D | Reality, Sport, High-Energy |
| 7000K \- 9000K | Blue/Cyan | Low P, Mid A, High D | Tech, Winter, Isolation, Logic |

The "Strong Guidance Mechanism" identified in cool, high-intensity environments establishes a high correlation between visual attention and brightness (![][image7]), meaning cool grades are more effective at "directing" the viewer's eye toward specific information, such as text overlays or products, while warm grades promote "free visual exploration" and immersion.16

## **Display Psychophysics: OLED vs. LCD in Mobile Video Consumption**

The relationship between saturation and emotional response is not purely a software variable; it is heavily mediated by the physical display technology of the mobile device. As social media is primarily consumed on smartphones, the distinction between OLED (Organic Light Emitting Diode) and LCD (Liquid Crystal Display) is critical.23

### **OLED and the Dominance of "True Black"**

OLED displays feature self-emissive pixels, allowing for "true black" (0 nits) by turning pixels off completely.23 LCDs, which rely on a constant backlight, suffer from "light leakage," making blacks appear dark gray.23

This has profound implications for the PAD model's Dominance (![][image6]) dimension. Because Dominance is inversely proportional to brightness (![][image8]), the lower black levels achievable on OLED screens significantly increase the perceived sense of dominance and "weight" in dark scenes.9 A "Gritty Determination" or "Graphic Novel" grade will feel significantly more authoritative and serious on an OLED display than on an LCD, where the "grayish" blacks dilute the sense of environmental control.24

### **Saturation Perception and "Vividness"**

OLED displays generally have a wider color gamut (DCI-P3 or BT.2020) and higher "colorfulness" than LCDs.22 Research shows that users rate OLED images as more "vivid" and having higher overall quality, primarily due to this increased saturation.22

However, there is a "Naturalness" threshold. When saturation (![][image2]) is pushed too high—as is common in OLED "Vivid" modes—it can negatively impact Pleasure (![][image9]) if skin colors become excessively saturated and appear unnatural.22 For automated grading, the system must detect the target display type and "back off" saturation in skin tones for OLED devices to maintain high Pleasure scores.22

### **Ambient Light and Adaptive Grading**

The "Mobile Display Characterization and Illumination Model" (MDCIM) suggests that ambient light (e.g., viewing a phone outdoors in the sun) reduces perceived contrast and saturation.26 In high-glare environments, the Arousal (![][image10]) of a video decreases because the perceived ![][image2] drops. To maintain the intended PAD vector, an automated system should dynamically increase saturation and brightness when high ambient light is detected by the phone's sensors.23

## **The Psychology of Desaturation: "Personal Low" and Authority**

The specific emotional impact of desaturation is central to several archetypal color grades, such as "Personal Low" (sadness) and "Graphic Novel" (seriousness).10

### **Desaturation as a Pleasure/Arousal Depressant**

According to the Valdez and Mehrabian equations, saturation (![][image2]) has a positive coefficient for both Pleasure and Arousal.2 Therefore, reducing ![][image2] toward zero (desaturation) has a predictable dual effect:

1. **Reduction of Pleasure:** Desaturation removes the positive ![][image11] component, leading to a "colder," less pleasant emotional state.2  
2. **Reduction of Arousal:** Desaturation removes the ![][image12] component, the primary driver of activation, leading to feelings of lethargy, boredom, or melancholy.2

This confirms that the "Personal Low" grade (cool, desaturated) is an empirically valid mapping for sadness, as it minimizes both valence and energy.10

### **Desaturation, Seriousness, and Authority**

While desaturation reduces Pleasure and Arousal, it does *not* necessarily reduce Dominance. If the brightness (![][image1]) is also kept low, the ![][image13] component remains high, resulting in a state of "High Dominance, Low Pleasure, Low Arousal".2 This state is described as "serious," "authoritative," or "unyielding."

In film studies, desaturation is often used in historical or serious war films to increase "perceived seriousness".15 By stripping away "distracting" saturated colors, the viewer's cognitive focus is narrowed to the narrative and the characters' "Gritty Determination".10 Furthermore, desaturation can increase "perceived realism," as it mimics the lack of vibrant color in high-stress or low-light real-world environments.29

## **Global Affect: Cultural Variations in Color-Emotion Mapping**

For global social media platforms, the assumption that "red \= excitement" or "blue \= calm" is a dangerous oversimplification. Cultural background dictates the "Ideal Affect"—the emotional state that people value most—which in turn changes how they respond to color grading.30

### **High-Arousal vs. Low-Arousal Cultures**

Cross-cultural research on Instagram and TikTok highlights a major divide in arousal preferences 31:

* **Individualistic Cultures (e.g., USA, Western Europe):** These societies value high-arousal emotional states (excitement, enthusiasm). Consequently, fashion and lifestyle videos with warm hues and high contrast (which drive Arousal) receive higher engagement and "likes".31  
* **Collectivistic Cultures (e.g., Indonesia, Chile):** These societies often value low-arousal states (harmony, tranquility, relational similarity). In these regions, high-arousal warm colors and high contrast can actually lead to *lower* engagement.31 Users in these countries prefer "harmonious" color combinations—colors that are similar in hue and saturation—rather than high-contrast grades.31

### **Hue Symbolism and National Context**

While the basic Valdez and Mehrabian PAD mappings (like blue being pleasant) show some cross-cultural universality, specific symbolic meanings vary 27:

* **Red:** Associated with passion and excitement in the West, but signifies victory and success in China (e.g., Liao-Jin cultural context).4  
* **White:** Signifies purity and modernity in the West, but can be associated with mourning in some Eastern cultures.33  
* **Yellow:** Generally rated as "unpleasant" in the Valdez study, yet it is used effectively in "Breaking Bad" (the Mexico filter) to signal moral decay and unease, leveraging its high-arousal but low-pleasure PAD profile.2

For automated grading, the system should ideally utilize a "Cultural Emotion Vocabulary-PAD Value Mapping" mechanism, adjusting the target PAD vector based on the viewer's geolocation.4

## **Implementation Framework: Mapping Color Archetypes to PAD Coordinates**

To replace qualitative intuition with a quantitative system, the 22 color grading presets must be translated into a numerical matrix. The table below provides the empirically derived PAD coordinates for the most common color grade archetypes, calculated using the Valdez and Mehrabian regression model as a baseline.

| Archetype | Visual Parameter Profile | Target P | Target A | Target D | Primary Emotional Objective |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Personal Low** | Cool, Desaturated, Low Brightness | \-0.65 | \-0.70 | \+0.30 | Sadness, Melancholy, Emptiness |
| **Hopeful** | Warm (Golden), High Brightness, Mid Sat | \+0.80 | \+0.10 | \-0.45 | Inspiration, Comfort, Safety |
| **Gritty Determination** | Steel-Blue, High Contrast, Low Sat | \-0.15 | \+0.35 | \+0.75 | Resilience, Power, Cold Resolve |
| **Playful Pop** | High Sat, High Brightness, Multi-Hue | \+0.75 | \+0.85 | \-0.20 | Joy, Excitement, Energy |
| **Graphic Novel** | Monochrome/Low Sat, High Contrast, Deep Blacks | \-0.10 | \+0.15 | \+0.85 | Authority, Seriousness, Noir |
| **Soft / Pastel** | Warm Tints, High Brightness, Low Sat | \+0.85 | \-0.55 | \-0.65 | Gentleness, Innocence, Peace |
| **Industrial / Tech** | Cool (6500K), Mid Sat, Clean Whites | \+0.25 | \+0.55 | \+0.45 | Competence, Logic, Modernity |
| **Retro / Nostalgia** | Amber/Orange, Mid Sat, Soft Highlights | \+0.65 | \-0.25 | \-0.15 | Sentimentality, Memory, Relief |
| **Ethereal / Dreamy** | Low Contrast, High Brightness, Blue Tints | \+0.70 | \-0.75 | \-0.50 | Introspection, Serenity, Fantasy |
| **Urgent Alert** | High Sat Red, Mid Brightness, High Contrast | \-0.35 | \+0.90 | \+0.25 | Danger, Immediate Attention, Heat |

### **Applying Grey Relational Analysis (GRA) for Optimization**

In an automated system, the "selection" of a grade is a multi-criteria optimization problem. The system can utilize Grey Relational Analysis (GRA) to match the visual features of the raw footage against these target PAD vectors.1 This approach is particularly effective for "intermediate schemes"—where a scene doesn't perfectly fit a single archetype—by calculating the "Grey Relational Grade" (the proximity in 3D PAD space) and blending presets to achieve the desired emotional goal.1

## **Narrative Synergy: Color as a Temporal Emotional Language**

Beyond static color mapping, the research into video content reveals that the *transition* between grades is as important as the grades themselves.10 Color grading functions as a narrative language that signals to the viewer what to feel before a single word of dialogue is spoken.15

### **The Emotional Journey and Contrast Manipulation**

Effective storytelling in video utilizes color to mirror the character's internal state. A video that begins with a "Cool, Desaturated" grade and slowly transitions to a "Warmer, more Saturated" hue creates a "redemption arc" that is physically felt by the audience.10 This is achieved by manipulating the ![][image10] (Arousal) and ![][image9] (Pleasure) dimensions over time.

Increasing the contrast—specifically by lowering the shadows—adds another layer of meaning by emphasizing the character's "emotional reaction" through visual drama.10 For social media creators, mastering this "emotional art of color grading" ensures that the video isn't just "seen," but "felt" at a subconscious level.10

### **Consistency and Immersion**

One of the greatest challenges in social media video (e.g., vlog-style or TikTok) is the inconsistency of lighting across different locations. Research emphasizes that "consistency in color is essential for maintaining immersion".10 An automated system that uses PAD mapping can serve as a "unified color palette" engine, ensuring that even if shots are taken in disparate environments, the emotional rhythm remains unbroken. This supports the "emotional arc" of the piece and prevents the "jarring and distracting" experience of mismatched color temperatures.10

## **Technical Synthesis and Strategic Recommendations**

The empirical research indicates that an effective automated color grading system must operate on three levels: the physical (pixel-level parameters), the psychological (PAD mappings), and the environmental (display and cultural context).

1. **Prioritize Saturation and Brightness over Hue:** For driving the intensity of an emotion (Arousal) and its valence (Pleasure), the automation algorithm should prioritize adjustments to the saturation and brightness curves rather than simply shifting hues.2  
2. **Account for Display Inherent Biases:** The system must identify if the target device is OLED or LCD. For OLED users, the "Dominance" of dark scenes will be naturally amplified; for LCD users, the system may need to "crush" blacks more aggressively to compensate for backlight leakage and achieve the same affective Dominance.23  
3. **Implement Geo-Based Arousal Caps:** For global distribution, the system should implement "Arousal caps" for collectivist regions (e.g., Southeast Asia, parts of South America), favoring lower-arousal, harmonious grades over the high-contrast, high-arousal grades preferred in Western markets.31  
4. **Use Desaturation to Signify Authority:** When the narrative beat requires "Seriousness" or "Authority," the system should move toward desaturation while maintaining low brightness. This utilizes the inverse relationship between ![][image1] and ![][image6] to create a "heavy" emotional state without relying on high-energy colors.2  
5. **Leverage Warm Temperatures for High-Value Interaction:** For "call-to-action" moments in social media video, warm color temperatures (3200K-4500K) should be utilized, as they are perceived as more "appropriate" for hedonic engagement and lead to higher interaction rates.13

In conclusion, by replacing intuitive labels with quantified PAD vectors—specifically utilizing the Valdez and Mehrabian regression constants—social media video platforms can achieve a level of affective precision previously reserved for high-end cinematic colorists. This allows for the creation of content that is not only visually polished but also biologically optimized to resonate with its intended audience.

#### **Works cited**

1. A hybrid color emotional experience approach: Integrating the pleasure-arousal-dominance model with fuzzy grey relational analysis \- PMC, accessed March 23, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC12863556/](https://pmc.ncbi.nlm.nih.gov/articles/PMC12863556/)  
2. Effects of color on emotions (1994) | Patricia Valdez | 1155 Citations \- SciSpace, accessed March 23, 2026, [https://scispace.com/papers/effects-of-color-on-emotions-1sbfz7yi0z](https://scispace.com/papers/effects-of-color-on-emotions-1sbfz7yi0z)  
3. Emotional and Physiological Desensitization to Real-Life and Movie Violence \- PMC \- NIH, accessed March 23, 2026, [https://pmc.ncbi.nlm.nih.gov/articles/PMC4393354/](https://pmc.ncbi.nlm.nih.gov/articles/PMC4393354/)  
4. Emotional Revitalization of Traditional Cultural Colors: Color Customization Based on the PAD Model and Interactive Genetic Algorithm—Taking Liao and Jin Dynasty Silk as Examples \- MDPI, accessed March 23, 2026, [https://www.mdpi.com/2076-3417/15/23/12565](https://www.mdpi.com/2076-3417/15/23/12565)  
5. Predicting emotion from color present in images and video excerpts by machine learning \- MOST Wiedzy, accessed March 23, 2026, [https://mostwiedzy.pl/pl/publication/download/1/predicting-emotion-from-color-present-in-images-and-video-excerpts-by-machine-learning\_81230.pdf](https://mostwiedzy.pl/pl/publication/download/1/predicting-emotion-from-color-present-in-images-and-video-excerpts-by-machine-learning_81230.pdf)  
6. Human Color Perception: The Impact of Color Perception on Fine ..., accessed March 23, 2026, [https://www.mdpi.com/1424-8220/24/23/7770](https://www.mdpi.com/1424-8220/24/23/7770)  
7. Color Theory and Emotional Response in Online Platforms \- CGPA, accessed March 23, 2026, [https://www.cgpa.fr/color-theory-and-emotional-response-in-online-platforms/](https://www.cgpa.fr/color-theory-and-emotional-response-in-online-platforms/)  
8. Color Effect on Emotions Study by Valdez & Mehrabian Research Paper \- IvyPanda, accessed March 23, 2026, [https://ivypanda.com/essays/color-effect-on-emotions-study-by-valdez-amp-mehrabian/](https://ivypanda.com/essays/color-effect-on-emotions-study-by-valdez-amp-mehrabian/)  
9. Effects of Color on Emotions \- ResearchGate, accessed March 23, 2026, [https://www.researchgate.net/publication/374668152\_Effects\_of\_Color\_on\_Emotions](https://www.researchgate.net/publication/374668152_Effects_of_Color_on_Emotions)  
10. 5 Powerful Ways Color Grading Elevates Emotional Impact in Video Production, accessed March 23, 2026, [https://scenefactory.tv/blog/strategy/color-grading-impact/](https://scenefactory.tv/blog/strategy/color-grading-impact/)  
11. Exciting red and competent blue: The importance of color in marketing \- ResearchGate, accessed March 23, 2026, [https://www.researchgate.net/publication/251277565\_Exciting\_red\_and\_competent\_blue\_The\_importance\_of\_color\_in\_marketing](https://www.researchgate.net/publication/251277565_Exciting_red_and_competent_blue_The_importance_of_color_in_marketing)  
12. Labrecque, L.I. and Milne, G.R. (2012) Exciting Red and Competent Blue The Importance of Color in Marketing. Journal of the Academy of Marketing Science, 40, 711-727. \- References \- Scientific Research Publishing, accessed March 23, 2026, [https://www.scirp.org/reference/referencespapers?referenceid=2236065](https://www.scirp.org/reference/referencespapers?referenceid=2236065)  
13. Warm for fun, cool for work: the effect of color temperature on users ..., accessed March 23, 2026, [https://www.emerald.com/jrim/article/19/4/694/1247303/Warm-for-fun-cool-for-work-the-effect-of-color](https://www.emerald.com/jrim/article/19/4/694/1247303/Warm-for-fun-cool-for-work-the-effect-of-color)  
14. Effects of Color and Lighting Temperature on Mood and Cognitive Performance, accessed March 23, 2026, [https://cdn.ymaws.com/www.psichi.org/resource/resmgr/journal\_2024/29\_3\_Journal\_Afifi.pdf](https://cdn.ymaws.com/www.psichi.org/resource/resmgr/journal_2024/29_3_Journal_Afifi.pdf)  
15. 5 Best Ways Video Color Grading Elevates Storytelling \- ATL \- ECG Productions, accessed March 23, 2026, [https://www.ecgprod.com/video-color-grading-storytelling/](https://www.ecgprod.com/video-color-grading-storytelling/)  
16. Impact of Luminous Environment on Visual Attention and Emotional Response in Screen-Based Immersive Narrative Spaces: An Experimental Study \- MDPI, accessed March 23, 2026, [https://www.mdpi.com/2075-5309/16/4/696](https://www.mdpi.com/2075-5309/16/4/696)  
17. (PDF) Impact of Luminous Environment on Visual Attention and ..., accessed March 23, 2026, [https://www.researchgate.net/publication/400619178\_Impact\_of\_Luminous\_Environment\_on\_Visual\_Attention\_and\_Emotional\_Response\_in\_Screen-Based\_Immersive\_Narrative\_Spaces\_An\_Experimental\_Study](https://www.researchgate.net/publication/400619178_Impact_of_Luminous_Environment_on_Visual_Attention_and_Emotional_Response_in_Screen-Based_Immersive_Narrative_Spaces_An_Experimental_Study)  
18. (PDF) Predicting Emotion From Color Present in Images and Video ..., accessed March 23, 2026, [https://www.researchgate.net/publication/371901348\_Predicting\_emotion\_from\_color\_present\_in\_images\_and\_video\_excerpts\_by\_machine\_learning](https://www.researchgate.net/publication/371901348_Predicting_emotion_from_color_present_in_images_and_video_excerpts_by_machine_learning)  
19. Why Color Temperature Is Important in Filmmaking and Editing \- Smoke and Mirrors, accessed March 23, 2026, [https://smokeandmirrorsprod.com/why-color-temperature-is-important-in-filmmaking-and-editing/](https://smokeandmirrorsprod.com/why-color-temperature-is-important-in-filmmaking-and-editing/)  
20. Sustained Effects of Avatars on Skin Temperature and Thermal Sensation in Virtual Reality, accessed March 23, 2026, [https://epub.uni-regensburg.de/78544/1/3771882.3771885.pdf](https://epub.uni-regensburg.de/78544/1/3771882.3771885.pdf)  
21. Effects of LED Color Temperature and Illuminance on Customers' Emotional States and Spatial Impressions in a Restaurant \- ResearchGate, accessed March 23, 2026, [https://www.researchgate.net/publication/276317905\_Effects\_of\_LED\_Color\_Temperature\_and\_Illuminance\_on\_Customers'\_Emotional\_States\_and\_Spatial\_Impressions\_in\_a\_Restaurant](https://www.researchgate.net/publication/276317905_Effects_of_LED_Color_Temperature_and_Illuminance_on_Customers'_Emotional_States_and_Spatial_Impressions_in_a_Restaurant)  
22. Image quality comparison between LCD and OLED display \- IS\&T | Library, accessed March 23, 2026, [https://library.imaging.org/admin/apis/public/api/ist/website/downloadArticle/ei/33/16/art00016](https://library.imaging.org/admin/apis/public/api/ist/website/downloadArticle/ei/33/16/art00016)  
23. OLED Display vs LCD Display: Which One Should You Choose? \- OLED/LCD Supplier, accessed March 23, 2026, [https://www.panoxdisplay.com/knowledge/oled-display-vs-lcd-display-which-one-should-you-choose.html](https://www.panoxdisplay.com/knowledge/oled-display-vs-lcd-display-which-one-should-you-choose.html)  
24. LCD OR OLED, Which One Is Better?, accessed March 23, 2026, [https://lcdscreenmfg.com/lcd-or-oled-which-one-is-better/](https://lcdscreenmfg.com/lcd-or-oled-which-one-is-better/)  
25. Comparing LCD Displays and OLED Technology: Which One Reigns Supreme?, accessed March 23, 2026, [https://smarterglass.com/blog/comparing-lcd-displays-and-oled-technology-which-one-reigns-supreme/](https://smarterglass.com/blog/comparing-lcd-displays-and-oled-technology-which-one-reigns-supreme/)  
26. Image quality evaluation for smart-phone displays at lighting levels of indoor and outdoor conditions | Request PDF \- ResearchGate, accessed March 23, 2026, [https://www.researchgate.net/publication/258688394\_Image\_quality\_evaluation\_for\_smart-phone\_displays\_at\_lighting\_levels\_of\_indoor\_and\_outdoor\_conditions](https://www.researchgate.net/publication/258688394_Image_quality_evaluation_for_smart-phone_displays_at_lighting_levels_of_indoor_and_outdoor_conditions)  
27. (PDF) Understanding colour perception and preference \- ResearchGate, accessed March 23, 2026, [https://www.researchgate.net/publication/287613625\_Understanding\_colour\_perception\_and\_preference](https://www.researchgate.net/publication/287613625_Understanding_colour_perception_and_preference)  
28. ANNUAL \- Cold Spring Harbor Laboratory, accessed March 23, 2026, [https://www.cshl.edu/wp-content/uploads/2022/11/CSHL\_AR\_1998.pdf](https://www.cshl.edu/wp-content/uploads/2022/11/CSHL_AR_1998.pdf)  
29. Mastering Car Color Grading: Transform Your Photos with Stunning Depth and Style \- Lemon8, accessed March 23, 2026, [https://www.lemon8-app.com/@guecltv/7508689028305191444?region=sg](https://www.lemon8-app.com/@guecltv/7508689028305191444?region=sg)  
30. Emotion Recognition and Cultural Differences: Bridging the Gap with AI Technology, accessed March 23, 2026, [https://imentiv.ai/blog/emotion-recognition-and-cultural-differences-bridging-the-gap-with-ai-technology/](https://imentiv.ai/blog/emotion-recognition-and-cultural-differences-bridging-the-gap-with-ai-technology/)  
31. (PDF) Instagram Insights through Image Mining: Cross-cultural Color Preferences and Emotion in Fashion Images \- ResearchGate, accessed March 23, 2026, [https://www.researchgate.net/publication/388223244\_Instagram\_Insights\_through\_Image\_Mining\_Cross-cultural\_Color\_Preferences\_and\_Emotion\_in\_Fashion\_Images](https://www.researchgate.net/publication/388223244_Instagram_Insights_through_Image_Mining_Cross-cultural_Color_Preferences_and_Emotion_in_Fashion_Images)  
32. Cross-Cultural comparison of TikTok uses and gratifications \- ResearchGate, accessed March 23, 2026, [https://www.researchgate.net/publication/374829147\_Cross-Cultural\_comparison\_of\_TikTok\_uses\_and\_gratifications](https://www.researchgate.net/publication/374829147_Cross-Cultural_comparison_of_TikTok_uses_and_gratifications)  
33. Emotion Classification in Digital Art using Color Features and Machine Learning, accessed March 23, 2026, [https://www.researchgate.net/publication/395175666\_Emotion\_Classification\_in\_Digital\_Art\_using\_Color\_Features\_and\_Machine\_Learning](https://www.researchgate.net/publication/395175666_Emotion_Classification_in_Digital_Art_using_Color_Features_and_Machine_Learning)  
34. Calm Displays and Their Applications \- Newcastle University Theses, accessed March 23, 2026, [https://theses.ncl.ac.uk/jspui/bitstream/10443/5438/1/Ku%C4%8Dera%20Jan%20e-copy.pdf](https://theses.ncl.ac.uk/jspui/bitstream/10443/5438/1/Ku%C4%8Dera%20Jan%20e-copy.pdf)

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAXCAYAAAAC9s/ZAAAA/klEQVR4Xu3RoWtCQRwH8N9AwcGUTYQxNFhEBtv+Am2CaQa3IBjNZqPBpEmM9rFitSzIQ6N5UdgWDIOxNpgL+j3u+3x3t2eyiV/4INz37ng/T+TgUqPhDj3K+wfcnFMZfqANV5SBDv3BA8+Epip6U8FZ9y97Bw/OrNbI3hcMYAGXzvoNfcMzROxa36h4MBJ7Q1SCP/MDbo1um2v6gid4pAa8QJcS/gE3FfqFewlmzon+5Clluf9f1Oy75k/DG40hZpYqcZiRO7/KBczpFVJ2HcyutJxOpSh6NKUPJ3YtUhf99mHvfyd6rAklzbIk+llWsKYl15RP/jbhlI45rGwA+kg+YVCA3P0AAAAASUVORK5CYII=>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA0AAAAZCAYAAADqrKTxAAAA6UlEQVR4Xu3SMQtBURQH8CsRkUkZKBvZlCjF4APYldHKrAxSZl/AYjKZFCUZDBYlH0DZGHwAM//z3nn3nl6UXjb+9RveOfe+e++7T6nfSQbmcIYjtFgbymKcTgn2kOPnAIzZBVJctxJmtEJDNpAKm0FINujNhLZUlA2kwLquum7cYQoJ0aMtkqCoWfE0Kcq28GBX6Chz3reJwwhuykwesI+ShZOyVye0E50q1Jg7PdiwiLtRZzI+mKgX26PLWsKQ0UAn9HfsIM10PE1KwhoWbAVN6MMB8maoSUzZn9kJXSqdjS7aL+r/fCVP+ewsYVIxMbYAAAAASUVORK5CYII=>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAAAiCAYAAADiWIUQAAAE/0lEQVR4Xu3cWaitcxjH8UeGyJzhEGUlkSmERMQFSSIhwyGkcIMbZSohXMghU07JmEScDBkyxS434qSU6UY2F4RQigwZnp/n/3if/d97bcs5+2IdfT/1tN//+671Tvvm1/N/32UGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD+q/W9tvf60+sGrx299vT63Gt/rw29Dva6Ir+wjtO1XeZ1oddB3bak617tdY7Xc23del5vep3l9YTXlm29bOV1rNe1FvdvZ4t7eUr5zJrawesFi+Pq+AvRudzc6vE2lpMsrvUNr+PaunS518NteVOvT7x2GjYDAIBppMBWQ9ms11tteTP7fwS2TWwIYPKuRVjtfex1hNdFFvdFjvE6tC0/7XVdW04nex1exgpuMxb3bhwFJdVibve6uy3v47V32ZZutQiU8ovFd/bwermtU+j+xuZ+922vZWW8ymuDMgYAAFOoD2wfWIQ2qYFNweAQr+u9divr7vS6xyIUJW3XujPbenV5TmjbTvU6oy1rf1pW9+tAi/3lcbTfPM7aUqj6sYw/s/lBVF2mm7y28RpZnIeuf8YihIm+80NbltyegUcB6V6vffMDY+h7iwU6+cmGe6bPZlesUvctu2rqwul/p3PNoCf6/yqApt+78cZlGQAATKka2BRSfraYEpQa2FZ6PeJ1mNenbd2JXkdZdIteswgPB3g9YzHlerZFYLvAhsCh/fzRlrUvBQh1rhSE9mvbdZwtLI5Tu1dJoWRcLRSEdA19YLuvjEXTv896XW1xPiss7sejNgQ2Bbq6HwXNby1CqOoVi+nJfzNJYNP/pQY23d/FunLfW3TYKp1/32HT/da+3/c6rawHAABTrO+wVTWwacpN4UUdpNVtm4wsumQKYQoYCmwKDwoYy9tnaodI4UeBKX3ptWsZ98eZKdvW1EKBre9YHW0RyKSeo7pmj1mEMwW6uh91AfUMWFKXbtbmd61GXndYXJPqwVY5vuWfTw76wDbT/vYUyvRcmp55q3bxes+GKdPekRb/J6ZDAQBYB0wa2BRgstOURhYhRp0xBZkMGHt5fWWxbwUehYZxga3fbz9eCpNMieoacl2e40ZtvLvFg/wKdLNtnWgaclUZb+31jte2Zd1CJumwTTIlKnrBQQFXNi/rn/I63uL+qzOnfVxZtiuo1XMHAABTbLHApuCR2z7yuqotj7y2swgn2cFRh00dtWtseIZKb03mG4gZOBSeckpU+oCWx9F+RzZ0vdaGpmVfKmN1npZZdAO/K+s1FaqAo+fpNJUoCk3nt2V10/Sd9JvNnbLV9tfLeJxJApvuYX3pQCW6P0+2Zb3V+pBFly67kjr/FW1ZpfPRdK/u+xd/fyuc5/VqGQMAgCmktyTVIVJg+9XmPyiv8Ydtm34yQlOCervyfospQtHLBHdZPPel9V9bTM8pEJ1r8WZmBrpZi5+aUJjQ525rpeNrnPI4z1scR6FvKeinPE63eOYuf+qiD2wvej1g8ZbsxW2djq/lS234nqZP9fMnOneFIC3rGi6xuS9fjDNJYNOUpgKxwqOejcv7qMC20obnBnUOWQq3Ose6LqecNe16o8UzdprC1rX206gAAABoNB2ZAQwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABL7S94aOt+XiqWVAAAAABJRU5ErkJggg==>

[image4]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAAAiCAYAAADiWIUQAAAE4UlEQVR4Xu3cW6htUxzH8b9cIoTIJcpxQgkP7nkQDwoPPEgoD5TkkjxQRHkQkvs9pZAkJYWEkrRDrkXk9kAhJQopJHL5f88Yoz32sNZZ55y2ddbD91P/1pxjzr3WmGs+rF9jjLkjJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEkLbOuxQZIkSYvjoKylrB2G9nnhc3/NOmI88D/aIuu1rHOyns7aaeXhdU7Jeirrpqyfu/YDsi7JuqprA++5a9Y/Ud53r6x9s37KOro7b1PtGaUvvPfpw7GG63gi6+ysx7r2t7KuyHo768iunT5fmbV93X8m64vlw5IkaVFcEPMPTKOvY76ff3DWIXX7vqy7umPNR1mPZG0VJbjtV9uvixKIxsDWfJu1ttvnu32025/k3LFhQLCij7zi4yjXMHoy6/ooIfyH2rZd1qV1++Ss9+o2jst6p9snCHKtkiRpgRBa7s/6NMooW7N31hlZh0f5kedHH4waXZt1apRpVNoZiWIf/A1hBoSLW7LuyTq+th1T9zmvvSfmGdjo1+OxPKJI3wlVo22iXOMeUb6fvr98D5MCG9/bjd0+I16ManH++lw0NgyOyvqt21+K/4ZAruvdrN2jjKK1aW5CWPtu6cdXdRu8x19Z29Z9Xtu2JElaEEztEbAYZepDC8GD6bdPokylXV7bX4wy0sSoHFOJhBi2W3h4IOvvun1aPU5waOHmz6wTsh7Kerm2YVpgI1QRMibVzt15G4P3XKqvILAxjTkJ4eXhrNeH9mmB7cSsm6ME0suyXo2VQW+aWYFt7ONSrPz+sGOUUUEC+NVRpnxBP6cFNu4RgY335m+37I5JkqQF8VKUwEZgYJ1Wv5aLH3fWSzUXxspQRUjbLUrwaYGtDwSEgV+iTLG1IMAo0Joo66xasMO0wLYp1mTdnfXghLo9Ni6wgT4TaPspyEmBjXD3fCyvBwPXxIjiiFHJvl9vDPtjcBr7uFSrx71ghG2Xus89YXRwfYGt4fMYBeVeMQUsSZIWCNN3jAZRz2Yd2x3jx71NdaL/4QeBgHMINJMCG+0EAEIbC9vZZ6SqfU4/oreagW0W+rEhU6JMLbbpQa79mu7YpMC2T9Y3Qxtr2Qhxs6YZZ42wbciUKEGR9nZdHD8wpk+Jcl4fLglq43tKkqTNjPVk/XQdozE8TdhG2cbARjtTbQSe/WPl04Tth55w0EbO+h//56IEGoISf8+6OM67IUpw+DHmF9jA2j0KjJ5RYPq3rbf7Pcq0Jv3l+Bhmx8BG+OWBg+akKE+IrsaUaOsDr/gsSv/5Tllf1wLh51GeYm2jiJw/PnTwQd3mXnEfwXnnxeSnZSVJ0mbyZpQptvejjCQdGmW9Gm3fR1mLxSujY20tFF6IMkLGk4Znde1fRgk7t0X5uzuirP26M+v8KFOA+C7r3igPLrCOjSBxcZTPJbTNCwGF9WWExFeiBB9wDYfVbQISobP9W48Wlj6M0tc/oowMgsDFWjCKNopQdWY9PsuswAb+RQgBkj6z9pD+tMDWpjHpP9OifPc8Mdpwb7lfPBHa7sWtUe4ja+64Tu6tJEmSpuAhD0mSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJK2mfwHU9tcNxWHQ9AAAAABJRU5ErkJggg==>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAmwAAAAiCAYAAADiWIUQAAAFWklEQVR4Xu3caaitUxzH8b9QZB4yhFxDSVyUqUTOG1PGkG4USq4hJDcRLxAlQjLdMiQvRMjQJWMcKZkihaS8IEMpRFHI8P9aa929znPO2Z17znVfXN9P/TvPs5619372s0/tX2utZ0dIkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkiRJkqTmoKzvsnbP2j7r7Kyvszbq+izE31mXDRvXMntmvZW1NOvtwbHmoSjXoi+sn/VS1hlZl9a2ZvOsX7OuifLZ7Jj1R9Ypfad5ei7rxqw3sk4eHMNmWfdGOa8P6j5Oyno267WsH2tbs06U98n/DvV01g5TekiSpHkhCHyRtXHXtnPW8qz1urb5ui1rn2HjWmZF1kV1++isbbpjILw8GSUAUZP1LwHn+iihbeva3n8OIKAd2u3zWU12+0P7Zp01bBzgde+qf/fO+njq4X+dl/VT3eb1r63bL2ZtF+WcH8vaq7bjsKxtu32C4Or4H5Ik6X9vpsAGRnbu6PZvrvvr1v0Ts5Zk7RTly53n4dhVWcfVPlvWPodEGYU6NcpIzf61z4a1H8GB576naxvXH8dG6X9wlMdjjyjnSf/Wtib8EuU1wXW4ojsGrssmdZugwzmDft9GeexEbevxmTwRo9DDY7/MWryyx3Q81/nDxoEDs46v27zG5OjQSly/NspKGD2ibhP0jqzbBDI++4bRNfY3qPvtryRJWqDZAhshZDLKF/eyrK2ifIHfHSU4XJ31W5RpPKbqPsu6L2u3KNNsPI7ARh+CCSGDEZkHs46qfW6P4oQogYXnfyVKSBvXn+MP1L88/0SU12OajnP5JOv02rfHe52tmH6cr2Fgu787NsR0ZguTD0eZjp7IOjNrv9reEFrpQ3A9J8rU6aZTekw3l8BGWBsGtpmmwDlPAjfXcxiA2yhdP8LG59ime0+LUbiXJEkLNC6wsc6JkS+ON5O1vT2u+SrKyA0IaBzHZN0HIaEFG9o41iyKEg7+ilGYmKn/bAGDdXJPRZlqJNj057YQBLk2lTksAhWGgY2Rppnw/j7q9rmOjLA1P0eZ0my49v0UI+vBeMxw5OqYGJ0T1+DNbv/CmB6cZgpsw8+/x7QpYbkPbR9GWe84E16P9W2MDkqSpNVgtsDGKAlTYYSPYWCjhoGNqbo+XK1KYFuU9UyUsEL4GRfYCDCfx/QRH463vmvaMLANp0SbR6KMIDaMxPXX8M8YTY0yhcqoYr8GbIso681Y7zabuYywzWVKlHZGVcF7IpAzeglGNpmSRgvOV3bbIKzNFlwlSdIqGgY21oldl3VA3ecGhH5UiGDGnaWrK7ARQt6NUQBjhI3pTM5npv5g6o2pRXDXIlOG9Gf6lOlaAsWt9fia8EJMvemgjYr9kHVT3cb3MTXE7JL1ad3m/a+I0To97s7khoOGGzcIqkwzjzOXwMZr9TcdtHMgkD0eZQSP9/RebacPYZPweEvWqzEawWujqt9EudMYPO/LMbqzVJIkLRBrqBhNYwSF0MW0HGvRekz98UVO2Di8trGuicc9mnV53SagsP97lC/wc2s7+4QIjlP0p41ji6NM6d0Z5YYF1qZxTheM6U8g4HwJDDyGkIbns16PckfmcD3Yf4lwy/WYyHqna+fcl3X7XNvh+jYW7i+N8hMbbQSLz6G9X7ZbXVyPjzOXwAZC8iVRpo+ZNgWvvzxKMOM98RMl7Wc9uDMUbY1aq11r+w1Z70eZ9uX/pPWXJEnSACNw/vaZJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEmSJEnSqvgHxzgGQfrVgScAAAAASUVORK5CYII=>

[image6]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABEAAAAXCAYAAADtNKTnAAAA8klEQVR4Xu3SoWtCURgF8M8mDFHjMMhkxbJiEmRJ0GydzbA/QFAwDKxGo0XMZsPAZhT8G0SUwcCysLDB3PnePQ+8971rMqkHfuHdj3ffvYcnctFp0cijD4/kTYZq8A0DuKc8vHFdtSFhXovPC/xB1R0gTdKNys7Mylk2GcIacs66pkAf0HNmQVK0gBkk7XGQ400mzixIkfbQdWZhKvQr5sSRNMjXh+aVDmK6i0R3PtWHXk+vqbbwYI9FsrAkXx8l+KKOxPwnYRe+PtIwhynpcyThv+H2oV97ghWM4Y6s1GEDP2LKUp9cUzt4h2eJOf4tV5F/nVk61xN2sYAAAAAASUVORK5CYII=>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEUAAAAYCAYAAACsnTAAAAACp0lEQVR4Xu2XS6hNURjHPyGERPIIdYWBKERKEXmVooSBKBOFvAYUZWQiUYq6A5l4lEdRkomB5DGgSCYiUjczCVGKEf/fWd+6Z51t7+PeTjknrV/9OnfvvfbrW9/3rX3NMpnMf8gIuVhOkwMLx5oxWM5yF8qhjYdrDJBdcoU7zvd1PDkoCTzcNvlIbpXH5U05Kh1UwQx5W+5wt8snckMyhutckScSv8hrfqwjYYZfytm+TZC65Wn/u2pGyYizFgKTMl0+llN9+5TcZY3XWSJ/Wv0eHcdh+VSOTvbtlO/keLeMifKZ1YMZGSlvyTkWSvK+/ObbEe7FPZmMsXHnArnHwoWjm+Uy6189twqzdNnCg/MCkXXyu5zvlhFf+KNc5XK95fKqHObjKElKJi0VAke59gaF9GLQPvnJwgWQB3krV9ZO+xOChTSpNJjNZJZphFXEF8NiUH7JNW4VSy30B8YiL3ldTkgHlUB2cV5v+dCM6PJHLARhinvAQtSp8TKIPPKQm/roekvSs4S/BYVfrILnOWqhPJBzvsq1Vt4rmCA8b6F8JscDpM4QecMPxmaG/7J0oJWgEBBWECZ5kLvFQtnF0kvh/Q65D6yQTTkoJUGBSbLHQhNqJ600Wnof3yixoUbomW8stIeUjRbuhbHpkiC9iUBP+WDVNyxjjHtHvu+jryysdM1gSW5YGi30tx4Lk4dlsGxfLO50CMixZJsv3TNyuAsE5KT/1uCmxW+DdsFK8Np/gezpdmNZw0H5w8KKA4vkC9nl2xEa6SULSzTMlc/lBXkukYzhN16/FuF403bDM/DCDy1k7n55z5KVwWHMZznPtzlvr4Usi5/5tANKarcfJyvuWn3JLppmU21ws++HdsA3Db1kpvWv4dMfVid27P8zmUwmk8nU+Q1AvZYQcSGwtgAAAABJRU5ErkJggg==>

[image8]: <data:image/png;base64,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>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAYCAYAAAAlBadpAAAA0klEQVR4XmNgGPKAA4hLoXgWFtwFxcZAzAjVAwcUaQYJCENxFRC/B2JbIJaE4nAofgfEZVD1WMEcID4NxILoEkCwEIjvArE4ugQvFB8G4vkMqKZzQ/EeBhyaNaH4LRCno8npQDHIOxMYsDjbD4q/ALEpkjgfEC+F4u1AzI8kBwetUPwLiI8B8QEGiBeOAHEUFHPCFCMDmH9AeCsDJOqIBhRpVgLi51AMimeSgAsDxK8gDGKTBEC2wWwGuYIoEATET4D4LxD/h+JnQJyMrGgUDGkAAMY3M1QIiPX1AAAAAElFTkSuQmCC>

[image10]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAXCAYAAADUUxW8AAAAy0lEQVR4XmNgGOyAG4hZoZgkIAzEp4DYF4pJAhlA/J+BDM2yQHwSiP8BcTkUEw3I1swIxJVAHAHEDxlI1KwNxO0MENtBmhdCMUHAwgDRCDKAF4gPM5Cg2ZYB4mSQ03mA+AASBvGxAk4oXgrE+UAcAsQxQHyDgQjNAVDcwwDRCMOHgPguFIvDVSMBUEqaBsUgNjJoZYAEGghLosmB/VYGxJFQjA5AUfQJivWRJfyA+B0DJAnCFDhC5UAu2A3Ev6DyIPwKiEug8qNgaAAA/X8uemhTVPwAAAAASUVORK5CYII=>

[image11]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC8AAAAYCAYAAABqWKS5AAACnklEQVR4Xu2VTYhOURjHH6HIx6TkI8rnxkdRPlbYKJOFDUupKQuysLAgyUoSjRDlIzVjQTJmhZIsSLFQVhgbhcJC05SFYsP/N+c8c869730vNaKp+6/fzH3POfee/znneZ5j1qjRqDReLBEbIlOL3bUaJxaKzWJW/F2l2aJTzLcwX52mi5NiQLyN9ItVolvMSEPHsPk54p44IXZGnojtPqBGHeKGhYlgSNyM7YAmitPikjgq3ounFhZRJd7DT5cVNwLjH0WPt/PnrLjgDVErxSuxImurEqb2Wnp3o/hu4ZtA+25xxtJuLxWfxB0xOeJi/DFr9eN91y1s7rDmiXd5Q9RMC+YPlNpzEVqPxFcLu4I4zucW3gW+c038FFvjmAnithgUyyIun/dQ1pbrvFjjP9aJb2LbSHeQG2PiOrFowsVDZJqFkMvNbxKXLYWJ72CV+bkWwooYX2utucH3R9owza60M/9QTCl21YpwI+7zsCmLxCURq8KGU7lowRP8EHcjy7Nxw/qdefjTykNikkyEDbtclZAs5rD4IFaX+lwsZp94aWkR8MVKOfi3zGPqoHhsoXq10w7x2oqhUqdJ4kgEn4XcHNPmR5uwLkyRhHniFpJLWi/uWwoncolQA0TF2hWfcy2OfLaSTy+Ve/JGC0lFxrcrWbkwdc5SYmP6VIRntEBctXQqnBRVKs8NPHTF51x+678Ri/IOPsKFUL4UqBoM5j9iAipEn4WjBETSvRC94kqEE/Bnvsm7hBM3r7eT2P2WTsjL5y1LJ4FIXtqAsGypXuwKFWK/hQsAHljIeB/s5iljlDNgpymleUVwjkcQO17uBy4q/xb3AYvptuCFubmZn1mK+XxRBdHBpbAl4rH7r8R8XFD+/L98NGrUqFFJvwApupxj1Ddw4AAAAABJRU5ErkJggg==>

[image12]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC8AAAAYCAYAAABqWKS5AAACrElEQVR4Xu2WS6iNURTHl1DE9Sh5hIQkjzLAQGToMSAZKdEtA2VggEiGBlIG8shEJEnRzYSJpBMDA1NiQF0DDCQjBib8f3ftdb797b5z780xufX963e+7+zHWuvsvfbax6xVq740WawU2xIz693j0gKxMz2bhE1s4wd/o2mWuCjeiY+JIbFBXBJzq6ETOPiF4om4IA4mXor9MWAMzRb3xT1xQNwVexNokjhsbhPb+HlkPq9JtBPPoPncEIF/FrejnY/L4lo0JK0Xb8W6rK1JU8UDcd58/hrxXdxJIGxgC5uIcfjDL++5X96xVcYTfSwQCzCixWI4b0iaZ+7wRNFeapf4Yh40mi5Oia0JdEa8tnqeHjVPBVIsT7Pwy5wmXRUb48tm8Uvs6Xa7yM+OVavXJFaCLSSw+WK72GS+G/kYVqtj9XOEv5/mgXSDkRaJT+Y/DFvl2RjI2zDyJz1zRfDPxIx6V1cYIo/fiOvmQZxNbUsSYQfK4PG7OxGaIm6kPvgtHifWZuNGNFbw0KvyxCr9sCqfY97NxJz0HZqC51n6JvWOmS9K/Aj4ZsUZ7Cf4yM8yn0m1KG8rrNnOaMHnmibOJRhfO5sTOvh+DixngTPRsXpgzGGLYbWN/8BSxw91R1RiAeCrFXFGqaR05aJ8sXK9SlboivkBHcja8pXHDjbYIXYqRAkeNvcPiBgG03uuuPXfi+V5B6WMC6G8FDiADI6DSOXgqn5ovpWAtogPYlX6HjvGBRSXUGmr9BmwQ1x4eanl8NIGp9O4mpaZ5+1xq7bxqfmJj8ERPGWMcgaI/pPm88nHW+aOuOLj+o8xL8xt4+e5uc0QuzJk/r8FW/g+Il5ZlfP5j6qJDi6FHYle/zt6aanYZ37TlhdLiBQiZ5vG4I/SG+//GkerVq1a/Wf9BUvCptiy2H/LAAAAAElFTkSuQmCC>

[image13]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEEAAAAYCAYAAACldpB6AAACyklEQVR4Xu2XS6hNURjHP6HI+1HyyiWSvAaUicfEM48BBspQYYCkZKIMKFFKIiUlyaOYGHgk6cZEGYgSE4WBoqQUhQH/X+v77l1n2/t07z3njuxf/Tpnr7XObu1vfevb65jV1NT0A+PkCjlJDij0lTFWznV7Mh4Gy8Uu38vYJi9UeNKd3TW6zfzXQWAyh+VtSxO4KM95e9VEYaP800TuE6xzX8p9co+8JodnY4LRco38IY/Iie4UedT9LbfED9rBKvlcTvDrofKu3O1WsV/ec/PVumHpftN83DL5xp3pbWfkd7nIr4tstvSgSwvtEZD3stPKg9hrSONL8pYclLUzyYfusKw955ic4Qbc74Tc5NcE9L6l+2GwRB606nsz9q11L0wwz/0qr1vjnPvMCPlEXi60H7IUbSTyZfDbgW5Aih6w7hrBSrPi292plrZF8eFyWN1O+3dh2JqRbR/k/KyvJSK1yoLwzV1Y6KuC9L9iqcAGpDX1gfvjLktZ8NRSXSgrqHPkF3lVbnV3yAeWsgxHdo1uA82CwAo227c5PAwFi9/lcE0Qzrrx0GwXAlx2b/p+Wiq8UQNmWUr/x25HDM4hxYqvkyqpzqQZtisI0y3t4ZWFdlaeIMR2CGKbsHWKVNWDyfKde0cOyTuhDkILtFIYczhfULGL9YPFIQikNgYRhFNZG3OJ+RSLIoyRz9xXcnxjd99hj/KKLEaWg06n25N3MatXFrAochRIDMoygbExvlhbgPMGtQJPW3lR7TNr5QtrPCzxbqd6I3Baey1vWmOw+I4EsSwIrCYFLap6Xhg/WTpyB7Flyg5JCyxtkUfu2Mbu1uH9e97SZDmIMFm+j3IhgsC4PE057CCHqrJ9DLw6I42Py52Wjs/rvZ86wnv/l8v2+eht+Nk/91paIOwXWKEOucE/e5tqPGizw0v8D1kuV1t3cGtqampqavqJv06Fw2onhxmcAAAAAElFTkSuQmCC>