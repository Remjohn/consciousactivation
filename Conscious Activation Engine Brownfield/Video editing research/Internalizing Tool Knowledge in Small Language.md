# Internalizing Tool Knowledge in Small Language

*Source PDF: `Internalizing Tool Knowledge in Small Language.pdf`*

*Total Pages: 9*

---


## Page 1


Internalizing Tool Knowledge in Small Language
Models via QLoRA Fine-Tuning
Yuval Shemla∗, Ayal Yakobe†, Tanmay Agarwal†, Dhaval Patel‡, Kaoutar El Maghraoui†
∗Columbia School of General Studies, Columbia University, NY, USA
†Columbia Engineering, Columbia University, NY, USA
‡IBM Research, NY, USA
ys3571@columbia.edu, amy2127@columbia.edu, ta2830@columbia.edu, pateldha@us.ibm.com, kaoutar@cs.columbia.edu
Abstract—Tool-using language agents commonly include full
tool schemas in every prompt, even when the available tools are
fixed across many queries. This repeated schema context increases
input length and can make small models unreliable planners. We
study whether small language models can internalize a fixed
tool catalog through supervised parameter-efficient fine-tuning,
enabling structured tool planning without explicit tool descriptions
at inference time.
Using AssetOpsBench, an industrial asset-operations bench-
mark with MCP-style tools, we fine-tune Gemma 4 E4B and
Qwen3-4B with 8-bit QLoRA on approximately 1,700 tool-
use examples. Under description-free inference, the fine-tuned
models outperform an unfine-tuned schema-informed baseline
that receives the full tool catalog, while reducing prompt length
by 94.7%. The best Gemma run achieves an AT-F1 of 0.65 and
an overall LLM-judge score of 3.88, compared with 0.47 and 2.88
for the informed baseline.
These results suggest that, for fixed tool catalogs, supervised
QLoRA fine-tuning can shift tool knowledge from prompt context
into adapter weights, reducing repeated schema overhead while
maintaining or improving tool-planning quality.
I. INTRODUCTION
Large language models (LLMs) are increasingly used as
planning components in tool-using agents, where they de-
compose user requests, select tools, construct arguments, and
coordinate multi-step workflows. In many current tool-use
pipelines, including MCP-style systems [1], the model receives
a serialized tool catalog in the prompt so that it can infer
which tools exist and how they should be called. This schema-
informed approach is flexible: new tools can be added by
updating the prompt. However, it also repeats the same catalog
across queries, creating substantial input overhead.
This paper studies a narrower but practically important
regime: fixed-catalog tool planning. In many enterprise and
industrial deployments, the available tool catalog changes
slowly relative to the number of user queries. In such settings,
repeatedly prompting with full tool descriptions may be
unnecessary. We ask whether this stable catalog knowledge can
instead be amortized into a small model through supervised
fine-tuning, allowing the model to generate structured tool-use
plans without receiving tool descriptions at inference time.
This setting targets two related inefficiencies. First, small
language models often require extensive tool-context prompting
to produce valid plans. Second, repeated schema prompting can
dominate the input budget. In our AssetOpsBench setting [2],
the serialized tool catalog accounts for approximately 2,200
of the 2,400 prompt tokens, while the user query itself is
short. Description-free inference removes this catalog section
entirely, reducing the prompt to approximately 128 tokens and
asking the fine-tuned model to recover server routing, tool
selection, argument keys, and dependency structure from its
learned parameters.
A. Contributions
We propose and evaluate description-free tool planning:
a fixed-catalog setting in which the model must generate
structured tool-use plans without receiving tool descriptions at
inference time. Our contributions are:
1) We formalize static-catalog description-free tool planning,
where a model must select MCP servers, tools, arguments,
and dependencies for a fixed catalog while omitting the
serialized tool catalog from the inference prompt.
2) We develop a catalog-grounded supervised fine-tuning
protocol in which a teacher model has access to full tool
schemas during data construction, while the student model
is trained and evaluated with the tool catalog removed.
3) We show that 8-bit QLoRA fine-tuning on approximately
1,700 examples enables ∼4B parameter models to out-
perform an unfine-tuned schema-informed baseline on
AssetOpsBench, despite receiving no tool descriptions at
inference time.
4) We evaluate whether the resulting specialization preserves
broader model capability, showing that LoRA rank in-
duces a quality–retention trade-off between tool-planning
performance and general multiple-choice accuracy.
II. RELATED WORK
A. Tool-Use and Function-Calling Evaluation
Tool-use evaluation has evolved from measuring whether
models can call individual APIs to testing tool selection,
argument construction, dependency tracking, and multi-step
execution. API-Bank [3] introduced a runnable benchmark for
tool-augmented LLMs with 73 API tools. BFCL [4] evaluates
function calling across serial and parallel invocations using
AST-based evaluation. MCP-Bench [5] extends this to MCP-
style agents, evaluating multi-step tasks that require cross-tool
coordination across live MCP servers. Our work does not
propose a new benchmark; instead, we study a stricter inference
arXiv:2605.17774v2  [cs.CL]  26 May 2026


## Page 2


