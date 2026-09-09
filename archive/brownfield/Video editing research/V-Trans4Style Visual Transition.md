# V-Trans4Style Visual Transition

*Source PDF: `V-Trans4Style Visual Transition.pdf`*

*Total Pages: 26*

---


## Page 1


V-Trans4Style: Visual Transition
Recommendation for Video Production Style
Adaptation
Pooja Guhan1,2 , Tsung-Wei Huang2 , Guan-Ming Su2 ,
Subhadra Gopalakrishnan2 , and Dinesh Manocha1
1 University of Maryland, College Park MD 20740, USA
2 Dolby Laboratories, Sunnyvale CA 94085, USA
Abstract. We introduce V-Trans4Style, an innovative algorithm tai-
lored for dynamic video content editing needs. It is designed to adapt
videos to different production styles like documentaries, dramas, feature
films, or a specific YouTube channel’s video-making technique. Our al-
gorithm recommends optimal visual transitions to help achieve this flex-
ibility using a more bottom-up approach. We first employ a transformer-
based encoder-decoder network to learn recommending temporally con-
sistent and visually seamless sequences of visual transitions using only
the input videos. We then introduce a style conditioning module that
leverages this model to iteratively adjust the visual transitions obtained
from the decoder through activation maximization. We demonstrate the
efficacy of our method through experiments conducted on our newly
introduced AutoTransition++ dataset. It is a 6k video version of Auto-
Transition Dataset that additionally categorizes its videos into different
production style categories. Our encoder-decoder model outperforms the
state-of-the-art transition recommendation method, achieving improve-
ments of 10% to 80% in Recall@K and mean rank values over baseline.
Our style conditioning module results in visual transitions that improve
the capture of the desired video production style characteristics by an
average of around 12% in comparison to other methods when measured
with similarity metrics. We hope that our work serves as a foundation
for exploring and understanding video production styles further. [Project
Website]
Keywords: video transitions · video style · transition recommendation
· video editing
1
Introduction
With the growing popularity and consumption of digital content, creating high-
quality videos still remains a time-consuming, expensive, and highly creative
task. To meet the ever-growing demand for diverse and captivating multimedia
experiences, the strategic act of adapting videos into various production styles
emerges as an invaluable resource. Video production styles encompass distinct ap-
proaches and techniques employed in crafting videos. These styles aim to convey
arXiv:2501.07983v1  [cs.CV]  14 Jan 2025


## Page 2


2
Guhan, Pooja et al.
specific messages, elicit emotions, or achieve particular aesthetics. While there is
no finite set of video styles, they can be attributed to genre-specific approaches,
such as those used in documentaries, feature films, news/reportage, drama, and
vlogs. Additionally, video styles can be specific to famous directors and content
creators, or they may reflect an organization’s distinctive marketing styles [2].
These video styles can be achieved with a mix of multiple visual elements, in-
cluding camera angles, scene organization, and visual transitions [25]. Adapting
videos into these varied styles can help content creators create videos for diverse
audience preferences and consistently deliver captivating content that stands out
in the competitive landscape of digital media. However, editing videos to specific
styles remains a laborious task. In this work, we limit our scope of understand-
ing the dependence of video styles on visual transitions. Visual transitions serve
Input Video
(Production style: Cinematic) 
Encoder 
Decoder
Style Conditioning 
Module
Desired Production Style (Input): 
Indian Drama
Result Video
(Production style: Indian Drama)
Output: Sequence of 
Visual Transitions
Black Fade 
Zoom In
Fig. 1: Our goal is to recommend the optimal visual transition sequence for enabling
the adaptation of a given video to any desired production style. We propose V-
Trans4Style, a novel bottom-up approach consisting of an encoder-decoder architecture
and a style conditioning module.
as the creative glue during post-production, seamlessly connecting video clips
and enhancing the video’s flow and style. These effects enable smooth shifts be-
tween shots, often introducing a visual and sometimes thematic link between
them [1]. Fades, dissolves, wipes, cross-fades, etc are among the various types
of transitions, and they have a significant impact on the overall look and feel of
the video [30]. Today, state-of-the-art video editing softwares [5] offer capabili-
ties for implementing these transitions in videos. For non-professionals lacking
expertise in cinematography and design, the challenge lies in selecting transi-
tions from numerous possibilities and exploring various combinations to adapt
videos for different production styles. Even seasoned editors grapple with its
time-consuming nature. Video templates, i.e., pre-designed and pre-structured
video layouts, available today are limited, rigid, and are not tailored for the
user’s video content on which it is being applied. This thereby, reduces the over-
all quality of the adapted video. Therefore, we introduce an automated method
of recommending transitions for adapting videos for different video production
styles. To attain our objective, we must navigate through certain challenges.
Firstly, no publicly available dataset provides the different sets of transitions


## Page 3


V-Trans4Style
3
that need to be applied to the same video to adapt it for different styles. De-
veloping such a dataset is also an extremely tedious task. Additionally, unlike
measurable aspects of video production such as frame rate or resolution, video
style is abstract and lacks concise formulation. Apart from the desired video
style, the sequence of transitions being predicted for adapting a video should
also match the dynamics and rhythm of the video content as much as possible
to allow for video continuity.
Main Contributions: To overcome these challenges, we present V-Trans4Style.
Targeting video editing applications, our goal is to provide content creators with
a user-friendly approach that can enable them to adapt their videos to different
production styles, ultimately enhancing engagement and broadening audience
appeal. Our main contributions can be summarized as follows:
1. We present the first algorithm that facilitates video adaptation to various
styles during video editing. The input is a video comprised of an ordered set
of video clips and the name of the desired video production style. The output
is the recommended sequence of visual transition classes that the user should
use to adapt the input video to the desired video production style.
2. We present a novel method that follows a bottom-up approach to recommend
transitions suitable for video production style adaptation. We first train a
transformer encoder-decoder architecture to learn to recommend temporally
and visually consistent visual transitions. We then use our style condition-
ing module to perform a controlled update of its latent embedding during
inference time via activation maximization. This leads to the introduction
of video production style-based characteristics in the sequence of transitions
obtained from the decoder.
3. We create AutoTransition++, a mini representative dataset of AutoTransi-
tion [23] consisting of 6k videos. Additionally, in a bid to fortify our research
foundation, we also include additional annotations to categorize the videos
within it into five distinct video production styles.
We show quantitative evaluations on AutoTransition++. Our encoder-decoder
model shows an improvement of at least 10% in Recall@K and mean rank metrics
as compared to the baseline. Additionally, we show that our style conditioning
module can help better capture the video production style characteristics by
12% as compared to baselines.
2
Related Works
Video Editing. The recent surge in the popularity of video editing is largely
attributed to advancements in generative AI technologies. Within this field, four
main categories of work have emerged. The first category focuses on content
manipulation, where existing visual elements are modified on a frame-by-frame
basis. This empowers users to substitute specific objects with their preferred
choices [8, 15, 20]. Another aspect involves altering the visual appearance of
frames, such as transforming them into sketches or anime, without removing or


