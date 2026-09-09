# Bounding Box-Guided Diffusion for Synthesizing

*Source PDF: `Bounding Box-Guided Diffusion for Synthesizing.pdf`*

*Total Pages: 9*

---


## Page 1


Bounding Box-Guided Diffusion for Synthesizing
Industrial Images and Segmentation Maps
Emanuele Caruso*, Alessandro Simoni*, Francesco Pelosin*
Covision Lab
Brixen, South Tyrol, Italy
name.surname@covisionlab.com
Abstract
Synthetic dataset generation in Computer Vision, particu-
larly for industrial applications, is still underexplored. In-
dustrial defect segmentation, for instance, requires highly
accurate labels, yet acquiring such data is costly and time-
consuming. To address this challenge, we propose a novel
diffusion-based pipeline for generating high-fidelity indus-
trial datasets with minimal supervision. Our approach con-
ditions the diffusion model on enriched bounding box rep-
resentations to produce precise segmentation masks, en-
suring realistic and accurately localized defect synthesis.
Compared to existing layout-conditioned generative meth-
ods, our approach improves defect consistency and spa-
tial accuracy.
We introduce two quantitative metrics to
evaluate the effectiveness of our method and assess its im-
pact on a downstream segmentation task trained on real
and synthetic data. Our results demonstrate that diffusion-
based synthesis can bridge the gap between artificial and
real-world industrial data, fostering more reliable and
cost-efficient segmentation models.
The code is publicly
available at https://github.com/covisionlab/
diffusion_labeling.
1. Introduction
Dataset synthesis has gained significant importance in re-
cent years, particularly within the Natural Language Pro-
cessing (NLP) community, where we witnessed major im-
provements in both academic and industrial applications
[3, 5, 37]. These methods have proven especially valuable
in scenarios where collecting and annotating real-world data
is expensive or impractical.
In contrast, dataset synthesis in Computer Vision re-
mains an emerging field and its usage is still under study
[8, 9]. Its potential to reduce labeling costs and mitigate
data scarcity constitute an appealing property for the deep
*Equal contribution.
learning paradigm. Despite its potential, the field remains
relatively underexplored compared to its NLP counterpart.
This is particularly true in domains where acquiring precise
labeled data is both costly and time-consuming, such as in-
dustrial inspection, medical imaging, and remote sensing.
In these domains, even small inaccuracies in annotation can
significantly impact model performance, making synthetic
data generation a compelling alternative.
Most of the recent research in synthetic data for vision
has focused on text-to-image generation [20, 33, 39], lever-
aging generative models to create realistic visuals from tex-
tual descriptions. While these advancements have paved
the way for creative applications and content generation,
their direct applicability to real-world industrial settings re-
mains limited. Industrial datasets, in particular, suffer from
challenges such as class imbalances, labeling inconsisten-
cies and high quality standards. These issues necessitate
the development of tailored synthesis techniques capable of
generating high-fidelity data hopefully with minimal man-
ual intervention.
A critical challenge is the automatic creation of indus-
trial dataset samples, where balancing efficiency with accu-
racy is difficult. Fully automated synthesis risks generating
unrealistic or irrelevant samples, reducing the utility of the
data. On the other hand, manual supervision, while improv-
ing accuracy, is often infeasible due to time and cost con-
straints — especially when dealing with complex imaging
systems that go beyond human perception such as infrared
imaging [36]. Industrial defect segmentation exemplifies
this challenge, as it demands highly precise annotations to
train reliable models.
To address these limitations, we propose a novel pipeline
for generating realistic synthetic samples with cheap su-
pervision. Our approach leverages diffusion models condi-
tioned on human-provided bounding boxes to produce pre-
cise segmentation masks. By doing so, we unlock the gen-
eration of high-quality industrial datasets while exploiting
human domain expertise but with a significant reduction in
the burden of manual annotation.
arXiv:2505.03623v2  [cs.CV]  27 Jan 2026


## Page 2


