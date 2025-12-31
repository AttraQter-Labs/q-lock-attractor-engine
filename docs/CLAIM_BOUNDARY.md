# SPECTRUM GSE v1.0 — Claim Boundary Document

## Purpose

This document establishes the **explicit claim boundary** for SPECTRUM GSE v1.0.

It serves as both a legal protection and scientific integrity document,
clearly stating what SPECTRUM GSE does, does not do, and cannot do.

## What SPECTRUM GSE Does

### 1. Basin-Preserving Stabilization
- Pulls computational states into stable attractor basins
- Reduces noise-driven variance while preserving signal structure
- Operates deterministically on per-run basis (not ensemble)

### 2. Topology Preservation
- **NEVER** modifies circuit structure, equations, or execution semantics
- Preserves distribution topology (no topological mutations)
- Maintains unitarity and causality

### 3. Procedural History (Π) Preservation
- Treats procedural history as first-class variable
- **NEVER** averages away Π-divergence
- Recognizes that identical equations ≠ identical outcomes

### 4. Refusal-Based Safety
- **EXPLICITLY REFUSES** operations outside admissible bounds
- Scalar mode disabled by default policy
- No silent degradation (refusals are logged and visible)

### 5. Exploratory Hypothesis Generation (Explorer Engine)
- Enumerates procedural variants without constraint
- Generates hypothesis space for validation
- Operates WITHOUT refusals (by design)

### 6. Validation & Falsification (Validator Engine)
- Validates procedural variants against invariants
- Refuses unsafe transformations
- Stabilizes accepted variants

## What SPECTRUM GSE Does NOT Do

### 1. NOT an Optimizer
- **Does NOT** chase maxima or minimize objectives
- **Does NOT** perform gradient descent or parameter tuning
- **Does NOT** optimize gate counts, depth, or performance metrics

### 2. NOT Error Correction
- **Does NOT** implement QEC codes (surface codes, topological codes, etc.)
- **Does NOT** perform syndrome detection or correction
- **Does NOT** encode logical qubits

### 3. NOT a Compiler
- **Does NOT** transpile circuits to hardware gates
- **Does NOT** perform circuit rewriting or optimization passes
- **Does NOT** map to specific hardware topologies

### 4. NOT a Simulator
- **Does NOT** execute circuits or predict outcomes
- **Does NOT** compute probability distributions via simulation
- **Does NOT** provide expectation values or measurement results

### 5. NOT a Predictive Model
- **Does NOT** use machine learning or statistical inference
- **Does NOT** train on data or adapt parameters
- **Does NOT** make probabilistic predictions

### 6. NOT Probabilistic Smoothing
- **Does NOT** perform ensemble averaging
- **Does NOT** apply statistical noise reduction
- **Does NOT** assume ensemble equivalence

## What is Refused By Design

### 1. Scalar Mode (Experimental)
Scalar mode is **REFUSED** unless ALL of the following conditions hold:
- `noise ≤ 0.003` (SCALAR_NOISE_LIMIT)
- `phase_dispersion ≤ 0.2` (SCALAR_PHASE_LIMIT)
- `procedural_disorder ≤ 0.4` (SCALAR_PI_LIMIT)
- `topology != "high"`

**Reason**: Scalar mode is powerful but dangerous. Hard refusal prevents misuse.

### 2. Topology Mutation
Any operation that would modify circuit structure is **REFUSED**.

**Reason**: Topology preservation is a foundational invariant.

### 3. Learning or Adaptation
Any operation involving parameter learning or adaptation is **REFUSED**.

**Reason**: Deterministic behavior is required for scientific reproducibility.

### 4. Silent Degradation
Any operation that would degrade a circuit without explicit notice is **REFUSED**.

**Reason**: Silent degradation is scientifically dishonest.

## What Falsifies the Engine

SPECTRUM GSE is **falsified** if any of the following occur:

