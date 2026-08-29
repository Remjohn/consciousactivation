# Question Heritage Audit 09 — *Influence: The Psychology of Persuasion*

**Author:** Robert B. Cialdini, Ph.D.  
**Replacement source:** uploaded `Influence.md` (full Markdown replacement for the abbreviated book file in the ZIP)  
**Source basis:** complete available Markdown, Source Pages 1–279  
**Audit status:** `COMPLETE — MARKDOWN BASIS`  
**Source verification:** `VERIFIED FROM REPLACEMENT MARKDOWN`

## 0. Source Verification & Reading Record

This audit uses the newly supplied full `Influence.md` as the authoritative working source, exactly as instructed. The file contains the full book text, not the previously abbreviated summary. The Markdown begins with a conversion notice stating that the original PDF remains authoritative. Source Pages 1–279 are represented, with explicit empty-extraction markers on **Pages 1, 2, 6, 214, 234, 250, 274, and 276**.

Because the original PDF is not included in the bundle, those eight pages cannot be manually verified. They are therefore recorded as evidence limitations rather than reconstructed from neighboring text. The substantive book content surrounding the gaps is available in the Markdown, including Chapters 1–7, Reader's Reports, notes, bibliography, and index material.

This is a **Markdown-complete audit with eight unverified source-page extractions**. All page references below use the replacement Markdown's `Source Page` markers.

The source is about **influence and compliance**, not interviewing. The audit separates transferable question-context mechanisms from persuasion tactics.

No Question Primitive YAML, canonical `PRM-QST-*` ID, registry entry, or production runtime code was modified.

## 1. Executive Summary & Computational Reframing

*Influence* contributes a different layer to Question Intelligence than the preceding interview books. Its core concern is not “what question should I ask?” but **how context, wording, sequencing, social cues, and perceived reasons can change the recipient's response to a request**.

For CAE, the most useful transfer is therefore not to encode persuasion tactics as “question tricks.” Instead, the book suggests that a question is a **social stimulus embedded in a choice architecture**. The same semantic request can produce different responses depending on what precedes it, the explanation attached to it, the perceived legitimacy of the source, the respondent's prior commitments, and the respondent's perception of alternatives.

The strongest candidate mechanisms are:

1. **Reason-giving / because framing.** Cialdini recounts Langer's copying-machine experiment in which a request accompanied by “because” produced substantially higher compliance, even when the following reason added little new information (pp. 13–14). For CAE, the transferable insight is that respondents often need a comprehensible reason for why a question is being asked.
2. **Reciprocal exchange framing.** The reciprocity chapter shows that receiving something can create a perceived obligation to give something in return (pp. 23–35). In interviewing, this should be transformed into **transparent mutual contribution**—for example, explaining that the interviewer will share context or findings—rather than engineered indebtedness.
3. **Reciprocal-concession sequencing.** The rejection-then-retreat technique creates compliance by making the second request look like a concession from the first (pp. 36–51). As a CAE mechanism, its ethical value is limited, but its structural lesson about perceived movement and negotiation sequencing is relevant.
4. **Commitment-consistency anchoring.** Once people take a position, subsequent behavior is influenced by the desire to act consistently with that prior commitment (pp. 53–89). A safe interview application is to ask respondents to clarify or refine their own earlier statement rather than strategically corner them with it.
5. **Self-generated commitment.** Written or public commitments are described as stronger because the individual sees the commitment as their own (pp. 68–80). In CAE, this points toward asking respondents to articulate their own standards, decision criteria, or definitions before evaluating a concrete case.
6. **Social-proof calibration.** When people are uncertain, they look to others' behavior as evidence of what is appropriate (pp. 126–156). The CAE-safe application is to use social context as a topic for inquiry, not as hidden pressure: “What were others doing?” can reveal the respondent's decision environment.
7. **Liking / similarity / association.** The liking chapter describes similarity, familiarity, compliments, cooperation, and positive associations as factors affecting influence (pp. 157–205). The interview-relevant mechanism is not flattery, but recognizing that relational fit changes how openly a respondent engages.
8. **Authority framing.** Titles, expertise, credentials, and visible trappings can influence deference (pp. 217–230). For CAE, legitimate expertise can help establish context, but authority must not replace evidence or pressure disclosure.
9. **Scarcity and freedom restriction.** Perceived scarcity can increase value, and restrictions on freedom can increase desire to restore that freedom (pp. 237–271). The safe CAE application is primarily diagnostic: ask how deadlines, exclusivity, or constraints affected a decision rather than manufacturing urgency.


