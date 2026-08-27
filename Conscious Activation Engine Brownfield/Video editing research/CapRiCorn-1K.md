# CapRiCorn-1K

*Source PDF: `CapRiCorn-1K.pdf`*

*Total Pages: 22*

---


## Page 1


CapRiCorn-1K: A Comprehensive Benchmark for Video Captioning
and Subject Referential Consistency Across Temporal Scales
Xinlong Chen1,2,3*, Jiafu Tang4, Yue Ding1,2, Yizhuo Jia5, Bozhou Li6, Bohan Zeng6,
Yang Shi6, Shihao Li4, Yiyan Ji4, Qiang Liu1,2†, Weihong Lin3, Yuanxing Zhang3,
Pengfei Wan3, Liang Wang1,2, Tieniu Tan1,2,4
1NLPR, CASIA
2UCAS
3Kling Team
4NJU
5FDU
6PKU
Abstract
Accurate and comprehensive video captions
with consistent subject references are criti-
cal for downstream understanding and genera-
tion tasks. However, few existing benchmarks
can objectively and comprehensively evaluate
these properties across diverse durations and
scenarios, thereby hindering the advancement
of video captioning models. To bridge this
gap, we propose CapRiCorn-1K, a compre-
hensive benchmark designed to evaluate both
video captioning quality and subject referen-
tial consistency across long temporal horizons
and diverse video domains. To accommodate
varied evaluation needs, our benchmark sup-
ports both audiovisual and visual-only settings.
Extensive experiments on CapRiCorn-1K re-
veal that current models generally struggle to
generate accurate and comprehensive captions
while maintaining consistent subject references.
Moreover, as video duration increases, both
the overall caption quality and subject referen-
tial consistency decline. Notably, our evalua-
tion metrics exhibit strong correlations with
the performance of downstream understand-
ing and generation tasks conditioned on the
generated captions, further validating their ef-
fectiveness. The project is available at https:
//github.com/xlchen0205/CapRiCorn-1K.
1
Introduction
With the rapid advancement of Multimodal Large
Language Models (MLLMs), video captioning has
evolved from a basic descriptive task into a core
semantic interface that bridges multimodal percep-
tion with linguistic semantics (Chen et al., 2025a;
Tang et al., 2025; Li et al., 2026). High-quality
video captions not only facilitate the effective align-
ment of audio, visual, and textual modalities during
pre-training (Xu et al., 2025b; Team et al., 2025),
*This work was conducted during the author’s internship
at Kling Team, Kuaishou Technology
†Corresponding author: qiang.liu@nlpr.ia.ac.cn
but also inject crucial semantic knowledge into
downstream multimodal understanding and gen-
eration tasks (Long et al., 2025; Du et al., 2025;
Shi et al., 2025; Hua et al., 2026). Extensive re-
search has demonstrated that enhancing the qual-
ity of video captions yields stable and significant
performance gains across a wide range of applica-
tions (Team, 2026b; Chen et al., 2024; Wang et al.,
2025b; An et al., 2025; Ding et al., 2026).
Despite the broad utility of video captioning,
current mainstream evaluation benchmarks (Wang
et al., 2024; Chai et al., 2024; Tang et al., 2025)
generally suffer from limitations such as (1) re-
stricted video durations; (2) homogeneous content
genres; and (3) a lack of scene transitions. The first
two constraints prevent existing benchmarks from
comprehensively and objectively assessing mod-
els’ captioning capabilities across varying temporal
scales and dynamic real-world environments. Fur-
thermore, the absence of scene changes obscures a
critical challenge: maintaining consistent subject
references throughout the generated captions, a dif-
ficulty significantly amplified by dynamic scene
transitions. As illustrated in Figure 1, ambiguous
or inconsistent references to the same subject can
severely mislead downstream understanding and
generation tasks, such as causing reasoning failure
when used as the memory of an LLM agent, or
leading to subject collapse during video reconstruc-
tion. Consequently, strong performance on exist-
ing benchmarks often fails to translate into robust
real-world capabilities, hindering researchers from
accurately identifying true performance boundaries
and conducting targeted optimizations.
To better reflect real-world model performance,
an ideal video captioning benchmark should satisfy
several essential criteria. At the data level, it should
include videos featuring extended temporal spans,
diverse domains, and dynamic scene transitions
that mirror realistic visual complexity. At the evalu-
ation level, beyond overall caption quality, it should
arXiv:2606.21949v1  [cs.CV]  20 Jun 2026


## Page 2


Caption as memory
LLM-Agent
Question: Does the man initially 
wearing a striped shirt success-
fully hunt any quail?
Thinking: Initially, a man in a striped shirt agrees to join a quail hunt. However, 
when the scene shifts to the forest, only a few hunters dressed in hunting attire are
mentioned, with no further reference to him again…
Answer: Unable to determine.
<man_1>: Everything's ready for the quail hunt!
<man_1> 
<man_2> 
<man_3> 
<man_2> 
<man_3> 
<man_1> 
<man_3>: … But let's go kill some birds. I'm psyched.
<man_2>: … See you later.
<man_3>: … why do I have to be in camouflage so the quail doesn't see me?
Input Video
Baseline Caption
A man in a striped shirt and a woman in a white knit top and headscarf lead the group, engaging in lively conversation… Another individual, sporting a 
bright orange hunting vest and holding a shotgun, stands out with a playful demeanor… (missing <man_3>) … The setting shifts to a wooded area, where two men dressed in 
hunting attire walk through a dense forest… The sequence ends with a close-up of one of the hunters holding a shotgun, appears to be searching the surroundings…
For Understanding
For Generation
Caption for reconstruction
Video Generator
Original video
* indicates subject collapse in the generated videos caused by inconsistent 
or ambiguous references of the same subject within the caption.
<man_2> 
<man_1> 
<man_2*> 
<man_1*> 
<man_1*> 
Original video
Leads to
reasoning failure
Referential
consistency lost!
Leads to
subject collapse
Figure 1: The impact of ambiguous or inconsistent subject references. In the latter half of the baseline caption, the
model fails to maintain consistent references to the previously mentioned subject (underlined). Such referential
inconsistency degrades downstream performance, leading to reasoning failure when the caption serves as memory
for LLM agents in understanding tasks, and causing subject collapse during video reconstruction in generation tasks.
also focus on subject referential consistency, which
is particularly challenged by these scene transitions.
Additionally, given that video captioning models
are commonly developed under either audiovisual
or visual-only assumptions, a more comprehensive
benchmark should be modality-flexible to support
evaluations across both settings.
Motivated by these considerations, we intro-
duce CapRiCorn-1K, the first benchmark dedi-
cated to evaluating video Captioning and subject
Referential Consistency across long temporal hori-
zons and diverse video scenarios.
As detailed
in Table 1, CapRiCorn-1K comprises 1,000 man-
ually collected videos featuring dynamic scene
transitions. In addition to evaluating overall cap-
tion quality, we further introduce a novel met-
ric to quantitatively measure subject referential
consistency within generated captions. Further-
more, CapRiCorn-1K supports unified evaluation
under both audiovisual (default) and visual-only
(CapRiCorn-1K-V) settings.
Extensive experiments on CapRiCorn-1K reveal
that current models fall short of generating accu-
rate and comprehensive captions while maintain-
ing consistent subject references. Notably, the per-
formance of open-source models degrades signif-
icantly as video duration scales up. To validate
the reliability of our benchmark, we employ these
captions both as memory for LLM-based agents
and as intermediate representations for video recon-
struction. Experimental results demonstrate that
caption quality evaluated on CapRiCorn-1K cor-
relates strongly with performance in downstream
understanding and generation tasks.
Our contributions are summarized as follows:
• We introduce CapRiCorn-1K, the first benchmark
designed to evaluate video captioning and subject
referential consistency across extended temporal
horizons, diverse domains, and dynamic scene
transitions, enabling a more faithful and compre-
hensive assessment of captioning performance
under both audiovisual and visual-only settings.
• Through extensive experiments, we demonstrate
that existing models generally struggle to gener-
ate accurate and comprehensive captions while
maintaining consistent subject references. As
video duration increases, both overall caption
quality and subject referential consistency exhibit
a noticeable decline among open-source models.
• By leveraging captions as memory for LLM-
based agents and as intermediate representations
for video reconstruction, we show that caption
quality, as evaluated on CapRiCorn-1K, strongly
correlates with downstream performance in both
understanding and generation tasks.


## Page 3


Benchmark
Modality
# Videos
Video Duration
Diverse
Sources
Newly
Collected
Scene
Trans.
Sbj. Ref.
Consist.
Min.
Avg.
Max.
DREAM-1K (Wang et al., 2024)
V
1,000
1 s
9 s
49 s
✓
✗
✗
✗
VDC (Chai et al., 2024)
V
1,027
8 s
28 s
163 s
✓
✗
✗
✗
CaReBench (Xu et al., 2024)
V
1,000
1 s
14 s
124 s
✓
✗
✗
✗
VidCapBench (Chen et al., 2025c)
V
643
4 s
10 s
14 s
✓
Partial
✗
✗
SALMONN-2 testset (Tang et al., 2025)
A + V
483
31 s
51 s
60 s
✗
Unknown
Partial
✗
UGC-VideoCap (Wu et al., 2025)
A + V
1,000
8 s
24 s
60 s
✗
✓
✗
✗
Omni-Cloze (Ma et al., 2025)
A + V
2,320
0 s
34 s
60 s
✓
✗
✗
✗
CapRiCorn-1K (Ours)
V / (A+V)
1,000
15 s
252 s
600 s
✓
✓
✓
✓
Table 1: Comparison with widely-used video captioning benchmarks. Key dimensions include: evaluation modality
(Modality, “A” for audio and “V” for visual); total number of videos (# Videos); video duration statistics (Min.,
Avg., Max.); diversity of video sources (Diverse Sources); whether the videos are independently collected rather
than sampled from existing public datasets (Newly Collected); the presence of scene transitions in most videos
(Scene Trans.); and the assessment of subject referential consistency in captions (Sbj. Ref. Consist.).
2
Related Work
2.1
Audiovisual Video Captioning
The rapid advancement of audiovisual understand-
ing models (Cheng et al., 2024; Hou et al., 2024;
Panagopoulou et al., 2023; Shu et al., 2025; Sun
et al., 2024; Ye et al., 2024) has catalyzed remark-
able progress in audiovisual video captioning. Re-
cent efforts have explored various complementary
directions: video-SALMONN-2 (Tang et al., 2025),
UGC-VideoCaptioner (Wu et al., 2025), and Omni-
Captioner (Ma et al., 2025) prioritize audiovisual
information comprehensiveness; AVoCaDO (Chen
et al., 2025a) focuses on temporal coherence across
audiovisual streams; DiaDem (Chen et al., 2026)
and D-ORCA (Tang et al., 2026) emphasize the
fidelity of dialogue descriptions; StoryTeller (He
et al., 2024) incorporates movie cast lists as aux-
iliary inputs to link dialogue with characters; and
several recent studies (Li et al., 2026; Yao et al.,
2026; Geng et al., 2025; Team, 2026b; Pu et al.,
2026) explore structured, time-aware captioning.
Despite model-level advancements, current eval-
uation benchmarks lag behind, failing to adequately
capture real-world complexity. As detailed in Ta-
ble 1, most existing benchmarks are restricted by
limited video durations, narrow domain diversity,
and a lack of scene transitions. Such limitations
hinder reliable evaluation in dynamic real-world
scenarios, thereby impeding the iterations of cap-
tioning models toward practical deployment. To
bridge this gap, we introduce CapRiCorn-1K, a
comprehensive benchmark designed to evaluate
video captioning over extended temporal horizons,
diverse video domains, and rich scene transitions.
2.2
Visual-Only Video Captioning
In the visual-only domain, most existing works (Hu
et al., 2024; Xue et al., 2025; Chen et al., 2025b)
have primarily focused on short-video captioning.
OwlCap (Zhong et al., 2026) and the Tarsier se-
ries (Wang et al., 2024; Yuan et al., 2025) construct
large-scale, high-quality datasets to enable the gen-
eration of detailed captions that effectively balance
dynamic motion and static visual details. Aurora-
Cap (Chai et al., 2024) reduces the input sequence
length through token merging while maintaining
caption quality.
Regarding long-video captioning, existing works
primarily adopt a bottom-up paradigm (Islam et al.,
2024; Wei et al., 2025; Chu et al., 2025), where
videos are first segmented into shorter clips for lo-
calized captioning before global aggregation. On
the evaluation side, LongCaption-Bench (Wei et al.,
2025) pioneers the assessment of detailed long-
video captioning by measuring caption length, over-
all quality, and video-caption relevance. Subse-
quently, RICE-Benchmark (Yang et al., 2025b) ex-
plores the evaluation of identity-matching. How-
ever, it only annotates 30 frame indices for subjects
in a long video, and such coarse-grained annota-
tions may lead to artificially inflated recall and
underestimated precision. In addition, both bench-
marks rely on direct LLM-based scoring for cap-
tion quality evaluation, which offers limited inter-
pretability. Furthermore, neither benchmark has
been open-sourced, restricting their utility in guid-
ing the iterations of long-video captioning models.
In contrast, CapRiCorn-1K provides a fine-grained
evaluation framework that jointly measures caption
quality and subject referential consistency based


