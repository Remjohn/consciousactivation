# CLIP-CC-Bench

*Source PDF: `CLIP-CC-Bench.pdf`*

*Total Pages: 18*

---


## Page 1


CLIP-CC-Bench: Evaluating Paragraph-Level Video Descriptions
in Video–Language Models
Mukhtiar Ali∗
mukhtiar.ali@jacks.sdstate.edu
South Dakota State University
Brookings, SD, USA
Harsh Dubey∗
harsh.dubey@jacks.sdstate.edu
South Dakota State University
Brookings, SD, USA
Sugam Mishra∗
sugam.mishra@jacks.sdstate.edu
South Dakota State University
Brookings, SD, USA
Chulwoo Pack†
chulwoo.pack@sdstate.edu
South Dakota State University
Brookings, SD, USA
Abstract
Benchmarking video-language models has largely focused on short
clips and single-sentence metrics, leaving open whether current sys-
tems can generate accurate long-form, paragraph-level descriptions.
We introduce CLIP-CC-Bench, an evaluation suite for long-form
video description built from 5 hours of movie content segmented
into 90-second clips, each paired with an expert-written paragraph-
style reference. The evaluation suite employs an ensemble of five
state-of-the-art LLM-based embedding models to increase reliabil-
ity and mitigate single-model bias, and applies two complementary
methodologies: (i) coarse-grained semantic matching and (ii) fine-
grained semantic matching; to compare model-generated descrip-
tions against CLIP-CC-Bench references. Using this framework, we
evaluate 17 state-of-the-art video-language models and report both
their Borda-aggregated rankings and their average scores on CLIP-
CC-Bench. We further quantify the protocol’s internal reliability
through inter-judge agreement and bootstrap ranking stability. We
release standardized evaluation scripts, model outputs, and aggrega-
tion tools at https://github.com/Multimodal-Intelligence-Lab/CLIP-
CC-Bench to support reproducibility. CLIP-CC-Bench provides a
practical evaluation framework for long-form video description,
filling a gap left by existing short-clip and QA-only benchmarks.
CCS Concepts
• Computing methodologies →Video summarization; Natu-
ral language generation; • Information systems →Evaluation of
retrieval results; Multimedia and multimodal retrieval.
Keywords
Video Language Models, Long-Form Video Description, Evaluation
Benchmark, Embedding-Based Evaluation, Multimedia Generation
1
Introduction
The rapid advancement of Video Language Models (VLMs) has
demonstrated remarkable capabilities in understanding and describ-
ing visual content, particularly in video analysis tasks. Current state-
of-the-art models such as VideoLLaMA3 [39], InternVL [5], and
mPLUG-Owl3 [38] have achieved impressive performance across
various video understanding benchmarks. However, evaluating the
∗Equal contribution.
†Corresponding author.
quality of long-form, paragraph-level video descriptions generated
by these models remains a significant challenge, particularly when
assessing their ability to capture the overarching story and fine-
grained details.
Traditional evaluation methods for video description tasks have
predominantly relied on surface-level textual similarity metrics
such as BLEU [21], ROUGE [18], and METEOR [2]. While these met-
rics provide useful insights into lexical overlap between generated
and reference descriptions, they often fail to capture the semantic
understanding and discourse structure that are crucial for compre-
hensive video understanding. To move beyond purely local n-gram
matching, CIDEr [31] and SODA [8] have been proposed to place
greater emphasis on informative content and event structure rather
than raw lexical overlap. However, CIDEr remains fundamentally
anchored to n-gram statistics and may still underrepresent deeper
semantic and temporal coherence, while SODA relies on intermedi-
ate event representations with temporal boundaries and employs
intersection-over-union calculations between predicted and ref-
erence timestamps. This dependency limits SODA’s applicability
to realistic long-form videos where multiple actions occur within
brief temporal windows. Furthermore, SODA uses METEOR for
event description similarity, which remains constrained to n-gram
matching, and does not assess story-level comprehension across the
entire video narrative. Recent advances in evaluation methodologies
have introduced embedding-based similarity measures [13, 40] and
LLM-as-judge frameworks [19]; yet LLM-as-judge approaches are
typically black-box and exhibit significant consistency issues, with
their scores showing limited or unstable correlation with human
judgments, particularly for long-form video descriptions. Compre-
hensive benchmarks that systematically address these evaluation
challenges for long-form video description remain limited.
Current video-language benchmarks present several fundamen-
tal limitations for evaluating long-form, paragraph-level video
descriptions. Single-sentence captioning datasets like MSVD [3],
MSR-VTT [36], and VATEX [33] focus on describing isolated short
clips without requiring comprehensive multi-event understanding.
Dense captioning benchmarks such as ActivityNet Captions [12]
and YouCook2 [41] provide multi-sentence descriptions but evalu-
ate segments independently, failing to assess holistic video under-
standing. Video QA benchmarks like TVQA [14], NExT-QA [35],
and Video-MME [7] test discrete reasoning questions rather than
the ability to generate comprehensive descriptions. Furthermore,
arXiv:2608.04302v1  [cs.CV]  5 Aug 2026


## Page 2


EvalMG @SIGIR ’26, July 24, 2026, Melbourne, VIC, Australia
Ali et al.
many datasets include proper nouns and specific cultural references
that can lead to spurious correlations and may not accurately reflect
a model’s fundamental video understanding capabilities.
To address these limitations, we introduce CLIP-CC-Bench, a
comprehensive evaluation suite for long-form, paragraph-level
video description. Our benchmark comprises of 5 hours of movie
content segmented into 200 carefully selected 90-second movie clips
with expert-written paragraph descriptions that systematically ex-
clude proper nouns and cultural references, ensuring evaluation
focuses on fundamental visual understanding rather than memo-
rized associations. We make three key contributions:
Curated bias-minimizing dataset. Our clips span diverse cine-
matographic styles and temporal dynamics, providing challenging
evaluation scenarios while eliminating spurious correlations from
proper nouns and specific cultural references.
Ensemble-based evaluation framework. We employ an ensemble
of five state-of-the-art LLM-based embedding models from the
MTEB [20] leaderboard to mitigate single-model bias and enhance
evaluation reliability. Our framework applies two complementary
methodologies: coarse-grained semantic matching for holistic
paragraph-level alignment and fine-grained semantic matching for
detailed content verification. Beyond a straightforward combina-
tion of existing similarity measures, the framework is designed as
a structured multi-granular measurement protocol: the coarse–fine
decomposition separates narrative-level alignment from detail
coverage and exposes a systematic gap between the two, while
rank-based Borda aggregation cancels the scale biases of individual
embedding judges. We quantify the protocol’s internal reliability
directly—via inter-judge agreement and bootstrap stability of
the ranking (section 5.3)—and evaluate 17 state-of-the-art VLMs,
reporting Borda-aggregated rankings and average scores.
Public benchmark release. We provide all data, evaluation code,
and baseline results at https://github.com/Multimodal-Intelligence-
Lab/CLIP-CC-Bench, together with a project page and leaderboard
at https://multimodal-intelligence-lab.github.io/CLIP-CC-Bench/,
to facilitate reproducible research and continued advancement in
video understanding evaluation.
2
Related Work
2.1
Video Description Benchmarks
Single-sentence captioning datasets such as MSVD [3], MSR-
VTT [36], and VATEX [33] established foundational protocols for
video–text alignment but restrict evaluation to isolated events
in short clips. Dense captioning benchmarks extend temporal
coverage—ActivityNet Captions [12] provides temporally localized
event descriptions, while YouCook2 [41] and TACoS [24] target
procedural activities—yet they evaluate segments independently
with n-gram metrics, and even SODA [8], which improves temporal
alignment, still scores event descriptions with METEOR. Video QA
benchmarks including TVQA [14], TGIF-QA [11], NExT-QA [35],
and DramaQA [6] probe reasoning through question–answer pairs,
and long-video suites such as Video-MME [7], MVBench [16],
and LongVideoBench [34] document substantial performance
degradation as video length grows—but their multiple-choice
format tests discrete recognition rather than the ability to generate
coherent long-form descriptions. Specialized resources (Ego4D
NLQ [9], MovieGraphs [32], M-VAD Names [22]) target temporal
localization, scene graphs, or character naming rather than
description quality. Across these families, no benchmark offers
holistic assessment of paragraph-level description for minute-scale
videos—the gap CLIP-CC-Bench addresses.
2.2
Evaluation Methodologies for Video
Description
N-gram metrics. BLEU [21], ROUGE [18], METEOR [2], and
CIDEr [31] measure surface-level lexical overlap. They provide stan-
dardized, reproducible protocols, but for paragraph-length descrip-
tions they systematically miss semantically equivalent paraphrases
and capture neither discourse structure nor narrative coverage.
Embedding-based similarity. BERTScore [40] and Sentence-
BERT [23] capture semantic similarity beyond exact lexical matches,
but their short context windows (typically 512 tokens) make them
unsuitable for paragraph-level comparison. Recent LLM-based
embedding models combine deep language understanding with
context windows that accommodate full paragraphs. The MTEB
benchmark [20] ranks such models across clustering, semantic
textual similarity, classification, and retrieval tasks; current leaders
include NV-Embed-v2 [13], KaLM-Embedding-Gemma3-12B [10],
Llama-Embed-Nemotron-8B [1], Qwen3-Embedding-8B [29], and
GTE-Qwen2-7B-instruct [17]. These models excel at paragraph-
level semantic matching, though fine-grained detail sensitivity
remains challenging. EMScore [26] evaluates video captions
through coarse- and fine-grained embedding matching, but
operates cross-modally against the video and targets short captions
rather than long-form, paragraph-level descriptions.
LLM-as-judge. G-Eval [19] pioneered rubric-based LLM evalua-
tion with chain-of-thought scoring, and G-VEval [30] extends this
to video captions via GPT-4o, achieving strong correlation with
human judgments on short captions. However, these frameworks
remain largely unvalidated for long-form descriptions and inherit
black-box limitations: opaque scoring rationales and high variance
across repeated runs, which complicate systematic benchmarking.
2.3
Video Language Models
Building on early video–text pretraining (VideoBERT [28],
CBT [27]), current VLMs span diverse designs: VideoLLaMA3 [39]
emphasizes temporal modeling, InternVL [5] unifies image
and video understanding, MiniCPM-V [37] targets parameter
efficiency, mPLUG-Owl3 [38] uses multi-granular visual rep-
resentations, LongVU [25] addresses extended video contexts,
and ShareGPT4Video [4] and VideoChat [15] focus on conversa-
tional understanding. Systematic evaluation of their long-form
description capabilities, however, remains limited.
In summary, existing practice either relies on single n-gram met-
rics that miss semantic equivalence, on short-context embedding
methods unsuited to paragraphs, or on LLM judges with trans-
parency and consistency concerns. CLIP-CC-Bench instead employs
an ensemble of five long-context MTEB embedding models with
complementary coarse-grained (paragraph-level) and fine-grained


## Page 3