t = T
t = 0
Reverse diffusion process
Condition
Figure 1. Overview of the proposed diffusion-based approach that generates both RGB and segmentation map in industrial setting.
In industrial settings, diffusion models have been em-
ployed for data synthesis only in classification tasks [28].
However, to the best of our knowledge and according to
a recent review [41], no existing work has addressed the
challenge of synthetic dataset generation for semantic seg-
mentation, generating high quality labels from inexpensive
annotation.
We present a diffusion-based approach, depicted in Fig-
ure 1, that generates RGB images and semantic maps lever-
aging an enriched bounding box representation as condi-
tioning. We compare it with a modified state-of-the-art ap-
proach on layout-conditioned generation [40]. Our baseline
exhibits superior consistency in generating defects within
the provided bounding box annotations, making it prefer-
able over existing generative pipelines. In this regard, we
propose two metrics to quantitatively evaluate the obtained
results. Ultimately, we provide some experiments showing
the quality of the generated data by monitoring the perfor-
mance of a downstream segmentation task trained on both
real and synthetic data. Thus, we shed light on the potential
of diffusion-based synthesis in bridging the gap between ar-
tificial and real-world industrial data, fostering more accu-
rate and efficient computer vision models for segmentation.
To sum up, our main contributions are as follows:
• We introduce a novel synthetic data generation pipeline
that leverages diffusion models conditioned on human-
provided bounding boxes to generate high-fidelity indus-
trial dataset samples.
• The proposed approach, thanks to an enriched bounding
box representation, ensures that the generated defects re-
main both realistic and accurately localized within the
bounding box boundary, enhancing segmentation consis-
tency.
• By reducing the reliance on manual labeling, our method
significantly lowers the cost and time required for curat-
ing industrial datasets while maintaining high annotation
quality.
• We propose two metrics and evaluate our approach
against a state-of-the-art conditioned diffusion pipeline,
demonstrating competitive performance and improved
control over defect placement.
• Our findings highlight the potential of diffusion-based
dataset synthesis to improve industrial defect segmenta-
tion models, unlocking the development of more robust
computer vision solutions in real-world settings.
2. Related Works
Synthetic data generation has been explored through vari-
ous methodologies, each catering to specific domains and
applications.
3D Game Engines. One prevalent approach leverages
3D game engines such as Unreal Engine [1], where meticu-
lously crafted scenes or objects serve as high-fidelity prox-
ies of reality. This method has been widely adopted, lead-
ing to the creation of extensive datasets and comprehensive
frameworks [7, 25, 27], which have subsequently facilitated
advancements in novel methodologies [32, 42].
GAN / Diffusion. Another powerful paradigm involves
neural generative models. Techniques such as GANs [10]
and diffusion models [15] have demonstrated remarkable
efficacy in producing high-fidelity synthetic data.
These
models have found widespread applications, ranging from
medical imaging [6, 11, 31], self-driving car research [22,
24], privacy preservation [17] and finally in robotics, where
has been investigated for pose estimation, as discussed in
[29].
Foundation Models. Recently, foundation models have
also been explored for synthetic data generation. Notably,
COSMOs [23] facilitates the creation of entire synthetic
video sequences, while large vision-text models have been
widely utilized for generative applications [20, 33, 39].
Conditioned Generation. Our pipeline not only gen-
erates RGB images but also their correspondent labels. A
related study [35], proposes a method for end-to-end RGB
and label generation for satellite data. While their approach
is purely generative, ours allows human intervention, grant-
ing users the flexibility to place annotations as needed. This
distinction enhances the control and accuracy of label gen-
eration.
Additionally, we consider [40], a generative approach
that conditions data synthesis on bounding boxes. We will
compare our method with this approach in later sections to
provide a comprehensive evaluation of our proposed frame-
work.


## Page 3


