# Level Investigation Trace — {{TRACE_ID}}

**Inquiry:** {{INQUIRY}}  
**Initial Operating Level:** `{{INITIAL_LEVEL}}`  
**Terminal Operating Level:** `{{TERMINAL_LEVEL}}`  
**Stop Condition Met:** `{{STOP_CONDITION}}`

---

## 1. Traversal Step Log

| Step # | From Level | To Level | Agent | Inspection Target | Observed Ground Truth Evidence |
|---|---|---|---|---|---|
| 1 | `{{STEP1_FROM}}` | `{{STEP1_TO}}` | `{{STEP1_AGENT}}` | `{{STEP1_TARGET}}` | {{STEP1_EVIDENCE}} |
| 2 | `{{STEP2_FROM}}` | `{{STEP2_TO}}` | `{{STEP2_AGENT}}` | `{{STEP2_TARGET}}` | {{STEP2_EVIDENCE}} |

---

## 2. Empirical Ground Truth Summary
- **Verified Fact:** {{VERIFIED_FACT}}
- **Code Reference:** `{{CODE_PATH}}#L{{LINE_NUMBER}}`
- **Execution Test Command:** `{{TEST_CMD}}`

---

## 3. Ascent Conclusion & Abstraction Impact
- **Impact on Documentation (Level 02):** {{DOC_IMPACT}}
- **Impact on Plan (Level 03):** {{PLAN_IMPACT}}
- **Verdict:** `{{VERDICT}}`
