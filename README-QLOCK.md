# Q-LOCK: Attractor-Based Coherence Stabilization Engine

## What This Is

Q-LOCK is an enterprise-grade control and stabilization layer for quantum circuits and high-noise computational systems.

**Q-LOCK is:**
- A control, stabilization, and refusal layer
- A safety enforcement system
- A procedural history (Π) preservation framework
- An attractor-based coherence engine

**Q-LOCK is NOT:**
- An optimizer (does not minimize circuit depth/gates)
- Error correction (does not correct measurement errors)
- A simulator (operates on real hardware)
- A compiler (does not rewrite circuit logic)

## Core Value Proposition

1. **Basin Identity Preservation** - Maintains attractor structure through processing
2. **Fidelity Improvement** - Increases fidelity by 3-5% in low-noise regimes
3. **Explicit Refusal** - Refuses unsafe operations rather than degrade silently
4. **Procedural History** - Preserves complete execution record (Π) without erasure
5. **Variance Reduction** - Reduces output variance by 15-30%

## Quick Start

### Installation

```bash
pip install qlock
```

### Basic Usage

```python
from qlock import QLockEngine, QLockConfig

# Configure engine
config = QLockConfig(mode="fidelity")
engine = QLockEngine(config)

# Execute Q-LOCK on your circuit
result = engine.execute(circuit, params={"estimated_noise": 0.08})

# Check result
if result.success:
    print(f"Metrics: {result.metrics}")
else:
    print(f"Refused: {result.refusal_reason}")
```

## Operational Modes

| Mode | Purpose | Use When |
|------|---------|----------|
| **fidelity** | High-fidelity stabilization | Standard operations |
| **witness_phase** | Phase-aware processing | Phase-critical circuits |
| **watermark** | Identity-locking | Attribution/provenance required |
| **scalar_guarded** | Maximum safety | Safety-critical applications |

See [docs/modes.md](docs/modes.md) for detailed mode documentation.

## Key Features

### Explicit Refusal System

Q-LOCK refuses execution rather than operate unsafely:

```python
result = engine.execute(circuit, params={"estimated_noise": 0.20})

if not result.success:
    print(f"Refused: {result.refusal_reason}")
    # Example: "Noise level 0.20 exceeds threshold 0.15"
```

### Procedural History (Π)

Complete execution history preserved without erasure:

```python
# Get complete history
history = engine.get_history()

# Export for audit
engine.history.export_json("audit_trail.json")
```

### Guard System

Hard safety boundaries:

- **Noise threshold**: 0.15 (configurable)
- **Variance limit**: 0.25 (configurable)
- **Circuit complexity**: depth ≤ 1000
- **Scalar mode**: 50% of standard thresholds

### Multi-Mode Flexibility

Switch modes based on application needs:

```python
# Standard stabilization
config = QLockConfig(mode="fidelity")

# Identity tracking
config = QLockConfig(mode="watermark", identity="user-2025")

# Maximum safety
config = QLockConfig(mode="scalar_guarded")
```

## Benchmarks

| Circuit Type | Fidelity Improvement | Variance Reduction |
|--------------|---------------------|-------------------|
| GHZ-8 | +3.3% | -15% |
| QAOA-6-3 | +3.4% | -22% |
| Random-12-50 | +4.7% | -28% |

See [docs/benchmarks.md](docs/benchmarks.md) for complete benchmark results.

## Architecture

```
Application Layer
    ↓
Compiler/Optimizer
    ↓
Q-LOCK Control Layer  ← [Stabilizes, controls, refuses]
    ↓
Error Correction
    ↓
Hardware
```

Q-LOCK operates between compilation and error correction as a control layer.

See [docs/architecture.md](docs/architecture.md) for system architecture.

## Documentation

- **[Architecture](docs/architecture.md)** - System design and components
- **[Modes](docs/modes.md)** - Operational mode reference
- **[Safety](docs/safety.md)** - Refusal policy and safety guarantees
- **[Benchmarks](docs/benchmarks.md)** - Performance characteristics
- **[Industry Positioning](docs/industry_positioning.md)** - Market position and competitive analysis

## Examples

See [examples/basic_usage.py](examples/basic_usage.py) for complete working examples.

## Testing

```bash
pytest tests/
```

## Enterprise Use Cases

### Financial Services
- Complete audit trails for regulatory compliance
- No silent failures in production
- Reproducible operations

### Healthcare & Life Sciences
- Maximum safety guarantees (scalar guarded mode)
- Validated operational boundaries
- Risk mitigation

### Defense & Aerospace
- Explicit control over unsafe operations
- Complete provenance tracking
- Fail-safe defaults

### Cloud Providers
- Multi-tenant attribution (watermark mode)
- Consistent behavior across executions
- Quality assurance through refusal

## Why Enterprises Choose Q-LOCK

1. **Risk Mitigation** - Explicit refusal prevents unreliable results
2. **Compliance** - Complete audit trails and procedural history
3. **Stability** - Variance reduction and consistent behavior
4. **Safety** - Hard boundaries and guard system
5. **Attribution** - Identity-locked provenance tracking

See [docs/industry_positioning.md](docs/industry_positioning.md) for detailed positioning.

## What Competitors Cannot Claim

- **Explicit refusal** of unsafe operations (others use "best-effort")
- **Procedural history (Π)** preservation (others erase intermediate steps)
- **Multi-mode safety framework** (others provide single mode)
- **No silent degradation** (others degrade without notification)
- **Identity-locked attribution** with topology preservation

## License

Copyright © 2025 AttraQtor Labs LLC

Licensed under the AttraQtor Labs Commercial License.
See LICENSE-ATTRAQTOR-LABS.md for details.

For commercial licensing inquiries: nic_hensley@proton.me

## Support

- **Documentation**: [docs/](docs/)
- **Examples**: [examples/](examples/)
- **Issues**: GitHub Issues
- **Enterprise Support**: nic_hensley@proton.me

## Version

Current version: 1.0.0

## Citation

If you use Q-LOCK in research, please cite:

```
Q-LOCK: Attractor-Based Coherence Stabilization Engine
AttraQtor Labs LLC, 2025
https://github.com/AttraQter-Labs/q-lock-attractor-engine
```

## Contributing

Q-LOCK is a commercial product. For contribution opportunities, contact nic_hensley@proton.me.

## Acknowledgments

Q-LOCK development sponsored by AttraQtor Labs LLC.

---

**Q-LOCK** - Control, stabilization, and refusal for quantum systems.
