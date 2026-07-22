# **CCP V9.1 — Expression Capture & Archetype Routing Update**

## **Operational Patch for Interview-First Expression Sessions**

**Document Type:** CCP System Patch  
**Project:** Conscious Coaching Platform / Conscious Media Factory / Conscious Rivers  
**Version:** V9.1  
**Status:** Implementation Doctrine  
**Purpose:** Update CCP V9 with the operational capture layer, interview asset contract standard, archetype routing logic, and Guest Asset Pack production rules.

---

# **I. Executive Summary**

CCP V9 established the shift from a Telegram-first trigger engine to an interview-first expression engine.

CCP V9.1 implements the missing operational layer.

The new doctrine is:

Every interview is a Complete Expression Session.  
Every question is an Interview Asset Contract.  
Every answer is routed through archetype schemas.  
Every asset is produced through CMF render routes.  
Every output receives an evaluation receipt.

The system no longer treats interviews as informal conversations that later become content.

Instead, CCP treats interviews as structured expression capture environments.

The human layer activates authentic speech.

The backend layer transforms that speech into assets, products, and memory.

---

# **II. What V9.1 Adds**

V9.1 adds seven implementation layers:

1. **Recording Configuration** inside the Complete Expression Session.  
2. **Remote Recording Protocol** for Google Meet \+ phone master recording.  
3. **Two-Person In-Person Recording Protocol** for vertical social-media capture.  
4. **Expression Session Quality Gate** before the interview begins.  
5. **Interview Deck as Asset Contract** standard.  
6. **Archetype Contract Registry integration** for asset routing.  
7. **Guest Asset Pack fulfillment logic** for 4 videos, 2 carousels, 2 meme visuals, 2 poll visuals, and reaction seeds.

V9 remains the strategic doctrine.

V9.1 is the production patch.

---

# **III. Updated Core Flow**

The V9.1 production flow is:

Guest / Client Invite  
↓  
Guest Dossier  
↓  
Audience Reality Brief  
↓  
Interviewer Pre-Induction  
↓  
Interview Asset Contracts  
↓  
Recording Configuration  
↓  
Complete Expression Session  
↓  
Expression Moment Extraction  
↓  
Archetype Contract Routing  
↓  
Asset Package Spec  
↓  
Complete Editing Sessions  
↓  
CMF Render Routes  
↓  
Evaluation Receipts  
↓  
Guest Asset Pack Delivery

---

# **IV. Complete Expression Session V2**

The Complete Expression Session is now the upstream source object for all interview-first content production.

It is not the same as the Complete Editing Session.

The Complete Expression Session captures the human expression event.

The Complete Editing Session renders a specific media asset.

One Complete Expression Session can produce many Complete Editing Sessions.

Complete Expression Session  
↓  
Multiple Expression Moments  
↓  
Multiple Asset Routes  
↓  
Multiple Complete Editing Sessions

---

# **V. Complete Expression Session V2 Schema**

{  
  "expression\_session\_id": "xes\_2026\_0001",  
  "guest\_id": "claude\_ntahuga",  
  "interviewer\_id": "emmanuel",  
  "session\_type": "remote\_single\_guest\_interview",  
  "session\_goal": "guest\_asset\_pack",  
  "conversation\_language": "fr",  
  "system\_label\_language": "en",  
  "recording\_configuration": {},  
  "guest\_dossier": {},  
  "audience\_reality\_brief": {},  
  "interviewer\_resonance\_context": {},  
  "matrix\_of\_edging\_brief": {},  
  "narrative\_state\_map": {},  
  "interview\_asset\_contracts": \[\],  
  "pre\_session\_quality\_gate": {},  
  "recording\_artifacts": \[\],  
  "transcript": {},  
  "timestamped\_anchor\_hits": \[\],  
  "expression\_moments": \[\],  
  "core\_archetype\_candidates": \[\],  
  "asset\_derivative\_candidates": \[\],  
  "meme\_mechanism\_candidates": \[\],  
  "reaction\_candidates": \[\],  
  "cmf\_route\_candidates": \[\],  
  "asset\_package\_spec": {},  
  "post\_session\_learning": {},  
  "evaluation\_receipt": {}  
}