condition within a fixed-domain benchmark: the model must
plan without receiving tool descriptions at inference time.
B. Schema-Informed and Retrieval-Augmented Tool Learning
A dominant approach to tool use is to expose tool information
at inference time through prompt schemas or retrieved documen-
tation. Gorilla [6] fine-tunes models for API invocation with
retrieval-aware training. ToolLLM [7] constructs ToolBench
over 16,464 real-world APIs with a neural API retriever.
ToolACE [8] shows that high-quality synthetic function-calling
data with automatic verification can train strong small models.
These approaches are well suited to broad or changing API
ecosystems. Our setting makes the opposite trade-off: we
assume a fixed, mature tool catalog and ask whether its schema
information can be amortized into model parameters.
C. Tool and Skill Internalization
Recent work has begun to move tool or skill knowledge
from prompt context into model parameters. ToolGen [9]
represents each tool as a unique vocabulary token, integrating
tool knowledge into the language model’s generation process
and enabling unified tool retrieval and calling across over
47,000 tools. SKILL0 [10] studies skill internalization for
embodied agents by providing skill context during RL training
and progressively withdrawing it until the agent operates
without runtime skill retrieval. Our work is motivated by the
same observation, prompt-time tool context is expensive, but
uses a different approach: ordinary supervised fine-tuning with
QLoRA on a fixed industrial catalog, without special tool
tokens, vocabulary expansion, or reinforcement learning.
D. Prompt Compression and Schema Removal
Prompt-compression methods such as LLMLingua [11]
reduce inference cost by removing less important prompt
tokens. Description-free tool planning can be viewed as an
extreme fixed-catalog variant of prompt compression: rather
than compressing the tool catalog, we remove the entire
serialized schema from the inference prompt. The missing
catalog information must therefore be recovered from the fine-
tuned model weights rather than from a shorter prompt. Unlike
standard knowledge distillation [12], we do not require teacher
model inference at test time.
E. Parameter-Efficient Fine-Tuning and Retention
LoRA [13] freezes the pretrained model and trains low-rank
adapter updates, while QLoRA [14] further reduces memory
by quantizing the frozen base model. Although adapter-based
fine-tuning generally reduces catastrophic forgetting compared
with full fine-tuning [15], adapter updates can still bias the
effective model toward the fine-tuning distribution and degrade
prior capabilities. This is especially relevant for tool planning,
where the training distribution consists of structured plans
rather than general natural language. We therefore evaluate
both tool-planning quality and general multiple-choice retention
after fine-tuning.
F. Industrial Tool-Planning Benchmarks
We use AssetOpsBench [2] because it provides a bounded
but realistic industrial tool-planning environment with domain-
specific MCP servers, simulated telemetry, human-authored
scenarios, and multi-step workflows. This differs from broad
benchmarks such as ToolBench [7] and MCP-Bench [5], which
evaluate large-scale tool discovery or cross-domain MCP usage.
Our goal is not broad generalization to unseen tools, but
controlled evaluation of whether a stable MCP-style catalog
can be internalized into a small model.
III. PROBLEM DEFINITION
We formalize the setting studied in this paper as description-
free tool planning for a fixed tool catalog. Let T denote a
tool catalog containing a set of MCP servers, tools, argument
schemas, return types, and natural-language tool descriptions.
A user query is denoted by x, and the desired output is a
structured plan y = (s1, . . . , sn) consisting of ordered planning
steps. Each step si specifies a task description, an MCP server,
a tool, a JSON argument object, dependencies on previous
steps, and an expected output.
In standard schema-informed tool planning, the model
receives both the user query and a serialized representation of
the tool catalog, denoted d(T ). The model therefore generates
plans according to
pθ(y | x, d(T )),
(1)
where θ are the parameters of the pretrained model. This
is the common prompting paradigm used by many tool-use
systems: every query is accompanied by the full or partial tool
catalog so the model can infer which tools exist and how they
should be called.
In contrast, description-free tool planning removes the
serialized catalog from the inference-time prompt. The model
must instead generate a valid plan using only the user query
and the structured output format:
pθ′(y | x),
(2)
where θ′ denotes the parameters of the model after tool-use
fine-tuning. The goal is for θ′ to encode enough information
about T
to recover correct server routing, tool selection,
argument construction, and dependency ordering without seeing
d(T ) at inference time.
This setting differs from general open-ended tool use in
an important way: the tool catalog is assumed to be fixed
during evaluation. We do not attempt to generalize to unseen
tools. Instead, we study whether knowledge of a stable catalog
can be shifted from prompt context into model parameters.
This creates a trade-off between adaptability and efficiency.
Prompt-based methods can immediately support new tools by
adding their descriptions to the prompt, while description-free
fine-tuning reduces prompt length and inference overhead but
requires additional training or adapter updates when the tool
catalog changes.


## Page 3


