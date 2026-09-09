# BBQ-to-Image Numeric Bounding Box and Qolor Control in

*Source PDF: `BBQ-to-Image Numeric Bounding Box and Qolor Control in.pdf`*

*Total Pages: 13*

---


## Page 1


BBQ-to-Image: Numeric Bounding Box and Qolor Control in
Large-Scale Text-to-Image Models
Eliran Kachlon
Alexander Visheratin
Nimrod Sarid
Tal Hacham
Eyal Gutflaish
Saar Huberman
Hezi Zisman
David Ruppin
Ron Mokady
BRIA AI
Figure 1: Bounding-box and RGB-controlled image generation and refinement. BBQ enables precise spatial and
color control by conditioning on explicit numeric bounding boxes and RGB values. In the example, the exact locations
of the people and the dog are specified via bounding boxes, and the colors of their clothing are defined using RGB
triplets. Beyond initial generation, BBQ enables structured refinement by modifying only the numeric parameters in
the caption and re-generating the image. Due to the model’s disentangled control over layout and color, updating
bounding boxes (e.g., swapping the man and the woman, or moving the dog to the right) or modifying RGB values
results in consistent, targeted changes while preserving the rest of the scene.
1
arXiv:2602.20672v1  [cs.CV]  24 Feb 2026


## Page 2


Abstract
Text-to-image models have rapidly advanced in realism
and controllability, with recent approaches leveraging
long, detailed captions to support fine-grained generation.
However, a fundamental parametric gap remains: exist-
ing models rely on descriptive language, whereas pro-
fessional workflows require precise numeric control over
object location, size, and color. In this work, we intro-
duce BBQ, a large-scale text-to-image model that directly
conditions on numeric bounding boxes and RGB triplets
within a unified structured-text framework.
We obtain
precise spatial and chromatic control by training on cap-
tions enriched with parametric annotations, without ar-
chitectural modifications or inference-time optimization.
This also enables intuitive user interfaces such as object
dragging and color pickers, replacing ambiguous iterative
prompting with precise, familiar controls. Across com-
prehensive evaluations, BBQ achieves strong box align-
ment and improves RGB color fidelity over state-of-the-
art baselines. More broadly, our results support a new
paradigm in which user intent is translated into an inter-
mediate structured language, consumed by a flow-based
transformer acting as a renderer and naturally accommo-
dating numeric parameters.
1
Introduction
Text-to-image models have rapidly evolved from casual
creative tools into professional-grade systems, achieving
unprecedented levels of realism and visual fidelity. Recent
works have significantly advanced controllability by train-
ing on long structured captions, most notably FIBO [1], as
well as concurrent systems such as Hunyuan 3.0 [2] and
FLUX.2 [3]. By encoding fine-grained visual attributes
explicitly in text, these models allow users to specify and
control nearly every aspect of an image using language
alone. Unlike earlier approaches, such models exhibit nat-
ural disentanglement, enabling refinement of a specific vi-
sual factor, such as lighting, object appearance, or expres-
sion, while keeping other aspects unchanged.
Despite this progress, a fundamental parametric gap
remains. Text-based controllability is inherently descrip-
tive and imprecise for attributes that require exact numeric
specification. In this work, we focus on three such at-
tributes: size, location, and color. Current models rely
on subjective linguistic descriptors such as “crimson” or
“bottom-right,” whereas professional workflows demand
deterministic precision in the form of explicit RGB val-
ues and pixel-accurate bounding boxes. Moreover, para-
metric grounding naturally enables intuitive interaction:
bounding boxes support direct object manipulation (e.g.,
dragging), and RGB values integrate seamlessly with
color pickers. This replaces ambiguous natural-language
prompting with precise and familiar user interfaces.
In this paper, we show that large-scale text-to-image
models can be adapted to process numeric inputs for
precise parametric control. We introduce BBQ, a large-
scale text-to-image model capable of controlling Bound-
ing Boxes and Qolors directly. Unlike prior approaches,
BBQ requires no architectural modifications, no special
grounding tokens, and no inference-time optimization. In-
stead, parametric control is achieved solely by augment-
ing the training captions, resulting in a simple yet power-
ful solution that scales naturally to professional use.
To generate training data, we augment FIBO-style
structured captions with explicit numeric attributes, in-
cluding RGB color values and object bounding boxes. For
inference, we fine-tune a vision–language model (VLM)
to serve as an inference-time bridge, converting short
natural-language prompts into detailed parametric de-
scriptions that BBQ can execute faithfully.
More broadly,
our framework highlights a new
paradigm for image generation. Rather than generating
images directly from user-written text, user intent is first
translated, by a VLM, into an intermediate, structured lan-
guage, which is then consumed by a flow-based trans-
former acting as a renderer. Within this paradigm, we
show that the intermediate language can naturally accom-
modate numeric parameters, enabling precise, determin-
istic control without sacrificing expressiveness.
Through extensive evaluation, we demonstrate that
BBQ achieves strong results in precision for object lo-
cation, size, and color control, demonstrating that large-
scale text-to-image models can natively process numeric
parameters within a unified text-based framework.
2
Related Works
Text-to-image models.
Diffusion models have become
the primary framework for text-to-image generation.
Early models [4–6] established the power of condition-
ing on strong language encoders, while latent diffusion
made large-scale training practical [7, 8]. Recently, ar-
chitectures have shifted toward transformer backbones
and flow-matching objectives [9–13]. Together, these ad-
vances have pushed the boundaries of visual fidelity.
Long and structured captions.
While early models re-
lied on noisy, web-scraped data [14], recent works [9,
11, 15] show that descriptive synthetic captions signifi-
cantly improve prompt alignment.
Recently, FIBO [1]
extended this approach by using vision-language mod-
els to produce long, structured JSON captions that cap-
ture all visual factors in the image, including object at-
tributes, spatial relations, and photographic style. This ap-
2


## Page 3