## Page 4


on video keypoints. Crucially, CapRiCorn-1K will
be fully open-sourced to facilitate future research.
3
CapRiCorn-1K
3.1
Overview
As a benchmark tailored for evaluating video cap-
tioning over extended temporal spans, CapRiCorn-
1K aims to comprehensively assess both the overall
caption quality and the referential consistency of
recurring subjects across diverse video scenarios.
In this section, we detail the evaluation protocols,
video collection criteria, annotation methodology,
and statistical characteristics of CapRiCorn-1K.
3.2
Evaluation Protocols
Inspired by the video-SALMONN-2 testset (Tang
et al., 2025), we first decompose each video into a
sequence of categorized keypoints. A judge model
(GPT-4.1) is then employed to verify the mention
status of each keypoint within the generated cap-
tion, thereby evaluating the overall captioning qual-
ity. Furthermore, to assess the model’s ability to
maintain referential consistency for the same sub-
ject over long contexts, we utilize these keypoints
as anchors to extract corresponding subject descrip-
tions from the caption. The judge model then deter-
mines whether the descriptions associated with the
same ground-truth subject remain referentially con-
sistent within the caption context, thereby deriving
a subject referential consistency score. The com-
plete evaluation pipeline is illustrated in Figure 2,
with formal definitions provided below.
3.2.1
Overall Captioning Quality
For a given video, we first manually identify a set
of ground-truth subjects S = {s1, s2, . . . , sm} and
partition the video into a set of keypoints K =
{k1, k2, . . . , kn}. As detailed in Section 3.4, these
keypoints are classified into five categories: inter-
subject interaction (Kinter), independent subject
events (Kindep), background details (Kbg), transi-
tions (Ktrans), and non-subject information (Knon).
The judge model evaluates the overall caption-
ing quality by assigning a discrete mention status
yi ∈{correct, partial, none} to each keypoint ki,
corresponding to “correctly mentioned”, “partially
mentioned or containing errors”, and “not men-
tioned”. Let Kcorrect = {ki ∈K | yi = correct}
and Kpartial = {ki ∈K | yi = partial}, we define
Accuracy (Acc) and Coverage (Cov) to measure
the overall caption quality as follows:
Acc = |Kcorrect|
|K|
,
Cov = |Kcorrect| + |Kpartial|
|K|
.
(1)
3.2.2
Subject Referential Consistency
To assess the referential consistency for a specific
subject sj, we utilize keypoints as anchors to ex-
tract subject descriptions from the caption, and
subsequently determine whether these descriptions
co-refer to the same subject contextually. Formally,
let Ksj ⊆Kinter ∪Kindep denote the set of subject-
related keypoints associated with sj.
For each
keypoint ki ∈Ksj that has been judged as cor-
rectly or partially mentioned (i.e., with mention
status yi ∈{correct, partial}), the judge model
extracts the corresponding localized subject de-
scription from the caption. This yields a set of
caption-derived subject descriptions belonging to
sj, denoted as Dsj = {dj,1, dj,2, . . . , dj,Nj}.
Notably, a subject’s appearance (e.g., cloth-
ing) may vary across different scenes. Therefore,
evaluating referential consistency relying solely
on the isolated semantics of the descriptions in
Dsj is inadequate. Considering that continuous
subject tracking requires the caption to explicitly
document these appearance variations, the judge
model is instructed to perform co-reference clus-
tering on Dsj based on the caption context, re-
sulting in disjoint co-reference partitions Psj =
{Pj,1, Pj,2, . . . , Pj,Cj}.
A naive approach to quantifying subject referen-
tial consistency is to rely on the number of clusters,
|Psj|, where more clusters indicate lower consis-
tency. However, this could introduce bias by ig-
noring the size distribution among clusters. For in-
stance, given |Dsj| = 6, a cluster size distribution
of {1, 1, 4} inherently reflects higher consistency
than {1, 2, 3}, despite both yielding |Psj| = 3.
To mitigate this bias, we draw inspiration from
the Rand Index (Rand, 1971) and define the subject-
level referential consistency score (Refj) as the
ratio between: (i) the number of pairwise combi-
nations of subject descriptions in Dsj that belong
to the same cluster, and (ii) the total number of
pairwise combinations among all keypoints in Ksj.
Crucially, by utilizing |Ksj| rather than |Dsj| in the
denominator, the metric explicitly penalizes models
that inflate consistency scores by generating overly
concise captions (i.e., where |Dsj| ≪|Ksj|). For
subjects with |Ksj| ≥2 (a condition met by all


## Page 5


<man_1>: A man with blue hair, wearing a black leather jacket over a blue shirt.
<man_2>: A man with long black hair and a beard, wearing a long black coat.
<woman_1>: A woman initially wearing blue medical scrubs, later a black top.
<man_3>: An older, balding man wearing glasses and a black priest's outfit.
Inter-Subject Interaction: Seated in a dental chair, the man with long 
hair (<man_2>) talks to the woman in medical scrubs (<woman_1>) 
while she uses a dental tool to examine his teeth.
Independent Subject Events: In the priest's office, the older man in 
glasses (<man_3>) leans forward, gesturing with his hands as he 
expresses his frustration about his declining influence.
Background Details: The priest's office is cluttered with books, papers, 
and religious artifacts, with a large window letting in natural light.
Main Subjects
Transitions: The video transitions from the perspective of watching 
in front of the TV to the television broadcast itself, featuring a female 
presenter in a red dress.
Non-Subject Information: A television presenter in a bright red dress 
stands on a studio set, introducing strange news stories about a 
helpful dog and an angel ordering from a restaurant.
Subject-Related Keypoints
Other Keypoints
Metrics for Overall Quality:
Acc & Cov
Metrics for Referential 
Consistency: Ref
Description clustering
within each subject
For (partially) correct 
subject-related 
keypoints
Judge Model with 
Video Caption
Step 1: Keypoint-Based 
Caption Quality Assessment
Calculate metrics
Calculate metrics
Step 2: Referential
Consistency Evaluation
Mention Status of Keypoints
Keypoint-1
Correct
Keypoint-2
Partially Correct
Keypoint-3
Not Mentioned
…
…
Subject Description in Caption
<man_1>
[desc_1, desc_2, …]
<man_2>
[desc_1, desc_2, …]
…
…
<man_1>
[(desc_1, desc_3, desc_4), 
(desc_2, desc_5), …]
…
…
Figure 2: Evaluation pipeline of CapRiCorn-1K: (1) determining the mention status of all keypoints to assess overall
caption quality (Acc & Cov); and (2) extracting the localized subject descriptions from the caption for all mentioned
subject-related keypoints, which are then clustered to assess referential consistency (Ref).
subjects in CapRiCorn-1K), Refj is formulated as:
Refj =
P|Psj |
c=1
 |Pj,c|
2

 |Ksj |
2

,
(2)
where |Pj,c| denotes the number of descriptions
within the c-th cluster. Finally, the video-level ref-
erential consistency score (Ref) is computed by
averaging across all subjects:
Ref = 1
|S|
X
sj∈S
Refj.
(3)
3.3
Video Collection
Unlike many existing benchmarks that sample eval-
uation subsets from established datasets, we manu-
ally collect and process videos from the Internet.
To enable a more comprehensive assessment of
video captioning performance across diverse sce-
narios, CapRiCorn-1K is carefully curated to cover
extended and balanced temporal spans, as well as
a wide variety of video content. Regarding video
duration, we substantially broaden the temporal
scope compared with mainstream benchmarks, se-
lecting videos ranging from 15 seconds to 10 min-
utes. Videos shorter than 15 seconds are excluded
because they typically contain limited dynamics. In
terms of content diversity, we collect videos from
eight major categories to ensure broad domain cov-
erage: Relationship, Youth, Entertainment, History,
Family, Lifestyle, Fantasy, and Mystery. Each ma-
jor category is further divided into multiple fine-
grained subcategories, as detailed in Table 5.
Furthermore, to better reflect real-world dynam-
ics and to more rigorously evaluate referential con-
sistency for the same subject over time, each video
is required to contain at least one scene transition,
rather than merely camera-shot changes within a
single scene. This criterion forces models to rely
on genuine, identity-related visual cues rather than
relative spatial positioning to track subjects. To
introduce an additional layer of complexity, ap-
proximately 40% of the collected videos feature
subjects undergoing clothing changes.
Finally, we impose additional requirements such
as video resolution to guarantee video quality.
More details are provided in Appendix A.
3.4
Data Annotation
Following video collection, we conduct rigorous
manual annotation. Compared to automated anno-
tation, whose scope and accuracy are inherently
limited by the capabilities of the underlying model,
manual annotation better reflects real-world re-


