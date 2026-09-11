# Question Heritage Audit — Change Your Questions, Change Your Life

**Author:** Marilee Adams, Ph.D.
**Source file:** `books_markdown/Change_Your_Questions_Change_Your_Life_-_Marilee_Adams.md`
**Edition / publication:** Second Edition; Berrett-Koehler Publishers, 2009 copyright, paperback 2010 printing noted in source metadata
**Audit status:** `COMPLETE`
**Source verification:** `VERIFIED`

## 0. Source Verification & Reading Record

The assigned local source is the full Markdown conversion of Marilee Adams's *Change Your Questions, Change Your Life*. The conversion manifest records 145 source pages, 143 nonempty extractions, and empty extraction pages 1 and 145. Per the operator instruction for this audit, those blank pages are ignored and all 143 populated pages are treated as the operative source. The Markdown itself identifies the conversion method as the bundled `prepare_book_markdown.py`/pypdf pipeline and says the original PDF remains authoritative. Because the PDF is not in the supplied bundle, this audit verifies continuity and content against the populated Markdown rather than claiming independent PDF inspection.

The full populated source was read end-to-end: introduction, all twelve chapters, tools section, notes, acknowledgments, author/about-the-Inquiry-Institute material, and closing pages. The source runs from page 21 through populated page 143; only pages 1 and 145 are empty.

Execution remains audit-only. No Question Primitive YAML, canonical primitive ID, registry entry, or production runtime code was created or modified. The audit distinguishes direct source claims from auditor synthesis and from CAE application hypotheses.

## 1. Executive Summary & Computational Reframing

Adams's central contribution is not merely “ask better questions.” It is a control loop for changing the mental state from which questions are generated and answered. The narrative treats internal self-questions as behavior-generating instructions that shape attention, interpretation, emotion, action, and results (pp. 30–32). The Choice Map then operationalizes a Learner/Judger distinction, observation, switching, and question selection (pp. 38–48, 73–79).

For CAE Question Intelligence, the reframing is stateful. A question's function depends on current stance, situation, desired result, active assumptions, and whether inquiry seeks facts, interpretation, possibilities, relationship repair, or action. Adams operationalizes observation, Judger-to-Learner switching, assumption exposure, first-person ideation, question-only generation, and a twelve-question diagnostic (pp. 91–105, 118–133).

The book therefore offers a reusable architecture around **question function + operator state + transition**. A strong implementation should preserve the transition and answer transformation, not merely copy question stems.

## 2. Candidate Question Mechanisms

### M1 — Observer-State Gate
**Source location:** pp. 40–43; 46–48; 118–120.

**Description:** Before attempting to change the situation, explicitly observe current thoughts, feelings, language, mood, and bodily signals without immediately judging or acting. Adams describes the observer as a capacity for stepping outside the current reaction and asking, in effect, “What is present now?” (pp. 40, 46–48, 120). The source ties this to distinguishing one’s interpretation from what is actually happening.

**Differentiating property:** The mechanism is a pre-question state gate. It can inspect the questioner as part of the problem before inspecting the interviewee or topic.

**Formula:** notice signal -> pause/nonjudgmental observation -> identify current Self-Q / state -> only then select next question.

**Preconditions:** enough attention to pause; a high-activation cue is detectable.

**Inappropriate conditions:** emergencies requiring immediate action; contexts where “observe yourself” would become avoidance.

**Expected answer transformation:** reactive, self-protective framing -> more deliberately selected inquiry. CAE relevance is strongest as a trigger before tough questions or after a sudden defensive reaction.

**Uncertainty:** The book strongly asserts behavioral benefit, but most evidence is experiential and narrative rather than controlled experimental validation.

### M2 — Judger-to-Learner Switch
**Source location:** pp. 44–49; 73–79; 128–129.

**Description:** Detect a Judger state, then ask a Switching question designed to move from reaction into curiosity and choice. Examples include “How else can I think about him?”, “What’s happening here?”, “What are the facts?”, and “What’s my choice right now?” (pp. 44, 78, 129).