Figure 2: End-to-end parametric workflow. A short prompt is expanded by a VLM into a structured JSON that
includes numeric bounding boxes and RGB values (for clarity, we show only the parametric fields for the woman).
The JSON is then provided to BBQ to generate an image. Users can edit specific fields (e.g., box coordinates or
color values), and BBQ updates the output accordingly while preserving unrelated content, demonstrating native
disentanglement. Notably, BBQ receives no image input, and consistency is maintained solely through the disentangle
structured conditioning.
proach achieved state-of-the-art prompt alignment and in-
troduced fine-grained control, enabling “native disentan-
glement” where modifying a single attribute in the JSON
affects only the intended visual factor. However, FIBO re-
lies on natural language (e.g., “red” or “top-left”) that still
involves semantic ambiguity. BBQ builds on this founda-
tion by replacing descriptive strings with absolute preci-
sion, integrating RGB values and bounding boxes to tran-
sition from semantic alignment to exact pixel-level and
chromatic controllability.
Region-controlled text-to-image.
Traditional layout-
to-image frameworks [7, 16–22] that generate images
given bounding boxes are usually limited to constrained
vocabularies [23]. Recent works like ReCo [24], GLI-
GEN [25], InstanceDiffusion [26] and Ranni [27] mit-
igate these gaps by introducing specialized position to-
kens or modifying model architectures to inject regional
grounding signals. Related controllable diffusion frame-
works such as ControlNet [28] and Composer [29] fur-
ther enable spatial control through additional condition-
ing pathways. Training-free approaches such as BoxD-
iff [30] and MultiDiffusion [31] also support region con-
straints by altering the denoising process at inference
time. While effective, these approaches necessitate com-
plex structural changes, auxiliary conditioning mecha-
nisms, or inference-time modifications. In contrast, BBQ
unifies high-precision spatial control within a single struc-
tured textual representation, enabling exact coordinate
guidance without any architectural modifications to the
underlying model.
Color-palette generation.
Controlling color distribu-
tion is a classical challenge in image synthesis [32–36].
Early deep learning efforts incorporated generative and
adversarial frameworks to better model realistic and di-
verse color distributions [37–44]. More recent approaches
attempt to provide fine-grained control over color at-
tributes within text-to-image diffusion models.
These
include methods that train and fine-tune existing mod-
els [27, 29, 45], as well as training-free approaches [46–
48] that enable color control by manipulating the sam-
pling process or exploiting existing semantic bindings,
bypassing the need for additional fine-tuning. However,
these methods often rely on specialized adapters, task-
specific loss functions, or additional inference-time op-
timization steps. In contrast, BBQ achieves precise RGB-
level color attribution by encoding explicit RGB triplets
directly within the textual conditioning, without introduc-
ing architectural changes or inference-time modifications.
3


## Page 4


Fire hydrant to
(70.8, 87.5, 25.2, 95.2)
Fire hydrant to
Warmer color
palette
Cat to
Parrot flying at
(32.3, 66.3, 6.6, 23.5)
Grayscale
Shirt to
Goose to black
Colder color
palette
Figure 3:
Disentangled parametric refinement via
structured re-generation. Each example starts from an
image generated from a structured JSON prompt. We then
edit only the relevant JSON fields and re-generate using
the same random seed. Although the model does not ob-
serve the original image, it produces localized changes
that follow the modified parameters while preserving the
rest of the scene, demonstrating strong parametric disen-
tanglement. Ground-truth bounding boxes are overlaid for
visualization.
3
Method
We now describe our framework, BBQ. Our objective is to
adapt a large-scale text-to-image model to accept numeric
bounding boxes and colors as conditioning inputs, such
that the generated image is faithfully aligned with these
parametric specifications.
Formally, let M denote a text-to-image model trained
to generate images conditioned on a long structured cap-
tion P [1]. We extend this model to additionally condition
on numeric bounding boxes {bi}N
i=1 and colors {ci}N
i=1
for each of the N objects in P, producing an image
M(P, {bi}N
i=1, {ci}N
i=1)
that is accurately aligned with the specified parameters.
Unlike standard text-to-image generation, where spa-
tial and chromatic attributes are described linguistically,
bounding boxes and colors in our framework are repre-
sented numerically: (1) each bounding box is defined as
b = (x0, y0, x1, y1) ∈(0, 1)4, where (x0, y0) and (x1, y1)
are the relative coordinates corresponding to the top-left
and bottom-right of the bounding box, and (2) each color
is defined as an RGB triplet c ∈[0, 255]3.
In this section, we show that such adaptation is fea-
sible at large scale without architectural changes or ad-
ditional loss functions, relying solely on dataset aug-
Original
BBQ (Ours)
FIBO
Flux.2
NB
Figure 4: Text-as-a-Bottleneck Reconstruction (TaBR).
Starting from the original image (left), a detailed caption
is generated and used as input to each model. The re-
sulting reconstructions are compared against the original.
BBQ more faithfully preserves scene layout, object rela-
tions, and fine-grained attributes than competing state-of-
the-art models, demonstrating improved expressiveness.
mentation.
In Section 3.1, we describe how we aug-
ment structured training captions with numeric bound-
ing boxes and colors ({bi}N
i=1, {ci}N
i=1). Section 3.2 de-
tails the training procedure of BBQ, including the incor-
poration of parametric supervision without architectural
modifications. Finally, in Section 3.3, we describe how
we bridge the gap between user intent and a valid struc-
tured prompt. Specifically, we first present the transla-
tion of a short natural-language caption into a full long
structured parametric prompt (P, {bi}N
i=1, {ci}N
i=1), and
then describe how users can interactively modify bound-
ing boxes or colors, e.g., by dragging objects or adjusting
color values, while maintaining global consistency within
the structured representation.
3.1
Enriching
the
Training
Data
with
Bounding Boxes and Colors
In BBQ, we extend the common practice of synthetic
captioning for text-to-image training. Starting from long
structured captions [1], we augment each caption with nu-
meric bounding boxes and RGB colors. Although extract-
ing such parameters is well studied in vision and graphics,
we find that general-purpose LLM/VLM systems (e.g.,
Gemini 2.5 [49]) are not sufficiently reliable for high-
precision outputs.
Therefore, for each image we first
generate a FIBO-style structured caption, following [1].
For every object mentioned in the caption, we extract its
bounding box from grounded SAM2 [50], estimate rel-
ative depth using Depth Anything V2 [51], and obtain
4


## Page 5


