# OmniShotCut

*Source PDF: `OmniShotCut.pdf`*

*Total Pages: 18*

---


## Page 1


OmniShotCut: Holistic Relational Shot Boundary
Detection with Shot-Query Transformer
Boyang Wang1, Guangyi Xu1, Jiahui Zhang1, Zhipeng Tang2, Zezhou Cheng1
1University of Virginia
2University of Massachusetts Amherst
Project Page: Omni-Shot-Cut.github.io
Abstract
Shot Boundary Detection (SBD) aims to automatically identify shot changes and
divide a video into coherent shots. While SBD was widely studied in the literature,
existing methods often produce non-interpretable boundaries on transitions, miss
subtle yet harmful discontinuities, and rely on noisy, low-diversity annotations and
outdated benchmarks. To alleviate these limitations, we propose OmniShotCut to
formulate SBD as structured relational prediction, jointly estimating shot ranges
with intra-shot relations and inter-shot relations, by a shot query-based dense
video Transformer. To avoid imprecise manual labeling, we adopt a fully synthetic
transition synthesis pipeline that automatically reproduces major transition families
with precise boundaries and parameterized variants. We also introduce OmniShot-
CutBench, a modern wide-domain benchmark enabling holistic and diagnostic
evaluation. Experiments on the benchmarks demonstrate the effectiveness and
generality of our method.
1
Introduction
Modern video production is inherently compositional, where multiple shots are assembled through
editing operations rather than captured in a single continuous take. The transitions between these
shots follow artistic principles, spanning from abrupt hard cuts and jump cuts to gradual effects such
as dissolves, fades, wipes, etc. To understand the structural composition of such edited videos, it is
necessary to identify the most atomic temporal units, a group of frames that form a coherent shot.
This task is known as Shot Boundary Detection (SBD).
Shot Boundary Detection [43, 29, 30, 33] has long been regarded as a well-established problem in
video understanding. However, despite its apparent maturity, progress in this area has stagnated. We
revisit SBD from the perspective of its downstream applications and ask: has the problem truly been
well defined and solved, and is it addressed in the most efficient and scalable manner? We argue that
current SBD pipelines remain limited along several practical axes.
First, the predicted shots lack interpretability, as it is unclear whether a predicted boundary corre-
sponds to a scene or an editing transition (see Fig. 1a). For each detected shot, the output should not
be limited to a simple temporal range, but should also include higher-level structural information
that better supports downstream applications. For instance, in video generation [35, 42, 2], transition
may be less critical, and clean vanilla shot segments are often preferred. To this end, we introduce
intra-shot relation classification as the outputs of the model. The intra-label characterizes the shot
itself, indicating whether it is a vanilla segment or a specific transition type.
Second, previous SBD models fail to detect subtle yet harmful discontinuities (i.e., sudden jumps) that
negatively affect downstream tasks. Sudden jump (see Fig. 1b) introduces excessive abrupt motion or
texture change in two consecutive frames, which exert negative influence on motion tracking [17],
video segmentation [12], latent video compression [2, 42, 35], and more downstream tasks. To this
end, we introduce inter-shot relation classification. The inter-label captures its relationship with the
preceding shot, modeling the cross-shot continuity relationship. Further, existing state-of-the-art SBD
Preprint.
arXiv:2604.24762v2  [cs.CV]  21 May 2026


## Page 2


(a) No Relational Information
Shot A
Shot B
(c) Ambiguous Transition Boundaries
Which frame marks the START and which marks the END of this transition?
Answer: f4 tis the transition start; f11 transition end
f1
f3
f4
f5
f2
f6
f7
f8
f9
f10
f11
f14
f12
f13
Boundary Detected                Boundary Detected
Transition Type                      Dissolve? Fade? Wipe? Cut?
(b) Neglect Tiny Continuity Jump 
Sudden Jump: Abrupt Motion Discontinuity when editor crops a segment of 
the video. 
Failed on Traditional Shot Boundary Detection Model.
Discontinues 
Shot A
Shot B
Figure 1:
Limitations of traditional Shot Boundary Detection models. (a) Detected Shots
are hard to interpret: predicted boundaries lack explicit transition semantics; (b) Sudden Jump is
under-modeled and often missed; (c) Human annotations are unreliable for gradual transitions with
subtle start/end frames.
models, such as TransNetV2 [29] and AutoShot [43], rely on 3D CNN architectures that are not well-
suited for our richer formulation. Instead, we design a shot query-based Transformer architecture that
jointly optimizes all objectives through shared hidden states, enabling unified modeling of temporal
shot range prediction and relational understanding.
Third, human-supervised annotation struggles to localize subtle changes accurately (see Fig. 1c).
Prior works [4, 5, 3] heavily rely on manually annotated real-world data for shot boundary detection.
However, transition labeling is highly labor-intensive and inherently imprecise. In particular, humans
struggle to accurately localize subtle boundaries, such as the exact start and end frames of fading or
dissolve effects, where minor changes in illumination and transparency are difficult to perceive. As a
result, manual annotation is not well-suited for fine-grained transition modeling. More importantly,
transition effects are in fact generated by video editing software (e.g., Apple iMovie or Adobe
professional editing suites). Instead of investing costly human effort in reverse annotation, we propose
a forward generation strategy that programmatically reproduces transitions (Fig. 2), which covers 9
main types and 30 subtypes, and yields hundreds of variations by sweeping controllable parameters
in directions, edges, intensity, layout, and more. This methodology enables the construction of
a synthetic training dataset with precise transition ranges, while covering rare yet realistic cases
(e.g., mosaic, puzzle, cube, doorway) that are underrepresented in existing datasets. Furthermore,
naively stitching together unrelated videos does not reflect real-world editing patterns. To address
this, we leverage a self-supervised learning method to group semantically similar videos from our
million-scale video clips pool, thereby simulating more realistic transition contexts.
Fourth, existing benchmarks contain noisy annotations, outdated and narrow domain video sources,
and miss the focus of the sudden jump, which fail to reflect the diversity and complexity of modern
video content. To close this gap, we introduce OmniShotCutBench, a contemporary SBD benchmark
built from wide-domain, highly complex sources, with intra- and inter-shot relational labels and,
importantly, a confidence scoring system to account for human judgment uncertainty. We hope
OmniShotCutBench can offer a more holistic and diagnostic evaluation for modern Shot Boundary
Detection.
In summary, our contributions are as follows:
• We reformulate Shot Boundary Detection by enriching each shot with both intra-shot and
inter-shot relational information, moving beyond simple temporal range prediction.
• We propose a shot query-based Transformer architecture that jointly optimizes range predic-
tion and relational classification within a unified hidden state.
• We introduce a fully synthetic pipeline with novel self-supervised clustering that groups
similar but not identical clips and provides precise, diverse labels without manual annotation.
• We introduce a new benchmark for modern shot boundary detection that captures diverse con-
temporary transition patterns and sudden jumps, where our model consistently outperforms
existing methods across multiple evaluation dimensions.
2


## Page 3


