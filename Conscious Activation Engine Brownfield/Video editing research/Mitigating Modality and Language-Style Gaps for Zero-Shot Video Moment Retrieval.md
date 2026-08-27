# Mitigating Modality and Language-Style Gaps for Zero-Shot Video Moment Retrieval

*Source PDF: `Mitigating Modality and Language-Style Gaps for Zero-Shot Video Moment Retrieval.pdf`*

*Total Pages: 28*

---


## Page 1


Mitigating Modality and Language-Style Gaps
for Zero-Shot Video Moment Retrieval
Jihyun Lee⋆, Cheol-Ho Cho⋆, Woojin Jun , Woojin Jeong , and Jae-Pil
Heo⋆⋆
Sungkyunkwan University, Suwon, Republic of Korea
Abstract. Zero-shot video moment retrieval (ZMR) aims to overcome
the limitations of traditional approaches that require large-scale datasets
annotated with text and its relevant temporal spans. Despite advances in
pre-trained vision–language models (VLMs) and multimodal large lan-
guage models (MLLMs), existing ZMR methods still heavily depend on
query-to-video content similarity, making them vulnerable to modal-
ity and language-style gaps. These gaps lead to unreliable span pro-
posals and unstable moment retrieval results. To address this issue, we
propose Self-Similarity-based Moment proposal and Scoring (Self-SiMS)
that instead exploits intrinsic relationships within videos, enabling ro-
bust span generation and scoring. By deriving self-similarity only from
the video content, we circumvent the noisy and mismatched patterns
of query–frame or query–caption similarities, thereby mitigating both
modality and language-style gaps. Furthermore, we introduce a query-
aware MLLM-based reasoning stage to further sharpen alignment be-
tween text and video. Extensive experiments demonstrate that Self-SiMS
achieves the state-of-the-art performance across ZMR benchmarks.
1
Introduction
With the rapid expansion of multimedia content, video has become a primary
medium for obtaining information. Consequently, retrieving specific moments
from videos relevant to natural language queries has garnered significant atten-
tion across both academia and industry. A central task in this area is video
moment retrieval (VMR) [2, 8, 17, 45], which aims to localize the most relevant
temporal segment in a video based on a given text query. This task remains par-
ticularly challenging due to the need to pinpoint precise moments within videos
that often contain multiple semantically similar scenes.
Previous studies have primarily focused on training VMR models using datasets
annotated with temporal spans. However, such approaches require extensive
manual labeling, which is both costly and labor-intensive. To overcome this limi-
tation, recent research has explored zero-shot video moment retrieval (ZMR) [29,
⋆These authors contributed equally.
⋆⋆Corresponding author
arXiv:2607.19027v1  [cs.CV]  21 Jul 2026


## Page 2


2
J. Lee et al.
(a) Modality Gap in QF Sim.
Query-Frame similarity
1.0
0.0
Score
Frame
Low & Flat signal
GT moment
Modality Gap
Frame feat.
Query feat.
Frame
Query
(c) Ours – Span Gen. with Self-Sim.
Boundary score
1.0
0.0
Score
Frame
GT moment
Candidate
Span
Two men are looking at 
tools in Home Depot.
(b) Language-style Gap in QC Sim.
Query-Caption similarity
1.0
0.0
Score
Frame
Noisy signal
GT moment
Sim.
MLLM
captions
Query
Language-style Gap
Frames
MLLM
captions
Frame
Self-Sim.
Caption
Self-Sim.
Query
No Modality 
Gaps
No Language-
style Gaps
“…holding a hammer…”
“…reaching for something…”
Fig. 1: Comparison of different similarity computation for candidate span generation.
(a) Query–Frame similarity suffers from a modality gap between textual and visual
features, producing low and flat similarity signals. (b) Query–Caption similarity allevi-
ates modality issues but introduces a language-style gap, yielding noisy and inconsistent
similarity patterns. (c) Our method leverages intra-video self-similarity, avoiding such
modality and language-style gaps, and produces more stable boundary scores.
32,40,46,50], leveraging vision-language models (VLMs) [19,20] and multimodal
large language models (MLLMs) [9, 38, 39] pretrained on large-scale data to
perform retrieval without additional supervision. Although these methods have
shown promising performance in ZMR, they still face a critical limitation stem-
ming from the unreliable query-based similarity score used to generate and score
candidate spans (i.e., moment proposals). Specifically, existing methods [46,50]
rely on the similarity between text query and video contents, represented by
either visual features or MLLM-generated captions. However, these similarities
are inherently affected by modality and language-style gaps, leading to the gen-
eration of unstable spans. Fig. 1 conceptually summarizes how each approach
computes similarity scores and visualizes the score tendencies observed at the
video instance level when applying each method.
As illustrated in Fig. 1(a), methods based on query–frame similarity [50] are
affected by the modality gap between textual and visual representations. Even
inside the ground-truth moment, the similarity can remain low and flat, making
it difficult to distinguish the relevant temporal region from the surrounding con-
text. Query–caption similarity [46] partially alleviates this issue by converting
visual content into text, as shown in Fig. 1(b). However, it introduces a language-
style gap between human-written queries and MLLM-generated captions. Even
for visually similar frames, the captions may focus on different aspects of the
same scene, such as objects, actions, or fine-grained sub-events. For example,
given the query "Two men are looking at tools in Home Depot," captions may
alternately emphasize "holding a hammer" or "reaching for something." These
descriptions can be valid, but their inconsistent focus leads to noisy and unstable
query–caption similarity trajectories.
To avoid relying on such query-dependent signals, we use query-independent
intra-video self-similarity for span generation. As shown in Fig. 1(c), we com-
pute self-similarity maps from both frame features and MLLM-generated cap-
tion features, and derive boundary scores by detecting changes in their temporal


## Page 3


Mitigating Modality and Language-Style Gaps for ZMR
3
(b) IOR distribution Comparison
Query-frame IOR dist.
0.0
1.0
2.0
3.0
4.0
5.0
Query-caption IOR dist.
0.0
1.0
2.0
3.0
4.0
5.0
Self-Sim. IOR dist. (Ours) 
0.0
1.0
2.0
3.0
4.0
5.0
(a) Inner-to-Outer Ratio (IOR) 
Inner
Outer
IOR  =
Query-based Sim. Score 
Frame
Sim.
Inner
Outer
1.0
0.0
GT
Self-Similarity map
Frame
GT
OuterInner
Outer
Frame
Inner > Outer
Fig. 2: Illustration and comparison of the Inner-to-Outer Ratio (IOR). (a) The IOR
measures how much higher the similarity is within the ground-truth (Inner) region than
in the surrounding (Outer) area. The middle and right examples illustrate how the Inner
and Outer regions are obtained from query-based similarity scores and from the self-
similarity map, respectively. (b) Comparison of IOR distributions on the QVHighlights
validation set shows that our method achieves consistently higher IOR values than
query–frame and query–caption similarities, indicating stronger discrimination between
relevant and irrelevant segments.
similarity patterns. These boundary scores are then used to generate candidate
spans. Since this process depends only on the internal structure of the video,
rather than query–frame or query–caption matching, the resulting spans are less
affected by modality and language-style gaps.
While these trends are discovered at the instance level, similar patterns
emerge at the dataset level as well. To further examine these trends at the
dataset level, we define the Inner-to-Outer Ratio (IOR) as a quantitative mea-
sure. Fig. 2(a) illustrates the definition of IOR, which measures how much higher
the similarity is within the ground-truth (Inner) region than in the surrounding
(Outer) area. An IOR above 1.0 indicates stronger similarity within the ground-
truth span, whereas lower values imply weak discrimination, thereby measuring
how well each method separates relevant from irrelevant segments. Fig. 2(b)
reports the IOR distributions on the QVHighlights validation set as a represen-
tative example. The query–frame similarity exhibits IOR values concentrated
around 1.0, corresponding to the flat similarity patterns observed earlier and in-
dicating that the modality gap leads to weak discrimination between inner and
outer regions. The query–caption similarity shows a broad and unstable distribu-
tion, reflecting the noisy similarity trajectories caused by inconsistent alignment
between queries and generated captions. In contrast, our method yields IOR val-
ues consistently above 1.0, indicating that it effectively captures intrinsic video
structure and produces discriminative similarity scores across the dataset.
Building on this idea, we propose Self-Similarity-based Moment Proposal and
Scoring (Self-SiMS), which leverages intra-video self-similarity for both candi-
date generation and span scoring. For span generation, self-similarity provides
query-independent temporal structure, avoiding unstable query-frame or query-
caption signals. For span scoring, we first use the most reliable query-caption
signals within each span and then refine the score with self-similarity to reflect


## Page 4