Target Color
BBQ (Ours)
FIBO
Flux.2
NB
Figure 5: Color-conditioning accuracy. Each example
shows the target color (left) and images generated by dif-
ferent models when conditioned on the same object and
exact RGB value. BBQ achieves high chromatic fidelity
to the target color and produces competitive results com-
pared to state-of-the-art text-to-image models under iden-
tical color-conditioning prompts.
dominant object colors using Pylette [52]. We replace se-
mantic location and qualitative color terms with explicit
bounding box coordinates and RGB triplets. Finally, a
global RGB palette from Pylette is added to capture the
overall color scheme. This automated extraction provides
the precise parametric grounding required to align nu-
meric tokens with visual synthesis.
3.2
BBQ: Large-Scale Training to Control
Bounding Boxes and Qolors
Unlike prior approaches that introduce new architectures,
loss functions, or extended inference procedures to en-
able parametric control, we show that strong bounding-
box grounding can be achieved by large-scale training
on enriched captions alone. We initialize from the 8B-
parameter FIBO backbone [1], which is designed to pro-
cess long structured captions, and continue training on
25M images paired with our parametric captions.
We train the model following FIBO’s hyperparame-
ters [1], using the AdamW optimizer [53] with weight de-
cay of 1×10−4, β1 = 0.9, β2 = 0.999, and ϵ = 1×10−15.
The learning rate is set to 1×10−4 with a constant sched-
ule and a warmup of 10K steps.
Training follows the
flow-matching formulation [54], with a logit-normal noise
schedule combined with resolution-dependent timestep
shifting [9]. The model was trained for 80,000 steps with
an effective batch size of 512 in resolution 10242. Post-
“A knight located at (top left: (27.2, 36.3), bottom right: (54.8, 98)) is going
towards a dragon at (top left: (63.1, 14.7), bottom right: (77.1, 29.1)).”
BBQ (ours)
NB
Flux.2
“Three glass bottles standing in a row: a red bottle at (top left: (12.5, 30), bottom
right: (27.5, 80)), a green bottle at (top left: (42.5, 30.0), bottom right: (57.5,
80.0)), and a blue bottle at (top left: (72.6, 30.0), bottom right: (87.6, 80.0)).”
BBQ (ours)
NB
Flux.2
“A monkey at (”top left”: (16.5, 59.8), ”bottom right”: (35, 85)) is going to-
wards a zebra at (”top left”: (54.3, 17.1), ”bottom right”: (92.3, 89.7))”
BBQ (ours)
NB
Flux.2
Figure 6: Bounding-box accuracy. We compare BBQ
with Nano Banana Pro and Flux.2 Pro on prompts that in-
clude explicit numeric bounding-box specifications (over-
laid on the images).
While the baseline models often
struggle to consistently follow these spatial constraints,
BBQ reliably places objects within the specified boxes.
training, we perform aesthetic finetuning with 3,000 hand-
picked images, followed by DPO training [55] with dy-
namic beta [56] to improve text rendering.
As shown in Figure 1, BBQ adapts effectively to the
new conditioning format and follows numeric inputs with
high fidelity.
Furthermore, Figure 3 demonstrates that
BBQ preserves FIBO’s native disentanglement: using the
same random seed, we modify only the relevant fields in
the structured JSON and re-generate the image, resulting
in targeted changes to the specified attribute while the rest
of the scene remains largely unchanged.
3.3
The Parametric Bridge:
From Short
Captions to Long, Structured, Paramet-
ric Prompts
The trained model enables new forms of user interaction,
including object dragging, resizing, and recoloring. How-
ever, building a complete end-to-end system introduces
two key challenges. First, when a user edits a bounding
box, the system must preserve global coherence and avoid
breaking the composition. For example, if two people are
hugging and the user separates their boxes, the underly-
ing action must necessarily change. Second, for genera-
tion from scratch, a short natural-language prompt must
5


## Page 6


Table 1: Text-as-a-Bottleneck Reconstruction (TaBR).
Win rate is computed as the fraction of images where
BBQ is preferred over the competing model among de-
cisive comparisons (ties ignored). Confidence intervals
correspond to 95% Wilson score intervals. BBQ outper-
forms all evaluated baselines across all comparisons.
Model (vs. BBQ)
BBQ win rate↑
95% CI
Nano Banana Pro
65.2%
[50.8, 77.3]
FIBO
76.1%
[62.1, 86.1]
FLUX.2 Pro
93.3%
[82.1, 97.7]
be expanded into a full structured caption with a plausi-
ble composition, now including explicit bounding boxes
and colors. While BBQ provides unprecedented precision
through its parametric schema, manually authoring JSON
prompts with exact RGB triplets and normalized bound-
ing box coordinates is impractical for human users.
To address these inference-time gaps, we fine-tune
Qwen-3 VL 4B [57] to serve as an inference-time bridge
that translates natural-language intent into the parametric
language consumed by the generator. We train on synthet-
ically generated short prompts and editing instructions,
using the same structured schema employed for FIBO
BBQ. Training is performed on 8×H100 with a total of
3B tokens. To improve robustness, we decouple image-
conditioned and text-only tasks during training and repeat
each with different seeds, then final weights are produced
via model merging [58].
The VLM operates in three modes: (1) Generate, which
expands a brief prompt into a complete parametric JSON;
(2) Refine, which edits an existing JSON in response
to textual instructions (e.g., shifting bounding boxes or
adjusting colors) while maintaining internal consistency;
and (3) Inspire, which extracts a parametric description
from a reference image to serve as a template for genera-
tion and editing. In practice, we find that state-of-the-art
VLMs such as Gemini 2.5 [49] can also serve as an ef-
fective inference-time bridge. The workflow of BBQ is
described in Figure 2.
4
Experiments
In this section, we present a comprehensive evaluation
of BBQ, comparing it to existing state-of-the-art models.
Our experiments are designed to isolate three complemen-
tary properties: (1) expressiveness, (2) spatial accuracy
under numeric box constraints, and (3) color fidelity un-
der explicit RGB specification. Evaluation methods are
described in Section 4.1, qualitative results are provided
in Section 4.2, and quantitative results are discussed in
Section 4.3.
4.1
Evaluation Metrics
We evaluate BBQ using three complementary metrics
that
capture
different
aspects
of
controlled
image
synthesis:
(1)
Text-as-a-Bottleneck
Reconstruc-
tion (TaBR) [1] measures overall expressiveness via
caption→generation→reconstruction, (2) Bounding-box
accuracy
measures
spatial
grounding
under
box-
conditioned prompts, using COCO with YOLO-based
detection [23, 59] and LVIS with box-conditioned zero-
shot grounding [60], and (3) Color accuracy measures
parametric color fidelity by clustering generated pixels in
CIELab space using K-means and reporting perceptual
color differences via CIEDE2000 (∆E00) and the a–b
chroma distance.
For TaBR and color accuracy, we
compare
BBQ
against
state-of-the-art
text-to-image
baselines (FIBO, Nano Banana Pro, and Flux.2 Pro). For
bounding-box accuracy, we additionally compare against
InstanceDiffusion [26] and GLIGEN [25], widely used
box-grounded generation methods.
Text-as-a-Bottleneck.
TaBR [1] measures the overall
expressive power by anchoring the evaluation in images
rather than subjective text reasoning. Following FIBO, we
begin with a real image, produce a detailed caption using
a VLM, and then regenerate the image from this caption
alone. Annotators are then presented with the original im-
age alongside two reconstructions from different models
and asked: “Which image is more similar to the original?”
Like in FIBO, we perform this measurement on a test-set
of 60 image that are not part of our training data.
For BBQ and FIBO we utilize their native structured
schemas for compatibility, while for Nano Banana Pro
and Flux.2 Pro, we report the best result among three
methods: (a) BBQ parametric captions, (b) FIBO long
structured captions, and (c) detailed free-text descriptions
including precise Hex codes for object colors. To avoid
evaluation bias from the captioning pipeline, we use a
neutral VLM that is independent of BBQ and the data
preparation used for FIBO.
YOLO- and LVIS-based scores.
We follow the evalu-
ation protocol of InstanceDiffusion [26] to assess spatial
alignment between generated images and input bounding
boxes. A pretrained object detector is applied to the gener-
ated images, and the predicted boxes are compared against
the input box coordinates. For COCO evaluation, we use
YOLOv8 and report AP, AP50, and AR on COCO2017-
val. For large-vocabulary evaluation, we follow the LVIS
protocol using a ViTDet-L detector.
Color-conditioning accuracy.
To evaluating color fi-
delity we wish to isolate the specific object and remove
6