## Page 6


quirements and yields more reliable ground truth.
To support the evaluation of subject referential
consistency in video captioning, we first identify
the primary subjects within each video. A subject
is defined as a character who actively drives the
storyline and significantly contributes to the nar-
rative progression. Two annotators independently
identify the subjects and cross-validate their results,
with discrepancies resolved by a senior annotator.
Subsequently, we annotate keypoints across five
categories to comprehensively evaluate overall cap-
tion quality and subject referential consistency:
• Inter-Subject Interactions: Interactions among
multiple subjects;
• Independent Subject Events: Actions or events
performed by a single subject;
• Background Details: Contextual information
such as visual background elements, ambient
sounds, and other environmental cues;
• Transitions: Scene transitions, camera shifts,
and environmental changes;
• Non-Subject Information: Salient events or de-
tails not directly related to the primary subjects.
To balance annotation granularity with evalua-
tion cost, three annotators independently identify
approximately 40 salient keypoints per video. Two
senior annotators then each review the three anno-
tation sets and select keypoints exhibiting high con-
sensus and critical narrative importance. Finally,
a lead expert consolidates and verifies these two
refined sets to form the final keypoint collection.
Furthermore, to cater to visual-only captioning
models, two additional annotators filter and cross-
validate this final collection to derive a vision-only
keypoint subset, denoted as CapRiCorn-1K-V. Dis-
agreements during this stage are likewise resolved
by a senior annotator. Detailed information regard-
ing the annotators is provided in Appendix B.
3.5
Benchmark Statistics
As shown in Table 1 and Figure 3, CapRiCorn-
1K comprises 1,000 newly collected videos evenly
distributed across eight major categories. Video
durations range uniformly from 15 to 600 seconds,
yielding an average length of 252 seconds. No-
tably, each video features an average of 3.1 scene
transitions, with the transition density scaling with
video duration, reflecting the high dynamics of our
benchmark. In terms of annotations, each video is
meticulously labeled with an average of 4.4 sub-
Video Durations (s)
60
15
120
240
360
480
600
Number of Videos
Scene Transitions (avg)
(b) Distributions of Video Duration and Scene Transitions
(a) Video Categories
Mystery
83
Relationship
145
Youth
82
Entertainment
172
History
170
Family
186
Lifestyle
72
Fantasy
90
Deduction
Crime
Romance
Friendship
Professional
Campus
Growth
Sketch
Sports
Variety
Drama
Culture
Politics
Military
Society
Support
Conflict
Bonding
Leisure
Nature
Adventure
Sci-Fi
Urban
Figure 3: Statistics of CapRiCorn-1K: (a) Diverse cate-
gory distribution; and (b) Balanced duration distribution
with rich scene transitions.
jects, 21.5 salient subject-related keypoints, and
14.9 salient keypoints of other types.
4
Experiments
Our evaluation adheres to the official protocols of
each model by default. When such protocols are un-
available, given the substantial length of the videos,
we uniformly sample frames up to the maximum
context window supported by the model while pre-
serving sufficient frame resolution. More imple-
mentation details are provided in Appendix D.
4.1
Captioning Models
For the default audiovisual setting (CapRiCorn-
1K), we assess the Gemini series (Comanici
et al., 2025), Qwen-Omni series (Xu et al.,
2025a,b),
video-SALMONN-2
series
(Tang
et al., 2025),
ARC-Qwen-Video (Ge et al.,
2025),
OmniVinci (Ye et al., 2025),
UGC-
VideoCaptioner (Wu et al., 2025), AVoCaDO (Chen
et al., 2025a), DiaDem (Chen et al., 2026), and
ASID-Captioner (Li et al., 2026).
For the visual-only setting (CapRiCorn-1K-V),
we evaluate Tarsier2 (Yuan et al., 2025), MiMo-
VL (Xiaomi, 2025), Qwen3-VL (Bai et al., 2025),
InternVL3.5 (Wang et al., 2025a), Qwen3.5 (Team,


## Page 7


Model
Size
Overall
(0, 2] min
(2, 5] min
(5, 8] min
(8, 10] min
Acc
Cov
Ref
Acc
Cov
Ref
Acc
Cov
Ref
Acc
Cov
Ref
Acc
Cov
Ref
Gemini-3.1-Pro
-
42.5
53.3
39.1
40.9
53.4
42.4
44.7
54.8
40.4
42.4
52.7
35.3
42.2
51.6
35.4
Gemini-3-Flash
-
41.5
52.8
39.6
42.8
55.9
46.3
42.1
52.9
38.1
41.1
51.3
36.6
38.5
48.3
32.3
Qwen2.5-Omni
3B
4.1
11.6
0.5
5.8
15.9
1.2
4.1
11.5
0.2
2.6
8.4
0.1
2.3
7.1
0.1
video-SALMONN-2+
3B
9.4
19.0
1.1
11.8
23.5
1.9
9.1
18.1
0.8
8.1
16.8
0.6
6.5
14.1
0.4
UGC-VideoCaptioner
3B
11.8
21.8
3.6
17.4
30.6
7.4
11.0
20.1
2.1
8.3
17.0
1.4
6.5
13.2
0.9
ASID-Captioner
3B
12.8
23.2
7.0
21.7
37.2
14.9
11.9
21.3
5.2
6.3
13.9
1.7
4.5
9.8
0.7
ARC-Qwen-Video-Narrator
7B
2.3
3.2
0.6
4.6
6.7
1.5
1.5
0.2
0.2
1.0
1.2
0.1
0.6
0.8
0.0
Qwen2.5-Omni
7B
5.1
13.2
0.6
6.7
17.4
1.2
5.9
13.7
0.5
3.4
10.0
0.3
2.6
8.5
0.1
OmniVinci
9B
5.9
13.3
1.2
9.9
21.2
2.5
5.3
12.0
0.6
3.2
8.3
0.4
2.5
6.2
0.5
ARC-Qwen-Video
7B
6.9
10.9
2.0
9.2
15.3
3.4
7.2
11.0
1.8
5.8
9.0
1.4
2.8
4.4
0.4
video-SALMONN-2+
7B
9.3
18.7
1.4
12.1
24.0
2.3
9.1
17.5
1.0
7.2
15.6
0.6
6.7
13.8
1.0
ASID-Captioner
7B
18.9
31.1
12.9
30.2
47.3
26.3
18.6
30.4
10.3
10.5
19.3
3.8
7.7
14.9
1.9
video-SALMONN-2
7B
22.5
37.6
11.3
27.6
46.0
18.2
23.2
37.6
10.6
19.9
33.2
7.1
14.3
26.2
4.0
DiaDem
7B
24.6
35.8
14.5
40.0
54.7
31.3
23.1
33.2
10.2
13.6
23.0
3.3
10.3
18.3
2.0
AVoCaDO
7B
28.8
41.9
18.4
43.7
60.6
36.6
29.8
42.4
15.8
17.0
27.5
5.2
12.9
22.3
3.1
Qwen3-Omni-Instruct
30B-A3B
10.3
20.2
1.6
13.3
24.6
2.5
10.6
20.3
1.6
8.0
17.6
0.9
6.5
14.5
0.7
Qwen3-Omni-Captioner
30B-A3B
14.3
27.5
4.1
18.1
33.5
7.0
14.4
27.4
3.4
11.4
23.0
2.3
10.2
21.4
1.9
video-SALMONN-2+
72B
11.5
21.5
1.9
14.6
26.8
3.0
10.9
20.1
1.4
9.6
18.8
1.3
8.6
16.5
1.1
Table 2: Evaluation results of audiovisual captioning models on CapRiCorn-1K.
Model
Size
Overall
(0, 2] min
(2, 5] min
(5, 8] min
(8, 10] min
Acc
Cov
Ref
Acc
Cov
Ref
Acc
Cov
Ref
Acc
Cov
Ref
Acc
Cov
Ref
Tarsier2
7B
7.5
18.8
4.6
9.2
23.6
7.0
7.5
18.7
4.3
6.8
15.9
3.6
5.1
12.9
1.8
MiMo-VL
7B
11.7
23.7
1.5
15.6
30.2
2.8
11.9
24.4
1.4
9.6
19.9
0.5
6.2
14.6
0.3
Qwen3.5
9B
10.7
24.7
3.1
15.2
31.9
6.3
10.5
25.0
2.5
7.3
19.2
1.4
6.2
16.5
0.2
InternVL3.5
8B
13.2
28.2
5.4
18.4
35.3
9.8
12.4
27.8
4.1
10.1
23.3
3.0
8.3
20.7
1.7
Qwen3-VL
8B
15.8
30.2
5.1
23.3
40.6
10.8
14.3
28.7
3.0
11.2
23.7
1.9
9.0
20.1
1.1
Qwen3.6
27B
13.4
27.8
3.1
19.0
36.5
6.7
12.3
26.9
1.8
9.9
22.1
1.1
8.1
19.0
0.8
Qwen3.6
35B-A3B
11.7
25.8
2.9
16.2
32.6
5.2
11.1
25.5
2.6
8.6
21.5
1.1
7.8
18.3
1.1
Qwen3.5
122B-A10B
11.7
25.6
2.6
15.2
31.9
5.2
12.1
25.6
1.7
9.0
21.1
1.2
7.7
18.6
0.5
Table 3: Evaluation results of visual-only captioning models on CapRiCorn-1K-V.
2026a), and Qwen3.6 (Qwen Team, 2026a,b).
4.2
Main Results
Tables 2 and 3 present the performance of various
audiovisual captioning models on CapRiCorn-1K
and vision-only captioning models on CapRiCorn-
1K-V, respectively. Our key findings are as follows:
• Performance Gap and Long-Video Robust-
ness.
Existing models generally struggle to
generate accurate and comprehensive captions
with consistent subject references. Overall, the
closed-source Gemini series consistently outper-
forms open-source models by a large margin,
and its captioning performance only degrades
marginally as video duration increases. In con-
trast, open-source models exhibit severe perfor-
mance drops on longer videos, particularly in
maintaining referential consistency.
• Limitations of Existing Benchmarks. While
certain specialized open-source models (e.g., AV-
oCaDO and DiaDem) achieve overall captioning
quality comparable to the Gemini series on short
videos (0 to 2 minutes), they lag substantially
behind in terms of subject referential consistency
and long-video robustness. One possible reason
is that these models are primarily optimized for
existing benchmarks, which mainly emphasize
overall caption quality on short videos, thereby
overlooking long-duration videos and subject ref-
erential consistency, both of which are more crit-
ical in real-world applications.
• Captioning Performance Depends on Multiple
Factors. Although increasing parameter scale
yields performance gains within specific model
families (e.g., Qwen2.5-Omni, Qwen3.5, and
video-SALMONN-2+), larger model size alone
does not guarantee superior performance. For in-
stance, despite having only 7B parameters, AVo-
CaDO substantially outperforms the 72B version
of video-SALMONN-2+. This highlights that
captioning capability is also influenced by other
critical components, such as architectural design,


