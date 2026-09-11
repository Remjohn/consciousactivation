# CAE Agent Authoring Skill

## Purpose
Create, upgrade, review, and migrate CAE agents to **CAE Agent Kernel v0.4**. Produce behavioral expert agents rather than static role descriptions.

## Inputs
Required: agent ID/name, role, operating level, mission, primary output, and neighboring agents. Preferred: existing agent file, skills/workflows, CAE level definitions, project principles, and handoff targets.

## Authoring Rules
1. Read the v0.4 kernel first.
2. Preserve the source agent's valid mission, boundaries, operating level, responsibilities, skills, and outputs.
3. Convert responsibilities into observable behaviors.
4. Give the agent a real expert worldview and decision heuristics.
5. Encode investigation and evidence behavior appropriate to its level.
6. Encode uncertainty, contradiction, failure, escalation, and handoff.
7. Add an agent-specific quality loop.
8. Add a natural-language capability menu.
9. Write 500–700 words of substantive content; target 550–650.
10. Reject generic filler used only to hit the word count.
11. Never weaken kernel requirements.

## Required Shape
```markdown
# <Name>

## Kernel
## Identity & Persona
## Operating Doctrine
## Decision Heuristics
## Activation & Context
## Investigation Protocol
## Evidence & Uncertainty
## Execution Loop
## Quality Loop
## Boundaries & Escalation
## Handoff Protocol
## Capability Menu
## Output Contract
```

## Authoring Sequence

### 1. Establish the unique boundary
Answer: "What is this agent uniquely accountable for that its nearest neighbors are not?"
Then define owns, influences, inspects, does not decide, and escalation.

### 2. Build the persona
Define optimization target, distrust signal, preferred trade-off, characteristic question, and characteristic failure mode. Persona must alter behavior.

### 3. Write heuristics
Create 5–8 behavioral rules using verbs such as prefer, verify, compare, challenge, preserve, refuse, test, escalate.

### 4. Define investigation
Specify starting level, descent triggers, permitted evidence, stop conditions, lineage requirements, and what happens when documentation and implementation disagree.

### 5. Define execution
Describe how this agent moves from request to evidence to model/decision to output. Include when it pauses, asks, delegates, or escalates.

### 6. Define the quality loop
Use common checks—completeness, consistency, evidence, traceability, boundaries, downstream usefulness—plus one domain-specific adversarial lens.

### 7. Define handoff
Specify likely senders/receivers and the exact packet required for clean continuation.

### 8. Lint
Confirm every required section exists, the agent is materially differentiated, there are no placeholders, and substantive word count is 500–700.

## Upgrade Mode
Rewrite around the kernel rather than appending the kernel to a v0.3 file. Keep the original domain intent, but convert thin bullets into executable behavior. Do not collapse specialized knowledge into generic instructions.

## Review Rubric
Score 0–2 for: distinct identity, behavioral specificity, heuristics, investigation depth, evidence discipline, uncertainty handling, quality loop, handoff quality, boundary clarity, downstream utility. Any zero in evidence, quality, or boundaries blocks publication.

## Completion Contract
Return file path, word count, kernel version, validation result, unresolved assumptions, and recommended neighboring-agent review.
