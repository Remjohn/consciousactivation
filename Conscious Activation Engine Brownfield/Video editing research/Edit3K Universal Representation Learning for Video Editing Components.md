# Edit3K Universal Representation Learning for Video Editing Components

*Source PDF: `Edit3K Universal Representation Learning for Video Editing Components.pdf`*

*Total Pages: 11*

---


## Page 1


Edit3K: Universal Representation Learning for Video Editing Components
Xin Gu1,2,†,‡, Libo Zhang2,3,†, Fan Chen1, Longyin Wen1, Yufei Wang1, Tiejian Luo2, Sijie Zhu1,∗
1ByteDance Inc. 2University of Chinese Academy of Sciences
3Institute of Software Chinese Academy of Sciences
{fan.chen, longyin.wen, yufei.wang, sijiezhu}@bytedance.com
guxin21@mails.ucas.edu.cn, libo@iscas.ac.cn, tjluo@ucas.ac.cn
Abstract
This paper focuses on understanding the predominant
video creation pipeline, i.e., compositional video editing
with six main types of editing components, including video
effects, animation, transition, filter, sticker, and text.
In
contrast to existing visual representation learning of vi-
sual materials (i.e., images/videos), we aim to learn vi-
sual representations of editing actions/components that are
generally applied on raw materials. We start by propos-
ing the first large-scale dataset for editing components of
video creation, which covers about 3, 094 editing compo-
nents with 618, 800 videos. Each video in our dataset is ren-
dered by various image/video materials with a single edit-
ing component, which supports atomic visual understand-
ing of different editing components. It can also benefit sev-
eral downstream tasks, e.g., editing component recommen-
dation, editing component recognition/retrieval, etc. Exist-
ing visual representation methods perform poorly because
it is difficult to disentangle the visual appearance of editing
components from raw materials. To that end, we benchmark
popular alternative solutions and propose a novel method
that learns to attend to the appearance of editing compo-
nents regardless of raw materials. Our method achieves fa-
vorable results on editing component retrieval/recognition
compared to the alternative solutions. A user study is also
conducted to show that our representations cluster visually
similar editing components better than other alternatives.
Furthermore, our learned representations used to transi-
tion recommendation tasks achieve state-of-the-art results
on the AutoTransition dataset. The code and dataset are
released at https://github.com/GX77/Edit3K.
∗Corresponding author, sijiezhu@bytedance.com
† Equal contribution
‡ This work was done during the first author’s internship at ByteDance
Raw Material
Text
Video Effect
Transition
Sticker
Filter
Animation
Video 
Representation Learning
Editing Component 
Representation Learning
Add Editing Components
Figure 1.
An overview of generic video representation learn-
ing and editing components representation learning. The embed-
ding of generic video representation learning is clustered based on
video content, e.g., semantics, context, etc, while the ideal editing
component representation should be only dependent on the applied
editing components rather than the content of raw materials.
1. Introduction
Video has emerged as a major modality of data across var-
ious applications, including social media, advertising, edu-
cation, and entertainment. The predominant video creation
pipeline for production, i.e., compositional video editing, is
based on the combination of editing components (Fig. 1),
e.g., video effect, animation, transition, filter, sticker, and
text. Tons of videos are created with these editing com-
ponents every day on various video creation platforms, but
little effort has been made to understand these editing com-
ponents. Specifically, learning universal representations for
editing components is unexplored but critical for lots of
downstream tasks in video creation fields, e.g., effects rec-
ommendation, detection, recognition, generation, etc.
Existing video representation learning methods [9, 14,
1
arXiv:2403.16048v2  [cs.CV]  25 Feb 2025


## Page 2


28, 32, 33] are usually developed on object-centric action
recognition datasets, e.g., Kinetics [16], to encode the in-
formation from the video content, e.g., semantics, the ac-
tion of the subjective, context, motion, etc. However, edit-
ing components usually do not have clear semantics, sub-
jective action, or context information. They could be a sim-
ple chroma change of the whole image or local effects like
scattering stars. Some components are special homography
transformations on the raw material (i.e., image/video) and
the rendered result is highly dependent on the appearance
of the raw material. Thus, it is extremely challenging to
learn a representation that encodes the information of edit-
ing components regardless of raw materials. Fig. 1 shows a
comparison between generic video representation learning
and our task. To the best of our knowledge, how to learn
universal representations for diverse types of editing com-
ponents remains unexplored in representation learning lit-
erature, and none of the existing datasets supports research
on learning universal representation for the 6 major types of
video editing components.
In this paper, we propose the first large-scale video edit-
ing components dataset, i.e., Edit3K, to facilitate research
on editing components and automatic video editing. The
proposed dataset contains 618, 800 videos covering 3, 094
editing components of 6 major types. Each video is ren-
dered with one editing component with both image and
video materials to enable atomic research on single editing
components. Given that the editing component is visually
mixed with raw materials, the key challenge of this problem
is to distinguish editing components in the rendered frames
but ignore the changes in the raw materials. We benchmark
popular representation learning methods, e.g., contrastive
learning and masked autoencoder, and propose a tailored
contrastive learning loss that better solves this problem. In
addition, we propose a novel embedding guidance archi-
tecture that enhances the distinguishing ability of editing
components by providing feedback from the output embed-
ding to the model. The learned editing element representa-
tions of our method can be directly applied to downstream
tasks e.g., transition recommendation [27], achieving state-
of-the-art results. Attention map visualization shows that
our model learns to focus on the editing components with-
out pixel-level supervision. We summarize our contribu-
tions as follows:
• We introduce the first large-scale dataset for video edit-
ing components covering 3, 094 atomic editing actions of
6 major categories, which makes it possible to learn uni-
versal representations for all 6 categories of editing com-
ponents.
• We propose a novel embedding guidance architecture that
aims to distinguish the editing components and raw mate-
rials, along with a specifically designed contrastive learn-
ing loss to guide the training process.
• We benchmark major alternative methods and validate the
superiority of our method in various scenarios. Exten-
sive experiments show state-of-art performance on both
Edit3K and AutoTranstion datasets.
2. Related Work
Video Editing/Creation Conventional workflow of video
editing requires a deep understanding of the raw im-
age/video materials and professional knowledge of editing
and aesthetics, e.g., manually cutting videos and selecting
editing effects, thus is extremely time-consuming for the
video creators. Automatic video editing can significantly
improve editing efficiency and it has been explored from
different perspectives [11, 18, 27]. Koorathota et al. [18] fo-
cus on contextual and multimodal understanding for video
editing. Frey et al. [11] transfer editing styles from a source
video to a target video with matched footage, considering
framing, content type, playback speed, and lighting of in-
put video segments. AutoTransition [27] proposes to au-
tomatically recommend transitions based on the previous
video frames and audio. Recently, there has been a thread
of works [4, 19, 35] using GAN [12] or diffusion [15, 25]
model to generate videos, but they are still not widely de-
ployed in real-world video creation applications. We con-
sider them as orthogonal works and they could be combined
with our work in the future.
Editing Components for Video Creation To the best of
our knowledge, none of the existing works provides a com-
prehensive study on video editing components. The most
related work, AutoTransition [27] is proposed for a spe-
cific downstream task, i.e., transition recommendation. The
AutoTransition dataset contains 104 transitions and only 30
transitions are used for the transition recommendation task.
This work only focuses on one specific type and does not
support learning universal representation for all the major
6 types of editing components.
Visual Representation Learning Visual representation
learning has been extensively studied for video data [10].
Early works conduct supervised classification [9, 29] on
large-scale datasets, e.g., Kinetics [16], to learn strong pre-
trained representation. Recent self-supervised representa-
tion learning methods, e.g., contrastive learning [5, 13, 21,
22] and masked autoencoder [2, 14, 28], have achieved
comparable performance as supervised methods on down-
stream tasks[10]. The key insight is to learn a representation
space where visually similar videos are close to each other.
However, existing works have limitations on learning repre-
sentation for editing components from video data (Sec. 5.2),
because these methods are not designed to distinguish the
raw material and editing components in the video frames.
2