## Page 4


4
Guhan, Pooja et al.
replacing any objects [26]. This closely aligns with existing literature on image
style transfer in terms of their end objectives. Text-driven methods for modifying
visual content have also gained considerable popularity recently. The third cate-
gory encompasses tasks related to video summarization and highlight detection.
In this context, the goal is to pinpoint specific frames in the video that satisfy
particular queries [17,27,29] directly linked to the video’s content. Finally, the
fourth category pertains to the fundamental elements of video editing, including
cuts [4,19], transitions [23,24], and camera placements [21]. Additionally, there is
a wealth of research focused on video frame interpolation [12,18] and enhancing
the overall rendering quality of videos [9].
Visual Transitions in Videos. Visual transitions in video editing play a crucial
role in maintaining continuity, influencing the perception of time, and amplifying
the video’s ability to convey specific moods and emotions. Previous research has
primarily focused on identifying transitions in videos [16] and understanding
their impact on the viewing experience [28]. Among the existing literature, the
work closest to our objectives is [23], where they introduce a visual transition
recommendation system. While both their work and ours address the problem of
recommending visual transitions, our focus is specifically on ensuring coherence
and conformity of the recommended transitions with the intended production style
characteristics of the video.
Video Editing Datasets. Current video editing-related datasets are primarily
based on classifying video shots [3, 10], visual scene recognition, detecting and
identifying cuts in videos [19], multi-camera editing [21], detecting transitions
and recommending transitions [23]. However, there are no existing datasets, that
also give information regarding what video style category these fall under. The
lack of this information has made the task of solving problems related to how
style associates with the different video editing non-trivial. We, therefore, extend
the Autotransition dataset [23] to incorporate the video style-related labels.
Despite these advancements, there is a notable absence of work exploring the
distinct styles of video production and their unique compositions. Our work aims
to bridge this gap by examining the intersection of video editing and produc-
tion style, contributing to a deeper understanding of their unique characteristics.
Moreover, while previous works have primarily focused on manipulating the orig-
inal visual content, we instead only concentrate on altering the manner in which
different video clips are stitched together to compose the video.
3
Task Definition
A video V comprises of ordered video clips represented by  V  = \ {c_ 1, c _2, ..., c_n\} ,
where  c_i , for i ∈{1, 2, ..., n}, represents the  i^{th} video clip out of a total of  n 
video clips in  V . Now, consider the task of adapting video  V to adapt to a
different production style  s . Our objective here is to estimate the sequence of
visual transitions T = {tr1, tr2, ..., trn−1} that will facilitate the transformation
of the video for the given desired video style s. Here, trk for k ∈{1, ..., n−1} is the


## Page 5


V-Trans4Style
5
transition being recommended between video clips ck and ck+1 in the adapted
video. T can be an altered version of the transitions that V might have had
before production style adaptation or an entirely new sequence. In our method,
we take V and s as input and generate T as the output.
4
Dataset
4.1
AutoTransition Dataset
This dataset [23] primarily consists of 35k videos with each video annotated for
the set of transitions that have occurred. They provide information regarding
the class of transition, the timestamp of when it begins, when it ends, duration,
and type of transition. Overall, the dataset has 93 transitions. However, most of
the dataset transitions are spread across 30 different visual transitions. Some of
these transitions include pull-in, mix, dissolve, and black fade.
AutoTransition++ Dataset. We release a mini representative dataset of
the AutoTransition dataset comprising 6k videos to handle computational con-
straints. The transition distribution within AutoTransition++ mirrors that of
the AutoTransition dataset. Also, in our endeavor to enable the seamless adapta-
tion of videos across various styles using transitions, autotransition presents two
significant limitations. Firstly, it only provides a single set of transition anno-
tations for each video, leaving a gap in the availability of transition information
tailored to diverse video styles. This absence restricts its direct applicability for
adaptation across different style variations. Secondly, the dataset does not dis-
close the video style for each entry, impeding our ability to leverage this crucial
information for more effective and nuanced video adaptation.
A careful manual examination of the production styles of the videos within
the dataset resulted in categorizing the videos into five main categories: vlog,
influencer-centric, nature/urban-related scenes, photo slideshows, and anime.
The videos in these categories differed not only in terms of content but also
in the distribution of transitions. Therefore, the categorization was found rea-
sonable to be considered as five different video styles available in the dataset.
We enlisted the expertise of 8 seasoned annotators who possess extensive expe-
rience in evaluating a diverse range of visual content. They were initially made
to undergo a training phase where they evaluated our style categorization using
a curated selection of videos spanning various styles. This not only refined their
understanding of the task but also ensured uniformity and comprehension of the
distinct style labels. 1379 samples from the AutoTransition++ dataset were an-
notated with video-style labels. The distribution of visual transitions observed
in the annotated samples for the different video styles has been plotted in Fig. 2.
Fig. 2 also indicates that the different styles may incorporate common transi-
tions, potentially blurring the lines that distinguish one style from another. The
discerning factor between different video styles need not be only the presence of
a few unique transitions but also the frequency with which specific transitions
are employed in one style as compared to the other. This behavior is observed


## Page 6


6
Guhan, Pooja et al.
pull-in
mix
pull-out
circle-1
open
windmill
cube
switch
left
pane
circle-2
right
black-fade
turn-page
clock-wipe
blinds
heart-1
squeeze
floodlight
down
kaleidoscope
memory-1
white-flash
memory-2
blur
gradient-wipe
superimpose
dissolve-1
star-1
blanch
Vlog
Influencer
Photos-slideshow
Nature/Urban scenes
Anime
Video Production Style Categories
Transition Classes
Fig. 2: Bivariate distribution observed between the different styles and the visual tran-
sitions deployed across the 1379 video production style annotated videos within Auto-
Transition++.
not only among the samples annotated by us but also in video style analysis
shown by [23]. However, [23] have not released the video style data.
5
V-Trans4Style
Our overarching goal is to recommend visual transitions to facilitate the adapta-
tion of a video to a different production style. The top transitions obtained from
our algorithm should ideally satisfy three conditions. They should (a) match
the video content and dynamics (b) ensure video continuity and (c) exhibit the
desired production style characteristics. To this end, we opt for a bottom-up
approach. Our algorithm consists of three main components: an encoder (E),
a decoder (D), and a style conditioning module (SCM). Our encoder-decoder
is neural-network-based. Their combination is employed to learn a generative
model of visual transitions solely from video clips. Given an input V (set of
ordered video clips used in input video, Sec. 3), we feed it through the encoder
to obtain its embedding vector z. z is then fed to the decoder. The decoder will
then generate the corresponding sequence of n −1 transitions that only satisfy
conditions (a) and (b). n is the number of video clips in V . The trained encoder-
decoder network is subsequently used by the most crucial part of our algorithm,
the style conditioning module. It uses a gradient-based optimization approach
through activation maximization [6] to update z. This will favorably influence
the decoder outputs (i.e., the sequence of n −1 visual transitions) and thereby,
also satisfy condition (c).
5.1
Pre-trained Transition and Style Embeddings
This step serves as a pre-processing stage in the algorithm, aiming to derive
meaningful representations for distinct visual transitions and video styles. As