Standard
schema-
informed
planning
Description-free
fine-tuned
planning
User query
x
Tool catalog
d(T )
servers,
tools, args
Base LLM planner
pθ(y | x, d(T ))
Structured
tool plan
y = (s1, . . . , sn)
MCP servers
and tools
Tool knowledge
repeated in
every prompt
∼2,400 input tokens
QLoRA fine-tuning
on tool-use examples
User query
x
QLoRA fine-tuned
small LM
pθ′(y | x)
Structured
tool plan
y = (s1, . . . , sn)
MCP servers
and tools
Tool knowledge
internalized in
adapter weights
∼128 input tokens
94.7%
prompt-token reduction
Fixed-catalog trade-off: prompt-time
adaptability vs. inference-time efficiency
Fig. 1. Schema-informed versus description-free tool planning. Standard prompting supplies the user query and serialized tool catalog d(T ) at each call, while
QLoRA internalizes fixed-catalog tool knowledge into adapter weights, enabling MCP tool-use planning from the query alone.
Following the AssetOpsBench output format, generated
plans use the field name #Agent to identify the responsible
component. In our MCP setting, this field corresponds to the
MCP server responsible for the tool call. We use “server” in
prose and preserve #Agent when referring to the literal output
format.
We evaluate this setting using four criteria. First, the
generated plan must select the correct MCP servers and tools.
Second, it must construct valid argument keys and values for
each selected tool. Third, it must order tool calls into a coherent
dependency structure. Fourth, it should achieve these objectives
while reducing prompt length relative to schema-informed
prompting. The central question of this work is therefore:
Can a small language model internalize a fixed tool
catalog through parameter-efficient fine-tuning, al-
lowing it to outperform schema-informed prompting
while omitting tool descriptions at inference time?
IV. METHODOLOGY
We evaluate whether supervised fine-tuning can substitute
for prompt-time tool descriptions in a fixed-catalog setting. The
experiments compare schema-informed prompting, description-
free prompting without fine-tuning, and description-free prompt-
ing after QLoRA fine-tuning. We then analyze adapter rank
and capability retention to quantify the cost of specialization.
A. Benchmark and Data
a) Catalog-grounded description-free SFT.: We use a
teacher–student data construction protocol. During data con-
struction, the teacher model (Gemini 2.5 Flash [16]) receives
the full serialized catalog d(T ) and produces schema facts,
question-to-plan mappings, and execution-style traces. During
student training and evaluation, the serialized catalog is
TABLE I
ASSETOPSBENCH MCP SERVER INVENTORY USED IN THIS WORK
MCP Server
Tools
IoT
4
FMSR
2
TSFM
6
Utilities
3
WorkOrder
8
removed from the prompt. The student observes only the user
query, output-format instructions, and target plan, forcing the
adapter to encode tool names, server ownership, argument keys,
and common dependency patterns in its parameters rather than
relying on prompt-time schemas.
b) AssetOpsBench.: We use AssetOpsBench [2] as the
primary benchmark for both data construction and evaluation.
The benchmark contains 152 natural-language scenarios, each
requiring the model to select appropriate domain tools, generate
valid arguments, and order tool calls into a structured execution
plan. Each plan consists of sequenced steps in a structured
format specifying a task description, the assigned MCP server,
the tool to call, JSON arguments, and inter-step dependencies.
Table I gives a compact overview of the MCP servers and tool
counts.
c) Training data.: The resulting data comprises three
types of supervised fine-tuning examples (see Appendix A for
composition). Tool and server knowledge examples teach the
model which MCP servers and tools exist, how they are associ-
ated, what arguments each tool requires, and how to distinguish
between near-miss tools such as get_failure_modes
and get_failure_mode_sensor_mapping. Question-
to-plan examples, based on the 152 AssetOpsBench scenarios


## Page 4


TABLE II
BASE MODELS USED FOR FINE-TUNING
Gemma 4 E4B
Qwen3-4B
Total params
∼8B w/ PLE
4.0B
Active params
4.5B
3.6B
Layers
42
36
Attention
Hybrid
GQA
Hidden size
2560
2560
Vocab size
262K
152K
together with generated paraphrases, teach the model to map a
natural-language query to a structured plan; each plan is vali-
dated to follow the required #Task/#Agent/#Tool/#Args
format. Execution-style examples combine planning steps with
execution traces and placeholder-resolution patterns such as
{step_N}.
d) Prompt structure.: At inference time, each query is
embedded in a structured planning prompt (shown in full in
Appendix B). The prompt contains four components: a system
preamble describing the model’s role as a planning assistant;
the complete tool catalog listing all MCP server names, tool
signatures, argument types, and descriptions (∼2,200 tokens);
the structured output format specification (#Task/#Agent/
#Tool/#Args/#Dependency/#ExpectedOutput); and
the user question. The full prompt totals approximately 2,400
tokens. In the description-free setting, we remove the complete
tool-catalog component while keeping the system preamble,
output-format specification, and user question, reducing the
prompt to ∼128 tokens—a 94.7% prompt-token reduction.
e) Data split.: We use a pattern-aware stratified 80/20
split over the 152 scenarios, where each scenario is assigned
a pattern based on its dominant task family, tool set, and
step count. The split is performed at the scenario level before
paraphrase expansion, so all paraphrases and derived traces
for a given scenario remain exclusively in either training or
test. This produces 122 training scenarios and 30 held-out test
scenarios. The full training corpus contains approximately 1,833
examples. We define three training configurations: Config A
(Plan-only, ∼1,200 examples), Config B (Tool-knowledge
only, ∼500 examples), and Config C (Tool+Plan, ∼1,741
examples). We use Config C as the primary configuration
because it provides the broadest tool-knowledge coverage. Data-
composition ablations are in Appendix A.
B. Models and Training
We compare two open-source instruction-tuned models:
Gemma 4 E4B-it [17] and Qwen3-4B [18]. Table II summarizes
their architectural differences. Both share a hidden size of 2560
but differ in depth, attention mechanism, and vocabulary size.
Both models are fine-tuned using QLoRA with 8-bit quanti-
zation, which keeps the base model weights fixed while training
a small set of adapter parameters. We use the same Config C
dataset for both models (1,741 training, 92 evaluation examples)
and train with identical hyperparameters unless otherwise stated:
LoRA rank r = 32, α = 64, dropout 0.05, learning rate
2 × 10−4 with cosine schedule, batch size 2 with gradient
accumulation of 4, 2 epochs, early stopping with patience 2,
and 436 total training steps. All linear layers are targeted.
Although the two models use the same LoRA rank, the
resulting trainable-parameter fraction differs due to model-size
differences. For Gemma, rank 32 corresponds to approximately
0.63% trainable parameters, whereas for Qwen3 it corresponds
to approximately 1.62% and about 2.6× higher adaptation
intensity. This difference directly affects retention, as discussed
in Section V-C.
C. Evaluation Protocol
We evaluate plans using two complementary approaches.
Structural metrics provide deterministic, reproducible scores
but can penalize valid plans that deviate from the gold reference.
LLM-based judging captures semantic quality and accepts valid
alternative formulations, but may exhibit grading bias. Using
both approaches and checking for agreement provides more
robust evidence than either alone.
For structural evaluation, we report AT-F1, which extracts
the set of (MCP server, tool) pairs from actionable steps
(excluding steps where agent or tool is “none”) in both the gold
and candidate plans and computes set-based F1 (precision =
matched pairs / candidate pairs, recall = matched pairs / gold
pairs). We also report ArgKey-F1, which measures whether the
model predicts the correct argument field names for matched
tool calls. For semantic evaluation, we use Gemini 2.5 Flash as
an LLM-as-judge [19] to rate each plan on six dimensions on a
1–5 scale: correctness, server routing, tool selection, argument
quality, efficiency, and dependency correctness. The judge
overall score is the mean of all six dimensions. Full judge
prompts are in Appendix A.
We evaluate models under three prompting conditions:
informed, where full tool descriptions are included in the
prompt; description-free, where the base model receives only
the user query with no tool schemas; and fine-tuned description-
free, where the fine-tuned model generates plans without tool
schemas at inference time.
We also evaluate capability retention using 100 multiple-
choice questions drawn from MMLU [20], ARC-Challenge
[21], and HellaSwag [22]. This measures whether tool-use
specialization degrades general reasoning behavior that may
still be needed by a multi-purpose planner. Details are in
Appendix B.
V. EXPERIMENTAL RESULTS
A. Main Result: Description-Free Fine-Tuning Improves Tool
Planning
We first evaluate whether fine-tuning can replace prompt-
time tool descriptions. The unfine-tuned Gemma 4 E4B model
is evaluated in two conditions. In the informed condition,
the prompt contains the system preamble, full serialized tool
catalog (∼2,200 tokens of schema text), the output format
specification, and the user query, totaling approximately 2,400
input tokens per query (see Appendix B). In the description-
free condition, the same unfine-tuned model receives only the