**Differentiating property:** Unlike generic reframing, the switch is contingent on an identified state and is designed as a rescue operation: Judger -> Switch -> Learner.

**Formula:** state cue -> acknowledge Judger -> switching question -> newly available perspective/options -> next action.

**Preconditions:** recognition of the state; a questioner willing to suspend the first interpretation.

**Inappropriate conditions:** when the Judger conclusion is being treated as settled fact with no need for inquiry, or when switching would suppress legitimate criticism rather than improve it.

**Expected answer transformation:** defensive or adversarial answer -> more exploratory answer, often with added facts or alternative explanations.

**Uncertainty:** The mechanism is highly actionable, but causal generalization beyond the author's examples should remain provisional.

### M3 — Assumption-Busting Question Audit
**Source location:** pp. 92–94; 127; 133.

**Description:** When stuck, surface hidden assumptions explicitly: assumptions about self, others, the past, resources, and what is or is not possible; then test alternative interpretations. Adams presents this as a disciplined way to expose blind spots (pp. 93, 127).

**Differentiating property:** It targets the unseen premise underneath a question rather than merely asking for more facts.

**Formula:** state problem -> list assumptions -> test each -> generate alternative interpretation -> re-question.

**Preconditions:** a situation involving uncertainty, interpersonal interpretation, or a stalled goal.

**Inappropriate conditions:** cases where assumptions are externally verified facts; prolonged assumption-searching after the decision threshold is met.

**Expected answer transformation:** confident but premise-bound explanation -> qualified, comparative, more evidence-seeking response.

### M4 — Other-Person Perspective Query
**Source location:** pp. 93–98; 133.

**Description:** Ask what the other person is thinking, feeling, and wanting, rather than only defending one's own interpretation. It is one of Ben's three explicit questions and appears in the Top Twelve list (pp. 93, 133).

**Differentiating property:** The mechanism redirects inquiry from “What do I believe about them?” to “What might be their internal position?”

**Formula:** suspend certainty -> model other's thinking/feeling/wanting -> ask/verify -> update relationship model.

**Preconditions:** a meaningful interpersonal counterpart and some uncertainty about motives or needs.

**Failure mode:** mind-reading if the inferred answer is not verified.

**Expected transformation:** accusation/attribution -> perspective hypothesis and potential clarification.

### M5 — Ask/Listen Ratio Correction
**Source location:** pp. 34–36; 122–124.

**Description:** Deliberately increase asking and reduce telling, then evaluate the effect. Adams explicitly frames interpersonal questioning as a practical communication ratio and asks readers to notice the quantity and quality of their questions (pp. 34, 123–124).

**Differentiating property:** This is a conversation-level allocation mechanism rather than a single question type.

**Formula:** estimate ask/tell ratio -> increase inquiry -> monitor response quality and contribution -> adjust.

**Preconditions:** conversational exchange with reciprocal participation.

**Inappropriate conditions:** situations where the interviewer must provide necessary instructions, disclose facts, or protect time/clarity.

**Expected transformation:** answer dependence on interviewer -> greater guest contribution and information yield.

### M6 — ABCC Choice Process
**Source location:** pp. 77–79; 92; 128.

**Description:** Aware: “Am I in Judger?” Breathe: pause and regain objectivity. Curiosity: “What’s happening here? What are the facts?” Choose: decide what to do with the improved view (pp. 77–78).

**Differentiating property:** It packages state detection, physiological interruption, evidence inquiry, and choice into a deterministic four-step recovery sequence.

**Formula:** Aware -> Breathe -> Curiosity -> Choose.

**Preconditions:** a reactive or high-stakes moment where a short pause is possible.

**Inappropriate conditions:** immediate safety situations or any context where breathing/pause language would be patronizing.

**Expected transformation:** emotional certainty -> fact-seeking plus explicit choice.

### M7 — Contribution-Oriented Inquiry
**Source location:** pp. 96, 104–105; 130.

