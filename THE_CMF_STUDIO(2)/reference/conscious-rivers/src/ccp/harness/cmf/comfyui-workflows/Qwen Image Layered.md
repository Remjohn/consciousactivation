## Qwen-Image-Layered: Towards Inherent Editability via Layer Decomposition

## Shengming Yin^1 Zekai Zhang^2 Zecheng Tang^2 Kaiyuan Gao^2

## Xiao Xu^2 Kun Yan^2 Jiahao Li^2 Yilei Chen^2 Yuxiang Chen^2

## Heung-Yeung Shum^3 Lionel M. Ni^1 Jingren Zhou^2 Junyang Lin^2 Chenfei Wu^2 *

(^1) HKUST(GZ) (^2) Alibaba (^3) HKUST
Input Image OutputLayers
Recolor Replace Revise Remove Resize Reposition
Figure 1. Qwen-Image-Layered is capable of decomposing an input image into multiple semantically disentangled RGBA layers, thereby
enabling inherent editability, where each layer can be independently manipulated without affecting other content.

## Abstract

```
Recent visual generative models often struggle with con-
sistency during image editing due to the entangled nature of
raster images, where all visual content is fused into a sin-
gle canvas. In contrast, professional design tools employ
layered representations, allowing isolated edits while pre-
serving consistency. Motivated by this, we propose Qwen-
Image-Layered, an end-to-end diffusion model that decom-
poses a single RGB image into multiple semantically disen-
tangled RGBA layers, enabling inherent editability, where
each RGBA layer can be independently manipulated with-
out affecting other content. To support variable-length de-
composition, we introduce three key components: (1) an
*Corresponding author.
```
```
RGBA-VAE to unify the latent representations of RGB and
RGBA images; (2) a VLD-MMDiT (Variable Layers De-
composition MMDiT) architecture capable of decomposing
a variable number of image layers; and (3) a Multi-stage
Training strategy to adapt a pretrained image generation
model into a multilayer image decomposer. Furthermore, to
address the scarcity of high-quality multilayer training im-
ages, we build a pipeline to extract and annotate multilayer
images from Photoshop documents (PSD). Experiments
demonstrate that our method significantly surpasses exist-
ing approaches in decomposition quality and establishes a
new paradigm for consistent image editing. Our code and
models are released on https://github.com/QwenLM/Qwen-
Image-Layered
```
# arXiv:2512.15603v1 [cs.CV] 17 Dec 2025


Figure 2. Visualization of Image-to-Multi-RGBA (I2L) on open-domain images. The leftmost column in each group shows the input
image. Qwen-Image-Layered is capable of decomposing diverse images into high-quality, semantically disentangled layers, where each
layer can be independently manipulated without affect other content.


Figure 3. Visualization of Image-to-Multi-RGBA (I2L) on images containing texts. The leftmost column in each group shows the input
image. Qwen-Image-Layered is capable of accurately decomposing both text and objects into semantically disentangled layers.


## 1. Introduction

Recent advances in visual generative models have enabled
impressive image synthesis capabilities [5, 10–12, 24, 31,
34, 41, 42]. However, in the context of image editing,
achieving precise modifications while preserving the struc-
ture and semantics of unedited regions remains a significant
challenge. This issue typically appears as semantic drift
(e.g. unintended changes to a person’s identity) and geo-
metric misalignment (e.g. shifts in object position or scale).
Existing editing approaches fail to fundamentally ad-
dress this problem. Global editing methods [4, 9, 21, 26, 39,
43, 48], which resample the entire image in the latent space
of generative models, are inherently limited by the stochas-
tic nature of probabilistic generation and thus cannot ensure
consistency in unedited regions. Meanwhile, mask-guided
local editing methods [8, 29, 35] restrict modification within
user-specified masks. However, in complex scenes, espe-
cially those involving occlusion or soft boundaries, the ac-
tual editing region is often ambiguous, thus failing to fun-
damentally solve the consistency problem.
Rather than tackling this issue purely through model de-
sign or data engineering, we argue that the core challenge
lies in the representation of images themselves. Traditional
raster images are flat and entangled: all visual content is
fused into a single canvas, with semantics and geometry
tightly coupled. Consequently, any edit inevitably prop-
agates through this entangled pixel space, leading to the
aforementioned inconsistencies.
To overcome this fundamental limitation, we advocate
for a naturally disentangled image representation. Specif-
ically, we propose representing an image as a stack of se-
mantically decomposed RGBA layers, as illustrated in the
upper part of Fig. 1. This layered structure enables inherent
editability with built-in consistency: edits are applied exclu-
sively to the target layer, physically isolating them from the
rest of the content, and thereby eliminating semantic drift
and geometric misalignment. Moreover, such a layer-wise
representation naturally supports high-fidelity elementary
operations—such as resizing, repositioning, and recoloring,
as demonstrated in the lower part of Fig. 1.
Based on this insight, we introduce Qwen-Image-
Layered, an end-to-end diffusion model that directly de-
composes a single RGB image into multiple semantically
disentangled RGBA layers. Once decomposed, each layer
can be independently manipulated while leaving all other
content exactly unchanged—enabling truly consistent im-
age editing. To support variable-length decomposition, our
image decomposer is built upon three key designs: (1)
an RGBA-VAE that establishes a shared latent space for
both RGB and RGBA images; (2) a VLD-MMDiT (Vari-
able Layers Decomposition MMDiT) architecture that en-
ables training with a variable number of layers; and (3)
a Multi-stage Training strategy that progressively adapts a

```
pretrained image generation model into an multilayer image
decomposer. Furthermore, to address the scarcity of high-
quality multilayer image data, we develop a data pipeline to
filter and annotate multilayer images from real-world Pho-
toshop documents (PSD).
We summarize our contributions as follows:
```
- We propose Qwen-Image-Layered, an end-to-end diffu-
    sion model that decomposes an image into multiple high-
    quality, semantically disentangled RGBA layers, thereby
    enabling inherently consistent image editing.