## Page 7


V-Trans4Style
7
𝑐!
𝑐"
𝑐#
Video Backbone 
Positional Encoding 
Transformer Encoder 
Linear Layer 
Linear Layer 
𝒉𝒕𝒇𝒆
𝒛𝒕
Transformer Decoder 
Past Transitions Embeddings 
[ℎ!
"#$%"#, ℎ&
"#$%"#, … , ℎ'(&
"#$%"#] 
Linear Layer
Classifier
𝒉𝒕
𝒕𝒇𝒅
𝒉𝒕
𝒅𝒆𝒄𝒐𝒅𝒆
Encoder 𝜺
Decoder 𝒟
SCM
𝒛𝒕
𝒛𝒕"𝟏
𝑡𝑟*
Transition 
Class  at step 𝑡
SoftMax
𝒉𝒕
𝒍𝒐𝒈𝒊𝒕
Input Video Clips
Desired Video Production 
Style Name
Fig. 3: V-Trans4Style: Ordered clips {c1, c2, .., cn} in V is fed to an Encoder E to
obtain zt. Decoder D takes in zt and outputs a sequence of transitions in n −1 steps.
At each step t, the D outputs trt. The masked transformed decoder uses past transition
embeddings in every step to compute htfd
t
. zt is same (i.e., z = zt) across all steps during
the joint training of E and D. Only components connected by →are active during
training. SCM is an inference-time module. At inference, for every step t, SCM takes
in current zt to estimate the appropriate zt+1 for the next step to produce production
style favorable transition trt.
detailed in [23], specific transitions share common visual effects, such as pull-
in and pull-out. Additionally, as depicted in Fig. 2, certain sets of transitions
are more prevalent in videos associated with one style compared to the other.
It is anticipated that the learned embeddings corresponding to these transi-
tions will capture these characteristics. To achieve this, we employ a multitask
learning-based network, MLN (Fig. 4). The network optimizes on two tasks: (1)
classifying visual transitions and (2) predicting the video style in which the tran-
sition will be employed. The network takes in only the video segment associated
with a visual transition and obtains its visual features using a video backbone.
These features are then linearly transformed and normalized to obtain a unit
vector, U. The unit vector U is then sent to two linear classifiers for transition
class prediction and video style prediction respectively. The embeddings corre-
sponding to each transition in the dataset and style are sampled from U (Refer
to appendix for details). Therefore, this will give us the set of visual transition
embeddings Etr = {etr
1 , etr
2 , ..., etr
Ntr} where etr
i
for i ∈{1, 2, ..., Ntr} represents
the embedding corresponding to the ith transition class. Ntr denotes the total
number of visual transition classes. With transition embeddings, we will also get
the set of style embeddings, Estyle = {estyle
1
, estyle
2
, ..., estyle
Nstyle}. Here, estyle
i
for
i ∈{1, 2, ..., Nstyle} refers to the embedding corresponding to the ith style and
Nstyle denotes the total number of video styles available.


## Page 8


8
Guhan, Pooja et al.
5.2
Encoder and Decoder
Our algorithm strongly depends on the encoder E and decoder D. Their col-
laborative operation to generate visual transitions using clips forms the core
of V-Trans4Style. The transitions obtained using E and D should take into ac-
count not only the visual content but also the temporal dependency between
transitions to ensure video continuity. Taking this into consideration, we employ
a transformer encoder-decoder-based architecture. The input is a sequence of
video clips in the order they appear in the input video. The output is a sequence
of transitions satisfying transition conditions (a) and (b).
We begin by uniformly sampling w frames from each video clip in V . These
are then fed into a video backbone following standard practices [23] to obtain an
embedding eV . In our experiments, we use SlowFast [7] as our video backbone.
Before sending the visual features of the video clips to the transformer encoder,
learnable position embeddings are element-wisely added to them. This is to
encourage the model to consider the sequence of the video clips in the input
video into consideration while recommending the sequence of transitions. The
transformer encoder outputs htfe that is fed to a fully connected layer to obtain
z. Therefore, E(V ) = z. To ensure video continuity, the decoder D is designed to
recommend one transition at a time, relying on previously generated transitions.
It uses a masked transformer decoder using a masked multi-head self-attention
on the target transition sequence. The attention for each transition is restricted
to cover only those preceding it in the sequence by using a triangular mask.
This ensures that D’s transition recommendation is causal and therefore, usable
during inference time when the full target transition sequence is not available.
For n video clips in V , D recommends transitions across n −1 steps. At each
step t, z along with transitions observed till step t −1 (obtained after masking)
fed to the transformer decoder outputs htfd
t
. Subsequently, hdecode
t
is fed into
another linear layer to produce hlogit
t
. To train the encoder-decoder part of the
algorithm, we make use of the following loss function:
  L _V = L_{classif i cation} + \lambda L_{masked\_triplet} 
(1)
where Lclassification corresponds to the cross entropy loss computed between
hlogit
t
and ytrans
t
(the ground truth transition classes for step t) across all time
steps. λ is a scalar hyperparameter. Lmasked_triplet is the masked triplet loss
computed as:
 \label {eqn:ma s
k
ed_ t r
i
plet_loss} L_{mas
k ed\_trip
l
e t} 
= \ fra
c  {1}{N_{tr}-1}\sum _{i\neq gt, i\in 1,...,N_{tr}} \mathcal {T}(h_t^{decode}, e_{gt}^{tr}, e_i^{tr}) 
(2)
where etr
gt represents the transition embedding corresponding to the ground truth
transition class and etr
i represents the transition embedding corresponding to the
ith class of transitions, except ground truth class. T calculates the triplet margin
loss for each triplet (hdecode
t
, etr
gt, etr
i )
  \m at hc a l {T}(a,  p ,  n) = m ax (\phi (a, p) - \phi (a, n) + m, 0) 
(3)


## Page 9


V-Trans4Style
9
m is the soft margin, a, p, n are anchor, positive sample and negative samples
respectively. Ntr is the total number of visual transition classes available. ϕ(x, y)
denotes the similarity metric between x and y. In this case, it is taken to be the
dot product between the two. We can define ϕ therefore as,
  \p hi  ( x,  y) = <x, y> 
(4)
Frames 
corresponding to 
Visual transition
Video Backbone
Linear
Linear Classifier
Linear Classifier
Transition class
Video Production Style
class
Normalize
𝒰
Fig. 4: MLN: The green box shows the region where the visual transition occurred in
the video. The frames corresponding to this transition are fed to a video backbone and
then through a linear layer to obtain U after normalization. This is then fed to linear
classifiers for predicting the transition class and the video style.
5.3
Style Conditioning Module
E-D network construction and training objective will only enable attainment
of visually and temporally coherent transitions. Incorporating video production
style information within the E-D network itself can be complex due to the ab-
sence of task-appropriate datasets (as discussed in Sec. 1 and 4). Therefore, we
propose a style conditioning module(SCM) to alter (if needed) the transition
choices made by the decoder above to align them with the requirements of the
desired video style. It is designed to eliminate the need to train E-D for each style
separately or have access to transition annotations for each style for each video
sample. SCM is activated after training the encoder-decoder network during in-
ference time. Its operational principle relies on the fundamental recognition that
the outputs derived from the decoder are driven by z. Therefore, this implies
that any alteration to z will change the decoder outputs. We leverage this simple
yet crucial property to achieve the purpose of this module in V-Trans4Style. We
implement the style conditioning module by employing a gradient-based opti-
mization strategy, guided by activation maximization(AM) [6] to update z. The
update is designed to ensure that the transition sequence generated by the de-
coder D exhibits the desired production style characteristics. We execute SCM
at every decoding step during inference. Therefore, let zt be the input to D at
step t. In our case, AM refers to the process of using backpropagation through


## Page 10


10
Guhan, Pooja et al.
the decoder weights to identify a permutation of zt to bring about a desired
change in the output of the decoder at step t + 1. This therefore requires us
to establish one or more distinct differentiable loss functions that can guide the
optimization of zt. These loss functions are equivalent to setting constraints that
the updated zt should try to satisfy. In our case, we have two loss functions.
Embedding Loss (LE). This ensures that zt is updated in a direction that
results in the decoder generating a transition sequence that facilitates the adap-
tation of the input video to the intended style.
  \ m a thcal {L _E} = 
1
 - \sigma _{cos}(e_\mu , e_k^{style}) 
(5)
where σcos(a, b) refers to the cosine similarity computed between two d-dimensional
vectors a, b ∈Rd, i.e.,
  \sigm a _
{ co s }
 (a, b) = \frac {<a, b>}{||a||_2 . ||b||_2} 
(6)
Additionally estyle
k
is the embedding corresponding to the kth video style among
Nstyle video styles (Refer Sec. 5.1) and we define eµ as the average of embeddings
corresponding to transitions that have been observed till decoder step t for the
video.
  e
_
\
mu 
= \sum 
_{i=1}^{t} h_i^{decode} 
(7)
Reconstruction Loss(LR). This ensures that there isn’t a significant deviation
in the values of zt that can compromise the integrity of the information derived
from the input video. To compute this, we trained a decoder Dψ that takes in
zt to retrieve back htfe. Referring to Sec. 5.2, htfe was obtained after encoding
the input and zt after processing it further. Therefore, even after the alteration
of zt, we can be sure that the input information has still been preserved in z
if we can reliably reconstruct htfe. More details about Dψ can be found in the
appendix. Essentially, let
  \mat h cal {D}_\psi (z_t) = \hat h^{tfe} 
(8)
Therefore, the reconstruction loss LR can be computed as
  \ma t hcal { L _R}(z) = |\hat h^{tfe} - h^{tfe}|_1 
(9)
htfe is not updated in this process. Therefore ∀decoding step t = 1 to n −1,
zt will be optimized to reconstruct the same htfe. The overall loss function used
for the optimization of zt
  \ma t hcal  {L}(z_t) = \alpha _\mathcal {E} \mathcal {L_E} + \alpha _\mathcal {R} \mathcal {L_R} 
(10)
where αE and αR are the step sizes corresponding to LE and LR respectively.
zk is initially assigned to be equal to zt. The following optimization process is
then run for 5000 iterations with a learning rate β to finally obtain zt+1 (Ref.
Fig 3).:
  z_ { k+ 1 } \leftarrow z_k - \beta \nabla \mathcal {L}(z_k) 
(11)


## Page 11


V-Trans4Style
11
Finetuning the transition sequence: After n −1 decoder steps, we obtain the
preliminary sequence of transitions T that can enable video style adaptation.
Optionally, we can finetune this sequence further if needed without affecting any
parameters or disrupting any required conditions drastically. We take inspiration
from RRT [13], a path-planning algorithm to do so. We consider the sequence of
hdecode
t
for t ∈{1, 2, ...n −1} that was generated in the process to obtain trt. By
the training construction of the decoder, trt corresponds to the transition class
whose pre-trained embedding is closest to hdecode
t
. For RRT instead, we consider
its K nearest pre-trained embeddings using a distance metric. K value should
not be too high or too low. A high K value can change T more than we need
and a very low K might not make much difference to T. K denotes the extent of
exploration we wish to do. Each of the K transitions is then iteratively evaluated
to compute eµ that is closest to the desired video style embedding, i.e., estyle
k
.
6
Experiments and Results
We first discuss implementation details, the metrics used, and baselines com-
pared with in Sec. 6.1. Our algorithm is a bottom-up approach to obtain visual
transitions that can facilitate the adaptation of a video to a different produc-
tion style. Each component plays a crucial role in building the entire algorithm.
Sec 6.2 analyzes each of their performance in detail.
6.1
Implementation Details
Model Details. Similar to AutoTransition [23], we have employed SlowFast
8x8 as the video backbone to extract visual features. This is used in the encoder
component as well as for both obtaining pre-trained transition and style embed-
dings. E and D each use 2 transformer layers for encoding and decoding with
dmodel = 512 and nhead = 8.
Data Pre-processing and Training Details. The maximum number of or-
dered clips considered in a video is user defined. For experiment purposes, we
have considered it as 8. For both, obtaining pre-trained transition embeddings
and transition sequence recommendations, we sample 16 frames with an image
size of 224 x 224 from each video clip in V . The former uses a batch size of 64
while the latter uses 16. Both training processes are run for a total of 60 epochs.
The model parameters of the last epoch are used to obtain the embeddings cor-
responding to the Ntr = 30 transition classes and Nstyle = 5 video production
style classes from MLN(Fig. 4). We train all our networks using the Adam op-
timizer [14] with a learning rate 1e-5. The margin m in triplet loss is set to 0.5.
We run our experiments on the AutoTransition++ dataset. For training E and
D, we use 80% of the data for training, validate the performance on 10% of the
data, and test on the remaining 10% of the data. We train all models on 8 A5000
GPUs. In SCM, we use an SGD optimizer [22] for optimization and a learning
rate of 0.1, αE and αR = 1. All codes were implemented using Pytorch [11].


## Page 12


12
Guhan, Pooja et al.
Metrics and Baselines. For a fair evaluation of only our encoder-decoder
model and pre-trained embeddings, we consider the metrics used by the only
other relevant baseline, AutoTransition. These include Recall@K where K∈{1, 5}
and Mean Rank. The evaluation is done for every transition in the sequence. For
SCM, we consider cosine similarity, which informs us about how relevant a
method’s recommended transitions are for the video production style we wish to
achieve.
Transition
Evaluation Metrics
Embedding
Recall@1↑Recall@5↑
Transition Classifier [23]
97.85
99.78
MLN Task-1
96.67
98.77
MLN Task-2
93.45
99.54
(a)
(b)
Fig. 5: (a) Compares transition classification results between [23]’s classifier and MLN.
MLN Task-1 is for Transition classification, and Task-2 is for video production style
classification. (b) Displays t-SNE visualizations of the transition embeddings. Fig. (A)
depicts embeddings from [23]’s method, while (B) represents embeddings from MLN.
6.2
Comparisons and Analysis
Pre-Trained Transition and Style Embeddings. Fig.5 provides insights
into the quality of pre-trained transition embeddings used for training E and D,
and style embeddings for SCM. MLN differs from [23]’s classifier in its ability
to obtain transition embeddings that obeyed both visual and style similarities.
Given the relatively smaller number of constraints, it is expected that the transi-
tion embeddings in the case of [23] will be comparatively more distinctly placed
(as observed in Fig.5b) as compared to that obtained using MLN. This compar-
ison aims to highlight that the additional style constraint in MLN doesn’t sig-
nificantly compromise transition classification accuracy while maintaining high
video style classification. Therefore, the differences between different transition
and style classes have been captured by MLN reliably.
Encoder-Decoder. In this work, we have limited our scope to understanding
visual content in videos and visual transitions. We, therefore, compare Auto-
Transition’s performance when using only visual inputs. Table 1 shows the re-
sults obtained from our experiments. Three notable observations emerge. Firstly,
both methods mostly demonstrate superior performance with pre-trained transi-
tion embeddings compared to randomly initialized embeddings. This underscores
the effectiveness of leveraging pre-trained embeddings for better mapping of the


## Page 13


V-Trans4Style
13
Table 1: Quantitative Results. We show the quantitative results of our encoder-
decoder model compared to AutoTransition [23] (only visual component included), our
baseline.
Transition
Method
Evaluation Metrics
Embedding
Recall@1↑Recall@5↑Mean Rank↓
Random
AutoTransition [23]
15.24
42.00
9.1
V-Trans4Style(E + D)
18.43
47.39
8.19
Transition Embedding [23] (Pre-Trained) AutoTransition [23]
16.93
44.58
8.82
V-Trans4Style(E + D)
23.24
56.06
6.77
MLN Transition
AutoTransition [23]
12.12
36.66
10.48
Embedding (Pre-Trained)
V-Trans4Style(E + D)
22.59
61.03
5.90
visual space to the transition space. Secondly, our encoder-decoder model con-
sistently outperforms AutoTransition across all metrics, regardless of the chosen
type of embedding. This suggests that capturing temporal relations between
transitions and visual content leads to more accurate recommendations for tran-
sitions. Thirdly, examining our model’s performance with transition embeddings
from [23]versus those from MLN reveals intriguing insights. Although the dif-
ference is subtle, it’s worth noting that Recall@1 is higher when using [23]’s
embeddings, whereas Recall@5 exhibits the opposite trend. This can be at-
tributed to the distribution of transitions in the embedding space. Fig.5b(A)
demonstrates better separation between transitions, explaining the higher pre-
cision of our encoder-decoder trained on [23]. On the other hand, Fig. 5b(B)
illustrates closer proximity between transitions, elucidating the higher Recall@5
when trained using MLN
Ablation Experiments on Encoder-Decoder Losses. Table 2 summarizes
results from an ablation experiment on the two loss functions used. When using
Lclassification alone, we observe the highest Recall@5 but the lowest Recall@1.
Conversely, using only Lmasked_triplet shows the opposite trend. The combina-
tion of both losses provides the most balanced results. This behavior can be
attributed to the specific strengths of each loss function, with Lclassification
emphasizing broader classification accuracy and Lmasked_triplet focusing on in-
tricate relationships within the data. The combination of both losses allows for a
balanced optimization, leveraging the strengths of each to achieve a more com-
prehensive performance across both metrics.
Style conditioning Module (SCM). To evaluate SCM, we randomly selected
100 videos from the test dataset, each comprising more than 6 video clips. For
each of the production styles defined in AutoTransition++ dataset, we computed
the cosine-similarity between eµ, i.e. the mean embedding of all the transitions
predicted for a video and the desired video production style embedding. Table 3
shows the mean of the cosine similarity scores obtained across the 100 samples
for each of the baseline methods. Higher similarity scores are better. Apart from


## Page 14


14
Guhan, Pooja et al.
Table 2: Loss Ablation Experiments. We show ablation experiments on the loss
functions used to train our encoder-decoder model. Bold denotes best while underline
denotes second-best
Loss
Evaluation Metrics
Function
Recall@1↑Recall@5↑Mean Rank↓
Lclassification
11.63
69.00
11.41
Lmasked_triplet
16.89
45.79
8.57
Lclassification + Lmasked_triplet
22.59
61.03
5.90
Table 3: Qualitative Results - SCM. We show the quantitative results of our
algorithm to recommend transitions to enable the adaptation of video production styles
with baselines. Bold denotes best while underline denotes second-best. The higher the
similarity better it is.
Method
Video Production Styles
Vlog
Anime Influencer Photos Nature
AutoTransition [23]
-0.007 0.0308
-0.089
-0.05
-0.025
V-Trans4Style(E & D)
-0.01
-0.035
-0.022
-0.018
0.013
V-Trans4Style(E & D, SCM w/o RRT)
0.018
0.0194
0.0102
0.0211 0.0496
V-Trans4Style(E & D, SCM w/ RRT)
0.188
-0.001
0.227
0.7286 0.356
Anime, we can observe that SCM improves the suitability of transitions for
adapting to the desired production style.
7
Conclusion, Limitations and Future Work
We present V-Trans4Style, a bottom-up approach for recommending visual tran-
sitions that adapt videos to different production styles, such as documentaries,
feature films, and dramas. Our 3-component algorithm inputs a video and de-
sired production style class to output a sequence of recommended transitions.
The encoder-decoder model maps the vision space to the transition space, ensur-
ing visually and temporally consistent recommendations. The style conditioning
module uses activation maximization to adjust the latent embedding, enabling
the decoder to produce style-specific transitions. We demonstrate our results
on AutoTransition++, a mini version of the AutoTransition dataset with 6k
videos. While this work focuses on visual transitions, future research will ex-
plore other editing elements like camera motion, cuts, and audio. Nevertheless,
our current work lays a crucial foundation for understanding video production
styles and their connections to editing elements.


## Page 15


V-Trans4Style
15
Acknowledgements
This work was done by Pooja as part of an internship with Dolby Laboratories.
References
1. Adobe Creative Cloud: Types of visual transitions. https://www.adobe.com/
creativecloud/video/discover/types-of-film-transitions.html, accessed:
2023-11-13
2. Alghamdi, E.A.: What makes video-based academic lectures difficult for language
learners to comprehend? the role of multimodal complexity. Foreign Language
Annals (2024)
3. Bain, M., Nagrani, A., Brown, A., Zisserman, A.: Condensed movies: Story based
retrieval with contextual embeddings. In: Proceedings of the Asian Conference on
Computer Vision (2020)
4. Chen, B., Ziai, A., Tucker, R.S., Xie, Y.: Match cutting: Finding cuts with smooth
visual transitions. In: Proceedings of the IEEE/CVF Winter Conference on Appli-
cations of Computer Vision. pp. 2115–2125 (2023)
5. Cloud, A.C.: Adobe premiere pro cc. línea) Disponible en: http://www. adobe.
com/mx/products/premiere. html (2014)
6. Erhan, D., Bengio, Y., Courville, A., Vincent, P.: Visualizing higher-layer features
of a deep network. University of Montreal 1341(3), 1 (2009)
7. Feichtenhofer, C., Fan, H., Malik, J., He, K.: Slowfast networks for video recog-
nition. In: Proceedings of the IEEE/CVF international conference on computer
vision. pp. 6202–6211 (2019)
8. Frühstück, A., Sarafianos, N., Xu, Y., Wonka, P., Tung, T.: Vive3d: Viewpoint-
independent video editing using 3d-aware gans. In: Proceedings of the IEEE/CVF
Conference on Computer Vision and Pattern Recognition. pp. 4446–4455 (2023)
9. Gao, Y., Cao, Y., Kou, T., Sun, W., Dong, Y., Liu, X., Min, X., Zhai, G.: Vdpve:
Vqa dataset for perceptual video enhancement. In: Proceedings of the IEEE/CVF
Conference on Computer Vision and Pattern Recognition. pp. 1474–1483 (2023)
10. Hassanien, A., Elgharib, M., Selim, A., Bae, S.H., Hefeeda, M., Matusik, W.: Large-
scale, fast and accurate shot boundary detection through spatio-temporal convo-
lutional neural networks. arXiv preprint arXiv:1705.03281 (2017)
11. Imambi, S., Prakash, K.B., Kanagachidambaresan, G.: Pytorch. Programming with
TensorFlow: Solution for Edge Computing Applications pp. 87–104 (2021)
12. Kalluri, T., Pathak, D., Chandraker, M., Tran, D.: Flavr: Flow-agnostic video
representations for fast frame interpolation. In: Proceedings of the IEEE/CVF
Winter Conference on Applications of Computer Vision. pp. 2071–2082 (2023)
13. Karaman, S., Walter, M.R., Perez, A., Frazzoli, E., Teller, S.: Anytime motion
planning using the rrt. In: 2011 IEEE international conference on robotics and
automation. pp. 1478–1483. IEEE (2011)
14. Kingma, D.P., Ba, J.: Adam: A method for stochastic optimization. arXiv preprint
arXiv:1412.6980 (2014)
15. Lee, S.H., Kim, S., Yoo, I., Yang, F., Cho, D., Kim, Y., Chang, H., Kim, J.,
Kim, S.: Soundini: Sound-guided diffusion for natural video editing. arXiv preprint
arXiv:2304.06818 (2023)
16. Nam, J., Tewfik, A.H.: Detection of gradual transitions in video sequences using
b-spline interpolation. IEEE Transactions on Multimedia 7(4), 667–679 (2005)


