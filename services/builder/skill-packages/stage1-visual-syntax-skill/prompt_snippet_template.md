# Harness Build Prompt Snippet — Template

This is what the operator actually copy-pastes per harness. It is deliberately thin. It identifies the harness and tells the agent to execute the Skill — it does not restate any rule that already lives in `SKILL.md`. If you ever find yourself adding a rule here instead of in `SKILL.md`, stop — put it in the Skill instead, so it governs every future call automatically instead of only the one you're editing.

---

```text
STAGE 1 — SINGLE HARNESS BUILD CALL

harness_id: <HARNESS_ID>
source_zip: <path — already selected by operator>

Execute: /stage1-visual-syntax-skill/SKILL.md
Process ONLY this harness. Do not proceed to any other harness in this call.
Stop after the contract report. Do not self-declare STAGE1_COMPLETE.
```

---

## Why it's this short

Everything else — what counts as a valid observation, how taxonomy resolution works, what the data-integrity receipt must contain, what technical status means, why `STAGE1_COMPLETE` requires both a technical pass and an operator APPROVE, why this is one-harness-at-a-time — already lives in `SKILL.md` and `contracts/`. Restating any of it here would create two places where the rules live, and the two would eventually drift. If the definition of a taxonomy candidate turns out to be wrong, it gets fixed once, in the Skill. Nobody has to hunt through past prompts to find every place the old definition was copy-pasted.

## Filling in the template

* `harness_id` — the harness the operator is choosing to build right now. This is the operator's selection act referenced in `SKILL.md` §0 — nothing downstream re-asks whether this harness "should" be built.
* `source_zip` — wherever the operator has the actual bytes for this harness. The Skill's integrity receipt (§3) will record and check the hash of whatever is at this path; it does not evaluate whether the path is the "right" or "allowed" one.

## What happens if the agent tries to do more than this

If a Harness Build Call somehow results in the agent processing a second harness, batching, or skipping the stop-and-report step, that is a Skill-execution defect, not an acceptable optimization — see `SKILL.md` §12.