## Page 3


Raw Material
Text
Video Effect
Transition
Sticker
Filter
Animation
Figure 2. Examples of 6 major types of video editing components, i.e., video effect, animation, transition, filter, sticker, and text.
Video Effect
Animation
Transition
Filter
Sticker
Text
Total
Classes
888
176
204
228
1000
598
3,094
Rendered Videos
177,600
35,200
40,800
45,600
200,000
119,600
618,800
Table 1. The statistical information of the proposed Edit3K dataset.
3. Edit3K Dataset
Existing video datasets mostly focus on understanding the
overall content of the video frames, e.g., action, context, se-
mantics, and geometry, which can not support the research
for understanding video editing components. The most re-
lated dataset is proposed in AutoTransition [27], but this
dataset only contains one editing component type (i.e., 104
transitions) out of the major six types with limited coverage.
To the best of our knowledge, our dataset is the first large-
scale editing component dataset for video creation covering
all the six major types, i.e., video effect, animation, transi-
tion, filter, sticker, and text.
3.1. Editing Component Definition
There is no formal definition for the 6 types of editing com-
ponents in the academic literature, so we summarize the ma-
jor difference between them and describe their connection
with existing concepts. Examples are shown in Fig. 2.
Both video effects and filters change the appearance of
material images or video frames toward a specific style, but
video effects focus more on local editing, e.g., adding shin-
ing star-shaped markers. Filters mainly change the over-
all style of the whole scene, e.g., adjusting the illumination
and chroma. Animation can be considered as a homography
transformation applied to the whole material, which is sim-
ilar to camera viewpoint changes. The transition is applied
to connect two materials with appearance changes and fast
motion. The sticker simply uses copy-paste to add another
foreground object on top of the current material, which is
similar to image composition [36]. However, some of the
stickers are video stickers and the stickers may look differ-
ent in each frame. Text is a special sticker whose content
can be edited by the user, but the text style can be changed
by applying different fonts.
We focus on text font/style
rather than the content in this paper.
3.2. Dataset Generation
It is challenging to collect an academic dataset for editing
components because online published videos [27] usually
apply multiple editing components sparsely in an entangled
way. Most of the frames may contain no editing component
or only a simple filter, while a small number of frames (e.g.
a 0.5 s slot) could have stickers/text, video effects, and ani-
mations at the same time. To address this limitation, we pro-
pose to render videos based on existing raw materials and
a pre-defined set of editing components using a free-to-use
video editing tool, i.e., CapCut [1]. Each video only con-
tains one disentangled editing component to support atomic
research on all editing components with a balanced distri-
bution.
We use images and videos from the ImageNet [6] and
ImageNet-Vid [6, 26] datasets as raw materials for render-
ing. For each video, we randomly take two images/videos
as the source material pair for two video slots, and each slot
lasts 2 seconds. If the component is a transition, we add
it between the two slots, which lasts for 2s, and each slot
is reduced to 1s. Otherwise, we apply the component on
both the two slots, which covers 4s. In total, we generate
618, 800 videos covering 3, 094 editing components.
3