## Page 8


Model
GPT-4.1
Qwen3-235B-A22B
Acc
Cov
Ref
Acc
Cov
Ref
Gemini-3.1-Pro
42.5
53.3
39.1
27.2
51.6
35.4
Qwen2.5-Omni
5.1
13.2
0.6
5.3
16.8
1.3
Qwen3-Omni-Captioner
14.3
27.5
4.1
10.7
29.1
4.7
ASID-Captioner-7B
18.9
31.1
12.9
12.7
30.4
13.0
AVoCaDO
28.8
41.9
18.4
18.9
41.7
18.9
Table 4: Ablation on the judge model.
training data distribution and optimization strate-
gies, rather than parameter scale alone.
4.3
Ablation on the Judge Model
In the main experiments, we adopt GPT-4.1 as
the judge model. To account for scenarios where
closed-source APIs are unavailable, and to further
assess the generalizability of our evaluation proto-
col across different judge models, we conduct an
ablation study by replacing GPT-4.1 with the open-
source Qwen3-235B-A22B-Instruct (Yang et al.,
2025a). The results are reported in Table 4.
The experimental results reveal that, although
the absolute scores produced by different judge
models exhibit fluctuations, which may stem from
inherent model-specific biases (e.g., Qwen3-235B-
A22B-Instruct tending to be more conservative on
Accuracy), the relative rankings among the eval-
uated models remain largely consistent. Specifi-
cally, the Pearson correlation coefficients (Benesty
et al., 2009) between the scores produced by dif-
ferent judge models across the three evaluation
metrics reach 0.999, 0.998, and 0.998, respectively
(p < 0.001), indicating that our evaluation proto-
col is not strictly dependent on a specific judge
model. Instead, as long as the judge model pos-
sesses strong capabilities and can deliver stable,
fair judgments, it is suitable for integration into
CapRiCorn-1K.
4.4
Correlation with Downstream Tasks
To validate the reliability of our evaluation metrics,
we apply the generated captions to downstream
understanding and generation tasks, examining the
correlation between downstream task performance
and our metric scores in Figure 4.
For the understanding task, we adopt M3-Bench-
web (Long et al., 2025), a benchmark featuring
long videos designed to evaluate the reasoning ca-
pabilities of multimodal agents for long-term mem-
ory. Following the “Socratic Models” paradigm
used in M3-Bench-web, we first generate video
captions using different captioning models and then
10
20
30
40
50
30.0
40.0
50.0
60.0
Average Score
on M3-Bench-web
r = 0.925
0
10
20
30
40
35.0
45.0
55.0
65.0
Person Understanding
on M3-Bench-web
r = 0.995
10
20
30
40
50
(Acc + Cov) / 2
2.0
2.5
3.0
3.5
4.0
Similarity to
Original Video
r = 0.987
0
10
20
30
40
Ref
2.0
2.5
3.0
3.5
4.0
Subject Consistency
r = 0.987
Fit
Gemini-3.1-Pro
Qwen2.5-Omni-7B
Qwen3-Omni-Captioner
ASID-Captioner-7B
AVoCaDO
Figure 4: Correlation between evaluation metrics on
CapRiCorn-1K with downstream task performance.
supply these captions as memory to a fixed LLM
agent (GPT-4.1). Consequently, the reasoning per-
formance of this LLM agent serves as a direct in-
dicator of caption quality. As illustrated in the
upper panel of Figure 4, the overall caption quality
(measured by Acc and Cov) exhibits a strong cor-
relation with the average score of the LLM agent
on M3-Bench-web (upper left), yielding a Pearson
correlation coefficient of 0.925. Moreover, the con-
sistency of subject references within the captions
(measured by Ref) shows an even stronger corre-
lation with the “Person Understanding” subset of
M3-Bench-web (upper right), achieving a Pearson
correlation coefficient of 0.995.
For the generation task, we randomly sample 50
videos from CapRiCorn-1K and leverage captions
generated by different models to reconstruct the
original videos using LTX-2.3-22B-dev (HaCohen
et al., 2025). Human evaluators then rate both
the similarity between the generated and original
videos, as well as the subject consistency within
the generated videos, on a scale from 1 to 5. These
scores, averaged across three annotators, serve as
a reliable proxy for caption quality. The results in
the lower panel of Figure 4 demonstrate that the
overall caption quality is highly correlated with
video similarity, while the referential consistency
of subjects in the captions aligns strongly with the
subject consistency of generated videos, with both
Pearson correlation coefficients reaching 0.987.
4.5
Further Analysis
Additional investigations regarding the impacts of
caption length, input frame count, and input res-
olution, along with a detailed error analysis, are
provided in Appendix C.


## Page 9


5
Conclusion
In this paper, we present CapRiCorn-1K, a compre-
hensive benchmark designed to evaluate video cap-
tioning and subject referential consistency across
diverse durations and scenarios. To better capture
real-world complexity, we manually collect and
annotate 1,000 videos spanning long temporal hori-
zons and various domains. Furthermore, we pro-
pose a suite of evaluation metrics to assess overall
caption quality and subject referential consistency
under both audiovisual and vision-only settings. By
integrating the generated captions into downstream
understanding and generation tasks, we demon-
strate that the evaluation results on CapRiCorn-1K
exhibit strong correlations with downstream task
performance, thereby validating the reliability and
practical utility of our benchmark.
Limitations
While CapRiCorn-1K significantly extends the
video duration compared to existing video caption-
ing benchmarks, its scope remains restricted to
videos under 10 minutes. Given that current mod-
els still face considerable challenges within this
time span, we hope our benchmark serves as a
stepping stone, leaving the evaluation of longer
videos to future research. Additionally, due to
the substantial domain differences between human
and non-human subjects, coupled with the preva-
lence of human-centric content in practical applica-
tions (e.g., human-computer interaction and surveil-
lance), our study prioritizes referential consistency
in human subjects as a more critical and immedi-
ate challenge to address, leaving the exploration of
non-human subjects for future work.
Ethical Considerations
The videos in CapRiCorn-1K are collected from
publicly available online platforms. To strictly ad-
here to copyright regulations and respect intellec-
tual property rights, our benchmark will be released
under highly restrictive licensing terms, allowing
its use exclusively for academic research purposes.
References
Zhaochong An, Menglin Jia, Haonan Qiu, Zijian Zhou,
Xiaoke Huang, Zhiheng Liu, Weiming Ren, Kumara
Kahatapitiya, Ding Liu, Sen He, and 1 others. 2025.
Onestory: Coherent multi-shot video generation with
adaptive memory. arXiv preprint arXiv:2512.07802.
Shuai Bai, Yuxuan Cai, Ruizhe Chen, Keqin Chen,
Xionghui Chen, Zesen Cheng, Lianghao Deng, Wei
Ding, Chang Gao, Chunjiang Ge, and 1 others.
2025. Qwen3-vl technical report. arXiv preprint
arXiv:2511.21631.
Jacob Benesty, Jingdong Chen, Yiteng Huang, and Is-
rael Cohen. 2009. Pearson correlation coefficient.
In Noise reduction in speech processing, pages 1–4.
Springer.
Wenhao Chai, Enxin Song, Yilun Du, Chenlin Meng,
Vashisht Madhavan, Omer Bar-Tal, Jenq-Neng
Hwang, Saining Xie, and Christopher D Manning.
2024. Auroracap: Efficient, performant video de-
tailed captioning and a new benchmark.
arXiv
preprint arXiv:2410.03051.
Lin Chen, Xilin Wei, Jinsong Li, Xiaoyi Dong,
Pan Zhang, Yuhang Zang, Zehui Chen, Haodong
Duan, Bin Lin, Zhenyu Tang, and 1 others. 2024.
Sharegpt4video: Improving video understanding and
generation with better captions. Advances in Neural
Information Processing Systems, 37:19472–19495.
Xinlong Chen, Yue Ding, Weihong Lin, Jingyun
Hua, Linli Yao, Yang Shi, Bozhou Li, Yuanxing
Zhang, Qiang Liu, Pengfei Wan, and 1 others.
2025a. Avocado: An audiovisual video captioner
driven by temporal orchestration.
arXiv preprint
arXiv:2510.10395.
Xinlong Chen, Weihong Lin, Jingyun Hua, Linli Yao,
Yue Ding, Bozhou Li, Bohan Zeng, Yang Shi, Qiang
Liu, Yuanxing Zhang, and 1 others. 2026. Diadem:
Advancing dialogue descriptions in audiovisual video
captioning for multimodal large language models.
arXiv preprint arXiv:2601.19267.
Xinlong Chen, Yuanxing Zhang, Yushuo Guan, Wei-
hong Lin, Zekun Wang, Bohan Zeng, Yang Shi, Si-
han Yang, Qiang Liu, Pengfei Wan, and 1 others.
2025b. Vidbridge-r1: Bridging qa and captioning for
rl-based video understanding models with intermedi-
ate proxy tasks. arXiv preprint arXiv:2506.09079.
Xinlong Chen, Yuanxing Zhang, Chongling Rao,
Yushuo Guan, Jiaheng Liu, Fuzheng Zhang, Chengru
Song, Qiang Liu, Di Zhang, and Tieniu Tan. 2025c.
Vidcapbench: A comprehensive benchmark of video
captioning for controllable text-to-video generation.
In Findings of the Association for Computational
Linguistics: ACL 2025, pages 8543–8563.
Zesen Cheng, Sicong Leng, Hang Zhang, Yifei Xin, Xin
Li, Guanzheng Chen, Yongxin Zhu, Wenqi Zhang,
Ziyang Luo, Deli Zhao, and 1 others. 2024. Videol-
lama 2: Advancing spatial-temporal modeling and
audio understanding in video-llms. arXiv preprint
arXiv:2406.07476.
Sanghyeok Chu, Seonguk Seo, and Bohyung Han.
2025.
Fine-grained captioning of long videos
through scene graph consolidation. arXiv preprint
arXiv:2502.16427.


## Page 10