## Page 16


16
Guhan, Pooja et al.
17. Narasimhan, M., Rohrbach, A., Darrell, T.: Clip-it! language-guided video sum-
marization. Advances in Neural Information Processing Systems 34, 13988–14000
(2021)
18. Niklaus, S., Hu, P., Chen, J.: Splatting-based synthesis for video frame interpo-
lation. In: Proceedings of the IEEE/CVF Winter Conference on Applications of
Computer Vision. pp. 713–723 (2023)
19. Pardo, A., Heilbron, F.C., Alcázar, J.L., Thabet, A., Ghanem, B.: Moviecuts: A
new dataset and benchmark for cut type recognition. In: European Conference on
Computer Vision. pp. 668–685. Springer (2022)
20. Qi, C., Cun, X., Zhang, Y., Lei, C., Wang, X., Shan, Y., Chen, Q.: Fatezero: Fusing
attentions for zero-shot text-based video editing. arXiv preprint arXiv:2303.09535
(2023)
21. Rao, A., Jiang, X., Wang, S., Guo, Y., Liu, Z., Dai, B., Pang, L., Wu, X., Lin, D.,
Jin, L.: Temporal and contextual transformer for multi-camera editing of tv shows.
arXiv preprint arXiv:2210.08737 (2022)
22. Robbins, H., Monro, S.: A stochastic approximation method. The annals of math-
ematical statistics pp. 400–407 (1951)
23. Shen, Y., Zhang, L., Xu, K., Jin, X.: Autotransition: Learning to recommend
video transition effects. In: European Conference on Computer Vision. pp. 285–300.
Springer (2022)
24. Tang, S., Feng, L., Kuang, Z., Chen, Y., Zhang, W.: Fast video shot transition lo-
calization with deep structured models. In: Asian Conference on Computer Vision.
pp. 577–592. Springer (2018)
25. Viewinder: Film school: How editing can transform genre. https://viewinder.
com/editing-transforms-genre/
26. Wang, W., Xie, K., Liu, Z., Chen, H., Cao, Y., Wang, X., Shen, C.: Zero-shot video
editing using off-the-shelf image diffusion models. arXiv preprint arXiv:2303.17599
(2023)
27. Yasmin, G., Chowdhury, S., Nayak, J., Das, P., Das, A.K.: Key moment extraction
for designing an agglomerative clustering algorithm-based video summarization
framework. Neural Computing and Applications 35(7), 4881–4902 (2023)
28. Zhang, T., Tian, F., Hou, X., Xie, Q., Yi, F.: Evaluating the effect of transitions on
the viewing experience for vr video. In: 2018 International Conference on Audio,
Language and Image Processing (ICALIP). pp. 273–277. IEEE (2018)
29. Zhang, Y., Kampffmeyer, M., Liang, X., Tan, M., Xing, E.P.: Query-conditioned
three-player
adversarial
network
for
video
summarization.
arXiv
preprint
arXiv:1807.06677 (2018)
30. Zhou, J.: The analysis of short film shooting and editing techniques. In: 2nd Inter-
national Conference on Education, Language and Art (ICELA 2022). pp. 322–329.
Atlantis Press (2023)