4
J. Lee et al.
internal content consistency. This design reduces the effect of noisy query-caption
alignment while preserving temporally coherent candidate spans.
Finally, to accurately select the final span from semantically similar span
candidates, we introduce a query-aware MLLM-based re-ranking step. In this
stage, representative frames from each span are directly evaluated against the
query using an MLLM with a yes/no prompt. Instead of computing similarity
after independently generating representations for the query and video, we lever-
age the MLLM’s query-aware capabilities to further reduce both modality and
language-style gaps, resulting in more accurate span scoring.
To sum up, our contributions are as follows:
– We first explicitly identify and address the modality and language-style gaps
in zero-shot video moment retrieval (ZMR), where mismatches between text
queries and video contents, whether visual features or MLLM-generated cap-
tions, can lead to inaccurate span scoring.
– To mitigate these gaps, we propose Self-Similarity-based Moment proposal
and Scoring (Self-SiMS). To the best of our knowledge, our work is the
first to leverage temporal self-similarity for generating candidate spans in a
training-free ZMR, and to score these spans using intra-video relations.
– We further introduce a query-aware MLLM re-ranking step, where candi-
date spans are directly evaluated against the text query using an MLLM to
mitigate the gaps above.
– Our method achieves the state-of-the-art performance on ZMR benchmarks,
demonstrating the effectiveness of combining Self-SiMS with query-aware
MLLM re-ranking in mitigating modality and language-style gaps and im-
proving ZMR.
2
Related works
Video moment retrieval. Video moment retrieval (VMR) aims to retrieve
relevant temporal segments from an untrimmed video given a natural language
query. Early work treated this as a query-to-segment matching problem using
joint video–text feature learning and alignment techniques [2,8,15]. With the in-
troduction of large-scale datasets such as ActivityNet [3] and QVHighlights [17],
subsequent methods explored attention mechanisms, cross-modal transformers,
and contrastive learning for improved localization [17, 20, 26, 37, 45, 47]. Recent
approaches also leverage pre-trained vision–language models (VLMs) such as
BLIP [20], BLIP-2 [19], and instruction-tuned video models [28, 49], achieving
strong results in moment retrieval and highlight detection. However, these ad-
vances still rely on large-scale span annotations, motivating research into weakly-
supervised and zero-shot retrieval.
Zero-shot video moment retrieval. Traditional VMR approaches rely on
densely annotated datasets that precisely align queries with video moments [17,
37], but such annotations are costly and labor-intensive, motivating research


## Page 5


Mitigating Modality and Language-Style Gaps for ZMR
5
into zero-shot video moment retrieval (ZMR) [29, 40]. Early zero-shot methods
leveraged pretrained VLMs such as CLIP [32] to compute query–frame similarity
without training data [29], yet they struggled to capture temporal relationships.
Moreover, recent studies show that off-the-shelf multimodal large language mod-
els (MLLMs) can achieve competitive zero-shot performance without additional
training [7, 10, 25, 42]. Despite these advances, existing methods still rely on
query–video content similarity using either visual features or MLLM-generated
captions for candidate span generation and scoring, which makes them vulner-
able to modality and language-style gaps and limits precise moment localization.
Modality and language-style gaps in text-visual alignment. Pretrained
VLMs [19, 20, 32] trained on large-scale text–image pairs have advanced cross-
modal understanding, yet a modality gap remains, causing inaccurate similar-
ity matching. Prior works address this by introducing learnable gap parame-
ters [43], enhancing semantic modeling [24], or generating captions with MLLMs
to bridge text and visuals. However, MLLM-generated captions inherently create
a language-style gap with human-written queries, which some studies mitigate
by augmenting queries with complementary descriptions [22, 46]. Despite these
prior efforts, ZMR still suffers from both gaps, often leading to unreliable span
generation and scoring. Therefore, we propose a novel framework that leverages
video-intrinsic self-relationships to mitigate them jointly.
Self-similarity for temporal boundary modeling. Self-similarity has been
studied as a fundamental cue for capturing internal relational patterns in images
and videos [35]. Building on this idea, recent works exploit temporal similarity
to obtain pseudo temporal proposal during training. PSVL [29], a training-based
MR method, constructs a frame-wise self-similarity matrix to discover pseudo
event regions and pairs them with pseudo queries, which are then used to train
a localization model. Similarly, another training-based video grounding frame-
work [13] segments videos using a temporal similarity matrix and trains a ground-
ing model by aligning the resulting pseudo proposals with pseudo language fea-
tures in a pretrained vision-language space. In contrast, we alleviate modality
and language-style gaps in a training-free manner: we derive query-agnostic can-
didate spans from intra-video self-similarity and perform span scoring, thereby
reducing reliance on unstable query-dependent similarity scores.
3
Method
3.1
Overview
Given an untrimmed video V = {vi}L
i=1 with L sampled frames and a tex-
tual query Q, zero-shot video moment retrieval aims to localize the temporal
span aligned with Q without requiring any training. Fig. 3 illustrates the overall
pipeline of Self-SiMS. We first extract frame features F f and frame-wise caption
features F c, and use them to build two temporal self-similarity maps, M f and
M c. These maps are merged into a unified self-similarity map M, from which


## Page 6


6
J. Lee et al.
walking 
down...
MLLM
Aggregates 𝑴𝒇 and 𝑴𝒄 to 𝑴 
1 1 0
1 1 0
0 0 0 0 0
0 1 1
0 1 1
-1 -1
-1
-1
-1
-1
-1
-1
Sec 3.2 Self-Sim based Span Gen.
Sec 3.3 Scoring w/ Self-Sim Aware.
Sec 3.4 Q-Aware MLLM Re-ranking
gu
Query-Aware MLLM
Sampling 𝑵𝑹 frames with Q-C scores 
Candidate Spans 
Select top-𝒌𝑪 spans according to 𝑺 
Text query
Prompting with frame and query
Text query
𝑺(𝟏)
∗ 
Re-rank candidate spans with 𝑺∗ 
0.9
0.5
𝑀𝑓
Frame Temporal 
Self-similarity
Caption Temporal 
Self-similarity
Contrastive Kernel 𝑲
Candidate Spans ℇ
Rank Candidates with 𝑺
‘Rank 1’ 
, 𝑺𝒏
‘Rank 1’ 
‘Rank 𝒌𝑪’ 
, 𝑺(𝟏)
, 𝑺(𝒌𝑪)
Yes,  48%
Yes,  93%
𝑺(𝒌𝑪)
∗
 
Boundary Score 
‘Rank 1’ 
, 𝑺(𝒌𝑪)
∗
𝑀
…
Encoder
Encoder
𝑀𝑐
𝑺𝒏
𝑸 
Q-C scores 
𝑺𝒏𝑺 
Part of 𝑴 
Key 
Frame
𝜿𝒏
Span 
Score 𝑺𝒏 
𝑬𝒏
Average
Average top-𝒌𝑺
𝑵𝑲
𝜿𝒏.
Fig. 3: The overview of our Self-Similarity based Moment proposal and Scoring (Self-
SiMS). First, features from the frames and captions are extracted to construct two
distinct self-similarity maps, M f and M c, which are then aggregated into a unified map,
M. Each frame is then evaluated with a boundary score computed using a contrastive
kernel, and candidate spans are generated in temporal order (Sec. 3.2). Next, the spans
are ranked based on query-matching span score SQ, which is computed by averaging
the top-kS query-caption scores. In addition, the self-matching span score SS is derived
from the unified Self-similarity map M and then combined with the former score (Sec.
3.3). Finally, the MLLM-based reranking is applied to the top-ranked spans by asking
whether each query-frame pair is relevant, and the probability of the ’Yes’ answer is
used as the score (Sec. 3.4).
we compute boundary scores with a contrastive kernel and generate candidate
spans. Each candidate is then scored by combining the Query-Matching Span
Score SQ, computed from the top-kS query–caption similarities within the span,
and the Self-Matching Span Score SS, which measures internal span consistency
using M. The combined score S ranks the candidates, and the top-kC spans are
further re-ranked by an MLLM through a query-aware Yes/No verification.
Span Boundary Scores. Inspired by the event boundary detection method
proposed in
[12], we calculate self-similarity to construct the Temporal Self-
similarity Matrix (TSM), M ∈RL×L. First, we apply ℓ2-normalization to the
extracted features, F f for frames and F c for captions, resulting in ˆF f and ˆF c,
respectively. Then, the TSMs for the frames and captions are computed as M f =
ˆF f( ˆF f)⊤and M c = ˆF c( ˆF c)⊤. To integrate both modalities, we construct the
unified TSM M by equally weighting M f and M c, i.e., M = 1
2(M f + M c).
To evaluate whether a frame is likely to be a boundary, we examine a local
patch of the self-similarity map around that frame. Intuitively, a good boundary
separates two temporally coherent regions. Frames before the boundary should
be similar to each other, frames after the boundary should also be similar to each
other, but frames across the boundary should be less similar. The contrastive
kernel captures this pattern by rewarding within-side similarities and penalizing
cross-side similarities. Specifically, the kernel K ∈RNK×NK has positive weights


## Page 7


Mitigating Modality and Language-Style Gaps for ZMR
7
in the top-left and bottom-right quadrants, negative weights in the top-right and
bottom-left quadrants, and zeros in the central row and column. The boundary
score of the i-th frame is computed as
  b _i  = P_i \odot K, 
(1)
where Pi is an NK ×NK patch of M centered at the diagonal position (i, i), and
⊙denotes element-wise multiplication. The TSM is zero-padded so that this
operation can be applied uniformly to every frame.
Candidate Spans. To generate candidate spans from the boundary scores,
we define a set of instance-wise dynamic thresholds T = {τ1, τ2, . . . , τNT }, which
adapt to the intra-video context variability measured from the frame features F f.
Based on this variability, videos with more diverse contexts are assigned lower
thresholds for finer temporal partitioning, whereas more homogeneous videos
receive higher thresholds for coarser segmentation. This variability-aware de-
sign removes the need for manual threshold tuning and generalizes well across
datasets. Detailed formulations are provided in the Appendix. For each τj ∈T ,
we construct boundary set Bj containing the indices of frames that are both
above the threshold and correspond to local maxima of the boundary scores:
  \ m a t hc a l { B} _ j = \ {\ ,  i \ ; \ mid  \; b_i \geq \tau _j,\; b_i \geq b_{i-1},\; b_i \geq b_{i+1} \,\} \;\cup \; \{1, L\}. 
(2)
Here, the two extreme frames, 1 and L, are included to ensure that the candidate
spans cover the entire duration of the video. By the boundary set, we obtain a
candidate span En formally defined as:
  E _n  = 
\ { i  \;
\mi
d  \;
 e _n
^ s  \le i \le e_n^e \}, \quad 1 \leq e_n^s < e_n^e \leq L, 
(3)
where each pair (es
n, ee
n) is formed by two successive frame indices in the temporal
order within the same boundary set Bj, thereby ensuring that the resulting
different spans do not overlap. Finally, the set of all candidate spans across
thresholds is formally denoted by
  \mat hca l  { E } = \{E_1, E_2, \dots , E_{N_{s}}\}, 
