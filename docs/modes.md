# Q-LOCK Operational Modes

## Overview

Q-LOCK provides four distinct operational modes, each suited for different stabilization requirements and risk profiles.

## Mode Selection

Modes are selected at engine initialization:

```python
engine = QLockEngine(mode="fidelity")
```

**Mode selection is explicit. No mode auto-enables.**

## Fidelity Mode

**Purpose**: High-fidelity stabilization with basin preservation

**Use Cases**:
- Production quantum circuits
- Circuits requiring maximum fidelity to ideal distributions
- General-purpose stabilization

**Characteristics**:
- Primary stabilization mode
- Balances fidelity with noise resilience
- Suitable for most applications

**Guarantees**:
- Preserves algorithmic intent
- Maintains basin identity
- High fidelity to ideal output distributions

## Witness Phase Mode

**Purpose**: Phase-coherent stabilization with witness verification

**Use Cases**:
- Phase-sensitive quantum algorithms
- Interference-based protocols
- Coherence-critical applications

**Characteristics**:
- Preserves phase relationships
- Includes witness-based verification
- Optimized for coherence

**Guarantees**:
- Phase coherence maintained
- Witness verification of transformations
- Basin identity preserved

## Watermark Mode

**Purpose**: Identity locking only, no topology changes

**Use Cases**:
- Circuit provenance tracking
- Authentication and non-repudiation
- Minimal intervention requirements

**Characteristics**:
- **No gate additions or removals**
- **No topology modifications**
- Embeds identity signature only

**Guarantees**:
- Exact topology preservation
- Deterministic identity embedding
- Minimal perturbation

## Scalar Guarded Mode

**Purpose**: Strict boundary enforcement for safety-critical scenarios

**Use Cases**:
- Safety-critical applications
- Risk-averse deployments
- Bounded optimization problems

**Characteristics**:
- **Explicit hard boundaries**
- **Never auto-enables**
- **Refuses operations outside safe ranges**

**Boundaries**:
- Scalar values: [0.01, 0.99]
- Circuit depth: < 100 gates
- Parameter count: < 50 parameters

**Refusal Conditions**:
- Scalar values outside bounds → REFUSED
- Circuit depth exceeds limit → REFUSED
- Parameter count exceeds limit → REFUSED

**WARNING**: This mode is restrictive by design. Only use when strict safety guarantees are required.

## Mode Comparison

| Feature | Fidelity | Witness Phase | Watermark | Scalar Guarded |
|---------|----------|---------------|-----------|----------------|
| Topology Changes | Yes | Yes | No | Yes |
| Primary Use | General | Phase-sensitive | Provenance | Safety-critical |
| Restrictiveness | Moderate | Moderate | Minimal | High |
| Auto-enable | No | No | No | **Never** |

## Mode Selection Guidelines

**Choose Fidelity Mode when**:
- General-purpose stabilization needed
- Balanced approach desired
- No specific constraints

**Choose Witness Phase Mode when**:
- Phase coherence is critical
- Interference effects matter
- Quantum algorithms rely on phase

**Choose Watermark Mode when**:
- Only identity tracking needed
- Circuit must remain unchanged
- Minimal intervention required

**Choose Scalar Guarded Mode when**:
- Safety is paramount
- Operating in bounded regime
- Explicit refusal preferred over silent failure

## Switching Modes

Modes cannot be changed dynamically. To switch modes, create a new engine instance:

```python
fidelity_engine = QLockEngine(mode="fidelity")
watermark_engine = QLockEngine(mode="watermark")
```

This design ensures mode isolation and prevents unintended mode transitions.