- We design the image decomposer from three aspects: 1)
    an RGBA-VAE to provide shared latent space for RGB
    and RGBA images. 2) a VLD-MMDiT architecture to fa-
    cilitate decomposition with variable number of layers. 3)
    a Multi-stage Training strategy to adapt a pretrained im-
    age generation model to a multilayer image decomposer.
- We develop a data processing pipeline to extract and an-
    notate multilayer images from Photoshop documents, ad-
    dressing the lack of high-quality multilayer images.
- Extensive experiments demonstrate that Qwen-Image-
    Layered not only outperforms existing methods in de-
    composition quality but also unlocks new possibilities for
    consistent, layer-based image editing and synthesis.

## 2. Related Work

### 2.1. Image Editing

```
Image editing has made significant progress in recent years
and can be broadly categorized into two paradigms: global
editing and mask-guided local editing. Global editing meth-
ods [4, 9, 21, 26, 39, 42, 43, 48] regenerate the entire im-
age to achieve holistic modifications, such as expression
editing and style transfer. Among these, Qwen-Image-
Edit [42] leverages two distinct yet complementary feature
representations—semantic features from Qwen-VL [3] and
reconstructive features from VAE [19]—to enhance consis-
tency. However, due to the inherent stochasticity of gener-
ative models, these approaches cannot ensure consistency
in unedited regions. In contrast, mask-guided local editing
methods [8, 29, 35] constrain modifications within a spec-
ified mask to preserve global consistency. DiffEdit [8], for
instance, first automatically generates a mask to identify re-
gions requiring modification and then edits the target area.
Although intuitive, these approaches struggle with occlu-
sions and soft boundaries, making it difficult to precisely
identify the actual editing region and thus failing to funda-
mentally resolve the consistency issue. Unlike these works,
we propose decomposing the image into semantically dis-
entangled RGBA layers, where each layer can be inde-
pendently modified while keeping the others unchanged,
thereby fundamentally ensuring consistent across edits.
```

### 2.2. Image Decomposition

Numerous studies have attempted to decompose images
into layers. Early approaches addressed this problem by
performing segmentation in color space [2, 20, 37]. Sub-
sequent work has focused on object-level decomposition
in natural scenes [28, 30, 47]. Among these, PCNet [47]
learns to recover fractional object masks and contents in
a self-supervised manner. More recent research has ex-
plored decomposing images into multiple RGBA layers [7,
18, 36, 38, 45]. One class of these methods leverages seg-
mentation [33] or matting [23] to extract foreground ob-
jects, followed by image inpainting [46] to reconstruct the
background. For instance, LayerD [36] iteratively extracts
the topmost unoccluded foreground layer and completes
the background. Accordion [7] proposes using Vision-
Language Models [25] to guide this decomposition process.
Another category of work introduces mask-guided, object-
centric image decomposition [18, 45], which decomposes
an image into foreground and background layers based on
a provided mask. These methods generally require seg-
mentation to provide initial mask. However, segmentation
often struggles with complex spatial layouts and the pres-
ence of multiple semi-transparent layers, resulting in low-
quality layers. Moreover, multilayer decomposition typi-
cally requires recursive inference, leading to error propaga-
tion. Consequently, existing methods fail to produce com-
plete, high-fidelity RGBA layers suitable for editing. In
contrast to the aforementioned approaches, Qwen-Image-
Layered employs an end-to-end framework to decompose
input images directly into multiple high-quality RGBA lay-
ers, thereby enhancing decomposition quality and enabling
consistency-preserving image editing.

### 2.3. Multilayer Image Synthesis

Multilayer image synthesis has also garnered sustained at-
tention [6, 15–18, 32, 49, 50]. As a pioneer in layered
image generation, Text2Layer [50] first trains a two-layer
image autoencoder [19] and subsequently trains a diffu-
sion model [13] on the latent representations, enabling the
creation of two-layer images. LayerDiffusion [49] intro-
duces latent transparency into VAE and employs two dif-
ferent LoRA [14] with shared attention to generate fore-
ground and background. Through carefully designed inter-
layer and intra-layer attention mechanisms, LayerDiff [17]
is able to synthesize semantically consistent multilayer im-
ages. To achieve controllable multilayer image generation,
ART [32] proposes an anonymous region layout to explic-
itly control the layout. LayeringDiff [18] first generates a
raster image using existing text-to-image models, and then
decomposes it into foreground and background based on a
mask. Qwen-Image-Layered is capable of decomposing AI-
generated raster images into multiple RGBA layers, thus
enabling multilayer image generation.

## 3. Method

```
We propose an end-to-end layering approach that directly
decomposes an input RGB image I ∈ RH×W×^3 into N
RGBA layers L∈ RN×H×W×^4 , where each layer Licom-
prises a color component RGBiand an alpha matte αi, i.e.
Li= [RGBi;αi]. The original image can be reconstructed
by sequential alpha blending as follows:
```
```
C 0 = 0
Ci= αi· RGBi+ (1− αi)· Ci− 1 i = 1,..., N
```
```
where Cidenotes the composite of the first i layers, and the
final composite satisfies I = CN. Building upon Qwen-
Image [42], we develop Qwen-Image-Layered from the fol-
lowing three aspects:
```
- 1) In contrast to previous decomposer [45] that employs
    separate VAEs, we propose an RGBA-VAE that encodes
    both RGB and RGBA images. This approach narrows the
    latent distribution gap between the input RGB image and
    the output RGBA layers.
- 2) Unlike prior methods that decompose images into fore-
    ground and background [18, 45], we propose a VLD-
    MMDiT (Variable Layers Decomposition MMDiT),
    which supports decomposition into a variable number of
    layers and is compatible with multi-task training.
