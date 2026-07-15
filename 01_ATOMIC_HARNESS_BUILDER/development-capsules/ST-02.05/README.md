# ST-02.05 Development Capsule

This capsule governs only the `DECLARED_BOUNDARY` mode of confirmed Story `ST-02.05`, “Ratify and Freeze the Draft Harness Boundary.” It is category-neutral and continues the completed synthetic Builder Core proof after `ST-01.02/SYNTHETIC_DEFINITION`.

The bounded outcome is: an authorized human can approve, revise, or reject the declared synthetic atomic boundary; approval atomically records the decision and freezes a transparent Draft Harness Model whose fields retain authority and knowledge status. Downstream work can consume only the frozen boundary and may not silently broaden, merge, or split it.

This capsule does not authorize implementation. Its authorization gate is `READY_AWAITING_HUMAN_AUTHORIZATION`, and the only accepted phrase is:

`AUTHORIZE BUILDER ST-02.05 DECLARED-BOUNDARY BOUNDED IMPLEMENTATION`

That phrase authorizes this Story implementation only. It does not itself ratify a boundary, authorize `ST-03.03`, certify a Harness, or authorize production, Format 02, VAE, Delegation runtime, conversational, GPU, provider, evaluator, or publication behavior.

Run tests with `PYTHONPATH=src`. The current verified baseline is `57 passed`; bare `python -m pytest -q` is not the repository invocation because the project uses a `src/` layout.