**Computational model:** `question → context → respondent interpretation → response → state update`

## 2. Candidate Question Mechanisms

### M1 — Reason-Giving Question Frame

**Source location:** pp. 13–14.

**Source-grounded description:** A request preceded by a reason or “because” can be more effective than the same request without a reason. The source cites an experiment in which even a weak or obvious “because” formulation produced increased compliance.

**Differentiating property:** It reduces ambiguity about **why the respondent is being asked to act**.

**Sequence:** state the request → give a truthful, relevant reason → ask → observe whether comprehension improves.

**CAE-safe boundary:** The reason must be genuine. The mechanism should not be implemented as a linguistic trigger for automatic compliance.

**Expected transformation:** unexplained request → understandable request → more informed willingness to answer.

**CAE relevance:** very high as a transparency rule.

### M2 — Reciprocal Context Setting

**Source location:** pp. 17–35, 48–56.

**Source-grounded description:** Reciprocity creates an expectation that a benefit or favor will be returned. The source also shows that uninvited gifts can create obligations and that such obligations can be exploited.

**Differentiating property:** It explains how perceived **exchange balance** affects response behavior.

**CAE-safe sequence:** clarify what the interview provides and what participation asks; offer genuine reciprocal value; avoid creating an artificial debt.

**Expected transformation:** one-sided extraction → transparent exchange → better understanding of participation terms.

**CAE relevance:** moderate; the ethical boundary is central.

### M3 — Concession-Sequence Questioning

**Source location:** pp. 36–51.

**Source-grounded description:** A large initial request followed by a smaller request can appear as a concession and increase agreement to the second request. Cialdini describes this as the rejection-then-retreat technique.

**Differentiating property:** It uses **relative movement between requests**, not just the content of the second request.

**CAE application boundary:** Use only as an analysis lens for negotiation dynamics. Deliberately engineering an extreme first request to manipulate a guest is not a suitable CAE primitive.

**Potential safe use:** ask respondents how priorities changed as negotiations moved from an initial position to a later compromise.

### M4 — Prior-Statement Consistency Probe

**Source location:** pp. 53–80, 92–99.

**Source-grounded description:** People experience pressure to remain consistent with choices or positions they have already taken. The source discusses written commitments, public commitments, and self-image as mechanisms strengthening consistency.

**Differentiating property:** It uses the respondent's **own previous position as the informational reference point**.

**Sequence:** capture prior statement → later ask how that position applies to a concrete case → invite refinement, exception, or change.

**CAE-safe boundary:** The interviewer should allow revision. The goal is clarification, not trapping the respondent into defending an outdated statement.

**Expected transformation:** abstract position → applied example → consistency, exception, or reason for change.

**CAE relevance:** high.

### M5 — Self-Generated Standard Question

**Source location:** pp. 68–80.

**Source-grounded description:** Commitment is strengthened when a person actively takes a position or records it as their own. The source discusses written and public commitments and the role of self-image.

**Differentiating property:** It creates a **respondent-authored evaluative standard** before discussing an instance.

**Sequence:** ask respondent to define what good practice, success, responsibility, or fairness means → later present the concrete case → ask how the standard applies.

**Expected transformation:** vague values → explicit criterion → case evaluation.

**CAE relevance:** very high, especially for leadership and decision interviews.

### M6 — Social-Context Question

**Source location:** pp. 126–156.

