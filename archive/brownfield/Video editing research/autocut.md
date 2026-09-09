# autocut

*Source PDF: `autocut.pdf`*

*Total Pages: 18*

---


## Page 1


AutoCut: End-to-end advertisement video editing based on multimodal
discretization and controllable generation
Milton Zhou1,2,*
Sizhong Qin1,2,*
Yongzhi Li2,†
Quan Chen2,‡
Peng Jiang2
1Tsinghua University
2Kuaishou Technology
{zhoukx23, qsz23}@mails.tsinghua.edu.cn
{liyongzhi03,chenquan06,jiangpeng}@kuaishou.com
Abstract
Short-form videos have become a primary medium for dig-
ital advertising, requiring scalable and efficient content
creation.
However, current workflows and AI tools re-
main disjoint and modality-specific, leading to high pro-
duction costs and low overall efficiency. To address this
issue, we propose AutoCut, an end-to-end advertisement
video editing framework based on multimodal discretiza-
tion and controllable editing. AutoCut employs dedicated
encoders to extract video and audio features, then applies
residual vector quantization to discretize them into uni-
fied tokens aligned with textual representations, construct-
ing a shared video–audio–text token space. Built upon a
foundation model, we further develop a multimodal large
language model for video editing through combined mul-
timodal alignment and supervised fine-tuning, supporting
tasks covering video selection and ordering, script gen-
eration, and background music selection within a unified
editing framework. Finally, a complete production pipeline
converts the predicted token sequences into deployable long
video outputs.
Experiments on real-world advertisement
datasets show that AutoCut reduces production cost and it-
eration time while substantially improving consistency and
controllability, paving the way for scalable video creation.
Code and data are available at: https://github.
com/AdAutoCut/Autocut
1. Introduction
Advertising videos have become one of the most influen-
tial forms of digital marketing, allowing brands to com-
municate persuasive narratives through multimodal visual
storytelling. However, producing short-form advertisement
videos remains a costly and labor-intensive process that
involves scripting, material shooting, editing, and post-
*Equal contribution. Work done during an internship at Kuaishou.
†Project Leader, ‡Corresponding author.
AutoCut Model
Prompt
1 fps
20 fps
Background Music
Visual 
Encoder
Visual 
Encoder
Audio
Encoder
Video
Database
Audio
Database
Video Embeddings
Audio Embeddings
Video Embeddings
RQ-VAE
Encoder
RQ-VAE
Encoder
Video Tokens
Audio Tokens
Video Tokens
Audio Tokens
Text Tokens
RQ-VAE
Decoder
RQ-VAE
Decoder
TTS
Engine
Retrieve
Retrieve
Scripts
Video clips
Result Ads
Video
This T-shirt is
a
hit-crafted
with precision
and
designed
for style…
Audios
Subtitle
Figure 1. Overview of the AutoCut framework. Low–fps frames
are tokenized for efficient multimodal reasoning, while high–fps
frames are kept for accurate visual matching and clip retrieval.
Given optional inputs, AutoCut predicts video, text, and audio to-
kens, which are decoded or retrieved to compose the final adver-
tisement video.
production refinement. This multi-stage workflow requires
professional expertise and substantial manual effort, creat-
ing high entry barriers for small enterprises and non-expert
creators [41, 50].
To alleviate these challenges, recent studies have ex-
arXiv:2603.28366v1  [cs.CV]  30 Mar 2026


## Page 2


plored intelligent systems that automate parts of the video
creation pipeline. Early works such as VideoDiscovery [50]
and Wei et al. [41] proposed multimodal retrieval frame-
works that generate advertising videos directly from de-
scriptive copy, reducing manual effort but still relying on
rigid, predefined templates.
Lin et al. [22] and Tang et
al. [31] further introduced multimodal editing and segment-
assemblage networks to improve visual coherence. Nev-
ertheless, these modular approaches remain constrained by
handcrafted rules and offer limited global controllability.
With the emergence of multimodal large language mod-
els (MLLMs), new opportunities have arisen for end-to-end
video understanding and editing. Cheng et al. [6] proposed
a text-to-edit paradigm that enables users to create videos
through natural-language instructions, while Qian et al. [29]
introduced VC-LLM, which achieves human-comparable
advertisement video generation via multi-resolution spa-
tial–temporal reasoning. These studies highlight the poten-
tial of MLLMs to unify perception, understanding, and cre-
ation within a single framework. However, directly apply-
ing standard MLLM models to advertising creation scenar-
ios is limited by constrained context window sizes, making
it challenging to handle large-scale video retrieval and edit-
ing tasks.
Nevertheless, existing systems still face three major ob-
stacles that hinder scalable, controllable, and coherent video
creation:
• Loose multimodal coupling.
Representations across
modalities are often weakly aligned, preventing unified
reasoning among video, audio, and textual signals.
• Lack of interpretable control. Most models do not pro-
vide structured or discrete representations, making it dif-
ficult to adjust narrative rhythm, temporal composition,
and content emphasis in a controllable manner.
• Fragmented understanding and generation. Current
pipelines treat multimodal understanding and generation
as separate processes, leading to inconsistent optimiza-
tion and unstable editing quality.
In this work, we present AutoCut, an end-to-end intelli-
gent advertisement video editing framework that integrates
multimodal discretization and controllable editing. Auto-
Cut unifies video, audio, and textual information within a
shared discrete token space, enabling fine-grained multi-
modal reasoning and precise editing control. By leveraging
large-scale real-world advertisement data, AutoCut signifi-
cantly reduces production costs while enhancing coherence,
controllability, and creative quality.
Our main contributions are summarized as follows:
• Proposes the first unified framework that bridges multi-
modal understanding and controllable editing for adver-
tisement video creation.
• Designs a multimodal discretization strategy that trans-
forms video, audio, and text signals into interpretable
tokens, enabling controllable and semantically aligned
video editing.
• Establishes a large-scale advertisement video dataset and
demonstrates through extensive experiments that Auto-
Cut achieves superior coherence, editing consistency, and
content controllability compared with existing methods.
2. Related Work
2.1. Template-Based Methods
Early research formalized video editing as rule-based or
template-based composition to maintain narrative coher-
ence and stylistic consistency.
Ahanger and Little [1]
introduced metadata-driven dynamic composition, while
systems such as QuickCut [34] and multi-camera frame-
works [2] extended these ideas to dialogue-driven and
viewpoint-driven assembly.
Commercial tools including
Magisto, CapCut, and iMovie encoded cinematic conven-
tions into templates that automatically determine shot or-
der, transition types, and pacing. Lu et al. [24] added rule-
constrained optimization for product-oriented video edit-
ing. Although these systems maintain structure, their de-
pendence on predefined rules restricts flexibility. Recent
datasets such as AVE [3] and shot-order benchmarks [20]
have enabled data-driven extensions beyond handcrafted
templates.
2.2. Retrieval-Based Methods
Retrieval-based approaches frame editing as multimodal
search followed by clip assembly.
Systems such as
VideoDiscovery [50] and Wei et al. [41] retrieve footage
aligned with textual descriptions for advertisement creation.
Script-driven methods including Write-A-Video [36], B-
Script [14], and Transcript-to-Video [44] improve textual-
visual alignment, while Story-Driven Editing [39] enhances
temporal organization. For multi-source workflows, Deep-
QAMVS [26] and Condensed Movies [5] address summa-
rization and narrative reconstruction. These methods pro-
vide efficient clip-level editing but remain limited by dataset
coverage and retrieval accuracy.
VEU-Bench [19] offers
complementary evaluation for understanding editing oper-
ations and narrative structure.
2.3. Generative Methods
Generative approaches synthesize or modify content be-
yond direct retrieval.
Early research explored unsuper-
vised highlight detection [30, 43, 47] and multimodal sum-
marization [25, 52]. M-SAN [31] introduced importance
and coherence rewards for advertisement editing, and mul-
timodal encoders [10] improved cross-modal representa-
tion learning. Interactive systems such as ReelFramer [37],
ChunkyEdit [16], and ExpressEdit [33] support text-guided
and sketch-guided content manipulation. Hybrid pipelines


## Page 3