(4)
where Ns denotes the total number of candidate spans. Note that each En in
this set refers to the corresponding candidate span and can be referred to as the
“n-th span” in subsequent descriptions.
3.2
Span Scoring with Self-Similarity Awareness
To identify the relevant candidate span, each span should have its relevance
score with the query. Previous approach [46] computes this score by averaging
the frame-level similarities between the query and captions. However, such mean-
based scoring is unreliable, as query–caption similarity often exhibits noisy and
inconsistent distributions due to the language-style gap.


## Page 8


8
J. Lee et al.
To mitigate this limitation, we use the top-kS frame-level similarities within
the span for scoring, which are robust to the corruption induced by the language-
style gap. In addition, to enhance the reliability of scoring, we propose the Self-
Matching Span Score, derived from TSM. Finally, each candidate span is scored
by combining the Query-Matching Span Score and the Self-Matching Span Score.
Query–Matching Span Score. Given a textual query Q, we extract the query
feature F q using the same encoder employed for the caption features F c. Then,
the cosine similarity between the query feature and caption features is calculated
to produce the frame-level scores Sf ∈RL as follows:
  
\ l
a b e l  
{
eq :f ra m
e _score} S^f_i = \frac {F^q \cdot F^c_i}{\|F^q\| \; \|F^c_i\|}, 
(5)
where F c
i and Sf
i denote the caption feature and frame-level score of the i-th
frame, respectively. The Query-Matching Span Score (QMS), denoted as SQ, is
defined as the mean of the top-kS frame scores within each span. Specifically,
for the n-th span En, containing the indices from the start to the end frames es
n
and ee
n, the score is computed as follows:
  
S ^ Q
_n
 =
 
\
frac 
{
1
} { k_S
} 
\
su
m  _{i=e^\text {s}_n}^{e^\text {e}_n} \mathbf {1}\left [i \in I_{k_S}^{E_n}\right ] S^f_i, 
(6)
where IEn
kS is a set of indices with the top-kS highest frame-level scores defined
in Eq. (5) within En. This approach prioritizes the most relevant frames over
the average, helping to mitigate noise in the query–caption similarity by using
the most reliable scores. As a result, the span score more reliably reflects each
span’s relevance to the query.
Self-Matching Span Score. However, relying solely on a subset of sampled
frames inherently limits the ability to capture alignment between the query and
the full temporal context of a span. To address this issue, we leverage the previ-
ously computed TSM used in span generation to evaluate contextual consistency
within the span while reducing the influence of the language-style gap. The Self-
Matching Span Score (SMS), denoted as SS, is defined as the mean similarity
between the key frame, which is the frame with the highest frame-level score in
the span, and all other frames within that span. Let κn denote the index of the
key frame in the span En, that is,
  \ kap pa 
_n =  \
a rg \max _{i \in E_n} S^f_i. 
(7)
Then, SMS for the n-th candidate span is calculated as
  
S ^
S
_n =
 
\fra
c {1}{|E_n|} \sum _{j \in E_n} M_{\kappa _n, j}, 
(8)


## Page 9


Mitigating Modality and Language-Style Gaps for ZMR
9
where Mi,j denotes the element of the TSM M at the position (i, j). As a result,
candidate spans that are longer yet include inconsistent contexts are suppressed
through reduced span scores. Finally, the total score Sn of the candidate span
is weighted sum of SQ
n and SS
n as follows:
  S _n  = (1
- \ a lp
ha
 ) \, S^Q_n + \alpha \, S^S_n, \quad \alpha \in [0,1], 
(9)
where α is a hyperparameter for the span score weights.
3.3
Query-Aware Gap Reduction via MLLM Re-Ranking
Recent remarkable advances in multimodal large language models (MLLMs) have
demonstrated exceptionally strong cross-modal reasoning ability, making them
effective for re-ranking tasks [6,11,21,36]. Building on this, we further reduce the
language-style gap between queries and MLLM-generated captions by refining
candidate spans through MLLM-based re-ranking.
Concretely, we re-rank the top-kC candidate spans from the initial scoring
stage, ranked according to their span score S. Let S(m) and E(m) denote the m-
th highest span score and its corresponding candidate span, where 1 ≤m ≤kC.
Within each selected span, we sample NR representative frames according to
their query–caption similarity score. Further details of the NR frame sampling
process are provided in the Appendix. Then, each representative frame is evalu-
ated by the MLLM using a Yes/No prompt, and the resulting logits are converted
into probabilities via softmax. The resulting Yes probability is used as Sr
i , denot-
ing the frame-level re-ranking score for the i-th frame. By averaging the top-kR
highest values from the set of frame-level re-ranking scores Sr
i , we compute the
span-level re-ranking score SR
(m). Finally, S∗
(m), the final score of E(m), is defined
as a weighted combination of the initial span score S(m) and the MLLM-based
re-ranking signal SR
(m):
  
S_{ ( m) } ^*  = ( 1 - \b
eta 
) \ , S _{(m)} + \beta \, S_{(m)}^R, \quad \beta \in [0,1], 
(10)
where β is a weighting parameter. This re-ranking process leverages the MLLM’s
cross-modal reasoning to directly verify semantic alignment between the query
and candidate captions, rather than relying solely on similarity scores, enabling
query-aware reasoning and more reliable selection of the most relevant spans.
4
Experiments
4.1
Experimental Setup
Datasets. We evaluate our method on four widely used benchmarks. QVHigh-
lights [17] includes user-generated videos with fine-grained highlight annotations.
Charades-STA [8] contains indoor daily activities paired with temporal sentence


## Page 10


10
J. Lee et al.
Method
Setting
QVHighlights test
QVHighlights val
R1@0.5 R1@0.7 mAP@0.5 mAP@avg R1@0.5 R1@0.7 mAP@0.5 mAP@avg
Moment-DETR [17]
FS
52.9
33.0
54.8
30.7
54.2
33.4
55.4
31.1
UMT [23]
FS
56.4
40.8
53.1
35.4
-
-
-
-
CPL [52]
WS
30.8
10.8
22.8
-
-
-
-
-
CPI [14]
WS
32.3
11.8
23.7
-
-
-
-
-
TFVTG‡ [50]
ZS
21.6
8.0
20.1
7.9
21.0
7.4
19.2
7.3
Moment-GPT [46]
ZS
58.3
37.7
55.1
35.0
58.9
38.6
55.7
35.9
Self-SiMS (Ours)
ZS
59.7
42.2
59.2
38.3
61.0
43.2
60.5
39.3
Table 1: Comparison on QVHighlights test and validation sets. FS: Fully Supervised,
WS: Weakly Supervised, ZS: Zero-Shot. ‡: Reproduced with the same LLM and FPS
with ours.
descriptions. ActivityNet-Captions [15] covers diverse human activities with tem-
porally aligned captions. Additionally, we incorporate TVR [18], which features
long-form videos and complex natural language queries, to further validate the
generalizability of our approach across varied video–language domains.
Metrics. Following prior zero-shot video moment retrieval (ZMR) works, we
evaluate our method using standard metrics tailored to each dataset. For QVHigh-
lights, we report Recall@1 at IoU thresholds of 0.5 and 0.7, along with mAP@0.5
and the average mAP across multiple thresholds. These metrics jointly reflect
the retrieval accuracy and the quality of segment ranking. For Charades-STA,
ActivityNet-Captions, and TVR, we adopt R1@0.3/0.5/0.7 and mean IoU (mIoU),
which evaluate both temporal localization precision and the alignment between
predicted and ground-truth segments.
Implementation Details. We set the frame rates of QVHighlights, Charades-
STA, ActivityNet-Captions, and TVR to 0.5, 1, 1, and 1 fps, respectively. Fol-
lowing prior work [46], we use 0.5 fps for QVHighlights, and we set the remaining
datasets to 1 fps for consistency. We employ LLaMA-3.2-11B-Vision-Instruct [9]
for both video frame captioning and the final re-ranking stage. For scoring,
the number of top scores is fixed at 3 for both initial span scoring (kS) and
re-ranking (kR). We re-rank the top-kC candidate spans with kC = 5. In the
re-ranking stage, NR frames are sampled from each span, set to half of the span
length with lower and upper bounds of 10 and 30, respectively. The weighting
parameters for the final span score, α and β, are set to 0.1 and 0.5, respectively.
All experiments are conducted on an NVIDIA RTX A6000 GPU.
4.2
Comparison With the State-of-the-Arts
Tabs. 1,2, and 3 report the performance of various ZMR methods across bench-
mark datasets. In Tab. 1, Self-SiMS outperforms existing ZMR baselines across
all evaluation metrics on the QVHighlights. Note that TFVTG‡ was reproduced
using the same large language model (LLM) employed in our framework, since
TFVTG does not officially provide LLM rephrasing output for QVHighlights.
Tab. 2 presents the performance comparison on Charades-STA and ActivityNet-
Captions. To ensure fairness, we reproduced TFVTG† at 1 fps, as the original


## Page 11


