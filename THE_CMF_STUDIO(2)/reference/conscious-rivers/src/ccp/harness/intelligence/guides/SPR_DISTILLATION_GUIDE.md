# SPR Distillation Guide

> How to compress narrative_dna into 48-60 word latent space primers

---

## What is SPR Distillation?

**SPR (Sparse Priming Representation)** distillation is the process of compressing the structured `narrative_dna` object into a 48-60 word prose that activates the LLM's latent space for targeted quote extraction.

---

## The Distillation Algorithm

```
INPUT: narrative_dna object from STEP 5A
OUTPUT: spr_text (48-60 word prose)

SENTENCE 1: state_alpha.sensory_anchor → felt suffering (8-12 words)
SENTENCE 2: the_abyss.sensation → breaking point (8-12 words)
SENTENCE 3: the_spark.insight_quote → coach insight (8-12 words)
SENTENCE 4: state_omega.action → new behavior (8-12 words)
SENTENCE 5: state_omega.result → measurable proof (8-12 words)
SENTENCE 6: gift → what they offer (8-12 words)
```

---

## Distillation Rules

| Rule | Requirement |
|------|-------------|
| **Word Count** | EXACTLY 48-60 words (count before finalizing) |
| **Sentences** | 4-6 complete sentences |
| **Emotional Grounding** | Show how the speaker FEELS, not just thinks |
| **Verbatim Language** | Use exact words/phrases from the transcript |
| **Associations** | Include metaphors, analogies from the transcript |
| **Compression** | Capture maximum meaning with minimum words |
| **Sensory Detail** | Include physical/bodily sensations |

---

## Step-by-Step Process

### Step 1: Extract Key Elements from narrative_dna

From the narrative_dna object, extract:

```
1. state_alpha.sensory_anchor → "weight of eyelids every afternoon"
2. the_abyss.sensation → "(Frustration_Burning, Tears_Behind_Smile)"
3. the_spark.insight_quote → "gut not absorbing nutrients (08:23)"
4. state_omega.action → "Daily probiotic protocol"
5. state_omega.result → "Energy from 3/10 to 8/10"
6. internal_monologue → "I thought exhaustion was just part of being a mom"
```

### Step 2: Write Each Sentence

Transform each element into an emotionally grounded sentence:

| Element | Raw Data | SPR Sentence |
|---------|----------|--------------|
| Suffering | "weight of eyelids" | "She dragged through days like a zombie, weight pressing her eyelids by afternoon." |
| Breaking Point | "Frustration_Burning" | "The doctor's 'nothing wrong' broke her—frustration burning behind forced smiles." |
| Coach Insight | "gut not absorbing" | "Dr. Maria saw what medicine missed: gut not absorbing nutrients properly." |
| New Behavior | "Daily probiotic" | "Now she listens to her body first." |
| Proof | "3/10 to 8/10" | "Energy climbed from 3 to 8 within six weeks." |
| Gift | What they share | "She helps other mothers trust their bodies." |

### Step 3: Combine and Count

Combine all sentences and count words:

> "She dragged through days like a zombie, weight pressing her eyelids by afternoon. The doctor's 'nothing wrong' broke her—frustration burning behind forced smiles. Dr. Maria saw what medicine missed: gut not absorbing nutrients properly. Now she listens to her body first. Energy climbed from 3 to 8 within six weeks. She helps other mothers trust their bodies."

**Word count: 56 words ✅**

### Step 4: Adjust if Needed

- If too short (<48 words): Add more sensory detail from transcript
- If too long (>60 words): Compress phrases, remove redundancy

---

## Examples by Arc Type

### The Witness Arc (56 words)
> "She dragged through days like a zombie, weight pressing her eyelids by afternoon. The doctor's 'nothing wrong' broke her—frustration burning behind forced smiles. Dr. Maria saw what medicine missed: gut not absorbing nutrients properly. Now she listens to her body first. Energy climbed from 3 to 8 within six weeks. She helps other mothers trust their bodies."

### The Breakthrough Arc (54 words)
> "He performed perfection while dying inside, chest tight in every meeting, panic his silent partner. The boardroom attack stripped the armor—vulnerability exposed, control lost. His daughter's question pierced the facade: 'Daddy, are you sad?' Permission to stop performing arrived like relief. Panic attacks dissolved from weekly to zero. He now models presence, not perfection, for his team."

### The Rally Arc (52 words)
> "She hid from old partners, shame knotting her stomach after the bankruptcy hearing. The courtroom silence crushed her identity as entrepreneur. Coach Marcus reframed failure as fuel: 'Your bankruptcy is your MBA.' Lightness replaced shame. New business grew from zero to 500K in eighteen months. She now speaks about failure to help founders rise."

---

## Quality Checklist

Before finalizing, verify:

- [ ] Word count is 48-60 words
- [ ] Each sentence is emotionally grounded (feelings, not just facts)
- [ ] Uses verbatim language from transcript where possible
- [ ] Includes measurable result with NUMBER
- [ ] Captures the full transformation arc (before → breaking point → insight → after → proof → gift)
- [ ] Reads as prose, not as a list

---

## Common Mistakes to Avoid

| Mistake | Why It's Wrong | Fix |
|---------|----------------|-----|
| "She was tired" | Too generic, no sensory detail | "Weight pressed her eyelids by afternoon" |
| "She learned a method" | No emotional grounding | "The insight clicked: gut not absorbing nutrients" |
| "She got better" | No measurable proof | "Energy climbed from 3 to 8" |
| 70+ words | Too long, dilutes priming effect | Compress each sentence to 8-12 words |
| Bullet points | Wrong format | Write as flowing prose |

---

## File Location

This guide is referenced from: `commands/cmf-diagnose.md` (STEP 5B)

---

**END OF GUIDE**