Script 2
<|audio_start|>
<|audio_0_2|>
<|audio_1_7|>
…
<|audio_7_1>
<|audio_end|>
<|video_start|>
<|video_0_2|>
<|video_1_7|>
…
<|video_7_8>
<|video_end|>
<|text_start|>
Script 1
<|text_end|>
Script 1
…
Audio
…
Text 1
Frame 1
Frame 2
<|clip_start|>
<|clip_end|>
Text 2
Frame 3
Frame 4
<|clip_start|>
<|clip_end|>
Frame 5
<|clip_end|>
LLM
Original Embedding
Added Token Embedding
LLM Backbone
Stage1: Align Added
Embeddings
Stage2: Multi-Task
Supervised Fine-tuning
Video Selection
Video Sorting
Script Generation
BGM Selection
BGM
LLM
Multimodal
Tokenization
Alignment
Input Sequence
Task-Specific Data
Figure 2. Overview of the proposed AutoCut framework. Multimodal tokenization converts scripts, frames, and audio into unified
discrete tokens, which are organized into an alignment input sequence. Stage 1 performs multimodal alignment on large-scale data to
align the added token embeddings with the LLM backbone. Stage 2 applies task-specific SFT for video selection, video sorting, script
generation, and BGM selection.
such as Computational Video Editing [17] integrate retrieval
and generation using semantic alignment and HMM-based
optimization. Benchmarks including Shot2Story [11] and
Synchronized Video Storytelling [46] further evaluate story-
level controllability. Despite these advances, generative ap-
proaches still struggle with temporal consistency, realism,
and multi-scene stability.
2.4. MLLM-Based Methods
Multimodal Large Language Models shift video editing
from pattern-driven workflows toward reasoning-driven or-
chestration across modalities. Systems such as LAVE [35],
Ding et al. [7], and LITA [13] incorporate temporal cues
such as time tokens or SlowFast [8] features for lo-
calized editing.
Subsequent methods including Text-to-
Edit [6], VC-LLM [29], and Tree-of-AdEditor [51] apply
high-level reasoning to multi-scene advertisement assem-
bly.
Shots2Stories [21] further investigates LLM-guided
shot ordering and clip-level coherence.
A related direction combines MLLMs with diffusion
models for pixel-level manipulation. Systems such as In-
structX [27], UNIC [48], UniVideo [40], and VEGGIE [49]
focus on instruction-driven visual transformation rather
than clip selection, sequencing, or narrative assembly.
Although these methods demonstrate strong multimodal
reasoning, most rely on separate modules for understand-
ing, retrieval, and composition. This separation limits narra-
tive coherence, cross-modal stability, and fine-grained con-
trol in advertisement video creation. To address these lim-
itations, we propose AutoCut, which discretizes video, au-
dio, and text into a unified token vocabulary and performs
end-to-end multimodal reasoning for coherent and control-
lable editing.
3. Method
We propose AutoCut, a unified framework for multimodal
discretization and controllable video editing. As illustrated
in Figure 2, AutoCut converts continuous video and audio
embeddings into discrete tokens, trains a large language
model to capture cross-modal dependencies, and recon-
structs coherent short-video advertisements through token
retrieval and rendering.
3.1. Task Formulation
Our framework is designed to handle multiple tasks in ad-
vertisement video editing, where multimodal inputs—text,
video, and audio—interact within a shared representation
space. Let X = {xp, xt, xv, xa} denote the set of pos-
sible input modalities, including product information (xp),
textual script (xt), video clips (xv), and background music
(xa). Depending on the specific task, the model receives
a subset of these modalities as input and produces task-
dependent outputs y, such as clip sequences, textual scripts,
or background music.
To comprehensively evaluate the framework, we define
four representative tasks that correspond to the major stages
of the ad-creation workflow: (1) video selection, (2) tempo-


## Page 4


ral ordering, (3) script generation, and (4) background mu-
sic selection. These tasks together assess the model’s multi-
modal reasoning ability and its capacity to achieve coherent
and controllable advertisement editing.
3.2. Multimodal Encoder
Visual Encoder. We adopt an off-the-shelf CNN encoder
based on the ResNet-50[12] architecture to extract dense
frame-level embeddings from video frames. The visual en-
coder was pre-trained with a contrastive learning objective
on a large corpus of real-world advertising video frames.
As a result, the extracted embeddings exhibit strong seman-
tic expressiveness and high discriminability, which greatly
facilitate subsequent quantization and enable effective re-
trieval of video segments in downstream applications. We
choose this encoder as a practical trade-off between repre-
sentation quality, cost, and efficiency.
Audio Encoder. We utilize Pretrained Audio Neural Net-
works (PANNs) [15] to obtain high-level audio embeddings
from each clip. Trained on the large-scale AudioSet dataset,
PANNs demonstrate strong generalization across diverse
acoustic environments. Each audio segment is first con-
verted into a log-mel spectrogram and processed by the
Wavegram-Logmel-CNN backbone to capture both tempo-
ral and spectral features. The resulting embeddings, repre-
senting the semantic acoustic content, are then discretized
through the RQVAE quantizer to form audio tokens aligned
with the unified multimodal vocabulary.
3.3. Tokenization and Codebook Construction
The video and audio embeddings are continuous, while
large language models operate on discrete token sequences.
To bridge this gap, we adopt the Residual Quantized Vari-
ational AutoEncoder (RQVAE) [18] to discretize contin-
uous multimodal representations.
RQVAE progressively approximates high-dimensional
latent features through residual quantization, enabling effi-
cient compression into a limited codebook. This process es-
tablishes a bidirectional mapping between continuous em-
beddings f and discrete token indices z, trained via cosine
reconstruction loss:
Lrec = 1 −cos( ˆf, f),
(1)
where ˆf denotes the reconstructed feature. We set the code-
book size to 256×8, encoding each video frame or audio
segment into eight tokens. This configuration achieves high
reconstruction quality (cosine similarity of 0.89 for video
and 0.96 for audio) while maintaining manageable token
length. The discrete tokens are then integrated into a shared
multimodal vocabulary with text tokens.
3.4. Multimodal Alignment
With the unified token vocabulary established, we perform
a multimodal alignment stage to teach the model how video,
audio, and text tokens correspond to each other. Each train-
ing sample consists of temporally aligned sequences of mul-
timodal tokens serialized into a unified input string. The
model is optimized under a next-token prediction paradigm:
LNTP = −
X
t
log P(xt | x<t),
(2)
where xt denotes tokens from any modality.
We use Qwen3-8B [45] as the base model and train on
approximately 700K filtered advertisement samples. Dur-
ing alignment, the backbone is kept frozen, and only the
newly introduced multimodal embedding layers are up-
dated. This design stabilizes early training and ensures that
video, audio, and text representations are projected into a
shared semantic space before full task-specific adaptation.
Through this stage, the model learns essential cross-
modal correspondences, such as script–scene grounding,
audio–visual rhythm synchronization, and basic temporal
structures common in short-video advertisements.
3.5. Supervised Fine-Tuning
Following multimodal alignment, we perform supervised
fine-tuning (SFT) to teach the model task-specific behavior.
In contrast to the alignment stage, which applies next-token
prediction to the entire sequence, SFT computes the loss
only over the response portion of the sequence. Each train-
ing sample consists of an input context and a designated
target output such as an ordered clip sequence or a gener-
ated script. The model is optimized to accurately produce
this target segment.
We employ full-parameter fine-tuning using the same
optimization setup as in the alignment stage.
Through
this SFT procedure, AutoCut learns to perform control-
lable editing actions conditioned on user inputs, enabling
coherent and stylistically consistent advertisement creation
across a wide range of editing scenarios.
3.6. Retrieval and Rendering
After the model generates discrete token sequences, we re-
construct playable videos through retrieval and rendering as
shown in Figure 1. Video tokens are mapped to the near-
est clip embeddings in the material database using FAISS-
based similarity search, producing visually matched scenes.
Audio tokens are decoded or retrieved to align background
music and voice-over components. Finally, ffmpeg is used
to concatenate video clips, add transitions, overlay subti-
tles, and render the final MP4 output. This process bridges
token-level editing decisions and executable video produc-
tion, ensuring that AutoCut’s outputs are realistic, coherent,
and production-ready.


## Page 5


0
40
80 120 160
0.0
0.6
1.2
1.8
2.4
Count
1e4
Clips per Video
0
40
80 120 160
0.0
1.5
3.0
4.5
6.0
Count
1e6
Clip Duration (sec)
0
150
300
450
0.0
0.4
0.8
1.2
Count
1e4
Video Duration (sec)
0
50
100 150 200
0.0
0.4
0.8
1.2
Count
1e6
Clip Text Length
0
400 800 12001600
0
2
4
6
Count
1e3
Video Text Length
0
8
16
24
0
2
4
6
Count
1e3
Clips per Video
3
6
9
12
0.0
1.5
3.0
4.5
Count
1e5
Clip Duration (sec)
0
15
30
45
60
0
1
2
3
4
Count
1e3
Video Duration (sec)
0
30
60
90 120
0.0
0.4
0.8
1.2
Count
1e5
Clip Text Length
0
100 200 300 400
0
2
4
6
Count
1e2
Video Text Length
Figure 3. Dataset statistics for the multimodal alignment (top) and SFT (bottom) stages. The alignment dataset is substantially larger but
exhibits more diverse and irregular distributions, while the SFT dataset is smaller yet more balanced and of higher annotation quality.
4. Experiments
4.1. Dataset Construction
All data are collected from short-form advertisement videos
sourced from online platforms. Each record includes a com-
plete advertisement video together with its associated prod-
uct metadata, such as category, brand, and selling points.
Data Parsing.
Each advertisement video is parsed into three modali-
ties: text, video, and audio. The spoken script is extracted
by ASR and aligned with timestamps at the clip level.
Video frames are sampled at 1 fps with ffmpeg and en-
coded into visual embeddings, while raw audio is separated
with pydub, followed by speech–music separation and au-
dio embedding extraction using pann inference [15]. Fi-
nally, each video is segmented into short clips according to
punctuation-aligned ASR timestamps, yielding a sequence
of synchronized multimodal segments.
Data Processing. The parsed multimodal data are used to
construct two datasets: a large-scale multimodal alignment
dataset and a smaller SFT dataset.
For the multimodal alignment stage, advertisements with
strong user engagement are retained, while videos that con-
tain lyrical music or lack human speech are removed. Video
and audio embeddings are discretized into token represen-
tations through RQVAE models, and the three modalities
are integrated into unified advertisement samples. After fil-
tering, the alignment dataset contains approximately 700K
samples.
For the SFT stage, additional selection is applied to build
a curated subset for downstream training. We retain videos
shorter than 120 seconds, with clip lengths between 2 and
60 seconds, and with high visual-text relevance measured
by Qwen-VL. Around 100K samples remain after filtering.
Each record includes product metadata and is reorganized
to support four task types:
• Video Selection: Select relevant clips from a candidate
pool.
• Video Sorting: Arrange selected clips into a coherent
temporal sequence.
• Script Generation: Produce textual narration aligned
with the visual content.
• Background Music Selection: Retrieve or generate mu-
sic that matches the multimodal context.
This task-oriented design enables the model to learn
multimodal understanding and prediction in a unified man-
ner and forms the basis for controllable video editing. De-
tailed construction procedures are provided in the supple-
mentary material.
Data Statistics. Figure 3 reports the core statistics shared
by both training stages, including the number of clips per
video, clip duration, overall video duration, clip text length,
and video text length. These measurements describe the
temporal structure and linguistic density of advertisement
videos.
For the multimodal alignment stage, we use a large-scale
corpus that presents broad variation across all five metrics.
Although the data contain imperfect boundaries and par-
tially noisy transcripts, the scale and diversity of the cor-
pus are valuable for learning stable cross-modal alignment
among video, audio, and text tokens.
For the SFT stage, we curate a smaller yet significantly
higher-quality subset. The same statistics apply, but the data
provide cleaner segmentation and more accurate textual an-