Mitigating Modality and Language-Style Gaps for ZMR
11
Method
Setting
Charades-STA
ActivityNet-Captions
R1@0.3 R1@0.5 R1@0.7 mIoU R1@0.3 R1@0.5 R1@0.7 mIoU
VTimeLLM [10]
FS
55.3
34.3
14.7
34.6
44.8
29.5
14.2
31.4
Moment-DETR [17]
FS
62.1
48.2
25.3
42.3
52.6
32.5
15.3
37.8
CNM [51]
WS
50.0
36.2
14.2
34.2
51.3
30.3
11.4
33.9
CPL [52]
WS
56.0
38.1
20.3
37.8
52.4
30.9
12.0
32.6
TFVTG† [50]
ZS
64.7
29.8
9.8
38.2
49.9
26.8
12.6
34.2
TFVTG‡ [50]
ZS
64.8
30.0
10.1
38.4
49.5
26.5
12.3
34.0
Moment-GPT [46]
ZS
58.2
38.4
21.6
36.5
48.1
31.1
14.9
30.8
Self-SiMS (Ours)
ZS
62.7
39.7
21.0
41.9
49.9
28.2
13.8
34.7
Table 2: Comparative evaluation on Charades-STA and ActivityNet-Captions. ZS:
Zero-Shot. †: Reproduced results with the same FPS with ours. ‡: Reproduced with
the same LLM and FPS with ours.
Method
TVR
s
f
R1@0.3 R1@0.5 R1@0.7 mIoU
40 1.0
13.1
6.0
3.0
15.1
TFVTG‡ [50] 50 0.5
14.4
6.9
2.7
15.4
20 0.5
21.7
9.6
4.0
18.6
Ours
-
-
26.6
13.5
6.1
20.2
Table 3: Comparison on TVR validation dataset. For the baseline methods, s
(stride) and f (max stride factor) are dataset-specific hyperparameters as reported
in TFVTG [50].
results were reported at 3 fps. TFVTG achieves relatively high R@0.3 and mIoU
but exhibits clear drops at higher IoU thresholds (R1@0.5 and R1@0.7), as its
query–visual similarity often results in overly long spans. Conversely, Moment-
GPT performs better at higher thresholds but worse at R@0.3 and mIoU, in-
dicating that its query–caption similarity produces precise yet unstable short
matches. In contrast, our Self-SiMS overcomes these issues by producing more
consistent spans aligned with the ground-truth, achieving the highest mIoU and
more reliable temporal localization while maintaining competitive recall.
Tab. 3 summarizes the evaluation on the TVR dataset. As the official imple-
mentation of Moment-GPT is unavailable, we omit its results for fairness. For
TFVTG, we report multiple configurations using the hyperparameters s (stride)
and f (max stride factor) as specified in the original paper, ensuring a fair
comparison. Our Self-SiMS consistently surpasses the baseline across all param-
eter settings, marking a substantial improvement. Moreover, while the baseline
requires dataset-specific hyperparameter tuning, Self-SiMS delivers strong per-
formance with a single configuration, highlighting its robustness.
4.3
Ablation Studies
Length of Candidate Spans Analysis.
Fig. 4 illustrates the candidate span length distributions on Charades-STA
(left) and ActivityNet-Captions (right). The ground-truth (GT) distribution is
indicated by the red dashed line. This analysis helps explain the performance


## Page 12


12
J. Lee et al.
0
50
100
150
length
0
5
10
15
20
25
length
counts
counts
TFVTG
Moment-GPT
Self-SiMS (Ours)
GT
Average of all GTs
2000
6000
10000
1000
3000
5000
15000
25000
Fig. 4: Histogram of all span lengths on Charades-STA (left) and ActivityNet-Captions
(right).
Method
Oracle-mIoU (%) Avg. # Span Cand.
TFVTG
38.16
8.38
Moment-GPT
65.01
7.62
Self-SiMS (Ours)
71.13
6.46
Table 4: Comparison of Oracle mIoU
on the QVHighlights validation set.
Avg. # Span Cand. denotes the aver-
age number of span candidates across
on dataset.
5.0
0.0
1.0
2.0
3.0
4.0
0.0
1.0
2.0
3.0
1.5
1.5
2.5
Query-Frame sim.
Query-Caption sim.
Self-sim. (Ours)
IOR = 1
Inner > Outer
Fig. 5: Inner-to-Outer Ratio (IOR) distri-
butions on Charades (left) and ActivityNet-
Captions (right).
differences observed on these two datasets, particularly the recall tendencies in
Tab. 2. TFVTG, affected by the modality gap, produces uniform similarity scores
with weak temporal distinction. Consequently, it often produces excessively long
spans, achieving relatively high R@0.3 but exhibiting clear degradation under
stricter IoU thresholds. Conversely, Moment-GPT suffers from a language-style
gap, leading to noisy and unstable similarity score distribution. These sharp,
unstable peaks often yield overly short spans that perform better under tight
criteria such as R@0.7 yet fail to capture full GT intervals. In contrast, our Self-
SiMS generates balanced spans that align more closely with the GT distribution
by leveraging self-similarity free from such modality and style gaps, resulting in
higher mIoU and more consistent temporal localization performance.
Effectiveness of Span Generator. To validate the effectiveness of our span
generator, we evaluate Oracle mIoU on the QVHighlights, comparing against
TFVTG [50] and Moment-GPT [46]. Oracle mIoU is defined as the mean IoU
obtained by selecting the candidate span with the maximum overlap with the
ground truth, reflecting the quality of the span candidates. As shown in Tab. 4,
our method achieves an Oracle mIoU of 71.13, outperforming both baselines.
Moreover, although this performance generally increases with a larger number
of candidate spans, our method achieves the best results despite requiring the
lowest average number of candidates (6.46). This improvement demonstrates
that our method generates more reliable spans by capturing the intrinsic struc-
ture of the video while avoiding modality and language-style gaps.
Inner-to-Outer Ratio Distribution. Fig. 5 reports IOR distributions on
Charades-STA and ActivityNet-Captions, where higher IOR values indicate stronger
separation between the ground-truth span and surrounding background. Self-


## Page 13


Mitigating Modality and Language-Style Gaps for ZMR
13
Method
R1@0.5 R1@0.7 mAP@0.5 mAP@avg
Mean scoring
55.7
40.9
56.7
37.1
QMS
59.5
42.1
59.4
38.6
+ SMS
60.3
42.9
59.6
38.7
+ Re-ranking
61.0
43.2
60.5
39.3
Table 5: Scoring component analysis
of our scoring methods. QMS denotes
the Query-Matching Score, and SMS
denotes the Self-Matching Span Score.
Model
Component MLLM / LLM
#Params
Runtime
TFVTG
Rephrasing
GPT4-Turbo [1] ≥100B (est.)
–
Moment-GPT
Rephrasing
LLaMA3 [9]
8B
6.3s
Captioning
MiniGPT-v2 [5]
7B
249.4s
Reranking
V-ChatGPT [27]
7B
7.4s
Ours
Captioning
LLaMA3.2-V [9]
11B
140.7s
Reranking
LLaMA3.2-V [9]
11B
13.0s
Captioning
MiniGPT-v2 [5]
7B
249.4s
Reranking
MiniGPT-v2 [5]
7B
9.7s
Table 6: Comparison of MLLM/LLM usage,
model scale, and per-video runtime across
TFVTG, Moment-GPT, and our method.
SiMS shows higher and more stable IOR values, demonstrating that its self-
similarity-based boundary scores capture temporal segments more reliably and
lead to robust localization.
Scoring Component Analysis. We conduct an ablation study on the QVHigh-
lights validation set to analyze the contribution of each component in our pro-
posed scoring and re-ranking pipeline, with the results presented in Tab. 5. The
baseline adopts naive mean scoring, which averages all frame-level scores within
a span, as in prior methods. Replacing mean scoring with the Query-Matching
Span Score (QMS) yields improvements across all metrics, supporting our hy-
pothesis that employing the most relevant signals is more effective than relying
on the average of noisy query-caption scores. Adding the Self-Matching Span
Score (SMS) on QMS further increases performance, particularly for recall-based
metrics such as R1@0.5 and R1@0.7, indicating that incorporating the entire
span context through self-similarity enables more precise localization of ground-
truth moments. Finally, incorporating MLLM re-ranking on top of QMS with
SMS yields additional gains across all metrics by leveraging the MLLM’s ability
to understand cross-modal information. This demonstrates that each component
of the pipeline contributes effectively to the overall performance.
Complexity comparison. We compare the per-video runtime of TFVTG [50],
Moment-GPT [46], and our method using 100 randomly sampled videos from
Charades-STA [8]. Since non-MLLM/LLM components, such as our scoring
stage, are lightweight (0.194s per video), we focus on MLLM/LLM-dependent
stages and use a frame batch size of 1 for both captioning and reranking.
Tab. 6 summarizes the model configurations and runtimes. TFVTG uses GPT-4
Turbo [1] for query rephrasing. Its runtime cannot be directly measured because
it is accessed through a commercial API, and its model size is estimated to ex-
ceed 100B parameters. Moment-GPT employs three separate models for query
rephrasing, captioning, and reranking, resulting in a total footprint of 22B pa-
rameters. In contrast, our default setting uses a single LLaMA-3.2-Vision [9]
model family for both captioning and reranking, reducing the model footprint
to 11B parameters. Furthermore, reranking is computationally efficient because
it evaluates only a small number of sampled representative frames. To ensure
a fair comparison under the same MLLM, we additionally replace LLaMA-3.2-
Vision with MiniGPT-v2, which is also adopted by Moment-GPT. Under this


## Page 14