## Page 5


Fig. 2. Structural planning metrics across all four configurations. Fine-tuned
models operating without tool descriptions surpass the informed baseline on
AT-F1, server routing, and tool selection.
Fig. 3. LLM-as-judge scores (1–5 scale) across five evaluation dimensions.
Fine-tuned models operating without tool descriptions outperform the informed
baseline on every dimension.
system preamble, output format, and user query (∼128 tokens).
The description-free baseline achieves zero AT-F1, confirming
that the base model cannot reliably produce valid tool-use plans
without explicit tool descriptions.
Fine-tuning changes this substantially. Figs. 2 and 3 show
that fine-tuned models perform well in the description-free
setting and outperform the informed baseline on both structural
and semantic evaluation metrics.
The fine-tuned Gemma model (Config C, r=32) reaches an
AT-F1 of 0.635 and an overall judge score of 3.60, compared
with 0.47 and 2.88 for the informed baseline. Server routing and
tool-selection accuracy remain high, reaching approximately 95–
98% across the held-out evaluation set. The fine-tuned Qwen3
model achieves an AT-F1 of 0.605 and an overall judge score
of 3.78, while using substantially less memory. Both models
substantially outperform the informed baseline, confirming that
fine-tuned description-free planning is viable. As shown in
the rank sweep (Section V-B), a separate Gemma training run
with the same configuration achieves a judge score of 3.88,
indicating that the improvement over the informed baseline
is robust across runs despite some run-to-run variance on the
30-scenario test set.
Metric agreement. Structural and judge-based metrics
agree directionally: both rank the configurations in the same
Fig. 4. Training and evaluation loss over 436 steps (2 epochs). Both models
converge smoothly to comparable final evaluation losses (Gemma 0.331, Qwen3
0.347), despite Qwen3 starting from a higher initial loss.
Fig. 5. Effect of LoRA rank on planning quality (Gemma 4 E4B). Both Judge
Overall (left axis) and AT-F1 (right axis) peak at r=32 and decline at r=64,
suggesting diminishing returns at higher adapter capacity.
broad order—description-free baseline worst, informed baseline
substantially better, and fine-tuned description-free models
best. This agreement is useful because AT-F1 is deterministic
but strict, while LLM judging captures semantically valid
alternatives but may introduce grading bias.
Because the 1–5 judge scale has a floor of 1.0, the description-
free baseline’s score of 1.88 corresponds to 0.88/4.0 on a zero-
anchored scale, confirming near-zero semantic planning quality
in the absence of either tool descriptions or fine-tuning.
Both models converge smoothly within two epochs (Fig. 4),
reaching comparable evaluation losses (Gemma 0.331; Qwen3
0.347). The prompt-token savings are substantial: description-
free inference after fine-tuning reduces the planning prompt
from ∼2,400 tokens to ∼128 tokens, a 94.7% reduction.
B. LoRA Rank Selection
Having established that fine-tuning enables description-free
inference that surpasses the informed baseline, we next study
how adapter capacity affects planning quality. LoRA rank
r controls the number of trainable parameters and thus the
model’s capacity to absorb new tool-use knowledge. We sweep
r ∈{8, 16, 32, 64} on Gemma 4 E4B, corresponding to
trainable-parameter fractions from 0.32% to 2.51%.
As shown in Fig. 5, both metrics rise steeply from r=8
(Judge 3.77, AT-F1 0.56) to r=16 (Judge 3.81, AT-F1 0.63)


