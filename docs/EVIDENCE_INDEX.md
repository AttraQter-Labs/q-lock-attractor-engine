# Evidence Index — SPECTRUM GSE v1.0

This document enumerates all empirical and procedural evidence
supporting the claims of SPECTRUM GSE.

---

## E1 — Canonical Proof Run
- Artifact: `proofs/canonical_proof_run.md`
- Artifact: `proofs/canonical_proof_run.json`
- Demonstrates:
  - Variance reduction: 46.1%
  - Topology immutability: verified
  - Determinism: reproducible outputs
  - Scalar refusal enforcement: disabled by policy

---

## E2 — Repeatability Tests
- Tests: `tests/test_repeatability.py`
- Result:
  - Identical inputs → identical outputs
  - Π-variation preserved, not collapsed
  - Watermark mode produces identical results across runs

---

## E3 — Refusal Surface Enforcement
- Tests: `tests/test_refusal.py`, `tests/test_scalar_guard.py`
- Result:
  - Scalar refused outside admissible region
  - No unsafe contraction allowed
  - EngineRefusal raised with explicit reasons
  - All four conditions must be satisfied for scalar admission

---

## E4 — CI Verification
- Workflow: `.github/workflows/ocir-pip-ci.yml`
- Verifies on every push:
  - No learning (learning=false in all reports)
  - No topology mutation (topology_mutation=false in all reports)
  - No scalar activation (SCALAR mode never in reports)
  - Proof run executes successfully
  - Version freeze (Version: 1.0.0 in core.py)
  - 19 unit tests pass

---

## E5 — Documentation Consistency
- `README.md` - Status badge: "Canonical v1.0 — Frozen"
- `docs/LIMITATIONS.md` - Hard limits documented
- `docs/CLAIM_BOUNDARY.md` - Falsification conditions explicit
- `docs/GOVERNANCE.md` - Frozen-core model enforced
- `docs/AUDITABILITY.md` - Third-party audit specifications

All claims are matched to enforceable checks.

---

## E6 — Negative Capability
SPECTRUM GSE explicitly demonstrates:
- What it cannot do (documented in WHEN_NOT_TO_USE.md)
- When it refuses (scalar mode conditions)
- Where falsification occurs (CLAIM_BOUNDARY.md)

This is considered affirmative evidence.

---

## E7 — Explorer-Validator Separation
- Tests: `tests/test_explorer_engine.py`
- Example: `examples/explorer_validator_workflow.py`
- Result:
  - ExplorerEngine generates variants without constraints
  - ValidatorEngine applies stability checks
  - Epistemic boundary preserved

---

## E8 — Backward Compatibility
- Code: `qlock/engine/core.py`
- Result:
  - TractorEngine alias maintained for ValidatorEngine
  - No breaking changes for existing users
  - Functional rename only

---

## Summary
SPECTRUM GSE v1.0 claims are supported by:
- Executable proof (canonical_proof_run.py)
- Enforced invariants (CI pipeline)
- Auditable refusal (test suite)
- Reproducible CI evidence (19 tests, proof run)
- Frozen behavioral specification (v1.0.0)

No claims rely on interpretation alone.
