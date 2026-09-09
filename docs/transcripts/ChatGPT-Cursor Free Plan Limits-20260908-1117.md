# Cursor Free Plan Limits

**User:** Anonymous  
**Created:** 9/8/2026 10:57:53  
**Updated:** 9/8/2026 11:13:28  
**Exported:** 9/8/2026 11:17:02  
**Link:** [https://chatgpt.com/c/6a9fce10-1dac-83eb-b961-dab8e940aefb](https://chatgpt.com/c/6a9fce10-1dac-83eb-b961-dab8e940aefb)  

## Prompt:
9/8/2026, 11:01:39 AM

what are the models available now in the free version of cursor?? also what are the limits when you are in the free plan?? can I use it for these type of tasks?? basically I use chatgpt claude and grok parallel accounts to implement my specs and save them in a zip file 

I give them access to my codebase via zipfiles as well

once they've completed the budle they hand me the files then I would like to have cursor free version with my repo to do this 

like for instance: 

"Apply all bundles in Mandates implementation/epoch_04/. Read their AGENT_HANDOFF.md files, copy and wire the files into the repo under the ATC protocol, run the relevant tests across all 6 mandates (CA-M007, CA-M017, CA-M018, CA-M019, CA-M039, CA-M040), resolve any dependency/fixture gaps, verify 100% pass rate, update walkthrough.md, and commit the verified epoch to git."

## Response:
9/8/2026, 11:01:39 AM

> **Searching the web**
>
>
> **Searching 3 websites**
>
> 
>
> Worked for a few seconds

Yes - **your workflow is a very good fit for Cursor**, but there’s an important catch: **the current Free/Hobby plan is much more restricted than “Cursor with whatever model you want.”**

I checked Cursor’s current docs/pricing and recent Cursor staff clarification, because this has changed recently.

### What you get on Cursor Free/Hobby right now

Cursor calls the free tier **Hobby**. It includes:

- **Limited Agent requests**
- **Limited Tab completions**
- **Composer**
- Agent, Chat and Tab functionality using **Auto**
- No credit card required. ([Cursor](https://prod.cursor.com/en-US/pricing?utm_source=chatgpt.com))

The big limitation is **model selection**.

As of the current September 2026 behavior, the Free/Hobby model picker is **locked**. Cursor staff specifically confirmed that on Free, the model picker stays locked to **Cursor Grok 4.6 Medium**, and BYOK with your own Anthropic/OpenAI key does **not** unlock Agent/Chat model selection. You need Pro for that. ([Cursor - Community Forum](https://forum.cursor.com/t/cant-switch-model/169806/10?utm_source=chatgpt.com))

So I would think of Free as:

> **Cursor Agent powered by a constrained Cursor-selected model**

rather than:

> **A free IDE where I can choose Claude/GPT/Grok/etc.**

### What models does Cursor have overall?

The current Cursor model catalog includes quite a lot:

| Family | Current models |
|---|---|
| Cursor | **Grok 4.6**, Grok 4.5, Composer 2.5 |
| Anthropic | Claude Fable 5.1, Claude Opus 5, Claude Sonnet 5 |
| Google | Gemini 3.1 Pro, Gemini 3.8 Flash |
| OpenAI | GPT-5.6 Luna, GPT-5.6 Sol, GPT-5.6 Terra |

Cursor's current documentation separates the first-party **Cursor Models** pool (Grok + Composer) from the third-party model pool. ([Cursor](https://cursor.com/docs/models-and-pricing))

But **most of those are not selectable on Hobby**.

---

# For your particular workflow: YES, with qualifications

Your workflow is actually a pretty sensible architecture:

**ChatGPT + Claude + Grok**

↓ independently implement/speculate/review

**implementation bundles**

↓  

`epoch_04/`

```text
CA-M007/
    ...
CA-M017/
    ...
CA-M018/
    ...
...

AGENT_HANDOFF.md
```

↓

**Cursor**

> Apply all bundles, integrate them into the real repository, run everything, repair integration problems, verify, document, commit.

That's exactly the sort of job an agentic coding IDE is designed for. Cursor describes its Agent as being able to understand a codebase, build features, fix bugs, review changes, etc. ([Cursor](https://cursor.com/docs?utm_source=chatgpt.com))

And importantly, **Cursor Agent can work against your local repository**, meaning it isn't necessary to give Cursor a giant ZIP every time. You open the actual repo in Cursor and let the agent inspect/edit/run commands in that working tree.

---

# Your example is actually a good Cursor task

This:

> "Apply all bundles in Mandates implementation/epoch_04/. Read their AGENT_HANDOFF.md files, copy and wire the files into the repo under the ATC protocol, run the relevant tests across all 6 mandates (CA-M007, CA-M017, CA-M018, CA-M019, CA-M039, CA-M040), resolve any dependency/fixture gaps, verify 100% pass rate, update walkthrough.md, and commit the verified epoch to git."

is **much more appropriate for Cursor Agent than for a normal chat window.**

Why?

Because the agent can potentially:

1. inspect the repository
2. inspect all six bundles
3. read `AGENT_HANDOFF.md`
4. inspect existing architecture
5. copy/move files
6. modify imports
7. modify registrations/configuration
8. execute tests
9. inspect failures
10. modify fixtures/dependencies
11. rerun tests
12. inspect the final diff
13. update documentation
14. create a git commit

That iterative **read → modify → execute → diagnose → modify → test** loop is the important part.

Cursor also has a Plan Mode specifically intended for larger implementation jobs: it researches the codebase and produces a plan before making changes. ([Cursor](https://cursor.com/docs/agent/plan-mode?utm_source=chatgpt.com))

---

# But I would NOT use Free as your primary "integration agent"

This is the important distinction.

Your workload isn't:

> "Make me a small function."

It's closer to:

> **"Take six independently-produced implementation packages and integrate them into an existing architecture, then prove the resulting repository works."**

That's a relatively demanding agent workload.

The free tier has **limited Agent usage**, and once you hit that limitation you're done until the allowance resets. Cursor doesn't publish a simple permanent number like "exactly X full agents per month" on the current Hobby pricing page; it describes it as limited usage. ([Cursor](https://prod.cursor.com/en-US/pricing?utm_source=chatgpt.com))

And your task can burn considerably more agent usage than a normal request because the agent may need many turns of:

```text
inspect
→ edit
→ test
→ failure
→ inspect
→ edit
→ test
→ failure
→ fix
→ test
→ verify
```

So **Free is excellent for trying this workflow**, but I wouldn't design your entire development pipeline around the assumption that Free will reliably finish a large epoch every time.

---

# The really interesting part of your workflow

I actually think you have the beginnings of a **very good multi-agent software-development pipeline**.

I'd structure it like this:

```text
                  SPEC
                   │
       ┌───────────┼───────────┐
       ↓           ↓           ↓
    ChatGPT      Claude       Grok
       │           │           │
       │           │           │
       └────── implementation ─┘
                   │
                   ↓
          REVIEWABLE BUNDLES
                   │
                   ↓
       Mandates implementation/
              epoch_04/
                   │
                   ↓
              CURSOR AGENT
                   │
       ┌───────────┼───────────┐
       ↓           ↓           ↓
    integrate    test       repair
       │           │           │
       └───────────┼───────────┘
                   ↓
              verification
                   ↓
             walkthrough.md
                   ↓
              git commit
```

In other words:

### ChatGPT / Claude / Grok
are your **implementation workers / competing designers**.

### Cursor
becomes your **repository integration + verification agent**.

That's a very reasonable division of labor.

---

# One thing I'd change in your handoff system

I'd make `AGENT_HANDOFF.md` extremely structured.

For example:

```text
# Mandate: CA-M007

## Objective
...

## Files Added
...

## Files Modified
...

## Integration Points
...

## Dependencies
...

## Fixtures
...

## Required Commands
...

## Tests
...

## Expected Results
...

## Architectural Constraints
...

## Known Limitations
...

## DO NOT
...

## Verification Checklist
- [ ] files copied
- [ ] imports wired
- [ ] registration completed
- [ ] fixtures installed
- [ ] unit tests pass
- [ ] integration tests pass
- [ ] no unrelated regressions
```

Then Cursor isn't trying to infer the entire contract from six ZIP files.

It gets a **machine-readable-ish integration contract**.

That will make your workflow substantially more reliable.

---

# And I'd change your Cursor prompt slightly

Instead of immediately saying "apply everything", I'd use a two-phase approach.

### Phase 1 - audit

Give Cursor:

> Inspect `Mandates implementation/epoch_04/` and the repository. Read every `AGENT_HANDOFF.md`. Do not modify files yet. Build an integration plan showing, for each mandate, the files to add/modify, integration points, dependencies, fixtures, tests, and any conflicts between bundles. Identify anything that violates the ATC protocol or existing repository architecture.

Then review its plan.

### Phase 2 - execute

Then:

> Execute the approved epoch integration plan. Apply all six mandates. Preserve existing architecture and ATC protocol. Run the specified tests after each logical integration group. Resolve dependency, fixture, import, registration, and integration failures rather than merely reporting them. Do not weaken or delete tests to obtain a passing result. At the end, run the complete relevant test suite, verify 100% pass rate, inspect the final git diff, update walkthrough.md, and create a git commit containing only the verified epoch changes.

That's considerably safer.

---

# One particularly important rule

I would explicitly tell Cursor:

> **Do not modify tests merely to make them pass.**

And:

> **Do not declare success based on individual mandate tests if the cross-mandate suite has not passed.**

Because you're using several independent AI systems to produce code, **integration conflicts are probably the main thing Cursor needs to catch.**

You want Cursor to act more like:

**integration engineer + CI engineer + code reviewer**

rather than simply another code generator.

---

# Is Free powerful enough?

My assessment for *your* workflow:

| Task | Cursor Free |
|---|---|
| Open your existing repo | ✅ |
| Understand repository | ✅ |
| Read handoff files | ✅ |
| Modify source | ✅ |
| Run terminal commands/tests | ✅ |
| Git operations | ✅ |
| Small bug fixes | ✅ |
| Small feature integration | ✅ |
| One mandate | 🟢 likely reasonable |
| Six-mandate epoch | 🟡 possible, but usage may run out |
| Large multi-step integration | 🟡 |
| Repeated autonomous debugging | 🟠 free limits become a problem |
| Choose Claude/GPT/Grok manually | ❌ on current Hobby |
| Use your own API keys to bypass model restriction | ❌ on current Hobby |
| Long-running serious integration pipeline | 🟠/🔴 I'd use Pro |

The **model restriction** is arguably more important than the raw usage limit for you. Current Cursor documentation says Hobby gets the core Agent/Chat/Tab functionality with limited usage, while Cursor's own pricing page reserves extended Agent limits and frontier-model access for Pro+. ([Cursor](https://prod.cursor.com/en-US/pricing?utm_source=chatgpt.com))

---

## My recommendation for your setup

I'd actually try this:

**Keep your existing three AI subscriptions.**

Use them as your **parallel implementation layer**.

Then install Cursor Free and use it as:

> **the local integration/verification layer.**

If it consistently gets through your epochs before hitting its limits, you've got a very cheap fourth agent.

If you repeatedly hit the Hobby ceiling halfway through epochs, **then Pro becomes much more compelling**, because your bottleneck isn't generating the individual implementations anymore - it's having a capable agent stay in the repository long enough to integrate and verify them.

And Cursor's current Pro is **$20/month**, with extended Agent limits and access to frontier models. ([Cursor](https://prod.cursor.com/en-US/pricing?utm_source=chatgpt.com))

So I **wouldn't pay for Cursor immediately**. Your proposed Free experiment is exactly the right way to determine whether its Agent capacity is sufficient for the size of your epochs.

**One caveat:** don't confuse Cursor's current model catalog with what Free actually lets you choose. The catalog is broad; **Hobby is intentionally constrained**. The current Cursor staff confirmation from August 31, 2026 is unusually explicit about that. ([Cursor - Community Forum](https://forum.cursor.com/t/cant-switch-model/169806/10?utm_source=chatgpt.com))

If you want, I can also design a **`AGENT_HANDOFF.md` + epoch directory protocol specifically for this ChatGPT/Claude/Grok → Cursor pipeline**, including how I'd structure the ZIP bundles so Cursor can integrate 6–20 mandates with minimal ambiguity.

---

**Sources:**

- [Cursor · Pricing](https://prod.cursor.com/en-US/pricing?utm_source=chatgpt.com)
- [Can't switch model - #10 by deanrie - Bug Reports - Cursor - Community Forum](https://forum.cursor.com/t/cant-switch-model/169806/10?utm_source=chatgpt.com)
- [Models & Pricing | Cursor Docs](https://cursor.com/docs/models-and-pricing)

## Prompt:
9/8/2026, 11:07:24 AM

I do not have funds now so I Just want to know if the limits on cursor will not be too limiting here's onve of the bundle and how it looks like 

It has ACTUALLY Been built from the same code base so why should it be difficult to just copy the files in the right places?? I dont get it... copying files in the codebase and running test via the terminal that shouldn't like crazy thing to do

[Attachment: CA-M020_BUNDLE.zip]

## Response:
9/8/2026, 11:07:35 AM

> **Inspecting ZIP archive contents**
>
>
> ****
>
> 
>
> **Inspected ZIP archives and agent handoff bundle contents**
>
> 
>
> Worked for 15s

Ah - **seeing the actual bundle changes my assessment quite a bit.** Your intuition is basically correct.

I inspected the `CA-M020_BUNDLE.zip` you uploaded, and this is **not** some giant autonomous coding task. The handoff is unusually explicit about exactly where the files go.

For CA-M020, the bundle literally says:

- add `reaction_receipts.py` → `services/interview/src/conscious_activations_interview_expression/reaction_receipts.py`
- add `test_ca_m020_reaction_receipts.py` → `tests/phase4/test_ca_m020_reaction_receipts.py`
- **no existing file is replaced**
- no database migration
- then run the supplied pytest command

So yes: **if your other bundles look like this, Cursor Free has a very realistic chance of handling your workflow.**

### What Cursor actually has to do

For this particular bundle, the agent's work is essentially:

```text
Read AGENT_HANDOFF.md
        ↓
copy 2 files into exact paths
        ↓
pytest -q tests/phase4/test_ca_m020_reaction_receipts.py
        ↓
if failure:
    inspect traceback
    determine whether it's an integration/dependency issue
    fix if appropriate
    rerun
        ↓
run broader regression test
        ↓
move to next mandate
```

That's **not crazy**.

And because you built the bundles from the **same codebase**, the situation is dramatically easier than asking an AI to merge arbitrary third-party code.

---

## The distinction I was making before

There are two very different scenarios:

### Scenario A - arbitrary AI-generated code

```text
Claude built feature against repo version A

ChatGPT built feature against repo version B

Grok built feature against repo version C

Cursor has repo version D

        ↓

"Figure out how all this fits together."
```

That's where things can get ugly.

### Scenario B - what you're actually doing

```text
                    SAME REPO SNAPSHOT
                          │
          ┌───────────────┼───────────────┐
          ↓               ↓               ↓
       ChatGPT          Claude           Grok
          │               │               │
          └───────────────┼───────────────┘
                          ↓
                 STANDARDIZED BUNDLE
                          │
                 exact destination
                    paths provided
                          │
                    AGENT_HANDOFF
                          │
                          ↓
                       Cursor
                          │
                   copy + test + fix
```

**That's much easier.**

The `AGENT_HANDOFF.md` in your bundle is doing a lot of the work already.

---

# And this bundle is particularly Cursor-friendly

Look at the important part:

> "This bundle contains only the two authorized paths below."

Then it gives exact source → destination mappings.

That's excellent for an agent.

You're effectively giving Cursor an **installation manifest**.

It doesn't have to decide:

> "Hmm, where should this file probably live?"

You have already told it.

Likewise:

> "No existing repository file is replaced by this bundle."

That removes another major ambiguity.

And:

> "No database migration is required."

Again, Cursor doesn't have to invent infrastructure work.

---

# Your biggest potential bottleneck is NOT the complexity

It's **usage consumption**.

That's the thing I'd test.

Suppose you give Cursor:

> Apply epoch 04.

And there are six bundles.

If every bundle is like CA-M020, the basic work could be quite modest:

```text
6 ×
  read handoff
  copy files
  run tests
  inspect result
```

If everything passes immediately, **that's a very small agent workload** compared with asking it to design and implement six mandates from scratch.

The problem happens when you get:

```text
CA-M007
   ↓
test failure
   ↓
debug
   ↓
dependency issue
   ↓
fix
   ↓
test

CA-M017
   ↓
test failure
   ↓
debug
   ↓
fixture problem
   ↓
fix
   ↓
test

...
```

Now the agent consumes substantially more interaction/context/tool usage.

But **that's a workload issue, not an inherent difficulty issue.**

---

# There's another thing in your favor

Your bundles already contain their own tests.

CA-M020 includes **11 acceptance/regression tests** covering things like:

- schema/invariant behavior
- persistence
- idempotency
- invalid media
- tampering
- dissociation
- regression behavior

And the handoff explicitly says which commands to run.

So Cursor doesn't need to invent a testing strategy.

It can simply execute the one supplied by the bundle.

That's exactly what I'd want an integration agent to receive.

---

# I'd actually make your epoch instruction more mechanical

Instead of asking Cursor to "figure out" everything, I'd give it something like:

**document: **

Apply the bundles in `Mandates implementation/epoch_04/` to the current repository.

For each bundle:

1. Read its `AGENT_HANDOFF.md` completely.
2. Follow its exact paste/integration instructions.
3. Do not invent alternative file locations or architectural changes when the handoff specifies an exact destination.
4. Do not overwrite existing files unless the handoff explicitly authorizes replacement.
5. Apply only the files and changes authorized by the bundle.
6. Run the targeted tests specified by the handoff.
7. If tests fail, inspect the failure and resolve genuine integration, dependency, import, fixture, or compatibility problems where possible.
8. Never weaken, delete, or modify tests merely to make them pass.
9. After each mandate, rerun its targeted tests and confirm they pass before proceeding.

After all six mandates have been applied:

- Run the relevant regression suites across CA-M007, CA-M017, CA-M018, CA-M019, CA-M039, and CA-M040.
- Resolve legitimate integration/dependency/fixture issues.
- Verify a 100% pass rate for the required test suites.
- Inspect the final git diff for unintended changes.
- Update `walkthrough.md` with the verified epoch results.
- Do not claim completion if the required tests are failing.
- Create a git commit containing the verified epoch changes.

At the end, report:
- bundles applied
- files added/modified
- tests executed
- final test counts/results
- any issues resolved
- any unresolved issues
- final commit SHA

That is much closer to what **your actual workflow needs**.

---

## One thing I would NOT ask Cursor to do

I wouldn't make it unzip things itself if you can avoid it.

I'd organize the repository/workspace so the bundles are already extracted:

```text
repo/
│
├── services/
├── tests/
├── walkthrough.md
│
└── Mandates implementation/
    └── epoch_04/
        ├── CA-M007/
        │   └── AGENT_HANDOFF.md
        ├── CA-M017/
        │   └── AGENT_HANDOFF.md
        ├── CA-M018/
        │   └── AGENT_HANDOFF.md
        ├── CA-M019/
        │   └── AGENT_HANDOFF.md
        ├── CA-M039/
        │   └── AGENT_HANDOFF.md
        └── CA-M040/
            └── AGENT_HANDOFF.md
```

Then Cursor sees the actual files and doesn't have to spend agent effort dealing with archive management.

---

# So, will Free be too limiting?

**Based on this bundle, I would now say: probably not for the initial integration work.**

I'd put it roughly like this:

| Your operation | Free suitability |
|---|---|
| Read `AGENT_HANDOFF.md` | 🟢 |
| Copy files | 🟢 |
| Make exact path changes | 🟢 |
| Run pytest | 🟢 |
| Run terminal commands | 🟢 |
| Fix a simple import/dependency error | 🟢 |
| Integrate one bundle like CA-M020 | 🟢 |
| Integrate six similar bundles | 🟢/🟡 |
| Debug a large number of cascading failures | 🟡 |
| Repeatedly run huge test suites | 🟡 |
| Implement missing functionality from scratch | 🟠 |
| Do all your original ChatGPT/Claude/Grok implementation work | 🔴 |

**That last distinction is important.**

You aren't asking Cursor to be your fourth primary developer.

You're asking it to be the **assembly + test + verification machine**.

And for that, your bundle architecture makes a lot of sense.

---

### One thing I'd be interested in seeing

**CA-M020 is only one bundle.** The thing that would let me give you a much more confident answer about whether Free will survive an entire epoch is seeing the **size/structure of one of your larger or messier bundles**-especially one where the tests currently don't all pass or where multiple existing files need wiring.

ask_user_files

If you upload one of those, I can compare it with CA-M020 and tell you **"this is likely a 5-minute Cursor job / this could burn a lot of Free usage"** rather than guessing.

## Prompt:
9/8/2026, 11:13:12 AM

so you suggest all the tests should be done in the ChatGPT/Claude/Grok implementation work ?? so no need to run the test inside cursor?? or it's safer to do both?

## Response:
9/8/2026, 11:13:13 AM

**Both. Definitely both.** But I would give the two stages different responsibilities.

Your current pipeline should be:

```text
ChatGPT / Claude / Grok
        │
        │ implement mandate
        ↓
   run its tests
        │
        ↓
   fix implementation
        │
        ↓
   bundle + AGENT_HANDOFF.md
        │
        │
        ▼
      Cursor
        │
        │ integrate bundle into actual repo
        ↓
   run targeted tests AGAIN
        │
        ↓
   fix integration problems
        │
        ↓
   run cross-mandate/regression tests
        │
        ↓
     verified epoch
```

### Why test twice?

Because **the first test answers a different question** from the second.

#### ChatGPT/Claude/Grok testing asks:

> "Does the implementation work in the environment/codebase I built it against?"

That's essential. You don't want to hand Cursor broken bundles.

#### Cursor testing asks:

> "Does this implementation still work after being installed into the actual repository alongside all the other mandates?"

That's equally important.

Even though you're using the same base codebase, things can change when you combine multiple mandates.

For example:

```text
CA-M020 alone
       ↓
11/11 tests pass ✅

CA-M017 alone
       ↓
24/24 tests pass ✅

CA-M039 alone
       ↓
18/18 tests pass ✅
```

Then:

```text
CA-M020 + CA-M017 + CA-M039
             ↓
       51 tests run
             ↓
       3 failures ❌
```

Those failures don't necessarily mean any individual implementation was bad.

They can be caused by:

- overlapping configuration
- imports/registrations
- shared fixtures
- dependency versions
- database state
- shared test infrastructure
- assumptions made independently by different implementations
- interactions between mandates

**That's precisely what you want Cursor to catch.**

---

## I would actually make Cursor's testing lighter than the implementation agents'

You don't want Cursor wasting its limited Free usage reproducing *everything* the other agents already proved.

I'd use three levels:

### 1. During implementation

ChatGPT/Claude/Grok:

```text
implement
→ targeted tests
→ fix
→ targeted tests
→ bundle
```

The bundle should ideally arrive at Cursor already green.

### 2. When Cursor installs each bundle

Cursor:

```text
copy/wire
→ targeted tests
```

This is cheap and gives you immediate confirmation that the installation didn't break anything.

### 3. At the end of the epoch

Cursor:

```text
all relevant mandate tests
        +
integration/regression tests
        +
broader project tests where appropriate
```

This is the **important second-level verification**.

---

# So your bundle shouldn't mean "tests are finished"

I'd think of `AGENT_HANDOFF.md` as saying:

> **"This implementation has been developed and validated. Here is exactly how to install and independently verify it."**

That distinction is valuable.

For example:

```text
CA-M020_BUNDLE.zip

AGENT_HANDOFF.md
reaction_receipts.py
test_ca_m020_reaction_receipts.py
```

The handoff might say:

```text
Implementation status:
- Implementation tests: PASS
- Expected targeted tests: 11 passed

Integration:
- No existing files replaced
- No migration required
- Exact destination paths listed below

Verification:
pytest -q tests/phase4/test_ca_m020_reaction_receipts.py
```

Then Cursor runs those tests **again after integration**.

---

# And there's a bigger advantage to your approach

You're effectively getting **independent verification from different AI contexts**.

Imagine:

**Claude**

> "My implementation passes."

↓

**Cursor**

> "After integrating it with the other five mandates, everything passes."

That's considerably stronger than simply trusting the first agent.

And if Cursor finds:

> `CA-M020` passes independently but fails after CA-M039 is installed

you've discovered a real integration problem **before committing the epoch**.

---

## I would NOT have Cursor blindly run the entire universe of tests after every file

That's where I agree with your concern about Free limits.

For six mandates:

```text
CA-M007
   ↓ targeted tests

CA-M017
   ↓ targeted tests

CA-M018
   ↓ targeted tests

...
```

Then once:

```text
ALL SIX INSTALLED
        ↓
cross-mandate tests
        ↓
relevant regression suite
        ↓
full required verification
```

That's a much better use of the limited agent allowance.

### In other words:

**Implementation agents prove the bundle.**

**Cursor proves the integration.**

**Cursor's final test run proves the epoch.**

That's the architecture I'd use for what you're doing.



---
Powered by [ChatGPT Exporter](https://www.chatgptexporter.com)