## Page 6


Fig. 6.
Overall MCQ accuracy before and after tool-use fine-tuning.
Gemma 4 E4B retains 79.8–82.1% of base performance; Qwen3-4B retains only
61.3%. Retention percentages shown inside bars. Per-benchmark breakdown
in Appendix B.
and peak at r=32 (Judge 3.88, AT-F1 0.65). At r=64, perfor-
mance slightly degrades (Judge 3.83, AT-F1 0.63), suggesting
diminishing returns at higher adapter capacity. This finding
is important for the retention analysis in Section V-C: while
r=32 maximizes planning quality, smaller ranks preserve more
general knowledge.
C. Capability Retention
A planner deployed inside a broader agent may still need
to recognize unrelated requests, answer simple questions,
or reason outside the tool catalog. We therefore measure
whether tool-use fine-tuning degrades general multiple-choice
performance. We use 100 questions from MMLU, ARC-
Challenge, and HellaSwag, independent of AssetOpsBench.
We compare Gemma at r=8 and r=32 to test the rank trade-off,
and Qwen3 at r=32.
As shown in Fig. 6, Gemma shows moderate degradation: the
base model scores 84.0% MCQ accuracy, dropping to 69.0%
at r=8 (82.1% retention) and 67.0% at r=32 (79.8% retention).
Per-question analysis reveals that Gemma at r=32 forgot 21 of
100 questions while learning 4 new ones. This reveals a quality–
retention trade-off: Section V-B showed that r=32 achieves the
best judge score (3.88 vs. 3.77 for r=8), but at the cost of 2.3
percentage points of retention. For deployment where general
reasoning matters, the smaller r=8 adapter may be preferable.
Qwen3 shows larger degradation: its base accuracy drops
from 75.0% to 46.0% after fine-tuning at r=32, or 61.3%
retention. One likely contributor is adaptation intensity: at
the same LoRA rank, Qwen3 trains 1.62% of its parameters
compared with 0.63% for Gemma. However, architecture,
tokenizer, and pretraining differences are confounded, so this
should not be interpreted as a causal explanation. The per-
benchmark breakdown (Fig. 9 in Appendix B) reveals that
Qwen3’s degradation is especially severe on logical reasoning
(75%→25%) and commonsense completion (50%→27%),
while Gemma’s degradation is more evenly distributed.
We verified that degradation was not caused by inference
quantization: the base Gemma model achieved 84% in bf16
TABLE III
PROFILING COMPARISON ON A100 80GB
Metric
Gemma
Qwen3
Base memory
11.5 GB
4.42 GB
Peak train memory
24.1 GB
16.06 GB
Train time
56 min
39.7 min
Inference speed
1.4 tok/s
3.49 tok/s
Eval time
59 min
40.7 min
Best eval loss
0.331
0.347
and 87% in 8-bit, confirming that quantization alone does not
explain the 84%→67% drop observed after fine-tuning.
D. Deployment Characterization
We report basic deployment measurements to characterize
the practical cost of description-free fine-tuning. Table III
summarizes the results on a single A100 80GB GPU.
Qwen3 uses 62% less base memory, trains 29% faster, and
runs 2.5× faster at inference while achieving a comparable
planning judge score. Qwen3’s speed advantage comes directly
from having fewer total parameters (4.0B vs. 8.0B), which
reduces the size of every 8-bit matrix multiplication. Full
profiling details, including the CUDA operator breakdown and
cost estimation, are provided in Appendix A.
Additional data-composition and quantization ablations are
provided in Appendices A and A.
VI. DISCUSSION
a) Fixed-catalog internalization.: The main result shows
that small models can learn a fixed tool catalog well enough
to plan without prompt-time tool descriptions. This does not
replace schema-informed prompting for open-world or rapidly
changing tools. Rather, it targets mature deployments where
the same catalog is reused across many queries and schema
knowledge can be amortized into adapter weights.
b) Why can description-free fine-tuning beat schema-
informed prompting?: One surprising result is that fine-tuned
description-free models outperform an unfine-tuned model that
receives the full schema. We hypothesize two mechanisms.
First, long schema prompts create context competition: the
serialized tool catalog dominates the input, and small models
may fail to attend to the relevant schema fragment. Second,
schema parsing is itself an inference-time task. Supervised
fine-tuning converts this into a learned mapping from user
intents to tool sequences, arguments, and dependencies. We do
not directly isolate these mechanisms, and future work should
evaluate fine-tuned models both with and without schemas at
inference time to separate internalization effects from context-
length effects.
c) Specialization trade-offs.: The retention results show
that tool internalization has a cost. Higher LoRA rank improves
planning quality but can degrade general multiple-choice
performance. This matters when the planner is part of a multi-
purpose agent that must handle both tool-related and unrelated
requests. Lower-rank adapters, replay data, or modular adapter


## Page 7