## Page 7


Table 2: Bounding-box alignment under box-conditioned generation on COCO and LVIS. We follow the In-
stanceDiffusion evaluation protocol using YOLO-based detection; the upper bound corresponds to detector perfor-
mance on real images. Across both datasets, BBQ consistently outperforms strong text-to-image baselines (Nano Ba-
nana Pro and Flux.2 Pro) and GLIGEN, while trailing the specialized InstanceDiffusion approach. Importantly, BBQ
achieves this without architectural modifications or grounding-specific components and is trained for high-fidelity
image synthesis, providing strong spatial control within a general large-scale and disentangle model, also allowing
intuitive refinement. Best results are in bold; second best are underlined.
COCO
LVIS
Method
AP
AP50
AR
AP
AP50
APs
APm
APl
APr
APc
APf
Upper bound (real images)
50.2
66.7
61.0
44.6
57.7
33.2
55.0
66.1
31.4
44.5
50.5
Flux.2 Pro
3.5
8.7
4.6
2.1
4.8
0.1
0.8
7.3
0.1
0.2
2.4
Nano Banana Pro
5
11.3
5.5
4.1
10.6
0.1
1
15.9
3.3
4
3.9
GLIGEN [25]
19.6
35.0
30.7
9.9
9.5
1.6
10.5
31.1
7.4
10.0
10.9
BBQ (ours)
28.6
40.9
38.2
13.1
20.1
1.6
13.9
37.4
13.1
14.0
12.7
InstanceDiffusion [26]
38.8
55.4
52.9
17.9
25.5
5.5
24.2
45.0
12.7
18.7
19.3
Table 3: Color fidelity comparison. ∆E00 (CIEDE2000) measures perceptual color difference, while a–b distance
captures chromaticity (hue and saturation) independently of lightness. We report mean, median, and 90th percentile
(p90), where lower values indicate better color accuracy.. Across both K = 5 and K = 8, BBQ achieves the lowest
a–b errors in all statistics, indicating the most accurate chromaticity control and fewer severe failures, while remaining
competitive under ∆E00 that penalizes lightness differences. Best results are in bold and second-best are underlined
(computed per K).
K
Model
a–b Mean↓a–b Median↓a–b p90↓∆E00 Mean↓∆E00 Median↓∆E00 p90↓
5
BBQ (ours)
7.16
6.67
13.30
5.93
5.76
9.62
Nano Banana Pro
10.91
7.52
20.80
6.50
5.72
11.00
FLUX.2 Pro
10.07
8.16
19.30
6.64
6.12
10.17
FIBO
10.32
9.44
20.36
6.74
7.32
10.52
8
BBQ (ours)
7.48
6.23
14.33
5.74
5.07
9.89
Nano Banana Pro
10.64
6.87
21.05
5.91
4.82
10.80
FLUX.2 Pro
9.50
8.26
17.98
5.67
5.42
9.99
FIBO
11.07
9.62
20.52
6.99
5.90
11.03
noise from other parts of the image. Therefore, we gen-
erated 200 images depicting single objects on white back-
ground, where each object was assigned a specific target
RGB color in the prompt. For evaluation, we extract ob-
ject pixels by masking out the white background using
foreground segmentation, and then apply K-means clus-
tering (with K = 5 and K = 8) in CIELab color space on
the extracted object pixels to identify the dominant color
palette. Clusters representing less than 5% of object pixels
are filtered out. Among the remaining clusters, we select
the one with the minimum distance to the target color. We
report two distance metrics: ∆E00 (CIEDE2000), which
measures perceptual color difference, and Euclidean dis-
tance in the a-b chromaticity plane, which isolates hue
and saturation differences independently of light.
For
both metrics, we report mean, median, and 90th percentile
(p90) statistics, where p90 captures tail behavior and ro-
bustness to difficult cases that may not be reflected by
central tendency alone. Like in TaBR, BBQ and FIBO
utilize their native structured schemas for compatibility,
where for FIBO we ask the VLM to choose the name of
the color that best describes the RGB. For Flux.2 Pro we
follow the prompting guide [61] and for Nano Banana Pro
we’ve found that the best results are achieved with the
same prompts as Flux.
4.2
Qualitative Results
In Figure 4, we present TaBR reconstructions, where BBQ
faithfully preserves the original pose, object relationships,
and overall scene layout. Figure 5 illustrates BBQ’s abil-
ity to follow explicit numeric color specifications: when
conditioned on exact RGB values, the model produces
visually accurate object colors and remains competitive
with state-of-the-art baselines. Figure 6 provides qual-
itative comparisons for bounding-box grounding against
strong general-purpose models, Nano Banana Pro and
Flux.2 Pro. While these baselines often struggle to sat-
7