Dissolve: Shot A gradually blends into Shot B
Shot A
Shot B
Fade: Shot A fades to black, then Shot B appears
Shot A
Shot B
Wipe: Shot B replaces A via moving boundary
Shot A
Shot B
Slide: Shot B slides over Shot A
Shot A
Shot B
Doorway: Two panels open revealing Shot B
Shot A
Shot B
Zoom: Transition via rapid zoom into next shot
Shot A
Shot B
Sudden Jump: Abrupt cut within same scene continuity
Hard Cut: Instant switch from Shot A to B
Figure 2:
Main Transition Types. We consider a diverse and comprehensive set of video shot
transitions that are largely underexplored in prior shot boundary detection works [43, 29, 30]. This
figure illustrates several representative transition types, including dissolve, fade, wipe, slide, doorway,
zoom, sudden jump, and hard cut. Each example shows the temporal progression from Shot A to
Shot B with the transition region highlighted. We skip the Pushing effect demo here. More subtypes
are provided in the supplementary.
2
Related Works
Shot Boundary Detection.
Shot Boundary Detection [16] operates on native, full video sequence
inputs without frame downsampling. It requires frame-level precision to localize each boundary. This
inherently demands high-density temporal inputs for the model. Traditional approaches, such as
PySceneDetect [8] and Koala-36M [37], primarily rely on handcrafted low-level features (e.g., color
histogram differences or structural similarity) to detect abrupt transitions. These methods are sensitive
to illumination changes and often struggle to capture higher-level semantic consistency across frames.
Deep learning-based methods have since become dominant, including DeepSBD [10], ClipShots [38],
TransNetV2 [29], and AutoShot [43]. They employ 3D CNNs to detect transition intervals. To handle
long sequences efficiently, these models often downsample spatial resolution aggressively (e.g., to
48 × 27) to reduce computational cost. To evaluate SBD, even though benchmarks like BBC [4],
RAI [5], and IACC3 [3] are popularly used with corresponding training datasets, many shot cut labels
lack a clear definition and neglect transitions and subtle motion discontinuity cases like sudden jumps.
In addition, these datasets are primarily derived from legacy broadcast footage and do not reflect the
diversity of modern video domains.
Downstream Applications.
Shot Boundary Detection has become increasingly important in dataset
curation for internet-scale in-the-wild videos. In data curation, massive raw long-form videos must
be segmented into temporally coherent clips without abrupt changes. The temporal consistency of
each clip is critical for training downstream models that demand continuous sequences of images,
like the video generation task. In state-of-the-art video generation, videos are encoded by a temporal
VAE [42, 35], where multiple frames share the same token. If sudden jumps are not accurately
detected, consecutive frames may exhibit drastic spatial shifts (e.g., a subject abruptly moving from
left to right), significantly hindering temporal compression and modeling. Moreover, shot boundary
detection models are widely used to filter in-the-wild online videos and have been incorporated
into numerous recent datasets and benchmark works [20, 21] as the key component in curation
preprocessing. In the scene segmentation task, MovieNet [13] provides a dataset that is first cropped
by SBD, and then the following works, like LGSS [27], BaSSL [24], ShotCOL [9], and Scene-
VLM [6], apply downsampled frames from the predicted shot boundaries to detect scene boundaries.
This growing reliance further underscores the need for a more precise, scalable, and transition-aware
shot boundary detection model.
Synthetic Data.
While supervised training on manually annotated pairs remains a standard approach
in computer vision, several domains have noted the difficulty of collecting precisely aligned data in
certain tasks. As a result, synthetic data generation strategies [23] have been increasingly adopted,
leveraging programmable forward transformations to automatically construct large-scale labeled
3


## Page 4


2. Basic Video Filter & Crop
3. Video Continuity Check and Motion Filter
Keep 50%
Keep 15%
Medium Motion
Slow motion
High Motion
Keep 90%
(a) Frame Similarity using DINOv3 Embedding
Cosine Similarity 
0.0
0.9
1.0
Clip0
Clip1
Clip2
Drop2
Drop1
𝛆sim(Threshold)
5. Video Clip Fusion and Transition Synthesis 
1. Diverse Internet Raw Video Collection (~2.5 Million Videos)
4. Automatic Semantic Clustering of Videos
Download
Download
…
Download
Download
Cluster #1 
Transition1
Transition2
Cluster #2 
Low < 400px
High ≥ 400px
25 fps
10 fps
sparse
dense
Keep
Cropped
(c) Max Duration Crop (≤ 1 min)
(a) Video Resolution
(b) FPS & Frame Count
Frame t
Frame t+1
Video Motion Scoring based on Dense Pixel Tracking
(b) Video Filtering based on Motion
Videos Clustering using 
Frist-frame DINOv3 Embedding 
Nature
Human
House
Clip1
Clip2
Clip3
Transition1
Clip1
Clip2
Figure 3:
Large-scale transition source video curation. (1) We collect ∼2.5M raw videos
from diverse Internet sources. (2) Videos are filtered based on resolution, frame rate, and duration
constraints. (3) Temporal continuity and motion strength are verified using frame-level semantic
similarity and dense motion tracking. (4) Remaining videos are automatically clustered using the SSL
data curation method [34] to group semantically similar videos. (5) Finally, video clips in the same
and different clusters are fused to synthesize large-scale shot boundary detection training datasets.
datasets. A representative example arises in low-level vision [39, 15, 36], where perfectly pixel-
aligned degraded inputs and original high-quality pairs are rarely available in real-world settings.
Instead, their degraded images or videos are synthesized via degradation to high-quality ground-truth
sources. Similarly, prior research [38] in image forensics and editing detection has leveraged scripted
pipelines to automatically synthesize Photoshop-manipulated images. For transition modeling, where
effects are typically synthesized by editing software, a programmatic synthesis strategy is therefore a
principled and effective solution. Though previous works like TransnetV2 [29] and DeepSBD [10]
mix real data with synthesized hard-cut and dissolve, most transition effects remain underexplored,
and we extend to dozens of transitions available. More importantly, we explore the extent to which
purely synthetic training data can push the limits of synthetic supervision.
3
Method
Problem Formulation.
We define the problem as empowering traditional Shot Boundary Detection
within an end-to-end model such that it not only predicts the temporal ranges of each shot, but also
outputs the intra-relation classification of the shot itself and the inter-relation classification with
respect to the previous shot. For intra-relation, we include 8 major categories, which includes vanilla
General video, Dissolve, Wipe, Push, Slide, Zoom, Fade, and Doorway. For inter-relation, we classify
whether the boundary corresponds to a Transition, a Hard Cut, or a Sudden Jump.
3.1
Automatic Video Transition Synthesis
To synthetically construct shot transitions, a clean video source pool is crucial. Our curation pipeline
is shown in Fig. 3. We first apply basic parameter filtering on duration, resolution, frames-per-second
(fps), and aspect ratio to all collected in-the-wild video sources and crop them into segments with
a maximum duration of 1 minute. To conservatively extract fluent video segments that contain no
abrupt content change, inspired by motion evaluation of VBench [14], we encode frames sampled at a
constant interval into DINO [28] embeddings, and compute the cosine similarity between consecutive
embeddings. If the cosine similarity is higher than the threshold εsim, this indicates that the two
frames are semantically consistent and do not exhibit an abrupt hard cut or transitions changing. We
continue this process until the similarity below εsim, at which point the clip is terminated. And then
we refresh the cache and start finding the next video clip. Empirically, we observe that this approach
4