## Page 17


V-Trans4Style: Visual Transition
Recommendation for Video-Production Style
Adaptation
—Appendix—
Pooja Guhan1 , Tsung-Wei Huang2 , Guan-Ming Su2 ,
Subhadra Gopalakrishnan2 , and Dinesh Manocha1
1 University of Maryland, College Park MD 20740, USA
2 Dolby Laboratories, Sunnyvale CA 94085, USA
1
AutoTransition++ Details
pull_in
mix
pull_out
circle_1
windmill
open
left
pane
switch
cube
circle_2
right
black_fade
clock_wipe
turn_page
blinds
floodlight
heart_1
down
kaleidoscope
memory_1
squeeze
blur
gradient_wipe
superimpose
star_1
dissolve_1
blanch
white_flash
memory_2
Transition Categories
Percentage
(A)
(B)
Fig. 1: (A) shows the transition distribution in AutoTransition++ dataset. (B) shows
the distribution of video production style labels available.
We have collected and showcased our proposed method of recommending
transitions based on the desired video production style on AutoTransition++, a
mini representative version of AutoTransition dataset. It consists of 6k videos.
The distribution of transitions in AutoTransition++ has been shown in Fig. 1.A.
1379 videos from these have been additionally annotated so far for video pro-
duction styles. We define the production styles considered as follows:
1. Vlog: A vlog is a video format that primarily centers around documenting
and sharing aspects of human experiences, including life, stories, or day-to-
day events. The content often revolves around the human subject, offering