## Page 4


Transformer
×𝑵𝒗
Embedding
Embedding
Queue
Clustering
Guidance
InfoNCE
Embedding
Centers
Embedding
Guided Spatial Encoder
ViT
...
...
Input Frame
×𝑵𝒕
...
...
Temporal Encoder
…...
…...
Guided Embedding Decoder
Transformer
×𝑵𝒅
Transformer
Class Token
Guidance Token
Image Token
Key, Value
Key, Value
Query
Query Token
Temporal Token
Loss
Figure 3. An overview of the proposed method. The input video frames are fed to the spatial and temporal encoder to generate the visual
features. Then the embedding decoder takes the visual features as key, value and generates the final editing component embeddings using
cross-attention mechanism with one query token. All encoders and decoders are guided with guidance tokens which are the embedding
centers of the embedding saved in a queue. The model is optimized with InfoNCE [13, 21] loss across the batch and the embedding queue
provides extra negative samples for an extra loss term. Best viewed on screen with zoom-in.
3.3. Dataset Statistics
Tab. 1 shows the detailed statistical information of the 6
categories of editing components in the proposed dataset.
Our dataset contains significantly (29.75×) more editing
components than AutoTransition [27] dataset. Unlike Auto-
Transition [27] which adopts online published videos with
unbalanced distribution, our dataset is more balanced across
different editing components which is critical for represen-
tation learning. Our dataset is the first one to provide edit-
ing components with static image materials, which provides
valuable research source data for understanding the motion
effect of editing components.
4. Method
Fig. 3 shows an overview of the proposed method. We first
formulate the problem in Sec. 4.1. Then we describe the
guided spatial-temporal encoder in Sec. 4.2 and the guided
embedding decoder in Sec. 4.3. Sec. 4.4 introduces the em-
bedding queue mechanism and Sec. 4.5 describes the loss
function.
4.1. Problem Formulation
Given the input video frames F = {fi}Nv
i=1 where fi ∈
RH×W ×C (H, W, C denote the height, width and chan-
nels), the goal of our model is to generate an embedding
that encodes the information of the editing component in
the video for recognition, recommendation, etc. An ideal
embedding should be dependent on the applied editing com-
ponents but independent of the raw video materials. In ad-
dition, we expect visually similar editing components to be
close to each other in the embedding space, e.g., all heart-
shaped video effects may be distributed in a cluster.
To achieve this goal, we formulate this special repre-
sentation learning task as a contrastive learning problem.
Given a set of raw material videos M = {mi}Nm
i=1 and
editing components E = {ej}Ne
j=1, we can render each
raw video with all the Ne editing components, resulting in
Nm × Ne rendered videos {(mi, ej)}. For the editing com-
ponent ek, all the rendered videos using this editing com-
ponent {(mi, ek)} are considered as positive samples for
each other. On the other hand, all the rendered videos with
other editing components {(mi, ej)|j ̸= k} are considered
negative samples for ek. A contrastive loss [13, 21] (Sec.
4.5) is then applied to pull the positive samples closer while
pushing the negative samples away in the embedding space.
4.2. Guided Spatial-Temporal Encoder
Guided Spatial Encoder. As shown in Fig. 3, the Nv in-
puts frames are fed to the spatial encoder separately. We
follow ViT [8] to evenly divide the input frame into small
patches with the size of 32 × 32. The patches are fed to
a linear projection layer [8] to generate patch embedding,
and positional embedding [8] is added to each embedding
to generate the image tokens (blue squares in Fig. 3). To
help the model distinguish editing components and raw ma-
terials in the rendered frames, we add another set of guid-
ance tokens (yellow squares in Fig. 3) in the input, which
will be described in Sec. 4.4. The guidance tokens can be
considered as feedback from the learned embedding to the
input and provide the spatial encode with prior knowledge
of possible editing components. The class token (red square
in Fig. 3) is concatenated to the input tokens to aggregate
the information from all the tokens. The tokens are fed to
multiple transformer layers with multi-head self-attention
[31], and the output class token of the last transformer layer
is used as the output of the whole frame.
Temporal Encoder.
For Nv input frames, Nv output
4


## Page 5