## Page 5


is effective at identifying fading dark frames and dissolve-induced transparent frames, cropping out
early when transitions start happening. Although this approach cannot guarantee that every extracted
clip is completely clean, in subsequent synthetic transition generation, training with a large proportion
of correctly labeled data can effectively mitigate the influence of noisy labels.
In this paper, identifying the Sudden Jump is a critical task. Sudden Jump typically arise during video
editing where a short period of segments is manually cropped, resulting in abrupt discontinuities,
where the video cannot be regarded as a fluent shot. Thus, we believe that sudden jump is aligned with
the purpose of the shot boundary detection task and should be solved in this domain. To incorporate
into our shot boundary detection framework, we explicitly estimate the motion strength during the
data curation stage. This enables us to select clips with medium-level motion intensity (neither too fast
nor too slow) as suitable sources for constructing sudden jump samples. We estimate motion strength
using the CoTracker3 [17] model, which provides dense tracking points with configurable grid density.
By measuring the displacement magnitude of tracked points across frames and averaging over all
frames, we obtain an overall motion strength score for each video. Further, another functionality of
motion strength information is that it can be helpful to increase video clip pool complexity. This is
because we observe that a large portion of raw clips exhibit small motion magnitudes; therefore, we
filter out these slow-motion cases with weak dynamic patterns.
Once each video clip is properly curated, we want to group similar but not identical videos into
the same cluster, such that the sources before and after a synthetic transition can be sampled with
high similarity to better simulate real-world video. We adopt the DINO representation and perform
Self-Supervised Learning-based (SSL) clustering following the methodology of [34]. For each video
clip, we extract the DINO embedding of its first frame, directly reusing the embeddings computed
during the earlier curation stage. And then, we apply a semantic deduplication [1] paradigm to
filter instances whose cosine similarity is less than the threshold εdup in each cluster. This avoids
near-duplicate videos when we are using large-scale random videos from the internet. Finally, we
apply hierarchical K-means [34] clustering to group semantically similar embeddings. Each cluster
represents a collection of videos sharing similar semantic content, like indoor scenes, vehicles,
housing, mountains, etc. The SSL method does not directly tell us what the content is, but it can
ensure that the contents are perceptually similar and strongly related.
Synthetic Transition Composition.
After the curation stage, we obtain a large collection of clean
video clips. We then randomly choose videos from this pool and stitch clips together with diverse
synthetic transitions (as shown in Fig. 2 and Fig. 7). In the synthesis, most video clips are sampled
from the same SSL-grouped cluster pools as previous videos, while we also allow cross-cluster
selection to reflect the unpredictability of real-world video editing (see Fig. 3 (5)). For sudden
jump cases, we restrict the video source selection to middle motion strength. Excessive camera or
object motion often induces large structural changes, making it difficult to distinguish from hard
cuts, whereas some small motion cases (e.g., static talk-show scenarios) yield changes that are barely
perceptible even to humans. The synthesis settings are detailed in the supplementary.
3.2
Shot Query-based Dense Video Transformer
As shown in Fig. 4, we propose a Shot Query-based end-to-end video Transformer model, which is
composed of the image encoder, Transformer encoder, and Transformer decoder. We start from the
image-based DETR [7] object detection Transformer model and introduce critical modifications for
our task. The input consists of video frames of length F, height H, and width W, forming a tensor in
RF ×H×W ×C. The video is first encoded by ResNet [11] as an image encoder in a frame-by-frame
manner.
The encoded per-frame features are fed into the Transformer encoder. We flatten the spatial and
temporal dimensions into a single dimension, resulting in a feature map of size Rd×(F ·H·W ), where
d is the hidden state dimension. Each Transformer encoder layer is composed of multi-head self-
attention. Since our input shifts from images to videos, the tokens in the Transformer remain
permutation-invariant by design, we need to extend the 2D position embedding to 3D position
embedding, introducing additional positional information along the temporal dimension. Specifically,
following the approach of VisTR [40], we generalize the cumulative spatial coordinates (x, y) to
3D (t, x, y) and apply sinusoidal embeddings along the temporal and spatial axes, enabling the
Transformer to model joint spatiotemporal relationships in video inputs. The 3D position embedding
5


## Page 6


Shot Detection Outputs
Frame 121
Frame 1
General shot
Frame 165
Frame 122
Dissolve Transition
Frame  169
Frame 166
General Shot
Image Encoder
In-the-wild videos
…
…
Transformer Encoder
Spatiotemporal Attention
Transformer Decoder
Learnable Shot Queries
…
Inter-Shot Self-Attention
Shot-to-Frame Cross-Attention
…
…
…
…
MLP
MLP
MLP
Shot Range
Intra-Shot Relation Inter-Shot Relation
Video frame tokens 
…
…
…
…
…
3D Positional Embed.
⊕
Figure 4:
Shot Query-based Dense Video Transformer. Frame tokens from input videos are
encoded using a spatiotemporal Transformer encoder with 3D positional embedding. Learnable
shot queries in the decoder interact with frame features through cross-attention to predict shot range,
intra-shot relation, and inter-shot relation.
will also be flattened to Rd×(F ·H·W ) and then added with the flattened video tokens before entering
the Transformer encoder.
The input to the Transformer decoder is a fixed-length set of trainable embeddings, referred to as shot
queries. At a high level, each shot query serves as a shot prediction slot, aggregating shot-specific
evidence from the video sources into a compact hidden state for decoding. The entire Transformer
decoder consists of multiple decoder layers. In each layer, the shot queries first undergo self-attention,
followed by cross-attention with the tokens Rd×(F ·H·W ) produced by the Transformer encoder. The
number of input shot queries is fixed. At the output stage, shot queries will predict a dedicated
termination token to explicitly indicate the end of shot prediction when it reaches the last shot. All
queries after the termination token are discarded, and only the preceding ones are considered valid
predictions.
Each shot query on the output of our Transformer decoder is passed through three heads: a range head,
an intra-relation head, and an inter-relation head. Directly adopting DETR-style [19] formulation
by replacing bounding box prediction with an L1 + 1D GIoU regression loss results in a suboptimal
learning objective for temporal range prediction (check Sec. 4.3). Regression over normalized
continuous coordinates is inherently ill-suited for accurate frame-level boundary localization across
long sequences, where even a one-frame deviation at a hard-cut transition constitutes a significant
error for the SBD task. To address this limitation, we reformulate range prediction as a discrete
classification problem over frame indices, which provides improved localization precision and more
stable optimization. Specifically, the range head predicts the index of the last frame of each shot pend,
formulated as a classification problem where the number of classes equals the total number of frames.
As shots in SBD are consecutive and non-overlapping, the start of each shot is implicitly defined by
the end of the previous one, with the first shot starting at frame 0. This classification formulation
for the range prediction does not require post-processing of heuristic thresholding like prior SBD
methods [29, 43]. Consequently, Hungarian matching [18] is no longer required. We retain auxiliary
supervision at intermediate decoder layers to facilitate stable optimization.
3.3
Evaluation Benchmark
We introduce OmniShotCutBench, a modern shot boundary detection benchmark designed to com-
prehensively evaluate models’ performance on versatile transitions from modern internet video
sources. Each range label is paired with a confidence score. This is because we recognize that human
perception is inherently insensitive to subtle transition variations, particularly in transparent dissolve
and fading effects. OmniShotCutBench is constructed entirely from real edited videos and is disjoint
from all synthetic training sources. No synthetic transitions generated by our pipeline are included in
the benchmark. The construction pipeline and statistics comparison is shown in Fig. 5.
6