Condition creation
Low-cost annotation
Diffusion model
Synthetic data
Figure 2. An overview of the proposed method: the user produces low-cost bounding box annotations which are then converted in two
representations (BASD and C-BASD). Later, these encodings, are fed into the diffusion to condition the generation of both high quality
RGB and segmentation masks of wood defects.
3. Method
In this section, we describe the proposed method shown in
Figure 2.
3.1. Problem statement
In this work, we address the challenging task of semantic
segmentation in an industrial setting. Since the lack of an-
notated data is very common, a way to tackle this problem
is to augment the annotations with synthetic samples. Thus,
we aim to adapt a conditional diffusion-based pipeline to
denoise both an RGB image and its segmentation map as
annotation.
Formally, we define a dataset D = {(In, Sn, Bn) | n =
1, . . . , N} where:
• IH×W ×3
n
is an RGB image,
• SH×W
n
is the corresponding segmentation map composed
of the discrete pixels values cij ∈{1, 2, 3, . . . , C} where
C is the total number of classes,
• Bn = {bk : (c, imin, jmin, imax, jmax), k = 1, . . . , K}
is a tuple that identifies the class of the object and its
bounding box location as the top left (imin, jmin) and
bottom right (imax, jmax) corners.
Our method applies the diffusion process to the couple
(In, Sn) conditioned on Bn.
In the following, we thor-
oughly describe how we preprocess the inputs and the train-
ing pipeline of the proposed method.
3.2. Data preprocessing
The first step is to process the segmentation map Sn and the
bounding boxes Bn to allow the diffusion process to work
with continuous values.
Segmentation map. Since the goal is to generate syn-
thetic samples according to the joint probability p(In, Sn),
we need to make sure that these data are in the same con-
tinuous space R. Drawing inspiration from [4, 35], we con-
vert the segmentation map into an analog bit representation.
Formally, the pixelwise discrete segmentation values cij are
mapped into a binary code defined as
bin : {1, 2, 3 . . . , C} →{0, 1}⌈log2 C⌉
(1)
After this encoding, the segmentation map dimension is
H × W × ⌈log2 C⌉. As proven by previous works [4],
this representation is more effective than one-hot encoding
which is also less efficient in terms of number of channels
in the presence of a high number of classes C. After the
binary encoding, a normalization is applied to change the
range from [0, 1] to [−1, 1] which is the same of the RGB
image In.
Bounding box. To condition the generation of the syn-
thetic couple (ˆIn, ˆSn) on the bounding boxes, we create an
enriched representation of Bn that encodes both spatial and
class information. The spatial information is captured in
terms of pixelwise encoding. Thus, we compute a Bound-
ing Box-Aware Signed Distance (BASD) map M d
n that as-
signs to each pixel (i, j) the minimum distance to the near-
est bounding box boundary point. The distance value is pos-
itive inside a bounding box and negative outside. Moreover,
a Bounding-Box Class (C-BASD) map M c
n is computed ac-
cordingly assigning to each positive value the correspond-
ing class of the boundary point. We formally define the
computation of M d
n and M c
n in Algorithm 1 and a visual-
ization of the resulting maps can be seen in Figure 2.
Before concatenating these two representation maps to
the couple (In, Sn), the class map M c
n is encoded with the
previously introduced analog bit paradigm obtaining an out-
put dimension of H ×W ×⌈log2 C⌉. Our encoding assigns
a single class per pixel but still handles overlapping bound-
ing boxes. When two boxes overlap, the class map forms
a structured pattern reflecting the overlap location instead
of arbitrarily selecting one class. This allows the network
to learn spatial relationships without needing explicit multi-
label assignments, which a pure analog bit encoding can not
achieve.


## Page 4


Figure 3. Some samples of the Wood Defect Detection [18] with the semantic segmentation labels. The wood defects are the following:
knot (blue), crack (red), quartzite (green), resin (yellow), marrow (magenta).
Algorithm 1 M d
n and M c
n computation. Comments in blue.
Require: Bounding boxes Bn
Ensure: M d
n of size (H, W), M c
n of size (H, W)
1: Initialize M d
n ←+∞for all pixels pij
2: Initialize M c
n ←0 for all pixels pij
3: for each bk ∈Bn with class c do
4:
Compute boundary pixels of bk:
5:
β ←Boundary(bk)
6:
for each pixel pij do
7:
Compute distance to the closest boundary point:
8:
dβ ←
min
(iβ,jβ)∈β
p
(i −iβ)2 + (j −jβ)2
9:
dβ ←dβ ∗InOutSign(pij, bk)
10:
Update M d
n and M c
n:
11:
if |dβn| < |M d
n(pij)| then
12:
M d
n(pij) ←dβ
13:
M c
n(pij) ←c
3.3. Conditioned Diffusion Model
To synthesize realistic and structurally consistent images,
we condition the denoising diffusion process on our en-
riched bounding box representation. A UNet architecture
takes as input (x0, (M d
n, M c
n)) where x0 = (In, Sn). The
output is the couple (ˆIn, ˆSn) comprising of an RGB image
plus its segmentation map with dimension H × W × 3 +
⌈log2 C⌉.
Given a clean sample x0, the forward diffusion process
gradually adds Gaussian noise:
q(xt | x0) = N(xt; √αt x0, (1 −αt)I),
(2)
where αt is the noise scheduling coefficient. The reverse
process learns to reconstruct x0 while incorporating the
structural constraints from the conditioning (M d
n, M c
n):
pθ(xt−1 | xt, M d
n, M c
n) =
N
 xt−1; µθ(xt, t, M d
n, M c
n), σ2
t I

