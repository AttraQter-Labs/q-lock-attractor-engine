# SPECTRUM GSE — Integration Guide

How to integrate SPECTRUM GSE into existing workflows.

## Integration Patterns

### 1. Post-Processing Layer
**Recommended for most users.**

```
Your workflow:
1. Execute circuit on hardware/simulator
2. Collect output distribution
3. Pass distribution to SPECTRUM GSE
4. Receive validation verdict + stabilized distribution (if accepted)
```

SPECTRUM GSE does not replace your execution engine.
It validates and stabilizes outputs after execution.

### 2. Repeatability Analysis
Use SPECTRUM GSE to detect procedural divergence:

```
Run 1: Circuit A → Distribution P1 → SPECTRUM GSE → Verdict V1
Run 2: Circuit A → Distribution P2 → SPECTRUM GSE → Verdict V2

Compare:
- Are P1 and P2 similar?
- Are V1 and V2 consistent?
- Does SPECTRUM GSE refuse one but not the other?
```

Refusal differences indicate procedural sensitivity.

### 3. Explorer–Validator Workflow
For hypothesis generation and falsification:

```
1. ExplorerEngine generates procedural variants
2. Execute each variant
3. ValidatorEngine validates each result
4. Analyze refusal patterns
```

Refusals surface hidden assumptions.

## Integration Points

### Python API
```python
from qlock.engine.core import ValidatorEngine
from qlock.engine.core import EngineContext, EngineMetrics

context = EngineContext(
    noise=0.002,
    depth=10,
    phase_dispersion=0.1,
    procedural_disorder=0.3,
    topology="low"
)

metrics = EngineMetrics(
    coherence_r=0.85,
    entropy_h=2.3,
    variance_v=0.05,
    bias_retention=0.92
)

engine = ValidatorEngine(context)
result = engine.apply(metrics, mode="fidelity")
```

### Adapter Interface (Simplified)
```python
from adapters.validator_engine import ValidatorEngineAdapter

adapter = ValidatorEngineAdapter()
verdict = adapter.apply(
    distribution=p,
    mode="fidelity",
    meta={"observer_id": "experiment-001"}
)

if verdict["status"] == "APPLIED":
    stabilized = verdict["distribution"]
else:
    refusal_reason = verdict["verdict"]
```

## Integration Checklist

- [ ] SPECTRUM GSE used **after** circuit execution
- [ ] Distributions normalized (sum to 1.0)
- [ ] Noise and context parameters set appropriately
- [ ] Refusals handled explicitly (not ignored)
- [ ] Scalar mode never auto-enabled
- [ ] Results logged for audit trail

## Common Integration Mistakes

### ❌ Using SPECTRUM GSE as a compiler
SPECTRUM GSE does not transpile or rewrite circuits.

### ❌ Expecting SPECTRUM GSE to improve metrics
SPECTRUM GSE validates stability, not performance.

### ❌ Ignoring refusals
Refusals are informative, not errors.

### ❌ Tuning SPECTRUM GSE parameters
Thresholds are hard-coded and not tunable.

### ❌ Averaging away procedural history
SPECTRUM GSE operates per-run, preserving Π.

## Platform-Specific Notes

### Qiskit
SPECTRUM GSE does not interface with Qiskit directly.
Extract the output distribution from `result.get_counts()` and pass to SPECTRUM GSE.

### Cirq
Extract probability distribution from measurement results.
SPECTRUM GSE operates on distributions, not circuits.

### Custom Simulators
SPECTRUM GSE accepts any normalized probability distribution.
Bridge your simulator output to SPECTRUM GSE via adapters.

## Support & Questions

For integration questions, see:
- `examples/proof_run.py` — Canonical usage example
- `examples/explorer_validator_workflow.py` — Advanced workflow
- `docs/USE_CASES.md` — When to use SPECTRUM GSE
- `docs/WHEN_NOT_TO_USE.md` — When NOT to use SPECTRUM GSE