**Description:** Shift from evaluating others for failure to asking what they can contribute, need, or want, and what effect the interviewer is having on them. Ben's breakthrough question is “What will help each of us make our best contribution?” (p. 104), followed by reflection on “What do other people have to offer?” and “What is my effect on them?” (p. 105).

**Differentiating property:** It changes the social objective from extraction/control to contribution discovery.

**Formula:** identify role conflict -> ask contribution/need/effect questions -> surface capabilities and needs -> redesign interaction.

**Preconditions:** collaborative work or interview contexts where other people's contribution has value.

**Inappropriate conditions:** situations where accountability or factual verification must come before collaborative framing.

**Expected transformation:** defensive or minimal answer -> capability, need, or support-oriented answer.

### M8 — Q-Storming
**Source location:** pp. 102–105; 131–132.

**Description:** Frame a problem and goal, elicit assumptions, then generate as many new questions as possible without interleaving answers or discussion. Questions are first-person singular/plural, mostly open-ended, and generated from Learner rather than Judger (pp. 102–104, 131).

**Differentiating property:** The unit of brainstorming is the question, and the explicit interruption rule prevents premature closure.

**Formula:** goal -> assumptions -> rapid question generation -> inspect novelty/gaps -> discuss -> action plan.

**Preconditions:** shared goal, psychological permission for imperfect questions, facilitator discipline.

**Inappropriate conditions:** time-critical incident response or meetings needing immediate execution rather than exploration.

**Expected transformation:** narrow solution set -> expanded problem representation and option space.

### M9 — Goal/Choice/Assumption/Responsibility Ladder
**Source location:** pp. 121–133, especially the Top Twelve Questions on pp. 132–133.

**Description:** Use a recurring sequence: desired outcome, choices, assumptions, responsibility, alternative perspective, other person's view, missing/avoided information, learning, action, further questions, win-win, possibility.

**Differentiating property:** It is a broad diagnostic lattice that prevents a conversation from jumping directly from problem to action.

**Formula:** want -> choices -> assumptions -> responsibility -> reframe -> perspective -> missing -> learn -> act -> ask -> mutual gain -> possible.

**Preconditions:** a complex decision or change question where several dimensions can be examined.

**Inappropriate conditions:** short factual lookups or highly constrained interviews where full traversal would be burdensome.

**Expected transformation:** single-track answer -> multi-dimensional response with options, ownership, uncertainty, and next steps.

### M10 — Positive/Successful-Experience Retrieval
**Source location:** pp. 73–74; 96; 121; 123–124.

**Description:** Deliberately recall a prior situation where the desired mindset or outcome worked, identify the questions that enabled it, and transfer learning to the current case. The tools section explicitly recommends learning from situations that worked as well as those that failed (p. 121).

**Differentiating property:** It retrieves functioning patterns rather than only diagnosing failure.

**Formula:** recall success -> isolate enabling questions -> compare with current state -> transfer/adapt.

**Preconditions:** some relevant prior experience exists.

**Inappropriate conditions:** novel crises with no useful analogue, or cases where prior success depended on materially different conditions.

**Expected transformation:** deficit-only explanation -> reusable success pattern and constructive action.

## 3. First-Principle Truths

**Principle 1 — Questions are action-shaping cognitive instructions.** Adams repeatedly argues that Self-Q's drive behavior and results, not merely information retrieval (pp. 31–32, 122). Auditor synthesis: question selection should therefore be modeled as an intervention on attention and action, not only as a request for an answer.

**Principle 2 — The state from which a question is asked matters to the quality of inquiry.** The Learner/Judger distinction, observer self, switching sequence, and bodily/mood cues all support this (pp. 40–48, 73–79). Auditor synthesis: the same surface question can have different operational effects depending on whether it is asked from curiosity, defense, blame, or openness.

**Principle 3 — Better inquiry expands the response space before narrowing it.** Q-Storming and the Top Twelve sequence explicitly delay closure, surface assumptions, and seek alternatives before action (pp. 102–105, 131–133). Auditor synthesis: CAE should distinguish exploratory expansion from answer extraction, because the former can materially improve downstream question selection.

## 4. MCDA — 0 to 200