## Page 8


isfy explicit numeric box constraints, BBQ consistently
aligns object placement with the specified regions, mo-
tivating our subsequent quantitative comparison against
dedicated layout-aware approaches such as InstanceDif-
fusion and GLIGEN. Additional results are presented in
Figure 7 demonstrating the effectiveness of our approach.
4.3
Quantitative Results
Text-as-a-Bottleneck.
Table 1 reports image-level pair-
wise preference results for the TaBR evaluation. We re-
port the win rate of BBQ as the fraction of images where
it is preferred over the competing model among decisive
outcomes (ties ignored), together with 95% Wilson score
confidence intervals. As shown in the table, BBQ consis-
tently outperforms its predecessor FIBO as well as state-
of-the-art general-purpose text-to-image models, includ-
ing Nano Banana Pro and Flux.2 Pro, demonstrating that
incorporating explicit numeric parameters improves re-
construction fidelity without sacrificing global coherence.
Bounding-box accuracy.
Table 2 evaluates spatial
grounding under box-conditioned prompts on COCO and
LVIS. Across both datasets, BBQ consistently outper-
forms strong text-to-image baselines such as Nano Ba-
nana Pro and Flux.2 Pro, as well as the dedicated ground-
ing model GLIGEN, while trailing the current state-of-
the-art InstanceDiffusion. These results position BBQ as
a strong non-specialized alternative for box-conditioned
generation.
Unlike InstanceDiffusion and GLIGEN,
which rely on grounding-specific architectural modifica-
tions or inference-time alignment mechanisms, BBQ is
trained at a substantially larger scale for general high-
fidelity image synthesis, achieving strong bounding-box
alignment without sacrificing expressiveness, inference
time or requiring specialized components. Furthermore,
unlike InstanceDiffusion, BBQ exhibits native disentan-
glement that enables intuitive parametric refinement, as
illustrated in Fig. 7 and Fig. 3
Color-conditioning accuracy.
Table 3 reports color fi-
delity using two complementary metrics. We primarily
focus on Euclidean distance in the a–b chromaticity plane,
which isolates hue and saturation differences while ig-
noring lighting, making it better aligned with our goal
of precise parametric color control independent of illu-
mination and shading. Under this metric, BBQ consis-
tently outperforms all competing models for both K = 5
and K = 8, achieving the lowest mean, median, and
90th-percentile errors, and indicating both superior aver-
age accuracy and substantially fewer severe failures. We
also report CIEDE2000 (∆E00), which penalizes light-
ness variation; some baselines achieve lower scores via
more uniform lighting, whereas BBQ preserves accurate
chromaticity under realistic lighting.
5
Conclusion
In this work, we introduced BBQ, a large-scale text-to-
image model that enables precise control over object lo-
cation, size, and color, through explicit numeric bound-
ing boxes and RGB values. BBQ directly addresses the
parametric gap between descriptive language and the de-
terministic numeric control required in professional work-
flows, demonstrating that such precision can be achieved
purely through large-scale training on enriched structured
captions, without architectural modifications or inference-
time optimization.
More broadly, BBQ highlights the
power of structured intermediate representations as a
bridge between user intent and generative rendering. By
translating natural-language prompts into a parametric
schema that supports direct numeric manipulation, our
framework enables intuitive interactive interfaces, such
as object repositioning and precise color selection, while
maintaining global scene coherence. This approach sug-
gests a path toward programmable, professional-grade im-
age synthesis systems that integrate additional precise
attributes, moving beyond descriptive prompting toward
truly controllable generative modeling.
References
[1] Eyal Gutflaish, Eliran Kachlon, Hezi Zisman, Tal
Hacham, Nimrod Sarid, Alexander Visheratin, Saar
Huberman, Gal Davidi, Guy Bukchin, Kfir Gold-
berg, et al. Generating an image from 1,000 words:
Enhancing text-to-image with structured captions.
arXiv preprint arXiv:2511.06876, 2025.
[2] Siyu Cao, Hangting Chen, Peng Chen, Yiji Cheng,
Yutao Cui, Xinchi Deng, Ying Dong, Kipper Gong,
Tianpeng Gu, Xiusen Gu, et al. Hunyuanimage 3.0
technical report. arXiv preprint arXiv:2509.23951,
2025.
[3] Stephen Batifol, Andreas Blattmann, Frederic Boe-
sel, Saksham Consul, Cyril Diagne, Tim Dockhorn,
Jack English, Zion English, Patrick Esser, Sumith
Kulal, et al. Flux. 1 kontext: Flow matching for in-
context image generation and editing in latent space.
arXiv e-prints, pages arXiv–2506, 2025.
[4] Alex Nichol, Prafulla Dhariwal, Aditya Ramesh,
Pranav Shyam, Pamela Mishkin, Bob McGrew, Ilya
Sutskever, and Mark Chen. Glide: Towards photore-
alistic image generation and editing with text-guided
8


## Page 9