14
J. Lee et al.
Text Query: Man talks to the camera under candlelight.
Ground-Truth
54s
82s
Text Query: person running up.
Ground-Truth
13.0s
21.7s
Ours
54s
82s
16s
TFVTG
100s
36s
60s
0
1
0
1
0
1
0
1
0
1
0
1
21.7s
12.8s
Ours
22.0s
10.0s
Moment-GPT
TFVTG
20.7s
4.9s
12s
108s
0.0s
21.7s
Moment-GPT
Fig. 6: Qualitative results on QVHighlights (left) and Charades-STA (right).
setting, the captioning cost is identical to that of Moment-GPT, while the rerank-
ing stage is slightly faster than when using LLaMA-3.2-Vision. Detailed perfor-
mance results obtained with MiniGPT-v2 are provided in the supplementary
MLLM ablation study. Notably, our method achieves comparable or superior
performance while using the same MLLM backbone.
4.4
Qualitative results
We provide a qualitative comparison in Fig. 6, illustrating span localization
results, TFVTG [50], Moment-GPT [46], and our method, along with the corre-
sponding span candidate score distributions. TFVTG, which relies on query–visual
frame similarity, generates overly long and inaccurate spans due to the modal-
ity gap that hinders fine-grained semantic alignment. Moment-GPT, which in-
stead depends on query–caption similarity, suffers from a language-style gap
that produces inconsistent similarity maps and hampers accurate localization.
In contrast, Self-SiMS leverages boundary scores derived from the self-similarity,
enabling robust localization of the correct spans.
5
Conclusion
In this paper, we first define the modality and language-style gaps in zero-shot
video moment retrieval (ZMR), and quantify their impact using the Inner-to-
Outer Ratio (IOR), which measures how well a similarity score separates the
ground-truth span from the surrounding background. To mitigate these gaps, we
propose Self-Similarity-based Moment Proposal and Scoring (Self-SiMS), which
leverages intra-video self-similarity for both span generation and scoring. Ex-
periments and ablations show that Self-SiMS mitigates errors from unreliable
query-dependent similarity and achieves robust performance, demonstrating self-
similarity as an effective cue for training-free ZMR.
Acknowledgements
This work was supported in part by MSIT/IITP (No. RS-2022-II220680, RS-
2020-II201821, RS-2019-II190421, RS-2024-00459618, RS-2024-00360227, RS-2024-
00437633, RS-2024-00437102, RS-2025-25442569), MSIT/NRF (No. RS-2024-
00357729), KNPA/KIPoT (No. RS-2025-25393280), and SEMES-SKKU collab-
oration funded by SEMES.


## Page 15


Mitigating Modality and Language-Style Gaps for ZMR
15
References
1. Achiam, J., Adler, S., Agarwal, S., Ahmad, L., Akkaya, I., Aleman, F.L., Almeida,
D., Altenschmidt, J., Altman, S., Anadkat, S., et al.: Gpt-4 technical report. arXiv
preprint arXiv:2303.08774 (2023)
2. Barrett, D.P., Barbu, A., Siddharth, N., Siskind, J.M.: Saying what you’re looking
for: Linguistics meets video search. IEEE transactions on pattern analysis and
machine intelligence 38(10), 2069–2081 (2015)
3. Caba Heilbron, F., Escorcia, V., Ghanem, B., Carlos Niebles, J.: Activitynet: A
large-scale video benchmark for human activity understanding. In: Proceedings of
the ieee conference on computer vision and pattern recognition. pp. 961–970 (2015)
4. Chatterjee, D., Remelli, E., Song, Y., Tekin, B., Mittal, A., Bhatnagar, B., Camgoz,
N.C., Hampali, S., Sauser, E., Ma, S., et al.: Streaming videollms for real-time
procedural video understanding. In: Proceedings of the IEEE/CVF International
Conference on Computer Vision. pp. 22586–22598 (2025)
5. Chen, J., Zhu, D., Shen, X., Li, X., Liu, Z., Zhang, P., Krishnamoorthi, R., Chan-
dra, V., Xiong, Y., Elhoseiny, M.: Minigpt-v2: large language model as a unified
interface for vision-language multi-task learning. arXiv preprint arXiv:2310.09478
(2023)
6. Chen, Z., Xu, C., Qi, Y., Guo, J.: Mllm is a strong reranker: Advancing mul-
timodal retrieval-augmented generation via knowledge-enhanced reranking and
noise-injected training. arXiv preprint arXiv:2407.21439 (2024)
7. Diwan, A., Peng, P., Mooney, R.: Zero-shot video moment retrieval with off-the-
shelf models. In: Transfer Learning for Natural Language Processing Workshop.
pp. 10–21. PMLR (2023)
8. Gao, J., Sun, C., Yang, Z., Nevatia, R.: Tall: Temporal activity localization via
language query. In: Proceedings of the IEEE international conference on computer
vision. pp. 5267–5275 (2017)
9. Grattafiori, A., Dubey, A., Jauhri, A., Pandey, A., Kadian, A., Al-Dahle, A., Let-
man, A., Mathur, A., Schelten, A., Vaughan, A., et al.: The llama 3 herd of models.
arXiv preprint arXiv:2407.21783 (2024)
10. Huang, B., Wang, X., Chen, H., Song, Z., Zhu, W.: Vtimellm: Empower llm to
grasp video moments. In: Proceedings of the IEEE/CVF Conference on Computer
Vision and Pattern Recognition. pp. 14271–14280 (2024)
11. Jin, C., Peng, H., Zhao, S., Wang, Z., Xu, W., Han, L., Zhao, J., Zhong, K.,
Rajasekaran, S., Metaxas, D.N.: Apeer: Automatic prompt engineering enhances
large language model reranking. In: Companion Proceedings of the ACM on Web
Conference 2025. pp. 2494–2502 (2025)
12. Kang, H., Kim, J., Kim, T., Kim, S.J.: Uboco: Unsupervised boundary contrastive
learning for generic event boundary detection. In: Proceedings of the IEEE/CVF
Conference on Computer Vision and Pattern Recognition. pp. 20073–20082 (2022)
13. Kim, D., Park, J., Lee, J., Park, S., Sohn, K.: Language-free training for zero-
shot video grounding. In: Proceedings of the IEEE/CVF Winter Conference on
Applications of Computer Vision. pp. 2539–2548 (2023)
14. Kong, S., Li, L., Zhang, B., Wang, W., Jiang, B., Yan, C., Xu, C.: Dynamic
contrastive learning with pseudo-samples intervention for weakly supervised joint
video mr and hd. In: Proceedings of the 31st ACM International Conference on
Multimedia. pp. 538–546 (2023)
15. Krishna, R., Hata, K., Ren, F., Fei-Fei, L., Carlos Niebles, J.: Dense-captioning
events in videos. In: Proceedings of the IEEE international conference on computer
vision. pp. 706–715 (2017)


## Page 16


16
J. Lee et al.
16. Lee, C., Roy, R., Xu, M., Raiman, J., Shoeybi, M., Catanzaro, B., Ping, W.:
Nv-embed: Improved techniques for training llms as generalist embedding models
(2025), https://arxiv.org/abs/2405.17428
17. Lei, J., Berg, T.L., Bansal, M.: Detecting moments and highlights in videos via
natural language queries. Advances in Neural Information Processing Systems 34,
11846–11858 (2021)
18. Lei, J., Yu, L., Berg, T.L., Bansal, M.: Tvr: A large-scale dataset for video-
subtitle moment retrieval. In: Computer Vision–ECCV 2020: 16th European Con-
ference, Glasgow, UK, August 23–28, 2020, Proceedings, Part XXI 16. pp. 447–463.
Springer (2020)
19. Li, J., Li, D., Savarese, S., Hoi, S.: Blip-2: Bootstrapping language-image pre-
training with frozen image encoders and large language models. In: International
conference on machine learning. pp. 19730–19742. PMLR (2023)
20. Li, J., Li, D., Xiong, C., Hoi, S.: Blip: Bootstrapping language-image pre-training
for unified vision-language understanding and generation. In: International confer-
ence on machine learning. pp. 12888–12900. PMLR (2022)
21. Lin, S.C., Lee, C., Shoeybi, M., Lin, J., Catanzaro, B., Ping, W.: Mm-embed: Uni-
versal multimodal retrieval with multimodal llms. arXiv preprint arXiv:2411.02571
(2024)
22. Liu, D., Qu, X., Dong, J., Nan, G., Zhou, P., Xu, Z., Chen, L., Yan, H., Cheng, Y.:
Filling the information gap between video and query for language-driven moment
retrieval. In: Proceedings of the 31st ACM International Conference on Multimedia.
pp. 4190–4199 (2023)
23. Liu, Y., Li, S., Wu, Y., Chen, C.W., Shan, Y., Qie, X.: Umt: Unified multi-modal
transformers for joint video moment retrieval and highlight detection. In: Proceed-
ings of the IEEE/CVF conference on computer vision and pattern recognition. pp.
3042–3051 (2022)
24. Liu, Z., Li, J., Xie, H., Li, P., Ge, J., Liu, S.A., Jin, G.: Towards balanced alignment:
Modal-enhanced semantic modeling for video moment retrieval. In: Proceedings of
the AAAI conference on artificial intelligence. vol. 38, pp. 3855–3863 (2024)
25. Luo, D., Huang, J., Gong, S., Jin, H., Liu, Y.: Zero-shot video moment retrieval
from frozen vision-language models. In: Proceedings of the IEEE/CVF winter con-
ference on applications of computer vision. pp. 5464–5473 (2024)
26. Ma, K., Zang, X., Feng, Z., Fang, H., Ban, C., Wei, Y., He, Z., Li, Y., Sun, H.:
Llavilo: Boosting video moment retrieval via adapter-based multimodal modeling.
In: Proceedings of the IEEE/CVF International Conference on Computer Vision.
pp. 2798–2803 (2023)
27. Maaz, M., Rasheed, H., Khan, S., Khan, F.: Video-chatgpt: Towards detailed video
understanding via large vision and language models. In: Proceedings of the 62nd
Annual Meeting of the Association for Computational Linguistics (Volume 1: Long
Papers). pp. 12585–12602 (2024)
28. Maaz, M., Rasheed, H., Khan, S., Khan, F.S.: Video-chatgpt: Towards de-
tailed video understanding via large vision and language models. arXiv preprint
arXiv:2306.05424 (2023)
29. Nam, J., Ahn, D., Kang, D., Ha, S.J., Choi, J.: Zero-shot natural language video lo-
calization. In: Proceedings of the IEEE/CVF international conference on computer
vision. pp. 1470–1479 (2021)
30. Oquab, M., Darcet, T., Moutakanni, T., Vo, H., Szafraniec, M., Khalidov, V.,
Fernandez, P., Haziza, D., Massa, F., El-Nouby, A., et al.: Dinov2: Learning robust
visual features without supervision. arXiv preprint arXiv:2304.07193 (2023)