| Mechanism | Determinism 40 | Evidence Yield 40 | Cognitive/Narrative 40 | Adaptability 30 | CAE Fit 30 | Cliché Resistance 20 | Total |
|---|---:|---:|---:|---:|---:|---:|---:|
| M1 Observer-State Gate | 31 | 27 | 34 | 25 | 29 | 15 | **161** |
| M2 Judger-to-Learner Switch | 35 | 29 | 36 | 28 | 30 | 16 | **174** |
| M3 Assumption-Busting Audit | 34 | 36 | 34 | 29 | 30 | 17 | **180** |
| M4 Other-Person Perspective Query | 27 | 31 | 35 | 29 | 28 | 13 | **163** |
| M5 Ask/Listen Ratio Correction | 28 | 33 | 28 | 27 | 25 | 10 | **151** |
| M6 ABCC Choice Process | 37 | 30 | 32 | 25 | 29 | 17 | **170** |
| M7 Contribution-Oriented Inquiry | 27 | 30 | 35 | 27 | 28 | 16 | **163** |
| M8 Q-Storming | 36 | 29 | 38 | 24 | 29 | 18 | **174** |
| M9 Goal/Choice/Assumption/Responsibility Ladder | 34 | 35 | 37 | 23 | 30 | 16 | **175** |
| M10 Positive/Successful-Experience Retrieval | 28 | 26 | 35 | 24 | 26 | 14 | **153** |

The highest scores go to mechanisms with a clear trigger-to-operation-to-state-change relationship and a visible answer-space effect. M3 leads because assumption testing changes what evidence is sought and which explanations remain viable (pp. 93–94, 127). M2 and M8 combine strong determinism with CAE fit: one changes stance at blockage; the other expands the question space (pp. 44, 128–132). M9 guards against premature closure, but full traversal is heavy for every interview turn. M5 is useful but generic unless its participation effect is contextualized.

## 5. Pareto / 80-20 Analysis

The highest-leverage cluster is **M2, M3, M8, and M9**. Together they cover four complementary moves: recover from a bad inquiry state, surface the premise underneath the current question, expand the space of possible questions, and then systematically inspect goal/choice/assumption/responsibility/perspective/action dimensions. M6 is a strong implementation wrapper around M2, especially for high-arousal contexts.

“High-value to study” is not equivalent to “eligible for promotion.” M2/M6 need cross-book testing against existing reframe or state-regulation concepts. M9 may be orchestration rather than one atomic primitive. M8 has unusually strong identity because its generation unit is questions rather than answers.

## 6. Answer Transformation Analysis

**M2:** reactive/defensive answer -> switching question -> curious, less adversarial answer -> better factual and relational signal. Source case: Ben's “prove I’m right” orientation changes toward “How can I understand?” (pp. 98–100).

**M3:** assumed explanation -> assumption audit -> multiple hypotheses + missing evidence -> more trustworthy interpretation. Ben's assumptions about Charles are weakened when he asks how else to think about him and what Charles may want (pp. 93–94).

**M6:** high-arousal certainty -> Aware/Breathe/Curiosity -> objective information search -> explicit choice. Stan's investment case shows the sequence moving him from rumor-driven judgment to fact collection before action (pp. 77–78).

**M8:** narrow solution framing -> question-only generation -> expanded question set + uncovered omissions -> broader decision space. Ben and Charles fill multiple sheets and discover questions they had not previously asked (pp. 102–105).

**M9:** problem statement -> structured twelve-question sweep -> answer includes goals, options, assumptions, responsibility, other viewpoints, missing information, learning, action, mutual gain, possibility (pp. 132–133). This is especially valuable when the guest's first answer is polished but incomplete.

## 7. Four CAE Case Studies

### Case 1 — Defensive executive on a failed product
The interviewer hears a confident explanation that another team caused the failure. Before escalating, CAE applies M2/M3: “How else might you think about what happened?” followed by “What assumptions are we making about where the failure began?” Expected response: the guest distinguishes verified facts from attribution and identifies a second causal pathway. Downstream use: stronger episode narrative because the answer contains competing explanations and ownership rather than a single blame story. This is an application hypothesis, not a claim from Adams.