---

# **VI. Recording Configuration**

Every Complete Expression Session must include a recording configuration.

This ensures the backend understands how the raw material was captured and how reliable it is for downstream production.

{  
  "recording\_configuration": {  
    "session\_mode": "remote\_single\_guest",  
    "conversation\_tool": "google\_meet",  
    "master\_recording\_source": "phone\_native\_video",  
    "backup\_recording\_source": "google\_meet\_recording",  
    "orientation": "vertical\_9\_16",  
    "framing\_mode": "single\_person\_vertical",  
    "safe\_zone\_profile": "reel\_vertical\_standard",  
    "phone\_position": "eye\_level\_stable",  
    "audio\_mode": "guest\_earbuds\_on\_laptop\_plus\_phone\_capture",  
    "lighting\_mode": "front\_soft\_light",  
    "file\_transfer\_required": true,  
    "quality\_check\_required": true  
  }  
}

---

# **VII. Recording Source Doctrine**

The standard remote recording doctrine is:

Laptop \= conversation  
Phone \= master recording  
Google Meet \= backup only

Google Meet is not the production source.

Google Meet exists so the interviewer and guest can speak naturally.

The phone recording is the master file.

The backend should assume that meeting-platform video is compressed and inferior unless explicitly configured otherwise.

---

# **VIII. Remote Single-Guest Recording Protocol**

## **Guest Setup**

The guest should:

1. Join Google Meet from a laptop.  
2. Use earphones or earbuds connected to the laptop.  
3. Place the phone on a tripod or stable support.  
4. Record vertically in 9:16.  
5. Place the phone at eye level.  
6. Frame from mid-chest to slightly above the head.  
7. Leave headroom above the head.  
8. Face a window or soft light.  
9. Avoid backlight.  
10. Clean the phone lens.  
11. Turn on Do Not Disturb.  
12. Check storage and battery.  
13. Record a 10-second test before starting.  
14. Upload the original file after the session.

## **Remote Guest Instruction**

The guest-facing explanation should remain simple:

We’ll use Google Meet only so we can talk naturally.  
Your phone recording is the high-quality video file.  
Please record yourself vertically on your phone while we speak.  
After the session, send the original video file through Drive, WeTransfer, iCloud, or another file link.  
Please avoid WhatsApp because it compresses the video.

---

# **IX. In-Person Two-Person Recording Protocol**

If recording two people with one phone for social-media clips:

## **Placement**

* Phone vertical.  
* Phone centered between both people.  
* Phone far enough back to fit both upper bodies.  
* Phone at or near eye level.  
* Both chairs angled slightly inward.  
* Both people fully inside frame.  
* Leave headroom above both heads.  
* Avoid placing one person too close to the edge.  
* Avoid placing the phone off to one side.  
* Avoid horizontal phone orientation when the goal is vertical clips.

## **Best Layout**

Guest A      small table / open space      Guest B  
     \\                                  /  
      \\                                /  
             Phone on tripod  
             centered and vertical

## **Two-Person Recording Configuration**

{  
  "session\_mode": "in\_person\_two\_person",  
  "master\_recording\_source": "phone\_native\_video",  
  "orientation": "vertical\_9\_16",  
  "framing\_mode": "two\_person\_wide\_vertical",  
  "phone\_position": "centered\_between\_subjects",  
  "chair\_angle": "slightly\_inward",  
  "safe\_zone\_profile": "two\_person\_reel\_vertical",  
  "quality\_check\_required": true  
}

---

# **X. Expression Session Quality Gate**

Before recording begins, CCP should run or manually confirm a quality gate.

## **Quality Gate Categories**

1. **Orientation**  
   * Phone is vertical.  
   * Frame is 9:16.  
   * No horizontal master file unless explicitly required.  
2. **Framing**  
   * Subject is not too low.  
   * Subject is not too far.  
   * Headroom exists.  
   * Hands/upper body are visible where possible.  
   * Face is not cut off.  
   * For two people, both are fully in frame.  