## Page 7


Dataset
Statistics
Annotations
Content
# Videos
Duration (min)
Avg Len (s)
# Cuts
Transition Type
Inter-shot 
Relation
Confidence
Genre Diversity
BBC
11
550
6.57
5,000
✗
✗
✗
RAI
10
100
5.65
1,060
✗
✗
✗
AutoShot
853
560
2.59
11,606
✗
✗
✗
OmniShotCut Bench
114
114
2.09
3,091
✓
✓
✓
Low
Medium
High
Low
Verification
Perform multi-round 
inspection
Constructing the final 
benchmark
100 mins videos
180,000+ frames
More than 2700 cuts
multiple inter or intra 
relations
Game
Vlog
Sports
Shorts Concert
Movie
Annotation
Annotate using self-
developed tool with 
iterative boundary and 
label refinement
1
2
3
4
Relation
Segment
Confidence 
0
2
1
Data Curation & Pre-processing
Collect modern videos of 
different genres from 
multiple sources
Annotator Training
Define transition types 
following standard video 
editing tools and 
tutorials
Refine labeling guideline 
via multi-round pilot 
annotations
Figure 5: OmniShotCutBench Pipeline and Data Statistics.
We collect diverse video sources with modern video editing techniques from the topics of vlog, anime,
movie, concert, documentary, monitor recording, game, sports, etc. We randomly truncate the videos
to one minute (or shorter) and standardize all videos to 480p resolution at 30 FPS to ensure consistent
temporal precision, which is critical for accurate shot boundary localization. In total, we curate 114
videos, which is 114 minutes of diverse, high-quality, and representative video sources.
To ensure high-quality annotations, following other datasets & benchmark works [21, 22], we
mimic their high-standard curation paradigm, as shown in Fig. 5. All annotators first studied
several professional video editing tutorials online and learning video editing applications like iMovie.
Annotators were required to review these materials prior to labeling to establish a clear understanding
of transition taxonomy and visual characteristics. We then conducted multiple rounds of pilot
annotations to align labeling criteria and ensure consistency across annotators. During the final
annotation phase, ambiguous or contentious cases were systematically documented and resolved
to maintain annotation quality and consistency. Analysis and visualization of our benchmark are
provided in the supplementary material. We will open-source this benchmark for future research.
4
Experiment
4.1
Implementation Details
We train our model with 8 Nvidia A100 GPUs for 50 epochs. Since training resolution is only
128x96, we choose the smallest pretrained ResNet18 [11] as the image encoder to maintain more
spatial tokens after the encoder. We set 3 Transformer encoders and 6 Transformer decoders for our
model, which is 34.49M parameters, out of which 11.17M is the ResNet backbone. We set 24 fixed
learnable shot query tokens as the input to the Transformer decoder, corresponding to the maximum
number of shots observed in a 100-frame training clip. The learning rate for the ResNet backbone
is set to 1e −5, and the Transformer encoder and decoder learning rate is 1e −4. Total batch size
across all GPUs is 64. We randomly crop 100 frames of the full video source for the training. In the
training, we do several online augmentations. This includes horizontal and vertical flip, color jittering,
blurring, Gaussian and Poisson noises, and compression artifacts [36]. More implementation details
are provided in the supplementary.
4.2
Experiment Results
Though our model jointly outputs the relational label, our capability is mainly inherited from shot
boundary detection. To evaluate traditional shot boundary detection, we choose to compare with main-
stream baselines in the literature, which include non-learning-based method PySceneDetect [8], and
previous state-of-the-art learning-based methods by 3D CNNs, TransNet V2 [29], and AutoShot [43].
The evaluation is done on OmniShotCutBench and legacy benchmark BBC Planet Earth Documen-
tation [4]. Our evaluation considers traditional shot range precision, recall, and F1 metrics, which
are based on the ShotBench in Cosmos [2]. We use their default tolerance of 2 frames. Further, we
specialize in the analysis of the transition of the IoU and sudden jump accuracy. For transition IoU,
we select the GT shots that are labeled with a transition label, and find the closest prediction results
to calculate the IoU, applying our human label confidence to dynamically adjust the tolerance range.
7


## Page 8


Table 1: Quantitative comparison with existing shot boundary detection methods. We report results
on the OmniShotCut Bench and the legacy BBC benchmark [4]. For our benchmark, we additionally
evaluate transition localization, sudden jump detection, and relation classification. All metrics are
higher the better. The best is highlighted.
OmniShotCut Bench
BBC Bench
Method
Trans.
IoU
Sudden
Jump
Acc.
Shot Range
Relation Acc.
Shot Range
Precision Recall
F1
Intra
Inter
Precision Recall
F1
PySceneDetect
0.183
0.417
0.833
0.689
0.755
-
-
0.893
0.884
0.889
TransNet V2
0.193
0.262
0.913
0.735
0.814
-
-
0.983
0.951
0.967
AutoShot
0.253
0.455
0.849
0.783
0.815
-
-
0.984
0.922
0.952
Ours
0.644
0.759
0.904
0.859
0.881 0.962
0.827
0.967
0.974
0.971
For sudden jump accuracy, we identify all ground-truth inter-relation labels corresponding to sudden
jumps and measure the proportion of correctly predicted shot cuts at the same frame index. A zero
tolerance is applied, as the transition is expected to occur instantaneously. We further evaluate intra-
and inter-relation classification accuracy, which is the number of correct classifications divided by the
total number of shots. For each ground-truth shot, the predicted shot with the highest IoU is selected
and used for classification comparison. All metrics count across all videos in the benchmark, instead
of the average per video. This is because the number of cuts is unbalanced in different videos.
Tab. 1 reports the quantitative results.
Traditional shot boundary detection methods such as
PySceneDetect [8], TransNetV2 [29], and AutoShot [43] achieve reasonable performance on overall
range-based metrics, with F1 scores between 0.75 and 0.82. However, they exhibit clear limita-
tions in transition localization and sudden jump detection. In particular, transition IoU remains
low (0.18–0.25), indicating that predicted boundaries are often only roughly aligned with the true
transition ranges. Sudden jump accuracy is also limited, suggesting difficulty in reliably detecting
instantaneous discontinuities. In contrast, our method significantly improves transition localization,
achieving a transition IoU of 0.644, substantially outperforming all baselines. It also achieves the best
range F1 score of 0.881. Moreover, our framework enables structured relation prediction, reaching
0.962 intra-shot accuracy and 0.827 inter-shot accuracy, which are not supported by prior methods. In
the legacy BBC benchmark [4] comparison, we applied an overlap window of 10 between processing
each clip and merging transition labels to match traditional hard-cut only output, and we achieved the
best range recall and F1. The visual result is available in the supplementary.
4.3
Ablation Study
In this section, we conduct ablation studies to examine the impact of key components and hyperpa-
rameter influence on our performance. Results are summarized in Tab. 2.
For the first study, we examine whether the DETR-style range regression objective, L1 + 1D
GIoU [7], is preferable to our proposed formulation, which converts boundary estimation to discrete
classification. In our model, we directly predict discrete boundary labels like classification. For the
L1 + 1D GIoU variant, the model outputs are passed through a sigmoid to map into [0, 1] range, and
then scaled by the maximum prediction length (100 frames in our training). Default 2D GIoU is
changed to a 1D version, based on [19]. As shown in Tab. 2 (a), L1 + 1D GIoU can slightly improve
transition IoU, but it degrades under stricter criteria, such as zero-tolerance sudden jump accuracy
and range F1. We attribute this drop to the inherent difficulty of regression losses in resolving the last
1-2 frames precisely, which is crucial for abrupt hard-cut and sudden-jump boundaries.
In Tab. 2 (b), we study the influence of sampling transition sources from the same SSL-curated
clusters [28, 34] versus purely random selection. In our base setting, we follow [34] and sample
transition sources from the same cluster with 75% probability. Hereby, we construct a variant where
all clips are selected at random. Pure random sampling consistently degrades performance across
all metrics. We hypothesize that semantically aligned clips produce more challenging synthesized
transitions during training, requiring the model to leverage fine-grained temporal and structural cues
to identify subtle content changes. In contrast, randomly paired clips often exhibit large semantic
discrepancies, making the discrimination task comparatively trivial.
8


