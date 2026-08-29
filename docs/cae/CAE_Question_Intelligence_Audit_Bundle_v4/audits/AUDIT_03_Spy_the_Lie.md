# Question Heritage Audit — *Spy the Lie*

**Author:** Philip Houston, Michael Floyd, Susan Carnicero, and Don Tennant  
**Source file:** `CAE_Question_Intelligence_Audit_Bundle_v4/books_markdown/Spy_the_Lie_-_Philip_Houston.md`  
**Edition / publication:** UK electronic edition, Icon Books Ltd, 2012; ISBNs shown in source: 978-1-84831-426-9 (ePub) and 978-1-84831-500-6 (Adobe ebook)  
**Audit status:** `COMPLETE`  
**Source verification:** `VERIFIED`

## 0. Source Verification & Reading Record

The assigned source was audited from the supplied Markdown conversion, as explicitly authorized for this execution because the original PDF is not included in the bundle. The conversion manifest records:

- converter: `pypdf`;
- extracted page count: 222;
- nonempty extraction pages: 220;
- empty extraction pages: 1–2;
- `complete_read_requires_manual_verification: true`.

The Markdown contains `Source Page` markers continuously from Source Page 1 through Source Page 222. Source Pages 1–2 contain explicit empty-extraction markers. Substantive text begins on Page 3 and continues through the index/glossary material on Page 222. The complete available Markdown was read, including the introduction, Chapters 1–14, both appendices, glossary, and index.

Because the original PDF is absent, Source Pages 1–2 cannot be manually compared against the page images. This is a **Markdown-complete audit with a front-matter verification limitation**, not a claim that the empty pages were visually verified. No material extraction gap was identified elsewhere in the supplied Markdown.

The source itself repeatedly warns against overgeneralizing behavioral cues. That warning is important to this audit: the book's strongest Question Intelligence contribution is not a universal “lie detector,” but a structured approach to **stimulus design, response observation, follow-up selection, and narrative expansion**.

No Question Primitive YAML, registry entry, canonical primitive ID, or production runtime code was created or modified.

## 1. Executive Summary & Computational Reframing

*Spy the Lie* contributes a highly procedural model of interviewing in which the question is treated as a **stimulus** and the response as evidence to be evaluated in context. The book's core architecture is an interaction loop: establish a systematic baseline of the situation, ask a clear question, observe the response in L-squared mode (“look and listen”), assess the response against the stimulus, and select the next question or maneuver accordingly.

The book is specifically concerned with deception detection, so much of its language and examples are adversarial. CAE should not import the deception-detection claim wholesale. The more general and transferable contribution is the book's treatment of questioning as **controlled information acquisition**.

Seven mechanisms are particularly important.

1. **Narrative-to-fact conversion.** Open-ended questions are used to establish a narrative foundation; the interviewer then reaches inside that narrative and tests an important claim with a focused closed-ended question (pp. 117–120). The book explicitly rejects the idea that open-ended questions are inherently superior.
2. **Stimulus clarity.** Questions should be short, simple, singular in meaning, and straightforward. Ambiguous or compound questions make it difficult to know what the respondent is reacting to and can create behavior that reflects confusion rather than the underlying issue (pp. 112–113, 119).
3. **Presumptive questioning.** After sufficient context or buy-in, the interviewer asks a question that presumes a relevant fact and requests particulars. In the source's examples, this can move the respondent from a denial strategy toward information disclosure (pp. 32, 116–118, 123–129).
4. **Bait / possibility questioning.** Hypothetical or possibility formulations are used to make the respondent consider a scenario without directly asserting it as fact. The source describes this as triggering “mind virus” or “viral thinking” and emphasizes that broader, implicit formulations can create more processing than explicit accusations (pp. 111–114, 127).
5. **Entrenchment avoidance.** Repeating a disputed question after a denial can cause the respondent to become psychologically committed to the previous answer. The recommended alternative is to change the question's angle, broaden the focus, or use a prologue or possibility formulation (pp. 123–129).
6. **Qualifier-to-question targeting.** Exclusion qualifiers such as “not really,” “for the most part,” or “basically” are treated as possible signs that information has been carved out. The next question should target the omitted region rather than challenge the qualifier itself (pp. 125–126).
7. **Catch-all and “what else?” expansion.** The book repeatedly uses broad follow-up operations to expose omissions and expand beyond the respondent's initial thesis. After multiple disclosures, it recommends exploring information in reverse order because the latest item may be the most reluctant or consequential disclosure (pp. 115, 120–121, 128–129).

