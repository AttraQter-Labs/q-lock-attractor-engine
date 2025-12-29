# Q-LOCK Safety Guarantees

## Core Safety Principles

Q-LOCK is designed as a safety-first control layer with explicit refusal mechanisms.

## Refusal Philosophy

**Q-LOCK refuses operations rather than failing silently.**

When guards detect unsafe conditions:
1. Processing stops immediately
2. Refusal verdict is issued with reason
3. Event is recorded in procedural history
4. No circuit transformation occurs

## Guard System

### Noise Guard

**Purpose**: Prevent processing in high-noise regimes

**Threshold**: Default 0.15 (configurable)

**Refusal Conditions**:
- Estimated circuit noise > threshold

**Rationale**: High noise compromises basin identity preservation. Refusing processing prevents harmful contractions.

### Scalar Guard

**Purpose**: Enforce hard boundaries for scalar mode

**Active Only In**: Scalar Guarded Mode

**Refusal Conditions**:
- Scalar value < 0.01 or > 0.99
- Circuit depth > 100
- Parameter count > 50
- Non-scalar circuit in scalar mode

**Rationale**: Scalar mode requires strict boundaries. Operations outside these boundaries risk instability.

## What Q-LOCK Does NOT Do

Q-LOCK is **not**:
- An error correction system
- A noise mitigation protocol
- A circuit optimizer
- A quantum simulator

Q-LOCK **is**:
- A control layer
- A stabilization engine
- A refusal system
- A provenance tracker

## Safety Boundaries

### Noise Thresholds

| Regime | Noise Level | Q-LOCK Action |
|--------|-------------|---------------|
| Low | < 0.05 | Accept (optimal) |
| Moderate | 0.05 - 0.15 | Accept (acceptable) |
| High | 0.15 - 0.30 | Refuse (threshold) |
| Extreme | > 0.30 | Refuse (dangerous) |

### Scalar Mode Boundaries

| Parameter | Safe Range | Action Outside |
|-----------|------------|----------------|
| Scalar value | [0.01, 0.99] | Refuse |
| Circuit depth | < 100 gates | Refuse |
| Parameter count | < 50 params | Refuse |

## History Preservation

**Critical Safety Feature**: Q-LOCK preserves procedural history (Π).

Unlike systems that erase operational history:
- All refusals are recorded
- All acceptances are recorded
- Identity provenance is maintained
- Audit trail is complete

This ensures:
- Non-repudiation
- Compliance readiness
- Post-incident analysis capability

## Basin Identity Preservation

Q-LOCK explicitly preserves basin identity:

**What This Means**:
- Circuits maintain their algorithmic intent
- Identity-locked signatures persist
- Distribution characteristics are stable

**Why This Matters**:
- Prevents harmful contractions
- Maintains circuit provenance
- Enables deterministic reproduction

## Configuration Safety

Guards can be configured, but **defaults are conservative**:

```python
config = {
    "noise_threshold": 0.15,  # Conservative default
}
engine = QLockEngine(mode="fidelity", config=config)
```

**Recommendation**: Use defaults unless specific requirements dictate otherwise.

## Refusal Handling

When a circuit is refused:

```python
result = engine.process(circuit, identity)

if result["status"] == "refused":
    reason = result["verdict"]
    # Handle refusal appropriately
    # Do NOT retry with relaxed constraints
    # Do NOT proceed with unprocessed circuit
```

**Best Practice**: Respect refusal verdicts. They indicate unsafe operating conditions.

## Safety vs. Performance

Q-LOCK prioritizes safety over performance:
- Refusal is acceptable
- Silent failure is not acceptable
- Explicit rejection > implicit degradation

## Compliance Considerations

Q-LOCK's explicit refusal and history preservation support:
- Audit requirements
- Regulatory compliance
- Risk management frameworks
- Post-deployment verification

## Risk Mitigation

Q-LOCK mitigates risks by:
1. **Refusing** unsafe operations (not attempting them)
2. **Recording** all decisions in history
3. **Preserving** basin identity (not corrupting it)
4. **Maintaining** procedural provenance (not erasing it)

This is enterprise-grade risk management, not research-grade experimentation.