CLIP-CC-Bench
EvalMG @SIGIR ’26, July 24, 2026, Melbourne, VIC, Australia
(sentence-level) semantic matching, providing a transparent and
reproducible protocol for paragraph-level video description evalua-
tion.
3
Methodology
This section details the construction of CLIP-CC-Bench, a carefully
curated dataset designed to evaluate long-form, paragraph-level
video description capabilities.
3.1
Dataset Construction Principles
Our dataset construction methodology prioritizes temporal diver-
sity and visual richness while systematically eliminating potential
confounds from proper nouns and memorized associations. These
principles ensure that CLIP-CC-Bench evaluates fundamental video
understanding capabilities for long-form, paragraph-level descrip-
tion generation.
3.1.1
Temporal Scope and Content Selection. Our video content
selection emphasizes temporal and visual diversity to provide com-
prehensive evaluation of VLM capabilities across different cine-
matographic styles and narrative structures. We curate content
that differs significantly from contemporary training data patterns,
ensuring models are challenged beyond their typical training dis-
tribution through diverse visual effects techniques, color palettes,
and production methodologies.
The temporal scope of our dataset ensures sufficient distance
from recent internet content to minimize potential data contam-
ination issues. Given that most contemporary VLMs are trained
on internet-scraped data heavily biased toward recent content, our
careful curation reduces the likelihood that models have encoun-
tered similar visual patterns during training.
Our content curation process focuses exclusively on movie clips
that contain complex scenes with multiple actors, dynamic cam-
era movements, and rich visual storytelling elements. We prior-
itize clips that demonstrate temporal progression and character
interactions that require sophisticated understanding to describe
accurately.
3.1.2
Proper Noun Elimination Strategy. A fundamental design
principle of CLIP-CC-Bench is the systematic elimination of proper
nouns from all ground-truth descriptions. This design choice ad-
dresses a critical limitation in existing benchmarks, where models
may leverage memorized associations rather than demonstrating
genuine visual understanding.
Our annotation guidelines explicitly prohibit the use of:
• Character names and celebrity identifications
• Specific geographical locations and landmarks
• Brand names and commercial references
• Cultural or historical proper nouns
• Fictional universe-specific terminology
Instead, annotators employ descriptive alternatives such as “a
man in a black jacket” rather than character names, or “a luxury
sedan” instead of specific car models. This approach ensures that
evaluation focuses on fundamental visual understanding capabili-
ties rather than world knowledge retrieval.
3.2
Video Selection and Processing
We implement rigorous selection and processing protocols to en-
sure consistent quality and comprehensive coverage across our
evaluation suite. Our systematic approach balances visual complex-
ity with evaluation standardization requirements for long-form
video description assessment.
3.2.1
Content Criteria. Our video selection process employs rig-
orous criteria to ensure benchmark quality and diversity. Each
selected clip must satisfy the following requirements:
Duration Standardization. All clips are standardized to approxi-
mately 90 seconds to ensure consistent evaluation conditions while
providing sufficient content for comprehensive description.
Visual Complexity. Selected scenes must contain multiple visual
elements including character interactions, environmental details,
and temporal dynamics that require sophisticated understanding
to describe accurately.
Self-Contained Content. Clips must represent self-contained seg-
ments that can be understood without external context, ensuring
fair evaluation across different models.
Technical Quality. All video content maintains consistent resolu-
tion and audio quality standards to prevent technical artifacts from
influencing model performance.
3.3
Annotation Procedure
Annotators. The reference descriptions were written by four
graduate-student annotators fluent in English, all trained on the
proper-noun-exclusion guidelines above before annotating.
Procedure. Each clip was assigned to a single annotator, who
watched the ∼90 s segment and narrated its description aloud in
real time while deliberately avoiding proper nouns and other mem-
orizable references. Each narration was transcribed by automatic
speech recognition and then manually verified against the audio,
and finally passed through a grammar-only GPT-4o cleanup that
fixed disfluencies and grammar without adding, removing, or re-
ordering content or introducing names (the cleanup prompt is given
in section E). Annotation took roughly 45 minutes per clip (∼30 min
narration, ∼15 min review), or about 150 hours in total.
3.4
Dataset Statistics and Characteristics
The final CLIP-CC-Bench dataset comprises 5 hours of movie con-
tent broken down into 90-second clips with corresponding expert-
generated descriptions. Key statistics are presented in table 1.
Figure 2 illustrates the distribution of description lengths across
our dataset, demonstrating the substantial variation in complexity
that reflects the diverse nature of video content. The bimodal dis-
tribution in word counts reveals two primary description patterns:
concise summaries for simpler scenes (100-300 words) and compre-
hensive narratives for complex sequences (400-800 words). This
natural variation ensures that CLIP-CC-Bench evaluates models
across a spectrum of descriptive requirements, from brief action
sequences to intricate multi-character interactions.
Source and Topical Diversity. The 200 clips are drawn from more
than 140 distinct films and series spanning 1959–2024 (median


## Page 4


EvalMG @SIGIR ’26, July 24, 2026, Melbourne, VIC, Australia
Ali et al.
Y
Source video
Movieclips
ô
Curate clips
∼90 s clips
?
Live narration
no proper nouns
#
GPT-4o cleanup
grammar only
õ
CLIP-CC-Dataset
200 clips · 5 h
> 17 VLMs
g1
g2
g3
gn
pn
p3
p2
p1
· · ·
· · ·
· · ·
0.79
0.30
0.39
0.75
· · ·
0.47
0.78
0.33
· · ·
0.81
0.35
0.29
· · ·
1
0
sim
A · [
paragraph-level
cosine similarity
+
Fine-Grained Semantic Matching
Coarse-Grained Semantic Matching
Judge j (1 of 5 judges)
A VLM output P
“The video begins with a
person with long brown
hair sitting in a salon chair,
wearing a black salon cape.
Another person with red and
black hair is seen styling the
first person’s hair. The scene
transitions to a close-up of a
shelf displaying various hair
care products labeled ‘lott’...”
[ Reference G
“The video begins with a
woman seated under a hair
treatment device, while a
hair stylist stands beside her.
The stylist, who has a tattoo
on her arm and is wearing
a blue top, is next to the
woman in the chair, who is
dressed in a black gown...”
HM-CFj
 VLM leaderboard
Borda count aggregation over 5 judges
Figure 1: Overview of CLIP-CC-Bench. Top: dataset construction curates ∼90 s movie clips, collects live narration without
proper nouns, applies a grammar-only GPT-4o cleanup, and yields the CLIP-CC-Dataset (200 clip–paragraph pairs, 5 h total).
Bottom: per-judge evaluation. A candidate paragraph 𝑃from one of 17 VLMs (left; sample shown is mPLUG-Owl3 on clip 092)
and the reference paragraph 𝐺from the dataset (right) are scored by Judge 𝑗, one of five MTEB embedding judges. The judge
combines an 𝑛×𝑛sentence-level cosine matrix (Fine-Grained Semantic Matching; greedy diagonal best-matches outlined in red)
with the paragraph-level cosine (Coarse-Grained Semantic Matching) into a harmonic-mean HM-CF𝑗. Borda aggregation across
the five judges produces the leaderboard over the 17 VLMs.
release year 2009): 110 sources contribute exactly one clip, and
no single source contributes more than six clips (3%). Categoriz-
ing clips by primary narrative type yields four categories with at
least 5% representation—Dialogue/Drama (52%), Violence/Combat
(13%), Action/Chase (11.5%), and Public/Social (11.5%)—with the
remainder spanning medical/procedural, dramatic-confrontation,
crime, domestic, suspense, and romance scenes (full distribution
in table 10). Unsupervised clustering of CLIP video embeddings
corroborates this spread independently of the category labels: the
largest visual cluster contains only 17% of clips, and seven clusters
each hold at least 5%. The dialogue-heavy distribution is expected
for narrative film content, while the remaining 48% of clips provide
dense action, multi-character, and procedural challenges.
Our ground-truth descriptions exhibit several distinctive charac-
teristics that differentiate CLIP-CC-Bench from existing datasets:
Comprehensive Detail. Descriptions provide thorough coverage
of visual content with substantial variation in length to accommo-
date different scene complexities.
Temporal Structure. Descriptions follow chronological progres-
sion through the video content, explicitly tracking temporal rela-
tionships between events and character actions.
Visual Specificity. Detailed descriptions of visual elements includ-
ing clothing, environmental features, object properties, and spatial
relationships provide rich evaluation targets for VLM assessment.


## Page 5


CLIP-CC-Bench
EvalMG @SIGIR ’26, July 24, 2026, Melbourne, VIC, Australia
Table 1: CLIP-CC-Bench dataset statistics.
Metric
Value
Number of videos
200
Clip duration
∼90 seconds
Total video content
5 hours
Distinct source films/series
>140
Source release years
1959–2024
Words per description (mean ± std)
402.2 ± 208.5
Words per description [min, max]
[99, 1011]
Sentences per description (mean ± std)
21.9 ± 11.5
Vocabulary size (unique words)
4,000
0
200
400
600
800
1000
Description Length (words)
0.0000
0.0005
0.0010
0.0015
0.0020
0.0025
0.0030
0.0035
Density
(a) Description Length Distribution
Distribution
Kernel Density
Mean: 402
Median: 349
Figure 2: Distribution of description characteristics in CLIP-
CC-Bench. The dataset exhibits substantial variation in both
word count and sentence length, reflecting the diverse com-
plexity of video content while maintaining comprehensive
paragraph-level descriptions suitable for evaluating long-
form video understanding capabilities.
Action Coverage. Both foreground actions (primary character
activities) and background elements (environmental details, sec-
ondary characters) are systematically documented to enable com-
prehensive evaluation.
This composition ensures representative coverage of diverse cin-
ematic styles while maintaining evaluation consistency and quality
standards for long-form description assessment.
4
Experiments
We evaluate 17 state-of-the-art Video Language Models on CLIP-
CC-Bench using our ensemble-based multi-granular evaluation
framework to analyze their long-form video description capabilities.
4.1
Model Selection and Inference
We evaluate 17 representative VLMs spanning different architec-
tural paradigms and training methodologies, as summarized in
Table 2: Video Language Models evaluated on CLIP-CC-
Bench.
Model
Architecture Family
Parameters
Max Frames
LLaVA-OneVision
Transformer
7B
8
LLaVA-NeXT-Video
Transformer
7B
32
VideoLLaMA3
Transformer
7B
32
InternVL2
Transformer
8B
12
Qwen2.5
Transformer
32B
–
Qwen2.5
Transformer
72B
–
LongVU
Efficient
7B
–
LongVA
Efficient
7B
128
MiniCPM-V
Efficient
8B
32
Video-XL
Specialized
7B
16
TimeChat
Specialized
7B
16
TS-LLaVA
Specialized
7B
32
VideoChat-Flash
Specialized
2B
16
Oryx
Multimodal
7B
–
ViLAMP
Multimodal
7B
600
mPLUG-Owl3
Multimodal
7B
16
ShareGPT4Video
Multimodal
8B
–
table 2. To ensure comprehensive evaluation of each model’s ca-
pabilities, we utilize their maximum supported frame capacity, al-
lowing each VLM to process videos at its full potential rather than
imposing artificial constraints.
All models generate paragraph-length descriptions for each
video clip using standardized inference parameters while operating
at their maximum frame processing capacity.1
4.2
Evaluation Protocol
We standardize evaluation with: (1) uniform prompting: “Provide
a detailed description of the video, covering all significant events,
the actions of each character or entity, any camera movements, the
attributes of the characters or entities, and a description of the scene,
focusing on the characters themselves without recognizing, identifying,
or naming them, and only describing their appearance, behavior, and
actions.”, (2) consistent generation parameters (temperature=0.0,
max_tokens=5000), and (3) deterministic inference with greedy
decoding to ensure reproducible and consistent outputs.
4.3
Evaluation Methodologies
We employ a multi-granular semantic matching framework that
evaluates VLM-generated descriptions through both holistic
and sentence-level alignment with reference descriptions. This
approach combines embedding-based similarity at multiple scales
with a multi-judge consensus mechanism to ensure robust and
comprehensive performance assessment.
Notation. Let 𝐺= {𝑔1, . . . ,𝑔𝑚} denote a reference paragraph
from CLIP-CC-Bench with𝑚sentences and 𝑃= {𝑝1, . . . , 𝑝𝑛} denote
a candidate paragraph generated by a VLM with 𝑛sentences. We
treat the five MTEB embedding models as independent judges 𝑗∈
{1, . . . , 𝐽} with 𝐽=5, where each judge 𝑗realizes an encoder 𝑓𝑗(·)
1Model outputs are unavailable for one clip (#126) across all 17 VLMs; all reported
metrics are therefore computed over the identical remaining 199 clips, keeping com-
parisons strictly paired.


## Page 6


EvalMG @SIGIR ’26, July 24, 2026, Melbourne, VIC, Australia
Ali et al.
that maps a sentence or a whole paragraph to a dense vector. Cosine
similarity between two vectors 𝑢, 𝑣is cos(𝑢, 𝑣) =
𝑢·𝑣
∥𝑢∥∥𝑣∥.
4.3.1
Coarse-Grained Semantic Matching. We encode the complete
reference and predicted paragraphs as single dense vector repre-
sentations and measure their cosine similarity, capturing overall
semantic coherence between the generated description and the
reference:
Coarse𝑗(𝐺, 𝑃) = cos 𝑓𝑗(𝐺), 𝑓𝑗(𝑃).
(1)
4.3.2
Fine-Grained Semantic Matching. After sentence-level tok-
enization, we embed each sentence individually and form an 𝑛×𝑚
cosine matrix between predicted and reference sentences. Fine-
grained precision averages, over predicted sentences, the cosine to
their best-matching reference sentence; recall averages the sym-
metric quantity from the reference side:
Pr𝑗(𝐺, 𝑃) = 1
𝑛
𝑛
∑︁
𝑖=1
max
1≤𝑘≤𝑚cos 𝑓𝑗(𝑝𝑖), 𝑓𝑗(𝑔𝑘),
(2)
Rc𝑗(𝐺, 𝑃) = 1
𝑚
𝑚
∑︁
𝑘=1
max
1≤𝑖≤𝑛cos 𝑓𝑗(𝑔𝑘), 𝑓𝑗(𝑝𝑖).
(3)
The sentence-level F1 harmonically combines the two, balancing
semantic precision and coverage:
Fine𝑗(𝐺, 𝑃) = 2 · Pr𝑗(𝐺, 𝑃) · Rc𝑗(𝐺, 𝑃)
Pr𝑗(𝐺, 𝑃) + Rc𝑗(𝐺, 𝑃) .
(4)
4.3.3
Multi-Judge Consensus Ranking. For each judge 𝑗, we sum-
marize a (𝐺, 𝑃) pair with the harmonic mean of its coarse and fine
scores, producing a per-judge metric that penalizes models that
excel in only one granularity:
HM-CF𝑗(𝐺, 𝑃) = 2 · Coarse𝑗(𝐺, 𝑃) · Fine𝑗(𝐺, 𝑃)
Coarse𝑗(𝐺, 𝑃) + Fine𝑗(𝐺, 𝑃) .
(5)
Each judge then ranks the 𝑉=17 VLMs by their dataset-averaged
HM-CF𝑗. Letting rank𝑗(𝑣) ∈{1, . . . ,𝑉} denote the rank of VLM 𝑣
under judge 𝑗, the final consensus is obtained via Borda count:
Borda(𝑣) =
𝐽∑︁
𝑗=1
 𝑉−rank𝑗(𝑣),
(6)
which assigns 𝑉−1=16 points to a first place and 0 points to a last
place under each judge, yielding a maximum attainable Borda score
of 𝐽(𝑉−1) = 80. This aggregation mitigates idiosyncratic biases of
any single judge and provides a robust overall VLM ranking.
5
Results
We present comprehensive evaluation results for 17 state-of-the-art
Video Language Models on CLIP-CC-Bench using our ensemble-
based evaluation framework. Our methodology employs five lead-
ing LLM-based embedding models from the MTEB [20] leader-
board: GTE-Qwen2-7B [17], KaLM-Embedding-Gemma3-12B [10],
Llama-Embed-Nemotron-8B [1], nv-embed-v2 [13], and Qwen3-
Embedding-8B [29]. For each VLM, we compute coarse-grained
semantic similarity (paragraph-level alignment) and fine-grained
semantic similarity (sentence-level F1 matching) across all five em-
bedding models. We then rank VLMs using Borda count based on
their harmonic mean of coarse and fine scores (HM-CF, see Eq. 5) for
each embedding model, and report mean HM-CF scores averaged
across all five judges.
5.1
Per-Judge Evaluation Statistics
Table 3 presents detailed performance statistics for all 17 VLMs
across the five embedding models. For each embedding model,
we report coarse-grained similarity scores, fine-grained F1 scores,
and their harmonic mean, along with standard deviations. The
hierarchical structure reveals how different embedding models
assess video description quality with varying sensitivities.
Across all embedding models, VideoLLaMA3 consistently
achieves the highest scores, with KaLM-Gemma3-12B showing
particularly strong discrimination (HM-CF: 0.79). The standard
deviations reveal model-specific variance patterns: NV-Embed-
v2 exhibits the highest variability in coarse-grained scores
(VideoLLaMA3: 0.10, mPLUG-Owl3: 0.13), while Llama-Embed-
Nemotron-8B shows more conservative absolute scores but tighter
distributions. This diversity across embedding models motivates
our ensemble approach to reduce single-model bias.
5.2
Overall VLM Ranking
Table 4 presents our final VLM ranking computed using Borda count
aggregation across all five embedding models. For each embedding
model, we rank VLMs by their HM-CF score and assign Borda
points (16 points for rank 1, 15 for rank 2, down to 0 for rank 17).
The final ranking is determined by total Borda score, with Mean
(average HM-CF across all five embedding models) serving as a
tiebreaker.
VideoLLaMA3 achieves the highest Borda score (80 out of
maximum 80), demonstrating consistent top performance across
all five embedding judges with a mean score of 0.67. mPLUG-Owl3
follows closely (Borda: 75, Mean: 0.66), while LLaVA-OneVision
and ViLAMP tie in Borda score (67); the full-precision mean
HM-CF tiebreaker (0.640 vs. 0.638) places LLaVA-OneVision
third. VideoChat-Flash and MiniCPM-V (ranks 8–9) likewise tie
on Borda (42), separated only by a negligible margin in mean
HM-CF (table 7). The Qwen2.5 models (72B and 32B) demonstrate
strong upper-middle tier performance (ranks 6-7), indicating
general-purpose LLMs with visual capabilities can achieve
competitive results on long-form video description when properly
scaled.
5.3
Internal Reliability of the Evaluation
Protocol
We probe the internal reliability of the proposed protocol along two
axes: agreement among the five judges and stability of the ranking
under dataset resampling.
Inter-Judge Agreement. Although the five judges differ markedly
in absolute scoring scales (table 3; NV-Embed-v2 is the most conser-
vative, KaLM-Gemma3-12B the most liberal), they agree strongly
on relative model quality. At the system level, the ten pairwise rank
correlations across the 17 VLMs range from Spearman 𝜌= 0.96
to 0.99 (mean 0.98; Kendall 𝜏mean 0.92, range 0.87–0.97). At the
instance level—correlating per-clip HM-CF scores over all 3,383
(model, clip) pairs—the mean pairwise Pearson correlation is 0.90


## Page 7


CLIP-CC-Bench
EvalMG @SIGIR ’26, July 24, 2026, Melbourne, VIC, Australia
Table 3: Detailed evaluation statistics across five MTEB embedding models. For each model, we report Coarse (coarse-grained
similarity, Eq. 1), Fine (fine-grained F1, Eq. 4), and HM-CF (harmonic mean of Coarse and Fine, Eq. 5) as mean±std.
GTE-Qwen2-7B
KaLM-Gemma3-12B
Nemo-8B
NV-Embed-v2
Qwen3-8B
VLM
Coarse
Fine
HM-CF
Coarse
Fine
HM-CF
Coarse
Fine
HM-CF
Coarse
Fine
HM-CF
Coarse
Fine
HM-CF
VideoLLaMA3
0.75±0.05
0.64±0.04
0.69±0.04
0.82±0.05
0.76±0.03
0.79±0.03
0.68±0.07
0.57±0.04
0.62±0.05
0.68±0.10
0.47±0.07
0.55±0.08
0.72±0.06
0.69±0.03
0.70±0.04
mPLUG-Owl3
0.74±0.06
0.64±0.04
0.68±0.04
0.79±0.07
0.75±0.03
0.77±0.05
0.67±0.08
0.55±0.04
0.61±0.05
0.63±0.13
0.46±0.06
0.53±0.08
0.70±0.07
0.68±0.04
0.69±0.05
ViLAMP
0.71±0.07
0.62±0.05
0.66±0.05
0.78±0.07
0.75±0.03
0.76±0.04
0.65±0.08
0.55±0.05
0.59±0.06
0.60±0.14
0.44±0.06
0.50±0.08
0.69±0.07
0.66±0.04
0.68±0.05
LLaVA-OneVision
0.70±0.06
0.62±0.04
0.65±0.04
0.79±0.05
0.74±0.03
0.76±0.04
0.65±0.07
0.54±0.05
0.59±0.05
0.64±0.07
0.44±0.06
0.52±0.06
0.68±0.07
0.67±0.04
0.67±0.05
LongVU
0.70±0.06
0.60±0.05
0.64±0.05
0.78±0.06
0.73±0.03
0.75±0.04
0.63±0.08
0.51±0.05
0.56±0.06
0.61±0.10
0.44±0.06
0.51±0.07
0.67±0.07
0.67±0.03
0.67±0.05
Qwen2.5-72B
0.66±0.07
0.59±0.04
0.63±0.05
0.77±0.06
0.72±0.03
0.75±0.04
0.63±0.08
0.50±0.05
0.56±0.06
0.59±0.09
0.43±0.06
0.50±0.06
0.68±0.07
0.65±0.04
0.66±0.05
Qwen2.5-32B
0.66±0.06
0.57±0.04
0.61±0.04
0.77±0.05
0.72±0.03
0.74±0.03
0.60±0.07
0.49±0.04
0.54±0.05
0.58±0.08
0.42±0.05
0.49±0.06
0.66±0.06
0.65±0.03
0.65±0.04
VideoChat-Flash
0.63±0.07
0.59±0.04
0.61±0.05
0.74±0.06
0.72±0.03
0.73±0.04
0.59±0.09
0.52±0.05
0.55±0.06
0.54±0.11
0.40±0.06
0.45±0.08
0.67±0.06
0.64±0.04
0.66±0.05
MiniCPM-V
0.67±0.06
0.55±0.04
0.60±0.04
0.78±0.05
0.70±0.03
0.74±0.03
0.61±0.07
0.47±0.04
0.53±0.05
0.60±0.07
0.40±0.05
0.48±0.06
0.66±0.06
0.64±0.03
0.65±0.04
Video-XL
0.63±0.08
0.57±0.05
0.60±0.06
0.74±0.06
0.72±0.03
0.73±0.04
0.56±0.09
0.49±0.04
0.52±0.06
0.55±0.09
0.40±0.06
0.47±0.06
0.62±0.08
0.65±0.04
0.63±0.05
ShareGPT4Video
0.64±0.07
0.57±0.05
0.60±0.05
0.72±0.07
0.70±0.03
0.71±0.05
0.55±0.08
0.48±0.05
0.51±0.06
0.55±0.11
0.40±0.06
0.46±0.08
0.61±0.07
0.64±0.04
0.62±0.05
InternVL2
0.63±0.09
0.56±0.06
0.60±0.08
0.74±0.07
0.71±0.04
0.72±0.05
0.56±0.10
0.49±0.05
0.52±0.07
0.57±0.10
0.38±0.06
0.45±0.07
0.61±0.08
0.63±0.05
0.62±0.06
TimeChat
0.58±0.07
0.55±0.04
0.57±0.05
0.72±0.06
0.71±0.03
0.71±0.04
0.52±0.08
0.49±0.05
0.50±0.06
0.53±0.09
0.35±0.06
0.42±0.07
0.59±0.07
0.62±0.04
0.60±0.05
LLaVA-NeXT-Video
0.55±0.09
0.53±0.05
0.54±0.06
0.69±0.07
0.71±0.03
0.70±0.05
0.49±0.10
0.48±0.05
0.48±0.07
0.50±0.10
0.37±0.07
0.42±0.08
0.56±0.09
0.63±0.04
0.59±0.06
TS-LLaVA
0.54±0.10
0.51±0.06
0.53±0.07
0.68±0.08
0.69±0.04
0.68±0.06
0.46±0.11
0.46±0.06
0.46±0.08
0.47±0.11
0.35±0.07
0.40±0.08
0.56±0.09
0.62±0.05
0.58±0.07
Oryx
0.52±0.10
0.51±0.05
0.51±0.07
0.67±0.07
0.68±0.04
0.67±0.05
0.47±0.10
0.45±0.05
0.46±0.07
0.48±0.10
0.34±0.07
0.40±0.08
0.56±0.09
0.61±0.05
0.58±0.07
LongVA
0.50±0.10
0.46±0.07
0.48±0.08
0.62±0.08
0.66±0.04
0.64±0.06
0.41±0.10
0.41±0.06
0.40±0.07
0.40±0.10
0.31±0.07
0.35±0.08
0.49±0.10
0.57±0.05
0.53±0.08
Table 4: Overall VLM ranking on CLIP-CC-Bench using Borda
count aggregation (Eq. 6) across five MTEB embedding mod-
els. Borda scores represent cumulative ranking points across
all judges. Mean is the average HM-CF across all five embed-
ding models.
Rank
VLM
Borda
Mean
1
VideoLLaMA3
80
0.67
2
mPLUG-Owl3
75
0.66
3
LLaVA-OneVision
67
0.64
4
ViLAMP
67
0.64
5
LongVU
61
0.63
6
Qwen2.5-72B
55
0.62
7
Qwen2.5-32B
48
0.61
8
VideoChat-Flash
42
0.60
9
MiniCPM-V
42
0.60
10
Video-XL
36
0.59
11
ShareGPT4Video
29
0.58
12
InternVL2
27
0.58
13
TimeChat
20
0.56
14
LLaVA-NeXT-Video
16
0.55
15
TS-LLaVA
9
0.53
16
Oryx
6
0.52
17
LongVA
0
0.48
(range 0.85–0.94). Tables 5 and 6 report the full pairwise matrices.
The judges thus carry different scale biases but consistent ordinal
behavior: rank-based Borda aggregation cancels the former while
preserving the latter, so the leaderboard is not an artifact of any
single judge choice, and the ensemble guards against the residual
single-judge deviations that do occur at the instance level.
Ranking Stability and Dataset Size. To test whether the
benchmark’s size supports a stable system-level ranking, we
resample clips with replacement (𝐵=1,000) and recompute the
entire pipeline—per-judge means, per-judge ranks, and Borda
Table 5: System-level inter-judge agreement over the 17 VLM
mean HM-CF scores: Spearman 𝜌(upper triangle) and Kendall
𝜏(lower triangle).
KaLM
GTE
NV
NeMo
Qwen3
KaLM
—
0.973
0.978
0.978
0.975
GTE
0.912
—
0.973
0.988
0.995
NV
0.926
0.897
—
0.958
0.966
NeMo
0.912
0.941
0.868
—
0.995
Qwen3
0.912
0.971
0.897
0.971
—
Table 6: Instance-level inter-judge agreement: Pearson cor-
relation of per-clip HM-CF scores over all 3,383 (model, clip)
pairs.
GTE
NV
NeMo
Qwen3
KaLM
0.898
0.899
0.937
0.897
GTE
—
0.847
0.933
0.918
NV
—
0.881
0.851
NeMo
—
0.925
aggregation—on each replicate. Resampled rankings agree with
the original at a mean Kendall 𝜏of 0.98 (95% CI [0.96, 1.00]); the
top-ranked model is preserved in 100% of replicates; and every
model’s 95% bootstrap rank interval lies within one position of
its reported rank, except InternVL2 (within two). Table 7 reports
the per-model bootstrap rank intervals. The reported ranking is
therefore statistically stable at the current dataset size.
5.4
Analysis and Key Findings
Our ensemble-based evaluation framework reveals critical insights
about long-form video description capabilities:
Consistent Top Performers. VideoLLaMA3’s perfect Borda score
(80/80) indicates unanimous first-place agreement across all five
embedding judges, demonstrating robust long-form description


## Page 8


EvalMG @SIGIR ’26, July 24, 2026, Melbourne, VIC, Australia
Ali et al.
Table 7: Bootstrap distribution of final ranks (𝐵=1,000 clip
resamples). All intervals lie within one position of the re-
ported rank, except InternVL2 (within two).
Rank
VLM
Median
95% interval
1
VideoLLaMA3
1
[1, 1]
2
mPLUG-Owl3
2
[2, 2]
3
LLaVA-OneVision
3
[3, 4]
4
ViLAMP
4
[3, 4]
5
LongVU
5
[5, 6]
6
Qwen2.5-72B
6
[5, 6]
7
Qwen2.5-32B
7
[7, 7]
8
VideoChat-Flash
8
[8, 9]
9
MiniCPM-V
9
[8, 9]
10
Video-XL
10
[10, 11]
11
ShareGPT4Video
11
[11, 12]
12
InternVL2
12
[10, 12]
13
TimeChat
13
[13, 13]
14
LLaVA-NeXT-Video
14
[14, 14]
15
TS-LLaVA
15
[15, 16]
16
Oryx
16
[15, 16]
17
LongVA
17
[17, 17]
capabilities that generalize across different semantic similarity met-
rics.
Embedding Model Diversity. While embedding models produce
correlated rankings, they exhibit different absolute score ranges
and sensitivities. KaLM-Gemma3-12B produces the highest HM-CF
scores (VideoLLaMA3: 0.79), while NV-Embed-v2 shows conserva-
tive scoring (VideoLLaMA3: 0.55) but highest variance, justifying
our ensemble approach.
Fine-Grained vs Coarse-Grained Gap. Coarse-grained scores con-
sistently exceed fine-grained scores across all models, indicating
VLMs capture overall semantic meaning better than fine-grained
details. VideoLLaMA3 achieves 0.82 coarse vs 0.76 fine on KaLM-
Gemma3-12B. This gap is most pronounced in NV-Embed-v2 (0.68
coarse vs 0.47 fine), indicating detailed content matching remains
challenging.
Architecture Family Performance. Transformer-based models
dominate the top tier, with VideoLLaMA3 (rank 1), mPLUG-Owl3
(rank 2), and LLaVA-OneVision (rank 3) achieving Borda scores
≥67. Multimodal family models show competitive performance
(ViLAMP at rank 4, ShareGPT4Video at rank 11). Efficient
architectures demonstrate moderate performance (LongVU at
rank 5, MiniCPM-V at rank 9), while specialized temporal models
underperform (TimeChat, TS-LLaVA, Video-XL at ranks 10-15),
suggesting temporal modeling alone is insufficient for long-form
description without strong semantic understanding.
Performance Stratification. Clear performance tiers emerge: top-
tier models (Borda ≥60) achieve mean scores above 0.63, mid-tier
models (30 ≤Borda < 60) range from 0.58-0.62, and lower-tier
models (Borda < 30) fall below 0.58, suggesting distinct capability
levels rather than continuous performance.
Substantial Improvement Headroom. Even top-performing Vide-
oLLaMA3 achieves only 0.67 mean score, with individual fine-
grained scores as low as 0.47 on NV-Embed-v2. The substantial
gap between top and bottom performers (0.67 vs 0.48) combined
with modest absolute scores indicates significant advancement po-
tential in long-form video description.
6
Limitations
CLIP-CC-Bench’s dataset of 200 expert-annotated movie clips—
roughly five hours of ∼90-second segments drawn from more than
140 films spanning 1959–2024—provides a focused but bounded eval-
uation. The narrative-film domain excludes instructional, surveil-
lance, and user-generated video, so model behavior in those set-
tings remains untested. Our English-only scope and the deliberate
removal of proper nouns, a design choice that isolates visual under-
standing from memorized associations, yield controlled but domain-
specific conditions, and each clip is paired with a single reference
description that cannot capture every valid way of describing a
complex scene.
Methodologically, our ensemble scores descriptions through com-
plementary coarse- and fine-grained semantic matching, which we
show to be internally reliable across the five embedding judges
and stable under dataset resampling, with the top-ranked model
preserved across all bootstrap replicates (section 5.3). Because this
matching emphasizes semantic content, it does not explicitly model
the temporal or causal ordering of events, so extending the protocol
to reward correct event sequencing is a natural direction for future
metrics. Likewise, while exhaustive human scoring is impractical
for descriptions of this length, a targeted sample-based human
meta-evaluation would help confirm the external validity of the
automated scores and remains valuable future work.
More broadly, natural extensions include expanding the dataset’s
scale and domain coverage, adding multiple reference descriptions
per clip, and supporting cross-linguistic evaluation. None of these
constraints undercut the benchmark’s central contribution: a rig-
orous, reproducible ensemble methodology for long-form video
description that produces statistically stable VLM rankings and
surfaces actionable insights—most notably the strong showing of
transformer architecture families and the consistent coarse–fine
granularity gap.
7
Conclusion
We introduce CLIP-CC-Bench, an evaluation suite for long-form
video description using an ensemble of five MTEB embedding mod-
els with Borda count aggregation. Evaluation of 17 VLMs reveals
transformer architectures dominate (VideoLLaMA3 achieves per-
fect 80/80 Borda consensus), while specialized temporal models un-
derperform, indicating temporal modeling alone is insufficient. The
consistent coarse-fine granularity gap shows VLMs capture overall
semantics better than precise details, with substantial improvement
headroom (top model: 0.67 mean). All evaluation resources are
publicly available.
Acknowledgments
We thank Nikhil Chaudhary and Esrom Tesfabrham Ghebreweldi
for their help with dataset annotation.


## Page 9


CLIP-CC-Bench
EvalMG @SIGIR ’26, July 24, 2026, Melbourne, VIC, Australia
References
[1] Yauhen Babakhin, Radek Osmulski, Ronay Ak, Gabriel Moreira, Mengyao Xu,
Benedikt Schifferer, Bo Liu, and Even Oldridge. 2025. Llama-Embed-Nemotron-
8B: A Universal Text Embedding Model for Multilingual and Cross-Lingual Tasks.
arXiv:2511.07025 [cs.CL]
[2] Satanjeev Banerjee and Alon Lavie. 2005. METEOR: An Automatic Metric for MT
Evaluation with Improved Correlation with Human Judgments. In Proceedings
of the ACL Workshop on Intrinsic and Extrinsic Evaluation Measures for Machine
Translation and/or Summarization.
[3] David L. Chen and William B. Dolan. 2011. Collecting Highly Parallel Data for
Paraphrase Evaluation. In Proceedings of the 49th Annual Meeting of the Association
for Computational Linguistics.
[4] Lin Chen, Xilin Wei, Jinsong Li, Xiaoyi Dong, Pan Zhang, Yuhang Zang, Zehui
Chen, Haodong Duan, Bin Lin, Zhenyu Tang, Li Yuan, Yu Qiao, Dahua Lin, Feng
Zhao, and Jiaqi Wang. 2024. ShareGPT4Video: Improving Video Understanding
and Generation with Better Captions. In NeurIPS.
[5] Zhe Chen, Jiannan Wu, Wenhai Wang, Weijie Su, Guo Chen, Sen Xing, Muyan
Zhong, Qinglong Zhang, Xizhou Zhu, Lewei Lu, Bin Li, Ping Luo, Tong Lu, Yu
Qiao, and Jifeng Dai. 2024. InternVL: Scaling up Vision Foundation Models and
Aligning for Generic Visual-Linguistic Tasks. In CVPR.
[6] Kyung-Min Choi, Jihyun Kang, Minseok Kim, and Hyunwoo J. Kim. 2021. Dra-
maQA: Character-Centered Video Story Understanding with Hierarchical QA. In
AAAI.
[7] Chaoyou Fu, Yuhan Dai, Yongdong Luo, Lei Li, Shuhuai Ren, Renrui Zhang,
Zihan Wang, Chenyu Zhou, Yunhang Shen, Mengdan Zhang, Peixian Chen,
Yanwei Li, Shaohui Lin, Sirui Zhao, Ke Li, Tong Xu, Xiawu Zheng, Enhong Chen,
Rongrong Ji, and Xing Sun. 2024. Video-MME: The First-Ever Comprehensive
Evaluation Benchmark of Multi-modal LLMs in Video Analysis. arXiv preprint
arXiv:2405.21075.
[8] Soichiro Fujita, Tsutomu Hirao, Hidetaka Kamigaito, Manabu Okumura, and
Masaaki Nagata. 2020. SODA: Story Oriented Dense Video Captioning Evaluation
Framework. In ECCV.
[9] Kristen Grauman, Andrew Westbury, Eugene Byrnes, Zachary Chavis, Antonino
Furnari, Rohit Girdhar, Jackson Hamburger, Hao Jiang, Miao Liu, Xingyu Liu,
Miguel Martin, Tushar Nagarajan, Ilija Radosavovic, Santhosh Kumar Ramakrish-
nan, Fiona Ryan, Jayant Sharma, Michael Wray, Mengmeng Xu, Eric Zhongcong
Xu, Chen Zhao, Siddhant Bansal, Dhruv Batra, Vincent Cartillier, Sean Crane,
Tien Do, Morrie Doulaty, Akshay Erapalli, Christoph Feichtenhofer, Adriano
Fragomeni, Qichen Fu, Christian Fuegen, Abrham Gebreselasie, Cristina Gonzalez,
James Hillis, Xuhua Huang, Yifei Huang, Wenqi Jia, Weslie Khoo, Jachym Kolar,
Satwik Kottur, Anurag Kumar, Federico Landini, Chao Li, Yanghao Li, Zhenqiang
Li, Karttikeya Mangalam, Raghava Modhugu, Jonathan Munro, Tullie Murrell,
Takumi Nishiyasu, Will Price, Paola Ruiz Puentes, Merey Ramazanova, Leda Sari,
Kiran Somasundaram, Audrey Southerland, Yusuke Sugano, Ruijie Tao, Minh Vo,
Yuchen Wang, Xindi Wu, Takuma Yagi, Yunyi Zhu, Pablo Arbelaez, David Cran-
dall, Dima Damen, Giovanni Maria Farinella, Bernard Ghanem, Vamsi Krishna
Ithapu, C. V. Jawahar, Hanbyul Joo, Kris Kitani, Haizhou Li, Richard Newcombe,
Aude Oliva, Hyun Soo Park, James M. Rehg, Yoichi Sato, Jianbo Shi, Mike Zheng
Shou, Antonio Torralba, Lorenzo Torresani, Mingfei Yan, and Jitendra Malik.
2022. Ego4D: Around the World in 3,000 Hours of Egocentric Video. In CVPR.
[10] Xinshuo Hu, Zifei Shan, Xinping Zhao, Zetian Sun, Zhenyu Liu, Dongfang
Li, Shaolin Ye, Xinyuan Wei, Qian Chen, Baotian Hu, and Min Zhang. 2025.
KaLM-Embedding: Superior Training Data Brings A Stronger Embedding Model.
arXiv:2501.01028 [cs.CL]
[11] Yunseok Jang, Yale Song, Youngjae Yu, Youngjin Kim, and Gunhee Kim. 2017.
TGIF-QA: Toward Spatio-Temporal Reasoning in Visual Question Answering. In
CVPR.
[12] Ranjay Krishna, Kenji Hata, Freddy Ren, Li Fei-Fei, and Juan Carlos Niebles. 2017.
Dense-Captioning Events in Videos. In ICCV.
[13] Chankyu Lee, Rajarshi Roy, Mengyao Xu, Jonathan Raiman, Mohammad Shoeybi,
Bryan Catanzaro, and Wei Ping. 2024. NV-Embed: Improved Techniques for
Training LLMs as Generalist Embedding Models. arXiv preprint arXiv:2405.17428.
[14] Jie Lei, Licheng Yu, Mohit Bansal, and Tamara L. Berg. 2018. TVQA: Localized,
Compositional Video Question Answering. In Proceedings of the 2018 Conference
on Empirical Methods in Natural Language Processing.
[15] KunChang Li, Yinan He, Yi Wang, Yizhuo Li, Wenhai Wang, Ping Luo, Yali Wang,
Limin Wang, and Yu Qiao. 2023. VideoChat: Chat-Centric Video Understanding.
arXiv preprint arXiv:2305.06355.
[16] Kunchang Li, Yali Wang, Yinan He, Yizhuo Li, Yi Wang, Yi Liu, Zun Wang,
Jilan Xu, Guo Chen, Ping Luo, Limin Wang, and Yu Qiao. 2023. MVBench: A
Comprehensive Multi-modal Video Understanding Benchmark. arXiv preprint
arXiv:2311.17005.
[17] Zehan Li, Xin Zhang, Yanzhao Zhang, Dingkun Long, Pengjun Xie, and Meishan
Zhang. 2023. Towards General Text Embeddings with Multi-stage Contrastive
Learning. arXiv:2308.03281 [cs.CL]
[18] Chin-Yew Lin. 2004. ROUGE: A Package for Automatic Evaluation of Summaries.
In Text Summarization Branches Out.
[19] Yang Liu, Dan Iter, Yichong Xu, Shuohang Wang, Ruochen Xu, and Chenguang
Zhu. 2023. G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment.
arXiv preprint arXiv:2303.16634.
[20] Niklas Muennighoff, Nouamane Tazi, Loïc Magne, and Nils Reimers. 2023. MTEB:
Massive Text Embedding Benchmark. arXiv:2210.07316 [cs.CL]
[21] Kishore Papineni, Salim Roukos, Todd Ward, and Wei-Jing Zhu. 2002. BLEU: a
Method for Automatic Evaluation of Machine Translation. In Proceedings of the
40th Annual Meeting of the Association for Computational Linguistics.
[22] Stefano Pini, Marcella Cornia, Federico Bolelli, Lorenzo Baraldi, Costantino Grana,
and Rita Cucchiara. 2019. M-VAD Names: a Dataset for Video Captioning with
Naming. Multimedia Tools and Applications 78, 24 (2019), 35583–35608.
[23] Nils Reimers and Iryna Gurevych. 2019. Sentence-BERT: Sentence Embeddings
using Siamese BERT-Networks. In Proceedings of the 2019 Conference on Empirical
Methods in Natural Language Processing and the 9th International Joint Conference
on Natural Language Processing.
[24] Anna Rohrbach, Marcus Rohrbach, and Bernt Schiele. 2014. Coherent Multi-
sentence Video Description with Variable Level of Detail. In German Conference
on Pattern Recognition.
[25] Xiaoqian Shen, Yunyang Xiong, Changsheng Zhao, Lemeng Wu, Jun Chen,
Chenchen Zhu, Zechun Liu, Fanyi Xiao, Balakrishnan Varadarajan, Florian
Schroff, Varun Jampani, Deqing Sun, and Vikas Chandra. 2024. LongVU: Spa-
tiotemporal Adaptive Compression for Long Video-Language Understanding.
arXiv preprint arXiv:2410.17434.
[26] Yaya Shi, Xu Yang, Haiyang Xu, Chunfeng Yuan, Bing Li, Weiming Hu, and Zheng-
Jun Zha. 2022. EMScore: Evaluating Video Captioning via Coarse-Grained and
Fine-Grained Embedding Matching. In CVPR. 17929–17938.
[27] Chen Sun, Fabien Baradel, Kevin Murphy, and Cordelia Schmid. 2019. Contrastive
Bidirectional Transformer for Temporal Representation Learning. arXiv preprint
arXiv:1906.05743.
[28] Chen Sun, Austin Myers, Carl Vondrick, Kevin Murphy, and Cordelia Schmid.
2019. VideoBERT: A Joint Model for Video and Language Representation Learn-
ing. arXiv preprint arXiv:1904.01766.
[29] Qwen Team. 2025. Qwen3 Embedding: Advancing Text Embedding and Reranking
Through Foundation Models. arXiv:2506.05176 [cs.CL]
[30] Tony Cheng Tong, Sirui He, Zhiwen Shao, and Dit-Yan Yeung. 2024. G-VEval:
A Versatile Metric for Evaluating Image and Video Captions Using GPT-4o.
arXiv:2412.13647 [cs.CV]
[31] Ramakrishna Vedantam, C. Lawrence Zitnick, and Devi Parikh. 2015. CIDEr:
Consensus-based Image Description Evaluation. In CVPR.
[32] Paul Vicol, Makarand Tapaswi, Lluis Castrejon, and Sanja Fidler. 2018.
MovieGraphs: Towards Understanding Human-Centric Situations from Videos.
In CVPR.
[33] Xin Wang, Jiawei Wu, Junkang Chen, Lei Li, Yuan-Fang Wang, and William Yang
Wang. 2019. VaTeX: A Large-Scale, High-Quality Multilingual Dataset for Video-
and-Language Research. In ICCV.
[34] Haoning Wu, Dongxu Li, Yizhuo Li, Yitian Yuan, Samson Tan, Ping Luo, Wayne
Wu, and Ziwei Liu. 2024. LongVideoBench: A Benchmark for Long-context
Interleaved Video-Language Understanding. arXiv preprint arXiv:2407.15754.
[35] Junbin Xiao, Xindi Shang, Angela Yao, and Tat-Seng Chua. 2021. NExT-QA: Next
Phase of Question-Answering to Explaining Temporal Actions. In CVPR.
[36] Jun Xu, Tao Mei, Ting Yao, and Yong Rui. 2016. MSR-VTT: A Large Video
Description Dataset for Bridging Video and Language. In CVPR.
[37] Yuan Yao, Tianyu Yu, Ao Zhang, Chongyi Wang, Junbo Cui, Hongji Zhu, Tianchi
Cai, Haoyu Li, Weilin Zhao, Zhihui He, Qianyu Chen, Huarong Zhou, Zhensheng
Zou, Haoye Zhang, Shengding Hu, Zhi Zheng, Jie Zhou, Jie Cai, Xu Han, Guoyang
Zeng, Dahai Li, Zhiyuan Liu, and Maosong Sun. 2024. MiniCPM-V: A GPT-4V
Level Multimodal LLM on Your Phone. arXiv preprint arXiv:2408.01800.
[38] Jiabo Ye, Haiyang Xu, Haowei Liu, Anwen Hu, Ming Yan, Qi Qian, Ji Zhang, Fei
Huang, and Jingren Zhou. 2024. mPLUG-Owl3: Towards Long Image-Sequence
Understanding in Multi-Modal Large Language Models. arXiv:2408.04840 [cs.CV]
[39] Boqiang Zhang, Kehan Li, Zesen Cheng, Zhiqiang Hu, Yuqian Yuan, Guanzheng
Chen, Sicong Leng, Yuming Jiang, Hang Zhang, Xin Li, Peng Jin, Wenqi Zhang,
Fan Wang, Lidong Bing, and Deli Zhao. 2025. VideoLLaMA 3: Frontier Multi-
modal Foundation Models for Image and Video Understanding. arXiv preprint
arXiv:2501.13106.
[40] Tianyi Zhang, Varsha Kishore, Felix Wu, Kilian Q. Weinberger, and Yoav Artzi.
2020. BERTScore: Evaluating Text Generation with BERT. In International Con-
ference on Learning Representations.
[41] Luowei Zhou, Chenliang Xu, and Jason Corso. 2018. Towards Automatic Learning
of Procedures from Web Instructional Videos. In AAAI.


## Page 10


EvalMG @SIGIR ’26, July 24, 2026, Melbourne, VIC, Australia
Ali et al.
A
Qualitative Examples
To illustrate the behavior of current VLMs on long-form, paragraph-level description, we present qualitative results for two videos drawn
from CLIP-CC-Bench: clip 112, a moderately complex snowy mountain encounter, and clip 053, a multi-character security checkpoint
scene with intricate card-passing choreography. For each clip we show sampled frames from the start and end of the 90 s segment, the
expert-annotated reference description, and the candidate descriptions from all 17 VLMs together with the per-judge cosine similarities and
the resulting Borda rank.
A.1
Clip 112: Snowy Mountain Encounter
Figure 3: Sampled frames from clip 112. Top: first ten frames. Bottom: last ten frames. Intermediate frames omitted.
Reference description. The video opens with a snowy landscape featuring tall, leafless trees, indicating a winter scene. The ground is completely
covered in snow, and in the background, someone is moving among the trees. The camera shifts to reveal a man in a red jacket and hat, with snow
in his beard, standing beside a dark horse against a snow-covered landscape and mountain backdrop. Emerging from the woods, an older man in
a fur coat and hat appears, holding a gun. The focus returns to the man in the red jacket, who appears startled as he speaks with the older man,
who responds. The man in the red jacket, holding the reins of the horse, talks to the older man as he approaches, gun in hand. The older man stops,
steps closer, and continues conversing, pointing the gun as he reveals a bone necklace around his neck. He makes a hand gesture, pats the arm of
the man in the red jacket, and then moves forward. The scene transitions to a snowy woodland area, where the older man walks ahead, with the
man in the red jacket following and holding his horse’s reins. Both men wear ski shoes to navigate the snow. The older man turns back briefly to
speak to the man in the red jacket before resuming his path. The scene then shifts to a large cottage house blanketed in snow, surrounded by a
peaceful, snow-covered landscape with a few trees.
Table 8: Per-VLM generated descriptions and per-judge cosine similarities for clip 112, sorted by Borda rank. Each numeric
column reports the harmonic-mean fine-grained / coarse-grained score HM-CF𝑗from one of the five MTEB judges.
VLM
Generated description
Borda
KaLM
GTE
NV
NeMo
Qwen3
llava_one_vision
The video begins with a serene winter scene, showcasing a snowy forest with tall, snow-covered trees. The ground is
blanketed in snow, and the sky is overcast, setting a cold and tranquil atmosphere. The scene transitions to a man in a red
jacket and a hat, standing next to a black horse. He is holding a rifle and appears to be in a conversation with another man who
is wearing a fur hat and a fur coat. The background reveals a snowy landscape with mountains in the distance, emphasizing
the harsh winter conditions. The man in the fur coat is holding a long stick and seems to be explaining something to the
man in the red jacket. The video continues with the man in the fur coat standing in the snowy forest, holding the long stick
and looking around. The man in the red jacket and hat is now standing next to him, holding a rifle and listening attentively.
The background remains consistent with the snowy landscape and the tall, snow-covered trees. The video wraps up with
the man in the fur coat continuing to hold the long stick and look around, while the man in the red jacket and hat remains
nearby, holding his rifle.
84
0.830
0.770
0.678
0.710
0.781
mplug
The video begins with a man in a red coat and hat standing next to a horse in a snowy landscape, with mountains in the
background. The scene transitions to another man in a fur coat and hat, holding a rifle, standing in a snowy forest. The man
in the red coat approaches the man in the fur coat, and they appear to be having a conversation. The man in the fur coat
then walks away, and the man in the red coat follows him. The video wraps up with the man in the fur coat walking through
the snowy forest, while the man in the red coat stands nearby, watching him.
81
0.835
0.736
0.637
0.673
0.767
videollama3
The video opens with a snowy forest scene. A man in a red coat and hat stands next to a horse, while another man dressed
in fur and carrying a rifle emerges from the trees. The two men engage in a conversation, with the man in the fur coat
gesturing emphatically. They continue their discussion, with the man in the red coat listening intently. As the conversation
progresses, the man in the fur coat becomes increasingly agitated, his gestures becoming more forceful. He points his rifle
towards the other man, who remains calm and composed. The tension between them is palpable, with the man in the fur
coat’s frustration evident in his body language and facial expressions. Eventually, the man in the fur coat turns and walks
away, leaving the man in the red coat standing alone by the horse. The video ends with a shot of a wooden cabin nestled in
the snowy landscape, suggesting a possible retreat or sanctuary for the characters. In summary, the video depicts a tense
confrontation between two men in a snowy forest setting. The man in the fur coat’s escalating agitation and the use of a
rifle create a sense of conflict and potential violence. The scene concludes with the man in the fur coat’s departure, leaving
the outcome of their interaction unresolved.
67
0.801
0.707
0.601
0.620
0.712
(Continued on next page)


## Page 11


CLIP-CC-Bench
EvalMG @SIGIR ’26, July 24, 2026, Melbourne, VIC, Australia
Table 8: (Continued) Per-VLM descriptions and scores for clip 112.
VLM
Generated description
Borda
KaLM
GTE
NV
NeMo
Qwen3
longvu
The video begins with a scene set in a wintry forest, where a person is seen walking through the snow, moving from the
right to the left of the frame. The environment is characterized by snow-covered ground and bare trees, suggesting a cold,
possibly remote location. The person’s attire, including a hat and a coat, is appropriate for the snowy conditions. The scene
is captured from a low angle, emphasizing the height of the trees and the person’s journey through the forest. As the video
progresses, the scene shifts to a more open, snowy landscape where a person is standing next to a dark-colored horse, facing
the camera. This individual is dressed in a red garment and a hat, with a strap across their chest, indicating a readiness for
travel or adventure. The horse, equipped with a saddle and bridle, suggests preparedness for riding. The background features
a mountainous terrain, adding to the sense of a rugged, possibly remote setting. The camera angle is direct, focusing on
the person and the horse against the wintry backdrop. The narrative then transitions to a close-up of an elderly man in
a fur hat and a coat with fur lining, standing in a snowy forest. His expression is solemn, and he appears to be in a state
of contemplation or concern. The camera zooms in on him, highlighting his facial features and the texture of his clothing
against the wintry forest setting. This shift in focus suggests a moment of significance or a pivotal moment in the story.
Subsequently, the video shows the elderly man standing in the same wintry forest, now holding a rifle, indicating a readiness
for action or defense. His expression is stern, and he appears to be addressing someone or something off-camera. The camera
maintains its focus on him, emphasizing his presence and the potential tension in the scene. The final scene captured in the
video shows the elderly man in a different location within the same wintry forest, now accompanied by a younger person.
They are standing in the snow, with the younger individual holding a rifle, mirroring the older man’s stance. The older man
is holding a stick, and both are facing forward, suggesting a shared focus or destination. The camera angle remains steady,
capturing the two figures against the wintry backdrop, emphasizing their presence and the potential narrative connection
between them. Throughout the video, the wintry forest setting serves as a consistent backdrop, with the changing scenes
and characters highlighting a narrative of travel, contemplation, and potential conflict or adventure.
61
0.798
0.685
0.587
0.595
0.724
vilamp
The video begins with a shot of a snowy forest, where a man in a fur coat and hat is walking through the trees. The camera
then cuts to another man, dressed in a red coat and hat, standing next to a horse. This second man appears to be speaking to
the first man, who is now closer to the camera. The first man seems to be listening intently, while the second man continues
to speak. The scene then cuts back to the first man, who is now holding a rifle. He appears to be preparing to shoot something.
The second man continues to speak, and the first man listens. The scene ends with the first man raising his rifle, aiming it at
the second man.
60
0.807
0.689
0.560
0.614
0.717
sharegpt4
The video begins with a scene set in a snowy landscape, where a man dressed in a fur-lined coat and a wide-brimmed hat is
seen walking towards the camera. He is accompanied by a horse, which is partially visible and appears to be moving in the
same direction as the man. The background is a wintry landscape with snow-covered ground and bare trees, suggesting a
cold, possibly remote location. The man’s attire and the presence of the horse suggest a historical or period setting, possibly
related to a narrative or a film. As the video progresses, the man continues his journey across the snowy terrain, with the
horse following closely behind. The environment remains consistent, with the snow-covered ground and bare trees in the
background. The man’s forward movement is evident, and the camera follows him, maintaining a steady focus on his journey.
The scene then shifts to a different location within the same snowy landscape, where the man is now seen standing still,
facing the camera. He is dressed in a fur-lined coat and a wide-brimmed hat, with a rifle slung over his shoulder, indicating a
readiness for action or defense. The background features a dense forest of bare trees, suggesting a change in location or
a different part of the same landscape. The camera has zoomed in on the man, focusing on his upper body and the rifle,
while the man’s posture and the environment suggest a moment of pause or contemplation. In the final scene, the man is
seen walking through the snowy landscape, moving towards the camera. His attire and the rifle remain consistent with the
previous scene, and the environment continues to be a snowy, forested area. The camera has zoomed out slightly, providing
a wider view of the man’s journey and the surrounding landscape. The man’s forward movement and the camera’s focus
on him suggest a continuation of his journey or mission, with the snowy forest setting providing a consistent backdrop
throughout the video.
59
0.784
0.684
0.590
0.608
0.722
videochatflash
A man wearing a red coat and brown hat is walking in the snow with his horse. A person wearing a fur coat, scarf, and hat
is standing next to the first man holding a rifle. In the background there are trees covered in snow, mountains, and a house.
56
0.775
0.652
0.582
0.631
0.725
minicpm
The video depicts a sequence of events set in a snowy forest, featuring two main characters and their interactions. Initially,
the scene is established with a view of a snow-covered landscape dotted with bare trees, indicating a cold environment.
One character, dressed in rugged attire including a hat and a red jacket, appears to be engaging with another individual or
object within this wintry setting. This person’s actions suggest they are either preparing for an activity or responding to
something occurring off-camera. As the video progresses, the focus shifts to a second character, who is clothed in fur-lined
garments and seems to be holding a rifle, suggesting readiness for hunting or defense. The presence of horses equipped
with gear hints at a journey or expedition taking place. Throughout the video, there is a dynamic interplay between these
two individuals as they navigate through the snowy terrain. At one point, the character in the red jacket moves away from
the foreground, leading to a moment where only the figure in fur-lined clothing is visible, emphasizing their isolation in
the woods. Subsequently, the camera reveals both characters again, with the individual in the red jacket now seen walking
through the forest, interacting with the environment by touching a tree branch, which indicates a moment of contemplation
or connection with nature. The narrative continues with the introduction of movement as the horse attached to the sled is
seen trotting forward, suggesting progression along their path. A close-up shot focuses on the character in the fur-lined
coat, who holds a rifle, reinforcing themes of survival or vigilance. Towards the end, the perspective widens to include more
of the wooded area and the sled, highlighting the ongoing journey. The interaction between the two characters becomes
clearer; one character extends a hand, possibly offering assistance or initiating communication, while the other stands
with the rifle, maintaining a stance that suggests preparedness. Overall, the video captures a series of moments involving
exploration, preparation, and subtle interaction between the two central figures amidst a serene yet challenging winter
backdrop, underscoring themes of endurance and companionship in a harsh natural setting.
54
0.784
0.688
0.588
0.572
0.711
(Continued on next page)


## Page 12


EvalMG @SIGIR ’26, July 24, 2026, Melbourne, VIC, Australia
Ali et al.
Table 8: (Continued) Per-VLM descriptions and scores for clip 112.
VLM
Generated description
Borda
KaLM
GTE
NV
NeMo
Qwen3
ts_llava
we see a scene from a movie featuring a group of men in a snowy forest. The main focus is on two characters, one of whom
is an older man with a long white beard and a red coat, standing in the foreground. He appears to be speaking to another
man who is standing slightly behind him. The older man is holding a rifle, suggesting he might be preparing for a hunt or a
confrontation. The other man is dressed in a brown coat and a hat, looking attentively at the older man. The scene is set in a
wintery landscape with snow-covered trees and a clear sky. The camera movements are smooth and natural, capturing the
characters’ expressions and body language. The older man’s beard is prominent, indicating his age and the harsh conditions
they are in. The other man’s attire and the way he holds his hat suggest he might be from a different culture or time period.
The overall atmosphere of the video is tense and dramatic, with the snowy forest setting adding to the sense of isolation and
danger. The characters’ actions and expressions hint at a storyline involving survival, conflict, or a significant event in their
lives.
49
0.785
0.655
0.541
0.592
0.724
Qwen2.5-32B
The video clip opens with a serene winter forest scene, where a lone figure dressed in a red coat and a wide-brimmed hat is
seen walking through the snow-covered landscape. The individual appears to be on horseback, as indicated by the presence
of a horse’s head in some frames. The setting is cold and desolate, with bare trees and a blanket of snow covering the ground,
suggesting a remote and harsh environment. As the scene progresses, another character emerges from the snowy woods,
wearing a heavy fur coat and a large white fur hat, indicating the extreme cold. This second character approaches the first,
and they engage in a conversation, their breath visible in the frigid air. The interaction seems tense, as both individuals
are equipped with weapons, hinting at potential conflict or a serious discussion. The camera captures close-up shots of
their faces, emphasizing their expressions and the gravity of the situation. The overall atmosphere is one of suspense and
tension, underscored by the stark, wintry backdrop and the characters’ rugged attire. The scene concludes with the two
figures standing face-to-face, their postures and expressions suggesting a pivotal moment in their encounter.
43
0.763
0.670
0.566
0.560
0.719
video_xl
The video begins with a serene winter landscape, showcasing a snow-covered forest with bare trees and a solitary figure
standing in the snow, facing away from the camera. The scene is tranquil, with no movement except for the slight swaying
of the trees, under an overcast sky. As the video progresses, the camera zooms in on the figure, revealing more details such
as a fur hat and a long coat, suggesting cold weather attire. The figure’s posture changes slightly, indicating some movement,
while the background remains consistent with the snowy forest setting. The focus then shifts to another individual, who
appears to be walking through the snow, carrying a rifle and wearing a red jacket. This person is also equipped with a fur
hat, emphasizing the cold environment. The camera captures this person from behind, moving forward into the snowy
landscape. Subsequently, the camera angle changes to show two individuals walking side by side through the snow, both
dressed in heavy winter clothing. One of them is holding a rifle, and they seem to be engaged in conversation or interaction,
as indicated by their body language and facial expressions. The video continues with these two individuals walking together,
maintaining their pace and direction through the snowy terrain. The camera follows them closely, capturing their journey
without any significant change in perspective or environment. Finally, the video transitions to a different scene where three
individuals are seen walking through a snowy landscape, with one leading the way and the other two following. The leading
individual is dressed in a dark coat and hat, while the others wear lighter-colored clothing. The camera captures this group
from behind, focusing on their movement through the snow-covered ground, with the environment remaining consistent
throughout the video.
40
0.752
0.671
0.570
0.563
0.696
Qwen2.5-72B
In a snowy, wooded landscape, two men dressed in rugged winter attire encounter each other amidst the stark beauty of a
snow-covered forest. The first man, wearing a fur-lined coat and hat, emerges from behind a tree, holding a rifle, while the
second man, clad in a red plaid shirt and brown hat, stands beside his horse, also armed with a rifle. They exchange tense
words, their breath visible in the cold air, as they assess each other’s intentions. The scene shifts to show them walking
through the trees, their figures framed by the bare branches, suggesting a cautious yet determined advance. The atmosphere
is thick with anticipation, hinting at a potential confrontation or alliance in this harsh, wintry setting.
34
0.754
0.663
0.532
0.563
0.703
llava_next_video
The video depicts a man standing in a snowy landscape, surrounded by trees. He is wearing a fur coat and a hat, suggesting
that it is cold. The man appears to be looking off into the distance, possibly observing something or someone. The camera
angle is from behind the man, giving a view of his back and the snowy landscape around him. The trees are covered in snow,
and the ground is also covered in a thick layer of snow. The man’s coat and hat are the only visible colors in the otherwise
white and gray landscape. The man’s posture is relaxed, and he seems to be at ease in the cold environment. The video does
not show any other characters or entities, and there are no significant actions or movements taking place. The scene is
peaceful and serene, with the man and the snowy landscape being the main focus.
23
0.748
0.602
0.544
0.537
0.629
oryx
The video opens with a serene winter scene set in a forest blanketed by snow. The trees, mostly birches given their distinctive
white bark and black markings, stand tall against the overcast sky. The ground is covered in a thick layer of untouched snow,
creating a tranquil and isolated atmosphere. As the camera slowly pans across the landscape, it reveals a solitary figure
moving through the trees. The person appears to be walking at a steady pace, their silhouette contrasting against the white
snow and the dark trunks of the trees. The scene conveys a sense of solitude and quietness, with the only movement coming
from the lone walker.
16
0.724
0.625
0.501
0.530
0.644
internvl
First, we see a rugged man with a bow and arrow standing in the snowy forest, dressed in medieval-style clothing, his face
looking off to the side. Next, he turns towards the camera with the bow drawn back, in a pose suggesting he is ready to shoot.
Then, he looks directly into the camera, creating a tense atmosphere. The man faces the camera again, this time looking
at the viewer as if to communicate or connect. The scene then shifts to a campset consisting of a teepee, people gathered
around it, including a man with a rifle. A woman in a red jacket and hat sits beside the teepee, while a man with a hat stands
in front of it, appearing in a tense conversation. The man with the rifle faces the woman, his stance indicating readiness.
Then, a group of men with rifles are shown, suggesting a sense of tension and alertness around them. They are walking
through the snow in the forest. We see a man on fire walking through the snowy forest on the right side of a large tree
trunk, followed by a group of people carrying rifles and walking together. Finally, the group of people enters the scene, with
various interactions taking place. We see more men standing together, a woman holding a baby, a small dog, and a horse.
The man in the red jacket and hat remains seated beside the teepee, watching the scene. Overall, this video seems to depict
an active scene from a historical or fictional setting, with tension and interactions among the characters, a mix of people,
animals, and objects. The snowy forest and campsite add to the ambiance and suggest a setting that is both rugged and tense.
16
0.735
0.637
0.475
0.533
0.623
(Continued on next page)


## Page 13


CLIP-CC-Bench
EvalMG @SIGIR ’26, July 24, 2026, Melbourne, VIC, Australia
Table 8: (Continued) Per-VLM descriptions and scores for clip 112.
VLM
Generated description
Borda
KaLM
GTE
NV
NeMo
Qwen3
timechat
In the video, a group of people are shown standing around a group of actors outside. They are in the middle of a scene where
an old man is talking to a couple of men. The old man is wearing a red beard and is holding a rifle. The men around him are
dressed in woolen clothing and are surrounded by pine trees. There is snow on the ground. The actors are standing in the
woods, and the scene seems to be set in the Wild West.
14
0.745
0.589
0.471
0.526
0.668
longva
The video is a compilation of scenes from the movie “The Three Amigos” featuring the comedic actor Steve Martin. In each
scene, Steve Martin is seen in various roles and situations, often interacting with other characters or performing humorous
antics. In one scene, he is dressed as a cowboy, riding a horse and wearing a red jacket. He appears to be in a western
setting with snow-covered ground and trees in the background. In another scene, he is seen in a more rustic attire, possibly
a fur-trader or a native American, with a long beard and a fur hat. He is standing in a snowy landscape with trees and
mountains in the distance. Throughout the video, there are shots of horses, trees, and snowy landscapes, suggesting that the
scenes take place in a cold, winter environment. The overall tone of the video is comedic, with Steve Martin’s expressive
facial expressions and body language adding to the humor.
8
0.680
0.586
0.503
0.501
0.603
A.2
Clip 053: Security Checkpoint Scene
Figure 4: Sampled frames from clip 053. Top: first ten frames. Bottom: last ten frames. Intermediate frames omitted.
Reference description. The video begins with a man in a black suit and blue shirt looking to his side as he unbuttons his jacket. A guard
observes him in a well-lit setting, with white panels in the background. As the camera shifts, it focuses on another man wearing a black jacket
and gray shirt, who removes his glasses and hands them to a guard while looking in another direction. The scene returns to the man in the blue
shirt, who receives instructions from a guard to raise his hand. He looks at his hand, pressing his palm inward, where he holds a green card.
Following the guard’s directions, he turns his wrist to reveal his palm, flipping the card to the back of his hand and holding it with his fingers. In
the background, the man in the black jacket and gray shirt is inspected by a second guard. The guard instructs the man in the blue shirt to turn
around and place his hands behind his head. The man complies, and while doing so, the green card becomes hidden. The camera then transitions
to a woman in a black dress, raising her hand as a guard inspects her. The camera cuts back to the man in the blue shirt, who is extending his
arms with an ace of spades card visible in his palm. As the guard inspects him, the man flips the card to the back of his hand. While the guard
examines his legs, the man discreetly flips the card again, catching it between his mouth and hand before moving it through his arm. The guard
asks the man to turn around, and as he does so, he tosses the card behind him. The camera follows the card as it drifts to the man in the black
jacket and gray shirt, who catches it from his right side, concealing it in his palm while being inspected from behind. The man slides the card into
his sleeve, and as the guard inspects his arms, the camera captures the card hidden within his sleeve. The camera then shifts to a man in a gray
suit with a red tie, standing in front of a display panel and looking in another direction. Behind him, a woman in a white apron and green gloves
touches the panel. As the man in the black jacket and gray shirt raises his arm, the card slides further down his sleeve, and the camera reveals it
gradually moving downward. In the background, a woman in a black dress watches him intently. The camera returns to the woman in the black
dress as she converses with a guard, keeping her hand raised and then walking away. The camera follows the card as it slips out of the man’s pant
leg and lands near the woman’s shoe as she walks past him. She notices the card, smiles subtly, and continues walking. A bald man then passes
her, exchanging a glance. The woman approaches another guard, subtly retrieves the card, and shows it to both the bald man and the man in the
black jacket. Following the guard’s instructions, she places her hands around her neck, tucking the card into her hair. She then lifts her hands and
turns around, slipping the card into her blouse discreetly as the guard inspects her. She turns back, showing her palms to the guard as instructed.
In the final scene, the guard asks her to raise her arms. As he inspects her, she suddenly pushes him back by his waist, placing her hands behind
her back and continuing to conceal the card within her dress.


## Page 14


EvalMG @SIGIR ’26, July 24, 2026, Melbourne, VIC, Australia
Ali et al.
Table 9: Per-VLM generated descriptions and per-judge cosine similarities for clip 053, sorted by Borda rank. The longva entry
has been truncated for space; see footnote in the table body.
VLM
Generated description
Borda
KaLM
GTE
NV
NeMo
Qwen3
videollama3
The video begins with a man in a suit standing in front of a security guard. The guard is holding a small card, and the man
in the suit is looking at it. The guard then asks the man to raise his hands, and the man complies. A woman in a black dress
then enters the scene and raises her hands as well. The man in the suit then takes out a playing card from his pocket and
shows it to the guard. The guard takes the card and examines it. The man in the suit then turns around and walks away. The
scene changes to a woman in a white lab coat working on a computer. She is joined by a man in a suit, and they both look at
the screen. The woman points at something on the screen, and the man nods. The scene then cuts back to the man in the
suit, who is now being held by a security guard. The man is raising his hands, and the guard is looking at him. The scene
then cuts to a close-up of the man’s hands, which are raised in the air. The man then lowers his hands, and the guard lets go
of him. The scene changes again to a woman in a black dress walking through a hallway. She is wearing high heels, and her
hair is styled in loose waves. She is followed by a man in a suit. The woman then stops and turns around to face the man.
She smiles and reaches out to touch his face. The man looks surprised, and he steps back. The woman then turns around and
walks away. The scene changes one last time to a woman in a black dress standing in front of a security guard. The guard is
holding her arms behind her back, and she is looking at him with a surprised expression. The woman then raises her hands,
and the guard releases her. The woman then turns around and walks away. In summary, the video depicts a series of events
involving a man in a suit, a woman in a black dress, and a security guard. The man in the suit is initially questioned by the
security guard, but he is eventually allowed to pass. The woman in the black dress is also questioned by the security guard,
but she is eventually released. The video ends with the woman in the black dress walking away from the scene.
83
0.809
0.726
0.566
0.633
0.694
vilamp
The video begins with a man in a black jacket and glasses being questioned by a security guard in a futuristic setting. The
guard, wearing a gray uniform and a cap, asks the man to raise his hands. The man complies, and the guard uses a device to
scan him. The scene transitions to a woman in a black dress and high heels, who is also being questioned by the same guard.
She raises her hands and appears to be under the same scanning device. The man then reveals a playing card, specifically an
Ace of Spades, from his sleeve. He explains that he has a special ability to manipulate playing cards. The guard and other
security personnel react with shock and awe. The scene ends with the man holding up the Ace of Spades card, emphasizing
his unique power.
82
0.796
0.702
0.560
0.633
0.708
mplug
The video begins with a man in a dark jacket and glasses standing in a modern, white room with geometric patterns on the
walls. He is adjusting his glasses, preparing for something important. The scene transitions to a security checkpoint where
a man in a light blue shirt is being scanned by a security officer in a gray uniform. The security officer uses a handheld
device to scan the man’s arms and body, ensuring he is not carrying any prohibited items. The man in the light blue shirt
raises his arms, and the security officer continues the scan. The scene then shifts to a woman in a black dress with cut-out
shoulders, who is also being scanned by the security officer. The woman raises her arms, and the security officer uses a
handheld device to scan her. The scene then shows a close-up of a hand holding a small, rectangular object, possibly a
security pass or identification card. The security officer in the gray uniform is seen holding the woman’s arm, guiding her
through the security process. The woman appears to be speaking to the security officer, possibly explaining something or
asking a question. The video wraps up with the woman and the security officer standing together, with the woman looking
slightly concerned or confused.
75
0.762
0.643
0.460
0.575
0.656
minicpm
The video sequence unfolds in a high-tech, futuristic setting with geometric patterns and advanced technology visible
throughout. It begins with two characters engaging in what appears to be a security or inspection process. One character,
dressed in a light blue shirt and dark trousers, is being approached by an individual in a uniform marked with a red emblem
on the arm. This interaction suggests a form of verification or questioning. As the scene progresses, the focus shifts to another
individual in a black sleeveless top, who seems to be in distress or resistance against a forceful action from a uniformed
figure. The tension escalates as this person is restrained, hinting at a conflict or confrontation within the sterile environment.
Subsequently, attention returns to the initial pair where the uniformed figure seems to be explaining something, possibly
about the procedure or outcome related to the earlier actions. The camera then moves to capture a card with a heart symbol,
which might signify a crucial element or clue within the narrative. The video continues with the restrained individual’s
perspective, showing them reaching out towards someone off-screen, indicating an attempt for connection or escape. The
presence of multiple individuals in uniforms suggests a broader operation or investigation taking place. A significant shift
occurs when the focus moves to a woman in a black dress, seemingly distressed, interacting with a man in a cap and uniform.
Their exchange involves gestures that suggest communication or negotiation amidst a backdrop of ongoing activity and
surveillance within the facility. Towards the end, the video captures moments of heightened emotion and physical interaction
between the woman and the uniformed man, culminating in a moment of release or relief. The woman’s body language
indicates a mixture of exhaustion and gratitude, while the man’s posture conveys a sense of completion or satisfaction.
Throughout the sequence, the camera movements vary from close-ups highlighting emotional expressions to wider shots
capturing the broader context of the interactions and the surrounding technological environment. The consistent use of
white and grey tones reinforces the clinical and controlled atmosphere of the setting.
65
0.712
0.563
0.413
0.473
0.640
Qwen2.5-72B
In a high-tech, modern setting with sleek white walls and advanced technology, a tense confrontation unfolds between a
group of individuals and security personnel. The scene begins with a man in a suit and tie being searched by two guards, who
find a small object on him. As the tension escalates, another man in a suit raises his hands in surrender while a third man in
a black jacket and glasses is also frisked. A woman in a black dress is seen being restrained by a guard, her arms raised as
she appears to be communicating with someone off-screen. The atmosphere is charged with urgency as the guards, dressed
in uniform with caps and badges, maintain control over the situation. The camera captures close-ups of the characters’ faces,
highlighting their expressions of concern and determination. The scene concludes with the woman being led away by the
guards, her back turned to the camera, as the other individuals remain under scrutiny.
63
0.707
0.575
0.410
0.501
0.623
(Continued on next page)


## Page 15


CLIP-CC-Bench
EvalMG @SIGIR ’26, July 24, 2026, Melbourne, VIC, Australia
Table 9: (Continued) Per-VLM descriptions and scores for clip 053.
VLM
Generated description
Borda
KaLM
GTE
NV
NeMo
Qwen3
longvu
The video depicts a sequence of events in a futuristic setting, beginning with a man in a suit and a security officer in a sterile
environment. The man is seen adjusting his glasses, and the scene transitions to a group of security officers interacting with
a man in a light blue shirt. The officers are shown conducting a thorough search on the man, including patting him down
and examining his belongings. The search process is meticulous, with the officers using various tools and techniques to
ensure a comprehensive examination. As the search progresses, the man in the light blue shirt is shown being searched
by multiple security officers, with the focus on his arms, hands, and eventually his head. The officers employ a range of
techniques, including physical searches, electronic devices, and specialized tools, to conduct a thorough examination. The
man appears to be cooperative throughout the process, allowing the officers to conduct their search without resistance. The
video then shifts to a scene where the man is being escorted by a security officer, indicating the end of the search process.
The man is shown being led away, suggesting that the search was completed and the officers are now escorting him out of
the area. The video concludes with the man being led away, with the security officer maintaining a firm grip on his arm,
indicating that the search has concluded and the man is being taken away.
59
0.703
0.596
0.347
0.476
0.596
llava_one_vision
The video takes place in a futuristic setting characterized by white geometric patterns on the walls and a large stack of black
boxes in the background. It begins with a man in a dark suit and tie standing in front of another man in a gray uniform with
a red emblem on the sleeve. The man in the suit gestures with his hands, while the man in the uniform looks on. The scene
transitions to a woman in a black sleeveless top and a black choker necklace, who raises her hands in the air, seemingly in a
state of distress or surprise. The man in the gray uniform approaches her, places a hand on his forehead, and then holds up a
small object with a patterned design. The woman looks at the object, and the man in the gray uniform turns to face her. The
video wraps up with the woman embracing the man in the gray uniform from behind, while the man in the dark suit stands
nearby. The background remains consistent throughout, featuring the white geometric patterns and the stack of black boxes.
58
0.687
0.593
0.412
0.471
0.571
timechat
In the video, a man is seen throwing playing cards while a woman is standing in front of him. The man and the woman are
both wearing suits, and they are in a futuristic-looking room with a computer screen in front of them. The woman is calm
and collected throughout the video.
51
0.679
0.533
0.411
0.435
0.588
sharegpt4
The video begins with a scene set in a modern, high-tech environment, featuring a man in a dark suit and a woman in a
black dress, both standing in a room with a large window and a geometric patterned wall. The man appears to be speaking
or reacting to something, while the woman looks off to the side, possibly listening or observing. The scene is static, with no
camera movement, and the lighting is bright, highlighting the room’s contemporary design. The video then transitions to a
different scene where two men are engaged in a conversation in a similar modern setting. One man, dressed in a dark suit,
is speaking and gesturing with his hands, while the other, wearing a light-colored shirt and a cap, listens attentively. The
background features a large window and a geometric patterned wall, consistent with the first scene. The camera remains
static, focusing on the interaction between the two men. Following this, the video shows a man in a light-colored shirt and
cap, standing in a room with a geometric patterned wall and a large window. He appears to be in motion, possibly walking or
turning, with his arms outstretched. The camera has moved to a side angle, capturing the man’s movement. The next scene
shows the same man in a different pose, with his arms raised and hands open, suggesting a gesture of surprise or excitement.
The background remains consistent with the previous scene, and the camera has moved to a side angle, capturing the man’s
upper body and the gesture. The video then shifts to a different setting, showing a man in a light-colored shirt and tie,
standing in a room with a geometric patterned wall and a large window. He appears to be in motion, possibly walking or
turning, with his arms outstretched. The camera has moved to a side angle, capturing the man’s movement. In the final
scene, the man in the light-colored shirt and tie is seen with his arms raised and hands open, suggesting a gesture of surprise
or excitement. The background remains consistent with the previous scene, and the camera has moved to a side angle,
capturing the man’s upper body and the gesture.
44
0.651
0.556
0.382
0.455
0.533
video_xl
A group of individuals is gathered in an indoor setting with a modern architectural style, featuring geometric patterns on the
walls and a high ceiling. The focus is on three main characters: two men and one woman. The first man, dressed in a dark
suit, stands facing the woman who is wearing a black top and has her back to the camera. He appears to be speaking to her,
gesturing with his hands as if explaining something. The second man, wearing a light blue shirt and a cap, stands behind the
first man, observing the interaction. His posture suggests he is listening attentively. As the sequence progresses, the woman
turns around, revealing a surprised expression. She seems to be reacting to something that has caught her attention or
caused her surprise. The second man’s expression changes from attentive to slightly concerned as he watches the woman’s
reaction. In the final moments, the woman’s expression shifts to one of shock or disbelief, and she raises her hands to her
face, possibly in reaction to what she has seen or heard. The second man reaches out to her, perhaps trying to comfort
or understand her reaction. Throughout the sequence, the camera remains mostly static, focusing on capturing the facial
expressions and body language of the characters, which convey a sense of drama and intensity in their interaction.
33
0.634
0.525
0.352
0.419
0.481
videochatflash
A man wearing a black coat is standing on the left side of another man, and he puts his glasses on. Another man in a grey
uniform is talking to him while putting his hands on his shoulders. A woman with brown hair is dancing on the right side of
the first man. The second man takes off his shirt and starts doing some exercises. In the background, there are white walls,
glass windows, and people’s voices can be heard.
31
0.643
0.505
0.316
0.409
0.540
longva†
The video appears to be a compilation of scenes from the movie “The Adjustment Bureau”. The film features an ensemble cast
including Matt Damon, Emily Blunt, John Krasinski, and Anthony Mackie. The setting is a futuristic cityscape with a sleek,
modern design. In the first scene, we see Matt Damon’s character, David Norris, in a conversation with a woman who is
adjusting his tie. This interaction seems to be a moment of casual interaction between two people. The second scene shows a
group of characters standing in a room with a large screen displaying various data points. One of the characters is holding up
a card that has a heart symbol on it. This could suggest a plot point or a symbolic gesture within the context of the film. The
third scene captures a moment where a character is seen with a concerned expression, possibly indicating tension or conflict
in the narrative. The fourth scene shows a character with a serious expression, looking at another character who is holding
a card. This could be a pivotal moment in the story, possibly involving a decision or revelation. ... [output truncated; the
remaining ∼10 000 characters consist of repetitive variants of “the [Nth] scene captures a character with a [emotion] expression,
holding a card with a heart symbol”, spanning hundreds of redundant rows; see Section B.3.]
29
0.600
0.526
0.294
0.413
0.563
(Continued on next page)


## Page 16


EvalMG @SIGIR ’26, July 24, 2026, Melbourne, VIC, Australia
Ali et al.
Table 9: (Continued) Per-VLM descriptions and scores for clip 053.
VLM
Generated description
Borda
KaLM
GTE
NV
NeMo
Qwen3
Qwen2.5-32B
The video sequence appears to depict a high-stakes, action-packed scenario set in a modern, possibly futuristic environment.
The scene opens with individuals in uniform, suggesting a security or military setting, engaging in what seems to be a
tense confrontation. A man in a suit is seen being restrained by uniformed personnel, indicating a situation where authority
figures are apprehending or controlling someone. The environment is sleek and technological, with large screens displaying
data and holographic elements, hinting at advanced surveillance or monitoring systems. As the sequence progresses, there is
a sense of urgency and chaos. Characters are shown raising their hands in surrender or compliance, while others appear
to be in distress or being subdued. The presence of a woman in a black dress being held back by uniformed officers adds
to the intensity of the scene, suggesting she might be involved in the unfolding drama. The quick cuts between different
angles and perspectives create a dynamic and fast-paced atmosphere, emphasizing the tension and conflict. The video also
includes moments of physical struggle, with characters being pushed against walls or restrained physically, highlighting the
physical nature of the confrontation. The overall tone is one of suspense and danger, with the characters’ expressions and
body language conveying fear, determination, and resistance. The setting, combined with the actions, suggests a narrative
involving espionage, rebellion, or some form of covert operation within a highly controlled environment. The use of close-ups
and rapid transitions further enhances the dramatic impact, drawing the viewer into the heart of the action.
28
0.652
0.481
0.314
0.376
0.542
ts_llava
we see a sequence of key frames from a video featuring actors in a futuristic setting. The main focus is on a man and a
woman who are in the midst of a conversation. The man, dressed in a gray suit, is seen gesturing with his hands, possibly
explaining something. The woman, wearing a black dress, is attentively listening. They are standing in a room with a white
floor and a large screen displaying what appears to be a map or a schematic. In the background, there are other individuals
present, including a man in a hat and a woman in a black dress. The room has a high-tech ambiance, with a large window
that offers a view of a cityscape. The overall scene suggests a narrative involving technology, communication, and possibly a
futuristic city. The video captures the characters’ expressions and body language, providing insight into their emotions and
the nature of their interaction. The camera movements and the use of close-ups and wide shots contribute to the immersive
experience of the video. The setting, characters, and their actions all contribute to the storytelling aspect of the video.
24
0.630
0.492
0.323
0.383
0.496
llava_next_video
In the video, we see a man and a woman in a room. The man is wearing a uniform, suggesting he might be a security officer
or a member of a service team. The woman is dressed in a black dress, which could indicate a formal or professional setting.
The man is holding a walkie-talkie, a device commonly used for communication in security or law enforcement contexts.
The woman is holding a phone, which she appears to be using to make a call. The man is gesturing with his hand, possibly
indicating a direction or a command. The woman is looking at the man, suggesting that she is engaged in a conversation
with him. The room they are in is not clearly visible, but it seems to be an indoor space with a neutral color scheme. The
lighting is bright, and there are no visible shadows or reflections. The video does not show any significant actions or events,
but it does provide a glimpse into the interaction between the man and the woman.
20
0.630
0.423
0.324
0.387
0.467
oryx
In the video, two individuals are engaged in a conversation within a modern, minimalist room characterized by its white
geometric patterns on the walls. The person on the left is dressed in a formal black suit and tie, appearing to be in his mid-30s
with short hair. He is seen gesturing with his hands as he speaks, indicating an animated discussion. The individual on the
right is wearing a gray uniform with a badge featuring a red emblem, suggesting a role of authority or service. This person
listens attentively, maintaining eye contact and occasionally nodding in response to the speaker. The setting suggests a
professional or official environment, possibly a meeting or interview taking place in a corporate or institutional space.
15
0.595
0.451
0.303
0.342
0.506
internvl
Sorry, I can’t provide descriptions for these images as they do not represent a coherent video.
5
0.525
0.183
0.199
0.203
0.343
† The full longva output for clip 053 is approximately 10 837 characters; we display the first ∼1 200 characters here as the description rapidly
degenerates into repetitive nonsense (analyzed in Section B.3).


## Page 17


CLIP-CC-Bench
EvalMG @SIGIR ’26, July 24, 2026, Melbourne, VIC, Australia
B
Analysis of VLM Performance
B.1
Cross-Exhibit Performance Patterns
The qualitative results in clips 112 and 053 reveal distinct perfor-
mance patterns across VLMs and embedding judges. In clip 112,
which features a moderately complex winter narrative, the top-
ranked VLM llava_one_vision (Borda 84) achieves strong, con-
sistent scores across all judges (KaLM 0.830, GTE 0.770, NV 0.678,
NeMo 0.710, Qwen3 0.781). Its description captures the essential
narrative arc — the encounter between two men in a snowy land-
scape — while identifying key visual elements such as clothing,
weapons, and environmental details.
Examining the per-judge HM-CF𝑗scores reveals a clear perfor-
mance stratification: top-tier VLMs (llava_one_vision, mplug,
videollama3) maintain scores above 0.70 across most judges, mid-
tier models (minicpm, ts_llava, Qwen2.5-32B) fall in the 0.60–0.75
range, and lower-tier models (oryx, internvl, longva) drop below
0.65. KaLM consistently produces the highest absolute scores while
NV-Embed yields the lowest, suggesting differential sensitivity to
description quality across embedding architectures.
B.2
Embedding-Judge Sensitivity to Description
Length
A critical observation emerges from clip 053, which presents a
complex multi-character security checkpoint scene with intricate
card-passing choreography. The reference description ( ∼2 665 char-
acters ) demands fine-grained temporal tracking and action sequenc-
ing. Here the cross-judge ordering diverges visibly from the clip 112
pattern. videollama3 (Borda 83) generates a 1 940-character de-
scription and maintains reasonable scores (KaLM 0.809, GTE 0.726,
Qwen3 0.694), but NV-Embed shows marked degradation (0.566),
revealing heightened sensitivity to length-precision mismatches.
In contrast, most judges (KaLM, GTE, NeMo, Qwen3) demon-
strate remarkable length invariance, with HM-CF𝑗remaining sta-
ble despite substantial candidate–reference length disparities. This
suggests these models capture semantic alignment largely inde-
pendently of verbosity, whereas NV-Embed appears to penalise
length mismatches more severely, artificially inflating the implicit
precision requirement. For example, mplug (Borda 75) generates a
concise 656-character description yet maintains respectable scores
under KaLM (0.762), GTE (0.643), and Qwen3 (0.656), while NV-
Embed assigns only 0.460.
B.3
The Pathological Case of LongVA on Clip
053
longva exhibits anomalous behavior on clip 053, generating an
extremely verbose 10 837-character description — more than four
times the reference length — that consists largely of repetitive, hal-
lucinatory content nominally grounded in the movie “The Adjust-
ment Bureau”. After a coherent first few sentences, the description
devolves into recursive patterns, repeatedly describing characters
“holding a card with a heart symbol” in numbered scenes that exceed
the actual video content. This pathological verbosity yields cata-
strophically low scores across all judges (KaLM 0.600, GTE 0.526,
NV 0.294, NeMo 0.413, Qwen3 0.563), with NV-Embed penalizing it
most severely.
Inspection reveals that the description bears almost no corre-
spondence to the security checkpoint narrative. It fabricates movie
references, invents non-existent scenes, and demonstrates complete
failure of temporal coherence. The repetitive pattern (“the [ordinal]
scene captures a character with a [emotion] expression, holding
a card with a heart symbol”) spans hundreds of lines without ad-
vancing narrative understanding. This failure mode highlights an
important limitation: when a VLM catastrophically misinterprets
content, its verbosity compounds the error, producing descriptions
that are simultaneously lengthy and semantically void.
B.4
Cross-Validation with Aggregate Rankings
The Borda rankings observed in both exhibits align with the over-
all VLM ranking reported in the main paper. Models that consis-
tently perform well across diverse video types (llava_one_vision,
mplug, videollama3) occupy top positions in both qualitative ex-
hibits and the aggregate quantitative ranking; conversely, mod-
els that struggle here (internvl, longva, oryx) consistently rank
lower in the comprehensive benchmark. This cross-validation be-
tween detailed qualitative analysis and large-scale quantitative
evaluation supports the robustness of our automated assessment
methodology.
The consistency of relative model orderings across very differ-
ent video complexities — from the comparatively straightforward
winter encounter (clip 112) to the intricate security choreography
(clip 053) — suggests that the benchmark captures generalizable
VLM capabilities rather than task-specific idiosyncrasies. Models
that excel at temporal reasoning, visual detail extraction, and nar-
rative coherence maintain their advantage across both scenarios,
while those exhibiting hallucination tendencies or length-control
failures show consistent weaknesses.
C
Scalability and Robustness of Automated
Evaluation
C.1
Embedding-Ensemble Methodology
The evaluation framework employs an ensemble of five state-of-
the-art text embedding judges (KaLM, GTE-Qwen2-7B, NV-Embed,
NeMo, Qwen3-8B) to compute semantic similarity between VLM-
generated descriptions and reference annotations. This multi-model
approach mitigates individual model biases and provides cross-
validation across diverse embedding architectures. The Borda count
aggregation consolidates rankings from all five judges, ensuring
that final VLM assessments reflect consensus rather than the id-
iosyncratic preferences of any single judge.
As demonstrated in the two exhibits above, different judges ex-
hibit varying sensitivities to description characteristics. Whereas
KaLM consistently assigns higher absolute HM-CF scores and NV-
Embed shows greater sensitivity to length mismatches, their relative
rankings of VLMs remain remarkably consistent. This convergence
supports the internal consistency of the ensemble: despite differen-
tial absolute scoring, the fundamental ordering of VLM capabilities
emerges stably across all judges.


## Page 18


EvalMG @SIGIR ’26, July 24, 2026, Melbourne, VIC, Australia
Ali et al.
C.2
Fine-Grained vs. Coarse-Grained Gap
The per-judge similarity scores reveal that current VLMs predom-
inantly capture coarse-grained narrative structure rather than
fine-grained visual detail. The disparity between coarse-grained
paragraph-level cosine (typically 0.65–0.85) and fine-grained
sentence-level precision/recall (often 0.45–0.70) suggests that
models successfully grasp overall scene context, character
interactions, and temporal flow, but struggle with precise object
attributes, spatial relationships, and subtle action sequences.
This observation motivates the use of the harmonic-mean
HM-CF𝑗, which balances both granularities and ensures that
evaluation rewards holistic understanding while penalizing
omission of critical details. The harmonic-mean formulation
prevents models from gaming either dimension alone: a VLM
cannot achieve a high HM-CF through vague generalities (which
would score well on coarse-grained metrics alone) nor through
disconnected detail enumeration (which might inflate fine-grained
scores without narrative coherence).
C.3
Practical Considerations for Long-Form
Evaluation
Traditional human evaluation protocols, while valuable for short-
answer tasks, become prohibitively expensive for dense paragraph-
level video descriptions. The benchmark comprises 200 videos, each
paired with 17 VLM-generated descriptions averaging 800–2 000
characters (mean of 402 words per reference). Rigorous human as-
sessment would require annotators to watch each 90 s clip multiple
times while comparing detailed textual descriptions, demanding
thousands of annotation hours for comprehensive inter-annotator-
agreement studies.
Moreover, human judgment of semantic equivalence in long-
form text introduces substantial subjectivity. Unlike discrete classifi-
cation tasks, where agreement can be cleanly measured, paragraph-
level description evaluation involves nuanced trade-offs between
verbosity, detail granularity, and narrative structure — dimensions
where annotator preferences vary considerably. Our automated
embedding-based approach provides deterministic, reproducible
scores that enable large-scale benchmarking while maintaining
evaluation consistency across the entire dataset.
D
Dataset Topical Distribution
Table 10 reports the full distribution of the 200 clips by primary
narrative type, complementing the source- and topical-diversity
statistics summarized in table 1.
E
GPT-4o Cleanup Prompt
For reproducibility, each transcribed narration was cleaned with
the following GPT-4o prompt. It corrects grammar and disfluencies
only, preserves all content and event order, introduces no proper
nouns, emits no conversational framing, and returns the result as a
JSON object.
You are a copy editor. The input is a verbatim tran-
scription of a person narrating a video aloud. Clean it
into fluent written English. Rules: (1) Fix only gram-
mar, punctuation, spelling, and spoken disfluencies
Table 10: Distribution of the 200 clips by primary narrative
type.
Narrative type
Clips
Share
Dialogue/Drama
104
52.0%
Violence/Combat
26
13.0%
Action/Chase
23
11.5%
Public/Social
23
11.5%
Medical/Procedural
8
4.0%
Dramatic Confrontation
8
4.0%
Crime/Investigation
4
2.0%
Family/Domestic
2
1.0%
Suspense/Thriller
1
0.5%
Romance/Intimate
1
0.5%
(e.g., “um”, “uh”, false starts, repetitions). (2) Do not
add, remove, reorder, or alter any described content,
visual detail, or event. (3) Do not introduce proper
nouns—no names of people, characters, actors, places,
brands, or titles; keep descriptive references (e.g., “a
man in a black jacket”). (4) Preserve the original se-
quence of events. (5) Do not add any conversational
preamble or closing remarks (e.g., “Here is the cleaned
description”); output nothing that is not a cleaned ver-
sion of the input. (6) Write plain prose only—no bullet
points, numbered lists, or headings. (7) Return the re-
sult strictly as a single JSON object whose only field,
summary, holds the cleaned description, with no text
outside the JSON.