class tokens are generated separately without temporal cor-
relation.
However, some editing components, e.g., ani-
mation, and transition, contain strong motion information
which requires strong temporal information to understand.
Therefore, we add a temporal encoder containing Nt self-
attention [31] transformer blocks to learn the temporal cor-
relation between frames. In addition, some editing compo-
nents may be indistinguishable if the sequential information
is missing. For example, “move to left transition” played in
reverse order is the same as “move to right transition”, so
we add position embedding [31] to the input tokens of the
temporal encoder to provide sequential information.
4.3. Guided Embedding Decoder
The output tokens of the spatial-temporal encoder contain
the mixed information from the editing components and
the raw materials.
Inspired by end-to-end object detec-
tion DETR [3], we leverage the cross-attention [31] mech-
anism to extract information corresponding to the editing
components from the input tokens. As shown in Fig. 3,
we first adopt the guidance tokens (Sec. 4.4) as the (key,
value) tokens of the cross-attention transformer block [31],
which represent the historical embedding of editing com-
ponents. One query token is fed to the first transformer
block to extract prior knowledge of the editing components
embedding.
The output token is then fed to the second
transformer block as the query token and the output of the
spatial-temporal encoder is used as (key, value) tokens. The
guided embedding decoder contains Nd layers of these two
transformer blocks, and the output token of the last layer is
used as the final embedding of the input video.
4.4. Embedding Queues
The limited batch size is not able to provide enough hard
negative samples for contrastive learning and this issue is
typically addressed with sample mining [34] or memory
bank/queue [13]. Different from the memory bank in MoCo
[13], we build the dynamic embedding queues to save the
recently generated embedding corresponding to all editing
components instead of the whole video set. For each spe-
cific editing component in the training set, we maintain a
first-in-first-out (FIFO) queue with the size of 5 to save the
most recently generated embedding corresponding to this
editing component during training. The memory cost of the
embedding queues is negligible, but it provides a large num-
ber of negative samples for contrastive learning (Eq. 2). All
the embeddings are l2-normalized before joining the queue.
Moreover, the embedding queues provide prior knowl-
edge of all the editing components that can be used as
guidance to improve the spatial-temporal encoder and the
embedding decoder for distinguishing editing components
from raw videos. However, using thousands of embedding
as guidance tokens would cost a lot in terms of GPU mem-
ory and computation, we thus adopt the embedding centers
as the guidance tokens. Since the 6 types of editing com-
ponents are naturally clustered into 6 corresponding centers
in the embedding space, we compute the embedding cen-
ters for the 6 types as guidance tokens by default, which
involves negligible memory and computation costs. Alter-
natively, k-means clustering centers also perform well as
guidance tokens (Sec. 5.4).
4.5. Loss Function
Our model is optimized with two loss terms, i.e., in-batch
loss and embedding queue loss. We adopt the widely used
InfoNCE loss [13, 21] formulation but use our task-specific
positive and negative definition (Sec. 4.1). We first sam-
ple Nb editing components in a batch, i.e., {ei}Nb
i=1. For
each editing component ei, we randomly select two positive
samples, and their embeddings are denoted as qi and ki. Ap-
parently, other embeddings in this batch, e.g., {kj}j̸=i are
negative samples for qi because they correspond to different
editing components. The in-batch loss is written as:
Lbatch = 1
Nb
Nb
X
i=1
−log
exp(qi · ki/τ)
PNb
j=1 exp(qi · kj/τ)
,
(1)
where · means the cosine similarity operation between two
embeddings and τ is the temperature.
Assume that we
have Ne editing components in total for the training. There
are Ne embedding queues (Sec. 4.4) saving the most re-
cent embeddings generated during training, we take the l2-
normalized average embedding in each queue as the refer-
ence embedding, i.e., {rj}Ne
j=1. The embedding queue loss
term is given as:
Lqueue = 1
Ne
Ne
X
i=1
−log
exp(qi · ri/τ)
PNe
j=1 exp(qi · rj/τ)
.
(2)
This term covers other hard negative editing components for
qi and improves both the performance and training stability.
The final loss is computed as L = Lbatch + Lqueue.
5. Experiment
5.1. Implementation Details
We implement our method using PyTorch [23].
We use
CLIP-B/32 [24] pre-trained weights to initialize the spatial
encoder and the remaining modules are all randomly initial-
ized. We follow BERT [7] to implement the self-attention
and cross-attention transformer block. For input videos, we
uniformly sample Nv = 16 frames from each video, and the
height H and width W of each frame is resized to 224×224.
We train our model with Adam [17] optimizer and cosine
[20] learning rate scheduling. The batch size Nb per GPU is
set to 8 by default and all models are trained for 20 epochs.
5


## Page 6