## Page 9


Table 2:
Ablation studies on key design choices. The best result within each ablation group is
highlighted in bold.
(a) Loss Design
Loss
Trans.
IoU
Sudden
Jump
Acc.
Range
F1
Intra / Inter
Acc.
Classification
0.644
0.759
0.881
0.962 / 0.827
L1 + 1D GIoU
0.718
0.717
0.857
0.956 / 0.809
(b) SSL Data Clustering
Setting
Trans.
IoU
Sudden
Jump
Acc.
Range
F1
Intra / Inter
Acc.
With
0.644
0.759
0.881
0.962 / 0.827
Without
0.551
0.664
0.861
0.957 / 0.722
(c) Short Dense Cuts Distribution
Setting
Trans.
IoU
Sudden Jump
Acc.
Range
F1
Intra / Inter
Acc.
With
0.644
0.759
0.881
0.962 / 0.827
Without
0.610
0.509
0.831
0.955 / 0.790
(d) Encoder Quantity
Quantity
Trans.
IoU
Sudden Jump
Acc.
Range
F1
Intra / Inter
Acc.
3 enc.
0.644
0.759
0.881
0.962 / 0.827
6 enc.
0.598
0.774
0.879
0.955 / 0.815
(e) Training Resolution
Resolution
Trans.
IoU
Sudden Jump
Acc.
Range
F1
Intra / Inter
Acc.
64×96
0.582
0.699
0.877
0.959 / 0.818
96×128
0.644
0.759
0.881
0.962 / 0.827
128×160
0.584
0.723
0.867
0.954 / 0.794
(f) Number of Shot Queries
Number
Trans.
IoU
Sudden Jump
Acc.
Range
F1
Intra / Inter
Acc.
12
0.556
0.735
0.876
0.953 / 0.833
24
0.644
0.759
0.881
0.962 / 0.827
48
0.590
0.753
0.873
0.959 / 0.811
Next, we aim to study whether modeling continuous dense hard cuts and the sudden jump during the
data synthesis is beneficial. Under purely random synthesis, fewer than 0.005% of generated samples
contain more than five consecutive hard cuts, despite such patterns being common in real-world
videos. Therefore, in our base setting, we enforce continuous hard cuts in 25% of the synthesized
videos. Removing this strategy leads to consistent performance degradation across all metrics, as
shown in Tab. 2 (c). These results suggest that understanding real-world shot distributions and
designing synthesis pipelines that better reflect such distributions are important for effective model
training.
For the architectural ablations in Tab. 2 (d)–(f), the base configuration provides the most balanced
overall performance. Increasing the number of encoder layers improves sudden jump accuracy, but
leads to noticeable degradation in most other metrics. A training resolution of 96×128 gives the best
resolution trade-off. For the number of shot queries, using 24 queries yields the strongest overall
results, achieving the best sudden jump accuracy and range F1, whereas 12 and 48 queries only
improve transition IoU and inter-label accuracy, respectively.
5
Conclusion
In this paper, we present OmniShotCut, reformulating shot boundary detection with explicit in-
tra-shot and inter-shot relations by a shot query-based Transformer framework. To overcome the
limitations of manual annotation, we develop a fully synthetic data synthesis pipeline that automat-
ically produces diverse transition effects with precise temporal supervision, and curate a modern
complex shot boundary detection benchmark. Experiments demonstrate that our approach achieves
superior performance across multiple benchmarks and evaluation metrics. Our results suggest that
fully synthetic supervision provides a scalable and effective paradigm for next-generation shot bound-
ary detection datasets. Moreover, our insights into intra- and inter-shot relations may further benefit
downstream applications that require more accurate and explainable shot boundary detection.
Limitations and Future Work.
Despite the strong performance, more sophisticated artistic and
semantically dynamic transitions may require additional modeling beyond our current synthetic
parameterization. In particular, capturing complex cinematic transition patterns could benefit from
large-scale industry-level transition template collections, which are not publicly available. Exploring
such resources remains an interesting direction for future work.
9


## Page 10