The computational reframing is:

`question stimulus → response observation → evidence/state update → targeted follow-up`

The transferable contribution is therefore the relationship between a question and the answer-state it creates, not a universal deception cue.

## 2. Candidate Question Mechanisms

### M1 — Narrative-to-Fact Pivot
**Source:** pp. 117–120.  
**Mechanism:** Use an open-ended question to establish the narrative, identify a consequential claim inside it, then test that claim with a focused closed-ended question.  
**Sequence:** narrative → important claim → precise probe → factual/corroborable answer → next probe.  
**Preconditions/failures:** requires a usable narrative and disciplined claim selection; premature narrowing can distort the story.  
**Answer transformation:** broad account → atomic proposition → testable detail.  
**CAE relevance:** very high.  
**Uncertainty:** CAE transfer is an auditor application, not a source claim.

### M2 — Stimulus-Specific Question Design
**Source:** pp. 112–113, 119–120.  
**Mechanism:** Because the question is the stimulus producing the response, keep it short, simple, singular in meaning, and straightforward.  
**Sequence:** define target → formulate one clear stimulus → ask → interpret response against that stimulus.  
**Preconditions/failures:** a defined target is required; oversimplification can remove needed context.  
**Answer transformation:** ambiguous response stimulus → interpretable response.  
**CAE relevance:** foundational architectural rule.

### M3 — Presumptive Detail Pivot
**Source:** pp. 32, 116–118, 123–129.  
**Mechanism:** After sufficient context, ask as though a relevant proposition is understood and request particulars.  
**Sequence:** context/buy-in → detail presumption → particulars/correction → verification or broadening.  
**Preconditions/failures:** premise must have a defensible basis; premature presumption can contaminate answers.  
**Answer transformation:** proposition/denial → concrete details or correction.  
**CAE relevance:** high, with transparent and non-coercive use.

### M4 — Qualifier-Targeted Follow-Up
**Source:** pp. 125–126.  
**Mechanism:** Treat exclusion qualifiers such as “not really” or “for the most part” as possible scope boundaries and ask neutrally about the excluded region.  
**Sequence:** qualifier → possible boundary → targeted follow-up → exception/nuance → revised scope.  
**Preconditions/failures:** a qualifier may be ordinary speech; it is a routing signal, not proof of deception.  
**Answer transformation:** qualified claim → precise boundary condition.  
**CAE relevance:** very high.

### M5 — Contradiction-Repair Follow-Up
**Source:** pp. 125–126.  
**Mechanism:** When a later statement differs from an earlier one, ask for reconciliation rather than bluntly accusing the respondent of contradiction.  
**Sequence:** discrepancy → neutral confirmation/reconciliation → reason for change or corrected account → preserved discrepancy + stronger chronology.  
**Preconditions/failures:** both statements must be captured accurately; excessive softness can leave the discrepancy unresolved.  
**Answer transformation:** conflicting versions → explanation, correction, or chronology.  
**CAE relevance:** exceptionally high.

### M6 — Lateral Broadening / Reverse-Order Exploration
**Source:** pp. 128–129; related “What else?” material pp. 115–121.  
**Mechanism:** Resist drilling immediately into a narrow thesis; broaden the information field, collect related material, then revisit the latest/highest-value disclosure.  
**Sequence:** narrow thesis → broaden → adjacent episodes/details → prioritize → deepen/verify.  
**Preconditions/failures:** related information must exist; indiscriminate broadening can reduce coherence.  
**Answer transformation:** isolated claim → pattern/expanded narrative.  
**CAE relevance:** high.