## Page 17


Mitigating Modality and Language-Style Gaps for ZMR
17
31. Radford, A., Kim, J.W., Hallacy, C., Ramesh, A., Goh, G., Agarwal, S., Sastry, G.,
Askell, A., Mishkin, P., Clark, J., Krueger, G., Sutskever, I.: Learning transferable
visual models from natural language supervision (2021), https://arxiv.org/abs/
2103.00020
32. Radford, A., Kim, J.W., Hallacy, C., Ramesh, A., Goh, G., Agarwal, S., Sastry, G.,
Askell, A., Mishkin, P., Clark, J., et al.: Learning transferable visual models from
natural language supervision. In: International conference on machine learning. pp.
8748–8763. PmLR (2021)
33. Reimers, N., Gurevych, I.: Sentence-bert: Sentence embeddings using siamese bert-
networks. arXiv preprint arXiv:1908.10084 (2019)
34. Ren, S., Yao, L., Li, S., Sun, X., Hou, L.: Timechat: A time-sensitive multi-
modal large language model for long video understanding. In: Proceedings of the
IEEE/CVF Conference on Computer Vision and Pattern Recognition. pp. 14313–
14323 (2024)
35. Shechtman, E., Irani, M.: Matching local self-similarities across images and videos.
In: 2007 IEEE conference on computer vision and pattern recognition. pp. 1–8.
IEEE (2007)
36. Sun, W., Yan, L., Ma, X., Wang, S., Ren, P., Chen, Z., Yin, D., Ren, Z.: Is chatgpt
good at search? investigating large language models as re-ranking agents. arXiv
preprint arXiv:2304.09542 (2023)
37. Sun, Y., Xu, Y., Xie, Z., Shu, Y., Du, S.: Gptsee: Enhancing moment retrieval and
highlight detection via description-based similarity features. IEEE Signal Process-
ing Letters 31, 521–525 (2023)
38. Touvron, H., Lavril, T., Izacard, G., Martinet, X., Lachaux, M.A., Lacroix, T.,
Rozière, B., Goyal, N., Hambro, E., Azhar, F., et al.: Llama: Open and efficient
foundation language models. arXiv preprint arXiv:2302.13971 (2023)
39. Touvron, H., Martin, L., Stone, K., Albert, P., Almahairi, A., Babaei, Y., Bash-
lykov, N., Batra, S., Bhargava, P., Bhosale, S., et al.: Llama 2: Open foundation
and fine-tuned chat models. arXiv preprint arXiv:2307.09288 (2023)
40. Wang, G., Wu, X., Liu, Z., Yan, J.: Prompt-based zero-shot video moment retrieval.
In: Proceedings of the 30th ACM international conference on multimedia. pp. 413–
421 (2022)
41. Wang, L., Yang, N., Huang, X., Yang, L., Majumder, R., Wei, F.: Improving text
embeddings with large language models (2024), https://arxiv.org/abs/2401.
00368
42. Wattasseril, J.I., Shekhar, S., Döllner, J., Trapp, M.: Zero-shot video moment re-
trieval using blip-based models. In: International Symposium on Visual Computing.
pp. 160–171. Springer (2023)
43. Xiao, J., Song, Z., Hu, J., Cheng, H., Hu, Z., Li, J., Hong, R.: Contrastive align-
ment with semantic gap-aware corrections in text-video retrieval. arXiv preprint
arXiv:2505.12499 (2025)
44. Xu, Y., Sun, Y., Xie, Z., Zhai, B., Du, S.: Vtg-gpt: Tuning-free zero-shot video
temporal grounding with gpt. Applied Sciences 14(5),
1894 (Feb 2024). https:
//doi.org/10.3390/app14051894, http://dx.doi.org/10.3390/app14051894
45. Xu, Y., Sun, Y., Zhai, B., Jia, Y., Du, S.: Mh-detr: Video moment and highlight
detection with cross-modal transformer. In: 2024 International Joint Conference
on Neural Networks (IJCNN). pp. 1–8. IEEE (2024)
46. Xu, Y., Sun, Y., Zhai, B., Li, M., Liang, W., Li, Y., Du, S.: Zero-shot video moment
retrieval via off-the-shelf multimodal large language models. In: Proceedings of the
AAAI Conference on Artificial Intelligence. vol. 39, pp. 8978–8986 (2025)


## Page 18


18
J. Lee et al.
47. Xu, Y., Sun, Y., Zhai, B., Xie, Z., Jia, Y., Du, S.: Multi-modal fusion and query
refinement network for video moment retrieval and highlight detection. In: 2024
IEEE International Conference on Multimedia and Expo (ICME). pp. 1–6. IEEE
(2024)
48. Zhai, X., Mustafa, B., Kolesnikov, A., Beyer, L.: Sigmoid loss for language image
pre-training (2023)
49. Zhang, H., Li, X., Bing, L.: Video-llama: An instruction-tuned audio-visual lan-
guage model for video understanding. arXiv preprint arXiv:2306.02858 (2023)
50. Zheng, M., Cai, X., Chen, Q., Peng, Y., Liu, Y.: Training-free video temporal
grounding using large-scale pre-trained models. In: European Conference on Com-
puter Vision. pp. 20–37. Springer (2024)
51. Zheng, M., Huang, Y., Chen, Q., Liu, Y.: Weakly supervised video moment lo-
calization with contrastive negative sample mining. In: Proceedings of the AAAI
Conference on Artificial Intelligence. vol. 36, pp. 3517–3525 (2022)
52. Zheng, M., Huang, Y., Chen, Q., Peng, Y., Liu, Y.: Weakly supervised temporal
sentence grounding with gaussian-based contrastive proposal learning. In: Proceed-
ings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition.
pp. 15555–15564 (2022)


## Page 19


Mitigating Modality and Language-Style Gaps for ZMR
1
Mitigating Modality and Language-Style Gaps
for Zero-Shot Video Moment Retrieval
Supplementary Material
6
Additional Method Details
6.1
Definition of Threshold for Generating Candidate Spans
In this section, we define the instance-wise dynamic threshold τj, which sup-
presses the frames with low boundary scores. The motivation for adopting a
dynamic threshold is that segmenting videos into contextually consistent spans
is highly sensitive to the variability of the context within the video. A fixed
threshold, which ignores this factor, fails to segment the videos appropriately.
Therefore, we propose the set of thresholds T = {τ1, τ2, . . . , τNT } which adapt
to the video context variability.
Video Context Variability. We introduce an indicator of intra-video context
variability to make the threshold respond to it. First, we ℓ2-normalize the frame
features F f ∈RL×Df into ˆF f. Then, we obtain the mean of the normalized
frame features µf as follows:
  \ m
u
 
^
f=\
fr a
c  {1}{L}\sum _{i=1}^{L}\hat {F}^f_i. 
(11)
Then, we apply zero-centering on ˆF f
i , that is, ˜F f
i
= ˆF f
i −µf. We define the
variability of the video context V by averaging the ℓ2-norm of zero-centered ˜F f
i :
  \
m
a
t
hca
l  { V
} =\frac {1}{L}\sum _{i=1}^{L}\|\Tilde {F}_i^f\|_2. 
(12)
The above formulations can be interpreted as follows: if the original frame fea-
tures F f are uniformly spread over an arbitrary hypersphere, the mean vector
µf computed after ℓ2-normalization will be close to the zero vector, which in
turn makes V close to 1. Conversely, if the frame features are biased toward a
particular direction, which means that some frame features have similar con-
text, the mean vector µf will also be shifted toward that direction, resulting in
a smaller norm of ˜F f and consequently a lower V. In other words, V reflects the
diversity of the contexts contained in a video instance. Therefore, we regard V
as an indicator of the intra-video context variability.
Definition of Threshold. Next, we define the threshold τj based on the video
context variability. It is obvious that videos with diverse contexts should undergo
fine-grained segmentation whereas homogeneous ones require coarse-grained seg-
mentation. Thus, the threshold should decrease as the indicator V grows, that


## Page 20


2
J. Lee et al.
is, leading to more candidate spans by increasing the size of boundary set Bj.
In contrast, the threshold should grow as the indicator V decreases, thereby re-
ducing the number of candidate spans by suppressing more frames. Therefore,
we specify the threshold as inversely related to the variability:
  \ t a u _
j=1-\ la m bda
 _j\mathcal {V} \quad \text {where} ~\lambda _j\in \Lambda _{j=1}^{N_\tau }, 
(13)
where Λ is a set of constants that control threshold scaling and the generation of
spans with diverse lengths. In practice, we set Λ to {1, 2, 3} across the benchmark
datasets, hence Nτ = 3. Note that the threshold changes instance-wise via V.
6.2
Detailed Procedure of MLLM-Based Re-Ranking
In this section, we provide a more detailed explanation of the MLLM-based re-
ranking process, which complements the concise description in the main paper.
Candidate Selection. For efficiency, re-ranking is applied only to the top-
kC candidate spans from the initial scoring stage, as these are the most likely
to contain the correct answer. In our implementation, we set kC = 5, balancing
computational efficiency with sufficient coverage of promising spans. The selected
candidate spans are represented as
  \ math
ca l 
{E}_{
R} = \{ [e_n^{\text {s}}, e_n^{\text {e}}] \}_{n=1}^{k_C}, 
(14)
where es
n and ee
n denote the start and end frame indices of the n-th selected
span, forming the set of spans subject to re-ranking. For the n-th span [es
n, ee
n],
the number of frames is defined as
  