## Page 6


notations, making them better suited for training control-
lable editing behaviors and coherent advertisement genera-
tion.
By combining a diverse alignment corpus with a curated
SFT dataset, we adopt a two-stage pipeline consisting of
multimodal alignment followed by supervised fine-tuning.
This strategy removes the need for full-scale pretraining
while maintaining strong performance.
4.2. Evaluation Metrics
We employ a set of quantitative and qualitative metrics to
evaluate different aspects of the proposed framework, in-
cluding multimodal alignment, video clip selection, ranking
consistency, script quality, and audio retrieval performance.
All metrics are defined below.
Visual–Script Correlation (VSC). VSC measures the se-
mantic consistency between the selected video clips and the
corresponding advertisement script. Each video–script pair
is evaluated by a large language model (GPT-4o), which as-
signs a discrete score from {0, 1, 2} based on the degree of
alignment, where higher values indicate stronger semantic
correspondence.
Clips Selection Accuracy (CSA). CSA quantifies the ac-
curacy of identifying positive video clips. It is defined as:
CSA = Nselect
Ntotal
× 100%,
where Nselect denotes the number of samples that contain
only positive clips, and Ntotal represents the total number of
evaluated samples.
Clips Rank Accuracy (CRA). CRA evaluates the correct-
ness of the predicted order of video clips. It is calculated
as:
CRA = Ncorrect
Ntotal
× 100%,
where Ncorrect is the number of samples whose predicted
clip sequences match the reference ordering exactly, and
Ntotal is the total number of samples.
Script Quality (SQ). SQ evaluates the overall textual qual-
ity of the generated advertisement scripts. We employ a
GPT-4o–based evaluator following a three-category, 100-
point rubric that covers: (1) Basic Quality (30 pts), as-
sessing factual correctness, clarity, and content safety; (2)
Expression and Communication (40 pts), measuring lin-
guistic naturalness, audience engagement, and the clarity
of selling-point delivery; and (3) Length and Rhythm (30
pts), including line-level length consistency with reference
scripts and the fluency of phrasing and pausing. Scores from
these categories are summed to obtain the final SQ score.
Clip-Level Word Count Discrepancy (WCD). To evalu-
ate the temporal consistency between the generated script
and each video clip, we introduce the clip-level Word Count
Discrepancy:
WCD = |WordCountscript −WordCounttarget| .
A lower WCD indicates closer alignment between the tex-
tual content and the temporal structure of the corresponding
video clip, ensuring that the generated script matches the
expected speaking duration and maintains temporal consis-
tency at the clip level.
Music Similarity Score (MSS). To evaluate the quality
of background music prediction, we measure the semantic
similarity between the predicted BGM and the ground-truth
BGM. For each audio pair (apred, agt), we use the Music
Flamingo [9] model to first generate structured descriptions
of both audio clips (covering genre, tempo, instrumenta-
tion, structure, and emotional tone). The model then com-
pares the two descriptions and outputs a continuous similar-
ity score in the range [0, 1]:
MSS = FlamingoSim(Desc(apred), Desc(agt)) .
A higher score indicates that the predicted background mu-
sic is semantically closer to the ground-truth audio in terms
of musical attributes and emotional expression.
4.3. Experimental Details
The training parameter settings are provided in the sup-
plementary materials. For evaluation, we adopt a unified
evaluation protocol across all four tasks. All models are
prompted using the same instruction templates to ensure
consistent task definitions and comparable output formats.
All experiments are conducted on the same split of 364
videos to guarantee fairness across model types.
For text-only models such as Qwen3-8B and Qwen3-
32B, which cannot directly process visual inputs, each
video clip is converted into a short caption using Qwen2.5-
VL-32B. The caption describes the clip’s first frame and
serves as a lightweight textual proxy for the visual con-
tent, allowing text-only models to participate in all video-
related tasks without introducing additional modality gaps.
We additionally fine-tune a Qwen3-8B (Caption) baseline
on the same SFT dataset used by AutoCut. This baseline
uses the same task definitions and evaluation split, but op-
erates on captionized clip inputs rather than discrete video
tokens. Multimodal models retain their native frame-based
visual inputs. AutoCut further operates on discretized low-
fps video tokens and optionally incorporates textual or au-
dio tokens depending on the task, following its unified mul-
timodal representation scheme. We also introduce powerful
closed-source multimodal models such as GPT-4o as our
baseline to demonstrate the effectiveness of our approach.
For the background music retrieval task, we benchmark
only against MGSV [42] with GPT-4o, which is the sole


## Page 7


Table 1. Quantitative results across all tasks. The best results are boldfaced and the second best results are underlined.
Model
Video
Script
Audio
CSA
CRA
VSC
SQ
WCD ↓
MSS
Qwen3–8B[32] (Caption)
0.1374
0.01648
0.9308
79.9947
5.2648
–
Qwen3–8B (Caption + SFT)
0.5687
0.03022
1.1227
59.1592
6.8230
–
Qwen3–32B [32](Caption)
0.1731
0.01373
0.9342
80.7747
7.1023
–
Qwen2.5-VL–7B Instruct [4]
0.2418
0.01648
0.9649
79.4867
6.4709
–
Qwen2.5-VL–32B Instruct[4]
0.6648
0.02472
0.9980
78.3180
12.5071
–
InternVL-3.5-8B [38]
0.0247
0.01653
0.9466
81.0918
7.6415
–
LLaVA-v1.6-Mistral-7B-HF [23]
0.0027
0.00923
0.9914
56.1242
12.6580
–
GPT-4o [28] + MGSV [42]
0.2689
0.07756
1.1364
83.0290
7.7457
0.2656
Autocut (ours)
0.6593
0.10714
1.0360
84.6255
3.0182
0.3475
baseline equipped with a native audio encoder and mu-
sic–video matching capability.
Full prompt templates and example instructions are pro-
vided in the Supplementary Material.
4.4. Experimental Results
Table 1 summarizes the quantitative results on all four tasks.
The comparison includes both off-the-shelf text-only and
multimodal LLM baselines, as well as a Qwen3-8B (Cap-
tion) baseline trained on the same SFT tasks.
Across all tasks, AutoCut demonstrates strong and well-
rounded performance.
It obtains the best CRA score of
0.10714, indicating a clear advantage in recovering correct
clip order and modeling temporal structure. AutoCut also
achieves the best SQ score of 84.6255, the lowest WCD
of 3.0182, and the highest MSS of 0.3475, showing su-
perior script quality, temporal coherence, and background-
music matching. On clip-level understanding, it achieves
a CSA score of 0.6593, comparable to the best-performing
vision–language baselines, despite relying on lightweight
discretized video tokens.
Although GPT-4o and the fine-tuned Qwen3-8B (Cap-
tion) baseline both slightly outperform AutoCut on VSC,
AutoCut still achieves a strong score of 1.0360, indicating
good script–visual correspondence. More importantly, VSC
mainly reflects local semantic consistency rather than over-
all editing quality. AutoCut remains stronger on the more
practical task-level metrics, including CSA, CRA, SQ, and
WCD, while also being substantially more efficient than
caption-based pipelines.
In addition to strong editing performance, AutoCut is
also substantially more cost-efficient in deployment. Based
on our estimate, processing 100 videos costs about $2.5
with a GPT-4o API pipeline, compared with about $0.015
for AutoCut on a single RTX 4090, showing an order-of-
magnitude reduction in inference cost.
Taken together, these results show that AutoCut provides
the best overall balance across the key dimensions of ad-
0%
20%
40%
60%
80%
100%
Proportion
Visual
Smoothness
Logical
Consistency
Script-Visual
Alignment
BGM-Visual
Compatibility
Overall
Attractiveness
65%
18%
17%
68%
18%
14%
70%
26%
4%
52%
22%
26%
65%
20%
15%
User Study: 'AutoCut' vs 'GPT-4o'
Win
Tie
Loss
Figure 4.
User study results: win–loss ratios against GPT-4o
across five evaluation dimensions.
vertisement video editing. Its token-based multimodal rep-
resentation is particularly effective for structured editing
tasks, leading to stronger temporal reasoning, better script
planning, and higher practical usability.
4.5. Human Evaluation Results
Given the difficulty of fully assessing advertisement video
quality through automated metrics alone, we further con-
ducted a human evaluation to measure perceptual pref-
erence.
We performed a pairwise comparison study be-
tween videos created by AutoCut and those produced by
the strongest multimodal LLM baseline, GPT-4o. We re-
cruited 10 independent annotators and curated a set of 100
representative test samples. For each sample, the annotators
were shown two completed advertisement videos (A and B),
both promoting the same product and constructed from the
same pool of raw candidate clips.
After watching both videos, annotators were asked to in-
dicate their preference across five perceptual dimensions:


## Page 8


Table 2. Ablation on training settings.
Method
CSA
CRA
VSC
SQ
WCD ↓
sft only
0.4780
0.08242
1.0043
83.1898
4.4346
emb+full+sft
0.7170
0.05770
0.9669
78.9644
4.4984
emb+sft (ours)
0.6593
0.10714
1.0360
84.6255
3.0182
visual smoothness, logical consistency, script-visual align-
ment, BGM-visual compatibility, and overall advertisement
appeal.
For each dimension, participants could choose
Win, Loss, or Tie when the two versions were perceived as
equally good.
We summarize the preference trends in each dimension
by aggregating the proportion of times each method was fa-
vored. As shown in Figure 4, our method consistently out-
performs the strong GPT-4o baseline across all evaluation
dimensions, particularly in Script-Visual Alignment, high-
lighting the benefits of our multimodal joint modeling.
Due to space constraints, additional qualitative visual re-
sults can be found in the supplementary material.
4.6. Ablations
To validate the effectiveness of our two-stage training
pipeline, we conduct ablations across three settings (Ta-
ble 2): (1) sft only, (2) emb+full+sft, and (3) emb+sft (ours).
Our framework is designed as a lightweight two-stage pro-
cess: the first stage performs multimodal alignment, and the
second stage applies SFT to learn task-specific editing be-
havior.
Effect of Multimodal Alignment. Compared with sft only,
SFT introducing the alignment stage (emb+sft) yields con-
sistent improvements across CSA, CRA, VSC, and SQ,
while significantly reducing WCD. This confirms that ex-
plicitly aligning text, audio, and visual tokens provides a
stronger initialization for downstream editing tasks.
Effect of Additional Pre-training.
We further evaluate
an additional pre-training stage after multimodal alignment
(emb+full+sft). Despite slightly improving CSA, this set-
ting degrades CRA and SQ and increases WCD. We at-
tribute this behavior to the limited quality and weak label
consistency of the available pre-training corpus, which in-
troduces noise into the learned token distributions and in-
terferes with the alignment stage. Therefore, we adopt the
two-stage emb+sft pipeline as our default training strategy,
as it provides the best overall balance of accuracy, consis-
tency, and editing stability.
5. Discussion
Limitations. Although AutoCut demonstrates strong per-
formance across multimodal understanding and generation
tasks, several limitations remain.
(1) While unified to-
kenization substantially improves cross-modal alignment,
subtle desynchronization between video motion and audio
rhythm still occurs, indicating that multimodal coupling is
not yet fully unified. (2) Controllability remains primar-
ily at the clip level; the current framework does not yet
support fine-grained, emotion-aware, or frame-level edit-
ing, which limits narrative flexibility. (3) AutoCut adopts
a material-based editing paradigm, in which the rendering
stage retrieves and composes existing video and audio as-
sets from a material database. This design improves re-
alism and production readiness, but it does not synthesize
new video pixels or raw audio from scratch, and therefore
remains bounded by the coverage and quality of the avail-
able materials.
Future Directions. Future work will address these lim-
itations from multiple perspectives.
(1) Improve tempo-
ral alignment and multimodal coherence through cross-
attentive modeling and diffusion-based refinement, achiev-
ing tighter video–audio–text synchronization. Future work
can also explore stronger visual front-ends, such as ViT,
CLIP, or video-based encoders, to further improve repre-
sentation quality. (2) Enhance controllability via expanded
instruction sets and latent-space editing, enabling the model
to manipulate rhythm, tone, and emotion at a finer level. (3)
Integrate learned clip synthesis and adaptive retrieval into
a single decoding process, unifying generation and render-
ing and moving AutoCut toward fully generative, human-
aligned, and scalable video creation.
6. Conclusion
This paper presents AutoCut, an end-to-end framework
for advertisement video editing based on multimodal dis-
cretization and controllable editing. By transforming video,
audio, and textual inputs into a shared discrete token space
and aligning them through large-scale multimodal pretrain-
ing and fine-tuning, AutoCut bridges perception and cre-
ation within a unified reasoning framework.
Extensive
experiments on real-world advertisement datasets demon-
strate that AutoCut achieves superior semantic coherence,
controllability, and production efficiency compared with
retrieval- or template-based baselines. The study establishes
multimodal tokenization as a foundation for connecting dis-
crete reasoning and generative synthesis in video editing,
paving the way toward fully generative, human-aligned, and
scalable AI-driven media production.


## Page 9