.
(3)
where µθ(xt, t, M d
n, M c
n) is the predicted denoised estimate
and σt is the variance of the noise distribution.
The diffusion model is trained by minimizing the noise
prediction loss:
Ex0,M d
n,M cn,t,ϵ

∥ϵ −ϵθ(xt, t, M d
n, M c
n)∥2
,
(4)
with ϵ ∼N(0, I) representing the injected Gaussian noise.
This formulation ensures that the generated samples adhere
to both the semantic structure encoded in the segmentation
and the spatial constraints provided as bounding box condi-
tioning.
4. Experiments
In this section, we discuss the implementation details and
the industrial dataset we used for our experiments. Finally, a
thorough comparison between our approach and a state-of-
the-art conditional diffusion model [40] is assessed in terms
of quality and consistency.
4.1. Experimental setting
Diffusion model.
The proposed method follows the
DDPM [14] paradigm with a UNet [26] architecture trained
from scratch. We modified the input and output channels
accordingly to support our bounding box encoding repre-
sentation and the denoising of the segmentation map. Both
during training and testing the number of denoising itera-
tions were set to 1000. We trained for 300 epochs using
AdamW [21] as optimizer with learning rate 1e−5 and batch
size 8 on two Nvidia RTX 4090. The total training time is
approximately 1 day.
Downstream task. For the semantic segmentation down-
stream task we emploied a UNet architecture with a ResNet-
18 [12] backbone.
We used a single network for each
segmentation class to avoid class balancing problems and
concentrate on the synthetic data assessment. The training
lasted 100 epochs using AdamW as optimizer with learning
rate 1e−5 and batch size 64 on a single Nvidia RTX 4090.


## Page 5


FID ↓
KID ↓
LPIPS ↓
Data
@2048
@768
@192
@64
@2048
@768
@192
@64
AlexNet
VGG-16
SqueezeNet
Synth [40]
40.94
0.25
24.04
6.77
40.94
8.07
19 × 103
10 × 103
0.35
0.49
0.26
Synth Ours
45.47
0.30
14.49
3.09
45.46
8.73
10 × 103
3.6 × 103
0.28
0.43
0.21
Table 1. Assessment of generation quality. We report the FID and KID computed at different levels of the InceptionV3 [34] network, and
the LPIPS computed with several backbones AlexNet [19], SqueezeNet [16] and VGG-16 [30].
SAE (%) ↓
Method
Knot
Crack
Quartzite
Resin
Marrow
Avg
Layout Diffusion [40]
40.03
83.82
61.00
85.59
54.88
46.77
Ours
5.53
4.57
3.19
4.82
3.64
4.99
Table 2. Comparison between our method and [40] in terms of
Segmentation Alignment Error. The Avg is computed over all pix-
els.
Dataset. Since we focus on the industrial setting, we se-
lected the Wood Defect Detection [18] dataset, a seman-
tic segmentation and object detection collection of data for
the wood manufacturing industry. It contains 20276 images
with semantic segmentation and bounding box annotations
of 10 different classes of wood defects. In our experiments,
we decided to aggregate the 4 classes of knots and avoid-
ing the classes of blue stain and overgrown that are un-
derrepresented. Thus, we obtained a dataset comprising of
20107 images with a total of 5 defect classes (knot, crack,
quartzite, resin, marrow).
Moreover, we split the dataset into three subsets: 70%
for training the diffusion model, 20% for training the seg-
mentation model, and 10% as a fixed real test set. Addi-
tionally, the bounding box annotations from the 20% real
split are used to generate synthetic data for evaluating the
semantic segmentation task. Figure 3 illustrates some sam-
ples from the original dataset.
4.2. Data synthesis assessment
To assess the quality of synthetic data, we compare our ap-
proach with the current state-of-the-art layout-conditional
diffusion model [40], utilizing its original code implemen-
tation and adapting it to take non-squared images. Specifi-
cally, we focus on evaluating the consistency between the
generated defects and their corresponding bounding box
constraints. To quantify this relationship, we introduce two
metrics, the Segmentation Alignment Error (SAE) and the
Empty Bounding-Box Rate (EBR).
Segmentation Alignment Error (SAE). With this mea-
sure we quantify how many generated defect pixels fall out-
side their designated bounding boxes, indicating misalign-
ment between the generated defects and their constraints.
Formally, let:
• ˆP be all the generated pixels of segmented defects,
• ˆPout be the generated pixels that fall outside the bounding
EBR (%) ↓
Method
Knot
Crack
Quartzite
Resin
Marrow
Avg
Layout Diffusion [40]
13.43
69.16
48.76
80.15
28.44
26.00
Ours
0.86
2.41
4.98
2.22
0.89
5.51
Table 3. Comparison between our method and [40] in terms of
Empty Bounding-Box Rate. The Avg is computed over all bound-
ing boxes.
boxes.
Thus, we define the metric as follows:
SAE =
ˆPout
ˆP
(5)
where a lower value indicates that the model is more con-
sistent with the generation condition.
As shown in Table 2, the method proposed in [40]
struggles to maintain defect placement within the bound-
ing boxes, resulting in a very high mean SAE of 46.77%
across all the defects. In contrast, our approach, leverag-
ing a dual bounding box encoding strategy (BASD and C-
BASD), significantly improves alignment, with only 4.99%
of generated pixels falling outside the given regions.
Empty Bounding-Box Rate (EBR). To assess whether
the generated defects correctly fall within their designated
bounding boxes, we define the Empty Bounding-Box Rate
(EBR). This metric quantifies how many bounding boxes
remain empty, meaning no synthetic pixels are generated
inside them. Formally, let:
• Ball = {bk | bk ∈Bn , n = 1, . . . , N} be the set of all
bounding boxes,
• Bmiss = {bk | bk ∈Ball , G ∩bk = ∅} be the subset of
bounding boxes that contain no generated pixels.
Thus, we define the metric as follows:
EBR = |Bmiss|
|Ball|
(6)
where higher values indicate that a larger number of bound-
ing boxes have been missed during generation, signifying a
poorer retrieval of the provided conditioning.
As reported in Table 3, the EBR metric shows the superi-
ority of our proposal in retrieval abilities by a large margin.
Specifically, our average EBR lies around 5.51% on the to-
tal amount of bounding boxes and surpasses by more than
20% points the competitor [40].