3. **Lighting**  
   * Face is visible.  
   * Light is in front or side-front.  
   * No strong backlight.  
   * No harsh overhead-only lighting.  
4. **Stability**  
   * Phone is not handheld.  
   * Tripod or stable support is used.  
   * Frame does not shake.  
5. **Audio**  
   * Guest can hear interviewer through earbuds.  
   * Room is not excessively noisy.  
   * Phone audio is acceptable as backup.  
   * Meeting audio exists as fallback.  
6. **File Safety**  
   * Battery sufficient.  
   * Storage sufficient.  
   * Do Not Disturb enabled.  
   * Original file delivery method confirmed.

## **Quality Gate Object**

{  
  "pre\_session\_quality\_gate": {  
    "orientation\_pass": true,  
    "framing\_pass": true,  
    "lighting\_pass": true,  
    "stability\_pass": true,  
    "audio\_pass": true,  
    "file\_safety\_pass": true,  
    "notes": \[\],  
    "approved\_for\_recording": true  
  }  
}

---

# **XI. Interview Deck as Asset Contract**

In V9.1, an interview deck is not a list of questions.

An interview deck is a collection of Interview Asset Contracts.

Each question must include enough structure for agents to:

* induce the right state,  
* create clean clipping starts,  
* prevent shallow answers,  
* route answers into archetypes,  
* generate asset derivatives,  
* choose CMF render modes,  
* evaluate output quality.

---

# **XII. Interview Asset Contract Schema**

{  
  "question\_id": "claude\_q01",  
  "target\_archetype": "Conceptual Contrast",  
  "asset\_derivatives": \[  
    "Identity Mirror",  
    "Quote-to-Question",  
    "Tension Poll"  
  \],  
  "target\_state": \[  
    "Authority",  
    "Vulnerability",  
    "Invitation"  
  \],  
  "edge\_product": "Forced identity vs integrated identity",  
  "cmf\_routes": \[  
    "Personal-Brand Commentary",  
    "Paper-Cut Explainer",  
    "Carousel Static / Motion"  
  \],  
  "guest\_asset\_pack\_potential": \[  
    "video",  
    "carousel",  
    "poll\_visual"  
  \],  
  "main\_question": "",  
  "first\_line\_anchors": {  
    "cinematic": "",  
    "emotional": "",  
    "reels\_hook": ""  
  },  
  "depth\_anchor": "",  
  "narrative\_instrumental\_followups": \[\],  
  "expected\_source\_material": \[\],  
  "clip\_start\_rule": "start\_at\_selected\_first\_line\_anchor",  
  "depth\_eval\_rule": "answer\_must\_contain\_specific\_cost\_or\_tension",  
  "landing\_eval\_targets": \[\],  
  "repair\_followups": {  
    "too\_historical": "",  
    "too\_abstract": "",  
    "too\_flat": "",  
    "not\_clip\_ready": ""  
  }  
}

---

# **XIII. First-Line Anchor Doctrine**

Every content-intended answer should have at least three First-Line Anchor options:

1. **Cinematic**  
2. **Emotional**  
3. **Reels Hook**

The purpose is not to script the guest.

The purpose is to create:

* a clean clip start,  
* an immediate emotional lane,  
* recognizable keywords for the backend,  
* a stronger first 2–3 seconds,  
* a consistent extraction boundary.

## **Example**

{  
  "first\_line\_anchors": {  
    "cinematic": "La nuit où mon identité est devenue dangereuse, j’étais dans une cour à Bwiza…",  
    "emotional": "À Bwiza, ce soir-là, j’ai senti l’air changer avant les mots…",  
    "reels\_hook": "Je suis entré dans cette cour comme un ami, et j’en suis sorti comme un suspect…"  
  }  
}

---

# **XIV. Depth Anchor Doctrine**

The Depth Anchor prevents the answer from flattening.

It is the human-interview equivalent of runtime cognitive constraint.

The First-Line Anchor controls the start.

The Depth Anchor controls the depth trajectory.

The landing is evaluated, not forced.

## **Example**

First-Line Anchor:  
“Je suis entré dans cette cour comme un ami, et j’en suis sorti comme un suspect…”

