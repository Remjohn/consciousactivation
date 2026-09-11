# CMF Delegation Validators

This package contains transport-neutral Stage 3 conformance validators for the
canonical contract registry. It validates JSON Schema payloads, producer
authority, lifecycle transitions, compatibility negotiation, and canonical
hash inputs. It does not implement message delivery or product behavior.

Run the suite from the repository root:

```powershell
python -m unittest discover -s packages/validators/tests -v
```