Query Video
3094 Candidate Videos
. . .
Figure 4. An example of editing components retrieval, which includes the query video and 3094 candidate videos. The green box indicates
the ground truth of this query video. Best viewed on screen with zoom-in.
Video Effect
Animation
Transition
Filter
Sticker
Texts
Avg.
R@1
R@10
R@1
R@10
R@1
R@10
R@1
R@10
R@1
R@10
R@1
R@10
R@1
R@10
VideoMAE [28]
10.4
16.1
21.6
29.1
15.0
23.8
4.9
6.2
5.2
5.3
6.8
6.8
10.7
14.5
VideoMoCo [13, 22]
37.3
72.8
27.3
61.0
19.6
47.8
18.4
44.1
60.3
94.9
38.6
93.8
33.6
69.1
Ours (Baseline)
33.5
71.5
22.4
68.4
30.0
76.2
15.6
40.6
56.6
93.9
28.8
85.4
31.2
72.7
Ours
55.3
80.6
51.6
81.8
54.6
85.3
22.5
48.0
85.8
98.2
46.0
89.7
52.6
80.6
Table 2. Comparison with state-of-the-art methods on Edit3K dataset for editing components retrieval in terms of R@k (%).
It takes 16.7 hours to train our representation model on 8
Nvidia A100 GPUs. The learning rate of the spatial encoder
is set to 1e −6, and we use 1e −5 for the rest of the model.
The numbers of layers in the temporal encoder and embed-
ding decoder, i.e., Nt, Nd, are both set to 2. For both the
encoder and the decoder, the number of attention head is set
to 8 and the hidden dimension is 512. The total number of
raw material videos and editing components, i.e., Nm, Ne,
are 200 and 3094, respectively. The temperature parameter
τ in Eq. 1, 2 is set to 0.7.
5.2. Editing Components Retrieval
In this section, we conduct experiments on the editing com-
ponent retrieval task to evaluate how the embeddings of
videos rendered from the same editing component and dif-
ferent materials are clustered. Specifically, we randomly
select one video rendered with a certain editing component
and one pair of raw materials as the query. Then we ran-
domly select a set of videos rendered with another pair of
materials and all editing components in the evaluation set
as the candidate set. If the retrieved video uses the same
editing component as the query video, this query is consid-
ered correct (the example is shown in Fig. 4). We report the
average Recall at k (denoted R@k) for all queries.
We compare our method with state-of-the-art video self-
supervised representation learning methods. Recent works
fall into two categories, i.e., contrastive learning [13] and
masked autoencoder [14]. Therefore, we select two best-
performing methods for comparison, i.e., VideoMoco [22]
and VideoMAE [28]. The original contrastive loss of Video-
Moco [13, 22] is conducted between different frame content
which does not work well on Edit3K dataset, we thus imple-
mented a tailored version using our contrastive loss between
editing components. We also re-train VideoMAE on Edit3K
dataset with their official code.
Tab. 2 shows the detailed performance of six types
of editing components, as well as the average accuracy.
The tailored version of VideoMoCo performs on par with
our baseline model, and our method performs significantly
(19%) better in terms of average R@1, indicating the supe-
riority of the proposed guidance architecture. VideoMAE
does not work well on Edit3K because it is optimized with
reconstruction loss which does not distinguish the raw ma-
terial and editing component in the video frames.
5.3. Editing Components Representation Distribu-
tion
Sec. 5.2 has verified that the embeddings of video with the
same editing components are well clustered in the embed-
ding space, we compute their embedding center as the em-
bedding of each editing component and evaluate the dis-
tribution across different editing components. Ideally, vi-
sually similar editing components should be close to each
other in the embedding space. We split the 3, 094 editing
components of Edit3K in half for open-set setting (details
in supplementary material), resulting in 1, 547 editing com-
ponents for training and the other half for evaluation. Af-
ter training is finished, we first compute the embedding for
the 1, 547 unseen editing components in the evaluation set,
where the embedding of each editing component is com-
puted as the center of all video embeddings correspond-
ing to this specific editing component. We randomly se-
lect 27 editing components from each of the 6 major types
as queries. Then, each query performs a search among the
embedding of all the editing components except the query
itself. The top-1 retrieved result is used for the user study,
resulting in 162 query-result pairs. We follow this process
to generate results for 4 methods, i.e., ‘Random’, ‘Video-
MoCo’, ‘Ours (Baseline)’, and ‘Ours’. In total, we get 648
query-result pairs for evaluation.
6


## Page 7


Query Video
✓
Select all the videos that are visually similar to the query video
Figure 5. An example from the user study. The users are asked to select all the videos that are visually similar to the query video. Best
viewed on screen with zoom-in.
Method
V. E.
Anim.
Tran.
Filt.
Stic.
Text
Avg.
Random
0.9
0.9
1.6
0.9
0.8
1.3
1.1
VideoMoCo
45.7
49.1
69.5
37.5
40.1
52.3
49.0
Ours (Baseline)
37.4
59.4
67.9
39.7
37.6
43.2
47.5
Ours
61.3
67.9
67.1
46.6
62.4
63.9
61.5
Table 3. The satisfactory rate (%) of different methods in user study. V.E., Anim., Tran., Filt., Stic. denote video effect, animation,
transition, filter, and sticker.
Query
Ours
Ours (Baseline)
VideoMoCo
Random
Figure 6. The top-1 similar editing components corresponding to the query editing component using different methods. The similarity is
computed based on the embedding centers of editing components and we show one frame of a randomly selected video corresponding to
each editing component for visualization. Best viewed with zoom-in.
The users are given 5 videos in a row, where the left col-
umn is the video for the query editing component, and the
other columns show the example videos for the retrieved
editing components corresponding to the 4 methods (an ex-
ample is shown in Fig. 5). The users are asked to select
the videos that are visually similar to the query and each
query is evaluated by at least 10 users. The selected results
are considered satisfactory and we compute the satisfactory
rate of different methods on all queries. As shown in Tab. 3,
‘Ours’ significantly outperforms the other three methods in
terms of average satisfactory rate, indicating the effective-
ness of the proposed guidance architecture and additional
loss on embedding distribution. The result is also consistent
across different editing component categories. Qualitative
results is provided in Fig. 6. The t-SNE [30] visualization
for the embedding space is provided in the supplementary
material.
5.4. Ablation Study
Different Modules. We conduct ablation study in Tab. 4
by removing different modules to demonstrate the effec-
tiveness of each module.
The ‘Baseline’ model with
7


## Page 8