Gheorghe Comanici, Eric Bieber, Mike Schaekermann,
Ice Pasupat, Noveen Sachdeva, Inderjit Dhillon, Mar-
cel Blistein, Ori Ram, Dan Zhang, Evan Rosen, and
1 others. 2025. Gemini 2.5: Pushing the frontier with
advanced reasoning, multimodality, long context, and
next generation agentic capabilities. arXiv preprint
arXiv:2507.06261.
Yue Ding, Yiyan Ji, Jungang Li, Xuyang Liu, Xinlong
Chen, Junfei Wu, Bozhou Li, Bohan Zeng, Yang
Shi, Yushuo Guan, and 1 others. 2026. Omnisift:
Modality-asymmetric token compression for efficient
omni-modal large language models. arXiv preprint
arXiv:2602.04804.
Yang Du, Zhuoran Lin, Kaiqiang Song, Biao Wang,
Zhicheng Zheng, Tiezheng Ge, Bo Zheng, and Qin
Jin. 2025. Vc4vg: Optimizing video captions for
text-to-video generation. In Proceedings of the 2025
Conference on Empirical Methods in Natural Lan-
guage Processing, pages 1124–1138.
Yuying Ge, Yixiao Ge, Chen Li, Teng Wang, Junfu Pu,
Yizhuo Li, Lu Qiu, Jin Ma, Lisheng Duan, Xinyu
Zuo, and 1 others. 2025.
Arc-hunyuan-video-7b:
Structured video comprehension of real-world shorts.
arXiv preprint arXiv:2507.20939.
Tiantian Geng, Jinrui Zhang, Qingni Wang, Teng
Wang, Jinming Duan, and Feng Zheng. 2025. Long-
vale: Vision-audio-language-event benchmark to-
wards time-aware omni-modal perception of long
videos.
In Proceedings of the Computer Vision
and Pattern Recognition Conference, pages 18959–
18969.
Yoav HaCohen, Benny Brazowski, Nisan Chiprut, Yaki
Bitterman, Andrew Kvochko, Avishai Berkowitz,
Daniel Shalem, Daphna Lifschitz, Dudu Moshe, Ei-
tan Porat, Eitan Richardson, Guy Shiran, Itay Chachy,
Jonathan Chetboun, Michael Finkelson, Michael
Kupchick, Nir Zabari, Nitzan Guetta, Noa Kotler, and
10 others. 2025. Ltx-2: Efficient joint audio-visual
foundation model. arXiv preprint arXiv:2601.03233.
Yichen He, Yuan Lin, Jianchao Wu, Hanchong Zhang,
Yuchen Zhang, and Ruicheng Le. 2024. Storyteller:
Improving long video description through global
audio-visual character identification. arXiv preprint
arXiv:2411.07076.
Wenxuan Hou, Guangyao Li, Yapeng Tian, and Di Hu.
2024. Toward long form audio-visual video under-
standing. ACM Transactions on Multimedia Comput-
ing, Communications and Applications, 20(9):1–26.
Shiyu Hu, Xuchen Li, Xuzhao Li, Jing Zhang,
Yipei Wang, Xin Zhao, and Kang Hao Cheong.
2024.
Fiova: A multi-annotator benchmark for
human-aligned video captioning.
arXiv preprint
arXiv:2410.15270.
Daili Hua, Xizhi Wang, Bohan Zeng, Xinyi Huang, Hao
Liang, Junbo Niu, Xinlong Chen, Quanqing Xu, and
Wentao Zhang. 2026. Vabench: A comprehensive
benchmark for audio-video generation. In Proceed-
ings of the IEEE/CVF Conference on Computer Vi-
sion and Pattern Recognition, pages 23345–23355.
Md Mohaiminul Islam, Ngan Ho, Xitong Yang, Tushar
Nagarajan, Lorenzo Torresani, and Gedas Bertasius.
2024. Video recap: Recursive captioning of hour-
long videos. In Proceedings of the IEEE/CVF Con-
ference on Computer Vision and Pattern Recognition,
pages 18198–18208.
Yunheng Li, Hengrui Zhang, Meng-Hao Guo, Wenzhao
Gao, Shaoyong Jia, Shaohui Jiao, Qibin Hou, and
Ming-Ming Cheng. 2026. Towards universal video
mllms with attribute-structured and quality-verified
instructions. arXiv preprint arXiv:2602.13013.
Lin Long, Yichen He, Wentao Ye, Yiyuan Pan, Yuan
Lin, Hang Li, Junbo Zhao, and Wei Li. 2025. See-
ing, listening, remembering, and reasoning: A multi-
modal agent with long-term memory. arXiv preprint
arXiv:2508.09736.
Ziyang Ma, Ruiyang Xu, Zhenghao Xing, Yunfei Chu,
Yuxuan Wang, Jinzheng He, Jin Xu, Pheng-Ann
Heng, Kai Yu, Junyang Lin, and 1 others. 2025.
Omni-captioner: Data pipeline, models, and bench-
mark for omni detailed perception. arXiv preprint
arXiv:2510.12720.
Artemis Panagopoulou, Le Xue, Ning Yu, Junnan
Li, Dongxu Li, Shafiq Joty, Ran Xu, Silvio
Savarese, Caiming Xiong, and Juan Carlos Niebles.
2023.
X-instructblip: A framework for aligning
x-modal instruction-aware representations to llms
and emergent cross-modal reasoning. arXiv preprint
arXiv:2311.18799.
Junfu Pu, Yuxin Chen, Teng Wang, and Ying Shan.
2026. Omniscript: Towards audio-visual script gen-
eration for long-form cinematic video. arXiv preprint
arXiv:2604.11102.
Qwen Team. 2026a. Qwen3.6-27B: Flagship-level cod-
ing in a 27B dense model.
Qwen Team. 2026b. Qwen3.6-35B-A3B: Agentic cod-
ing power, now open to all.
William M Rand. 1971. Objective criteria for the evalu-
ation of clustering methods. Journal of the American
Statistical association, 66(336):846–850.
Yang Shi, Jiaheng Liu, Yushuo Guan, Zhenhua Wu,
Yuanxing Zhang, Zihao Wang, Weihong Lin, Jingyun
Hua, Zekun Wang, Xinlong Chen, and 1 others. 2025.
Mavors: Multi-granularity video representation for
multimodal large language model. In Proceedings of
the 33rd ACM International Conference on Multime-
dia, pages 10994–11003.
Fangxun Shu, Lei Zhang, Hao Jiang, and Cihang Xie.
2025. Audio-visual llm for video understanding. In
Proceedings of the IEEE/CVF International Confer-
ence on Computer Vision, pages 4246–4255.


## Page 11


Guangzhi Sun, Wenyi Yu, Changli Tang, Xianzhao
Chen, Tian Tan, Wei Li, Lu Lu, Zejun Ma, Yux-
uan Wang, and Chao Zhang. 2024. video-salmonn:
Speech-enhanced audio-visual large language mod-
els. arXiv preprint arXiv:2406.15704.
Changli Tang, Yixuan Li, Yudong Yang, Jimin Zhuang,
Guangzhi Sun, Wei Li, Zejun Ma, and Chao Zhang.
2025. video-salmonn 2: Caption-enhanced audio-
visual large language models.
arXiv preprint
arXiv:2506.15220.
Changli Tang, Tianyi Wang, Fengyun Rao, Jing Lyu,
and Chao Zhang. 2026. D-orca: Dialogue-centric op-
timization for robust audio-visual captioning. arXiv
preprint arXiv:2602.07960.
Meituan LongCat Team, Bairui Wang, Bin Xiao,
Bo Zhang, Bolin Rong, Borun Chen, Chang Wan,
Chao Zhang, Chen Huang, Chen Chen, and 1 others.
2025. Longcat-flash-omni technical report. arXiv
preprint arXiv:2511.00279.
Qwen Team. 2026a. Qwen3.5: Accelerating productiv-
ity with native multimodal agents.
Tencent Hunyuan Team. 2026b.
Script-a-video:
Deep structured audio-visual captions via factorized
streams and relational grounding. arXiv preprint
arXiv:2604.11244.
Jiawei Wang, Liping Yuan, Yuchen Zhang, and Hao-
miao Sun. 2024. Tarsier: Recipes for training and
evaluating large video description models. arXiv
preprint arXiv:2407.00634.
Weiyun Wang, Zhangwei Gao, Lixin Gu, Hengjun Pu,
Long Cui, Xingguang Wei, Zhaoyang Liu, Linglin
Jing, Shenglong Ye, Jie Shao, and 1 others. 2025a. In-
ternvl3. 5: Advancing open-source multimodal mod-
els in versatility, reasoning, and efficiency. arXiv
preprint arXiv:2508.18265.
Xiao Wang, Jingyun Hua, Weihong Lin, Yuanxing
Zhang, Fuzheng Zhang, Jianlong Wu, Di Zhang, and
Liqiang Nie. 2025b. Haic: Improving human action
understanding and generation with better captions for
multi-modal large language models. In Proceedings
of the 63rd Annual Meeting of the Association for
Computational Linguistics (Volume 1: Long Papers),
pages 10158–10181.
Hongchen Wei, Zhihong Tan, Yaosi Hu, Chang Wen
Chen, and Zhenzhong Chen. 2025. Longcaptioning:
Unlocking the power of long video caption gener-
ation in large multimodal models. arXiv preprint
arXiv:2502.15393.
Peiran Wu, Yunze Liu, Zhengdong Zhu, Enmin Zhou,
and Junxiao Shen. 2025. Ugc-videocaptioner: An
omni ugc video detail caption model and new bench-
marks. arXiv preprint arXiv:2507.11336.
LLM-Core-Team Xiaomi. 2025. Mimo-vl technical
report. Preprint, arXiv:2506.03569.
Jin Xu, Zhifang Guo, Jinzheng He, Hangrui Hu, Ting
He, Shuai Bai, Keqin Chen, Jialin Wang, Yang Fan,
Kai Dang, and 1 others. 2025a.
Qwen2. 5-omni
technical report. arXiv preprint arXiv:2503.20215.
Jin Xu, Zhifang Guo, Hangrui Hu, Yunfei Chu, Xiong
Wang, Jinzheng He, Yuxuan Wang, Xian Shi, Ting
He, Xinfa Zhu, and 1 others. 2025b. Qwen3-omni
technical report. arXiv preprint arXiv:2509.17765.
Yifan Xu, Xinhao Li, Yichun Yang, Desen Meng, Rui
Huang, and Limin Wang. 2024. Carebench: A fine-
grained benchmark for video captioning and retrieval.
arXiv preprint arXiv:2501.00513.
Zihui Xue, Joungbin An, Xitong Yang, and Kristen
Grauman. 2025. Progress-aware video frame caption-
ing. In Proceedings of the Computer Vision and Pat-
tern Recognition Conference, pages 13639–13650.
An Yang, Anfeng Li, Baosong Yang, Beichen Zhang,
Binyuan Hui,
Bo Zheng,
Bowen Yu,
Chang
Gao, Chengen Huang, Chenxu Lv, and 1 others.
2025a.
Qwen3 technical report.
arXiv preprint
arXiv:2505.09388.
Zhantao Yang, Huangji Wang, Ruili Feng, Han Zhang,
Yuting Hu, Shangwen Zhu, Junyan Li, Yu Liu, and
Fan Cheng. 2025b.
Addressing the id-matching
challenge in long video captioning. arXiv preprint
arXiv:2510.06973.
Linli Yao, Yuancheng Wei, Yaojie Zhang, Lei Li, Xin-
long Chen, Feifan Song, Ziyue Wang, Kun Ouyang,
Yuanxin Liu, Lingpeng Kong, and 1 others. 2026.
Timechat-captioner: Scripting multi-scene videos
with time-aware and structural audio-visual captions.
arXiv preprint arXiv:2602.08711.
Hanrong Ye, Chao-Han Huck Yang, Arushi Goel, Wei
Huang, Ligeng Zhu, Yuanhang Su, Sean Lin, An-
Chieh Cheng, Zhen Wan, Jinchuan Tian, and 1 others.
2025. Omnivinci: Enhancing architecture and data
for omni-modal understanding llm. arXiv preprint
arXiv:2510.15870.
Qilang Ye, Zitong Yu, Rui Shao, Xinyu Xie, Philip Torr,
and Xiaochun Cao. 2024. Cat: Enhancing multi-
modal large language model to answer questions in
dynamic audio-visual scenarios. In European Confer-
ence on Computer Vision, pages 146–164. Springer.
Liping Yuan, Jiawei Wang, Haomiao Sun, Yuchen
Zhang, and Yuan Lin. 2025. Tarsier2: Advancing
large vision-language models from detailed video
description to comprehensive video understanding.
arXiv preprint arXiv:2501.07888.
Chunlin Zhong, Qiuxia Hou, Zhangjun Zhou, Yanhao
Zhang, Shuang Hao, Haonan Lu, He Tang, and Xi-
ang Bai. 2026. Owlcap: Harmonizing motion-detail
for video captioning via hmd-270k and caption set
equivalence reward. In Proceedings of the AAAI Con-
ference on Artificial Intelligence, volume 40, pages
13503–13511.