**Source-grounded description:** Under uncertainty, people can use others' behavior as evidence of appropriate action. The chapter discusses audience effects, uncertainty, similarity, and pluralistic ignorance.

**Differentiating property:** Instead of asking only “what did you decide?”, it asks **what social evidence surrounded the decision**.

**Sequence:** identify uncertain decision → ask what others believed/did → examine who counted as relevant evidence → ask how the respondent interpreted that signal.

**Expected transformation:** isolated decision → social decision environment → clearer explanation of influence.

**CAE relevance:** high as a contextual inquiry mechanism.

### M7 — Legitimate-Authority Context Question

**Source location:** pp. 217–230.

**Source-grounded description:** Titles, credentials, expertise, and authority symbols can produce deference. The source also notes that people can grant authority beyond legitimate expertise.

**Differentiating property:** It separates **source credibility from the content of the claim**.

**Sequence:** identify authority source → ask what made it credible → distinguish expertise, title, reputation, or appearance → examine how that credibility affected the decision.

**Expected transformation:** “we trusted the expert” → explicit basis of trust → evaluable authority claim.

**CAE relevance:** high for expert interviews and institutional decisions.

### M8 — Constraint / Scarcity Question

**Source location:** pp. 237–271.

**Source-grounded description:** Limited availability can raise perceived value; restricted freedom can produce reactance. The source discusses limited numbers, deadlines, and the effects of restricting information or choice.

**Differentiating property:** It treats **constraints as causal variables in decision narratives**.

**Sequence:** identify a scarce/limited option or constraint → ask how the limitation changed perception or urgency → separate actual resource limits from manufactured scarcity.

**Expected transformation:** decision outcome → constraint-aware explanation.

**CAE relevance:** moderate to high as a diagnostic question.

## 3. First-Principle Truths

### Principle 1 — Questions operate inside social context.

The book's central claim is that decisions are influenced by principles surrounding the request, not only by its literal content.

**CAE synthesis:** Store relevant context variables—reason, prior commitment, social reference, authority source, perceived scarcity—alongside the question itself.

### Principle 2 — Contextual influence can affect willingness independently of information quality.

The same question can receive different responses because the respondent interprets the interaction differently.

**CAE synthesis:** Answer quality should never be inferred directly from compliance or enthusiasm.

### Principle 3 — Self-authored standards are safer than interviewer-imposed standards.

The commitment chapter suggests that people organize later decisions partly around commitments they recognize as their own.

**CAE synthesis:** Asking respondents to define their own criteria can yield clearer evaluative answers without imposing the interviewer’s judgment.

### Principle 4 — Influence mechanisms must be separated from manipulation mechanisms.

The source explicitly describes how the same principles can be used honestly or exploitatively.

**CAE synthesis:** Ethical Question Intelligence should retain the descriptive mechanism while rejecting covert optimization for compliance.

## 4. MCDA — 0 to 200

| Mechanism | Determinism /40 | Evidence /40 | Cognitive-Narrative /40 | Adaptability /30 | CAE Fit /30 | Cliché Resistance /20 | Total |
|---|---:|---:|---:|---:|---:|---:|---:|
| M1 Reason-Giving Question Frame | 36 | 38 | 34 | 29 | 30 | 18 | **185** |
| M2 Reciprocal Context Setting | 29 | 37 | 34 | 25 | 23 | 17 | **165** |
| M3 Concession-Sequence Questioning | 31 | 38 | 33 | 25 | 17 | 18 | **162** |
| M4 Prior-Statement Consistency Probe | 36 | 38 | 37 | 29 | 29 | 19 | **188** |
| M5 Self-Generated Standard Question | 35 | 38 | 39 | 30 | 30 | 19 | **191** |
| M6 Social-Context Question | 34 | 37 | 39 | 30 | 30 | 19 | **189** |
| M7 Legitimate-Authority Context Question | 34 | 37 | 38 | 29 | 30 | 19 | **187** |
| M8 Constraint / Scarcity Question | 32 | 36 | 37 | 28 | 28 | 19 | **180** |