Depth Anchor:  
“Avant de parler d’histoire ou de politique, qu’est-ce que cette scène a fait au jeune Claude qui était là ?”

---

# **XV. Archetype Contract Registry Integration**

V9.1 formally connects the interview system to the new archetype registry architecture.

The routing chain is:

Expression Moment  
↓  
Core Content Archetype Schema  
↓  
Asset Derivative Schema  
↓  
Meme / Reaction Mechanism  
↓  
CMF Render Mode  
↓  
Evaluation Receipt

This prevents random content generation.

The system should know why each asset exists.

---

# **XVI. Required Registries**

## **1\. Core Content Archetype Schemas**

Define the meaning structure.

Examples:

* Transformation Story  
* Witness Story  
* Backstory Reveal  
* Confessional Turn  
* Conceptual Contrast  
* Visual Timeline  
* Worst Case Scenario  
* Shocking Comparison  
* Myth Debunk  
* Core Educator / Explainer  
* Challenger / Frame Breaker  
* Authority Proof Stack

## **2\. Asset Derivative Schemas**

Define packaging.

Examples:

* Dopamine Cliff Carousel  
* Relief Peak Carousel  
* Dilemma Poll / Would You Rather  
* Persuasive Micro-Claim  
* Thought Whisperer Extract  
* Mirror Prompt  
* Tension Poll  
* Quote-to-Question  
* Scene-to-Principle  
* Identity Mirror  
* Data Story Post

## **3\. Meme Mechanism Schemas**

Define humor psychology.

Examples:

* Benign Violation  
* Incongruity  
* Relief Theory  
* Superiority Theory  
* Micro-Contradiction  
* Tribal Absurdity  
* Status Satire

## **4\. Reaction Archetype Schemas**

Define participatory response content.

Examples:

* Validation Reaction  
* Solo Reaction  
* Vote Then React  
* Debate with Jury Mode  
* Reaction Duel  
* Reaction Seed

## **5\. CMF Render Mode Schemas**

Define production route.

Examples:

* Personal-Brand Commentary  
* Cinematic Story Commentary  
* Paper-Cut Explainer  
* Animated Avatar Explainer  
* Living Commentary Reaction  
* Conscious Reactions Editing  
* Meme / Dance / Reaction  
* Cinematic Metaphor  
* Data Story  
* Quiz / Ranking  
* Carousel Static / Motion

---

# **XVII. Guest Asset Pack Standard**

The Guest Asset Pack is the first paid proof unit.

## **Standard Deliverables**

4 videos  
2 carousels  
2 meme visuals  
2 poll visuals  
2–3 reaction seeds

## **Purpose**

The Guest Asset Pack proves:

* the guest can be activated,  
* the system can extract usable expression,  
* CCP can produce multi-format assets from one session,  
* the backend can route expression into repeatable content structures.

---

# **XVIII. Guest Asset Pack Compilation Logic**

## **4 Video Assets**

### **Video 1 — Cinematic Story Commentary**

Source archetypes:

* Transformation Story  
* Backstory Reveal  
* Worst Case Scenario  
* Witness Story

CMF routes:

* Cinematic Story Commentary  
* Personal-Brand Commentary

Purpose:

* story  
* emotional identification  
* narrative authority

---

### **Video 2 — Educational / Explainer**

Source archetypes:

* Core Educator / Explainer  
* Conceptual Contrast  
* Scene-to-Principle  
* Visual Timeline

CMF routes:

* Paper-Cut Explainer  
* Animated Avatar Explainer

Purpose:

* teaching  
* clarity  
* framework extraction

---

### **Video 3 — Challenger / Frame Breaker**

Source archetypes:

* Myth Debunk  
* Challenger / Frame Breaker  
* Industry Hypocrisy Exposure  
* Shocking Comparison

CMF routes:

* Personal-Brand Commentary  
* Conscious Reactions Editing

Purpose:

* authority  
* edge  
* belief correction

---

### **Video 4 — Reaction / Recognition Clip**

Source archetypes:

* Validation Reaction  
* Solo Reaction  
* Vote Then React  
* Audience Mirror Quiz  
* Reaction Seed

CMF routes:

* Living Commentary Reaction  
* Conscious Reactions Editing

Purpose:

* audience participation  
* social proof  
* comment generation

---

# **XIX. Carousel Assets**

## **Carousel 1 — Timeline / Story Arc**

Preferred archetypes:

* Visual Timeline  
* Transformation Story  
* Hero’s Journey  
* Backstory Reveal

Purpose:

* show evolution  
* teach through time  
* create narrative coherence

## **Carousel 2 — Relief / Contrast / Identity Mirror**

Preferred archetypes:

* Relief Peak Carousel  
* Conceptual Contrast  
* Identity Mirror  
* Scene-to-Principle  
* Quote-to-Question

Purpose:

* create recognition  
* compress insight  
* move viewer from tension to clarity

---

# **XX. Meme Visual Assets**

## **Meme 1 — Micro-Contradiction / Incongruity**

Purpose:

* compress paradox  
* create shareability  
* expose absurdity

Compatible mechanisms:

* Incongruity  
* Micro-Contradiction  
* Benign Violation

## **Meme 2 — Tribal Absurdity / Relief / Superiority**

Purpose:

* create group recognition  
* release tension  
* build social identity

Compatible mechanisms:

* Relief Theory  
* Superiority Theory  
* Tribal Absurdity  
* Status Satire

---

# **XXI. Poll Visual Assets**

## **Poll 1 — Tension Poll**

Purpose:

* force meaningful distinction,  
* generate comments,  
* create social participation.

Example:

“Le silence familial protège, blesse, ou les deux ?”

## **Poll 2 — Dilemma Poll / Would You Rather**

Purpose:

* reveal values,  
* create debate,  
* prepare Power Hour discussion.

Example:

“Vaut-il mieux connaître la vérité trop tôt, ou hériter du silence trop tard ?”

---

# **XXII. Reaction Seeds**

Every Guest Asset Pack should store reaction seeds even if not produced immediately.

Reaction seeds become future:

* Solo Reactions  
* Vote Then React  
* Debate with Jury Mode  
* Power Hour prompts  
* Telegram polls  
* challenge discussion prompts

## **Reaction Seed Object**

{  
  "reaction\_seed\_id": "rs\_001",  
  "source\_expression\_moment\_id": "em\_004",  
  "source\_quote": "Le silence d’un ami peut faire plus de bruit que la colère d’un ennemi.",  
  "reaction\_question": "Le silence d’un ami : trahison, peur, ou survie ?",  
  "compatible\_reaction\_formats": \[  
    "Validation Reaction",  
    "Vote Then React",  
    "Debate with Jury Mode"  
  \],  
  "status": "stored\_for\_future\_use"  
}

---

# **XXIII. CMF Integration**

Every asset route must become a Complete Editing Session.

The Complete Editing Session remains the CMF test boundary.

V9.1 simply clarifies that the Complete Editing Session is downstream of the Complete Expression Session.

## **Handoff Object**

{  
  "complete\_editing\_session\_request": {  
    "source\_expression\_session\_id": "xes\_2026\_0001",  
    "source\_expression\_moment\_id": "em\_002",  
    "asset\_type": "short\_video",  
    "core\_archetype": "Transformation Story",  
    "asset\_derivative": "Scene-to-Principle",  
    "cmf\_route": "Cinematic Story Commentary",  
    "visual\_style": "paper\_cutout\_stop\_motion",  
    "identity\_pack\_required": true,  
    "face\_video\_required": true,  
    "clip\_start\_timestamp": "00:14:23",  
    "clip\_end\_timestamp": "00:15:18",  
    "evaluation\_requirements": {}  
  }  
}

---

# **XXIV. Evaluation Requirements**

## **Expression Session Evaluation**

The session should be evaluated for:

* recording quality  
* anchor success  
* depth success  
* archetype coverage  
* asset yield  
* guest comfort  
* clipability  
* narrative density

## **Question Evaluation**

Each question should be evaluated for:

* Did it induce the target state?  
* Did the First-Line Anchor create a clean start?  
* Did the Depth Anchor prevent flattening?  
* Did the answer generate usable source material?  
* Did the answer route into at least one archetype?  
* Did the answer produce a strong landing?