## Page 6


Layout Diffusion
Ours
Figure 4. Qualitative comparison between our method and Layout Diffusion [40]. Each method shows the generated RGB image with
respect to the bounding box condition - the same for both methods - and the overlapped defect segmentation map. The wood defects are
the following: knot (blue), crack (red), quartzite (green), resin (yellow), marrow (magenta).


## Page 7


F1 (%) ↑
Train data
Knot
Crack
Quartzite
Resin
Marrow
Avg
Real
78.56
48.80
24.49
45.00
65.40
52.45
Synth [40]
72.15
8.20
21.03
18.01
58.04
35.49
Synth Ours
76.57
45.56
12.82
32.71
58.18
45.17
Real+Synth [40]
78.44
46.71
27.01
43.85
71.09
53.42
Real+Synth Ours
79.48
50.38
25.85
46.29
66.11
53.62
Table 4. Downstream task assessment in terms of F1 score using
real, synthetic and real+synthetic data during training.
Visual sample quality. To further analyze the quality
of the generated synthetic images, we report the Fr´echet In-
ception Distance (FID) [13], the Kernel Inception Distance
(KID) [2] and the LPIPS [38] metrics. As can be observed
in Table 1, our method tends to have better performance on
low-level features with regard to the FID and KID metrics,
meaning that the local perception of the details is better than
the competitor. Additionally, our method outperforms [40]
across all tested backbones in terms of LPIPS metric, con-
firming that the generated images exhibit higher perceptual
realism across different network architectures.
Qualitative results. To further illustrate this compar-
ison, Figure 4 depicts qualitative examples. Moreover, the
results demonstrate that [40] not only fails to confine defects
within the bounding boxes but also occasionally generates
wrong segmentation labels.
4.3. Downstream task evaluation
To evaluate the effectiveness of our synthetic data, we con-
duct a semantic segmentation experiment using a UNet ar-
chitecture trained on different data configurations.
Starting from the 20% split, we use the original bound-
ing box annotations as guidance to generate couples of im-
age and label. We do so for both methods, ours and [40].
We then use this synthetic split to train the segmentation
pipeline. Moreover, to ensure a fair comparison between
approaches, we discard synthetic pixel labels generated out-
side the bounding boxes conditioning. This prevents even-
tual generalization of the downstream segmentation given
by extra synthetic labels generated without explicit condi-
tioning.
Table 4 presents the F1 scores computed on the 10%
real test split, where we compare models trained on real
data, synthetic data, and a combination of both. Notably,
when training on synthetic data alone, our approach sur-
passes [40] by an impressive 10%, demonstrating its ability
to generate more valid training samples. This highlights the
superior quality and consistency of our synthetic segmenta-
tion maps, which provide a more reliable learning signal for
the segmentation task.
When incorporating real data into the training process,
the performance gap between the two methods narrows, as
real samples provide a strong baseline. However, even in
this hybrid setting, leveraging our synthetic data leads to
the best overall F1 score, achieving a +1.17% improvement
over using only real data. This result underscores the effec-
tiveness of our method in complementing real-world anno-
tations, reinforcing its practical utility in industrial applica-
tions where obtaining high-quality segmentation labels can
be costly and time-consuming.
5. Conclusion
In this work, we are the first [41] to study the problem of
data synthesis for semantic segmentation in industrial set-
tings, where quality and precision is of importance. We de-
vised a pipeline to generate synthetic RGB data and its seg-
mentation label counterpart at the same time, starting from
bounding box conditioning. This allows to decrease signifi-
cantly the labeling costs while preserving the quality of the
segmentation maps.
We validated the performances of our method by com-
paring our proposal with the current state-of-the art method-
ology adapted for the setting. We also assessed the qual-
ity of our generation through a downstream task, training a
UNet with a combination of real and synthetic data.
The experiments suggest that our proposal is robust to
spatial consistency generation, improving the performance
of the downstream segmentation task.
We also introduced dedicated metrics useful for the com-
munity to assess the correctness of layout-conditioned data
generation.
References
[1] Unreal Engine. https://www.unrealengine.com. 2
[2] Mikołaj Bi´nkowski, Dougal J. Sutherland, Michael Arbel,
and Arthur Gretton. Demystifying MMD GANs. In Inter-
national Conference on Learning Representations (ICLR),
2018. 7
[3] Xin Chan, Xiaoyang Wang, Dian Yu, Haitao Mi, and Dong
Yu. Scaling synthetic data creation with 1,000,000,000 per-
sonas. arXiv preprint arXiv:2406.20094, 2024. 1
[4] Ting Chen, Ruixiang Zhang, and Geoffrey E. Hinton. Analog
bits: Generating discrete data using diffusion models with
self-conditioning. In International Conference on Learning
Representations (ICLR), 2023. 3
[5] Zixiang Chen, Yihe Deng, Huizhuo Yuan, Kaixuan Ji, and
Quanquan Gu. Self-play fine-tuning converts weak language
models to strong language models. In International Confer-
ence on Machine Learning (ICML), 2024. 1
[6] Virginia Fernandez, Walter Hugo Lopez Pinaya, Pedro
Borges, Petru-Daniel Tudosiu, Mark S. Graham, Tom Ver-
cauteren, and M. Jorge Cardoso. Can segmentation models
be trained with fully synthetically generated data? In Sim-
ulation and Synthesis in Medical Imaging (MICCAI Work-
shops), 2022. 2
[7] Adrien Gaidon, Qiao Wang, Yohann Cabon, and Eleonora
Vig. Virtual worlds as proxy for multi-object tracking anal-