## Page 18


2
Guhan, Pooja et al.
viewers a personal and relatable glimpse into their world. Whether recount-
ing personal anecdotes, showcasing daily routines, or sharing unique expe-
riences, the essence of a vlog lies in its ability to intimately connect the
audience with the broader spectrum of human perspectives and lives.
2. Anime: These typically consist of compiled segments or scenes from anime
shows.
3. Influencer: These typically revolve around content related to fashion, lifestyle,
and personal experiences. This may encompass elements such as photoshoots,
selfies, and videos that highlight the influencer’s unique style and interests.
4. Nature/Urban Scenes: These feature content centered around natural envi-
ronments, encompassing landscapes, wildlife, and even urban settings. These
videos may showcase the beauty of nature, including animals, and provide
glimpses into the diverse landscapes of urban areas.
5. Photo Slideshow: These videos cover a range of themes, including images
commemorating significant life moments, compiling cherished memories (from
outings or important events), promoting a brand, or offering glimpses into a
forthcoming drama series by showcasing scenes captured during production.
These videos may be a seamless slideshow, weaving the images together to
present a cohesive narrative of a specific day or event. They can also fea-
ture slideshows of inanimate objects, food, and subjects beyond personal
experiences.
These definitions were agreed upon between all annotators before they started
with the annotation process. While the AutoTransition dataset [23] suggests the
availability of video style-related information, we still believe that the availability
of AutoTransition++ is useful due primarily due the following reasons:
1. The style information claimed by [23] is not publicly available.
2. The styles discussed in [23] seems to focus more on creating visually appeal
and emotions. The labels introduced by us on the other hand are more to
do with the format and content delivery than a specific visual or emotional
style. They describe the type of content and the way it is presented. We
believe this would be a useful addition to the dataset and hence the creation
of AutoTransition++.
Ethical Considerations:
The data collection process does not include any per-
sonal, private or sensitive information, and was deemed exempt from an ethics
review. The videos being annotated for video production styles are part of an
existing dataset AutoTransition. Additionally, the annotators were instructed to
flag any video with harmful or offensive content.
The dataset can be accessed on our project webpage: https://gamma.umd.
edu/v-trans4style/


