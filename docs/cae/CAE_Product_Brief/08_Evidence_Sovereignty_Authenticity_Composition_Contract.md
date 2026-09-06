# 8. Evidence Sovereignty, Authenticity & Composition Contract

CAE's central authenticity rule is simple: **the human source of meaning remains sovereign over the meaning extracted from them**. Everything else in the composition system follows from that rule. The engine may organize, rank, retrieve, structure, connect, clarify, render, and evaluate material, but downstream intelligence is not permitted to silently replace the evidence that made the Subject authoritative in the first place.

Evidence sovereignty begins with provenance. Every meaningful content object should be traceable to an upstream source: an interview moment, evidence package, approved research source, archival material, or another explicitly permitted source class. The repository already embodies this principle in multiple places. The pipeline's knowledge projection contract requires evidence references, relationship references, expression-moment references, lifecycle state, authority state, permitted actions, and content hashes. For interview-expression sources, the validator requires both reaction receipts and expression moments, rejecting incomplete provenance rather than allowing a plausible but untraceable projection through.

The next boundary is the **composition contract**. Not every format may use language in the same way. Video dialogue is governed by a strict lane because the audience reasonably assumes that the person on screen actually said the words attributed to them. Carousels and supervisuals may have a different permitted composition structure because visual editorial framing can sometimes require bridging language around the person's evidence. Headlines and hooks can operate under an editorial lane because a headline is not necessarily presented as the Subject's spoken sentence. These differences do not weaken authenticity. They make the rules explicit.

For CAE, the principal composition lanes are therefore:

**VERBATIM_ONLY** for spoken Subject dialogue and other outputs where exact authorship is implied.

**VOICE_DNA_BRIDGED** for formats that permit limited synthetic connective tissue around approved human evidence, subject to a strict cap.

**EDITORIAL_HEADLINE** for titles, hooks, framing labels, or other editorial language that does not falsely present itself as the Subject's speech.

The purpose of this polymorphism is not to give generation more freedom. It is to prevent ambiguity. When every artifact has a declared lane, the system can ask a concrete question: what kind of language is legally and product-wise permitted here? That is safer than relying on a vague global instruction such as “stay authentic.”

The **VERBATIM_ONLY** lane is the strongest boundary. When CAE presents a Subject as saying something, the underlying words must exist in source evidence. Editing may be limited to mechanically permitted transformations that do not change semantic authorship, and every transformation should remain traceable to the source segment. A model should not fill missing words, create a more elegant sentence, merge separate statements into an apparently spoken sentence, or fabricate a transition merely because the resulting cut would be stronger. If the required statement does not exist, the production system must either find another legitimate expression moment, return to elicitation, or accept that the intended artifact cannot be produced.

The **VOICE_DNA_BRIDGED** lane exists to solve a narrower problem. Some visual formats need concise connective text, explanatory framing, or transitions that were never spoken verbatim. CAE may generate such bridges only when the product contract explicitly permits them and when the bridge remains subordinate to established evidence. The synthetic contribution is capped at **≤20%** in the defined bridged lane. The cap is not a magical measure of authenticity; it is an enforceable release constraint intended to prevent the supporting layer from overwhelming the human source material.

The bridge also has qualitative rules. It cannot invent a lived event. It cannot introduce a new personal belief, emotional confession, quotation, credential, relationship, or causal claim that lacks evidence. It cannot manufacture “voice” by simulating a Subject's identity beyond the permitted contextual role. It should connect or clarify already-supported meaning, not create the meaning itself.

The **EDITORIAL_HEADLINE** lane allows a publisher or Operator to frame a piece without confusing the frame with a Subject quotation. This distinction is particularly useful for hooks. A headline may be sharper, shorter, or more dramatic than anything said in the interview while remaining clearly editorial. The product must prevent the interface and export formats from making that editorial language look like a verbatim quote. That is an authenticity problem as much as a copywriting problem.

CAE must also enforce a strong **no generative impersonation** boundary. It should not generate audio, video dialogue, or other media that falsely represents the Subject as saying words they did not say. The existence of a high-quality model does not change the contract. The system is intended to amplify human authority, not fabricate the performance of authority. This principle is especially important because the more natural synthetic media becomes, the less reliable audience intuition becomes as a safeguard. The product therefore needs explicit provenance rather than hoping viewers will detect fabrication.

Authenticity also requires source hierarchy. A public source about a Subject may establish context, but it does not automatically authorize a claim about what the Subject believes. A previous interview may provide continuity, but it does not automatically override a current statement. Archival material may support a media reference, but its rights status must still be resolved. CAE should keep source type, authority state, lifecycle state, and evidence quality visible enough for downstream validation to make a governed decision.

The asset-intelligence layer demonstrates this principle in a related way. Its domain model explicitly separates source type, media type, editorial insert role, rights status, timestamps, source SHA-256, semantic role, and catalog membership. This allows a discovered asset to be meaningful without treating “found” as equivalent to “approved.” The asset annotator rejects generic captions, enforces insert-duration constraints, and requires license or proof evidence when an asset is marked CLEARED. Authenticity is therefore implemented as structured state, not merely editorial taste.

Composition integrity should be observable. For each artifact, CAE should be able to answer: what source evidence supports it; which composition lane was used; what synthetic contribution, if any, exists; what model produced that contribution; what human decision authorized release; and what hashes or receipts connect the parts. The runtime's lossless lineage graph is designed to support exactly this kind of tracing, from SOURCE_EVIDENCE through COMPOSITION and RENDERED_ARTIFACT to OPERATOR_APPROVAL and APPROVED_RELEASE.

This contract has an important consequence for product strategy: **CAE should prefer missing output to fake output**. A weak artifact made by inventing connective tissue can damage the very authority the system is designed to build. A declared yield shortfall is an operational problem that can be managed. Untraceable authorship is a trust problem that compounds over time.

Evidence sovereignty therefore becomes a release philosophy:

**source truth before inference; inference before composition; composition before rendering; authorization before publication.**

The contract does not make CAE less creative. It moves creativity into legitimate spaces: choosing which evidence matters, discovering collisions, ordering moments, designing narrative tension, selecting media roles, framing a claim, choosing a hook, and designing the next question. The machine can still be highly intelligent. It simply cannot use intelligence as a license to erase authorship.

The result is a system in which authenticity is neither a branding slogan nor a manual proofreading habit. It is a technical property of the pipeline. CAE knows what is evidence, what is inference, what is composition, what is editorial framing, what is synthetic, and what has been approved. That is what allows a product built around generative intelligence to remain grounded in the human source that gives it something worth amplifying.