References
[1] Amro Abbas, Kushal Tirumala, Dániel Simig, Surya Ganguli, and Ari S Morcos. Semd-
edup: Data-efficient learning at web-scale through semantic deduplication. arXiv preprint
arXiv:2303.09540, 2023.
[2] Niket Agarwal, Arslan Ali, Maciej Bala, Yogesh Balaji, Erik Barker, Tiffany Cai, Prithvijit
Chattopadhyay, Yongxin Chen, Yin Cui, Yifan Ding, et al. Cosmos world foundation model
platform for physical ai. arXiv preprint arXiv:2501.03575, 2025.
[3] George Awad, Asad A Butt, Jonathan Fiscus, David Joy, Andrew Delgado, Willie Mcclinton,
Martial Michel, Alan F Smeaton, Yvette Graham, Wessel Kraaij, et al. Trecvid 2017: evaluating
ad-hoc and instance video search, events detection, video captioning, and hyperlinking. In
TREC video retrieval evaluation (TRECVID), 2017.
[4] Lorenzo Baraldi, Costantino Grana, and Rita Cucchiara. A deep siamese network for scene
detection in broadcast videos. In Proceedings of the 23rd ACM international conference on
Multimedia, pages 1199–1202, 2015.
[5] Lorenzo Baraldi, Costantino Grana, and Rita Cucchiara. Shot and scene detection via hierarchi-
cal clustering for re-using broadcast video. In International conference on computer analysis of
images and patterns, pages 801–811. Springer, 2015.
[6] Nimrod Berman, Adam Botach, Emanuel Ben-Baruch, Shunit Haviv Hakimi, Asaf Gendler, Ilan
Naiman, Erez Yosef, and Igor Kviatkovsky. Scene-vlm: Multimodal video scene segmentation
via vision-language models. arXiv preprint arXiv:2512.21778, 2025.
[7] Nicolas Carion, Francisco Massa, Gabriel Synnaeve, Nicolas Usunier, Alexander Kirillov, and
Sergey Zagoruyko. End-to-end object detection with transformers. In European conference on
computer vision, pages 213–229. Springer, 2020.
[8] Brandon Castellano. Pyscenedetect: Python and opencv-based scene cut/transition detection
program & library. https://github.com/Breakthrough/PySceneDetect, 2025. Soft-
ware.
[9] Shixing Chen, Xiaohan Nie, David Fan, Dongqing Zhang, Vimal Bhat, and Raffay Hamid.
Shot contrastive self-supervised learning for scene boundary detection. In Proceedings of the
IEEE/CVF conference on computer vision and pattern recognition, pages 9796–9805, 2021.
[10] Ahmed Hassanien, Mohamed Elgharib, Ahmed Selim, Sung-Ho Bae, Mohamed Hefeeda, and
Wojciech Matusik. Large-scale, fast and accurate shot boundary detection through spatio-
temporal convolutional neural networks. arXiv preprint arXiv:1705.03281, 2017.
[11] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image
recognition. In Proceedings of the IEEE conference on computer vision and pattern recognition,
pages 770–778, 2016.
[12] Hengrui Hu, Kaining Ying, and Henghui Ding. Segment anything across shots: A method and
benchmark. arXiv preprint arXiv:2511.13715, 2025.
[13] Qingqiu Huang, Yu Xiong, Anyi Rao, Jiaze Wang, and Dahua Lin. Movienet: A holistic dataset
for movie understanding. In European conference on computer vision, pages 709–727. Springer,
2020.
[14] Ziqi Huang, Yinan He, Jiashuo Yu, Fan Zhang, Chenyang Si, Yuming Jiang, Yuanhan Zhang,
Tianxing Wu, Qingyang Jin, Nattapol Chanpaisit, et al. Vbench: Comprehensive benchmark
suite for video generative models. In Proceedings of the IEEE/CVF Conference on Computer
Vision and Pattern Recognition, pages 21807–21818, 2024.
[15] Mehran Jeelani, Noshaba Cheema, Klaus Illgner-Fehns, Philipp Slusallek, Sunil Jaiswal, et al.
Expanding synthetic real-world degradations for blind video super resolution. In Proceedings of
the IEEE/CVF conference on computer vision and pattern recognition, pages 1199–1208, 2023.
10


## Page 11


[16] Tejaswini Kar, Priyadarshi Kanungo, Sachi Nandan Mohanty, Sven Groppe, and Jinghua Groppe.
Video shot-boundary detection: issues, challenges and solutions. Artificial Intelligence Review,
57(4):104, 2024.
[17] Nikita Karaev, Yuri Makarov, Jianyuan Wang, Natalia Neverova, Andrea Vedaldi, and Christian
Rupprecht. Cotracker3: Simpler and better point tracking by pseudo-labelling real videos. In
Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 6013–6022,
2025.
[18] Harold W Kuhn. The hungarian method for the assignment problem. Naval research logistics
quarterly, 2(1-2):83–97, 1955.
[19] Jie Lei, Tamara L Berg, and Mohit Bansal. Detecting moments and highlights in videos via
natural language queries. Advances in Neural Information Processing Systems, 34:11846–11858,
2021.
[20] Zhen Li, Chuanhao Li, Xiaofeng Mao, Shaoheng Lin, Ming Li, Shitian Zhao, Zhaopan Xu,
Xinyue Li, Yukang Feng, Jianwen Sun, et al. Sekai: A video dataset towards world exploration.
arXiv preprint arXiv:2506.15675, 2025.
[21] Zhiqiu Lin, Siyuan Cen, Daniel Jiang, Jay Karhade, Hewei Wang, Chancharik Mitra, Tiffany
Ling, Yuhan Huang, Sifan Liu, Mingyu Chen, et al. Towards understanding camera motions in
any video. arXiv preprint arXiv:2504.15376, 2025.
[22] Hongbo Liu, Jingwen He, Yi Jin, Dian Zheng, Yuhao Dong, Fan Zhang, Ziqi Huang, Yinan
He, Yangguang Li, Weichao Chen, et al. Shotbench: Expert-level cinematic understanding in
vision-language models. arXiv preprint arXiv:2506.21356, 2025.
[23] Alhassan Mumuni, Fuseini Mumuni, and Nana Kobina Gerrar. A survey of synthetic data
augmentation methods in machine vision. Machine Intelligence Research, 21(5):831–869, 2024.
[24] Jonghwan Mun, Minchul Shin, Gunsoo Han, Sangho Lee, Seongsu Ha, Joonseok Lee, and
Eun-Sol Kim. Bassl: Boundary-aware self-supervised learning for video scene segmentation.
In Proceedings of the Asian Conference on Computer Vision, pages 4027–4043, 2022.
[25] Kepan Nan, Rui Xie, Penghao Zhou, Tiehan Fan, Zhenheng Yang, Zhijie Chen, Xiang Li, Jian
Yang, and Ying Tai. Openvid-1m: A large-scale high-quality dataset for text-to-video generation.
arXiv preprint arXiv:2407.02371, 2024.
[26] Zhenglin Pan.
Sakuga-42m dataset:
Scaling up cartoon research.
arXiv preprint
arXiv:2405.07425, 2024.
[27] Anyi Rao, Linning Xu, Yu Xiong, Guodong Xu, Qingqiu Huang, Bolei Zhou, and Dahua Lin.
A local-to-global approach to multi-modal movie scene segmentation. In Proceedings of the
IEEE/CVF conference on computer vision and pattern recognition, pages 10146–10155, 2020.
[28] Oriane Siméoni, Huy V Vo, Maximilian Seitzer, Federico Baldassarre, Maxime Oquab, Cijo
Jose, Vasil Khalidov, Marc Szafraniec, Seungeun Yi, Michaël Ramamonjisoa, et al. Dinov3.
arXiv preprint arXiv:2508.10104, 2025.
[29] Tomás Soucek and Jakub Lokoc. Transnet v2: An effective deep network architecture for
fast shot transition detection. In Proceedings of the 32nd ACM International Conference on
Multimedia, pages 11218–11221, 2024.
[30] Tomáš Souˇcek, Jaroslav Moravec, and Jakub Lokoˇc. Transnet: A deep network for fast detection
of common shot transitions. arXiv preprint arXiv:1906.03363, 2019.
[31] Mohammad Reza Taesiri, Finlay Macklon, and Cor-Paul Bezemer. Clip meets gamephysics:
Towards bug identification in gameplay videos using zero-shot transfer learning. In Proceedings
of the 19th International Conference on Mining Software Repositories, pages 270–281, 2022.
[32] Zhiyu Tan, Xiaomeng Yang, Luozheng Qin, and Hao Li. Vidgen-1m: A large-scale dataset for
text-to-video generation. arXiv preprint arXiv:2408.02629, 2024.
11