### M7 — Catch-All Omission Check
**Source:** pp. 118, 120–121.  
**Mechanism:** At the end of a topic or interview, ask what has not been discussed but matters.  
**Sequence:** apparent completion → omission audit → new material → decide whether to pursue.  
**Preconditions/failures:** broad closure is useful only if the interviewer can recognize and route genuinely new material.  
**Answer transformation:** apparent completeness → uncovered information.  
**CAE relevance:** high, though “omission” must not be equated with lying.

## 3. First-Principle Truths

### Principle 1 — A question is a stimulus, so its design controls the interpretability of the response.

**Author-grounded claim:** The book explicitly argues that the behavior being analyzed is the direct result of the stimulus and therefore the question must be clear, short, simple, singular, and straightforward (pp. 112–113).

**Auditor synthesis:** A Question Intelligence system should score questions partly by whether the resulting answer can be attributed cleanly to one informational target.

### Principle 2 — Question type should be selected for the information state, not by a universal hierarchy.

**Author-grounded claim:** The book rejects the blanket preference for open-ended questions and shows open-ended questions as narrative foundations, closed-ended questions as factual probes, opinion questions as attitude probes, and catch-alls as omission checks (pp. 117–120).

**Auditor synthesis:** Question type is a **routing decision** determined by the current information need.

### Principle 3 — Follow-up quality is often more consequential than the initial question.

**Author-grounded claim:** The book repeatedly emphasizes follow-up: clarification, qualifier targeting, contradiction repair, bait/possibility, broadening, and “What else?” (pp. 115–129).

**Auditor synthesis:** The primitive unit for CAE should not be “question” alone. It should be **question + answer-state → next operation**.

## 4. MCDA — 0 to 200

| Mechanism | Determinism /40 | Evidence /40 | Cognitive /40 | Adaptability /30 | CAE /30 | Cliché Resistance /20 | Total |
|---|---:|---:|---:|---:|---:|---:|---:|
| M1 Narrative-to-Fact Pivot | 38 | 38 | 37 | 29 | 30 | 18 | **190** |
| M2 Stimulus-Specific Question Design | 39 | 37 | 34 | 29 | 30 | 18 | **187** |
| M3 Presumptive Detail Pivot | 35 | 37 | 35 | 27 | 26 | 18 | **178** |
| M4 Qualifier-Targeted Follow-Up | 36 | 37 | 38 | 30 | 30 | 19 | **190** |
| M5 Contradiction-Repair Follow-Up | 37 | 38 | 39 | 30 | 30 | 19 | **193** |
| M6 Lateral Broadening / Reverse-Order Exploration | 35 | 36 | 38 | 29 | 29 | 18 | **185** |
| M7 Catch-All Omission Check | 34 | 36 | 34 | 29 | 30 | 16 | **179** |

**Rationale:** M1/M5 score highest because they have explicit triggers, repeatable sequences, and strong answer transformations. M2 is nearly as high because it improves interpretability across the whole system. M4 is strong because a specific linguistic cue routes a specific follow-up. M6 provides breadth and pattern yield but requires judgment. M3 is powerful but premise-sensitive. M7 is broadly useful but less distinctive.

## 5. Pareto / 80-20 Analysis

The highest-leverage cluster is **M1, M2, M5, M6, and M7**.

M1 gives CAE a reliable way to convert a compelling narrative into testable information without sacrificing the guest's story. M2 improves the signal quality of every downstream response. M5 turns qualifiers into routing information. M6 makes contradictions productive rather than adversarial. M7 prevents the interviewer from becoming trapped inside the respondent's first narrow thesis.

M8 is a useful supporting operator but is less distinctive. M3 is powerful but should have stronger preconditions than the source sometimes implies. M4 deserves study, but its psychological “bait” framing should not be promoted into CAE as a manipulation primitive.

The important architectural finding is that **M2 is not merely another candidate mechanism**. It is a constraint on the entire system. If CAE asks compound, vague, or ambiguous questions, later answer analysis becomes less reliable because the system cannot cleanly attribute the response to a single stimulus.

## 6. Answer Transformation Analysis