- 3) To progressively adapt pretrained image generation
    model into a multilayer image decomposer, we design a
    multi-stage, multi-task training scheme that progressively
    evolves from simpler tasks to more complex ones.

### 3.1. RGBA-VAE

```
Variational Autoencoders (VAEs) [19] are commonly em-
ployed in diffusion models [34] to reduce the dimensional-
ity of the latent space, thereby improving both training and
sampling efficiency. In previous work, LayeringDiff [18]
utilized an RGB VAE to first generate the foreground layer
and subsequently applied an additional module to obtain
transparency. LayerDecomp [45] adopted separate VAEs
for the input RGB image and the output RGBA layers, re-
sulting in a distribution gap between the input and output
representations. To address these limitations, we propose
RGBA VAE, a four-channel VAE designed to process both
RGB and RGBA images.
Inspired by AlphaVAE [40], we extend the first convolu-
tion layer of the Qwen-Image VAE encoder E and the last
convolution layer of the decoderD from three to four chan-
nels. To enable reconstruction of both RGB and RGBA im-
ages, we train it using both types of images. For RGB im-
ages, the alpha channel is set to 1. To maintain RGB recon-
struction performance during initialization, we employ the
following initialization strategy. Let WE^0 ∈ RD^0 ×^4 ×k×k×k
and b^0 E∈ RD^0 denote the weight and bias of the first convo-
lution layer in the encoder, and WDl ∈ R^4 ×Dl×k×k×kand
```

#### RGBA-VAE

```
Encoder
```
```
Patchify
```
```
VLD-MMDiTBlock
```
```
VLD-MMDiTBlock
```
## ...

```
×N
```
```
Input Image
```
```
!
```
```
Text Prompt
```
```
UnPatchify
```
```
Target Layers
```
```
Patchify
```
```
Noise
```
```
Qwen2.5VL
```
```
(-1, -1, 0)
```
```
(-1, -1, -1) (-1, 0, -1) (-1, 1, -1)
```
```
(-1, -1, 1)
```
```
(0, -1, 0)
```
```
(0, -1, -1) (0, 0, -1) (0, 1, -1)
```
```
(0, -1, 1)
```
```
(1, -1, 0)
```
```
(1, -1, -1) (1, 0, -1) (1, 1, -1)
```
```
(1, -1, 1)
```
```
(2, -1, 0)
```
```
(2, -1, -1) (2, 0, -1) (2, 1, -1)
```
```
(2, -1, 1)
```
```
(2, 0, 0) (2, 1, 0)
```
```
(2, 0, 1) (2, 1, 1 )
```
```
width
```
```
layer
height
```
```
Decomposing
```
```
The image features
a stylized urban
scene split into two
contrasting halves.
On the left side,
there is a
grayscale ...
```
#### RGBA-VAE

```
Encoder
```
```
Figure 4. Overview of Qwen-Image-Layered. Left: Illustration of our proposed VLD-MMDiT (Variable Layers Decomposition MMDiT),
where the input RGB image and the target RGBA layers are both encoded by our proposed RGBA-VAE. During attention computation,
these two sequences are concatenated along the sequence dimension, thereby enhancing inter-layer and intra-layer interactions. Right:
Illustration of Layer3D RoPE, where a new layer dimension is introduced to support a variable number of layers.
```
blD∈ R^4 denote those of the last convolution layer in the
decoder, where k is the kernel size. We copy the parameters
from the pretrained RGB VAE into the first three channels
and set the newly initialized parameters as

```
WE^0 [:, 3 , :, :, :] = 0 WDl[3, :, :, :, :] = 0 blD[3] = 1
```
```
For the training objective, we use a combination of re-
construction loss, perceptual loss, and regularization loss.
After training, both the input RGB image and the output
RGBA layers are encoded into a shared latent space, where
each RGBA layer is encoded independently. Notably, these
layers exhibit no cross-layer redundancy; consequently, no
compression is applied along the layer dimension.
```
### 3.2. Variable Layers Decomposition MMDiT

```
Previous studies [7, 18, 36, 45] typically decompose images
into background and foreground, requiring recursive infer-
ence to perform multilayer decomposition. Instead, Qwen-
Image-Layered proposes VLD-MMDiT (Variable Layers
Decomposition MMDiT) to facilitate the decomposition of
a variable number of layers.
For Qwen-Image-Layered, it tasks an RGB image I ∈
RH×W×^3 as input and decomposes it into multiple RGBA
layers L ∈ RN×H×W×^4. Following Qwen-Image, we
adopt the Flow Matching training objective. Formally, let
x 0 ∈ RN×h×w×cdenote the latent representation of the
target RGBA layers L, i.e., x 0 = E(L). Then we sample
noise x 1 from standard multivariate normal distribution and
a timestep t ∈ [0, 1] from a logit-normal distribution. Ac-
```
```
cording to Rectified Flow [27], the intermediate state xtand
velocity vtat timestep t is defined as
```
```
xt= tx 0 + (1− t)x 1
```
```
vt=
```
```
dxt
dt
```
```
= x 0 − x 1
```
```
For the input RGB image I , we also use RGBA-VAE to en-
code it as a latent representation zI∈ Rh×w×c. Following
Qwen-Image, the text prompt is encoded into text condition
h with MLLM. In practice, we can use Qwen2.5-VL [3]
to automatically generate the caption for the input image.
Then, the model is trained to predict the target velocity with
loss function defined as the mean squared error between the
predicted velocity vθ(xt,t,zI,h) and the ground truth vt:
```
```
L = E(x 0 ,x 1 ,t,zI,h)∼D||vθ(xt,t,zI,h)− vt||^2
```
```
whereD denotes the training dataset.
Previous studies [16, 17] have achieved multilayer image
generation through sophisticatedly designed inter-layer and
intra-layer attention mechanisms. In contrast, we employ
a Multi-Modal attention [10] to directly model these rela-
tionships, as shown in the left part of Fig. 4. Specifically,
we apply 2 × patchification to the noise-free input image zI
and the intermediate state xtalong the height and width di-
mensions. In each VLD-MMDiT block, two separate sets of
parameters are used to process textual h and visual informa-
tion zI,xtrespectively. During attention computation, we
concatenate these three sequences, thereby directly model-
ing both intra-layer and inter-layer interactions.
```