## Page 12


Appendix
A
Video Collection Details
Beyond the requirements on video duration and
content diversity discussed in Section 3.3, we fur-
ther elaborate on our quality control protocols and
provide the complete taxonomy of our benchmark.
First, in terms of resolution and visual fidelity, all
videos are required to have a minimum resolution
of 720p. Videos exhibiting severe artifacts, such as
over-sharpening, noticeable mosaic distortion, or
audiovisual misalignment, are excluded. Second,
to prevent semantic leakage, we filter out videos
containing excessive on-screen subtitles, as such
text could inadvertently provide cues that confound
the evaluation of a model’s audiovisual fusion capa-
bility. Third, to minimize domain bias, we restrict
the collection to at most one video from each dis-
tinct source, such as a specific movie, television
series, or content creator. Finally, to reduce the
risk of data contamination, we not only exclude
samples from existing datasets but also prioritize
recently published videos. To respect copyright
constraints, our benchmark will be released under
highly restrictive licensing terms, permitting its use
exclusively for academic research purposes.
Due to space constraints in the main text, Fig-
ure 3 only illustrates the eight primary domains and
their major subcategories. To provide a comprehen-
sive overview, Table 5 provides the full taxonomy
of all 36 fine-grained video subcategories included
in our collection.
B
Human Annotators
During the video collection stage, we recruit ten
experienced video collectors through a crowdsourc-
ing platform to gather videos from the Internet that
satisfy our predefined selection criteria.
In the subsequent annotation stage, we re-
cruit twenty experienced multilingual annotators
through the same crowdsourcing platform to par-
ticipate in the labeling process. To illustrate the
annotation workflow, we provide a screenshot of
the annotation interface in Figure 5, which demon-
strates how annotators interact with the system and
complete annotation tasks.
To ensure the quality and reliability of both the
video collection and annotation, annotators are
compensated based on the time spent rather than
the number of samples completed, thereby reduc-
ing incentives for rushed or superficial work. Anno-
Major Category
Subcategories
Relationship
Friendship & Companionship; Romantic
Love; Professional Ties; Mentorship;
Community Life
Youth
Campus Life; Coming-of-Age; Ambition
& Dreams; Transition to Adulthood
Entertainment
Sketch Comedy; Variety & Reality Shows;
Lighthearted Drama; Sports Competition;
Musical & Dance Performances
History
Culture Heritage; Politics Affairs;
Military Conflict; Society Evolution;
Historical Biography; Memory
Family
Family Bonding; Mutual Support;
Family Conflict; Everyday Leisure;
Parenting & Education
Lifestyle
Urban Living; Rural Living; Nature &
Outdoors; Home & Settlement; Travel
& Exploration
Fantasy
Adventure & Exploration; Science Fiction;
Supernatural Themes
Mystery
Deduction & Detective; Crime Narratives;
Psychological Games
Table 5: Detailed video categories of CapRiCorn-1K.
tators are paid at a rate of USD 10 per hour, which
is highly competitive relative to prevailing industry
standards for comparable tasks.
C
Further Analysis
In this section, we provide additional analyses
from four distinct perspectives: (1) the relationship
between caption length and our evaluation met-
rics; (2) the trade-off between the number of input
frames and input resolution under a fixed context-
window budget; (3) the impact of the maximum
input frame count under a fixed resolution; and (4)
the impact of the maximum input resolution under
a fixed frame count. The corresponding results are
presented in Figure 6.
C.1
Analysis on Caption Length
Some caption evaluation benchmarks can obtain
artificially higher scores simply by encouraging
models to generate longer captions, which fails
to faithfully reflect the actual quality of the cap-
tions. To verify that our evaluation metrics are not
strongly correlated with caption length, we select
several representative captioning models and ana-
lyze the correlation between their performance on
CapRiCorn-1K and their average caption lengths,
as illustrated in Figure 6a. The results demonstrate
that the evaluation metrics of CapRiCorn-1K are
not directly associated with caption length. Specifi-


## Page 13


Figure 5: Screenshot of the annotation system interface.
cally, the Pearson correlation coefficients between
caption length and Acc, Cov, and Ref are 0.525,
0.561, and 0.429, respectively.
C.2
Analysis on Frame Count and Resolution
In the main experiments, our evaluation setting
prioritizes relatively high spatial resolution (typi-
cally 512 × 512) while determining the maximum
number of frames according to the context-window
limit of each model. To investigate the trade-off be-
tween frame count and resolution under a fixed
context-window budget, we take Qwen3-Omni-
Captioner as a case study. Specifically, we con-
strain the total number of visual tokens to approx-
imately 25K while varying the maximum frame
count and resolution for analysis. The results are
presented in Figure 6b.
The results show that excessively high resolu-
tion (which consequently leads to an insufficient
number of frames), as well as excessively large
frame counts (which consequently require overly
low resolution), both lead to performance degrada-
tion. Therefore, maintaining a sufficiently high res-
olution and then increasing the number of frames
within the context window budget is more benefi-
cial for captioning performance.
C.3
Analysis on Frame Count Only
To independently evaluate the effect of the maxi-
mum number of input frames, we conduct an ab-
(a) Analysis on caption length
(b) Analysis on frame count with resolution
# "&!%	$"&%"!





"'
%
"'%
#%







	

	



	

	
		






 +-&*)")$-%
	






!!*.
!!'"#-
*.'"#-
"#,&$%-
	






"#
/")()& +-&*)",
/")()&
"(&)&
,*
 +-&*)",
* 

 








	


	

	
 

	

	


 
" 
 

	
	


! 
	
	





"








(c) Analysis on frame count
(d) Analysis on resolution
Figure 6: Further analysis of captioning performance
with respect to (a) caption length; (b) the trade-off be-
tween frame count and resolution under a fixed context-
window budget; (c) frame count under a fixed resolution;
and (d) resolution under a fixed frame count.
lation study on the maximum input frame count
while fixing the input resolution of Qwen3-Omni-
Captioner to 512 × 512, as shown in Figure 6c.
The results indicate that, within the limitation of
the maximum context window, captioning perfor-
mance consistently improves as the maximum num-
ber of input frames increases.
C.4
Analysis on Resolution Only
To independently evaluate the effect of the maxi-
mum input resolution, we conduct an ablation study


## Page 14


on the input resolution while fixing the number of
input frames of Qwen3-Omni-Captioner to 200, as
shown in Figure 6d. The results demonstrate that,
within the limitation of the maximum context win-
dow, the captioning performance consistently im-
proves as the maximum input resolution increases.
C.5
Error Analysis
Through qualitative examination of failure cases,
we identify three representative scenarios in
CapRiCorn-1K that remain particularly challeng-
ing for current models.
• Clothing Changes (Figure 7). In such scenarios,
the model should not only precisely describe dif-
ferent outfits worn by the same subject, but also
explicitly articulate the clothing transitions be-
tween them to maintain consistent subject track-
ing throughout the caption. However, reliably
capturing and narrating such wardrobe changes
for a single subject remains a persistent challenge
for existing models.
• Multiple Subjects (Figure 8). As the number
of subjects increases, models tend to confuse
referential relationships among different subjects,
particularly when multiple subjects share similar
visual appearances or attributes.
• Multiple Scenes (Figure 9). Frequent scene tran-
sitions prevent the model from distinguishing
subjects based on relatively stable positional cues
within a single scene, thereby increasing the dif-
ficulty of maintaining consistent subject refer-
ences. As a result, models often resort to generat-
ing ambiguous references or producing incorrect
referential associations.
D
Implementation Details
Our evaluation adheres to the official protocols of
each model by default. When such protocols are un-
available, given the substantial length of the videos,
we uniformly sample frames up to the maximum
context window supported by the model while pre-
serving sufficient frame resolution. In this section,
we provide the detailed evaluation settings for all
models, which is also summarized in Table 6.
For Qwen2.5-Omni-style models, including
Qwen2.5-Omni, UGC-VideoCaptioner, AVoCaDO,
DiaDem, and ASID-Captioner, we set the maxi-
mum number of vision tokens per frame to 256,
corresponding to 200,704 pixels per frame (i.e.,
256 × 14 × 14 × 2 × 2). The frame rate is fixed at
2 FPS. Given a maximum context window of 32K
Model Class
Max Pixels per Frame
FPS
Max Frames
Audiovisual Models
Qwen2.5-Omni
200,704 (448×448)
2
200
Qwen3-Omni
262,144 (512×512)
2
200
video-SALMONN-2
147,456 (384×384)
1
110
video-SALMONN-2+
61,250 (~248×248)
10
768
OmniVinci
original
2
128
ARC-Qwen-Video
153,664 (392×392)
1
300
Vision-Only Models
Qwen3-VL
262,144 (512×512)
2
768
Qwen3.5
262,144 (512×512)
2
768
Qwen3.6
262,144 (512×512)
2
768
InternVL3.5
200,704 (448×448)
2
100
MiMo-VL
100,352 (224×224)
2
200
Tarsier2
460,800 (640×720)
-
256
Table 6: Implementation details of the evaluation set-
tings. Frames are initially sampled at the target FPS. If
the resulting frame count exceeds the Max Frames limit,
uniform sampling is applied to satisfy the constraint.
tokens, we set the maximum number of frames to
200, resulting in a maximum visual token length of
25,600 (i.e., 256 × 200/2 after accounting for tem-
poral aggregation). For Qwen3-Omni-style mod-
els, although the maximum context window is 64K,
their technical report indicates that training is con-
ducted only up to 32K context length. We therefore
adopt the 32K configuration for evaluation to en-
sure a consistent and comparable setting. All other
audiovisual models are evaluated using their de-
fault official configurations without modification.
For Qwen3-VL-style models, including Qwen3-
VL, Qwen3.5, and Qwen3.6, we set the maxi-
mum number of vision tokens per frame to 256,
corresponding to 262,144 pixels per frame (i.e.,
256 × 16 × 16 × 2 × 2), with 2 FPS and a maxi-
mum of 768 frames following the recommended
long-video setting. For InternVL3.5, we use the
official 448 × 448 input resolution, correspond-
ing to 200,704 pixels per frame and set the max
number of frames to 200 under the 32K context
budget to better support long-video evaluation. For
MiMo-VL, we set the max pixels to 100,352 (i.e.,
128 × 14 × 14 × 2 × 2), and use 2 FPS with a
maximum of 200 frames under its 16K context con-
straint. For Tarsier2, we keep its default maximum
pixel budget of 460,800 pixels per frame and in-
crease the frame number from the default 16 to the
supported maximum of 256.
All models evaluated in this work are strictly
limited to academic research purposes and com-
ply with their respective official licenses. For all
statistical analyses involving Pearson correlation
coefficients, we use SciPy version 1.14.1.