## Page 12


[33] Shitao Tang, Litong Feng, Zhanghui Kuang, Yimin Chen, and Wei Zhang. Fast video shot
transition localization with deep structured models. In Asian Conference on Computer Vision,
pages 577–592. Springer, 2018.
[34] Huy V Vo, Vasil Khalidov, Timothée Darcet, Théo Moutakanni, Nikita Smetanin, Marc
Szafraniec, Hugo Touvron, Camille Couprie, Maxime Oquab, Armand Joulin, et al. Au-
tomatic data curation for self-supervised learning: A clustering-based approach. arXiv preprint
arXiv:2405.15613, 2024.
[35] Team Wan, Ang Wang, Baole Ai, Bin Wen, Chaojie Mao, Chen-Wei Xie, Di Chen, Feiwu Yu,
Haiming Zhao, Jianxiao Yang, et al. Wan: Open and advanced large-scale video generative
models. arXiv preprint arXiv:2503.20314, 2025.
[36] Boyang Wang, Bowen Liu, Shiyu Liu, and Fengyu Yang. Vcisr: Blind single image super-
resolution with video compression synthetic data. In Proceedings of the IEEE/CVF winter
conference on applications of computer vision, pages 4302–4312, 2024.
[37] Qiuheng Wang, Yukai Shi, Jiarong Ou, Rui Chen, Ke Lin, Jiahao Wang, Boyuan Jiang, Haotian
Yang, Mingwu Zheng, Xin Tao, et al. Koala-36m: A large-scale video dataset improving
consistency between fine-grained conditions and video content. In Proceedings of the Computer
Vision and Pattern Recognition Conference, pages 8428–8437, 2025.
[38] Sheng-Yu Wang, Oliver Wang, Andrew Owens, Richard Zhang, and Alexei A Efros. Detecting
photoshopped faces by scripting photoshop. In Proceedings of the IEEE/CVF International
Conference on Computer Vision, pages 10072–10081, 2019.
[39] Xintao Wang, Liangbin Xie, Chao Dong, and Ying Shan. Real-esrgan: Training real-world
blind super-resolution with pure synthetic data. In Proceedings of the IEEE/CVF international
conference on computer vision, pages 1905–1914, 2021.
[40] Yuqing Wang, Zhaoliang Xu, Xinlong Wang, Chunhua Shen, Baoshan Cheng, Hao Shen, and
Huaxia Xia. End-to-end video instance segmentation with transformers. In Proceedings of the
IEEE/CVF conference on computer vision and pattern recognition, pages 8741–8750, 2021.
[41] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu,
Chang Gao, Chengen Huang, Chenxu Lv, et al. Qwen3 technical report. arXiv preprint
arXiv:2505.09388, 2025.
[42] Zhuoyi Yang, Jiayan Teng, Wendi Zheng, Ming Ding, Shiyu Huang, Jiazheng Xu, Yuanming
Yang, Wenyi Hong, Xiaohan Zhang, Guanyu Feng, et al. Cogvideox: Text-to-video diffusion
models with an expert transformer. arXiv preprint arXiv:2408.06072, 2024.
[43] Wentao Zhu, Yufang Huang, Xiufeng Xie, Wenxian Liu, Jincan Deng, Debing Zhang,
Zhangyang Wang, and Ji Liu.
Autoshot: A short video dataset and state-of-the-art shot
boundary detection. In Proceedings of the IEEE/CVF Conference on Computer Vision and
Pattern Recognition, pages 2238–2247, 2023.
12


## Page 13


Dip to White
Wipe Bars
Whip Pan
Spin In
Swap
Fade to Black
Spin Out
Wipe Circle Open
Wipe Spin
Fade from White
Fade from  Black
Push
Mosaic
Cross Blur
Puzzle Blend
Cross Zoom
Ripple Dissolve
Cube
Ripple Open
Figure 6:
Full Transition Types. We complement the transition types listed in the main paper
section.
Supplementary Material
This supplementary material provides more implementation and technical details and additional
qualitative visualization to complement the main manuscript. In Sec. A, we present full transition
genre types. In Sec. B, we present more information about the transition synthesis parameter setting.
In Sec. C, we present more implementation details for the model training and setting. In Sec. D, we
present the benchmark annotation GUI and details. In Sec. E, we present the visual comparisons
between different models.
A
Full Transition Genre Types
In the main paper, we provide the main transition type visualization. However, this is still not all
the types we consider. We consider numerous subtypes in transition and classify them into different
categories based on the pattern. The visualization is shown in Fig. 6.
We consider a diverse taxonomy of editing transitions covering both common and fine-grained
variants. Specifically, the transition set includes Dissolve transitions (Transparent Dissolve, Cross-
Blur Dissolve, and Ripple Dissolve); Wipe transitions (Unidirectional Wipe, Diagonal Wipe, Circular
Wipe, Bar Wipe, Ripple Wipe, Page-Curl Wipe, and Mosaic Wipe); Push transitions (Unidirectional
Push and Puzzle Push); Slide transitions (Horizontal Slide, Whip-Pan Slide, and Cube Slide); Zoom
transitions (Zoom In/Out, Spin In/Out, Cross Zoom, and Swap Zoom); Fade transitions (Fade to
Black, Fade to White, Fade from Black, Fade from White, Dip to Black, and Dip to White); and
Doorway transitions (Doorway Open).
13


## Page 14