References
[1] G. Ahanger and T.D.C. Little. Automatic composition tech-
niques for video production. IEEE Transactions on Knowl-
edge and Data Engineering, 10(6):967–987, 1998. 2
[2] Ido Arev, Hyun Soo Park, Yaser Sheikh, Jessica Hodgins,
and Ariel Shamir. Automatic editing of footage from multi-
ple social cameras. ACM Trans. Graph., 33(4):81:1–81:11,
2014. 2
[3] Dawit Mureja Argaw, Fabian Caba Heilbron, Joon-Young
Lee, Markus Woodson, and In So Kweon. The Anatomy
of Video Editing: A Dataset and Benchmark Suite for AI-
Assisted Video Editing. In Computer Vision – ECCV 2022,
pages 201–218, Cham, 2022. 2
[4] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin
Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun
Tang, Humen Zhong, Yuanzhi Zhu, Mingkun Yang, Zhao-
hai Li, Jianqiang Wan, Pengfei Wang, Wei Ding, Zheren
Fu, Yiheng Xu, Jiabo Ye, Xi Zhang, Tianbao Xie, Zesen
Cheng, Hang Zhang, Zhibo Yang, Haiyang Xu, and Jun-
yang Lin.
Qwen2.5-vl technical report.
arXiv preprint
arXiv:2502.13923, 2025. 7
[5] Max Bain, Arsha Nagrani, Andrew Brown, and Andrew Zis-
serman.
Condensed Movies: Story Based Retrieval with
Contextual Embeddings. In Computer Vision – ACCV 2020:
15th Asian Conference on Computer Vision, Kyoto, Japan,
November 30 – December 4, 2020, Revised Selected Papers,
Part V, pages 460–479, Berlin, Heidelberg, 2020. 2
[6] Dabing Cheng, Haosen Zhan, Xingchen Zhao, Guisheng
Liu, Zemin Li, Jinghui Xie, Zhao Song, Weiguo Feng,
and Bingyue Peng.
Text-to-edit: Controllable end-to-end
video ad creation via multimodal llms.
arXiv preprint
arXiv:2501.05884, 2025. 2, 3
[7] Zihan Ding, Xinyi Wang, Junlong Chen, Per Ola Kristens-
son, and Junxiao Shen. Prompt-driven agentic video editing
system: Autonomous comprehension of long-form, story-
driven media. arXiv preprint arXiv:2509.16811, 2025. 3
[8] Christoph Feichtenhofer, Haoqi Fan, Jitendra Malik, and
Kaiming He. SlowFast Networks for Video Recognition. In
2019 IEEE/CVF International Conference on Computer Vi-
sion (ICCV), pages 6201–6210, Seoul, Korea (South), 2019.
3
[9] Sreyan Ghosh, Arushi Goel, Lasha Koroshinadze, Sang-
gil Lee, Zhifeng Kong, Joao Felipe Santos, Ramani Du-
raiswami, Dinesh Manocha, Wei Ping, Mohammad Shoeybi,
and Bryan Catanzaro.
Music flamingo:
Scaling music
understanding in audio language models.
arXiv preprint
arXiv:2511.10289, 2025. 6
[10] Daya Guo and Zhaoyang Zeng. Multi-modal Representation
Learning for Video Advertisement Content Structuring. In
Proceedings of the 29th ACM International Conference on
Multimedia, pages 4770–4774, 2021. 2
[11] Mingfei Han, Linjie Yang, Xiaojun Chang, Lina Yao, and
Heng Wang.
Shot2Story: A New Benchmark for Com-
prehensive Understanding of Multi-shot Videos.
Interna-
tional Conference on Representation Learning, 2025:41665–
41677, 2025. 3
[12] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun.
Deep Residual Learning for Image Recognition.
In 2016
IEEE Conference on Computer Vision and Pattern Recog-
nition (CVPR), pages 770–778, 2016. 4
[13] De-An Huang, Shijia Liao, Subhashree Radhakrishnan,
Hongxu Yin, Pavlo Molchanov, Zhiding Yu, and Jan Kautz.
Lita: Language instructed temporal-localization assistant.
arXiv preprint arXiv:2403.19046, 2024. 3
[14] Bernd Huber, Hijung Valentina Shin, Bryan Russell, Oliver
Wang, and Gautham J. Mysore. B-Script: Transcript-based
B-roll Video Editing with Recommendations. In Proceed-
ings of the 2019 CHI Conference on Human Factors in Com-
puting Systems, pages 1–11, 2019. 2
[15] Qiuqiang Kong, Yin Cao, Turab Iqbal, Yuxuan Wang,
Wenwu Wang, and Mark D. Plumbley. PANNs: Large-Scale
Pretrained Audio Neural Networks for Audio Pattern Recog-
nition. IEEE/ACM Transactions on Audio, Speech, and Lan-
guage Processing, 28:2880–2894, 2020. 4, 5
[16] Mackenzie Leake and Wilmot Li.
ChunkyEdit: Text-first
video interview editing via chunking. In Proceedings of the
2024 CHI Conference on Human Factors in Computing Sys-
tems, pages 1–16, New York, NY, USA, 2024. 2
[17] Mackenzie Leake, Abe Davis, Anh Truong, and Maneesh
Agrawala. Computational video editing for dialogue-driven
scenes. ACM Trans. Graph., 36(4):130:1–130:14, 2017. 3
[18] Doyup Lee, Chiheon Kim, Saehoon Kim, Minsu Cho, and
Wook-Shin Han.
Autoregressive image generation using
residual quantization. In Proceedings of the IEEE/CVF Con-
ference on Computer Vision and Pattern Recognition, pages
11523–11532, 2022. 4
[19] Bozheng Li, Yongliang Wu, Yi Lu, Jiashuo Yu, Licheng
Tang, Jiawang Cao, Wenqing Zhu, Yuyang Sun, Jay Wu, and
Wenbo Zhu. VEU-Bench: Towards Comprehensive Under-
standing of Video Editing. In Proceedings of the IEEE/CVF
Conference on Computer Vision and Pattern Recognition,
pages 13671–13680, 2025. 2
[20] Yuzhi Li, Haojun Xu, and Feng Tian.
Shot sequence
ordering for video editing:
Benchmarks, metrics, and
cinematology-inspired computing methods. arXiv preprint
arXiv:2503.17975, 2025. 2
[21] Yuzhi Li, Haojun Xu, and Feng Tian. From Shots to Stories:
LLM-Assisted Video Editing with Unified Language Repre-
sentations. arXiv preprint arXiv:2505.12237, 2025. 3
[22] Qin Lin, Nuo Pang, and Zhiying Hong. Automated Multi-
Modal Video Editing for Ads Video. In Proceedings of the
29th ACM International Conference on Multimedia, pages
4823–4827, Virtual Event China, 2021. 2
[23] Haotian Liu, Chunyuan Li, Yuheng Li, Bo Li, Yuanhan
Zhang, Sheng Shen, and Yong Jae Lee.
Llava-next: Im-
proved reasoning, ocr, and world knowledge, 2024. 7
[24] Yujia Lu, Shi Chen, Shihui Shuai, Yuxi Wang, Changyuan
Yang, and Lingyun Sun. Computational Product Presenta-
tion Video Editing Framework Based on Editing Attribute
Constraints. Journal of Computer-Aided Design & Computer
Graphics, 32(7):1101–1110, 2020. 2
[25] Michele Merler, Khoi-Nguyen C. Mac, Dhiraj Joshi, Quoc-
Bao Nguyen, Stephen Hammer, John Kent, Jinjun Xiong,


## Page 10


Minh N. Do, John R. Smith, and Rogerio Schmidt Feris. Au-
tomatic Curation of Sports Highlights Using Multimodal Ex-
citement Features. IEEE Transactions on Multimedia, 21(5):
1147–1160, 2019. 2
[26] Safa Messaoud, Ismini Lourentzou, Assma Boughoula,
Mona Zehni, Zhizhen Zhao, Chengxiang Zhai, and Alexan-
der G. Schwing.
DeepQAMVS: Query-Aware Hierarchi-
cal Pointer Networks for Multi-Video Summarization.
In
Proceedings of the 44th International ACM SIGIR Confer-
ence on Research and Development in Information Retrieval,
pages 1389–1399, New York, NY, USA, 2021. 2
[27] Chong Mou, Qichao Sun, Yanze Wu, Pengze Zhang,
Xinghui Li, Fulong Ye, Songtao Zhao, and Qian He.
In-
structX: Towards Unified Visual Editing with MLLM Guid-
ance. arXiv preprint arXiv:2510.08485, 2025. 3
[28] OpenAI.
Gpt-4o
system
card.
arXiv
preprint
arXiv:2410.21276, 2024. 7
[29] Dongjun Qian, Kai Su, Yiming Tan, Qishuai Diao, Xian Wu,
Chang Liu, Bingyue Peng, and Zehuan Yuan. Vc-llm: Auto-
mated advertisement video creation from raw footage using
multi-modal llms. arXiv preprint arXiv:2504.05673, 2025.
2, 3
[30] Mrigank Rochan, Mahesh Kumar Krishna Reddy, Linwei
Ye, and Yang Wang. Adaptive Video Highlight Detection
by Learning from User History. In Computer Vision – ECCV
2020, pages 261–278, Cham, 2020. 2
[31] Yunlong Tang, Siting Xu, Teng Wang, Qin Lin, Qinglin Lu,
and Feng Zheng. Multi-modal Segment Assemblage Net-
work for Ad Video Editing with Importance-Coherence Re-
ward. In Computer Vision – ACCV 2022, pages 560–576,
Cham, 2023. 2
[32] Qwen Team. Qwen3 technical report, 2025. 7
[33] Bekzat Tilekbay, Saelyne Yang, Michal Adam Lewkowicz,
Alex Suryapranata, and Juho Kim. ExpressEdit: Video Edit-
ing with Natural Language and Sketching. In Companion
Proceedings of the 29th International Conference on Intel-
ligent User Interfaces, pages 50–53, New York, NY, USA,
2024. 2
[34] Anh Truong, Floraine Berthouzoz, Wilmot Li, and Maneesh
Agrawala. QuickCut: An Interactive Tool for Editing Nar-
rated Video. In Proceedings of the 29th Annual Symposium
on User Interface Software and Technology, pages 497–507,
New York, NY, USA, 2016. 2
[35] Bryan Wang, Yuliang Li, Zhaoyang Lv, Haijun Xia, Yan
Xu, and Raj Sodhi.
Lave: Llm-powered agent assistance
and language augmentation for video editing. arXiv preprint
arXiv:2402.10294, 2024. 3
[36] Miao Wang, Guo-Wei Yang, Shi-Min Hu, Shing-Tung Yau,
and Ariel Shamir. Write-a-video: Computational video mon-
tage from themed text. ACM Trans. Graph., 38(6):177:1–
177:13, 2019. 2
[37] Sitong Wang, Samia Menon, Tao Long, Keren Henderson,
Dingzeyu Li, Kevin Crowston, Mark Hansen, Jeffrey V
Nickerson, and Lydia B Chilton. ReelFramer: Human-AI
Co-Creation for News-to-Video Translation. In Proceedings
of the 2024 CHI Conference on Human Factors in Comput-
ing Systems, pages 1–20, New York, NY, USA, 2024. 2
[38] Weiyun Wang, Zhangwei Gao, Lixin Gu, Hengjun Pu, Long
Cui, Xingguang Wei, Zhaoyang Liu, Linglin Jing, Sheng-
long Ye, Jie Shao, et al. Internvl3.5: Advancing open-source
multimodal models in versatility, reasoning, and efficiency.
arXiv preprint arXiv:2508.18265, 2025. 7
[39] Zheng Wang, Jianguo Li, and Yu-Gang Jiang. Story-driven
Video Editing. IEEE Transactions on Multimedia, 23:4027–
4036, 2021. 2
[40] Cong Wei, Quande Liu, Zixuan Ye, Qiulin Wang, Xintao
Wang, Pengfei Wan, Kun Gai, and Wenhu Chen. UniVideo:
Unified Understanding, Generation, and Editing for Videos.
arXiv preprint arXiv:2510.08377, 2025. 3
[41] Yanheng Wei, Lianghua Huang, Yanhao Zhang, Yun Zheng,
and Pan Pan.
An Intelligent Advertisement Short Video
Production System via Multi-Modal Retrieval. In Proceed-
ings of the 45th International ACM SIGIR Conference on
Research and Development in Information Retrieval, pages
3368–3372, Madrid Spain, 2022. 1, 2
[42] Zijie Xin, Minquan Wang, Jingyu Liu, Quan Chen, Ye Ma,
Peng Jiang, and Xirong Li. Music grounding by short video.
In Proceedings of the IEEE/CVF International Conference
on Computer Vision, 2025. 6, 7
[43] Bo Xiong, Yannis Kalantidis, Deepti Ghadiyaram, and Kris-
ten Grauman. Less Is More: Learning Highlight Detection
From Video Duration. In Proceedings of the IEEE/CVF Con-
ference on Computer Vision and Pattern Recognition, pages
1258–1267, 2019. 2
[44] Yu Xiong, Fabian Caba Heilbron, and Dahua Lin. Transcript
to Video: Efficient Clip Sequencing from Texts. In Proceed-
ings of the 30th ACM International Conference on Multime-
dia, pages 5407–5416, New York, NY, USA, 2022. 2
[45] An Yang, Anfeng Li, Baosong Yang, Beichen Zhang,
Binyuan Hui, Bo Zheng, Bowen Yu, Chang Gao, Chen-
gen Huang, Chenxu Lv, Chujie Zheng, Dayiheng Liu, Fan
Zhou, Fei Huang, Feng Hu, Hao Ge, Haoran Wei, Huan
Lin, Jialong Tang, Jian Yang, Jianhong Tu, Jianwei Zhang,
Jianxin Yang, Jiaxi Yang, Jing Zhou, Jingren Zhou, Junyang
Lin, Kai Dang, Keqin Bao, Kexin Yang, Le Yu, Lianghao
Deng, Mei Li, Mingfeng Xue, Mingze Li, Pei Zhang, Peng
Wang, Qin Zhu, Rui Men, Ruize Gao, Shixuan Liu, Shuang
Luo, Tianhao Li, Tianyi Tang, Wenbiao Yin, Xingzhang
Ren, Xinyu Wang, Xinyu Zhang, Xuancheng Ren, Yang Fan,
Yang Su, Yichang Zhang, Yinger Zhang, Yu Wan, Yuqiong
Liu, Zekun Wang, Zeyu Cui, Zhenru Zhang, Zhipeng Zhou,
and Zihan Qiu.
Qwen3 technical report.
arXiv preprint
arXiv:2505.09388, 2025. 4
[46] Dingyi Yang, Chunru Zhan, Ziheng Wang, Biao Wang,
Tiezheng Ge, Bo Zheng, and Qin Jin. Synchronized Video
Storytelling: Generating Video Narrations with Structured
Storyline. In Proceedings of the 62nd Annual Meeting of the
Association for Computational Linguistics (Volume 1: Long
Papers), pages 9479–9493, Bangkok, Thailand, 2024. 3
[47] Huan Yang, Baoyuan Wang, Stephen Lin, David Wipf,
Minyi Guo, and Baining Guo. Unsupervised Extraction of
Video Highlights via Robust Recurrent Auto-Encoders. In
2015 IEEE International Conference on Computer Vision
(ICCV), pages 4633–4641, 2015. 2