Video Effect
Animation
Transition
Filter
Sticker
Texts
Avg.
R@1
R@10
R@1
R@10
R@1
R@10
R@1
R@10
R@1
R@10
R@1
R@10
R@1
R@10
Baseline
33.5
71.5
22.4
68.4
30.0
76.2
15.6
40.6
56.6
93.9
28.8
85.4
31.2
72.7
Baseline + Lq
40.3
76.4
32.7
69.2
30.9
72.9
20.8
39.8
58.8
94.6
36.1
90.2
36.6
73.8
Baseline + Lq + GT
43.2
75.9
37.4
70.9
39.2
76.4
20.8
44.3
58.1
95.1
41.5
92.4
40.0
75.8
Baseline + Lq + GD
51.0
78.6
41.0
82.0
49.8
87.5
21.0
44.9
79.2
97.7
52.1
90.3
49.0
80.2
Baseline + Lq + GT + GD
55.3
80.6
51.6
81.8
54.6
85.3
22.5
48.0
85.8
98.2
46.0
89.7
52.6
80.6
Table 4. Ablations study for different modules of our method on Edit3K for editing components retrieval in terms of R@k (%). Lq is the
embedding queue loss. ‘GT’ and ‘GD’ represent the guided tokens and guided decoder.
Method
R@1
R@10
None
36.6
73.8
K-Means
52.1
79.9
Default 6 Types
52.6
80.6
Table 5. Ablation of different methods for gen-
erating embedding centers on Edit3K for edit-
ing components retrieval in terms of R@k (%).
Pre-computed Transition Embedding
…
Transition 
Recommendation 
Model
Similarity Calculation
Ranking of Transitions
Input
Video
Figure 7. An overview of the transition recommendation pipeline.
Transition Embedding
Performance
Method
Dataset
R@1
R@5
Rank (↓)
Random [27]
-
25.67
66.30
5.65
Classification[27]
AutoTransition
28.06
66.85
5.48
Ours-A
AutoTransition
28.89
67.12
4.86
Ours-E
Edit3K
29.24
67.32
4.56
Table 6. Comparison of different transition embeddings on the AutoTransition [27] test set in terms of R@k (%) and mean rank. All the
rows use the same recommendation model training pipeline from [27] and the only difference is the pre-computed fixed embedding for the
transitions.
only spatial-temporal encoder and in-batch InfoNCE loss
achieves an average R@1 score of 31.2%. Adding the em-
bedding queue loss term (‘Baseline + Lq’) brings 5.4% im-
provement on the R@1 accuracy, indicating the effective-
ness of the Lq in Eq. 2. The R@1 is further improved by
3.4% when adding guidance tokens in the spatial encoder
(‘Baseline + Lq + GT’). Instead, deploying the guided em-
bedding decoder (‘Baseline + Lq + GD’) also gains 12.4%
improvement on R@1 over ‘Baseline + Lq’. The perfor-
mance is further improved when all the modules are em-
ployed (‘Baseline + Lq + GT + GD’), demonstrating the
effectiveness of the guidance architecture.
Embedding Centers. Tab. 5 shows the ablation study us-
ing different embedding centers as guidance tokens. Both
‘Default 6 Types’ and ‘K-Means’ perform well with a sig-
nificant performance boost over ‘None’ (no embedding cen-
ters), indicating our guidance architecture is generic for dif-
ferent clustering methods. The default version with 6 edit-
ing component types performs slightly better on Edit3K, but
the k-means clustering centers are more flexible for other
tasks.
5.5. Transition Recommendation
We conduct experiments on transition recommendation as a
downstream task to validate the generalization ability of our
learned universal representation. In [27], the embeddings
of transitions are pre-computed with a classification model
trained on AutoTransition dataset, and the embeddings are
fixed during the training of the recommendation model. As
shown in Fig. 7, we follow [27] to train transition recom-
mendation models which take a raw video as input and gen-
erate ranking scores for a set of transitions. We replace the
pre-computed transition embeddings with other alternative
methods to validate the benefit of a strong representation on
downstream tasks. We follow [27] to report R@k and mean
rank for evaluation.
Tab. 6 shows that the embedding of the proposed method
trained on AutoTransition datasets (‘Ours-A’) outperforms
the state-of-the-art result in [27] (‘Classification’), indi-
cating the superiority of the proposed architecture. Since
8


## Page 9