As shown in the right part of Fig. 4, we propose a
Layer3D RoPE within each VLD-MMDiT block to enable
the decomposition of a variable number of layers, while
supporting various tasks. Our design is inspired by the
MSRoPE from Qwen-Image [42], where the positional en-
coding in each layer is shifted towards the center. To ac-
commodate a variable number of layers, we introduce an
additional layer dimension. For the intermediate state xt,
the layer index starts from 0, and increases accordingly. For
conditional image input zI, we assign a layer index of -1,
ensuring a clear distinction from any positive layer indices
used in other tasks, e.g. text-to-multilayer image generation.

### 3.3. Multi-stage Training

Directly finetuning a pretrained image generation model to
perform image decomposition poses significant challenges,
as it not only requires adapting to a new VAE but also in-
volves learning new tasks. To address this issue, we propose
a multi-stage, multi-task training scheme that progressively
evolves from simpler tasks to more complex ones.
Stage 1: From Text-to-RGB to Text-to-RGBA. We be-
gin by adapting MMDiT to the latent space of RGBA VAE.
At this stage, we replace the original VAE and train the
model jointly on both text-to-RGB and text-to-RGBA gen-
eration tasks. This enables the model to generate not only
standard raster images (RGB) but also images with trans-
parency (RGBA).
Stage 2: From Text-to-RGBA to Text-to-Multi-
RGBA. Initially, the image generator is capable of produc-
ing only a single image. To support multilayer generation
and adapt to the newly initialized layer dimension, we in-
troduce a text-to-multiple-RGBA generation task. Follow-
ing ART [32], the model is trained to jointly predict both
the final composite image and its corresponding transpar-
ent layers, thereby facilitating information propagation be-
tween the composite image and its layers. We refer to this
model as Qwen-Image-Layered-T2L.
Stage 3: From Text-to-Multi-RGBA to Image-to-
Multi-RGBA. Up to this point, all tasks have been con-
ditioned exclusively on textual prompts. In this stage, we
introduce an additional image input, as detailed in Sec. 3.2,
extending the model’s capability to decompose a given
RGB image into multiple RGBA layers. We refer to this
model as Qwen-Image-Layered-I2L.

## 4. Experiment

### 4.1. Data Collection and Annotation

Due to the scarcity of high-quality multilayer images, pre-
vious studies [17, 18, 36, 50] have largely relied on either
synthetic data [38] or simple graphic design datasets (e.g.,
Crello [44]), which typically lack complex layouts or semi-
transparent layers. To bridge this gap, we developed a data

```
(a) Distribution of Layer Counts (b) Category Distribution
Figure 5. Statistics of the processed multilayer image dataset. (a)
Distribution of layer counts before and after merging. (b) Category
distribution in the final dataset.
```
```
pipeline to filter and annotate multilayer images derived
from real world PSD (Photoshop Document) files.
We began by collecting a large corpus of PSD files and
extracting all layers using psd-tools, an open-source
Python library for parsing Adobe Photoshop documents.
To ensure data quality, we filtered out layers containing
anomalous elements, such as blurred faces. To improve
decomposition performance, we removed non-contributing
layers that do not influence the final composite image. Fur-
thermore, given that some PSD files contain hundreds of
layers—thereby increasing model complexity—we merged
spatially non-overlapping layers to reduce the total layer
count. As shown in Fig. 5a, this operation substantially
reduces the number of layers. Finally, we employed
Qwen2.5-VL [3] to generate text descriptions for the com-
posite images, enabling Text-to-Multi-RGBA generation.
```
### 4.2. Implementation Details

```
Building upon Qwen-Image [42], we developed Qwen-
Image-Layered. The model was trained using the Adam
optimizer [1] with a learning rate of 1 × 10 −^5. For Text-
to-RGB and Text-to-RGBA generation, training was per-
formed on an internal dataset. For both Text-to-Multi-
RGBA and Image-to-Multi-RGBA generation, the model
was optimized on our proposed multilayer image dataset,
with the maximum number of layers set to 20. The training
process was conducted in three stages, comprising 500K,
400K, and 400K optimization steps, respectively.
```
### 4.3. Quantitative Results

```
4.3.1. Image Decomposition
To quantitatively evaluate image decomposition, we adopt
the evaluation protocol introduced by LayerD [36]. This
protocol aligns layer sequences of varying lengths using
order-aware Dynamic Time Warping and allows for the
merging of adjacent layers to account for inherent ambi-
guities in decomposition (i.e., a single image may have
multiple plausible decompositions). Quantitative results on
Crello dataset [44] are reported in Tab. 1. Following Lay-
erD [36], we report two metrics: RGB L1 (the L1 distance
```

```
Qwen
```
- Image Layered

```
Qwen
```
- Image Layered

```
LayerD
```
```
LayerD
```
```
Input Image Output Layer 1 Output Layer 2 Output Layer 3 Output Layer 4
```
Figure 6. Qualitative comparison of Image-to-Multi-RGBA (I2L). The leftmost column shows the input image; the subsequent columns
present the decomposed layers. Notably, LayerD [36] exhibits inpainting artifacts (Output Layer 1) and inaccurate segmentation (Output
Layer 2 and 3), while our method produces high-quality, semantically disentangled layers, suitable for inherently consistent image editing.

Table 1. Quantitative comparison of Image-to-Multi-RGBA (I2L) on Crello dataset [44]. RGB L1: L1 distance between RGB channels
weighted by the ground-truth alpha. Alpha soft IoU: soft IoU between predicted and ground-truth alpha channel.