### 1. Topology Mutation Detected
- If `topology_mutation = true` appears in any report
- If circuit structure is modified
- If distribution topology is altered

### 2. Learning Observed
- If non-deterministic behavior is detected
- If parameters adapt based on input
- If ensemble averaging occurs

### 3. Scalar Mode Bypass
- If scalar mode executes without ALL admissibility conditions met
- If refusal thresholds are ignored or bypassed

### 4. Basin Identity Violation
- If stabilization moves state to different attractor basin
- If procedural identity is not preserved

### 5. Procedural History Erasure
- If Π-divergence is averaged away
- If procedural history is treated as noise
- If identical equations produce identical outcomes (violates Π preservation)

## What Cannot Be Improved by Parameter Tuning

### Hard Limits (No Tunability)

1. **Variance Reduction**
   - Cannot reduce variance below noise floor
   - Cannot violate Shannon entropy bounds
   - Cannot create information

2. **Fidelity Preservation**
   - Cannot exceed physical constraints
   - Cannot violate unitarity
   - Cannot break causality

3. **Refusal Thresholds**
   - Scalar noise limit (0.003) is **HARD-CODED**
   - Scalar phase limit (0.2) is **HARD-CODED**
   - Scalar Π limit (0.4) is **HARD-CODED**
   - These are **NOT** tunable parameters

4. **Topology Immutability**
   - NO parameter can enable topology mutation
   - This is a **DESIGN INVARIANT**, not a tunable property

5. **Learning Prohibition**
   - NO parameter can enable learning
   - This is a **DESIGN INVARIANT**, not a configuration option

### Why These Limits Exist

These limits are **NOT** implementation bugs or optimization opportunities.
They are **intentional design boundaries** that preserve:
- Scientific reproducibility
- Falsifiability
- Explicit refusal over silent failure
- Procedural history integrity

## Legal & Scientific Protection

### Disclaimers

1. **No Performance Guarantees**
   - SPECTRUM GSE does NOT guarantee performance improvement
   - Results depend on noise characteristics and procedural context
   - NOT all circuits benefit from stabilization

2. **No Physical Advantage Claims**
   - SPECTRUM GSE does NOT claim to violate physical laws
   - Does NOT claim to create information or break entropy bounds
   - Does NOT claim to exceed theoretical limits

3. **No Liability for Misuse**
   - SPECTRUM GSE provides refusal-based safety
   - Users must respect refusal verdicts
   - Bypassing refusals voids all guarantees

### Use Case Boundaries

#### ✓ Appropriate Use Cases
- Noise-robust basin preservation
- Repeatability analysis across hardware runs
- Noise-stratified benchmarking
- Procedural divergence diagnosis
- Identity-locked quantum pipelines

#### ✗ Inappropriate Use Cases
- Circuit optimization (use a compiler)
- Error correction (use QEC codes)
- Performance tuning (use an optimizer)
- Outcome prediction (use a simulator)
- Parameter learning (use machine learning)

## Intellectual Property Notice

SPECTRUM GSE v1.0 includes original research concepts:
- Basin-preserving stabilization without topology mutation
- Procedural history (Π) as first-class variable
- Explorer-Validator epistemic dual architecture
- Refusal-based safety without silent degradation

No patents claimed. Open methodology.

## Version Freeze Statement

**SPECTRUM GSE v1.0 is behaviorally frozen.**

- NO learning will be added
- NO optimization will be added
- NO topology mutation will be permitted
- ONLY derivative extensions permitted

Core invariants are **IMMUTABLE**.

## Contact & Dispute Resolution

For questions about claim boundaries, falsification conditions, or appropriate use cases:
- See docs/FAQ.md for common questions
- See docs/FAILURE_MODES.md for known limitations
- See proofs/canonical_proof_run.md for verification evidence

**Last Updated**: 2025-12-31
**Version**: 1.0.0
**Status**: CANONICAL FREEZE