### M1 — Narrative-to-Fact Pivot
`broad narrative → identify consequential claim → focused factual probe → atomic claim / correction → corroboration target`

### M2 — Stimulus-Specific Question Design
`ambiguous multi-target question → singular clear stimulus → interpretable response → cleaner state/evidence update → better next question`

### M3 — Presumptive Detail Pivot
`high-level premise / partial buy-in → detail-presuming question → particulars, correction, or expanded narrative → usable evidence and chronology`

### M4 — Bait / Possibility Probe
`direct-question resistance → hypothetical/possibility frame → scenario-specific response or correction → candidate avenue for exploration`

### M5 — Qualifier-Targeted Follow-Up
`qualified claim → detect boundary marker → ask about excluded region → exception / nuance revealed → scope of claim becomes more precise`

### M6 — Contradiction-Repair Follow-Up
`statement A → later statement B differs → reconciliation question → reason for change / corrected value / chronology → stronger narrative model`

### M7 — Lateral Broadening / Reverse-Order Exploration
`narrow thesis → broaden information field → additional episodes/details → identify highest-value late disclosure → revisit strategically`

### M8 — Catch-All Omission Check
`apparently complete topic → omission audit → previously unmentioned material → decide whether new material changes the interview model`

## 7. Four CAE Case Studies

### Case 1 — Founder and a failed launch
**Context:** The founder says the failure was purely market-driven.  
**Operation:** M1; let the story unfold, then test a consequential forecast or warning with a precise factual probe.  
**Expected response:** concrete forecast/date/decision evidence.  
**Downstream use:** distinguishes retrospective narrative from what was known at the time.  
**Status:** CAE application hypothesis.

### Case 2 — Executive and “mostly positive” consultation
**Context:** Consultation is described as “for the most part positive.”  
**Operation:** M4; ask what part was least positive rather than challenging the qualifier.  
**Expected response:** specific objection, meeting, stakeholder, or decision.  
**Downstream use:** converts corporate generality into a boundary condition.  
**Status:** CAE application hypothesis.

### Case 3 — Scientist with changing sample numbers
**Context:** The scientist says 500 participants early and 420 later.  
**Operation:** M5; ask how the account moved from 500 to 420.  
**Expected response:** recruitment-versus-analysis distinction, exclusion criterion, or correction.  
**Downstream use:** accurate chronology and methodological explanation.  
**Status:** CAE application hypothesis.

### Case 4 — CEO describing an “isolated” complaint
**Context:** One customer incident is presented as exceptional.  
**Operation:** M6; broaden to other similar incidents, then return to the most consequential example.  
**Expected response:** additional episodes or a pattern.  
**Downstream use:** distinguish anomaly from recurring organizational issue.  
**Status:** CAE application hypothesis.

## 8. SWOT Analysis

**Strengths**
- Extremely procedural approach to question construction and follow-up.
- Strong distinction among question types based on information purpose.
- Treats the response as a stimulus-linked event rather than a free-floating behavior.
- Provides useful failure boundaries for compound, vague, negative, and repeated questions.
- Particularly strong on contradiction repair, qualifier targeting, and narrative-to-fact transitions.

**Weaknesses**
- The book's principal objective is deception detection, which can distort an otherwise transferable interviewing framework toward suspicion.
- Some psychological constructs, especially “mind virus” and deception-linked behavioral interpretations, should not be treated as established CAE facts.
- Several tactics depend on interviewer judgment and disciplined observation.
- The examples are frequently law-enforcement or investigative rather than consensual long-form interviewing.

**Opportunities**
- Build CAE follow-up routing around answer states such as qualifier, contradiction, omission, narrow thesis, and new factual claim.
- Use question clarity as a system-level quality gate.
- Separate narrative collection from fact testing.
- Add explicit contradiction-repair and scope-boundary operations to interview orchestration.
- Treat “what else?” and catch-all operations as completeness checks rather than suspicion triggers.

**Threats**
- Formulaic use of bait or presumptive questions can feel manipulative.
- Treating behavioral changes as evidence of lying can produce confirmation bias.
- Repeated probing can damage trust and reduce disclosure quality.
- A system optimized to “catch” people may become less useful for learning from them.