architectures may reduce this trade-off. A preliminary 10-
scenario end-to-end execution pilot validated that plan quality
correlates with task completion (70% success), but full closed-
loop evaluation remains for future work. Future work should
also study continual learning for adding new tools without
forgetting old ones, larger benchmarks, multi-seed runs with
confidence intervals, and optimized quantized kernels such as
GPTQ or AWQ.
VII. CONCLUSION
We studied description-free tool planning for fixed cata-
logs, where a model must generate structured MCP tool-
use plans without receiving tool descriptions at inference
time. On AssetOpsBench, 8-bit QLoRA fine-tuning enables
∼4B parameter models to outperform an unfine-tuned schema-
informed baseline while reducing prompt length by 94.7%.
The best Gemma run achieves 0.65 AT-F1 and a 3.88 judge
score, compared with 0.47 and 2.88 for the informed baseline.
The gains come with a specialization cost: LoRA rank affects
both planning quality and capability retention. Gemma retains
approximately 80–82% of its base MCQ performance after fine-
tuning, while Qwen3 shows larger degradation. Overall, these
results suggest that supervised adapter fine-tuning is a practical
mechanism for amortizing fixed tool-catalog knowledge in
small models, but that retention and catalog-update costs remain
important deployment considerations.
VIII. LIMITATIONS
This study is a proof of concept on AssetOpsBench. The
held-out evaluation set contains only 30 scenarios, and most
results are based on single fine-tuning runs rather than multiple
random seeds. Small differences between model variants should
therefore be interpreted cautiously.
Our evaluation focuses on plan quality rather than full closed-
loop execution. A deployed agent may fail at execution time
even when the generated plan is structurally correct. We do not
evaluate generalization to unseen tools; this is by design, as
description-free planning assumes a fixed catalog. Benchmark
coverage is incomplete: not all AssetOpsBench MCP servers,
scenarios, or asset classes are evaluated.
IX. USE OF GENERATIVE AI
We used generative AI tools for limited drafting, editing,
proofreading assistance, and exploratory scripting. The authors
reviewed, edited, and verified the final manuscript, experiments,
results, and references, and take full responsibility for the
content of the paper.
REFERENCES
[1] Anthropic, “What is the model context protocol (MCP)?” https:
//modelcontextprotocol.io/docs/getting-started/intro,
2026,
accessed:
Apr. 30, 2026.
[2] D. Patel, S. Lin, J. Rayfield, N. Zhou, C. Shyalika, S. R. Yarrabothula,
R. Vaculin, N. Martinez, F. O’donncha, and J. Kalagnanam, “Assetops-
bench: Benchmarking ai agents for task automation in industrial asset
operations and maintenance,” arXiv preprint arXiv:2506.03828, 2025.
[3] M. Li, Y. Zhao, B. Yu, F. Song, H. Li, H. Yu, Z. Li, F. Huang, and
Y. Li, “API-bank: A comprehensive benchmark for tool-augmented
LLMs,” in Proceedings of the 2023 Conference on Empirical
Methods in Natural Language Processing, 2023. [Online]. Available:
https://arxiv.org/abs/2304.08244
[4] S. G. Patil, H. Mao, C. C.-J. Ji, F. Yan, V. Suresh, I. Stoica, and J. E.
Gonzalez, “The Berkeley function calling leaderboard (BFCL): From
tool use to agentic evaluation of large language models,” in Advances in
Neural Information Processing Systems, 2024.
[5] Z. Wang, Q. Chang, H. Patel, S. Biju, C.-E. Wu, Q. Liu, A. Ding,
A.
Rezazadeh,
A.
Shah,
Y.
Bao,
and
E.
Siow,
“MCP-bench:
Benchmarking tool-using LLM agents with complex real-world tasks
via MCP servers,” in Workshop on Scaling Environments for Agents,
2025. [Online]. Available: https://openreview.net/forum?id=2InRbaYve7
[6] S. G. Patil, T. Zhang, X. Wang, and J. E. Gonzalez, “Gorilla: large
language model connected with massive apis,” in Proceedings of the
38th International Conference on Neural Information Processing Systems,
ser. NIPS ’24.
Red Hook, NY, USA: Curran Associates Inc., 2024.
[7] Y. Qin, S. Liang, Y. Ye, K. Zhu, L. Yan, Y. Lu, Y. Lin, X. Cong,
X. Tang, B. Qian, S. Zhao, L. Hong, R. Tian, R. Xie, J. Zhou,
M. Gerstein, dahai li, Z. Liu, and M. Sun, “ToolLLM: Facilitating large
language models to master 16000+ real-world APIs,” in The Twelfth
International Conference on Learning Representations, 2024. [Online].
Available: https://openreview.net/forum?id=dHng2O0Jjr
[8] W. Liu, X. Huang, X. Zeng, X. Hao, S. Yu, D. Li, S. Wang, W. Gan,
Z. Liu, Y. Yu, Z. Wang, Y. Wang, W. Ning, Y. Hou, B. Wang, C. Wu,
X. Wang, Y. Liu, Y. Wang, D. Tang, D. Tu, L. Shang, X. Jiang, R. Tang,
D. Lian, Q. Liu, and E. Chen, “ToolACE: Winning the points of LLM
function calling,” arXiv preprint arXiv:2409.00920, 2024.
[9] R. Wang, X. Han, L. Ji, S. Wang, T. Baldwin, and H. Li, “ToolGen:
Unified tool retrieval and calling via generation,” in The Thirteenth
International Conference on Learning Representations, 2025. [Online].
Available: https://arxiv.org/abs/2410.03439
[10] Z. Lu, Z. Yao, J. Wu, C. Han, Q. Gu, X. Cai, W. Lu, J. Xiao, Y. Zhuang,
and Y. Shen, “SKILL0: In-context agentic reinforcement learning for
skill internalization,” arXiv preprint arXiv:2604.02268, 2026.
[11] H. Jiang, Q. Wu, C.-Y. Lin, Y. Yang, and L. Qiu, “LLMLingua:
Compressing prompts for accelerated inference of large language
models,”
in
The
2023
Conference
on
Empirical
Methods
in
Natural
Language
Processing,
2023.
[Online].
Available:
https:
//openreview.net/forum?id=ADsEdyI32n
[12] C.-Y. Hsieh, C.-L. Li, C.-K. Yeh, H. Nakhost, Y. Fujii, A. Ratner, R. Kr-
ishna, C.-Y. Lee, and T. Pfister, “Distilling step-by-step! outperforming
larger language models with less training data and smaller model sizes,”
in Findings of the Association for Computational Linguistics: ACL 2023,
2023, pp. 8003–8017.
[13] E. J. Hu, yelong shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang,
L. Wang, and W. Chen, “LoRA: Low-rank adaptation of large language
models,” in International Conference on Learning Representations, 2022.
[Online]. Available: https://openreview.net/forum?id=nZeVKeeFYf9
[14] T. Dettmers, A. Pagnoni, A. Holtzman, and L. Zettlemoyer, “Qlora:
efficient finetuning of quantized llms,” in Proceedings of the 37th
International Conference on Neural Information Processing Systems,
ser. NIPS ’23.
Red Hook, NY, USA: Curran Associates Inc., 2023.
[15] J. Han, L. Du, H. Du, X. Zhou, Y. Wu, Y. Zhang, W. Zheng, and
D. Han, “SLIM: Let LLM learn more and forget less with soft LoRA
and identity mixture,” in Proceedings of the 2025 Conference of the
Nations of the Americas Chapter of the Association for Computational
Linguistics: Human Language Technologies (Volume 1: Long Papers),
L. Chiruzzo, A. Ritter, and L. Wang, Eds.
Albuquerque, New Mexico:
Association for Computational Linguistics, Apr. 2025, pp. 4792–4804.
[Online]. Available: https://aclanthology.org/2025.naacl-long.246/
[16] Google DeepMind, “Gemini 2.5 flash and 2.5 flash image model
card,”
https://storage.googleapis.com/deepmind-media/Model-Cards/
Gemini-2-5-Flash-Model-Card.pdf, 2025, accessed: Apr. 30, 2026.
[17] Google AI for Developers, “Gemma 4 model card,” Google AI for
Developers Documentation, 2026, accessed: Apr. 30, 2026. [Online].
Available: https://ai.google.dev/gemma/docs/core/model_card_4
[18] A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao,
C. Huang, C. Lv et al., “Qwen3 technical report,” arXiv preprint
arXiv:2505.09388, 2025.
[19] L. Zheng, W.-L. Chiang, Y. Sheng, S. Zhuang, Z. Wu, Y. Zhuang,
Z. Lin, Z. Li, D. Li, E. Xing, H. Zhang, J. E. Gonzalez, and
I. Stoica, “Judging LLM-as-a-judge with MT-bench and chatbot