```
Metric RGB L1↓ Alpha soft IoU↑
# Max Allowed Layer Merge 0 1 2 3 4 5 0 1 2 3 4 5
VLM Base + Hi-SAM [7] 0.1197 0.1029 0.0892 0.0807 0.0755 0.0726 0.5596 0.6302 0.6860 0.7222 0.7465 0.
Yolo Base + Hi-SAM 0.0962 0.0833 0.0710 0.0630 0.0592 0.0579 0.5697 0.6537 0.7169 0.7567 0.7811 0.
LayerD [36] 0.0709 0.0541 0.0457 0.0419 0.0403 0.0396 0.7520 0.8111 0.8435 0.8564 0.8622 0.
Qwen-Image-Layered-I2L 0.0594 0.0490 0.0393 0.0377 0.0364 0.0363 0.8705 0.8863 0.9105 0.9121 0.9156 0.
```
of the RGB channels weighted by the ground-truth alpha)
and Alpha soft IoU (the soft IoU between predicted and
ground-truth alpha channels). Due to a significant distribu-
tion gap between the Crello dataset and our proposed mul-
tilayer dataset—such as differences in the number of layers
and the presence of semi-transparent layers—we finetune

```
our model on Crello training set. As shown in Tab. 1, our
method achieves the highest decomposition accuracy, no-
tably achieving a significantly higher Alpha soft IoU score,
underscoring its superior ability in generating high-fidelity
alpha channels.
```

```
Change to a diagonal composition Move the pink words “Skate boarding” to the front of the girl, make the girl looks bigger.
```
```
Move the man to the right, keep
the background unchanged
```
```
Make the man face to the right and look
shorter, keep the background unchanged
```
```
Input Image Qwen-Image-Edit- 2509 Qwen-Image-Layered Qwen-Image-Edit- 2509 Qwen-Image-Layered
```
Figure 7. Qualitative comparison of image editing. The leftmost column is the input image; prompts are listed above each row. Qwen-
Image-Edit-2509 [42] struggles with resizing and repositioning, tasks inherently supported by Qwen-Image-Layered. Meanwhile, Qwen-
Image-Edit-2509 introduces pixel-level shifts (last row), while Qwen-Image-Layered can ensure consistency by editing specific layers.

```
Table 2. Ablation study on Crello dataset [44]. L: Layer3D Rope, R: RGBA-VAE, M: Multi-stage Training.
Metric Component RGB L1↓ Alpha soft IoU↑
# Max Allowed Layer Merge L R M 0 1 2 3 4 5 0 1 2 3 4 5
Qwen-Image-Layered-I2L-w/o LRM × × × 0.2809 0.2567 0.2467 0.2449 0.2439 0.2435 0.3725 0.4540 0.5281 0.5746 0.5957 0.
Qwen-Image-Layered-I2L-w/o RM ✓ × × 0.1894 0.1430 0.1255 0.1173 0.1138 0.1126 0.5844 0.6927 0.7576 0.7847 0.7954 0.
Qwen-Image-Layered-I2L-w/o M ✓✓ × 0.1649 0.1178 0.1048 0.0992 0.0966 0.0959 0.6504 0.7583 0.8074 0.8243 0.8310 0.
Qwen-Image-Layered-I2L ✓✓✓ 0.0594 0.0490 0.0393 0.0377 0.0364 0.0363 0.8705 0.8863 0.9105 0.9121 0.9156 0.
```
Table 3. Quantitative comparison of RGBA image reconstruction
on the AIM-500 dataset [22].

```
Model Base Model PSNR↑ SSIM↑ rFID↓ LPIPS↓
LayerDiffuse [49] SDXL 32.0879 0.9436 17.7023 0.
AlphaVAE [40] SDXlFLUX 35.7446 0.957636.9439 0.9737 10.9178 0.049511.7884 0.
RGBA-VAE Qwen-Image 38.8252 0.9802 5.3132 0.
```
4.3.2. Ablation Study

We conducted an ablation study on Crello dataset [44] to
validate the effectiveness of our proposed method. The re-
sults are presented in Tab. 2. For settings without multi-
stage training, we initialize the model directly from pre-
trained text-to-image weights. For experiments without
RGBA-VAE, we employ the original RGB VAE to encode

```
the input RGB image while retaining RGBA-VAE for out-
put RGBA layers. For variants without Layer3D RoPE, we
replace it with standard 2D RoPE for positional encoding.
All ablation experiments follow the same evaluation pro-
tocol as described in Sec. 4.3.1. As shown in the third
and fourth rows, multi-stage training effectively improves
decomposition quality. Comparing the second and third
rows, the superior performance in the third row indicates
that RGBA VAE effectively eliminates the distribution gap,
thereby improving overall performance. Furthermore, the
comparison between the first and second rows illustrates the
necessity of Layer3D Rope: without it, the model can not
distinguish between different layers, thus failing to decom-
pose images into multiple meaningful layers.
```

Figure 8. Qualitative comparison of Text-to-Multi-RGBA (T2L). The rightmost column shows the composite image. The second row
directly generates layers from text (Qwen-Image-Layered-T2L); the third row first generates a raster image (Qwen-Image-T2I) then de-
composes it into layers (Qwen-Image-Layered-I2L). ART [32] fails to follow the prompt, while Qwen-Image-Layered-T2L produces
semantically coherent layers, and Qwen-Image-T2I + Qwen-Image-Layered-I2L further improves visual aesthetics.

4.3.3. RGBA Image Reconstruction

Following AlphaVAE [40], we quantitatively evaluate
RGBA image reconstruction by blending the reconstructed
images over a solid-color background. Quantitative results
on AIM-500 dataset [22] are presented in Tab. 3, where
we compare our proposed RGBA VAE against LayerDif-
fuse [49] and AlphaVAE [40] in terms of PSNR, SSIM,
rFID, and LPIPS. As shown in Tab. 3, RGBA VAE achieves
the highest scores across all four metrics, demonstrating its
outstanding reconstruction capability.