diffusion models. arXiv preprint arXiv:2112.10741,
2021.
[5] Chitwan Saharia, William Chan, Saurabh Sax-
ena, Lala Li, Jay Whang, Emily L Denton, Kam-
yar Ghasemipour, Raphael Gontijo Lopes, Burcu
Karagol Ayan, Tim Salimans, et al. Photorealistic
text-to-image diffusion models with deep language
understanding. Advances in neural information pro-
cessing systems, 35:36479–36494, 2022.
[6] Aditya Ramesh, Prafulla Dhariwal, Alex Nichol,
Casey Chu, and Mark Chen.
Hierarchical text-
conditional image generation with clip latents. arXiv
preprint arXiv:2204.06125, 1(2):3, 2022.
[7] Robin Rombach,
Andreas Blattmann,
Dominik
Lorenz, Patrick Esser, and Bj¨orn Ommer.
High-
resolution image synthesis with latent diffusion
models. In Proceedings of the IEEE/CVF conference
on computer vision and pattern recognition, pages
10684–10695, 2022.
[8] Dustin Podell, Zion English, Kyle Lacey, Andreas
Blattmann, Tim Dockhorn, Jonas M¨uller, Joe Penna,
and Robin Rombach. Sdxl: Improving latent dif-
fusion models for high-resolution image synthesis.
arXiv preprint arXiv:2307.01952, 2023.
[9] Patrick Esser, Sumith Kulal, Andreas Blattmann,
Rahim Entezari, Jonas M¨uller, Harry Saini, Yam
Levi, Dominik Lorenz, Axel Sauer, Frederic Boesel,
et al. Scaling rectified flow transformers for high-
resolution image synthesis.
In Forty-first interna-
tional conference on machine learning, 2024.
[10] Black Forest Labs.
Flux.
https://github.
com/black-forest-labs/flux, 2024.
[11] Bingchen Liu, Ehsan Akhgari, Alexander Visher-
atin, Aleks Kamko, Linmiao Xu, Shivam Shrirao,
Chase Lambert, Joao Souza, Suhail Doshi, and
Daiqing Li.
Playground v3:
Improving text-to-
image alignment with deep-fusion large language
models. arXiv preprint arXiv:2409.10695, 2024.
[12] Qi Cai, Jingwen Chen, Yang Chen, Yehao Li,
Fuchen Long, Yingwei Pan, Zhaofan Qiu, Yiheng
Zhang, Fengbin Gao, Peihan Xu, et al. Hidream-i1:
A high-efficient image generative foundation model
with sparse diffusion transformer.
arXiv preprint
arXiv:2505.22705, 2025.
[13] Chenfei Wu, Jiahao Li, Jingren Zhou, Junyang Lin,
Kaiyuan Gao, Kun Yan, Sheng ming Yin, Shuai Bai,
Xiao Xu, Yilei Chen, Yuxiang Chen, Zecheng Tang,
Zekai Zhang, Zhengyi Wang, An Yang, Bowen
Yu, Chen Cheng, Dayiheng Liu, Deqing Li, Hang
Zhang, Hao Meng, Hu Wei, Jingyuan Ni, Kai Chen,
Kuan Cao, Liang Peng, Lin Qu, Minggang Wu, Peng
Wang, Shuting Yu, Tingkun Wen, Wensen Feng, Xi-
aoxiao Xu, Yi Wang, Yichang Zhang, Yongqiang
Zhu, Yujia Wu, Yuxuan Cai, and Zenan Liu. Qwen-
image technical report, 2025.
URL https://
arxiv.org/abs/2508.02324.
[14] Christoph Schuhmann, Romain Beaumont, Richard
Vencu, Cade Gordon, Ross Wightman, Mehdi
Cherti, Theo Coombes, Aarush Katta, Clayton
Mullis, Mitchell Wortsman, et al.
Laion-5b: An
open large-scale dataset for training next generation
image-text models. Advances in neural information
processing systems, 35:25278–25294, 2022.
[15] James Betker, Gabriel Goh, Li Jing, Tim Brooks,
Jianfeng Wang, Linjie Li, Long Ouyang, Juntang
Zhuang, Joyce Lee, Yufei Guo, et al. Improving im-
age generation with better captions. Computer Sci-
ence. https://cdn. openai. com/papers/dall-e-3. pdf,
2(3):8, 2023.
[16] Bo Zhao, Lili Meng, Weidong Yin, and Leonid Si-
gal. Image generation from layout. In Proceedings
of the IEEE/CVF conference on computer vision and
pattern recognition, pages 8584–8593, 2019.
[17] Wei Sun and Tianfu Wu. Image synthesis from re-
configurable layout and style. In Proceedings of the
IEEE/CVF International Conference on Computer
Vision, pages 10531–10540, 2019.
[18] Yandong Li, Yu Cheng, Zhe Gan, Licheng Yu,
Liqiang Wang, and Jingjing Liu. Bachgan: High-
resolution image synthesis from salient object lay-
out.
In Proceedings of the IEEE/CVF conference
on computer vision and pattern recognition, pages
8365–8374, 2020.
[19] Stanislav Frolov, Avneesh Sharma, J¨orn Hees,
Tushar Karayil, Federico Raue, and Andreas Den-
gel. Attrlostgan: Attribute controlled image synthe-
sis from reconfigurable layout and style. In DAGM
German Conference on Pattern Recognition, pages
361–375. Springer, 2021.
[20] Zejian Li, Jingyu Wu, Immanuel Koh, Yongchuan
Tang, and Lingyun Sun. Image synthesis from lay-
out with locality-aware mask adaption. In Proceed-
ings of the IEEE/CVF International Conference on
Computer Vision, pages 13819–13828, 2021.
[21] Zuopeng Yang, Daqing Liu, Chaoyue Wang, Jie
Yang, and Dacheng Tao. Modeling image composi-
tion for complex scene generation. In Proceedings of
9


## Page 10