## 5. Pareto / 80-20 Analysis

The strongest 80/20 cluster is **M1, M4, M5, M6, and M7**.

M1 improves transparency around the question itself. M4 makes the respondent's own prior statements usable as clarification anchors. M5 elicits explicit criteria before testing decisions. M6 reconstructs the social evidence surrounding uncertain choices. M7 makes authority claims examinable instead of treating expertise as a black box.

Together they give CAE a useful **context-of-decision layer**:

`question → reason → prior commitment → respondent criterion → social evidence → authority source → answer`

This is more valuable than importing compliance tactics directly.

M2 and M3 should remain analytical lenses rather than default question-generation rules. M8 should activate when deadlines, access limits, exclusivity, resource constraints, or reactance are actually part of the story.

## 6. Answer Transformation Analysis

### M1 — Reason-Giving Question Frame
`opaque request → truthful rationale → informed response → better participation and answer framing`

### M2 — Reciprocal Context Setting
`perceived extraction → transparent exchange context → clearer willingness/boundary → more legitimate participation`

### M3 — Concession-Sequence Questioning
`initial position → apparent movement/concession → revised request → explanation of negotiation dynamics`

### M4 — Prior-Statement Consistency Probe
`earlier position → concrete application → consistency / exception / revision → richer account of change`

### M5 — Self-Generated Standard Question
`implicit value → respondent-authored standard → concrete case → explicit evaluation`

### M6 — Social-Context Question
`isolated decision → relevant others and social signals → uncertainty/context reconstructed → better explanation`

### M7 — Legitimate-Authority Context Question
`authority claim → source of credibility → expertise/title/reputation separated → evidence-based trust assessment`

### M8 — Constraint / Scarcity Question
`decision outcome → actual constraint / perceived scarcity → causal effect on urgency/value → fuller decision model`

## 7. Four CAE Case Studies

### Case 1 — CEO explains a difficult strategic decision

**Context:** The CEO says, “It was obvious we had to do it.”

**Operation:** M7 Legitimate-Authority Context Question plus M6 Social-Context Question. Ask what made the conclusion obvious, who was regarded as authoritative, and what evidence others were using.

**Expected transformation:** unquestioned certainty → authority/source map + social evidence → reconstructable decision logic.

### Case 2 — Founder describes organizational standards

**Context:** A founder says accountability was “one of our core values,” but gives no concrete definition.

**Operation:** M5 Self-Generated Standard. Ask the founder to define what accountability meant in practice before introducing a specific failure episode.

**Expected transformation:** value statement → respondent-authored standard → application to real event.

### Case 3 — Executive reverses an earlier position

**Context:** Early in the interview the executive says layoffs were a last resort; later they say layoffs became the preferred route quickly.

**Operation:** M4 Prior-Statement Consistency Probe. Return to the earlier statement neutrally and ask what changed.

**Expected transformation:** apparent inconsistency → explicit change in assumptions, evidence, constraints, or priorities.

### Case 4 — Negotiator describes an urgent “limited window”

**Context:** A deal was accepted shortly before an advertised deadline.

**Operation:** M8 Constraint / Scarcity Question. Ask whether the deadline reflected a real operational constraint, a counterpart's strategy, or the negotiator's perception.

**Expected transformation:** deadline as background fact → causal account of urgency and perceived alternatives.

## 8. SWOT Analysis

**Strengths**
- Strong experimental/practitioner evidence base compared with many persuasion books.
- Clearly identifies repeatable psychological principles behind changes in response.
- Provides examples across commerce, politics, relationships, organizations, and everyday life.
- Useful for understanding how question context changes perceived choice.
- Strong distinction between prior commitment, social proof, authority, liking, reciprocity, and scarcity.

**Weaknesses**
- Primary objective is persuasion/compliance, not information discovery.
- Several tactics intentionally exploit automatic behavior.
- “Automatic influence” is not the same thing as better interviewing.
- Some effects depend heavily on context and the respondent's interpretation of the situation.
- It is not a complete interviewing framework.

