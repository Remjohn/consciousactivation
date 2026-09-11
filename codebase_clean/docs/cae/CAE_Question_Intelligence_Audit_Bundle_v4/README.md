# CAE Question Intelligence Audit Bundle v4

This bundle corrects the earlier design by making **book auditing the sole source-development phase**. Primitive creation is explicitly downstream.

### Execution order

1. Put each real book PDF/full text into the local workspace.
2. For each book, execute exactly one mandate from `02_mandates/books/`.
3. Each execution creates exactly one `AUDIT_*.md` file.
4. Operator reviews and accepts the audit.
5. Repeat until all 12 audits are accepted.
6. Only then activate the later cross-book clustering / Question Primitive Creation Skill gate.

### What is NOT created in this phase

No `PRM-QST-*` canonical registry objects. No production runtime integration. No Question IR implementation. No silent promotion of existing candidate YAMLs.
