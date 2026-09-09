# CMF Format Builder Operating Blueprint


## Drill-me prompt layer

The workstream prompts are bootstraps. They start each format module. They are not enough by themselves.

Every format workstream must also use the Drill-me prompts in:

```text
prompts/drill_me/
```

Use Drill-me before approving:
- a new format;
- a new dish;
- a new scene or slide syntax;
- any BBOX + WHY map;
- any pose/gaze/memetic acting style;
- any sonic guidance plan;
- any runtime and QA ownership decision.

Drill-me approval states are:

```text
blocked | revise | approve
```

Approval means the item can enter the module registry draft. It does not mean the format is finished.

The Drill-me layer prevents generic, semantic-first, visually unjustified, centroid, or runtime-ambiguous outputs from entering CMF Studio.