N ^ {f
} _ {n
}  = e_n^{\text {e}} - e_n^{\text {s}} + 1. 
(15)
Frame Sampling. For each span, our goal is to extract representative frames
that best capture the semantic content relevant to the query. To achieve this, we
use the previously computed query-caption (QC) scores Sf, which measure the
alignment between the query and individual video frames. Frames with higher
QC scores are prioritized for sampling, as they are assumed to be more in-
formative for query verification. The number of sampled frames is determined
adaptively according to the span length with a sampling rate ρ, and is clamped
between a minimum and maximum to avoid undersampling short spans or over-
sampling long spans:
  N _{R
}
 =
 \ma x \!\ b i g
 ( N ^
{f}_
{
\min }, \min ( \rho \cdot N^{f}_{n}, N^{f}_{\max })\big ), 
(16)
where N f
min and N f
max are 10 and 30, respectively. The NR frames with the high-
est QC scores are retained, and their indices are sorted in temporal order to
preserve sequential structure.


## Page 21


Mitigating Modality and Language-Style Gaps for ZMR
3
Prompting and Scoring. The sampled frames are passed to the MLLM for
comparison with the text query. To ensure consistent behavior, we employ a
structured prompt that asks the model whether the query is aligned with the
input frame. The prompt is designed as:
“You are a visual fact-checker. Your job is to verify a statement against a
single video frame. Do not infer or guess information that is not clearly
visible. Statement to verify: [Query]. Based strictly on the visual infor-
mation in the image, is this statement true? Answer with only ‘Yes’ or
‘No’.”
Here, [Query] denotes the placeholder where the text query is inserted. The
MLLM produces logits for both “Yes” and “No.” Let lyes
i
and lno
i
denote the logits
corresponding to i-th frame. The frame-level re-ranking score is defined as the
softmax probability of the “Yes” token:
  
S ^
r_i = \f
r
a
c {\exp 
(
l ^ {\text 
{ yes}}_i)}{\exp (l^{\text {yes}}_i) + \exp (l^{\text {no}}_i)}. 
(17)
Span-Level Score Aggregation. To obtain a re-ranking score for an en-
tire span, we aggregate the frame-level scores. Instead of averaging all sampled
frames, which may include noisy or less informative ones, we select the top-kR
verification scores (with kR = 3) and compute their mean:
  
S ^ R
_n
 =
 
\
frac 
{
1
} { k_R
} 
\
su
m  _{i=e^\text {s}_n}^{e^\text {e}_n} \mathbf {1}\left [i \in I_{k_R}^{E_n}\right ] S^r_i, 
(18)
where IEn
kR is a set of indices with the top-kR highest frame-level re-ranking scores
within the n-th candidate span En. This design emphasizes the most confident
evidence while reducing the impact of outliers.
7
Additional Analyses
7.1
Hyperparameter analysis
In this section, we analyze the key hyperparameters of Self-SiMS, including the
boundary score thresholds τ, the top-kS selection strategy, and the weighting
factors α and β. We examine how each component influences span generation
and scoring.
Boundary threshold T . We analyze the effectiveness of the dynamic thresh-
olds defined in T by comparing them with fixed threshold values. Fig. 7 reports
the performance of varying fixed thresholds (solid lines) against the instance-
wise dynamic threshold determined by ours (red lines). For fair comparison, each


## Page 22


4
J. Lee et al.
QVHighlight w/ Fixed 𝜏 
Charades w/ Fixed 𝜏 
ActivityNet w/ Fixed 𝜏 
Analysis of boundary threshold 𝜏 on mIoU performance
50
40
30
Ours
Fig. 7: mIoU performance comparison between fixed thresholds and our dynamic
threshold across three datasets.
fixed-threshold setting is also evaluated as a set of three thresholds, matching
the structure of our dynamic threshold set T . Across all datasets, the dynamic
threshold consistently achieves similar or higher mIoU than any fixed threshold
choice, demonstrating that adapting the threshold to the intra-video context
leads to more reliable boundary detection. This confirms that videos with di-
verse contexts benefit from finer segmentation, while more homogeneous videos
require coarser segmentation, validating the motivation behind incorporating V
into the boundary threshold design.
Self-matching span score weighting factor α. For the initial span score, the
weighting factor α controls the contribution of the self-matching span score (SMS)
relative to the query-matching span score (QMS). Fig. 8 illustrates the effect of
varying α. To fairly evaluate the contribution of SMS itself, this analysis ex-
cludes the MLLM re-ranking score and examines performance using only the
combination of QMS and SMS.
Across the three datasets, we observe generally consistent trends. Perfor-
mance drops when α becomes too small, indicating that relying only on QMS
without sufficient SMS contribution fails to capture the intra-span contextual
consistency provided by self-similarity. On the other hand, excessively large α
also degrades performance because overly emphasizing SMS reduces the influence
of query-dependent signals that are essential for accurate semantic alignment.
A moderate weighting around α = 0.1 yields strong and stable results across
all benchmarks, as indicated by the red dashed lines. This shows that balanced
integration of query-dependent and self-similarity-based signals results in robust
span scoring, and that the model remains stable without high sensitivity to α
within this range.


## Page 23


Mitigating Modality and Language-Style Gaps for ZMR
5
mIoU
R1@0.5
R1@0.7
(a) Weighting factor 𝛼analysis on QVHighlights
(b) Weighting factor 𝛼analysis on Charades-STA
(c) Weighting factor 𝛼analysis on ActivityNet-Captions
Ours
Ours
Ours
Ours
Ours
Ours
Ours
Ours
Ours
QVHighlight 
Charades
ActivityNet
Ours 
Fig. 8: Effect of weighting factor α on mIoU and recall across three datasets.
Reranking score weighting factor β. For the final span score, the weighting
factor β controls the contribution of the rereanked span score SR
(m) relative to
the initial span score S(m). Fig. 9 illustrates how varying the weighting factor β
affects performance across different datasets. We set the weighting factor β to 0.5
so that the re-ranking mechanism generalizes consistently across datasets, where
β = 0.5 corresponds to taking the average of the initial score S and the MLLM
re-ranking score. As shown in the ablation results, β = 0.5 provides a stable
choice, exhibiting high performance on all benchmarks with minimal sensitivity
in its neighborhood. Additionally, because the re-ranking stage evaluates only
a small set of sampled frames rather than the full span due to computational
cost, relying solely on the MLLM re-ranking score is not ideal. For this reason,
we combine the initial score S with the MLLM re-ranking score, which provides
a practical and effective balance between performance and efficiency.
Analysis of the Top-kS Parameter. Figure 10 shows the effect of varying
the top-kS parameter used in the Query-Matching Span Score. When kS = 1,
the score is determined by only a single frame, resulting in insufficient contex-
tual evidence within the span and consequently lower performance. Conversely,
as kS becomes too large, an increasing number of noisy query-caption scores
are included, which dilutes the contribution of highly relevant frames and leads
to performance degradation. Across all datasets, we observe that values in the
range of kS = 2 to 4 consistently achieve the best results. Within this range,
performance remains stable with minimal variation, indicating that the proposed
scoring method operates robustly without being overly sensitive to the specific


## Page 24


6
J. Lee et al.
QVHighlight 
Charades
ActivityNet
Analysis of weighting factor 𝛽 on mIoU performance
55
50
45
0.0
35
40
0.2
0.4
0.1
0.3
0.5
0.6
0.7
0.8
0.9
1.0
Our 𝛽 value 
Fig. 9: Effect of weighting factor β on mIoU for QVHighlights, Charades-STA, and
ActivityNet-Captions.
QVHighlight 
Charades
ActivityNet
Analysis of weighting factor Top-𝑘𝑆 on mIoU performance
55
50
45
1
35
40
3
5
2
4
6
7
8
9
10
Our 𝑘𝑆 value 
Fig. 10: Effect of Top-kS selection on mIoU for QVHighlights, Charades-STA, and
ActivityNet-Captions.
choice of kS.
Ablation on the self-similarity source for span generation. Tab. 7 com-
pares three variants of the temporal self-similarity map source used for span gen-
eration: frame-only M f, caption-only M c, and their fusion M = 1
2(M f+M c). We
report results on the QVHighlights [17] validation set, Charades-STA [8], and
ActivityNet-Captions [15], both before and after the MLLM-based re-ranking
stage, while keeping all other components unchanged. Before re-ranking, the
fused setting consistently provides the strongest overall performance, achieving
the best mAP on QVHighlights and the best mIoU on both Charades and Ac-
tivityNet. This suggests that visual and caption self-similarity provide comple-
mentary temporal cues: frame-only self-similarity yields strong structural bound-
aries, whereas caption-only self-similarity can capture semantic consistency but
is less stable when used alone. After re-ranking, a similar trend is still observed.
Although frame-only or caption-only sometimes achieves the best score on indi-
vidual recall metrics, the fused setting still gives the strongest overall and most
balanced performance across datasets, especially in mAP/mIoU. These results
support our design choice of constructing the temporal self-similarity map from


## Page 25


