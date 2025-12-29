# Q-LOCK Safety & Refusal Policy

## Safety Philosophy

Q-LOCK prioritizes explicit safety over implicit optimization. The engine will refuse execution rather than operate in unsafe regimes.

## Core Safety Principles

1. **Explicit Refusal Over Silent Failure**
   - Operations that cannot be safely performed are refused with clear reasons
   - No silent degradation or unpredictable behavior

2. **Conservative Operational Boundaries**
   - Noise and variance thresholds set below degradation points
   - Scalar mode operates at 50% of standard thresholds

3. **No Auto-Enable of Risky Modes**
   - Scalar guarded mode requires explicit confirmation
   - Safety-critical parameters cannot be bypassed

4. **Complete Audit Trails**
   - All refusals logged with detailed reasons
   - Procedural history (Π) preserved for analysis

5. **Fail-Safe Defaults**
   - Missing parameters trigger safe defaults or refusal
   - Unknown configurations refused rather than guessed

## Guard System

### Standard Guards

Applied to all modes except scalar_guarded:

**Noise Threshold: 0.15**
- Estimated noise must be ≤ 0.15
- Exceeding triggers refusal
- Rationale: Above 0.15, coherence preservation degrades significantly

**Variance Limit: 0.25**
- Estimated variance must be ≤ 0.25
- Exceeding triggers refusal
- Rationale: High variance indicates unstable distributions

**Circuit Complexity: depth ≤ 1000**
- Circuit depth must not exceed 1000 gates
- Exceeding triggers refusal
- Rationale: Complexity impacts stabilization effectiveness

### Scalar Mode Guards

Applied ONLY to scalar_guarded mode (in addition to standard guards):

**Strict Noise Threshold: 0.075**
- Half of standard threshold
- No exceptions

**Strict Variance Limit: 0.125**
- Half of standard limit
- No exceptions

**Temperature Limit: ≤ 1.5**
- Parameter-specific safety bound
- Prevents thermal degradation

**Explicit Confirmation Required**
- Must provide `scalar_mode_confirmed=True` in params
- No auto-enable, no defaults

## Refusal Scenarios

### Noise Exceeded

**Condition:**
```python
estimated_noise > noise_threshold
```

**Refusal Message:**
```
"Noise level 0.18 exceeds threshold 0.15"
```

**Resolution:**
- Reduce circuit depth
- Use error mitigation
- Switch to lower-noise hardware
- Adjust Q-LOCK thresholds (if justified)

### Variance Exceeded

**Condition:**
```python
estimated_variance > variance_limit
```

**Refusal Message:**
```
"Variance 0.30 exceeds limit 0.25"
```

**Resolution:**
- Stabilize input parameters
- Reduce measurement variance
- Use variance reduction techniques
- Review circuit design

### Circuit Complexity

**Condition:**
```python
circuit.depth() > 1000
```

**Refusal Message:**
```
"Circuit depth 1200 exceeds maximum supported depth (1000)"
```

**Resolution:**
- Decompose circuit into smaller sections
- Apply circuit optimization before Q-LOCK
- Use iterative processing
- Verify depth is required

### Scalar Mode Not Confirmed

**Condition:**
```python
mode == "scalar_guarded" and not params.get("scalar_mode_confirmed")
```

**Refusal Message:**
```
"Scalar mode requires explicit confirmation (scalar_mode_confirmed=True)"
```

**Resolution:**
- Add confirmation to parameters: `{"scalar_mode_confirmed": True}`
- Verify scalar mode is truly required
- Consider using standard fidelity mode instead

### Temperature Unsafe

**Condition:**
```python
params.get("temperature") > 1.5
```

**Refusal Message:**
```
"Temperature parameter exceeds scalar mode safety limit (1.5)"
```

**Resolution:**
- Reduce temperature parameter
- Verify temperature setting is intentional
- Use non-scalar mode if temperature must be high

### Missing Identity (Watermark Mode)

**Condition:**
```python
mode == "watermark" and identity is None
```

**Refusal Message:**
```
"Identity required for watermark mode"
```

**Resolution:**
- Provide identity in configuration: `QLockConfig(mode="watermark", identity="...")`
- Use different mode if identity not needed

## Handling Refusals

### Check Result Status

Always check execution results:

```python
result = engine.execute(circuit, params)

if not result.success:
    print(f"Execution refused: {result.refusal_reason}")
    # Handle refusal appropriately
else:
    # Proceed with successful result
    process_metrics(result.metrics)
```