### Case 2 — Founder with rehearsed innovation story
The founder repeatedly says the company “listens to customers.” CAE applies M8 in a compact adaptation: generate question variants internally—What customer assumption did we challenge? What did we learn that contradicted us? What question changed the roadmap? Expected guest response: a concrete turning point rather than a slogan. Downstream use: extract origin story mechanics and decision evidence.

### Case 3 — Conflict-heavy leadership interview
A leader becomes visibly tense when asked about a departed executive. CAE uses the M1/M6 state gate for the interviewer and then asks a Learner-oriented question: “What did you learn about how the two of you were interpreting the situation differently?” Expected response: less defensive narrative, more reflection and perspective-taking. Downstream use: richer relational explanation without forcing confession or confrontation.

### Case 4 — Strategic ambiguity with many plausible futures
A guest is asked where an industry is headed and gives one confident forecast. CAE applies M9: What do you want? What choices are open? What assumptions are you making? What might you be missing? What is possible? Expected response: explicit scenarios, uncertainty, decision criteria, and action conditions. Downstream use: reusable decision intelligence rather than a single prediction. Again, this is a CAE application hypothesis.

## 8. SWOT Analysis

**Strengths:** The book supplies explicit state transitions, concrete question lists, repeatable practice routines, team applications, and an unusually clear connection between internal questions and outward behavior. M2/M6 are especially operational because they include a trigger and a sequence. M8 has a distinct procedural constraint: generate questions before answers.

**Weaknesses:** Much evidence is narrative, workshop-derived, or experiential. “Learner” and “Judger” can become labels if observer discipline is omitted. The Top Twelve list overlaps generic coaching questions.

**Opportunities:** CAE can use the mechanisms as routing rules: reaction -> switch; hidden premise -> audit assumptions; premature closure -> expand; broad ambiguity -> sequence. This can improve sequencing without a large static prompt bank.

**Threats:** A mechanical implementation could sound therapeutic, preachy, or formulaic. Using Judger/Learner language with guests may create unwanted diagnosis. “Ask more” can reduce efficiency when information delivery is actually needed. Q-Storming can become noise if the problem, goal, or assumptions are not defined first.

## 9. Taxonomy & Orthogonal-Dimension Review

**Retained dimensions:** The source supports keeping mechanism type, trigger/condition, response transformation, contextual fit, and downstream use. It also reinforces a distinction between internal Self-Qs and interpersonal questions (pp. 122–124).

**Refinements:** A current question taxonomy should distinguish the **question wording** from the **operator state** and from the **transition target**. Adams makes this distinction explicit: a switching question is defined not only by words but by its role in moving Judger to Learner (pp. 128–129). Q-Storming similarly shows a mode where questions are generated “to think with,” not necessarily to ask another person (p. 131).

**New dimension discovered:** **Inquiry-State Transition** deserves explicit consideration as an orthogonal dimension. This dimension records whether a question is intended to stabilize, switch, expand, clarify, redistribute agency, or close an inquiry state. It is not synonymous with tone. Two questions can both be warm and open-ended while performing different state transitions.

**Additional refinement:** Add **Question Object** as a possible orthogonal dimension: self, other person, relationship/system, problem/goal, or future possibility. Adams's Self-Q/interpersonal distinction and her Top Twelve perspectives support this split (pp. 122–133).

**Do not force novelty:** “Learner vs Judger” should not automatically become a new taxonomy branch. It may be better represented as a state variable that conditions existing mechanisms.

**Unresolved:** whether positive framing is distinct once state transition is encoded, whether Q-Storming is orchestration rather than a primitive, and whether observer mode should be universal or triggered.

## 10. Cross-Book Clustering Hooks

Adams clearly overlaps with earlier Question Heritage themes around observation, adaptive follow-up, and reframing, but the distinctive hook is the explicit **state-to-question-to-result** chain. The closest conceptual neighborhood is likely the combination of Kvale/Brinkmann's interview craft, Grenny et al.'s state management under high stakes, and Kahneman's attention to assumptions and premature certainty. The present audit does not collapse these concepts. The useful comparison is whether Adams adds a more operational transition rule: detect the state, switch, then ask a question selected for the new state.

