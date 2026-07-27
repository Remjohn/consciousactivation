# State Machine

```text
created
source_loaded
format_programs_attached
composition_attached
scene_realization_compiled
timeline_compiled
proxy_rendered
eval_passed
revision_required
final_timeline_locked
final_rendered
approved
exported
```

Blocked transitions:

```text
cannot compile timeline before scene realization
cannot proxy render before timeline compiled
cannot final render before final timeline lock
cannot export before approval
```