## Page 8


arena,” in Thirty-seventh Conference on Neural Information Processing
Systems Datasets and Benchmarks Track, 2023. [Online]. Available:
https://openreview.net/forum?id=uccHPGDlao
[20] D. Hendrycks, C. Burns, S. Basart, A. Zou, M. Mazeika, D. Song, and
J. Steinhardt, “Measuring massive multitask language understanding,” in
International Conference on Learning Representations, 2021. [Online].
Available: https://arxiv.org/abs/2009.03300
[21] P. Clark, I. Cowhey, O. Etzioni, T. Khot, A. Sabharwal, C. Schoenick,
and O. Tafjord, “Think you have solved question answering? try arc, the
ai2 reasoning challenge,” arXiv preprint arXiv:1803.05457, 2018.
[22] R. Zellers, A. Holtzman, Y. Bisk, A. Farhadi, and Y. Choi, “HellaSwag:
Can a machine really finish your sentence?” in Proceedings of the
57th Annual Meeting of the Association for Computational Linguistics,
A. Korhonen, D. Traum, and L. Màrquez, Eds.
Florence, Italy:
Association for Computational Linguistics, Jul. 2019, pp. 4791–4800.
[Online]. Available: https://aclanthology.org/P19-1472/
APPENDIX
TABLE IV
THREE TRAINING DATASETS
Dataset
N
Source
Description
Tool Knowledge
∼500
Gemini 2.5 Flash
Tool taxonomy, own-
ership, args, routing,
hard negatives
Planning
∼1,200
Gold plans + para-
phrases
Scenario →concise
planning steps
Execution
∼100
Gold plans + traces
Scenario →planning
+ execution links
Note. Total ∼1,833 examples. Config C (Tool+Plan) uses ∼1,741 after
95/5 train/eval split.
We compare four data configurations using 8-bit QLoRA
with r=32 on Gemma 4 E4B. Fig. 7 shows the results.
Fig. 7. Effect of training data composition on planning quality. Plan-only data
achieves the highest judge score (3.90), while Tool-only data performs poorly
(2.59).
Plan-only training (Config A, ∼1,200 examples) achieves
the highest judge score of 3.90 and AT-F1 of 0.636. Adding
tool-knowledge examples (Config C) does not improve the
judge score in this run (3.60), though tool selection accuracy
is higher (94.9% vs. 92.9%). Tool-only training (Config B)
performs poorly (2.59). One possible explanation is that
planning examples expose tool usage in realistic query contexts,
whereas tool-knowledge examples are more declarative. We
treat these results as exploratory because the configurations
also differ in size and coverage, and run-to-run variance on
the 30-scenario test set can be substantial (see Limitations).
TABLE V
QUANTIZATION ABLATION (GEMMA 4 E4B, r=32)
Quantization
AT-F1
Judge
Train Time
8-bit
0.617
3.78
56 min
4-bit NF4
0.642
3.74
∼50 min
Note. Differences are marginal. We use 8-bit as the default for its higher
judge score.
All profiling was conducted on a single NVIDIA A100 80GB
GPU. Fig. 8 provides a visual comparison; Tables VI and VII
provide additional detail.
For profiling, we use the PyTorch Profiler, torch.cuda
memory tracking, and Weights & Biases. Training throughput
scaled from ∼886 tok/s at batch size 1 to ∼1,415 tok/s at
batch size 4, beyond which the model exceeded available
memory. The main CUDA bottleneck was MatMul8bitLt,
which accounted for 56.3% of total CUDA time, reflecting the
dominance of 8-bit matrix multiplication in quantized inference.
Fig. 8. Profiling comparison between Gemma 4 E4B and Qwen3-4B. Qwen3
uses less memory, trains faster, and achieves 2.5× higher inference throughput.
TABLE VI
CUDA OPERATOR BREAKDOWN (GEMMA INFERENCE, 64 TOKENS)
Operation
% CUDA Time
MatMul8bitLt
56.3%
aten::mm
18.2%
Attention kernel
8.7%
Other ops
16.8%
Note. Attention kernel refers to scaled_dot_product_attention.
Other ops include softmax, layer normalization, and related kernels.