## Page 8


ysis. In IEEE Conference on Computer Vision and Pattern
Recognition (CVPR), 2016. 2
[8] Scott Geng, Ranjay Krishna, and Pang Wei Koh. Training
with real instead of synthetic generated images still performs
better.
In Synthetic Data for Computer Vision Workshop
(CVPRW), 2024. 1
[9] Magnus Kaufmann Gjerde, Filip Slez´ak, Joakim Bruslund
Haurum, and Thomas B Moeslund. From nerf to 3dgs: A
leap in stereo dataset quality?
In Synthetic Data for Com-
puter Vision Workshop (CVPRW), 2024. 1
[10] Ian J. Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing
Xu, David Warde-Farley, Sherjil Ozair, Aaron C. Courville,
and Yoshua Bengio. Generative adversarial networks. Com-
munications ACM, 2020. 2
[11] Pengfei Guo, Can Zhao, Dong Yang, Ziyue Xu, Vish-
wesh Nath, Yucheng Tang, Benjamin Simon, Mason Belue,
Stephanie Harmon, Baris Turkbey, et al. Maisi: Medical ai
for synthetic imaging. IEEE/CVF Winter Conference on Ap-
plications of Computer Vision (WACV), 2025. 2
[12] Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun.
Deep residual learning for image recognition.
In IEEE
Conference on Computer Vision and Pattern Recognition
(CVPR), 2016. 4
[13] Martin Heusel, Hubert Ramsauer, Thomas Unterthiner,
Bernhard Nessler, and Sepp Hochreiter. Gans trained by a
two time-scale update rule converge to a local nash equilib-
rium. Advances in Neural Information Processing Systems
(NIPS), 2017. 7
[14] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising diffu-
sion probabilistic models. Advances in Neural Information
Processing Systems (NIPS), 33, 2020. 4
[15] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising dif-
fusion probabilistic models. In Advances in Neural Informa-
tion Processing Systems (NIPS), 2020. 2
[16] Forrest N Iandola, Song Han, Matthew W Moskewicz,
Khalid Ashraf,
William J Dally,
and Kurt Keutzer.
Squeezenet:
Alexnet-level accuracy with 50x fewer pa-
rameters and¡ 0.5 mb model size.
arXiv preprint
arXiv:1602.07360, 2016. 5
[17] Marvin Klemp, Kevin R¨osch, Royden Wagner, Jannik Quehl,
and Martin Lauer. LDFA: latent diffusion face anonymiza-
tion for self-driving applications. In IEEE Conference on
Computer Vision and Pattern Recognition (CVPR), 2023. 2
[18] P Kodytek, A Bodzas, and P Bilik.
A large-scale image
dataset of wood surface defects for automated vision-based
quality control processes. F1000Research, 2022. 4, 5
[19] Alex Krizhevsky, Ilya Sutskever, and Geoffrey E Hinton.
Imagenet classification with deep convolutional neural net-
works. In Advances in Neural Information Processing Sys-
tems (NIPS), 2012. 5
[20] Baiqi Li, Zhiqiu Lin, Deepak Pathak, Jiayao Emily Li,
Xide Xia, Graham Neubig, Pengchuan Zhang, and Deva Ra-
manan. Genai-bench: A holistic benchmark for composi-
tional text-to-visual generation. In Synthetic Data for Com-
puter Vision Workshop (CVPRW), 2024. 1, 2
[21] Ilya Loshchilov and Frank Hutter.
Decoupled weight de-
cay regularization. In International Conference on Learning
Representations (ICLR), 2019. 4
[22] Quang Nguyen, Truong Vu, Anh Tran, and Khoi Nguyen.
Dataset diffusion: Diffusion-based synthetic data generation
for pixel-level semantic segmentation. In Advances in Neural
Information Processing Systems (NIPS), 2023. 2
[23] NVIDIA.
Cosmos world foundation model platform for
physical ai, 2025. 2
[24] Ethan Pronovost, Meghana Reddy Ganesina, Noureldin
Hendy, Zeyu Wang, Andres Morales, Kai Wang, and Nick
Roy. Scenario diffusion: Controllable driving scenario gen-
eration with diffusion. In Advances in Neural Information
Processing Systems (NIPS), 2023. 2
[25] Alexander Raistrick, Lahav Lipson, Zeyu Ma, Lingjie Mei,
Mingzhe Wang, Yiming Zuo, Karhan Kayan, Hongyu Wen,
Beining Han, Yihan Wang, Alejandro Newell, Hei Law,
Ankit Goyal, Kaiyu Yang, and Jia Deng. Infinite photorealis-
tic worlds using procedural generation. In IEEE Conference
on Computer Vision and Pattern Recognition (CVPR), 2023.
2
[26] Olaf Ronneberger, Philipp Fischer, and Thomas Brox. U-net:
Convolutional networks for biomedical image segmentation.
In International Conference on Medical Image Computing
and Computer Assisted Intervention (MICCAI). Springer,
2015. 4
[27] German Ros, Laura Sellart, Joanna Materzynska, David
Vazquez, and Antonio M. Lopez. The synthia dataset: A
large collection of synthetic images for semantic segmen-
tation of urban scenes. In IEEE Conference on Computer
Vision and Pattern Recognition (CVPR), 2016. 2
[28] Thanyathep Sasiaowapak, Siridech Boonsang, Santhad Chu-
wongin, Teerawat Tongloy, and Pattarachai Lalitrojwong.
Generative ai for industrial applications: Synthetic dataset.
In International Conference on Information Technology and
Electrical Engineering (ICITEE), 2023. 2
[29] Alessandro Simoni, Stefano Pini, Guido Borghi, and Roberto
Vezzani. Semi-perspective decoupled heatmaps for 3d robot
pose estimation from depth maps. IEEE Robotics and Au-
tomation Letters (RAL), 2022. 2
[30] Karen Simonyan and Andrew Zisserman. Very deep con-
volutional networks for large-scale image recognition. In In-
ternational Conference on Learning Representations (ICLR),
2015. 5
[31] Youssef Skandarani, Pierre-Marc Jodoin, and Alain Lalande.
Gans for medical image synthesis: An empirical study. J.
Imaging, 2023. 2
[32] Chunyi Sun, Junlin Han, Weijian Deng, Xinlong Wang,
Zishan Qin, and Stephen Gould.
3d-gpt: Procedural 3d
modeling with large language models.
arXiv preprint
arXiv:2310.12945, 2023. 2
[33] Jiao Sun, Deqing Fu, Yushi Hu, Su Wang, Royi Rassin,
Da-Cheng Juan, Dana Alon, Charles Herrmann, Sjoerd van
Steenkiste, Ranjay Krishna, et al. Dreamsync: Aligning text-
to-image generation with image understanding feedback.
arXiv preprint arXiv:2311.17946, 2023. 1, 2
[34] Christian Szegedy, Vincent Vanhoucke, Sergey Ioffe, Jon
Shlens, and Zbigniew Wojna. Rethinking the inception ar-
chitecture for computer vision. In IEEE Conference on Com-
puter Vision and Pattern Recognition (CVPR), 2016. 5