## Page 11


[48] Zixuan Ye, Xuanhua He, Quande Liu, Qiulin Wang, Xin-
tao Wang, Pengfei Wan, Di Zhang, Kun Gai, Qifeng Chen,
and Wenhan Luo. UNIC: Unified In-Context Video Editing.
arXiv preprint arXiv:2506.04216, 2025. 3
[49] Shoubin Yu, Difan Liu, Ziqiao Ma, Yicong Hong, Yang
Zhou, Hao Tan, Joyce Chai, and Mohit Bansal. VEGGIE:
Instructional Editing and Reasoning Video Concepts with
Grounded Generation. In Proceedings of the IEEE/CVF In-
ternational Conference on Computer Vision, pages 15147–
15158, 2025. 3
[50] Yanhao Zhang, Qiang Wang, Yun Zheng, Pan Pan, and
Yinghui Xu. VideoDiscovery: An Automatic Short-Video
Generation System for E-commerce Live-streaming. In Pro-
ceedings of the 29th ACM International Conference on Mul-
timedia, pages 2771–2773, New York, NY, USA, 2021. 1,
2
[51] Yuqi Zhang, Bin Guo, Nuo Li, Ying Zhang, Shijie Wang,
Zhiwen Yu, and Qing Li.
Tree-of-AdEditor:
Heuristic
Tree Reasoning for Automated Video Advertisement Edit-
ing with Large Language Model.
In Thirty-Fourth Inter-
national Joint Conference on Artificial Intelligence, pages
8705–8713, 2025. 3
[52] Bin Zhao, Maoguo Gong, and Xuelong Li. Hierarchical mul-
timodal transformer to summarize videos. Neurocomputing,
468:360–369, 2022. 2


## Page 12


AutoCut: End-to-end advertisement video editing based on multimodal
discretization and controllable generation
Supplementary Material
7. Appendix
This appendix is organized as follows:
• 7.1 Model Architecture and Hyperparameters
model components and key training settings.
• 7.2 Post-Processing and Rendering Pipeline
steps for converting predictions into final ad videos.
• 7.3 GPT-4o Evaluation Prompts
prompts used for GPT-4o-based automatic evaluation.
• 7.4 Human Evaluation Criteria
criteria and guidelines for the pairwise user study.
• 7.5 Dataset Construction Details
details of alignment data, SFT filtering, and task format-
ting.
7.1. Model Architecture and Hyperparameters
Table 3. Hyperparameters for the video and audio RQ-VAE quan-
tizers.
RQ-VAE Configs
Video
Audio
Input feature size
128
2048
Quantization heads
8
8
Codebook size
256
256
Codebook dim
128
256
Shared codebook
False
False
Encoder MLP size
[512, 512] [1024, 512]
Decoder MLP size
[512, 512] [512, 1024]
Loss type
cosine
cosine
Reconstruction weight
1.0
1.0
Commitment weight
0.0
0.0
Optimizer weight decay
1e−4
1e−4
Initial learning rate
1e−3
1e−3
Min learning rate
2e−5
2e−5
Batch size
8192
8192
Max epochs
20
50
To convert continuous visual and audio embeddings into
discrete tokens, we train two modality-specific Residual
Quantized Variational Autoencoders (RQ-VAEs).
Both
models use multi-head residual quantization, cosine recon-
struction loss, and large-batch optimization, while differing
in encoder–decoder capacity to match modality characteris-
tics.
For video, 128-dimensional frame embeddings are quan-
tized using an 8-head residual quantizer with a 256-
entry codebook and lightweight two-layer MLP encoder–
Table 4. Hyperparameters used during the multimodal alignment
and SFT stages.
Config
Alignment Stage
SFT Stage
Base model
Qwen3-8B
Aligned model
Template
qwen3
qwen3
Cutoff length
8096
4000
Packing
Enabled
Disabled
Per-device batch size
2
1
Grad. accumulation
1
1
Learning rate
5e–5
1e–5
Epochs
5
3
LR scheduler
Cosine
Cosine
Warmup ratio
0.1
0.1
Precision
bf16
bf16
Optimizer
AdamW
AdamW
Flash attention
fa3
fa3
Resize vocab
Enabled
Disabled
decoder. This configuration balances reconstruction fidelity
and token compactness for downstream selection and order-
ing tasks.
For audio, the 2048-dimensional PANNs embeddings
require a wider asymmetric MLP architecture, while retain-
ing the same quantizer heads and codebook size. Training
follows the same objective and optimizer settings but uses a
longer schedule to accommodate higher input dimensional-
ity.
Both quantizers are trained on large-scale advertisement
datasets and monitored with Weights & Biases for stability.
A consolidated comparison of all model hyperparameters is
provided in Table 3.
We adopt a two-stage training pipeline to integrate mul-
timodal discrete tokens into the Qwen3-8B backbone and
enable controllable editing. The first stage performs mul-
timodal alignment, where the backbone is frozen except
for the newly added multimodal embedding layers. This
stage learns semantic correspondence across video, audio,
and text tokens using a cosine learning-rate schedule, a long
context window (cutoff 8096), and bf16 mixed precision.
Training uses a per-device batch size of 2, no gradient accu-
mulation, and runs for five epochs at a learning rate of 5e–5,
with packing and DeepSpeed ZeRO-2 to improve memory
and throughput.
The second stage applies supervised fine-tuning (SFT)
on the aligned model. Unlike alignment, SFT updates all


## Page 13