## **Asset Package Evaluation**

The Guest Asset Pack should be evaluated for:

* 4 videos produced or candidates identified  
* 2 carousels produced or candidates identified  
* 2 meme visuals produced or candidates identified  
* 2 poll visuals produced or candidates identified  
* reaction seeds stored  
* emotional range diversity  
* archetype diversity  
* CMF route diversity

## **CMF Evaluation**

Each rendered asset should evaluate:

* identity consistency  
* composition quality  
* style consistency  
* emotional accuracy  
* platform fit  
* negative space compliance  
* hook strength  
* shareability  
* routeability

---

# **XXV. V9.1 Insertions into Existing Documentation**

## **Insert into CCP V9 after Complete Expression Session**

Add:

V9.1 requires every Complete Expression Session to include a recording configuration, capture quality gate, and file delivery protocol. The quality of the human expression source determines the ceiling of all downstream CMF production.

## **Insert into Narrative State Induction section**

Add:

Every content-intended question must be represented as an Interview Asset Contract. The question is not merely a prompt; it is a routing object that defines archetype, asset derivatives, first-line anchors, depth anchors, CMF routes, and evaluation targets.

## **Insert into Guest Asset Pack section**

Add:

The Guest Asset Pack must compile across multiple asset classes: 4 video assets, 2 carousel assets, 2 meme visuals, 2 poll visuals, and 2–3 reaction seeds. Each deliverable must be traceable to a source expression moment and archetype route.

## **Insert into CMF handoff section**

Add:

CMF does not receive raw interview transcripts. CMF receives structured Complete Editing Session requests generated from Expression Moments, each containing archetype metadata, asset derivative metadata, render mode requirements, source timestamps, and evaluation requirements.

---

# **XXVI. Governing Laws of V9.1**

## **Law 1 — Capture Quality Is Strategic**

The recording setup is not a technical afterthought. It defines the ceiling of downstream asset quality.

## **Law 2 — Meeting Platforms Are Not Masters**

Google Meet, Zoom, or similar tools are conversation layers and backup sources. The phone or local recording is the master file unless otherwise specified.

## **Law 3 — Every Question Is a Contract**

A question must define its target archetype, expression state, anchors, depth path, asset routes, and evaluation logic.

## **Law 4 — Anchors Are Production Boundaries**

First-Line Anchors create clean starts for the guest, viewer, and backend.

## **Law 5 — Depth Anchors Prevent Centroid Answers**

The Depth Anchor ensures the guest does not remain in generic explanation mode.

## **Law 6 — Assets Are Compiled, Not Generated**

Every asset must be traceable to an expression moment, archetype, derivative, and CMF route.

## **Law 7 — Reaction Seeds Must Be Stored**

Not every reaction asset must be produced immediately, but every strong reaction surface should be preserved.

## **Law 8 — Telegram Comes Later**

Telegram becomes useful after the system has narrative context, challenge logic, and community prompts. It is not required for the first Guest Asset Pack.

## **Law 9 — Every Session Trains the System**

Every interview updates:

* guest profile  
* interviewer profile  
* anchor library  
* depth anchor library  
* archetype survival memory  
* CMF route performance  
* reaction seed library

## **Law 10 — Human Activation Remains the Source**

The backend multiplies expression. It does not replace the human experience that creates it.

---

# **XXVII. Final Position**

CCP V9.1 completes the operational bridge between human activation and deterministic media production.

The interview is no longer a loose conversation.

It is a structured capture environment.

The phone setup is no longer a practical detail.

It is part of the production doctrine.

The question deck is no longer a list of prompts.

It is a set of asset contracts.

The archetype stack is no longer a content inventory.

It is a schema registry.

The CMF pipeline is no longer fed by vague content ideas.

It is fed by expression moments with metadata, archetype routes, asset derivatives, and evaluation requirements.

The final summary:

**CCP V9.1 formalizes the capture layer: every interview becomes a Complete Expression Session with recording configuration, asset contracts, archetype routing, CMF render routes, and evaluation receipts.**

This patch makes V9 executable.