## Page 9


[35] Aysim Toker, Marvin Eisenberger, Daniel Cremers, and
Laura Leal-Taix´e. Satsynth: Augmenting image-mask pairs
through diffusion models for aerial semantic segmentation.
In IEEE Conference on Computer Vision and Pattern Recog-
nition (CVPR), 2024. 2, 3
[36] Doan Thinh Vo, Phan Anh Duc, Nguyen Nhu Thao, and
Huong Ninh. An approach to synthesize thermal infrared
ship images. In Synthetic Data for Computer Vision Work-
shop (CVPRW), 2024. 1
[37] Yizhong Wang, Yeganeh Kordi, Swaroop Mishra, Alisa Liu,
Noah A. Smith, Daniel Khashabi, and Hannaneh Hajishirzi.
Self-instruct: Aligning language models with self-generated
instructions. In Annual Meeting of the Association for Com-
putational Linguistics (ACL), 2023. 1
[38] Richard Zhang, Phillip Isola, Alexei A Efros, Eli Shecht-
man, and Oliver Wang. The unreasonable effectiveness of
deep features as a perceptual metric. In IEEE Conference on
Computer Vision and Pattern Recognition (CVPR), 2018. 7
[39] Yasi Zhang, Peiyu Yu, and Ying Nian Wu.
Object-
conditioned energy-based model for attention map alignment
in text-to-image diffusion models.
In Synthetic Data for
Computer Vision Workshop (CVPRW), 2024. 1, 2
[40] Guangcong Zheng, Xianpan Zhou, Xuewei Li, Zhongang Qi,
Ying Shan, and Xi Li. Layoutdiffusion: Controllable diffu-
sion model for layout-to-image generation. In IEEE Confer-
ence on Computer Vision and Pattern Recognition (CVPR),
2023. 2, 4, 5, 6, 7
[41] Hans Aoyang Zhou, Dominik Wolfschl¨ager, Constanti-
nos Florides, Jonas Werheid, Hannes Behnen, Jan-Henrick
Woltersmann, Tiago C. Pinto, Marco Kemmerling, Anas
Abdelrazeq, and Robert H. Schmitt.
Generative AI in
industrial machine vision - A review.
arXiv preprint
arXiv:2408.10775, 2024. 2, 7
[42] Kaiyang Zhou, Ziwei Liu, Yu Qiao, Tao Xiang, and
Chen Change Loy. Domain generalization: A survey. IEEE
Transactions on Pattern Analysis and Machine Intelligence
(TPAMI), 2023. 2