Product Information
Product Type: Wireless
Earbuds
Brand: Edifier EVO PRO
Features: [U-shaped in-
ear
fit,
Leather-texture
body,
instant
pairing,
Customizable
EQ,
Multiple
noise
modes,
Multiple ear tip sizes]
Edifier EVO PRO,
wireless earbuds,
Designed with a U-
shaped in-ear fit,
these earbuds connect instantly,
offer customizable EQ,
multiple noise modes,
and plenty of ear tips 
for the perfect fit,
a pair truly 
made for you!
[Clip 1]: 1s ~ 2s
[Clip 2]: 2s ~ 3s
[Clip 3] 3s ~ 5s
[Clip 5]: 7s ~ 8s
[Clip 6]: 8s ~ 9s
[Clip 7]: 9s ~ 10s
[Clip 8]: 10s ~ 11s
[Clip 9]: 11s ~ 13s
and a leather-textured case,
[Clip 4]: 5s ~ 7s
Case 1
Product Information
Product Type: Children’s
face cream
Brand: BODOREME
Features:
[Pump-style
dispenser,
Moisturizing
but
non-
sticky,
Blue
chamomile
with natural plant lipids]
Moms, you really need to 
listen to me this time,
you have to get your child’s 
face cream ready in advance.
your child’s skin 
condition, 
both convenient 
and hygienic.
This BODOREME
children’s face cream,
Its cloud-soft texture 
spreads easily,
It contains blue 
chamomile,
combined with 
natural plant lipids,
It’s a must for kids in 
autumn and winter,
[Clip 1]: 0s ~ 1s
[Clip 2]: 1s ~ 3s
[Clip 3] 3s ~ 4s
[Clip 5]: 5s ~ 7s
[Clip 7]: 9s ~ 10s
[Clip 10]: 14s~15s
[Clip 13]: 17s ~ 19s
[Clip 15: 21s ~ 23s
[Clip 17]: 25s ~ 26s
[Clip 4] 4s ~ 5s
[Clip 6]: 7s ~ 9s
[Clip 8]: 10s~12s [Clip 9]: 12s~14s
[Clip 11]: 15s~16s
[Clip 12]: 16s~17s
[Clip 14]: 19s~21s
[Clip 16: 23s ~ 25s
has already changed 
without you even noticing.
has a pump-
style design,
you just pump as 
much as you need,
moisturizes but 
not sticky,
Containing gentle 
and safe ingredients
whether your child 
is at school,
outdoors, or in dry air-conditioned 
rooms, this cream works perfectly.
so it’s even better 
to have two bottles.
Case 2
Figure 5. Qualitative case studies of our automatic ad video editing pipeline. For each case (top: wireless earbuds, bottom: children’s
face cream), we show the provided product information, selected video clips, and the aligned script sentences. Each frame strip visualizes
the model’s clip selection and ordering, together with the corresponding sentence and clip-level timestamps, illustrating how the system
produces a coherent, time-aligned ad from raw footage and product metadata.


## Page 14


parameters and disables packing to preserve task struc-
ture. It is trained on curated datasets covering video selec-
tion, clip ordering, script generation, and BGM selection,
using a shorter sequence length (cutoff 4000), a smaller
learning rate (1e–5), and a per-device batch size of 1 for
three epochs. The same optimizer, scheduler, and mixed-
precision settings are used as in the alignment stage.
All training experiments for both stages are conducted
on a cluster of 8 NVIDIA GPUs. All templates used dur-
ing SFT follow the qwen3 instruction format, and model
checkpoints are logged using Weights & Biases. Table 4
summarizes the hyperparameters used in the alignment and
SFT stages.
7.2. Post-Processing and Rendering Pipeline
In the main paper we have shown that our model achieves
strong performance on all sub-tasks and outperforms com-
parable baselines, both in quantitative metrics and in our
user study. Here, we detail the complete post-processing
and rendering pipeline that converts model outputs into a fi-
nal edited video. For clarity, AutoCut does not perform clip
or BGM selection by directly predicting fixed database in-
dices. Instead, the model outputs discrete token sequences
that are decoded into target embeddings, and the final video
or audio assets are retrieved from the material database
through similarity search. This retrieval-based design al-
lows the system to generalize to unseen clips and music
tracks, rather than memorizing a closed set of asset IDs.
Editing scenarios and model outputs.
We consider two
typical usage scenarios.
(1) Script–driven editing. The user provides (i) prod-
uct information, (ii) a pool of candidate product clips, and
(iii) a target ad script. Selection. Given the script and clip
pool, the model first performs a select task: it chooses clips
that are relevant to the script. We constrain the number
of selected clips to match the number of sentences in the
script. Sorting. The model then performs a sort task on
the selected clips, ordering them such that visual content
aligns with the sentence-level script order, based on learned
vision–language correlations. BGM selection. Finally, we
feed the ordered clip sequence together with the script and
product information into the model for background-music
(BGM) selection. The model outputs a sequence of discrete
audio tokens corresponding to a suitable BGM track for this
rough cut.
(2) Footage–driven editing. In the second scenario, the
user has already curated all relevant footage but has not yet
written an ad script; effectively, the select step has been per-
formed manually. Given the product information and the
set of clips, the model first generates an ad script whose
number of sentences matches the number of clips.
We
then apply the same sort and BGM selection steps as in the
script–driven pipeline.
In both scenarios, the model outputs discrete video to-
kens (for clips), audio tokens (for BGM), and the text script.
Token decoding and retrieval.
To map token sequences
back to concrete media assets, we use the RQVAE models
trained in the pre-processing stage. We first decode the dis-
crete tokens into continuous embeddings, and then perform
nearest-neighbor search in FAISS indices.
For
video
tokens,
FAISS
returns
a
pair
(frame id, clip id) for each token.
These identi-
fiers are structured:
• frame id is constructed from a base photo id (the
underlying source video) plus four digits encoding the
frame index within that video.
• clip id is constructed from the same photo id fol-
lowed by seven digits, where the first four digits denote
the starting frame of the clip and the last three digits en-
code its duration (at 1 fps).
For audio tokens, FAISS returns an audio id pointing to
a BGM track in our library.
Rendering strategies: by frame vs. by clip.
Using these
identifiers, we support two strategies for assembling the fi-
nal video.
By frame. We derive the starting frame from the last
four digits of frame id and use the stored clip length (in
frames at 1 fps) to cut a contiguous segment from the orig-
inal video. This provides frame-accurate control over clip
boundaries.
By clip.
We additionally maintain an alternative clip
segmentation defined independently of script boundaries.
Each source video is segmented into visually coherent clips
based on changes in visual continuity: we detect bound-
aries where the similarity between consecutive frame em-
beddings drops sharply. For each such segment (computed
at 20 fps), we average the frame embeddings to obtain a
single clip embedding. At inference time, retrieval is per-
formed over these “visual clips”, and we stitch together the
corresponding segments. This by-clip strategy is specifi-
cally designed to reduce visual jitter or abrupt cuts that may
occur if we follow sentence boundaries alone without con-
sidering the intrinsic visual structure of the footage.
Subtitles, TTS, and BGM mixing.
For each clip in the
final sequence, we associate one sentence of the provided
or generated script. We render the sentence as on-screen
subtitles and synthesize a voice-over track using text-to-
speech (TTS). In the current implementation we use a fixed
“avatar” voice; extending the model to select an appropri-
ate voice profile conditioned on the video content is left for
future work. Finally, we retrieve the BGM track using the


## Page 15


predicted audio id and mix it with the TTS audio when
compositing the final video.
For all user-study videos and the demo results reported
in the paper, we adopt the script–driven editing pipeline
(given script) together with the by-clip rendering strategy.
7.3. GPT-4o Evaluation Prompts
We provide additional details on the automated evaluation
procedures used to measure semantic alignment and script
quality. Full prompts are included as separate text files; here
we summarize their intended behavior.
VSC Scoring Prompt
The Visual–Script Correlation
(VSC) evaluator compares a single video frame with its cor-
responding script line. It is instructed to judge semantic
consistency and output a discrete score in {0, 1, 2}, indicat-
ing mismatch, partial relevance, or strong alignment. The
evaluator receives only the frame and the script line and is
constrained to return a numerical score. The full prompt is
provided in vsc prompt.txt.
SQ Scoring Prompt
The Script Quality (SQ) evaluator
applies a 100-point rubric covering correctness, clarity, lin-
guistic naturalness, selling-point communication, and tim-
ing/length alignment. It is given product metadata, a human
reference script, the generated script, and a pre-computed
line-level length-difference statistic.
The evaluator out-
puts a structured JSON object with category-level scores
and a brief justification.
The full prompt is included in
sq prompt.txt.
To ensure consistent behavior across evaluation runs,
both prompts explicitly define scoring boundaries, output
formats, and constraints that prevent the evaluator from in-
troducing additional commentary or unsupported interpre-
tations.
7.4. Human Evaluation Criteria
To assess perceptual advertisement quality beyond auto-
mated metrics, we conducted a controlled user study with
ten professional advertising specialists.
Each participant
evaluated ten video pairs, resulting in a total of 100 com-
parisons between videos generated by AutoCut and by the
GPT-4o + MGSV baseline. For fairness, the ordering of the
two videos in each pair was fully randomized, ensuring that
annotators could not infer the model identity. Instead of col-
lecting numerical scores, we adopt a pairwise comparison
protocol in which annotators simply choose the better video
for each criterion. This approach reduces calibration bias,
avoids inconsistent use of rating scales, and yields more sta-
ble and discriminative perceptual judgments.
Annotators compared each video pair across five dimen-
sions: visual smoothness, logical consistency, script–visual
Figure 6. Additional human study comparing AutoCut with Gem-
ini 3 on 50 advertisement videos. A large proportion of cases are
judged as Tie across all five dimensions, indicating that AutoCut
achieves performance highly comparable to this stronger and more
recent baseline.
alignment, BGM–visual compatibility, and overall adver-
tisement attractiveness. Table 5 summarizes the guidelines
used by annotators to judge the winner in each dimension.
7.5. Additional Human Study with Gemini 3
Since multimodal foundation models continue to improve
rapidly, we further compare AutoCut with a stronger and
more recent closed-source baseline, Gemini 3, which was
released after our original submission. We conduct an ad-
ditional pairwise human evaluation on 50 advertisement
videos using the same protocol as the main user study.
For each sample, annotators compare the completed ad-
vertisement videos generated by AutoCut and Gemini 3
across four dimensions: visual smoothness, logical consis-
tency, script–visual alignment, and overall advertisement
attractiveness. As in the main study, annotators choose Win,
Loss, or Tie for each dimension.
Figure 6 summarizes the results. We observe that Auto-
Cut achieves highly comparable performance to Gemini 3,
with a majority of cases resulting in Tie across all evalua-
tion dimensions. This result suggests that AutoCut remains
competitive even against a much stronger and more recent
multimodal baseline. Importantly, AutoCut achieves this
performance with a substantially smaller parameter scale
and lower computational cost, highlighting its practical ef-
ficiency for advertisement video editing.
7.6. Dataset Construction Details
7.6.1. Multimodal Alignment Dataset Construction
We start from short-form advertisements with high user en-
gagement, defined as videos whose click-through rate and
like-rate both lie in the top 10% on the platform. For each
video we collect product metadata (category, brand, selling
points) and process the three modalities in parallel (Fig. 7).
On the video side, we sample frames at 1 fps with
ffmpeg and encode them using an internal CNNv2 to ob-
tain dense visual embeddings. On the audio side, we extract
the audio track, separate background music from speech,
and embed the BGM with a PANNs-based service into
2048-D acoustic features. On the text side, ASR is applied
to the speech channel to obtain time-stamped transcripts; a
lightweight Qwen3-0.6B filter removes videos whose tran-


## Page 16


A hydrating makeup primer perfect for all seasons, 
The silky texture makes it easy to apply. 
Split into clips
by punctuation-based timestamps
Script 1
Script 2
v1 v2 v3 v4 v5 v6 v7 v8
…
…
v1 v2 v3 v4 v5 v6 v7 v8
…
…
a1
a2
a3
a4
a5
a6
a7
a8
Multimodal Alignment Data Construction
Data Filtering
1 < Clip Number < 60
1s < Clip Duration < 60s
1s < Video Duration < 60s
Product Information
Text 1
Clip 1 F
Text n
Clip n F
…
Qwen2.5VL-32B
Visual Script Relevance Score
4/5
2/5
3/5
5/5
…
5/5
Accept videos with >80% 
script-relevant clips
Task-Oriented SFT Dataset Construction
Video Selection
Video Sorting
Product Information
Full Script
Clip- 2 [0]
Clip+ 3 [1]
Clip- 3 [2]
Clip+ 1 [3]
Clip+ 4 [5]
Clip- 1 [6]
Clip+ 5 [7]
Clip- 5 [8]
Clip+ 2 [4]
Clip- 4 [9]
“You are a professional 
video editor…”
[1]
[3]
[5]
[7]
[4]
“Select clips relevant to 
the product and script”
Product Information
Full Script
Clip+ 3 [1]
Clip+ 1 [3]
Clip+ 4 [5]
Clip+ 5 [7]
Clip+ 2 [4]
“You are a professional 
video editor…”
[3]
[4]
[5]
[7]
[1]
“Sort clips by 
script order”
Script Generation
Clip3
Clip1
Clip4 Clip5
Clip2
“You are a script writer…”
“Generate a script based 
on the video content”
Product Information
Full Script
BGM Selection
Clip3
Clip1
Clip4 Clip5
Clip2
“Select a matching BGM”
Product Information
Full Script
Full BGM
Figure 7. Overview of our dataset construction pipeline. Top: multimodal alignment data construction. Raw ad videos are paired with
sentence-level scripts and product information, then segmented into short clips using punctuation-aligned timestamps, producing aligned
video tokens and audio tokens. Bottom-left: data filtering. We keep videos whose clip number and duration fall within preset ranges and
whose visual–script relevance score (estimated by Qwen2.5-VL-32B) exceeds an 80% threshold. Bottom-right: task-oriented SFT dataset
construction. From the filtered aligned data we instantiate four supervision signals: video selection, video sorting, script generation, and
BGM selection, each conditioned on product information and/or the full script.
scripts mainly contain song lyrics or lack coherent product
descriptions.
Visual and acoustic features are then discretized by the
RQ-VAE tokenizers (Sec. 3.3) to produce sequences of
video and audio code indices.
We define clips by ASR
punctuation boundaries and soft-align visual tokens whose
timestamps fall inside each sentence span. For every ad,
clip-level text and video tokens are concatenated into a
single sequence, and the audio-token summary of the full
BGM track is appended. This yields our multimodal align-
ment corpus for the first training stage, containing roughly
700K advertisements.
7.6.2. SFT Data Filtering Pipeline
From the alignment set, we derive an SFT-ready subset of
about 100K high-quality ads using the following filters:
• Duration: keep videos shorter than 120 s and clips within
2–60 s.
• Caption quality: discard ads with empty ASR, incoher-
ent lines, or heavy repetition.
• Visual–text relevance: for each clip, pair the first frame
with its ASR line and query Qwen2.5-VL-32B for a 0–5
relevance score; a video is retained only if at least 80%
of its clips score ≥4.
• Deduplication:
remove near-duplicates by hashing
{brand, product, script}.


## Page 17


This pipeline enforces strong multimodal consistency
and clean semantic grounding before constructing the task-
oriented SFT datasets.
7.6.3. Task-Oriented SFT Dataset Construction
The four supervised tasks introduced in Sec. 3 are con-
structed from the filtered pool. For training convenience,
some SFT tasks are expressed in an index-based output for-
mat. These indices serve only as task-level supervision over
the local candidate pool. In the full AutoCut pipeline, how-
ever, final video and audio asset grounding is performed by
embedding-based retrieval from the material database, as
described in Sec. 7.2. Since the main text focuses on task
definitions, here we summarize only the input–output for-
matting used to build the SFT dataset. All tasks are encoded
in a ShareGPT-style two-turn format with a system role
and a single human–assistant exchange.
• Video Selection. Input: product metadata, the full ad
script, and a pool of candidate multimodal clips (each clip
represented by its text snippet and video tokens). The
clips are presented in random order, and we make sure
that positive and negative clip ratios are 1:1. Output: the
subset of candidate clips that should appear in the final
ad, represented as indices within the local candidate pool.
• Video Sorting. Input: product metadata, the ordered ref-
erence script, and a set of selected clips whose order has
been randomly shuffled. Output: an ordering of the se-
lected candidate clips, represented as a permutation over
local candidate indices.
• Script Generation. Input: product metadata and an or-
dered sequence of clips. Output: a multi-line ad script
whose number of sentences matches the number of clips,
providing a sentence-level description aligned with the vi-
sual sequence.
• BGM Selection. Input: product metadata, the ordered
clips, and the full script.
Output: a discrete audio-
token sequence representing the target background-music
style, which is later grounded to a concrete track through
embedding-based retrieval.
For each task we construct approximately 25K–30K in-
stances, and adopt a 95/5 train–validation split. The clip-
level multimodal structure and the end-to-end SFT data con-
struction process are summarized in Fig. 7.


## Page 18


Table 5. Human evaluation criteria and decision guidelines used in the pairwise comparison study.
Criterion
Positive indicators
Negative indicators
Visual
Smoothness
• Transitions feel natural and continuous.
• No obvious stutter, jitter, or dropped
frames.
• Motion and camera movement appear sta-
ble.
• Noticeable lag, stutter, or frame skipping.
• Abrupt cuts that break visual flow.
• Shaky or inconsistent motion that dis-
tracts the viewer.
Logical
Consistency
• Shot order follows a clear story or expla-
nation.
• The same product and context are main-
tained throughout.
• Scene changes support a coherent narra-
tive or demo.
• Scenes feel random or out of order.
• Products or contexts change without ex-
planation.
• Transitions break the story or confuse the
viewer.
Script–Visual
Alignment
• The script accurately describes what ap-
pears on screen.
• Key selling points are shown at the right
visual moments.
• No hallucinated objects, brands, or func-
tions.
• The script mentions things not visible in
the video.
• Important visual content is not reflected
in the script.
• Timing between narration and visuals is
clearly off.
BGM–Visual
Compatibility
• Music tempo matches motion and editing
rhythm.
• Overall mood fits the product and sce-
nario.
• Volume and energy support, rather than
overshadow, the content.
• Music is too fast/slow compared with vi-
sual rhythm.
• Style or emotion of the music feels inap-
propriate.
• Sudden changes in volume or style that
distract the viewer.
Overall
Attractiveness
• The ad is engaging and easy to follow.
• Product value and advantages are clearly
conveyed.
• You would be more willing to consider
buying the product.
• The ad feels dull, confusing, or uncon-
vincing.
• Product value is unclear or poorly com-
municated.
• You would not be motivated to learn more
or purchase.
