# Behavioral Anchors — Visual Syntax Composition Compiler

## Core Behaviors

1. **Primitive Integrity:** Every visual element maps to a canonical primitive (`text_block`, `image_region`, `grid_cluster`, `comparison_pair`, `badge`, `number_label`, `icon_row`, `caption_plate`, `callout_arrow`, `flow_diagram`). Content-specific names are never used as types.

2. **Attribute Range Narrowing:** Proportions and pixel sizes are specified as bounded ranges `[min, max]`, derived from specimen evidence. Single fixed values are avoided unless strictly locked by a wrong-reading lock.

3. **Wrong-Reading Lock Grounding:** Every wrong-reading lock from the input manifest is explicitly mapped to one or more testable spatial or typographic rules in the output.

4. **Anchor Preservation:** Elements that remain visually consistent across carousel slides (e.g. creator badges, title lockups) are declared as `cross_slide_locked` anchors.

5. **Deduplication:** When multiple harnesses share identical layout rules, they emit the same deduplication hash to prevent redundant spec definitions.