1
2
3
4
5
6
7
8
Frame Index
1.0
0.9
0.8
Attention
1
2
3
4
5
6
7
8
Figure 8. Visualization of the attention map in the spatial and temporal encoder. The first row shows the spatial attention maps overlaid on
the 8 input frames, the bottom axis shows the temporal attention value for each frame. The model focuses on the lipstick-shaped sticker
for all the frames without explicit spatial supervision. Best viewed on the screen with zoom-in.
the transitions in AutoTransition dataset are included in
our Edit3K dataset, we further adopt the pre-computed
embedding on Edit3K (‘Ours-E’) and it brings additional
performance boosts, indicating the superiority of our di-
verse and balanced dataset. Note that all the rows use the
same recommendation method and the only difference is the
pre-computed transition embeddings, a slight performance
boost could indicate significant improvement on represen-
tation learning.
5.6. Attention Visualization
Fig. 8 shows both the spatial and temporal attention
map of our model by visualizing the multi-head self-
attention/cross-attention module of the last transformer
layer in the spatial encoder and temporal encoder, respec-
tively. The output of our model highly depends on the high-
lighted regions. In Fig. 8, a lipstick-shape sticker is added
in the middle of the scene with moving animals. Although
our model is not trained with explicit segmentation super-
vision, our model learns to focus on the sticker and ignore
the background changes when both the sticker and the back-
ground scene are moving. The temporal attention values of
the eight frames are similar to each other, as the sticker ap-
pears on all the frames. More results can be seen in the
supplementary material.
6. Conclusion
We introduce the first large-scale editing components
dataset with 618, 800 rendered videos covering 6 major
types of editing components, which can benefit related
downstream tasks.
We further propose a novel embed-
ding guidance architecture and a specifically designed con-
trastive loss for editing component representation learn-
ing. It achieves state-of-the-art performance on both editing
components retrieval and a major downstream task, i.e. tran-
sition recommendation. The user study also demonstrates
that the learned embedding distribution of our model is bet-
ter than that of existing methods.
One limitation is that our current model uses low frames
per second (FPS), which cannot handle extremely fast mo-
tion or appearance change. In addition, some editing com-
ponents may have very small changes on the raw videos
which is very challenging for our model to recognize with-
out raw video as input. How to efficiently take advantage of
the raw videos is worth exploring in the future.
With the rapid growth of video-sharing platforms, edited
videos have become one of the major data sources on the
Internet. This work serves as a solid step toward under-
standing video editing for better recommendation, security,
etc. The authors do not foresee any negative social impact.
References
[1] https://www.capcut.com/. 3
[2] Anurag Arnab, Mostafa Dehghani, Georg Heigold, Chen
Sun, Mario Luˇci´c, and Cordelia Schmid.
Vivit: A video
vision transformer. In Proceedings of the IEEE/CVF inter-
national conference on computer vision, pages 6836–6846,
2021. 2
[3] Nicolas Carion, Francisco Massa, Gabriel Synnaeve, Nicolas
Usunier, Alexander Kirillov, and Sergey Zagoruyko. End-to-
end object detection with transformers. In European confer-
ence on computer vision, pages 213–229. Springer, 2020. 5
[4] Duygu Ceylan, Chun-Hao P Huang, and Niloy J Mitra.
Pix2video: Video editing using image diffusion. In Proceed-
ings of the IEEE/CVF International Conference on Com-
puter Vision, pages 23206–23217, 2023. 2
[5] Xinlei Chen and Kaiming He. Exploring simple siamese rep-
resentation learning. In Proceedings of the IEEE/CVF con-
ference on computer vision and pattern recognition, pages
15750–15758, 2021. 2
[6] Jia Deng, Wei Dong, Richard Socher, Li-Jia Li, Kai Li,
and Li Fei-Fei. Imagenet: A large-scale hierarchical image
database. In 2009 IEEE conference on computer vision and
pattern recognition, pages 248–255. Ieee, 2009. 3
[7] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina
Toutanova.
Bert:
Pre-training of deep bidirectional
transformers for language understanding.
arXiv preprint
arXiv:1810.04805, 2018. 5
[8] Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov,
Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner,
9


## Page 10