### 4.4. Qualitative Results

4.4.1. Image Decomposition

We present a qualitative comparison of image decompo-
sition with LayerD [36] in Fig. 6. Notably, LayerD pro-
duces low-quality decomposition layers due to inaccurate
segmentation (layers 2 and 3) and inpainting artifacts (layer
1), rendering its results unsuitable for editing. In contrast,
our model performs image decomposition in an end-to-
end manner without relying on external modules, yielding
more coherent and semantically plausible decompositions,
thereby facilitating inherently consistent image editing.

4.4.2. Image Editing

In Fig. 7, we present a qualitative comparison with Qwen-
Image-Edit-2509 [42]. For Qwen-Image-Layered, we first
decompose the input image into multiple semantically dis-
entangled RGBA layers and then apply simple manual ed-
its. As illustrated, Qwen-Image-Edit-2509 struggles to fol-
low instructions involving layout modifications, resizing,
or repositioning. In contrast, Qwen-Image-Layered inher-
ently supports these elementary operations with high fi-
delity. Moreover, Qwen-Image-Edit-2509 introduces no-

```
ticeable pixel-level shifts, as shown in the bottom row. By
contrast, layered representation enables precise editing of
individual layers while leaving others exactly untouched,
thereby achieving consistency-preserving editing.
4.4.3. Multilayer Image Synthesis
In Fig. 8, we present a qualitative comparison of Text-to-
Multi-RGBA generation. In the second row, we directly
employ Qwen-Image-Layered-T2L for text-conditioned
multilayer image synthesis. Alternatively, we first generate
a raster image from text using Qwen-Image-T2I [42] and
then decompose it into multiple layers using Qwen-Image-
Layered-I2L. As illustrated, ART [32] struggles to generate
semantically coherent multilayer images (e.g. missing bats
and cat). In contrast, Qwen-Image-Layered-T2L produces
semantically coherent multilayer compositions. Moreover,
the pipeline combining Qwen-Image-T2I and Qwen-Image-
Layered-I2L further leverages the knowledge embedded in
the text-to-image generator, enhancing both semantic align-
ment and visual aesthetics.
```
## 5. Conclusion

```
In this paper, we introduce Qwen-Image-Layered, an
end-to-end diffusion model that decomposes a single RGB
image into multiple semantically disentangled RGBA
layers. By representing images as a stack of layers, our
approach enables inherent editability: each layer can be
independently manipulated while leaving all other con-
tent exactly unchanged, thereby fundamentally ensuring
consistency across edits. Extensive experiments demon-
strate that our method significantly outperforms existing
approaches in decomposition quality and establishes a
new paradigm for consistency-preserving image editing.
```

## References

```
[1] Kingma DP Ba J Adam et al. A method for stochastic op-
timization. arXiv preprint arXiv:1412.6980, 1412(6), 2014.
7
[2] Yagiz Aksoy, Tunc ̧ Ozan Aydin, Aljo ̆ ˇsa Smoli ́c, and Marc
Pollefeys. Unmixing-based soft color segmentation for im-
age manipulation. ACM Transactions on Graphics (TOG),
36(2):1–19, 2017. 5
[3] Shuai Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin
Ge, Sibo Song, Kai Dang, Peng Wang, Shijie Wang, Jun
Tang, et al. Qwen2. 5-vl technical report. arXiv preprint
arXiv:2502.13923, 2025. 4, 6, 7
[4] Tim Brooks, Aleksander Holynski, and Alexei A Efros. In-
structpix2pix: Learning to follow image editing instructions.
In Proceedings of the IEEE/CVF conference on computer vi-
sion and pattern recognition, pages 18392–18402, 2023. 4
[5] Qi Cai, Yehao Li, Yingwei Pan, Ting Yao, and Tao Mei.
Hidream-i1: An open-source high-efficient image genera-
tive foundation model. In Proceedings of the 33rd ACM In-
ternational Conference on Multimedia, pages 13636–13639,
```
2025. 4
[6] Junwen Chen, Heyang Jiang, Yanbin Wang, Keming Wu,
Ji Li, Chao Zhang, Keiji Yanai, Dong Chen, and Yuhui
Yuan. Prismlayers: Open data for high-quality multi-
layer transparent image generative models. arXiv preprint
arXiv:2505.22523, 2025. 5
[7] Jingye Chen, Zhaowen Wang, Nanxuan Zhao, Li Zhang, Di-
fan Liu, Jimei Yang, and Qifeng Chen. Rethinking layered
graphic design generation with a top-down approach. In
Proceedings of the IEEE/CVF International Conference on
Computer Vision, pages 16861–16870, 2025. 5, 6, 8
[8] Guillaume Couairon, Jakob Verbeek, Holger Schwenk,
and Matthieu Cord. Diffedit: Diffusion-based seman-
tic image editing with mask guidance. arXiv preprint
arXiv:2210.11427, 2022. 4
[9] Chaorui Deng, Deyao Zhu, Kunchang Li, Chenhui Gou,
Feng Li, Zeyu Wang, Shu Zhong, Weihao Yu, Xiaonan Nie,
Ziang Song, et al. Emerging properties in unified multimodal
pretraining. arXiv preprint arXiv:2505.14683, 2025. 4
[10] Patrick Esser, Sumith Kulal, Andreas Blattmann, Rahim
Entezari, Jonas Muller, Harry Saini, Yam Levi, Dominik ̈
Lorenz, Axel Sauer, Frederic Boesel, et al. Scaling recti-
fied flow transformers for high-resolution image synthesis.
In Forty-first international conference on machine learning,
2024. 4, 6
[11] Yu Gao, Lixue Gong, Qiushan Guo, Xiaoxia Hou, Zhichao
Lai, Fanshi Li, Liang Li, Xiaochen Lian, Chao Liao, Liyang
Liu, et al. Seedream 3.0 technical report. arXiv preprint
arXiv:2504.11346, 2025.
[12] Lixue Gong, Xiaoxia Hou, Fanshi Li, Liang Li, Xiaochen
Lian, Fei Liu, Liyang Liu, Wei Liu, Wei Lu, Yichun
Shi, et al. Seedream 2.0: A native chinese-english bilin-
gual image generation foundation model. arXiv preprint
arXiv:2503.07703, 2025. 4
[13] Jonathan Ho, Ajay Jain, and Pieter Abbeel. Denoising dif-
fusion probabilistic models. Advances in neural information
processing systems, 33:6840–6851, 2020. 5