## 9. Taxonomy & Orthogonal-Dimension Review

### Retained dimensions

**Information target.** The book strongly supports distinctions among narrative, factual detail, opinion, omission, contradiction, and scope.

**Cognitive/narrative function.** Narrative generation, factual testing, possibility exploration, clarification, and expansion are meaningfully different operations.

**Answer transformation.** The source is unusually compatible with representing the expected transformation from one answer state to another.

**Context sensitivity.** The same question type changes value depending on whether the interviewer is gathering a foundation, testing a detail, resolving a contradiction, or closing a topic.

### Refinements

1. **Question Type should be separated from Question Sequence Role.** “Closed-ended” describes a surface form; “narrative-to-fact pivot” describes an operational role. These should not be collapsed.
2. **Answer-State Trigger should be explicit.** Qualifier, contradiction, nonanswer, narrow thesis, new disclosure, and apparent completion are all triggers for different next moves.
3. **Stimulus Interpretability should be a quality dimension.** A question can be well-intentioned yet analytically weak if the respondent cannot tell what is being asked.
4. **Scope Direction should be represented.** A follow-up can move vertically into more detail or laterally toward related episodes.

### New dimension discovered — Response-Contingent Routing

**Evidence:** The book repeatedly prescribes the next question from the structure of the previous answer: a qualifier triggers a targeted question; an inconsistency triggers reconciliation; a narrow thesis triggers broadening; a narrative claim triggers a factual probe; “I don't remember” can trigger possibility exploration (pp. 119–129).

**Collision with current taxonomy:** A taxonomy organized only by question intent cannot represent why the same question is appropriate in one conversational state and inappropriate in another.

**Proposed distinction:** Add `answer_state_trigger → next_operation` as an orthogonal dimension.

**Operational value:** This allows CAE to generate questions dynamically without reducing the system to a bag of question templates.

### Distinction to remove or demote

**“Lie-detection cue” should not be a primary Question Intelligence dimension.** The book itself warns against global behavioral myths, baselining, eye contact, closed posture, generalized nervousness, blushing/twitching, and similar cues when their cause is unknown (pp. 130–136). These may be contextual observations, but they should not define question selection as deterministic truth signals.

### Unresolved questions

- How much of the book's effectiveness comes from question design versus interviewer authority or context?
- What evidence supports the claimed effects of bait/mind-virus questions outside adversarial interviews?
- How should CAE distinguish useful presumption from accidental answer contamination?
- Can response-contingent routing be formalized without overfitting to a small set of answer categories?

## 10. Cross-Book Clustering Hooks

**With *Get the Truth*:** strong overlap in presumptive questioning, broadening, and nonconfrontational follow-up. The likely merge zone is presumptive detail collection; this book's stronger distinctiveness is its explicit question-type and answer-routing framework.

**With *Find Out Anything From Anyone, Anytime*:** overlap around information extraction and strategic follow-up; this source more clearly formalizes the narrative-to-fact pivot.

**With *Talk to Me*, *The Art of the Interview*, and *InterViews*:** overlap in open-ended inquiry and clarification. The differentiator is the explicit rule that open-ended questions can be foundations for later precision probes.

**With *Crucial Conversations*:** overlap in preserving cooperation and avoiding defensiveness; this book supplies more granular follow-up routing.

**With *Influence*:** direct source connection through legitimacy statements (p. 125); CAE should separate ethical context-setting from persuasion designed to bypass deliberation.

**With *Thinking, Fast and Slow*:** conceptual overlap in bias, expectation, and the danger of intuitive behavioral myths. The shared architectural lesson is disciplined interpretation rather than intuition alone.

## 11. Candidate Promotion Recommendations