### Refusal Response Strategies

**1. Parameter Adjustment**
```python
# Attempt 1: Refused due to noise
result = engine.execute(circuit, {"estimated_noise": 0.18})

# Attempt 2: Adjust parameters
result = engine.execute(circuit, {"estimated_noise": 0.12})
```

**2. Circuit Modification**
```python
# Refused due to depth
if not result.success and "depth" in result.refusal_reason:
    # Decompose circuit
    sub_circuits = decompose(circuit)
    results = [engine.execute(sc) for sc in sub_circuits]
```

**3. Mode Change**
```python
# Refused in scalar mode
if result.verdict == "REFUSED":
    # Switch to standard fidelity mode
    engine.config.mode = "fidelity"
    result = engine.execute(circuit)
```

**4. Threshold Adjustment**
```python
# Adjust thresholds if justified
engine.guards.update_thresholds(
    noise_threshold=0.18,
    variance_limit=0.30
)
```

### Logging Refusals

Maintain refusal logs for analysis:

```python
refusal_log = []

result = engine.execute(circuit, params)
if not result.success:
    refusal_log.append({
        "timestamp": datetime.now(),
        "reason": result.refusal_reason,
        "verdict": result.verdict,
        "mode": result.mode
    })
```

## Safety in Production

### Pre-Deployment Validation

Before production deployment:

1. **Test refusal boundaries** with synthetic circuits
2. **Validate threshold settings** for your hardware
3. **Establish fallback strategies** for refusals
4. **Set up monitoring** for refusal rates
5. **Document operational procedures** for handling refusals

### Monitoring Refusal Rates

Track refusal statistics:

```python
total_executions = 0
refusals = 0

for circuit in workload:
    total_executions += 1
    result = engine.execute(circuit)
    if not result.success:
        refusals += 1

refusal_rate = refusals / total_executions
print(f"Refusal rate: {refusal_rate:.2%}")
```

**Acceptable refusal rates:**
- Development: 10-20% (expected during tuning)
- Staging: 5-10% (acceptable during validation)
- Production: <5% (target for stable operation)

**High refusal rates indicate:**
- Thresholds too conservative for workload
- Hardware noisier than expected
- Circuit designs need optimization
- Mode selection inappropriate

### Compliance and Audit

Q-LOCK's refusal system supports compliance:

**Audit Trail:**
- All refusals logged in procedural history (Π)
- Reasons captured with timestamps
- Complete execution record maintained

**Reporting:**
```python
# Export refusal history
history = engine.get_history()
refused = [h for h in history if h["verdict"] == "REFUSED"]

# Generate compliance report
report = {
    "total_executions": len(history),
    "refusals": len(refused),
    "refusal_reasons": [h["refusal_reason"] for h in refused]
}
```

## Customizing Safety Parameters

### When to Adjust Thresholds

Adjust only when:
- Hardware characteristics well-understood
- Empirical data supports adjustment
- Risk tolerance explicitly defined
- Regulatory compliance maintained

### How to Adjust

```python
# Create custom configuration
config = QLockConfig(
    mode="fidelity",
    noise_threshold=0.12,  # Stricter
    variance_limit=0.20,    # Stricter
    enable_refusal=True
)

engine = QLockEngine(config)
```

**Warning:** Loosening thresholds reduces safety guarantees. Document justification and obtain appropriate approvals.

## Emergency Procedures

### Disabling Refusal (Not Recommended)

Only for emergency debugging:

```python
config = QLockConfig(
    mode="fidelity",
    enable_refusal=False  # UNSAFE - for debugging only
)
```

**WARNING:** Disabling refusal removes safety protections. Use only in isolated testing environments.

### Safe Mode Recovery

If system experiencing excessive refusals:

1. **Enable strict mode** with conservative thresholds
2. **Switch to fidelity mode** (most permissive)
3. **Disable scalar operations** temporarily
4. **Review and adjust** workload parameters
5. **Gradually relax** constraints after validation

## Best Practices

1. **Default to refusal-enabled** - Safety first
2. **Monitor refusal rates** - Track trends
3. **Investigate refusals** - Don't ignore
4. **Document adjustments** - Maintain records
5. **Test boundaries** - Know your limits
6. **Maintain audit trails** - Preserve history (Π)
7. **Plan for refusals** - Build fallback strategies