Mitigating Modality and Language-Style Gaps for ZMR
7
Method
QVHighlights val
Charades-STA
ActivityNet-Captions
mAP mAP@0.5 R1@0.5 R1@0.7 mIoU R1@0.3 R1@0.5 R1@0.7 mIoU R1@0.3 R1@0.5 R1@0.7
Before re-ranking
frame-only
38.2
59.5
60.0
42.1
38.6
58.6
36.6
18.7
32.5
47.2
26.6
12.5
caption-only 35.6
57.0
57.0
39.0
38.6
58.6
36.2
18.7
33.7
48.9
27.6
13.4
fused
38.7
59.6
60.3
42.9
38.8
58.7
37.2
18.7
33.7
48.5
27.1
13.4
After re-ranking
frame-only
39.0
61.0
61.7
43.2
41.7
62.9
39.7
20.8
33.7
49.1
27.7
12.9
caption-only 36.2
58.0
57.8
39.6
41.5
62.9
39.2
20.2
34.7
50.5
28.5
13.9
fused
39.3
60.5
61.0
43.2
41.9
62.7
39.7
21.0
34.7
49.9
28.2
13.8
Table 7: Ablation on the self-similarity source used for span generation across three
benchmarks, before and after re-ranking.
Backbone
#Params
Scoring
mAP mAP@0.5 R1@0.5 R1@0.7
CLIP-B/32 [31]
87M
QMS only
31.5
49.2
42.9
29.0
QMS + SMS 35.3
54.3
54.1
37.9
SigLIP-B/16 [48]
200M
QMS only
31.3
48.6
42.5
28.3
QMS + SMS 34.8
53.8
53.6
36.8
DINOv2-Base (Ours) [30]
86M
QMS only
38.6
59.4
59.5
42.1
QMS + SMS 38.7
59.6
60.3
42.9
Table 8: Ablation on the visual encoder used to extract frame features for constructing
the temporal self-similarity matrix.
both frame and caption features, since their fusion yields more robust candidate
spans for moment retrieval.
7.2
Encoder robustness and ablation studies
Robustness of the self-matching score across visual encoders. Tab. 8
evaluates the robustness of Self-SiMS under different visual encoders on the
QVHighlights [17] validation set. Specifically, we compare QMS alone with the
combination of QMS and SMS before the re-ranking stage. Our DINOv2-based
setting consistently outperforms CLIP and SigLIP, even though the latter use
comparable or larger model sizes. In particular, DINOv2 captures temporal
variations more effectively, whereas CLIP and SigLIP tend to produce tempo-
rally smoother features [4]. Importantly, self-matching span score (SMS) yields
consistent gains across all evaluated encoders, indicating that the benefit of
self-similarity-based span scoring is robust to the choice of visual backbone.
Among the tested backbones, DINOv2-Base achieves the best overall perfor-
mance, demonstrating that it provides the most favorable balance between tem-
poral sensitivity and feature quality in our training-free setting.
Effect of text encoder capacity on the language-style gap. The language-
style (LS) gap in our setting is not merely a surface-level difference in wording,
but also arises from the inherent variability of MLLM-generated captions across


## Page 26


8
J. Lee et al.
Method
Text encoder
#Params mAP mAP@0.5 R1@0.5 R1@0.7
VTG-GPT [44]
E5-Mistral [41]
7B
30.87
50.80
51.94
33.16
NV-Embed [16]
7B
31.44
53.48
55.42
34.45
Sentence-BERT [33]
82M
34.9
56.56
59.03
38.9
Table 9: Ablation on the text encoder used to compute query-caption similarity in
the query-dependent VTG-GPT baseline.
visually similar frames. As a result, their shifting focus and granularity make
query-caption (QC) alignment noisy and temporally unstable. This motivates
an additional analysis of whether stronger text encoders alone can stabilize
QC alignment. To isolate this effect, we conduct an additional study on the
QVHighlights [17] validation set using VTG-GPT [44], a query-dependent base-
line whose span generation and scoring both rely solely on QC similarity. We
adopt VTG-GPT in this analysis because its official implementation is publicly
available, whereas the closely related Moment-GPT [46] does not provide an of-
ficial code release. This setting removes the influence of our self-similarity-based
span proposal and scoring, allowing us to directly examine the contribution of
the text encoder to QC matching. As shown in Tab. 9, replacing the default
Sentence-BERT encoder with larger alternatives, such as E5-Mistral [41] and
NV-Embed [16], does not improve performance. These results indicate that the
LS gap cannot be sufficiently resolved by stronger text encoding alone.
7.3
MLLM ablation studies and Computational efficiency analysis
Setting
Captioning
Re-ranking
mAP mAP@0.5 R1@0.5 R1@0.7
Moment-GPT [46] MiniGPT-v2 [5]
Video-ChatGPT [27]
35.9
55.7
58.9
38.6
Ours
MiniGPT-v2 [5]
–
38.6
59.9
59.9
42.3
LLaMA3.2-Vision [9] –
38.7
59.6
60.3
42.9
Ours
MiniGPT-v2 [5]
MiniGPT-v2 [5]
40.0
62.3
65.0
45.2
LLaMA3.2-Vision [9] LLaMA3.2-Vision [9]
39.3
60.5
61.0
43.2
Table 10: Ablation on MLLM choice for captioning and re-ranking on QVHighlights
validation.
Setting
Captioning
Re-ranking
Charades-STA
ActivityNet-Captions
mIoU R1@0.3 R1@0.5 R1@0.7 mIoU R1@0.3 R1@0.5 R1@0.7
Moment-GPT [46] MiniGPT-v2 [5]
Video-ChatGPT [27] 36.5
58.2
38.4
21.6
30.8
48.1
31.1
14.9
Ours
MiniGPT-v2 [5]
–
38.1
57.0
35.3
18.9
33.8
48.5
27.8
13.7
LLaMA3.2-Vision [9] –
38.8
58.7
37.2
18.7
33.7
48.5
27.1
13.4
Ours
MiniGPT-v2 [5]
MiniGPT-v2 [5]
41.3
62.4
38.7
20.7
34.5
49.4
27.8
13.9
LLaMA3.2-Vision [9] LLaMA3.2-Vision [9] 41.9
62.7
39.7
21.0
34.7
49.9
28.2
13.8
Table 11: Ablation on MLLM choice for captioning and re-ranking on Charades-STA
and ActivityNet-Captions.
MLLM ablation study. To verify that the performance improvement of our
framework does not simply arise from the choice of a stronger MLLM, we com-
pare different MLLM backbones within our pipeline. Tab. 10 compares different
MLLM choices for captioning and re-ranking on the QVHighlights [17] validation


## Page 27


Mitigating Modality and Language-Style Gaps for ZMR
9
set, while Tab. 11 reports the corresponding comparison on Charades-STA [8]
and ActivityNet-Captions [15]. Notably, our framework still achieves strong per-
formance when using MiniGPT-v2 [5], the same captioning backbone adopted by
prior work Moment-GPT [46], indicating that the improvement does not simply
come from switching to a larger MLLM. The MiniGPT-v2 variant also provides
a controlled efficiency comparison with Moment-GPT, as reported in Tab. 6
of the main paper. Under the same captioning backbone as Moment-GPT, Self-
SiMS uses only one 7B model for both captioning and re-ranking, compared with
Moment-GPT’s 22B model stack, and achieves slightly lower total MLLM/LLM
runtime. Its performance remains comparable across benchmarks and is even
slightly higher on QVHighlights, showing that our gain is not simply due to a
larger backbone or longer inference.
7.4
Effect of self-similarity scoring on the language-style gap
Subset
Method
Scoring mAP mAP@0.5 R1@0.5 R1@0.7
Full
Moment-GPT’s [46] Mean
55.7
40.9
56.7
37.1
Ours
QMS
59.5
42.1
59.4
38.6
Ours
+ SMS
60.3
42.9
59.6
38.7
Severe LS-gap
subset
Moment-GPT’s [46] Mean
25.9
43.7
34.0
24.5
Ours
QMS
31.3
51.8
43.4
30.7
Ours
+ SMS
31.7
52.8
45.3
32.6
Table 12: Performance on the full validation set and the severe Language-style (LS)
gap subset, where query-caption similarity is particularly unstable.
To further analyze the effect of self-similarity scoring modeling under a
language-style (LS) gap, we evaluate a subset of queries on the QVHighlights [17]
validation set for which query-caption (QC) similarity is particularly unstable,
corresponding to cases with a severe language-style gap. We use the first-order-
difference energy to measure how sharply the QC score changes over time; a
high value indicates that the similarity signal fluctuates strongly even within
the target moment. We define the severe LS-gap subset as queries whose QC
similarity is both noisy and weak within the ground-truth span. Concretely, we
select queries whose QC similarity has (i) first-order-difference energy in the top
quartile and (ii) mean similarity in the bottom quartile. As shown in Tab. 12,
replacing mean scoring scheme used in Moment-GPT [46] with query-matching
span score (QMS) consistently improves performance on both the severe LS-gap
subset and the full dataset, confirming that QMS provides a more stable span
score under unstable QC alignment. Additionally, adding self-matching span
score (SMS) produces consistent gains in both settings, with the improvement
being more pronounced on the severe LS-gap subset, particularly in terms of
R1@0.5 and R1@0.7. These results indicate that self-similarity-based modeling
effectively complements query-dependent scoring by stabilizing span-level deci-
sions in hard cases while still providing additional benefits in the general setting.


## Page 28


10
J. Lee et al.
7.5
Comparison of span generation strategies
Method
mAP@avg mAP@0.5 R1@0.5 R1@0.7
Sliding Window [34]
12.5
30.5
29.9
10.5
K-means clustering [29]
31.3
47.7
49.1
32.1
Ours
39.3
60.5
61.0
43.2
Table 13: Comparison of candidate span generation strategies.
Table 13 compares our self-similarity-based span generation strategy against
two generic query-agnostic alternatives: sliding-window proposals and clustering-
based proposals on the QVHighlights [17] validation set. For the sliding-window
baseline, we adopt a length-adaptive design inspired by TimeChat [34]; unlike the
fixed temporal scale used in that training-based framework, we set the window
size and stride proportionally to the video length as ⌊L/3⌋and ⌊L/6⌋, respec-
tively, in our training-free setting. For the clustering-based baseline, we follow
PSVL [29] and set the number of clusters to k = 5. Sliding windows serve as
a simple baseline that uniformly covers the temporal axis with fixed candidate
spans, while clustering-based proposals group temporally similar features with-
out explicitly modeling boundary transitions. In contrast, our method generates
candidate spans from self-similarity-derived boundary scores, producing more
precise temporal proposals and leading to best moment retrieval performance.
