# CS-005 Skill

## Purpose

Apply the Safe Zone Enforcer so faces, captions, and critical overlays stay inside biologically viable mobile viewing zones instead of fighting UI and thumb occlusion.

## Use This Skill When

- composing face, caption, and overlay placement
- adapting desktop-framed scenes for mobile export
- regenerating visuals that moved critical elements on screen

## Required Inputs

- element bounding boxes
- aspect ratio and platform layout
- UI exclusion zones
- element semantic priority

## Decision Procedure

1. Classify each critical element by priority.
2. Check whether it overlaps dead zones or low-value margins.
3. Return `PASS`, `REVISE`, or `BLOCK` with the violated placement rules.

## Runtime Guidance

- Safe zones are structural, not cosmetic.
- Do not let the final CTA, captions, or face anchor drift into platform chrome.
- Prefer upper-central placement for priority elements.