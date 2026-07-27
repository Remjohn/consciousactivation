# CS-002 Skill

## Purpose

Apply the Face Recognition Window so a scene uses a face as an early social lock instead of leaving the viewer in generic visual search.

## Use This Skill When

- selecting HOOK or teaching setups
- evaluating talking-head framing
- checking whether a scene introduces the coach face early enough

## Required Inputs

- face count
- shot scale
- face bounding boxes
- eye and mouth visibility
- time to face introduction

## Decision Procedure

1. Verify whether a usable face appears inside the recognition window.
2. Check that the face is large enough, readable, and positioned high enough.
3. Penalize multiple simultaneous faces unless comparison is intentional.

## Runtime Guidance

- Prefer one medium close-up face.
- Use the face as a recognition anchor, not as decorative presence.
- If the scene needs early trust, do not delay the face reveal.