**Opportunities**
- Add a `context_features` layer to Question Intelligence.
- Require truthful rationale for sensitive questions.
- Ask respondents to articulate their own standards and decision criteria.
- Reconstruct social and authority context around important decisions.
- Use prior commitments as clarification anchors while preserving the right to revise.

**Threats**
- Covert compliance optimization could violate CAE's truth-seeking purpose.
- Reciprocity can become artificial indebtedness.
- Authority cues can suppress critical evaluation.
- Scarcity framing can create urgency that contaminates deliberation.
- Consistency pressure can discourage legitimate revision.

## 9. Taxonomy & Orthogonal-Dimension Review

### Retain

**Context sensitivity** should remain distinct from question content. This book strongly supports the idea that the surrounding interaction changes response behavior.

**Prior-state dependency** should remain explicit. A prior commitment, concession, or social signal can change the meaning of a later question.

**Evidence-source type** should distinguish direct evidence, social evidence, authority evidence, and contextual constraints.

### New dimension — Influence Context

A useful orthogonal dimension is:

`reason / reciprocity / commitment / social proof / liking / authority / scarcity / reactance`

This should be **descriptive and diagnostic**, not a manipulation score.

### New dimension — Decision Environment

Several chapters suggest that the respondent's answer cannot be understood without the surrounding environment:

- who else was present,
- what authorities were trusted,
- what choices appeared available,
- what alternatives had already been rejected,
- what constraints were salient.

This can improve narrative reconstruction without using influence tactics.

### Refinement — Commitment State

Commitment should not be binary. The source suggests distinctions among:
- private thought,
- choice,
- written commitment,
- public commitment,
- action consistent with commitment.

CAE can use this as a question-routing dimension when exploring why a person did or did not follow through.

### Demote

**Automatic compliance strength** should not become a primary Question Intelligence objective. A question that makes a respondent more likely to say “yes” is not necessarily a better question.

Likewise, **psychological trigger optimization** should be excluded from canonical CAE primitives unless independently justified by the project's ethical and epistemic requirements.

## 10. Cross-Book Clustering Hooks

**With *Get the Truth*:** strong overlap around framing, commitment, rationalization, and state-dependent questioning. *Influence* supplies a broader social-psychology explanation for why context can change response behavior.

**With *Spy the Lie*:** overlap around stimulus design and the importance of how a question is presented. The key distinction is that *Influence* studies compliance, while *Spy the Lie* applies stimulus-response logic to investigative interviewing.

**With *Find Out Anything From Anyone, Anytime*:** overlap around question purpose and context, but *Influence* contributes the social conditions surrounding response rather than a discovery taxonomy.

**With *InterViews*:** important bridge via the idea that the interaction itself affects the answer. Self-generated standards and respondent-authored interpretations are particularly compatible with qualitative interviewing.

**With *Crucial Conversations*:** strong overlap around social context, perceived safety, commitment, and the risks of using influence under high stakes. Cross-book deduplication should distinguish ethical dialogue support from compliance engineering.

**With *Thinking, Fast and Slow*:** direct conceptual hook around heuristics, shortcuts, and situations in which contextual cues alter judgment.

**With *A More Beautiful Question*:** the common ground is using questions to uncover assumptions; *Influence* adds mechanisms explaining why the surrounding choice environment matters.

## 11. Candidate Promotion Recommendations

