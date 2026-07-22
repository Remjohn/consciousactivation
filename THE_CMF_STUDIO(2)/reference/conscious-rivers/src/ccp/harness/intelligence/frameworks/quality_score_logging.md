# Quality Score Logging System — Feedback Loop

**Principle XII:** "An algorithm that doesn't learn from its hits and misses becomes obsolete."

---

## Purpose

Track the QUALITY of each premise analysis output to:
1. Identify which Arc Hunters are performing well vs. poorly
2. Spot patterns in failures (e.g., "Breakthrough scripts consistently score low")
3. Trigger optimization when an Arc falls below acceptable thresholds
4. Build a historical dataset for future AI training

---

## Quality Score Calculation

The Premise Commander calculates a **Quality Score (0-100)** based on:

| Component | Weight | Criteria |
|-----------|--------|----------|
| **Frame Score** | 25% | Is the Frame Statement clear, specific, and arc-aligned? |
| **Cluster Balance** | 25% | Do all clusters have ≥2 quotes? Are they evenly distributed? |
| **Viral Peak Score** | 25% | What is the HIGHEST viral score among all selected quotes? |
| **Holographic Score** | 15% | Does the Hook pass the Fractal Hook test (score ≥7)? |
| **Speaker Enforcement** | 10% | Are all speaker rules followed (no Coach in Problem clusters, etc.)? |

**Formula:**
```
quality_score = (frame_score × 0.25) + 
                (cluster_balance × 0.25) + 
                (viral_peak × 0.25) + 
                (holographic_score × 0.15) + 
                (speaker_compliance × 0.10)
```

---

## Scoring Breakdown

### Frame Score (0-25)
- **25:** Frame is specific (Problem + Mechanism + Result), arc-aligned, and coach-present
- **20:** Frame is specific but missing one element
- **15:** Frame is vague or generic
- **10:** Frame is present but incorrect for the arc
- **0:** No frame or contradictory frame

### Cluster Balance (0-25)
- **25:** All clusters have 3+ quotes (STRONG)
- **20:** All clusters have 2+ quotes (ADEQUATE)
- **15:** 1-2 clusters are WEAK (1 quote)
- **10:** 1 cluster is MISSING
- **0:** Multiple clusters MISSING

### Viral Peak Score (0-25)
Take the HIGHEST final score (Trinity × Frame Alignment) among all selected quotes:
- **25:** Peak score ≥ 12 (Exceptional)
- **20:** Peak score 10-11.9 (Strong)
- **15:** Peak score 8-9.9 (Good)
- **10:** Peak score 6-7.9 (Adequate)
- **5:** Peak score 4-5.9 (Weak)
- **0:** Peak score < 4 (Fail)

### Holographic Score (0-15)
- **15:** Hook holographic_score ≥ 9
- **12:** Hook holographic_score 7-8.9
- **8:** Hook holographic_score 5-6.9
- **0:** Hook holographic_score < 5

### Speaker Compliance (0-10)
- **10:** All speaker rules followed perfectly
- **5:** 1 minor violation (e.g., Coach in W3 Mechanism, which is allowed but not preferred)
- **0:** Critical violation (e.g., Coach in W2 Problem)

---

## Quality Thresholds

| Score Range | Interpretation | Action |
|-------------|----------------|--------|
| **85-100** | Excellent | ✅ AUTHORIZE. No notes. |
| **70-84** | Good | ✅ AUTHORIZE with minor notes. |
| **50-69** | Acceptable | ⚠️ CONDITIONAL AUTHORIZE. Flag for review. |
| **0-49** | Poor | ❌ REJECT. Needs major revision. |

---

## Logging Protocol

After calculating the quality score, the Commander writes to:
`intelligence/logs/quality_scores.json`

**Entry Format:**
```json
{
  "project_id": "02_50-12_Audrey",
  "arc_type": "The Witness",
  "date": "2026-01-11T06:00:00Z",
  "quality_score": 87,
  "breakdown": {
    "frame_score": 23,
    "cluster_balance": 25,
    "viral_peak": 21,
    "holographic_score": 12,
    "speaker_compliance": 10
  },
  "notes": "Excellent testimonial. Strong proof cluster with specific metrics.",
  "status": "AUTHORIZED"
}
```

---

## Quarterly Review Protocol

**Trigger:** Every 10 projects OR every 3 months (whichever comes first)

**Process:**
1. **Generate Arc Performance Report:**
   - Calculate average quality_score per arc type
   - Identify worst-performing arc (lowest avg score)

2. **Flag for Optimization:**
   - If any arc averages < 60 after 10 projects → **OPTIMIZATION REQUIRED**
   - Review the arc's scoring rubric
   - Review the arc's cluster structure
   - Consider adding new functional tags or adjusting weights

3. **Update Intelligence:**
   - Document findings in `intelligence/logs/QUARTERLY_ARC_REVIEW_[DATE].md`
   - Propose rubric updates or arc hunter modifications

---

## Example Quarterly Report

```markdown
# Quarterly Arc Review — Q1 2026

## Performance Summary (15 projects analyzed)

| Arc Type | Projects | Avg Quality Score | Status |
|----------|----------|-------------------|--------|
| Witness | 6 | 82 | ✅ GOOD |
| Breakthrough | 4 | 58 | ⚠️ NEEDS OPTIMIZATION |
| Shared Struggle | 2 | 76 | ✅ GOOD |
| Confrontation | 3 | 71 | ✅ ACCEPTABLE |

## Findings

**Breakthrough Arc (58 avg):**
- **Issue:** B3 (EPIPHANY) cluster consistently WEAK
- **Root Cause:** Agents struggle to find the exact "Wait..." moment in transcripts
- **Proposed Fix:** Lower minimum score for B3 from 26/30 to 24/30
- **Alternative:** Add more specific extraction prompts for epiphany detection

**Action Items:**
1. Review `breakthrough_scoring.md` B3 weighting
2. Test revised rubric on 3 previously failed projects
3. Document results in next quarterly review
```

---

## Integration with Commander

Update THE PREMISE COMMANDER to:
1. Calculate quality_score after validation
2. Log to `quality_scores.json`
3. Include quality_score in `[PROJECT]_PREMISE_AUTHORIZED.md` output

---

**Usage:** Automatic. The Commander executes this after every validation.