the IEEE/CVF Conference on Computer Vision and
Pattern Recognition, pages 7764–7773, 2022.
[22] Wan-Cyuan Fan, Yen-Chun Chen, DongDong Chen,
Yu Cheng, Lu Yuan, and Yu-Chiang Frank Wang.
Frido: Feature pyramid diffusion for complex scene
image synthesis. In Proceedings of the AAAI con-
ference on artificial intelligence, volume 37, pages
579–587, 2023.
[23] Tsung-Yi Lin, Michael Maire, Serge Belongie,
James Hays, Pietro Perona, Deva Ramanan, Piotr
Doll´ar, and C Lawrence Zitnick. Microsoft coco:
Common objects in context. In European confer-
ence on computer vision, pages 740–755. Springer,
2014.
[24] Zhengyuan Yang, Jianfeng Wang, Zhe Gan, Lin-
jie Li, Kevin Lin, Chenfei Wu, Nan Duan, Zicheng
Liu, Ce Liu, Michael Zeng, et al. Reco: Region-
controlled text-to-image generation. In Proceedings
of the IEEE/CVF Conference on Computer Vision
and Pattern Recognition, pages 14246–14255, 2023.
[25] Yuheng Li, Haotian Liu, Qingyang Wu, Fangzhou
Mu, Jianwei Yang, Jianfeng Gao, Chunyuan Li, and
Yong Jae Lee. Gligen: Open-set grounded text-to-
image generation. In Proceedings of the IEEE/CVF
conference on computer vision and pattern recogni-
tion, pages 22511–22521, 2023.
[26] Xudong Wang, Trevor Darrell, Sai Saketh Ramb-
hatla, Rohit Girdhar, and Ishan Misra. Instancediffu-
sion: Instance-level control for image generation. In
Proceedings of the IEEE/CVF conference on com-
puter vision and pattern recognition, pages 6232–
6242, 2024.
[27] Yutong Feng, Biao Gong, Di Chen, Yujun Shen,
Yu Liu, and Jingren Zhou.
Ranni: Taming text-
to-image diffusion for accurate instruction follow-
ing. In Proceedings of the IEEE/CVF Conference
on Computer Vision and Pattern Recognition, pages
4744–4753, 2024.
[28] Lvmin Zhang, Anyi Rao, and Maneesh Agrawala.
Adding conditional control to text-to-image diffu-
sion models. In Proceedings of the IEEE/CVF In-
ternational Conference on Computer Vision (ICCV),
pages 3836–3847, 2023.
[29] Lianghua Huang, Di Chen, Yu Liu, Yujun Shen,
Deli Zhao, and Jingren Zhou.
Composer: Cre-
ative and controllable image synthesis with compos-
able conditions. In Proceedings of the 40th Inter-
national Conference on Machine Learning (ICML),
pages 13753–13773, 2023.
[30] Jinheng
Xie,
Yuexiang
Li,
Yawen
Huang,
Haozhe
Liu,
Wentian
Zhang,
Yefeng
Zheng,
and Mike Zheng Shou.
Boxdiff: Text-to-image
synthesis with training-free box-constrained diffu-
sion. In Proceedings of the IEEE/CVF International
Conference on Computer Vision, pages 7452–7461,
2023.
[31] Omer Bar-Tal, Lior Yariv, Yaron Lipman, and Tali
Dekel. Multidiffusion: Fusing diffusion paths for
controlled image generation. In Proceedings of the
40th International Conference on Machine Learning
(ICML), pages 1737–1752, 2023.
[32] Erik Reinhard, Michael Adhikhmin, Bruce Gooch,
and Peter Shirley. Color transfer between images.
IEEE Computer graphics and applications, 21(5):
34–41, 2002.
[33] Tomihisa Welsh, Michael Ashikhmin, and Klaus
Mueller. Transferring color to greyscale images. In
Proceedings of the 29th annual conference on Com-
puter graphics and interactive techniques, pages
277–280, 2002.
[34] Anat Levin, Dani Lischinski, and Yair Weiss. Col-
orization using optimization. In ACM SIGGRAPH
2004 Papers, pages 689–694. 2004.
[35] Huiwen Chang, Ohad Fried, Yiming Liu, Stephen
DiVerdi, and Adam Finkelstein. Palette-based photo
recoloring. ACM Trans. Graph., 34(4):139–1, 2015.
[36] Elad Aharoni-Mack, Yakov Shambik, and Dani
Lischinski. Pigment-based recoloring of watercolor
paintings. In Proceedings of the Symposium on Non-
Photorealistic Animation and Rendering, pages 1–
11, 2017.
[37] Richard Zhang, Phillip Isola, and Alexei A Efros.
Colorful image colorization.
In European confer-
ence on computer vision, pages 649–666. Springer,
2016.
[38] Richard Zhang, Jun-Yan Zhu, Phillip Isola, Xinyang
Geng, Angela S Lin, Tianhe Yu, and Alexei A
Efros.
Real-time user-guided image coloriza-
tion with learned deep priors.
arXiv preprint
arXiv:1705.02999, 2017.
[39] Chenyang Lei and Qifeng Chen.
Fully automatic
video colorization with self-regularization and diver-
sity. In Proceedings of the IEEE/CVF conference
on computer vision and pattern recognition, pages
3753–3761, 2019.
10


## Page 11