## Page 19


V-Trans4Style
3
2
Model Details
In this section, we provide additional details for two auxiliary models mentioned
in our work to develop V-Trans4Style. These include namely,MLN (Sec. 2.1)
and Dψ (Sec. 2.2).
2.1
MLN
The network, MLN shown in Fig. 4(in main paper) was used to obtain the pre-
trained embeddings for different transitions and video production styles. The
following loss function was used for training purposes:
 \la b el  { eqn : cond_ml} L_{mtl} = L_{TC} + \lambda L_{VPC}, 
(1)
LT C corresponds to the loss function for transition classification and LV P C cor-
responds to the loss function for video production style classification. Both LT C
and LV P C are cross-entropy (CE) loss functions. Training this network, however,
poses a challenge from the data perspective. More specifically, it relates to the
uneven number of labels available for each task. In the context of our problem, all
samples within the AutoTransition++ dataset can be used for training the tran-
sition classifier. However, not all of these samples have labels corresponding to
video production style too. Therefore, this imbalance in labeled samples across
both the tasks (i.e., transition and video production style classification) can
present challenges when training the multitask network MLN. We, therefore,
adopt selective task activation based training mechanism to maximize learning
by using the full potential of all our data samples. This implies that we activate
the branch corresponding to video production style classification only for inputs
containing labels for video production style. In other cases, only loss for transi-
tion classification is computed. Therefore the loss function can be modified as
follows:
  L_ {
m
tl }  = \ b e
gi n { c a ses} L_
{T C
} + \lambda L_{VPC} & \text {if } \hat {y}_{VPC} \text { exists}, \\ L_{TC} & \text {otherwise} \\ \end {cases} 
(2)
ˆyV P C refers to the video production style label for the sample.
Training Details:
Dataset split mentioned in Sec. 6.1 remains the same for
training MLN. We used a batch size of 64 and ran training for 30 epochs. We
used adam optimization with an initial learning rate of 1e-3.
2.2
Dψ
This component is introduced to calculate the reconstruction loss as defined in
Section 5.3. In this context, Dψ comprises two linear layers designed to take
input z and learn to produce htfe. During training, the encoder E remains fixed,
and the decoder D is not utilized. When presented with an input, E generates
htfe and subsequently derives z. This z is then fed into Dψ to ˆhtfe, i.e., the
reconstructed htfe. We compute L1 loss between htfe and ˆhtfe for training Dψ.


## Page 20


4
Guhan, Pooja et al.
Video Backbone 
Positional Encoding 
Transformer Encoder 
Linear Layer 
Linear Layer 
𝒉𝒕𝒇𝒆
𝒛
Encoder 𝜺
Linear Layer 
Linear Layer 
𝒉𝒕𝒇𝒆
"
Decoder 𝓓𝝍
𝑐%
𝑐&
𝑐'
Input Video Clips
Fig. 2: Dψ is used as a model capable of reconstructing the encoder feature vector
htfe. This property is used in the development of the reconstruction loss mentioned in
Sec. 5.3.
Training Details: Same data split used for training E and D is used for training
Dψ as well. We use Adam optimizer with initial learning rate of 1e −3 and run
the training for 60 epochs.
3
Additional Results
3.1
Pre-trained Transition and Style Embeddings
Fig 3 and Fig. 4 show the class-wise accuracies obtained for transition classifica-
tion and video style classification respectively using the multitask model MLN.
3.2
Quantitative Results
Testing on more videos. Table 3 in Sec. 6.2 showed results for randomly
selected 100 input videos. In Table 1 (Appendix), we perform the same exper-
iment on all videos that other components of V-Trans4Style have been tested
on. We compute the cosine similarity of the mean of the embeddings obtained
corresponding to the transitions recommended by the different methods and the
desired production style embedding. The similarity score is computed for each
video in the test dataset. The numbers reported in the table is the mean of the
cosine similarity scores obtained for every video across each style. We take the
mean of the transition embeddings as we are interested in understanding how
good the entire sequence of transitions is with respect to the desired production
style.


