# SPECTRUM GSE — Known Limitations

SPECTRUM GSE v1.0 has explicit, non-negotiable limitations.
These are by design, not bugs.

## Hard Limits (Cannot Be Tuned)

### 1. Scalar Mode Boundaries
Scalar mode is **refused** unless ALL conditions hold:
- `noise ≤ 0.003`
- `phase_dispersion ≤ 0.2`
- `procedural_disorder ≤ 0.4`
- `topology != "high"`

These thresholds are **hard-coded**.
They are not hyperparameters.

### 2. No Learning
SPECTRUM GSE does not:
- Adapt to data
- Improve with experience
- Train on examples
- Update internal parameters

This is a design guarantee.

### 3. No Topology Mutation
SPECTRUM GSE never:
- Adds gates
- Removes gates
- Reorders operations
- Changes circuit structure

This is enforced and verified by CI.

### 4. No Optimization
SPECTRUM GSE does not:
- Minimize objectives
- Maximize fidelity
- Search parameter spaces
- Improve performance metrics

Refusal is preferred over degradation.

## Scope Limits

### 1. Per-Run Operation
SPECTRUM GSE operates on individual runs.
It does not:
- Average ensembles
- Aggregate statistics
- Pool results
- Smooth distributions

Procedural history (Π) is preserved, not erased.

### 2. Post-Execution Only
SPECTRUM GSE validates after execution.
It does not:
- Control hardware
- Execute circuits
- Schedule jobs
- Interface with QPUs

It is a post-processing stability layer.

### 3. Distribution-Based Interface
SPECTRUM GSE operates on probability distributions.
It does not:
- Parse circuit syntax
- Understand gate semantics
- Reason about quantum operators
- Perform symbolic manipulation

## Behavioral Freeze

SPECTRUM GSE v1.0 is **behaviorally frozen**.

This means:
- No new modes will be added
- Thresholds will not be tuned
- Logic will not be modified
- Only bug fixes and documentation updates permitted

Only derivative extensions (new tools built on top) are allowed.

## Falsification Conditions

SPECTRUM GSE is falsified if:
1. Scalar mode is accepted outside admissibility surface
2. Topology is mutated
3. Learning behavior is detected
4. Procedural history (Π) is averaged away
5. Refusal logic is bypassed

See `docs/CLAIM_BOUNDARY.md` for full falsification criteria.

## What This Means for Users

- Do not expect SPECTRUM GSE to "improve" over time
- Do not expect hyperparameter tuning
- Do not expect new features in v1.x
- Do expect stability, reproducibility, and auditability

This is a scientific instrument, not a product with a roadmap.