## Page 15


<woman_1>: A woman with long blonde hair, initially seen in a black jacket and later wearing a teal robe. 
<man_1>: A man with short dark hair and a beard, wearing a teal robe.
<woman_2>: A woman with dark hair, wearing a white and green patterned robe.
Main Subjects
S1: A woman with long blonde hair in a black leather jacket (<woman_1>) sits on a red 
bench and speaks while looking off-camera.
S2: A woman with dark hair in a patterned robe (<woman_2>) stands beside a man in a 
teal robe (<man_1>), looking toward the camera.
S3: A woman with blonde hair in a teal robe (<woman_1>) walks behind a man in a teal 
robe (<man_1>) and a woman in a patterned robe (<woman_2>) while they are standing 
in a room with red walls.
Subject-Related Keypoints
O1: The first scene is set in an indoor lounge with wooden wall 
panels, a red cushioned bench, and a small table holding two 
white cups.
O2: The camera stays relatively steady, focusing on the subjects 
as they move or pose in the red-walled room.
O3: Bright, upbeat electronic background music plays 
throughout the video.
Other Keypoints
The video begins with a scene in what appears to be a casual indoor setting, possibly a cafe or lounge. Three individuals are seated on a bench against 
a backdrop of wooden panels. One person is wearing a black leather jacket and has long blonde hair (<woman_1>) . Nearby, another person is 
dressed in a yellow sweater and patterned pants, holding a phone… The scene transitions to a different room characterized by red walls and a large 
screen displaying an underwater scene. Here, a person wearing a light green shirt (<man_1>) is seen handling some clothes… During this 
sequence, a man (<man_1>)'s voice continues speaking… The view then shifts to show three individuals standing together. One of them is wearing 
a patterned shirt with a mix of white and another color (<woman_2>), while the other two are in light green shirts (<woman_1>, <man_1>). 
As these individuals interact, one of them (<woman_1>) turns and walks away, while another (<man_1>, <woman_2>) faces the screen, engrossed 
in its content. The final part of this clip focuses on a close-up of a person with long blonde hair, also wearing a light green shirt (<woman_1>), 
sitting against the red wall… 
Caption by video-SALMONN-2
Acc: 18.8; Cov: 37.5; Ref: 0.0
The video opens in a brightly lit, modern café or restaurant, featuring a woman with long blonde hair, wearing a black leather jacket (<woman_1>), 
seated at a table with a man in a yellow hoodie… The scene then transitions to a different setting, a brightly lit room with red walls and a large screen 
displaying a movie poster, featuring a woman with red hair and a traditional headdress, accompanied by Chinese text (<woman_2>). A man, 
wearing a light green chef's coat (<man_1>), is seen moving his arms and body in a lively, expressive manner… The video then shifts to a different 
area within the same establishment, where a woman with long brown hair, wearing a patterned white shirt (<woman_2>), is seen smiling and 
laughing, seemingly enjoying the lively environment. The camera pans to show a blonde woman in a blue top (<woman_1>), who is also smiling and 
appears to be engaged in conversation, further contributing to the cheerful and social ambiance. Throughout the video, the audio features a cheerful, 
upbeat music track, complementing the energetic and positive mood of the scenes…
Caption by UGC-VideoCaptioner
Acc: 18.8; Cov: 62.5; Ref: 0.5
Keypoint Mention Status: S1
S2
S3
O1
O2
O3
Keypoint Mention Status: S1
S2
S3
O1
O2
O3
Figure 7: Error analysis for clothing-change scenarios. Keypoints marked with
,
, and
are “correctly
mentioned”, “partially mentioned or containing errors”, and “not mentioned”, respectively. Subject descriptions are
highlighted in bold with the ground-truth subject-ID shown in parentheses immediately afterward. Different colors
representing consistent and correct, ambiguous, and inconsistent or incorrect subject references, respectively.
E
Prompt Details
Figures 10 and 11 illustrate the initial evaluation
step of CapRiCorn-1K, which involves determining
the mention status of each keypoint in the caption,
thereby enabling an assessment of overall caption
quality. For the subject-related keypoints that are
correctly or partially mentioned, the corresponding
localized subject descriptions are simultaneously
extracted from the caption. Descriptions associ-
ated with the same ground-truth subjects are then
clustered within the caption context to evaluate ref-
erential consistency, using the prompt in Figure 12.
Figures 13 and 14 present the prompt lists used
to generate captions for audiovisual video caption-
ing models and vision-only video captioning mod-
els, respectively. These prompts are randomly sam-
pled to assess both general captioning capabilities
and the ability to maintain subject referential con-
sistency within the generated captions.


## Page 16


<man_1>: A man with curly light brown hair, wearing a blue ‘Laugh Daily’ t-shirt. 
<man_2>: A man with short light brown hair, wearing a red t-shirt.    
<man_3>: A man with curly light brown hair, wearing a blue hoodie.
<man_4>: A man with brown hair and a goatee, wearing a grey t-shirt.   <man_5>: A man with short brown hair and glasses, wearing a white t-shirt.
Main Subjects
S1: Inside the vintage white van, a man in a blue hoodie (<man_3>) at 
the steering wheel and a man in a grey graphic t-shirt (<man_4>) in the 
passenger seat discuss a loud humming sound from the engine.
S2: Seated in the 2025 van, the man in the blue 'Laugh Daily' t-shirt 
(<man_1>) talks to the camera from the driver's seat, with the man in 
the red long-sleeved shirt (<man_2>) beside him and the man in the 
white t-shirt (<man_5>) in the back.
Subject-Related Keypoints
O1: The opening scene takes place in an outdoor paved area with green trees in the 
background. A white old van and a dark grey modern van are parked side-by-side, 
accompanied by energetic pop-rock music.
O2: The modern van's interior is sleek and modern, equipped with white cabinetry, 
LED lighting, a kitchenette with a sink and induction cooktop, and a compact bathroom.
O3: Multiple cuts alternate between the interior of the 1985 van and the 2025 van to 
highlight the technological differences.
Other Keypoints
The video opens with a nostalgic journey through time, showcasing two iconic vans: a 1985 Volkswagen van and a modern 2025 van. The scene transitions to a 
group of men, dressed casually in t-shirts and caps, gathered in an outdoor setting, surrounded by lush greenery. They stand in front of the vans, engaged in 
lively conversation and gestures, suggesting camaraderie and anticipation for an upcoming adventure… The scene shifts to the interior of the 1985 van, where a 
man in a blue hoodie (<man_3>) drives, and another man in a gray shirt (<man_4>) sits beside him, holding a drink. The driver (<man_3>) gestures 
animatedly, indicating a lively conversation… The group then transitions to the interior of the modern 2025 van, where the driver, still in the blue hoodie 
(<man_1>), continues to drive while the passenger in the gray shirt engages in conversation (<man_2>). The van's interior is sleek and modern, equipped with 
a touchscreen display and various amenities…
Caption by Qwen3-Omni-Captioner
Acc: 4.5; Cov: 15.9; Ref: 0.3
The video opens with a close-up, shaky shot of a man in a red t-shirt (<man_1>) gesturing with his hands in front of two vans, one white and one 
black, parked in a lot. The number "1985" appears in large, yellow, cartoon-style font at the bottom of the screen. The audio opens with an upbeat, 
funky electronic track with a driving beat, creating a sense of excitement and adventure. A male narrator (<man_1>) speaks with an enthusiastic and 
high-energy voice, "Today we're going on a road trip using a 1985 van and a 2025 van." The camera pans to a group of six men standing between the 
two vans, smiling and talking. The number \"2025\" appears in the same yellow font… The scene transitions to a shot of the two vans… The video 
returns to two men (<man_3>, <man_4>) in the driver's seats of the white van, laughing and talking. The narrator (<man_3>)’s voice becomes 
more animated and excited… The camera pans across the interior of the black van, showing its modern, open-concept layout with a kitchenette and a 
bed. The camera then moves to a shot of the man in the blue hoodie (<man_3>) sitting in the driver's seat of the white van, looking around with a 
surprised expression… The camera pans across the van's interior again, showing the two men in the front seats, laughing and talking… The camera 
then shows a shot of the white van's interior, with the two men (<man_3>, <man_4>) in the front seats, looking around in amazement. The camera 
then shows a close-up of the man in the blue hoodie (<man_3>) driving, looking focused. The camera pans across the interior of the black van, 
showing a close-up of the man in the blue hoodie (<man_1>) driving, looking excited…
Caption by AVoCaDO
Acc: 11.4; Cov: 25.0; Ref: 1.3
Keypoint Mention Status: S1
S2
O1
O2
O3
Keypoint Mention Status: S1
S2
O1
O2
O3
Figure 8: Error analysis in multi-subject scenarios. Keypoints marked with
,
, and
are “correctly mentioned”,
“partially mentioned or containing errors”, and “not mentioned”, respectively. Subject descriptions are highlighted
in bold with the ground-truth subject-ID shown in parentheses immediately afterward. Different colors representing
consistent and correct, ambiguous, and inconsistent or incorrect subject references, respectively.


## Page 17