| Mechanism | Recommendation | Reason |
|---|---|---|
| M1 Reason-Giving Question Frame | `PROMOTION_CANDIDATE` | Strong evidence and excellent CAE safety when the reason is genuine and transparent. |
| M2 Reciprocal Context Setting | `RESEARCH_MORE` | Useful ethically as transparency, but too close to compliance manipulation in its source form. |
| M3 Concession-Sequence Questioning | `RESEARCH_MORE` | Strong source support but poor fit as a default interview operator; better as a negotiation-analysis lens. |
| M4 Prior-Statement Consistency Probe | `PROMOTION_CANDIDATE` | High information yield when framed as clarification rather than entrapment. |
| M5 Self-Generated Standard Question | `PROMOTION_CANDIDATE` | Strong CAE fit; generates respondent-authored evaluation criteria. |
| M6 Social-Context Question | `PROMOTION_CANDIDATE` | Adds decision-environment intelligence and is broadly transferable. |
| M7 Legitimate-Authority Context Question | `PROMOTION_CANDIDATE` | Useful for separating expertise from authority effects and reconstructing trust. |
| M8 Constraint / Scarcity Question | `MERGE_CANDIDATE` | Likely best merged into a broader decision-context / constraint mechanism. |

No canonical primitive IDs are assigned pending cross-book deduplication.

## 12. Source Integrity / Evidence Boundary

1. The replacement `Influence.md` is the full Markdown source supplied for this audit; it materially supersedes the abbreviated summary source.
2. Empty extraction pages are **1, 2, 6, 214, 234, 250, 274, and 276**. Without the original PDF, those pages cannot be manually verified.
3. The audit uses only the available Markdown text and does not reconstruct missing-page content from outside sources.
4. The evidence supports influence/compliance contexts; it does not by itself establish that these techniques improve truthful interviewing.
5. Reciprocity, concession sequencing, authority, and scarcity can be manipulative when engineered. CAE should treat their presence as contextual variables or subjects of inquiry, not as hidden levers.
6. The copying-machine “because” experiment is useful here as evidence that a reason attached to a request can change response behavior; CAE should use truthful rationale to improve transparency, not as a compliance trigger.
7. Commitment-consistency pressure can encourage both coherence and unhelpful stubbornness. Interviewers must explicitly permit revision.
8. Social proof can reflect useful context but can also preserve group errors or pluralistic ignorance. Asking “what did others think?” should not imply that others were right.
9. Authority effects can improve efficient trust while also producing unwarranted deference. Expertise should therefore be separated from mere status cues.
10. Scarcity and reactance mechanisms are most safely used to understand why a past decision felt urgent or constrained, not to manufacture urgency during the interview.
11. The case studies are auditor-generated applications.
12. No conclusion in this audit treats willingness to comply as evidence of truthfulness.

## 13. Audit Conclusion

*Influence* does not belong in the CAE Question Intelligence library as a collection of persuasion tricks. Its highest-value contribution is a **context layer for interpreting and designing questions**.

The strongest transferable insights are: give a genuine reason for difficult questions; use respondents' prior statements as clarification anchors while preserving their right to change; ask people to articulate their own standards before evaluating a case; reconstruct the social and authority environment surrounding important decisions; and identify how scarcity, deadlines, and constrained alternatives affected judgment.

The key boundary is epistemic: **compliance is not information quality**. A question that increases agreement may reduce reliability if obligation, authority, urgency, or consistency pressure shapes the response. CAE should model these effects so it can recognize and compensate for them, not maximize them.

Cross-book integration should place these mechanisms beneath a shared `interaction_context` or `decision_environment` layer. This audit most strongly supports promotion of reason-giving, prior-statement consistency probing, self-generated standards, social-context inquiry, and legitimate-authority context questions. Reciprocity, concession sequencing, and engineered scarcity should remain analytical or research-only mechanisms until their ethical and epistemic boundaries are independently established.

**Completion record**

- **Audit:** 09
- **Book:** *Influence: The Psychology of Persuasion*
- **Author:** Robert B. Cialdini, Ph.D.
- **Source:** full replacement `Influence.md`
- **Source read:** available Markdown, Source Pages 1–279
- **Empty extractions:** 1, 2, 6, 214, 234, 250, 274, 276
- **Output:** `AUDIT_09_Influence.md`
- **Audit length:** approximately 3,700 words
- **Primitive registry:** unchanged
- **Runtime:** unchanged
- **Canonical IDs:** none assigned
- **Operator gate:** ready for `ACCEPT` / `RETURN_FOR_REVIEW` / `SOURCE_FAILURE`
