# Step 2C: Quality Gap Analysis Template (For Arc Hunters)

**This document provides the Step 2C template to be added after Step 2B in all Arc Hunters.**

---

## FOR BREAKTHROUGH ARC HUNTER

### Step 2C: Quality Gap Analysis (🆕 CRITICAL FEEDBACK LOOP)

**Purpose:** Detect when quotes exist but DON'T MEET cluster-specific quality thresholds.

After scoring all quotes in each cluster, perform **QUALITY CHECK**:

```
FOR each cluster:
  best_score = MAX(all quote scores in cluster)
  cluster_threshold = [from breakthrough_scoring.md cluster-specific minimums]
  
  IF best_score < cluster_threshold:
    → FLAG: Quality Gap Detected
    → ATTEMPT: Targeted pattern re-scan
    → REPORT: quality_gap_report entry
```

**Cluster-Specific Thresholds (from breakthrough_scoring.md):**
- B1 (ANXIETY): Minimum 22/30 + Emotion ≥8 on Vulnerability Hierarchy
- B2 (STRUGGLE): Minimum 20/30
- B3 (EPIPHANY): Minimum 26/30 + Specificity ≥8 on Epiphany Ladder + **SONIC VACUUM REQUIRED**
- B4 (EMPOWERMENT): Minimum 20/30

**Targeted Re-Scan Patterns by Cluster:**

**B3 (EPIPHANY) - If best_score < 26 OR Specificity < 8 OR Sonic Vacuum missing:**
- Search for: "Wait", "Suddenly", "Then I realized", "It hit me"
- Look for: Binary flip patterns ("I thought X, but actually Y")
- Check for: Pause moments, silence, "stop" language
- **CRITICAL:** Detect Sonic Vacuum timestamp (speaker pause/breath)

**B1 (ANXIETY) - If Emotion < 8 on Vulnerability Hierarchy:**
- Search for: "couldn't breathe", "suffocating", "drowning", "trapped"
- Look for: Physical panic symptoms ("chest tight", "racing heart")
- Check for: Claustrophobic metaphors

**B2 (STRUGGLE) - If best_score < 20:**
- Search for: "tried everything", "nothing worked", "getting worse"
- Look for: Escalation language ("more and more", "spiraling")

**Output Format (add to Quote Manifest):**

```json
"quality_gap_report": {
  "B3_EPIPHANY": {
    "status": "BELOW_THRESHOLD",
    "required_minimum": 26,
    "best_score_found": 21,
    "specificity_ladder_score": 6,
    "required_specificity": 8,
    "sonic_vacuum_detected": false,
    "pattern_search_attempted": ["Wait", "suddenly", "realized"],
    "patterns_found": 2,
    "reason": "Transcript lacks clear 'aha' moment with exact trigger phrase. Sonic Vacuum not detected.",
    "recommendation": "SOURCE_INSUFFICIENT - Epiphany is vague. Consider using different arc.",
    "alternative_quotes": [...]
  },
  "overall_quality_status": "QUALITY_GAPS_DETECTED",
  "commander_action_required": true
}
```

**Critical Rule:** DO NOT INVENT quotes. Report gaps honestly.

---

## FOR SHARED STRUGGLE ARC HUNTER

### Step 2C: Quality Gap Analysis (🆕 CRITICAL FEEDBACK LOOP)

**Cluster-Specific Thresholds:**
- SS1 (ISOLATION): Minimum 18/30
- SS2 (RECOGNITION): Minimum 22/30 + Specificity ≥7 on Collective Ladder
- SS3 (UNITY): Minimum 20/30
- SS4 (EMPOWERMENT): Minimum 20/30 + Collective CTA present

**Targeted Re-Scan Patterns:**

**SS2 (RECOGNITION) - If Specificity < 7 on Collective Ladder:**
- Search for: Statistics ("90%", "thousands of", "millions")
- Look for: Named demographics ("women in their 40s", "entrepreneurs")
- Check for: "We" language count ≥5 across script