<man_1>: A man with short reddish-blonde hair, initially wearing a light blue t-shirt, then a grey long-sleeved shirt. 
<man_2>: A man with dark wavy hair, often wearing a white headband.
<woman_1>: A woman with long wavy brown hair.
<man_3>: A man with dark brown hair, initially wearing a tan cowboy-style button-down shirt, then a white tank top with a neck brace.
Main Subjects
S1: The man in the blue t-shirt (<man_1>) shows a document to the woman 
(<woman_1>) and the man in the green tank top (<man_2>), explaining his vegetable 
oil fuel project.
S2: A man in a grey shirt (<man_1>) and a woman in a striped tank top (<woman_1>) 
look closely at a small potted plant together.
Subject-Related Keypoints
O1: An outdoor picnic area with wooden tables and benches, surrounded 
by trees and other people.
O2: Upbeat, rhythmic rock music plays throughout the montage of 
working on the car project.
O3: A woman in a pink top cooks at a stove in the kitchen while the 
young girl sneaks past.
Other Keypoints
At 0s, the video opens in a sun-dappled outdoor picnic area with wooden tables and lush greenery, where three young men gather: a muscular man 
with curly dark hair in a sleeveless olive shirt (<man_2>), a man in a light plaid shirt (<man_3>), and a man in a turquoise shirt (<man_1>)… 
At 12s, a woman with long brown hair in a striped tank top (<woman_1>) approaches the table carrying a tray of food… At 30s, the scene shifts 
to a garage where a man in a white shirt and shorts works on a car (<man_3>), with a yellow toolbox filled with cleaning supplies in the 
foreground… At 55s, the man in the white shirt and shorts (<man_3>) works on a car engine with an older man in a red shirt (<man_2>), who 
helps him… At 76s, the scene shifts to an outdoor area where the man in the sleeveless olive shirt (<man_2>) and the man in the light plaid shirt 
(<man_3>) stand near a white truck…
Caption by ASID-Captioner-7B
Acc: 11.4; Cov: 31.8; Ref: 1.2
Keypoint Mention Status: S1
S2
O1
O2
O3
The video starts with four students sitting around a wooden picnic table outside. One of them is wearing a blue t-shirt and has short, light hair
(<man_1>). He’s showing a paper to the others. Beside him sits a girl with long brown hair and a striped top (<woman_1>). Across from them are 
two other boys. One has a white headband and a green tank top (<man_2>), and the other is wearing a tan, Western-style shirt (<man_3>)… 
The scene then transitions into a montage of the students (<man_1>, <woman_1>, <man_2>, <man_3>) working on the car in a garage. A fast-paced, 
upbeat song starts playing. You see them (<man_1>, <man_2>, <man_3>) lifting the car, working under it, and tinkering with the engine. There are 
also shots of them (<man_1>, <woman_1>) studying in a library, looking at a small potted plant…  One of the boys is shown using a grinder 
(<man_2>), and sparks fly everywhere… As the montage continues, the group (<man_1>, <man_2>, <man_3>) is shown working together, painting 
parts of the car, and finally pouring vegetable oil into the tank using a funnel… Inside the car, the students are excited. One of the boys notes, 
"Smells like orange chicken."...
Caption by Gemini-3-Flash
Acc: 22.7; Cov: 29.5; Ref: 2.5
Keypoint Mention Status: S1
S2
O1
O2
O3
Figure 9: Error analysis in multi-scene scenarios. Keypoints marked with
,
, and
are “correctly mentioned”,
“partially mentioned or containing errors”, and “not mentioned”, respectively. Subject descriptions are highlighted
in bold with the ground-truth subject-ID shown in parentheses immediately afterward. Different colors representing
consistent and correct, ambiguous, and inconsistent or incorrect subject references, respectively.


## Page 18


Joint assessment of mention status and subject-description extraction for subject-related keypoints
You will be given a video caption and a specific event involving one or more subjects (predefined
and enclosed in <>; do NOT add any subjects that you think should be included). Your task is
to determine how this event is represented in the caption by assigning it to one of the following
categories:
- "correctly mentioned": the event is accurately described in the caption, possibly with only minor
omissions or negligible errors.
- "mentioned but with errors": the event is mentioned in the caption, but contains substantial
inaccuracies, distortions, or misleading details.
- "not mentioned": the event is not described in the caption at all.
If the classification is "correctly mentioned" or "mentioned but with errors":
- From the **local caption segment** at the moment the event occurs, identify the subject ID
enclosed in <> within the event, and extract the corresponding subject description from the **local
caption segment**. Only when the local subject description is overly vague (e.g., “his”, “her”,
“their”, “it”, “the man”) is it allowed to use the global context to obtain a more specific subject
description.
- The extracted content must be strictly from the local descriptions present in the caption text, NOT
copied or inferred from the provided subject description in the event.
- Each subject’s local description should be concise while still containing enough identifying
information.
If the classification is "not mentioned":
- Set the subject description value to null.
Video caption:
{}
Event:
{}
Subject ID list:
{}
Output format:
```json
{{
"event_type": "xx", // One of ["correctly mentioned", "mentioned but with errors", "not mentioned"]
"reason": "xx", // Brief justification for event_type; no double quotes inside
"subject_description_in_caption": {{
"<sbj_id_1>": xx,
"<sbj_id_2>": xx, // if exists
...
}} // **Brief subject descriptions dict (rather than event description)** summarized from caption
or null (only when the event_type is "not mentioned"). **Do not use any pronouns (e.g., his, her,
their, it)**; instead, replace them with their corresponding referents identified from the caption.
}}
```
Figure 10: Prompts to jointly evaluate the mention status of subject-related keypoints and extract subject descriptions
for the mentioned keypoints.


## Page 19


Prompts to evaluate the mention status of other keypoints not related to the subject
You will be given a video caption and a specific event. Your task is to determine how this event is
represented in the caption by assigning it to one of the following categories:
- "correctly mentioned": the event is accurately described in the caption, possibly with only minor
omissions or negligible errors.
- "mentioned but with errors": the event is mentioned in the caption, but contains substantial
inaccuracies, distortions, or misleading details.
- "not mentioned": the event is not described in the caption at all.
Video caption:
{}
Event:
{}
Output format:
```json
{{
"event_type": "xx", // One of ["correctly mentioned", "mentioned but with errors", "not mentioned"]
"reason": "xx", // Brief justification for event_type; no double quotes inside
}}
```
Figure 11: Prompts to evaluate the mention status of other keypoints not related to the subjects.


## Page 20


Prompts for clustering descriptions of the same ground-truth subject
You will be given a list of subject descriptions and a video caption. Your task is to group these
descriptions into clusters, where each cluster contains descriptions that refer to the same real-world
subject, based on both the descriptions and the caption context.
Descriptions should be grouped together only if they satisfy at least **one of** the following
conditions:
1. They share sufficiently specific matching **appearance attributes**, without considering
actions.
2. They contain the same subject name. In this case, attribute differences must be ignored, and
**all descriptions with the same subject name must always be grouped into a single cluster**.
3. Based on the video caption, it can be reasonably and clearly inferred that the descriptions refer
to the same subject.
Guidelines:
- Note that identical descriptions do not necessarily refer to the same subject.
- For example, multiple generic references such as “a girl” should be treated as distinct subjects,
because the only feature "girl" is too vague to determine that they refer to the same entity, unless
the caption clearly implies they refer to the same entity (e.g., there is only one girl in the caption).
- Similarly, ambiguous descriptions like "one of xxx" or "two other xxx", which lack distinguishing
details, should be treated as referring to different subjects (i.e., if the phrase "one of xxx" appears
four times, it should be classified as four **distinct** categories), unless the caption provides
sufficient evidence to identify them as the same entity.
- Conversely, non-identical descriptions may still refer to the same subject, as long as they convey
consistently matching attributes, share identical subject names, or can be reasonably and clearly
inferred from the caption.
- For example, descriptions with similar attributes such as “a boy with a light-grey shirt” and “the
boy in a grey shirt” should be grouped into the same category.
- Similarly, descriptions that include the same subject name, such as “James”, “James in a white
shirt” and “James, dressed in a dark suit jacket”, should also be grouped into one cluster, even if
their outfits differ, because they contain the same subject name.
- Ensure that every subject description is assigned to exactly one cluster.
List of subject descriptions:
{}
Video Caption:
{}
Output format:
```json
{{
"category_1": ["original subject description 1", "original subject description 2", ...],
"category_2": ["original subject description 3"], // optional
...
}}
```
Figure 12: Prompts for clustering descriptions of the same ground-truth subject.


## Page 21


List of prompts used to evaluate audiovisual video captioning models
1. Provide a comprehensive description of all the content in the video, leaving out no details. Be
sure to include as much of the audio information as possible, and ensure that your descriptions of
the audio and video are closely aligned. Ensure coherence in the description of the same subject
throughout.
2. Thoroughly describe everything in the video, capturing every detail. Include as much information
from the audio as possible, and ensure that the descriptions of both audio and video are well-
coordinated. Ensure coherence in the description of the same subject throughout.
3. Please describe all the information in the video without sparing every detail in it. As you
describe, you should also describe as much of the information in the audio as possible, and pay
attention to the synchronization between the audio and video descriptions. Ensure coherence in the
description of the same subject throughout.
4. Offer a detailed description of the video, making sure to include every detail. Also, incorporate
as much information from the audio as you can, and ensure that your descriptions of the audio and
video are in sync. Ensure coherence in the description of the same subject throughout.
5. Describe every aspect of the video in full detail, covering all the information it contains.
Additionally, include as much of the audio content as you can, and make sure your descriptions of
the audio and video are synchronized. Ensure coherence in the description of the same subject
throughout.
6. Please provide a thorough description of all the content in the video, including every detail. As
you describe, ensure that you also cover as much information from the audio as possible, and be
mindful of the synchronization between the audio and video as you do so. Ensure coherence in the
description of the same subject throughout.
7. Give a detailed account of everything in the video, capturing all the specifics. While doing so,
also include as much information from the audio as possible, ensuring that the descriptions of
audio and video are well-synchronized. Ensure coherence in the description of the same subject
throughout.
Figure 13: List of prompts used to evaluate the audiovisual video captioning models. During evaluation, prompts
are randomly sampled from this list.


## Page 22


List of prompts used to evaluate vision-only video captioning models
1. Provide a comprehensive description of all visible content in the video, leaving out no important
visual details. Describe the subjects, actions, scenes, objects, camera changes, and temporal
progression as clearly as possible. Ensure coherence in the description of the same subject
throughout.
2. Thoroughly describe everything that can be observed in the video. Include detailed information
about the people or subjects, their appearances, actions, interactions, background, scene transitions,
and changes over time. Ensure coherence in the description of the same subject throughout.
3. Please describe all visual information in the video in detail. Focus on the subjects, their actions,
spatial relationships, environment, objects, scene changes, and the overall temporal sequence of
events. Ensure coherence in the description of the same subject throughout.
4. Offer a detailed visual description of the video, making sure to cover important subjects, actions,
interactions, background details, object appearances, camera movements, and scene transitions.
Ensure coherence in the description of the same subject throughout.
5. Describe every visible aspect of the video in full detail. Pay attention to the identities and
appearances of recurring subjects, their actions, interactions, locations, and how the scene evolves
over time. Ensure coherence in the description of the same subject throughout.
6. Please provide a thorough visual description of the video, including all important details.
Describe what happens from beginning to end, and maintain consistent references to the same
subjects throughout the description. Ensure coherence in the description of the same subject
throughout.
7. Give a detailed account of the visual content in the video, capturing the subjects, objects, actions,
backgrounds, scene transitions, and temporal order of events. Ensure that recurring subjects are
described coherently and consistently. Ensure coherence in the description of the same subject
throughout.
Figure 14: List of prompts used to evaluate the vision-only video captioning models. During evaluation, prompts
are randomly sampled from this list.
