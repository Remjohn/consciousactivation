# Fractal Hook Validation — Holographic Test

**Principle XI:** "The story must be told in the first 3 seconds, and then retold in 60 seconds."

---

## The Holographic Hook Principle

A **Fractal Hook** (also called a Holographic Hook) is a C1/Hook cluster quote that:
1. **Encapsulates the ENTIRE arc** in one sentence
2. Contains Problem + Mechanism + Result (or hints at all three)
3. Makes sense EVEN IF the viewer stops watching after 5 seconds

**Bad Hook (Clickbait):** "I was anxious."  
→ Just the problem. No frame. Incomplete.

**Good Hook (Fractal/Holographic):** "With Adele, we detox the mind, not just the body."  
→ Contains: Method (detox), Coach (Adele), and Frame (mind-body connection). Complete.

---

## Validation Test

After selecting the Hook quote, ask these 3 questions:

### Q1: Frame Completeness
**"If the viewer stops watching after THIS quote, do they understand the CORE PREMISE?"**

| Score | Answer | Action |
|-------|--------|--------|
| 9-10 | YES — They know the full arc (Problem, Method, Result) | ✅ PASS |
| 7-8 | MOSTLY — They know 2 of 3 elements | ⚠️ FLAG |
| 5-6 | PARTIALLY — They know 1 element | ❌ REVISE |
| 0-4 | NO — It's just a teaser/symptom | ❌ REJECT |

**If Score < 7:** The Hook is NOT Holographic. Find a different quote.

### Q2: Promise vs. Lie
**"Does this Hook PROMISE what the video DELIVERS?"**

- **Promise:** The Hook sets up an expectation the video fulfills
- **Lie:** The Hook baits attention but the video is about something else

**Example:**
- Hook: "I lost 30 pounds in 8 weeks."
- Video Content: A testimonial about liver detox and energy (weight loss is barely mentioned)
- **Result:** LIE. This is clickbait, not a Fractal Hook.

**If it's a Lie:** ❌ REJECT

### Q3: Coach Presence
**"Is the COACH mentioned or implied in the Hook?"**

- Witness Arc: REQUIRED (Coach must be named in Hook)
- Confrontation Arc: Optional (focus is on the lie/system)
- Core Transformation Arc: REQUIRED (Coach's story)

**If Coach required but missing:** ❌ REVISE

---

## Scoring Formula

```
holographic_score = (frame_completeness × 0.6) + (promise_delivery × 0.3) + (coach_presence × 0.1)

If holographic_score < 7/10 → FLAG for revision
If holographic_score < 5/10 → REJECT
```

---

## Examples

### Example 1: Witness Arc (Matthis)

**Hook Quote:** *"With Adele, we detox the mind, not just the body."*

**Validation:**
- **Q1 (Frame Completeness):** 10/10 → Contains: Coach (Adele), Method (detox), Frame (mind-body)
- **Q2 (Promise vs. Lie):** 10/10 → Video is about mental/emotional detox. Promise delivered.
- **Q3 (Coach Presence):** 10/10 → "Adele" is named.

**Holographic Score:** (10×0.6) + (10×0.3) + (10×0.1) = **10/10** ✅ PERFECT

---

### Example 2: Breakthrough Arc (Bad Hook)

**Hook Quote:** *"I couldn't breathe. I was suffocating."*

**Validation:**
- **Q1 (Frame Completeness):** 3/10 → Only shows Problem (anxiety). No Method or Result.
- **Q2 (Promise vs. Lie):** 5/10 → Promises a story about anxiety, which it delivers. But incomplete.
- **Q3 (Coach Presence):** 0/10 → No coach mentioned.

**Holographic Score:** (3×0.6) + (5×0.3) + (0×0.1) = **3.3/10** ❌ REJECT

**Better Hook:** *"I thought I was broken. Then [Coach] taught me my anxiety was just fear wearing a mask."*
- Frame Completeness: 9/10 (Problem: broken, Method: Coach's teaching, Result: understanding)
- Promise: 9/10
- Coach: 10/10
- **New Score: 9.1/10** ✅ PASS

---

### Example 3: Confrontation Arc

**Hook Quote:** *"The diet industry has a 95% failure rate. They KNOW this."*

**Validation:**
- **Q1 (Frame Completeness):** 8/10 → Sets up "Industry Lie" frame. Missing the "Truth" alternative.
- **Q2 (Promise vs. Lie):** 10/10 → Video is about exposing diet industry. Promise delivered.
- **Q3 (Coach Presence):** N/A (Confrontation doesn't require coach in Hook)

**Holographic Score:** (8×0.6) + (10×0.3) + (5×0.1) = **8.3/10** ✅ PASS

---

## Integration with Arc Hunters

All Arc Hunters should add a **Step 4: Holographic Validation** after Hook selection:

```markdown
### Step 4: Holographic Validation (Principle XI)
For the selected C1 (HOOK) quote:
1. Calculate Frame Completeness (0-10)
2. Verify Promise vs. Lie (0-10)
3. Check Coach Presence (if required: 0-10)
4. Calculate holographic_score
5. If score < 7 → Find alternative Hook quote
6. If score < 5 → Report [MISSING_DATA] for Hook cluster
```

---

**Output Field:** Add to Quote Manifest:
```json
"C1_HOOK": {
  "selected_quote": "...",
  "holographic_score": 9.1,
  "holographic_breakdown": {
    "frame_completeness": 9,
    "promise_delivery": 9,
    "coach_presence": 10
  }
}
```

---

**Usage:** Load in all Arc Hunters during Hook/C1 cluster selection.