| Mechanism | Recommendation | Reason |
|---|---|---|
| M1 Narrative-to-Fact Pivot | `PROMOTION_CANDIDATE` | Clear, highly repeatable, strongly supported, and broadly useful beyond deception detection. |
| M2 Stimulus-Specific Question Design | `PROMOTION_CANDIDATE` | Architectural rule with direct effect on answer interpretability; suitable as a quality constraint. |
| M3 Presumptive Detail Pivot | `MERGE_CANDIDATE` | Strong mechanism, but substantial overlap with *Get the Truth*; compare cross-book evidence before creating anything canonical. |
| M4 Bait / Possibility Probe | `RESEARCH_MORE` | Distinctive but psychologically and ethically sensitive; transfer evidence is weaker than the structural evidence. |
| M5 Qualifier-Targeted Follow-Up | `PROMOTION_CANDIDATE` | Precise trigger and precise follow-up transformation; highly transferable to CAE. |
| M6 Contradiction-Repair Follow-Up | `PROMOTION_CANDIDATE` | Excellent CAE fit and especially useful because contradiction does not have to imply deception. |
| M7 Lateral Broadening / Reverse-Order Exploration | `PROMOTION_CANDIDATE` | Strong narrative leverage and distinct information-topology function. |
| M8 Catch-All Omission Check | `RESEARCH_MORE` | Useful but generic; determine whether its omission-audit framing adds enough distinctiveness over existing closure questions. |

No canonical primitive IDs are assigned.

## 12. Source Integrity / Evidence Boundary

1. The original PDF is absent. Source Pages 1–2 are empty in the Markdown and therefore cannot be visually verified.
2. The conversion manifest records 222 pages, 220 nonempty extractions, and empty pages 1–2.
3. The complete available Markdown from Source Page 3 through 222 was read, including substantive chapters and appendices.
4. The book's claims about deception-detection effectiveness are practitioner claims, not independently validated findings established by this audit.
5. The caution chapter itself warns against treating eye contact, posture, generalized nervousness, preemptive responses, blushing/twitching, clenched hands, and demographic baselines as deterministic deception indicators (pp. 130–136).
6. “Mind virus” and related terminology are source constructs; CAE should not encode them as universal psychological laws.
7. All CAE cases and transfer claims in this audit are auditor applications.
8. Presumptive/bait operations require special care because an unsupported premise can contaminate an answer. CAE should reject fabricated evidence, coercion, and adversarial “gotcha” tactics.

## 13. Audit Conclusion

*Spy the Lie* materially adds a **response-contingent question-routing architecture** to CAE Question Intelligence.

Its deepest contribution is not “how to spot a liar.” It is the operational discipline of asking a question that produces an interpretable answer, reading the answer as a structured state, and selecting the next operation accordingly. The strongest transferable mechanisms are the narrative-to-fact pivot, stimulus-specific question design, qualifier targeting, contradiction repair, and lateral broadening.

The book also exposes an important architectural distinction: **surface question form is not the same as operational role**. An open-ended question can be a narrative foundation; a closed-ended question can be a precision instrument; a presumptive question can be a detail collector; a catch-all can be an omission audit. Therefore CAE should not build its Question Intelligence taxonomy around “open vs. closed” or similar grammatical categories alone.

The next-stage work should be cross-book comparison, especially against *Get the Truth* and the other interviewing sources. The likely highest-value convergence is a generic **answer-state → next-question routing layer**, with book-specific tactics retained as evidence-backed variants. Before primitive promotion, the system should also test whether each candidate is sufficiently distinct, ethically safe, and robust outside deception-detection settings.

**Completion record**

- **Assigned audit:** Question Heritage Audit 03
- **Exact source:** `books_markdown/Spy_the_Lie_-_Philip_Houston.md`
- **Source read:** complete available Markdown, Source Pages 1–222
- **Conversion manifest:** `Spy_the_Lie_-_Philip_Houston.md.conversion.json`
- **Output:** `AUDIT_03_Spy_the_Lie.md`
- **Word count:** approximately 3,700 words
- **Unresolved evidence issue:** original PDF absent; Source Pages 1–2 are empty in the Markdown conversion and cannot be visually verified
- **Primitive registry:** unchanged
- **Runtime:** unchanged
- **Operator gate:** ready for `ACCEPT` / `RETURN_FOR_REVIEW` / `SOURCE_FAILURE`