## Page 21


V-Trans4Style
5
0
20
40
60
80
100
0
20
40
60
80
100
5
10
15
20
25
30
Transition Classes
(A)
Accuracy (%)
Transition Classes
(B)
5
10
15
20
25
30
0
0
Accuracy (%)
29
0: pull_in
15: blinds
1: mix                          16: heart_1
2: pull_out
17: squeeze
3: circle_1                   18: floodlight
4: open                         19: down
5: windmill                  20: kaleidoscope
6: cube                          21: memory_1
7: switch                       22: white_flash
8: left                             23: memory_2
9: pane                          24: blur 
10: circle_2                  25: gradient_wipe
11: right                        26: superimpose
12: black_fade
27: dissolve 
13: turn_page
28: star_1
14: clock_wipe
29: blanch 
Fig. 3: Transition class-wise testing accuracy obtained (A) using MLN (B) using
AutoTransition [23]’s transition classifier. As observed, adding the style conditioning
doesn’t affect the class-wise accuracies much.
0
20
40
60
80
100
Accuracy (%)
Vlog
Photos
slideshow
Influencer
Nature
/Urban 
scenes
Anime
AutoTransition++ Video Production Style Classes
Fig. 4: Video production style-wise testing accuracy obtained using MLN


## Page 22


6
Guhan, Pooja et al.
Table 1: Quantitative Results - SCM. We show the quantitative results (cosine
similarity) of our algorithm to recommend transitions to enable the adaptation of
video production styles with baselines. Bold denotes best while underline denotes
second-best. The higher the similarity better it is.
Method
Video Production Styles
Vlog
Anime Influencer Photos Nature
AutoTransition [23]
-0.0034 0.0009
0.0018
0.0097 -0.0031
V-Trans4Style(E & D)
-0.0003 -0.0337
-0.0219
-0.0076 0.0037
V-Trans4Style(E & D, SCM w/o RRT)
0.0194 0.0047
0.02
0.0196 0.0286
V-Trans4Style(E & D, SCM w/ RRT)
0.2345 0.0117
0.127
0.728
0.353
User Studies To verify the credibility of our results further, we conducted a
user study. The goal was to determine if the input videos show signs of adaptation
to a different video production style after using our method’s recommended
transitions In this study, we engaged 102 users with five sets of examples, each
checking the adaptation to a different video production style. Each set comprised
of two reference videos showcasing the desired production style and two video
options. One option resulted after using visual transitions recommended by V-
Trans4Style(E + D, SCM w/ RRT) whereas the other was created using visual
transitions recommended by V-Trans4Style(E +D). Both the video options were
developed using the same sets of video clips. The reference videos however were
different. The results depicted in Fig. 5 highlight our method’s capability to
imbue desired video production style traits into videos originally of a different
production style. All user studies have been conducted after IRB review.
V-Trans4Style 
(𝜀+  𝒟, SCM w/ RRT)
V-Trans4Style 
(𝜀+  𝒟)
24.67%
75.33%
Fig. 5: User Study Results.
3.3
Qualitative Analysis
We also show some qualitative results obtained from our model. We show the
first few transitions in each case as the videos are long and contain my clips


## Page 23


V-Trans4Style
7
and visual transitions in case of Fig 6 and 7. Fig 8 shows the changes occurring
in transitions being selected in a sequential manner to eventually achieve the
desired video production style. We can see that the centroid of the transition
embedding space (black cross mark) in case of V-Trans4Style moves closer to
the style embedding space centroid (red cross mark).
4
Broad Impact
Video production style adaptation addresses the growing demand for personal-
ized and engaging content. In today’s digital age, with video content everywhere,
viewers seek content that matches their preferences. The traditional one-size-fits-
all approach often falls short, failing to cater to diverse tastes. Adapting pro-
duction styles allows content creators to better serve varied audiences, including
novice creators, making content creation more inclusive. This approach fosters
creativity and innovation by experimenting with different styles. Our work in-
troduces V-Trans4Style, a method that recommends visual transitions to adapt
videos to different production styles. While complete adaptation involves chang-
ing elements like camera motions, cuts, colors, and audio, our work lays a strong
foundation for future research. Future work will explore interactions between
different editing elements and develop algorithms to streamline the adaptation
process. However, it’s important to consider potential negative impacts, such as
content homogenization and privacy concerns. Balancing benefits and risks is
crucial to ensure ethical content creation, promote diversity and inclusion, and
prioritize user well-being in the digital media ecosystem.


## Page 24


8
Guhan, Pooja et al.
Reference Vlog 
example 2nd
Transition
1st Transition
(V-Trans4Style)
2nd Transition
(V-Trans4Style)
1st Transition
(V-Trans4Style w/o SCM)
2nd Transition
(V-Trans4Style w/o SCM)
Reference Vlog 
example 1st Transition
Fig. 6: Set (A) corresponding to a reference video showcasing the “vlog" video style.
This is provided only to visually show the transitions that can occur in this kind of
video style. The input to our model is however only the class label. Set (B) corresponds
to the video obtained after applying the transitions recommended by V-Trans4Style.
Set (C) corresponds to the video obtained after applying the transitions recommended
simply by V-Trans4Style(E + D).


## Page 25


V-Trans4Style
9
Reference Photos 
slideshow example 
2nd Transition
1st Transition
(V-Trans4Style)
2nd Transition
(V-Trans4Style)
1st Transition
(V-Trans4Style w/o SCM)
2nd Transition
(V-Trans4Style w/o SCM)
Reference Photos 
slideshow example 1st
Transition
Fig. 7: Set (A) corresponding to a reference video showcasing the “photos slideshow"
video style. This is provided only to visually show the transitions that can occur in
this kind of video style. The input to our model is however only the class label. Set (B)
corresponds to the video obtained after applying the transitions recommended by V-
Trans4Style. Set (C) corresponds to the video obtained after applying the transitions
recommended simply by V-Trans4Style(E + D).


## Page 26


10
Guhan, Pooja et al.
AutoTransition
𝜀+ 𝒟(AutoTransition
pretrained transition 
embedding)
V-Trans4Style
X
X
X
X
X
X
X
X
X
X
X
X
X
X
X
X
X
X
X
X
X
X
X
X
Fig. 8: We took a video and adapted it to the Vlog production style. The figure
here shows the changes in transition embedding space with every transition recom-
mended in the sequence. We do this comparison across 3 methods - AutoTransition,
V-Trans4Style(E + D) trained on AutoTransition pre-trained transition embeddings
and our V-Trans4Style. Here, blue corresponds to the Vlog style embedding space
while Brown corresponds to the mean transition embedding space.We can observe that
in case of V-Trans4Style, the mean transition embedding progressively moves towards
the style embedding.Note that the progression of the transitions happen from left to
right. Red cross mark corresponds to the centroid of the style embedding space. White
cross mark denotes the centroid of the mean transition embedding space.
