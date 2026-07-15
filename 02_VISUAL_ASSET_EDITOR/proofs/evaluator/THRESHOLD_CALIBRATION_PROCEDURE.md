# Threshold-Calibration Procedure

Classification: `non_production_readiness_proof`

No final threshold is defined here.

1. Pin the evaluator, program, deterministic settings and calibration corpus digest.
2. Freeze the annotation rubric and adjudicate the calibration labels.
3. Keep the protected set sealed and prove non-overlap before tuning.
4. Produce per-dimension and per-slice score distributions with uncertainty and abstentions.
5. Evaluate candidate operating points against false-positive and false-negative consequences.
6. Decide non-compensable gates independently of ranking-score calibration.
7. Review critical false negatives case by case and document arbitration.
8. Obtain evaluation and product authority approval for any selected operating point.
9. Run the protected set once under release controls.
10. Retain the prior pinned baseline and rehearse rollback before promotion.

Any model, prompt, template, corpus, label-policy or applicability change invalidates the affected calibration and requires a versioned rerun.
