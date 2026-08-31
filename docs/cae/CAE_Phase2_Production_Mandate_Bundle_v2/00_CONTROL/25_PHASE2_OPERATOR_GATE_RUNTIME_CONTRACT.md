# Phase 2 — Operator Gate Runtime Contract

An Operator Gate is a durable CAE state boundary, not a conversational request.

Required:
- enter WAITING_OPERATOR (or canonical equivalent);
- persist immutable decision context;
- expose only through authenticated/authorized operator surfaces;
- persist approval/rejection as an authoritative CAE operation/receipt;
- resume from exact durable state;
- make repeated decisions idempotent;
- prevent the model from approving its own work;
- prevent UI-only approval state.
