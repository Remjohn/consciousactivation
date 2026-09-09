# Sonic Vacuum Detection Guide — Universal Protocol

**Principle IV:** "Music carries the emotion; Silence carries the epiphany."

---

## What is a Sonic Vacuum?

A **Sonic Vacuum** is the exact moment where:
1. The background music STOPS
2. The speaker pauses (often naturally)
3. The PIVOT or REALIZATION hits
4. Silence (or minimal ambient sound) holds for 1-3 seconds

**Purpose:** Create cinematic emphasis. The greatest viral moments occur when the noise stops.

---

## Arc-Specific Sonic Vacuum Rules

| Arc Type | Requires Vacuum? | Placement | Duration |
|----------|-----------------|-----------|----------|
| **Witness** | Optional | Before W4 (PROOF) — The moment of truth | 1-2s |
| **Breakthrough** | **MANDATORY** | Before B3 (EPIPHANY) — The "Wait..." moment | 2-3s |
| **Confrontation** | Optional | Before CF3 (TAKEDOWN) — The reveal | 1-2s |
| **Shared Struggle** | No | N/A | N/A |
| **Core Transformation** | Optional | CT2 (WOUND) — The vulnerability reveal | 1-2s |
| **Warning** | Optional | W3 (CRISIS) — The "and then..." moment | 1-2s |
| **Quiet Reflection** | Optional | QR3 (UNDERSTANDING) — The gift realization | 2-3s |
| **Comedic Reframe** | No | N/A (silence kills comedy) | N/A |
| **Divine Spark** | Optional | DS3 (GRACE) — The arrival moment | 2-3s |
| **Call to Adventure** | Optional | CA3 (SPARK) — The catalyst | 1-2s |
| **Rally** | Optional | R3 (RALLY POINT) — The "Not today" moment | 1-2s |
| **Ticking Clock** | Optional | TC2 (CATALYST) — When the deadline hits | 1s |
| **Sacred Return** | Optional | SR4 (GIFT) — The wisdom reveal | 2s |

---

## Detection Protocol

### Step 1: Identify the Pivot Cluster
Every arc has ONE cluster where the energy SHIFTS:
- Breakthrough: B3 (Anxiety → Epiphany)
- Witness: W4 (Discovery → Proof)
- Confrontation: CF3 (Lie → Takedown)

### Step 2: Find the Exact Quote
Within that cluster, find the quote where the shift happens. Look for:
- "Wait..."
- "And then..."
- "Suddenly..."
- "That's when..."
- A natural pause in speech (transcript shows "..." or long pause)

### Step 3: Mark the Timestamp
Extract:
- The EXACT second the realization begins
- The quote text before and after the pause
- Recommended silence duration

### Step 4: Output Format
```json
"sonic_vacuum": {
  "timestamp": "0:32",
  "cluster": "[CLUSTER_ID]",
  "trigger_quote": "[The exact quote]",
  "pause_point": "[Where in the quote does silence begin?]",
  "duration_seconds": 2,
  "instruction": "Kill background track. Hold silence for 2 seconds before resuming."
}
```

---

## Example: Breakthrough Arc

**Quote:** *"Wait... I thought I needed to control everything. [PAUSE] But letting go WAS the control."*

**Sonic Vacuum:**
```json
"sonic_vacuum": {
  "timestamp": "0:31",
  "cluster": "B3_EPIPHANY",
  "trigger_quote": "Wait... I thought I needed to control everything. But letting go WAS the control.",
  "pause_point": "After 'everything' — natural speaker pause",
  "duration_seconds": 2,
  "instruction": "Kill background track at 0:31. Hold silence through pause. Resume at 0:33."
}
```

---

## Example: Witness Arc (Optional)

**Quote:** *"Within 6 weeks, my energy went from a 3 to an 8. [PAUSE] I can work full days again."*

**Sonic Vacuum:**
```json
"sonic_vacuum": {
  "timestamp": "0:42",
  "cluster": "W4_PROOF",
  "trigger_quote": "Within 6 weeks, my energy went from a 3 to an 8. I can work full days again.",
  "pause_point": "After '8' — before the result statement",
  "duration_seconds": 1,
  "instruction": "Brief vacuum before 'I can work full days again' to emphasize result."
}
```

---

## When NOT to Use

**Avoid Sonic Vacuums when:**
- The arc is COMEDIC (silence kills comedy rhythm)
- The arc is SHARED STRUGGLE (communal energy needs music)
- There is NO natural pause in the speaker's delivery
- The quote is already understated (adding silence would make it awkward)

---

## Integration with Sonic Scribe

The Sonic Scribe agent reads the `sonic_vacuum` field and:
1. Marks it in the lyrics output
2. Instructs Suno.ai to create a music break at that timestamp
3. Ensures the video editor knows to hold the silence

---

**Usage:** All Arc Hunters should check for Sonic Vacuum opportunities in their PIVOT cluster.