```
[14] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-
Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen, et al.
Lora: Low-rank adaptation of large language models. ICLR,
1(2):3, 2022. 5
[15] Dingbang Huang, Wenbo Li, Yifei Zhao, Xinyu Pan, Yan-
hong Zeng, and Bo Dai. Psdiffusion: Harmonized multi-
layer image generation via layout and appearance alignment.
arXiv preprint arXiv:2505.11468, 2025. 5
[16] Junjia Huang, Pengxiang Yan, Jinhang Cai, Jiyang Liu,
Zhao Wang, Yitong Wang, Xinglong Wu, and Guanbin Li.
Dreamlayer: Simultaneous multi-layer generation via diffu-
sion mode. arXiv preprint arXiv:2503.12838, 2025. 6
[17] Runhui Huang, Kaixin Cai, Jianhua Han, Xiaodan Liang,
Renjing Pei, Guansong Lu, Songcen Xu, Wei Zhang, and
Hang Xu. Layerdiff: Exploring text-guided multi-layered
composable image synthesis via layer-collaborative diffu-
sion model. In European Conference on Computer Vision,
pages 144–160. Springer, 2024. 5, 6, 7
[18] Kyoungkook Kang, Gyujin Sim, Geonung Kim, Donguk
Kim, Seungho Nam, and Sunghyun Cho. Layeringdiff: Lay-
ered image synthesis via generation, then disassembly with
generative knowledge. arXiv preprint arXiv:2501.01197,
```
2025. 5, 6, 7
[19] Diederik P Kingma and Max Welling. Auto-encoding varia-
tional bayes. arXiv preprint arXiv:1312.6114, 2013. 4, 5
[20] Yuki Koyama and Masataka Goto. Decomposing images into
layers with advanced color blending. In Computer Graphics
Forum, pages 397–407. Wiley Online Library, 2018. 5
[21] Black Forest Labs, Stephen Batifol, Andreas Blattmann,
Frederic Boesel, Saksham Consul, Cyril Diagne, Tim Dock-
horn, Jack English, Zion English, Patrick Esser, et al. Flux.
1 kontext: Flow matching for in-context image generation
and editing in latent space. arXiv preprint arXiv:2506.15742,
2025. 4
[22] Jizhizi Li, Jing Zhang, and Dacheng Tao. Deep automatic
natural image matting. arXiv preprint arXiv:2107.07235,
2021. 9, 10
[23] Jiachen Li, Jitesh Jain, and Humphrey Shi. Matting anything.
In Proceedings of the IEEE/CVF Conference on Computer
Vision and Pattern Recognition, pages 1775–1785, 2024. 5
[24] Jian Liang, Chenfei Wu, Xiaowei Hu, Zhe Gan, Jianfeng
Wang, Lijuan Wang, Zicheng Liu, Yuejian Fang, and Nan
Duan. Nuwa-infinity: Autoregressive over autoregressive
generation for infinite visual synthesis. Advances in Neural
Information Processing Systems, 35:15420–15432, 2022. 4
[25] Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee.
Visual instruction tuning. Advances in neural information
processing systems, 36:34892–34916, 2023. 5
[26] Shiyu Liu, Yucheng Han, Peng Xing, Fukun Yin, Rui Wang,
Wei Cheng, Jiaqi Liao, Yingming Wang, Honghao Fu, Chun-
rui Han, et al. Step1x-edit: A practical framework for general
image editing. arXiv preprint arXiv:2504.17761, 2025. 4
[27] Xingchao Liu, Chengyue Gong, and Qiang Liu. Flow
straight and fast: Learning to generate and transfer data with
rectified flow. arXiv preprint arXiv:2209.03003, 2022. 6
[28] Zhengzhe Liu, Qing Liu, Chirui Chang, Jianming Zhang,
Daniil Pakhomov, Haitian Zheng, Zhe Lin, Daniel Cohen-Or,


and Chi-Wing Fu. Object-level scene deocclusion. In ACM
SIGGRAPH 2024 Conference Papers, pages 1–11, 2024. 5
[29] Qi Mao, Lan Chen, Yuchao Gu, Zhen Fang, and Mike Zheng
Shou. Mag-edit: Localized image editing in complex scenar-
ios via mask-based attention-adjusted guidance. In Proceed-
ings of the 32nd ACM International Conference on Multime-
dia, pages 6842–6850, 2024. 4
[30] Tom Monnier, Elliot Vincent, Jean Ponce, and Mathieu
Aubry. Unsupervised layered image decomposition into ob-
ject prototypes. In Proceedings of the IEEE/CVF inter-
national conference on computer vision, pages 8640–8650,