## Page 9


TABLE VII
EXPERIMENT COST BREAKDOWN (A100 AT $3.93/HR)
Component
A100 Hours
Cost
Gemma ablations
3.1
$12.18
Qwen3 train + eval
1.5
$5.78
Retention analysis
11.2
$44.00
Total
∼15.8
∼$62
A. Plan Quality Judge
We use Gemini 2.5 Flash (temperature=0, max_tokens=8192)
to evaluate each candidate plan against the gold reference.
The prompt provides the question, gold plan, candidate plan,
and tool inventory, and asks the judge to rate on a 1–5 scale
across six dimensions: correctness, server routing, tool selection,
argument quality, efficiency, and dependency correctness. Each
dimension includes a rubric (5 = matches gold reference, 3 =
partially correct, 1 = major errors). The judge returns a JSON
object with integer scores.
B. MCQ Retention Judge
For the retention benchmark, we use Gemini 2.5 Flash
(temperature=0, max_tokens=1024). The prompt provides the
question, answer choices, correct answer, and the model’s full
response. The judge is instructed to look at the final answer
the model commits to, ignoring intermediate reasoning, and
return a JSON object with a binary correct/incorrect grade. This
approach is more reliable than token-level evaluation because
instruction-tuned models produce chain-of-thought reasoning
before committing to an answer letter.
TABLE VIII
RETENTION BENCHMARK COMPOSITION
Source
N
Description
MMLU (5 subjects)
40
Knowledge and reasoning
ARC-Challenge
30
Grade-school science
HellaSwag
30
Commonsense completion
Total
100
Fig. 9. Per-benchmark MCQ accuracy for base and fine-tuned models. Qwen3-
4B shows severe degradation on Logic (75%→25%), Marketing (88%→38%),
and HellaSwag (50%→27%). Gemma degradation is more uniform across
benchmarks.
MMLU subjects are selected for a suitable difficulty range on
∼4B models (base accuracy 40–100%): High School Computer
Science, High School Geography, Logical Fallacies, Marketing,
and Miscellaneous. We avoid niche subjects where the base
model scores near zero, making retention difficult to interpret.
The evaluation protocol is fixed across all models: 100
MCQ examples loaded with a fixed random seed; the model is
prompted to think step by step and provide a final answer letter
(A/B/C/D); generation is capped at 512 tokens; Gemini judges
correctness. Overall retention = FT accuracy / base accuracy.
We summarize the informed and description-free prompts
used for AssetOpsBench scenario 114.
Question: “What are the failure modes of Chiller 6 that can
be identified by analyzing the data from the available sensors?”
a) Informed prompt.: The informed prompt contains four
components:
1) a system instruction describing the model as a planning
assistant for industrial asset operations;
2) the full tool catalog, including MCP server names, tool
signatures, argument schemas, and natural-language de-
scriptions;
3) the
required
structured
output
format:
#Task,
#Agent,
#Tool,
#Args,
#Dependency,
and
#ExpectedOutput;
4) the user question.
This prompt is approximately 2,400 tokens, of which roughly
2,200 tokens come from the serialized tool catalog.
b) Gold plan.: The gold plan contains four tool calls:
1) call
IoTAgent.assets
with
{"site_name":
"MAIN"} to identify the asset ID for “Chiller 6”;
2) call IoTAgent.sensors with the site name and asset
ID to retrieve available sensors;
3) call
FMSRAgent.get_failure_modes
with
{"asset_name": "Chiller 6"} to retrieve known
failure modes;
4) call FMSRAgent.get_failure_mode_sensor_mapping
using the failure modes and sensors from the previous
steps to determine which failures can be detected by
which sensors.
c) Description-free prompt.: In the description-free set-
ting, the entire tool catalog is removed. The model receives
only the system instruction, output-format specification, and
user question, reducing the input to approximately 128 tokens.
The fine-tuned model must therefore recover the same tool
sequence from internalized tool knowledge rather than from
prompt-time tool descriptions.