a) Genre Distribution
b) Transition Type Distribution
Figure 7: Left: Our curation pipeline scales to internet-scale, wide-domain video collection and
yields ∼1.5M curated clip source for transition synthesis; genres are annotated by Qwen3 [41].
Right: Transition statistics of the synthetic corpus. The inner ring shows the inter-shot relation
distribution, and the outer ring breaks down all of the main and sub-transition types that our pipeline
can synthesize. In total, we synthesize 11.9M transitions for training.
B
Transition Synthesis Details
In this section, we share our transition synthesis details, which are the key to our training dataset
construction. A preview can be found in Fig. 7.
In the curation stage, our video sources are mostly coming from existing video datasets on Hug-
gingface, which include datasets like OpenVid [25], VidGen [32], Sakuga [26], GamePhysics [31],
and several publicly accessible sources. we set continuous similarity threshold εsim to 0.9 and
deduplication threshold εdup to 0.05. The motion tracking [17] is sampled per 3 frames at 256x320
resolution. The number of SSL clusters [34] is set to 27,000, where we use DINOv3 [28] ViT large
variant. We discard cluster sizes that are less than 5 videos to avoid reusing the same video source.
We construct our synthetic transition training data via a fully parameterized pipeline. The number
of clips per video is sampled from a Poisson distribution with λ = 7.0 and constrained to [1, 28].
Clip durations are sampled from Gaussian distributions of N(2.8, 1.62) seconds. 75% of clips are
selected from the same DINOv3 [28] cluster to maintain semantic coherence. For sudden-jump cases,
we crop [24, 40] frames, and their valid source videos should be those with motion strength in the
[25, 60] percentile range, sorted from slowest to fastest. We further assign 25% of the synthesis to be
extremely short and dense composition, where we generate continuous 28 videos that are within the
duration of [0.15, 1.0] seconds for each clip. For the offline augmentation, we apply 5% on adding
subtitle text, and 7.5% on the lighting variations. In total, we create 300K synthetic videos used for
training, where each of them contains at least 240 frames at 24 fps. The quantity of synthesis videos
can be infinite, but we set it to 300K videos as a reasonable range.
The distribution of each transition is different. We sample 35% for the hard cut. In the dissolve type
transition, 9.4% is distributed for the transparent dissolve, 2.4% for the cross-blur dissolve, and 1.8%
for the ripple dissolve. In the wipe type transition, 4.7% is distributed evenly for the vanilla wipe
in up, down, bottom, and right directions, 2.4% for spin wipe, 2.4% for circle open and close wipe,
1.2% for the bar wipe, 1.2% for the ripple wipe, and 1.2% for the mosaic wipe. In the push-type
transition, 4.7% is distributed evenly for the vanilla push in up, down, bottom, and right directions,
and 1.8% for the puzzle blending push. In the slide-type transition, 4.7% is distributed evenly for the
vanilla slide, 4.1% for the whip pan, and 1.8% for the cube slide. In the zoom-type transition, 2.4% is
distributed for the zoom in, 2.4% for the zoom out, 2.4% for the spin in and out, 1.2% for the cross
zoom, and 1.8% for the swap. In the fading-type transition, 2.9% is distributed for fading the first
source to black or white screen, 2.9% for fading the second source from black or white screen, and
2.9% for the dip fading effect. In the doorway transition, 2.9% is distributed.
For all transition types, we carefully control as many parameters as possible to ensure consistency
and precise manipulation. This yields a large set of explicit control philosophies spanning (i) discrete
mode switches (e.g., transition direction, hard vs. soft edges, constant vs. linear smoothing), (ii)
temporal controls (including the start time, duration, and the speed curve of the transition over time),
(iii) spatial controls (anchor locations and margins for added text, effect centers for zoom/ripple, grid
14


## Page 15


① Load extracted frames
② Select a video case
③ Add or modify 
shot boundaries
④ Annotate segment type, 
relation, and confidence
Figure 8: Benchmark Annotation Tool. Annotators first load extracted frames and select a video
case. Shot boundaries are created by clicking between frames along the timeline. The right panel
provides an overview of segments and enables labeling of type, relation, and confidence. Additional
features, including multi-selection, auto-save, and frame-level inspection, facilitate efficient dataset
construction.
resolution for mosaic, doorway seam orientation), and (iv) intensity controls (blurring range and curve
shape, zoom magnitude and sampling density, lighting gains/gamma/contrast and color wash/spotlight
strength, feather widths for soft boundaries). Additionally, we control content-level factors such as
text selection and layout (wrapping, line count, spacing), while dropping near-duplicate frames on the
edge of transition phases. Overall, our transition synthesis pipeline defines a reproducible distribution
over diverse transitions with fine-grained, interpretable parameters that can be tuned. To implement
the transition, we apply LLM as an auxiliary tool, but humans do the final check to ensure that the
transition is correct.
C
More Implementation Details
For the model training, we optimize a weighted sum of three classification losses:
L = λrange Lrange + λintra Lintra + λinter Linter,
(1)
where
Lrange = 1
N
N
X
i=1
CE
 pend
i , yend
i

,
(2)
Lintra = 1
N
N
X
i=1
CE
 pintra
i
, yintra
i

,
(3)
Linter = 1
N
N
X
i=1
CE
 pinter
i
, yinter
i

.
(4)
In the experiment, λrange, λintra, λinter is set to 5, 1, 1.
D
Benchmark Annotation Details
As shown in Fig. 8, we develop an annotation tool for our OmniShotCut bench. This tool helps us
swiftly locate the boundaries on the per-frame level and label dense transition cases for long video
15


## Page 16


Figure 9: Annotation Tool Open-Image Inspection Mode. The Inspection mode shows the high
resolution and labeling details for the annotators to define subtle transition changes accurately. It can
be played as videos fluently by pressing the buttons to check gradual transitions frame-by-frame.
instances. To facilitate efficient annotation, we implement several useful features. A floating window
dynamically displays the current segment’s labels (type and confidence) or the relation label, allowing
annotators to quickly verify existing annotations. In addition, the tool supports multi-selection,
enabling annotators to label multiple segments or relations simultaneously with a single action. An
auto-save mechanism is also integrated to automatically store labeling progress and prevent data loss.
Certain transitions of interest in our benchmark, such as sudden jumps, dissolves, and fades, often
involve subtle frame-level changes that require careful inspection. To address this, we introduce an
open-image inspection mode (see Fig. 9). Annotators can open a frame by double-clicking or pressing
the space bar, which displays the frame along with its associated type, confidence, and relation
annotations. Using the left and right arrow keys, annotators can navigate through frames sequentially,
effectively previewing the sequence as a short video clip. These features together provide an efficient
and user-friendly platform for constructing and verifying our benchmark dataset. A preview of the
videos in the benchmark is shown in Fig. 10.
E
Visual Comparisons
The visual comparison result is shown in Fig. 11. As we can see, our model succeeded in the fading
and dissolve transition as well as sudden jump detection. Baseline models like TransNet V2 [29]
and AutoShot [43] failed, where they usually choose the start frame in the middle of the dissolve or
fading effects. This confusing first frame is not friendly for the downstream applications like video
generation, where they demand a clear first frame source for the image-to-video generation. Our
result aligns with the ground-truth labels. Further, these baselines cannot realize the sudden jump,
which lacks sensitivity to the subtle changes.
16


## Page 17


Figure 10: OmniShotCut Bench Sample Images. Our benchmark covers diverse topics spanning
lifestyle, sports, entertainment, anime, game, unboxing, vlog, shorts, tutorials, urban scenes, screen-
based media, and so on.
17


## Page 18


AutoShot
TransNet V2
GT
Ours
AutoShot
TransNet V2
Ours
GT
AutoShot
TransNet V2
Video 1
Video 2
Video 3
Ours
GT
Figure 11: Shot Boundary Detection Qualitative Comparisons. We compare TransNet V2 [29],
AutoShot [43], and ours on Fading (video 1), Sudden Jump (video 2), and Dissolve (video 3). Each
vertical bar with the same color denotes the start and end of a clip cut by the model. Zoom in for the
best view.
18