**SS4 (EMPOWERMENT) - If lacks Collective CTA:**
- Search for: "We refuse", "Together we", "We're done", "Let's"
- Look for: Collective action verbs ("stand", "rise", "reclaim")

**"We" Language Validation:**
- Count total "we/us/our" occurrences
- IF count < 5 → FLAG: "Insufficient community language"
- Attempt re-scan for collective framing

---

## FOR CONFRONTATION ARC HUNTER

### Step 2C: Quality Gap Analysis (🆕 CRITICAL FEEDBACK LOOP)

**Cluster-Specific Thresholds:**
- CF1 (SETUP): Minimum 18/30
- CF2 (THE LIE): Minimum 20/30 + Named villain present
- CF3 (TAKEDOWN): Minimum 24/30 + Evidence ≥8 on Evidence Ladder
- CF4 (TRUTH): Minimum 20/30
- CF5 (CONFIDENCE): Minimum 18/30

**Targeted Re-Scan Patterns:**

**CF2 (THE LIE) - If no named villain:**
- Search for: Proper nouns (capitalized multi-word phrases)
- Look for: Industry labels ("diet industry", "Big Pharma", "mainstream medicine")
- Check for: "They" references with specific antecedents

**CF3 (TAKEDOWN) - If Evidence < 8 on Evidence Ladder:**
- Search for: Statistics (`\d+%`, dollar amounts)
- Look for: "For example", "The data shows", "Look at"
- Check for: Logic patterns ("If X worked, why Y?")

**Villain Naming Validation:**
- Check CF2 for named entity
- IF missing → Re-scan for blame/critique targets
- IF still missing → FLAG: "No specific villain named"

---

---

## FOR CALL TO ADVENTURE ARC HUNTER

### Step 2C: Quality Gap Analysis (🆕 CRITICAL FEEDBACK LOOP)

**Cluster-Specific Thresholds:**
- CA1 (STATUS): Minimum 18/30
- CA2 (CALL): Minimum 22/30 + Specificity ≥8 on Invitation Ladder
- CA3 (RESISTANCE): Minimum 24/30 + Tangibility ≥8
- CA4 (LEAP): Minimum 24/30 + Kinetic Score ≥8

**Targeted Re-Scan Patterns:**

**CA2 (CALL) - If Specificity < 8:**
- Search for: "Email", "Phone call", "Meeting", "Sign", "Contract"
- Look for: Dates, times, locations
- Check for: Imperative verbs ("Come", "Go", "Look")

**CA3 (RESISTANCE) - If Tangibility < 8:**
- Search for: "Money", "Fear", "Reputation", "Safety", "Loss"
- Look for: Specific assets at risk ("Pension", "House", "Friendship")

---

## FOR COMEDIC REFRAME ARC HUNTER

### Step 2C: Quality Gap Analysis (🆕 CRITICAL FEEDBACK LOOP)

**Cluster-Specific Thresholds:**
- CR1 (SETUP): Minimum 18/30 + Deception Check (Must sound serious)
- CR2 (TWIST): Minimum 28/30 (Surprise ≥10)
- CR3 (ABSURDITY): Minimum 24/30 + Specificity ≥8
- CR4 (TRUTH): Minimum 20/30

**Targeted Re-Scan Patterns:**

**CR2 (TWIST) - If Surprise < 10:**
- Search for: "But actually", "Except", "Wrong", "Lie"
- Look for: Contradictions to CR1
- Check for: Timestamp < 20s

**CR3 (ABSURDITY) - If Specificity < 8:**
- Search for: Objects, Numbers, Brands, Colors
- Look for: Juxtapositions ("Yoga mat" + "Cigarette")

---

## FOR DIVINE SPARK ARC HUNTER

### Step 2C: Quality Gap Analysis (🆕 CRITICAL FEEDBACK LOOP)