The strongest cross-book comparison candidate is **assumption auditing**. Unlike a generic request for evidence, M3 is specifically designed to expose the questioner's own premise. Another useful comparison is **question-space expansion**: Q-Storming resembles brainstorming but changes the generation unit from answers to questions, which may make it orthogonal to ordinary ideation rather than duplicative.

## 11. Candidate Promotion Recommendations

| Mechanism | Recommendation | Rationale |
|---|---|---|
| M1 Observer-State Gate | `PROMOTION_CANDIDATE` | Strong precondition logic; likely useful as an adaptive gate rather than standalone wording. Needs cross-book validation. |
| M2 Judger-to-Learner Switch | `PROMOTION_CANDIDATE` | Clear trigger and state transition; unusually operational. Test for overlap with existing reframe/switch mechanisms. |
| M3 Assumption-Busting Question Audit | `PROMOTION_CANDIDATE` | High evidence and reasoning yield; broadly applicable to investigative and strategic interviews. |
| M4 Other-Person Perspective Query | `MERGE_CANDIDATE` | Valuable but likely overlaps perspective-taking mechanisms already present elsewhere in Question Heritage. |
| M5 Ask/Listen Ratio Correction | `RESEARCH_MORE` | Useful communication strategy, but the primitive boundary is too generic without stronger contextual determinism. |
| M6 ABCC Choice Process | `PROMOTION_CANDIDATE` | Highly procedural and easy to gate; may be better implemented as a composite operator pattern. |
| M7 Contribution-Oriented Inquiry | `RESEARCH_MORE` | Strong team/leadership value; narrower CAE identity than M3 or M8. |
| M8 Q-Storming | `PROMOTION_CANDIDATE` | Distinct unit of generation and anti-closure rule; especially relevant for pre-interview preparation and strategic sessions. |
| M9 Goal/Choice/Assumption/Responsibility Ladder | `RESEARCH_MORE` | High leverage but composite; likely better as an orchestration/template than one atomic primitive. |
| M10 Positive/Successful-Experience Retrieval | `RESEARCH_MORE` | Promising narrative-learning mechanism but overlaps success-recall approaches; requires more comparative evidence. |

No canonical primitive ID is assigned, and no promotion is implied to have already occurred.

## 12. Source Integrity / Evidence Boundary

The original PDF is absent, so page verification is based on populated Markdown. The manifest says the PDF remains authoritative and flags manual verification. Per the operator instruction, Markdown substitutes for the PDF and pages 1 and 145 are excluded as empty.

Some causal language is stronger than the evidence type. Claims of reliable life, team, or financial outcomes are treated as author-reported examples unless independently validated. References in the notes were not substituted for direct verification of Adams's mechanisms.

Memorable question lists can look more deterministic than they are. Future implementation should test whether each mechanism still works when stripped of metaphors, character names, and coaching context.

## 13. Audit Conclusion

*Change Your Questions, Change Your Life* materially adds a missing layer to Question Intelligence: **questions as controllable state transitions**. The most important contribution is not a vocabulary of empowering questions. It is the idea that an interviewer can observe the current inquiry state, detect when the current question-generation process is trapped, deliberately switch, and then select questions that change what information, perspective, contribution, or possibility becomes available.

For CAE, the highest-value research path is to test M2/M3/M6/M8 as operational mechanisms and to treat M9 as a possible orchestration layer. The taxonomy should explicitly consider Inquiry-State Transition and Question Object as orthogonal dimensions while resisting the temptation to canonize Judger/Learner as a top-level primitive family.

The next operator action is comparative validation across the broader Question Heritage set. No primitive should be promoted solely because this book presents it fluently or because its questions sound useful. Promotion should require cross-book distinctiveness, deterministic behavior, measurable answer transformation, contextual safety, and successful operation outside the book's coaching narrative.