Mostafa Dehghani, Matthias Minderer, Georg Heigold, Syl-
vain Gelly, et al. An image is worth 16x16 words: Trans-
formers for image recognition at scale. In International Con-
ference on Learning Representations, 2020. 4
[9] Christoph Feichtenhofer, Haoqi Fan, Jitendra Malik, and
Kaiming He. Slowfast networks for video recognition. In
Proceedings of the IEEE/CVF international conference on
computer vision, pages 6202–6211, 2019. 1, 2
[10] Christoph Feichtenhofer, Haoqi Fan, Bo Xiong, Ross Gir-
shick, and Kaiming He. A large-scale study on unsupervised
spatiotemporal representation learning.
In Proceedings of
the IEEE/CVF Conference on Computer Vision and Pattern
Recognition, pages 3299–3309, 2021. 2
[11] Nathan Frey, Peggy Chi, Weilong Yang, and Irfan Essa. Au-
tomatic non-linear video editing transfer.
arXiv preprint
arXiv:2105.06988, 2021. 2
[12] Ian Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing
Xu, David Warde-Farley, Sherjil Ozair, Aaron Courville, and
Yoshua Bengio. Generative adversarial networks. Commu-
nications of the ACM, 63(11):139–144, 2020. 2
[13] Kaiming He, Haoqi Fan, Yuxin Wu, Saining Xie, and Ross
Girshick. Momentum contrast for unsupervised visual rep-
resentation learning. In Proceedings of the IEEE/CVF con-
ference on computer vision and pattern recognition, pages
9729–9738, 2020. 2, 4, 5, 6
[14] Kaiming He, Xinlei Chen, Saining Xie, Yanghao Li, Piotr
Doll´ar, and Ross Girshick. Masked autoencoders are scalable
vision learners. In Proceedings of the IEEE/CVF conference
on computer vision and pattern recognition, pages 16000–
16009, 2022. 1, 2, 6
[15] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising dif-
fusion probabilistic models. Advances in neural information
processing systems, 33:6840–6851, 2020. 2
[16] Will Kay, Joao Carreira, Karen Simonyan, Brian Zhang,
Chloe Hillier, Sudheendra Vijayanarasimhan, Fabio Viola,
Tim Green, Trevor Back, Paul Natsev, et al. The kinetics hu-
man action video dataset. arXiv preprint arXiv:1705.06950,
2017. 2
[17] Diederik P Kingma and Jimmy Ba. Adam: A method for
stochastic optimization.
arXiv preprint arXiv:1412.6980,
2014. 5
[18] Sharath Koorathota, Patrick Adelman, Kelly Cotton, and
Paul Sajda. Editing like humans: a contextual, multimodal
framework for automated video editing. In Proceedings of
the IEEE/CVF Conference on Computer Vision and Pattern
Recognition, pages 1701–1709, 2021. 2
[19] Jun Hao Liew, Hanshu Yan, Jianfeng Zhang, Zhongcong Xu,
and Jiashi Feng. Magicedit: High-fidelity and temporally
coherent video editing.
arXiv preprint arXiv:2308.14749,
2023. 2
[20] Ilya Loshchilov and Frank Hutter. Sgdr: Stochastic gradient
descent with warm restarts. In International Conference on
Learning Representations, 2016. 5
[21] Aaron van den Oord, Yazhe Li, and Oriol Vinyals. Repre-
sentation learning with contrastive predictive coding. arXiv
preprint arXiv:1807.03748, 2018. 2, 4, 5
[22] Tian Pan, Yibing Song, Tianyu Yang, Wenhao Jiang, and Wei
Liu.
Videomoco: Contrastive video representation learn-
ing with temporally adversarial examples. In Proceedings
of the IEEE/CVF conference on computer vision and pattern
recognition, pages 11205–11214, 2021. 2, 6
[23] Adam Paszke, Sam Gross, Francisco Massa, Adam Lerer,
James Bradbury, Gregory Chanan, Trevor Killeen, Zeming
Lin, Natalia Gimelshein, Luca Antiga, et al. Pytorch: An im-
perative style, high-performance deep learning library. Ad-
vances in neural information processing systems, 32, 2019.
5
[24] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya
Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry,
Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learning
transferable visual models from natural language supervi-
sion. In International conference on machine learning, pages
8748–8763. PMLR, 2021. 5
[25] Robin Rombach, Andreas Blattmann, Dominik Lorenz,
Patrick Esser, and Bj¨orn Ommer.
High-resolution image
synthesis with latent diffusion models.
In Proceedings of
the IEEE/CVF conference on computer vision and pattern
recognition, pages 10684–10695, 2022. 2
[26] Xindi Shang, Tongwei Ren, Jingfan Guo, Hanwang Zhang,
and Tat-Seng Chua. Video visual relation detection. In ACM
International Conference on Multimedia, Mountain View,
CA USA, 2017. 3
[27] Yaojie Shen, Libo Zhang, Kai Xu, and Xiaojie Jin. Autotran-
sition: Learning to recommend video transition effects. In
European Conference on Computer Vision, pages 285–300.
Springer, 2022. 2, 3, 4, 8
[28] Zhan Tong, Yibing Song, Jue Wang, and Limin Wang.
Videomae: Masked autoencoders are data-efficient learners
for self-supervised video pre-training. Advances in neural
information processing systems, 35:10078–10093, 2022. 2,
6
[29] Du Tran, Heng Wang, Lorenzo Torresani, and Matt Feis-
zli.
Video classification with channel-separated convolu-
tional networks.
In Proceedings of the IEEE/CVF inter-
national conference on computer vision, pages 5552–5561,
2019. 2
[30] Laurens Van der Maaten and Geoffrey Hinton. Visualizing
data using t-sne. Journal of machine learning research, 9
(11), 2008. 7
[31] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszko-
reit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia
Polosukhin. Attention is all you need. Advances in neural
information processing systems, 30, 2017. 4, 5
[32] Limin Wang, Bingkun Huang, Zhiyu Zhao, Zhan Tong, Yi-
nan He, Yi Wang, Yali Wang, and Yu Qiao. Videomae v2:
Scaling video masked autoencoders with dual masking. In
Proceedings of the IEEE/CVF Conference on Computer Vi-
sion and Pattern Recognition, pages 14549–14560, 2023. 2
[33] Chen Wei, Haoqi Fan, Saining Xie, Chao-Yuan Wu, Alan
Yuille, and Christoph Feichtenhofer. Masked feature predic-
tion for self-supervised visual pre-training. In Proceedings of
the IEEE/CVF Conference on Computer Vision and Pattern
Recognition, pages 14668–14678, 2022. 2
10


## Page 11


[34] Chao-Yuan Wu, R Manmatha, Alexander J Smola, and
Philipp Krahenbuhl. Sampling matters in deep embedding
learning. In Proceedings of the IEEE international confer-
ence on computer vision, pages 2840–2848, 2017. 5
[35] Shuai Yang, Yifan Zhou, Ziwei Liu, and Chen Change
Loy. Rerender a video: Zero-shot text-guided video-to-video
translation. arXiv preprint arXiv:2306.07954, 2023. 2
[36] He Zhang, Jianming Zhang, Federico Perazzi, Zhe Lin, and
Vishal M Patel. Deep image compositing. In Proceedings
of the IEEE/CVF winter conference on applications of com-
puter vision, pages 365–374, 2021. 3
11