**Cluster-Specific Thresholds:**
- DS1 (DARK): Minimum 26/30 (Despair ≥9)
- DS2 (SPARK): Minimum 24/30 + Sensory Check (No Woo-Woo)
- DS3 (SURRENDER): Minimum 26/30 + Ego Death explicit
- DS4 (FLOW): Minimum 20/30

**Targeted Re-Scan Patterns:**

**DS2 (SPARK) - If Abstract ("I felt energy"):**
- Search for: "Heat", "Cold", "Light", "Sound", "Silence"
- Look for: "My chest", "My head", "My hands" (Somatic location)

**DS3 (SURRENDER) - If Ego Active:**
- Search for: "Give up", "Take it", "Done", "Stop fighting"
- Look for: Passive verbs vs Active verbs

---

**Usage:** Insert this Step 2C after Step 2B (Gap Analysis) in each respective Arc Hunter file.

**Integration Point:** Between "Step 2B: Gap Analysis" and "Step 3: Quote Scoring"

---

## FOR TICKING CLOCK ARC HUNTER

### Step 2C: Quality Gap Analysis (🆕 CRITICAL FEEDBACK LOOP)

**Cluster-Specific Thresholds:**
- TC1 (STAGNATION): Minimum 18/30 + Cost Specificity ≥8
- TC2 (URGENCY): Minimum 22/30 + Acceleration Check
- TC3 (DECISION): Minimum 26/30 + **SONIC VACUUM REQUIRED**
- TC4 (MOMENTUM): Minimum 20/30

**Targeted Re-Scan Patterns:**

**TC1 (STAGNATION) - If Specificity < 8:**
- Search for: "Years", "Money", "Lost", "Missed", "Regret"
- Look for: Specific numbers ($) or events
- Check for: "I wish I had started sooner"

**TC3 (DECISION) - If Impact < 10:**
- Search for: "Now", "Stop", "Decided", "Done", "Enough"
- Look for: Short binary phrases
- Check for: [SILENCE] markers

---

## FOR QUIET REFLECTION ARC HUNTER

### Step 2C: Quality Gap Analysis (🆕 CRITICAL FEEDBACK LOOP)

**Cluster-Specific Thresholds:**
- QR1 (NOISE): Minimum 18/30 + Contrast Check
- QR2 (PAUSE): Minimum 24/30 + Silence Duration Check
- QR3 (MEMORY): Minimum 26/30 + Sensory Specificity ≥9
- QR4 (WISDOM): Minimum 20/30

**Targeted Re-Scan Patterns:**

**QR3 (MEMORY) - If Sensory < 9:**
- Search for: "Smell", "Sound", "Light", "Touch", "Taste"
- Look for: Physical details ("Cold floor", "Yellow sun")
- Check for: "I remember..."

**QR1 (NOISE) - If Contrast < 7:**
- Search for: "Busy", "Fast", "Crazy", "Running", "Blind"
- Look for: High-energy verbs
- Check for: "I didn't stop"

---

## FOR SACRED RETURN ARC HUNTER

### Step 2C: Quality Gap Analysis (🆕 CRITICAL FEEDBACK LOOP)

**Cluster-Specific Thresholds:**
- SR1 (OLD WORLD): Minimum 18/30
- SR2 (TRIALS): Minimum 24/30 + Scar Specificity ≥8
- SR3 (RETURN): Minimum 22/30 + Contrast Check
- SR4 (GIFT): Minimum 24/30 + Utility ≥8

**Targeted Re-Scan Patterns:**

**SR2 (TRIALS) - If Specificity < 8:**
- Search for: "Lost", "Fail", "Pain", "Broke", "Empty"
- Look for: Description of the "Dragon" (Conflict)
- Check for: "I didn't think I'd make it"

**SR4 (GIFT) - If Utility < 8:**
- Search for: "You", "Here is", "Lesson", "Map", "Secret"
- Look for: Direct address to audience
- Check for: "So you don't have to"
