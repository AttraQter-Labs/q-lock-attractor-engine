# Q-LOCK Modes Reference

## Overview

Q-LOCK provides four operational modes, each designed for specific use cases. Mode selection determines the stabilization strategy and safety constraints applied to quantum circuits.

## Mode Comparison

| Feature | Fidelity | WitnessPhase | Watermark | Scalar Guarded |
|---------|----------|--------------|-----------|----------------|
| **Primary Use** | Standard stabilization | Phase-critical circuits | Identity tracking | Maximum safety |
| **Fidelity Preservation** | High | High | High | Highest |
| **Phase Tracking** | No | Yes | No | Yes |
| **Identity Locking** | No | No | Yes | No |
| **Noise Threshold** | 0.15 | 0.15 | 0.15 | 0.075 |
| **Requires Opt-in** | No | No | No | Yes |
| **Auto-enable** | Yes | Yes | Yes | Never |

## Fidelity Mode

**Purpose:** Primary operational mode for general-purpose quantum circuit stabilization.

**Characteristics:**
- Optimizes for high fidelity to baseline behavior
- Preserves basin identity
- Minimizes distributional drift
- Standard noise/variance thresholds

**When to Use:**
- Standard quantum algorithms
- General circuit stabilization
- Low to moderate noise environments
- Default choice for most applications

**Configuration:**
```python
from qlock import QLockEngine, QLockConfig

config = QLockConfig(mode="fidelity")
engine = QLockEngine(config)
result = engine.execute(circuit)
```

**Metrics Tracked:**
- Coherence preservation
- Entropy
- Variance
- KL divergence
- Fidelity score

## WitnessPhase Mode

**Purpose:** Phase-aware stabilization for circuits where quantum phase is critical.

**Characteristics:**
- Tracks phase evolution throughout execution
- Preserves phase coherence
- Phase-sensitive attractor stabilization
- Standard noise/variance thresholds

**When to Use:**
- Quantum algorithms relying on phase relationships
- Interference-based computations
- Phase estimation algorithms
- Circuits with critical superposition states

**Configuration:**
```python
config = QLockConfig(mode="witness_phase")
engine = QLockEngine(config)
result = engine.execute(circuit)
```

**Metrics Tracked:**
- Phase coherence
- Standard fidelity metrics
- Phase drift measures

**Notes:**
- Phase tracking adds observational overhead
- Use only when phase information is essential
- Compatible with standard error correction

## Watermark Mode

**Purpose:** Identity-locking and provenance tracking without circuit modification.

**Characteristics:**
- Embeds deterministic identity signatures
- No topology changes
- Preserves circuit logic completely
- Cryptographic identity binding

**When to Use:**
- Circuit attribution required
- Provenance tracking needed
- IP protection scenarios
- Audit trail requirements
- Multi-tenant environments

**Configuration:**
```python
config = QLockConfig(mode="watermark", identity="enterprise-id-2025")
engine = QLockEngine(config)
result = engine.execute(circuit)
```

**Metrics Tracked:**
- Identity fingerprint
- Topology preservation verification
- Standard fidelity metrics

**Important:**
- Requires identity string in configuration
- Does NOT optimize circuit
- Does NOT modify circuit behavior
- Purely for tracking and attribution

## Scalar Guarded Mode

**Purpose:** Maximum safety mode with explicit refusal under strict constraints.

**Characteristics:**
- Requires explicit opt-in confirmation
- Operates at 50% of standard thresholds
- Hard refusal outside narrow boundaries
- Never auto-enables
- Strictest operational regime

**When to Use:**
- Safety-critical applications
- Regulated environments
- High-compliance requirements
- Known-safe operational regimes only
- Experimental validation

**Configuration:**
```python
config = QLockConfig(
    mode="scalar_guarded",
    noise_threshold=0.075,  # Half of standard
    variance_limit=0.125     # Half of standard
)
engine = QLockEngine(config)

# Must explicitly confirm in parameters
result = engine.execute(
    circuit,
    params={"scalar_mode_confirmed": True}
)
```

**Additional Constraints:**
- Noise must be < 0.075 (vs 0.15 standard)
- Variance must be < 0.125 (vs 0.25 standard)
- Temperature parameter limited to ≤ 1.5
- Explicit confirmation required
- Will refuse if any constraint violated

**When Mode Refuses:**
- Missing `scalar_mode_confirmed=True` in params
- Noise exceeds strict threshold
- Variance exceeds strict limit
- Temperature > 1.5
- Any standard guard check fails

**Metrics Tracked:**
- All standard metrics
- Safety check results
- Refusal reasons (if rejected)

## Mode Selection Guidelines

### Choose Fidelity Mode If:
- General quantum algorithm execution
- Standard operational requirements
- No special phase or identity requirements
- Default choice

### Choose WitnessPhase Mode If:
- Phase relationships are critical
- Interference patterns must be preserved
- Phase estimation is performed
- Superposition phase matters

### Choose Watermark Mode If:
- Circuit attribution needed
- IP protection required
- Audit trails mandatory
- Multi-tenant environment
- Provenance tracking essential

### Choose Scalar Guarded Mode If:
- Safety is paramount
- Regulatory compliance required
- Known-safe regime operation only
- Experimental validation phase
- Minimum risk tolerance

## Switching Modes

Modes can be changed between executions:

```python
engine = QLockEngine(QLockConfig(mode="fidelity"))

# Execute in fidelity mode
result1 = engine.execute(circuit1)

# Switch to witness_phase mode
engine.config.mode = "witness_phase"
result2 = engine.execute(circuit2)
```

**Note:** Switching modes resets observer and history. Use separate engine instances for concurrent multi-mode operation.

## Mode Refusal Handling

All modes can refuse execution. Check results:

```python
result = engine.execute(circuit, params)

if not result.success:
    print(f"Refused: {result.refusal_reason}")
    print(f"Verdict: {result.verdict}")
else:
    print(f"Success: {result.metrics}")
```

## Best Practices

1. **Start with Fidelity Mode** - Default choice for most use cases
2. **Add WitnessPhase Only When Needed** - Phase tracking has overhead
3. **Use Watermark for Tracking** - Not for optimization
4. **Reserve Scalar Guarded for Safety-Critical** - Strictest mode
5. **Handle Refusals Gracefully** - Check result.success before proceeding
6. **Review History** - Use engine.get_history() for audit trails