2021. 5
[31] Dustin Podell, Zion English, Kyle Lacey, Andreas
Blattmann, Tim Dockhorn, Jonas Muller, Joe Penna, and ̈
Robin Rombach. Sdxl: Improving latent diffusion mod-
els for high-resolution image synthesis. arXiv preprint
arXiv:2307.01952, 2023. 4
[32] Yifan Pu, Yiming Zhao, Zhicong Tang, Ruihong Yin, Haox-
ing Ye, Yuhui Yuan, Dong Chen, Jianmin Bao, Sirui Zhang,
Yanbin Wang, et al. Art: Anonymous region transformer for
variable multi-layer transparent image generation. In Pro-
ceedings of the Computer Vision and Pattern Recognition
Conference, pages 7952–7962, 2025. 5, 7, 10
[33] Nikhila Ravi, Valentin Gabeur, Yuan-Ting Hu, Ronghang
Hu, Chaitanya Ryali, Tengyu Ma, Haitham Khedr, Roman
Radle, Chloe Rolland, Laura Gustafson, et al. ̈ Sam 2:
Segment anything in images and videos. arXiv preprint
arXiv:2408.00714, 2024. 5
[34] Robin Rombach, Andreas Blattmann, Dominik Lorenz,
Patrick Esser, and Bj ̈orn Ommer. High-resolution image
synthesis with latent diffusion models. In Proceedings of
the IEEE/CVF conference on computer vision and pattern
recognition, pages 10684–10695, 2022. 4, 5
[35] Enis Simsar, Alessio Tonioni, Yongqin Xian, Thomas Hof-
mann, and Federico Tombari. Lime: localized image edit-
ing via attention regularization in diffusion models. In 2025
IEEE/CVF Winter Conference on Applications of Computer
Vision (WACV), pages 222–231. IEEE, 2025. 4
[36] Tomoyuki Suzuki, Kang-Jun Liu, Naoto Inoue, and Kota Ya-
maguchi. Layerd: Decomposing raster graphic designs into
layers. In Proceedings of the IEEE/CVF International Con-
ference on Computer Vision, pages 17783–17792, 2025. 5,
6, 7, 8, 10
[37] Jianchao Tan, Jyh-Ming Lien, and Yotam Gingold. Decom-
posing digital paintings into layers via rgb-space geometry.
arXiv preprint arXiv:1509.03335, 2015. 5
[38] Petru-Daniel Tudosiu, Yongxin Yang, Shifeng Zhang, Fei
Chen, Steven McDonagh, Gerasimos Lampouras, Ignacio
Iacobacci, and Sarah Parisot. Mulan: A multi layer anno-
tated dataset for controllable text-to-image generation. In
Proceedings of the IEEE/CVF Conference on Computer Vi-
sion and Pattern Recognition, pages 22413–22422, 2024. 5,
7
[39] Peng Wang, Yichun Shi, Xiaochen Lian, Zhonghua Zhai,
Xin Xia, Xuefeng Xiao, Weilin Huang, and Jianchao Yang.
Seededit 3.0: Fast and high-quality generative image editing.
arXiv preprint arXiv:2506.05083, 2025. 4

```
[40] Zile Wang, Hao Yu, Jiabo Zhan, and Chun Yuan. Alphavae:
Unified end-to-end rgba image reconstruction and genera-
tion with alpha-aware representation learning. arXiv preprint
arXiv:2507.09308, 2025. 5, 9, 10
[41] Chenfei Wu, Jian Liang, Lei Ji, Fan Yang, Yuejian Fang,
Daxin Jiang, and Nan Duan. Nuwa: Visual synthesis pre- ̈
training for neural visual world creation. In European con-
ference on computer vision, pages 720–736. Springer, 2022.
4
[42] Chenfei Wu, Jiahao Li, Jingren Zhou, Junyang Lin, Kaiyuan
Gao, Kun Yan, Sheng-ming Yin, Shuai Bai, Xiao Xu, Yilei
Chen, et al. Qwen-image technical report. arXiv preprint
arXiv:2508.02324, 2025. 4, 5, 7, 9, 10
[43] Chenyuan Wu, Pengfei Zheng, Ruiran Yan, Shitao Xiao, Xin
Luo, Yueze Wang, Wanli Li, Xiyan Jiang, Yexin Liu, Junjie
Zhou, et al. Omnigen2: Exploration to advanced multimodal
generation. arXiv preprint arXiv:2506.18871, 2025. 4
[44] Kota Yamaguchi. Canvasvae: Learning to generate vector
graphic documents. In Proceedings of the IEEE/CVF Inter-
national Conference on Computer Vision, pages 5481–5489,
```
2021. 7, 8, 9
[45] Jinrui Yang, Qing Liu, Yijun Li, Soo Ye Kim, Daniil Pakho-
mov, Mengwei Ren, Jianming Zhang, Zhe Lin, Cihang Xie,
and Yuyin Zhou. Generative image layer decomposition with
visual effects. In Proceedings of the Computer Vision and
Pattern Recognition Conference, pages 7643–7653, 2025. 5,
6
[46] Tao Yu, Runseng Feng, Ruoyu Feng, Jinming Liu, Xin
Jin, Wenjun Zeng, and Zhibo Chen. Inpaint anything:
Segment anything meets image inpainting. arXiv preprint
arXiv:2304.06790, 2023. 5
[47] Xiaohang Zhan, Xingang Pan, Bo Dai, Ziwei Liu, Dahua
Lin, and Chen Change Loy. Self-supervised scene de-
occlusion. In Proceedings of the IEEE/CVF conference on
computer vision and pattern recognition, pages 3784–3792,
2020. 5
[48] Kai Zhang, Lingbo Mo, Wenhu Chen, Huan Sun, and Yu Su.
Magicbrush: A manually annotated dataset for instruction-
guided image editing. Advances in Neural Information Pro-
cessing Systems, 36:31428–31449, 2023. 4
[49] Lvmin Zhang and Maneesh Agrawala. Transparent image
layer diffusion using latent transparency. arXiv preprint
arXiv:2402.17113, 2024. 5, 9, 10
[50] Xinyang Zhang, Wentian Zhao, Xin Lu, and Jeff Chien.
Text2layer: Layered image generation using latent diffusion
model. arXiv preprint arXiv:2307.09781, 2023. 5, 7