[40] Jheng-Wei Su, Hung-Kuo Chu, and Jia-Bin Huang.
Instance-aware image colorization. In Proceedings
of the IEEE/CVF conference on computer vision and
pattern recognition, pages 7968–7977, 2020.
[41] Yanze Wu, Xintao Wang, Yu Li, Honglun Zhang,
Xun Zhao, and Ying Shan. Towards vivid and di-
verse image colorization with generative color prior.
In Proceedings of the IEEE/CVF international con-
ference on computer vision, pages 14377–14386,
2021.
[42] Satoshi Iizuka, Edgar Simo-Serra, and Hiroshi
Ishikawa. Let there be color! joint end-to-end learn-
ing of global and local image priors for automatic
image colorization with simultaneous classification.
ACM Transactions on Graphics (ToG), 35(4):1–11,
2016.
[43] Hyojin Bahng, Seungjoo Yoo, Wonwoong Cho,
David Keetae Park, Ziming Wu, Xiaojuan Ma, and
Jaegul Choo.
Coloring with words: Guiding im-
age colorization through text-based palette genera-
tion. In Proceedings of the european conference on
computer vision (eccv), pages 431–447, 2018.
[44] Yi Wang, Menghan Xia, Lu Qi, Jing Shao, and
Yu Qiao. Palgan: Image colorization with palette
generative adversarial networks.
In European
Conference on Computer Vision, pages 271–288.
Springer, 2022.
[45] Muhammad Atif Butt, Kai Wang, Javier Vazquez-
Corral, and Joost van de Weijer. Colorpeel: Color
prompt learning with diffusion models via color and
shape disentanglement. In European Conference on
Computer Vision, pages 456–472. Springer, 2024.
[46] Alexander Lobashev, Maria Larchenko, and Dmitry
Guskov.
Color
conditional
generation
with
sliced
wasserstein
guidance.
arXiv
preprint
arXiv:2503.19034, 2025.
[47] Tripti Shukla, Srikrishna Karanam, and Balaji Vasan
Srinivasan.
Test-time conditional text-to-image
synthesis using diffusion models.
arXiv preprint
arXiv:2411.10800, 2024.
[48] H´ector Laria, Alexandra Gomez-Villa, Jiang Qin,
Muhammad Atif Butt, Bogdan Raducanu, Javier
Vazquez-Corral, Joost van de Weijer, and Kai Wang.
Leveraging semantic attribute binding for free-lunch
color control in diffusion models.
arXiv preprint
arXiv:2503.09864, 2025.
[49] Gheorghe Comanici, Eric Bieber, Mike Schaek-
ermann, Ice Pasupat, Noveen Sachdeva, Inderjit
Dhillon, Marcel Blistein, Ori Ram, Dan Zhang,
Evan Rosen, et al. Gemini 2.5: Pushing the frontier
with advanced reasoning, multimodality, long con-
text, and next generation agentic capabilities. arXiv
preprint arXiv:2507.06261, 2025.
[50] Nikhila Ravi, Valentin Gabeur, Yuan-Ting Hu,
Ronghang Hu,
Chaitanya Ryali,
Tengyu Ma,
Haitham Khedr, Roman R¨adle, Chloe Rolland,
Laura
Gustafson,
Eric
Mintun,
Junting
Pan,
Kalyan Vasudev Alwala, Nicolas Carion, Chao-
Yuan
Wu,
Ross
Girshick,
Piotr
Doll´ar,
and
Christoph Feichtenhofer.
Sam 2: Segment any-
thing in images and videos.
arXiv preprint
arXiv:2408.00714,
2024.
URL
https://
arxiv.org/abs/2408.00714.
[51] Lihe Yang, Bingyi Kang, Zilong Huang, Zhen Zhao,
Xiaogang Xu, Jiashi Feng, and Hengshuang Zhao.
Depth anything v2. arXiv:2406.09414, 2024.
[52] qTipTip.
Pylette,
2025.
URL https://
qtiptip.github.io/Pylette/.
[53] Ilya Loshchilov and Frank Hutter.
Decou-
pled weight decay regularization.
arXiv preprint
arXiv:1711.05101, 2017.
[54] Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu,
Maximilian Nickel, and Matt Le. Flow matching for
generative modeling, 2023.
[55] Bram Wallace, Meihua Dang, Rafael Rafailov, Linqi
Zhou, Aaron Lou, Senthil Purushwalkam, Stefano
Ermon, Caiming Xiong, Shafiq Joty, and Nikhil
Naik.
Diffusion model alignment using direct
preference optimization.
In Proceedings of the
IEEE/CVF Conference on Computer Vision and Pat-
tern Recognition, pages 8228–8238, 2024.
[56] Jie Liu, Gongye Liu, Jiajun Liang, Ziyang Yuan, Xi-
aokun Liu, Mingwu Zheng, Xiele Wu, Qiulin Wang,
Wenyu Qin, Menghan Xia, et al. Improving video
generation with human feedback.
arXiv preprint
arXiv:2501.13918, 2025.
[57] Shuai Bai, Yuxuan Cai, Ruizhe Chen, Keqin Chen,
Xionghui Chen, Zesen Cheng, Lianghao Deng, Wei
Ding, Chang Gao, Chunjiang Ge, Wenbin Ge, Zhi-
fang Guo, Qidong Huang, Jie Huang, Fei Huang,
Binyuan Hui, Shutong Jiang, Zhaohai Li, Ming-
sheng Li, Mei Li, Kaixin Li, Zicheng Lin, Junyang
Lin, Xuejing Liu, Jiawei Liu, Chenglong Liu, Yang
Liu, Dayiheng Liu, Shixuan Liu, Dunjie Lu, Ruilin
Luo, Chenxu Lv, Rui Men, Lingchen Meng, Xu-
ancheng Ren, Xingzhang Ren, Sibo Song, Yuchong
Sun, Jun Tang, Jianhong Tu, Jianqiang Wan, Peng
11


## Page 12


Wang, Pengfei Wang, Qiuyue Wang, Yuxuan Wang,
Tianbao Xie, Yiheng Xu, Haiyang Xu, Jin Xu,
Zhibo Yang, Mingkun Yang, Jianxin Yang, An Yang,
Bowen Yu, Fei Zhang, Hang Zhang, Xi Zhang,
Bo Zheng, Humen Zhong, Jingren Zhou, Fan Zhou,
Jing Zhou, Yuanzhi Zhu, and Ke Zhu.
Qwen3-vl
technical report. arXiv preprint arXiv:2511.21631,
2025.
[58] Enneng Yang, Li Shen, Guibing Guo, Xingwei
Wang, Xiaochun Cao, Jie Zhang, and Dacheng Tao.
Model merging in llms, mllms, and beyond: Meth-
ods, theories, applications and opportunities. arXiv
preprint arXiv:2408.07666, 2024.
[59] Glenn Jocher, Jing Qiu, and Ayush Chaurasia. Ul-
tralytics YOLO, January 2023.
URL https://
github.com/ultralytics/ultralytics.
[60] Agrim Gupta, Piotr Dollar, and Ross Girshick. Lvis:
A dataset for large vocabulary instance segmenta-
tion. In Proceedings of the IEEE/CVF conference
on computer vision and pattern recognition, pages
5356–5364, 2019.
[61] Black Forest Labs. Prompting guide – flux.2 [pro]
& [max], 2025.
URL https://docs.bfl.
ai/guides/prompting_guide_flux2. Ac-
cessed: 2026-02-02.
12


## Page 13


A
Additional Refinement Examples
Original
Refined
Refined with overlaid bounding boxes
Figure 7: Refinement via structured parametric editing. The left column shows the original generations, while
the middle column presents refined results obtained by editing the structured parametric caption and re-generating
the image. In each example, both the numeric bounding boxes (object position and extent) and the object color are
modified, explicitly enforcing the target color #DD20A7, resulting in updated spatial layout and appearance while
preserving overall scene coherence. The right column overlays the exact numeric bounding boxes on the refined
images, illustrating precise alignment with the edited parameters.
13
