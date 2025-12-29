# Q-LOCK

**Attractor-Based Coherence Stabilization and Safety Engine**

Q-LOCK is a production-ready control, stabilization, and refusal layer for quantum circuits and high-noise computational systems.

## What This Is

Q-LOCK is:
- **A control layer** - Sits between user code and quantum hardware
- **A stabilization engine** - Preserves basin identity and improves fidelity
- **A refusal system** - Explicitly refuses unsafe operations
- **A provenance tracker** - Maintains complete procedural history (Π)

Q-LOCK is **NOT**:
- An optimizer
- Error correction
- A simulator
- A noise mitigation protocol

## Core Value

- **Preserves basin identity** - Circuits maintain their algorithmic intent
- **Improves fidelity and variance** - Modest but consistent improvements in low-noise regimes
- **Explicitly refuses harmful contractions** - Safety-first design with hard boundaries
- **Preserves procedural history (Π)** - Never erases operational provenance

## Quick Start

### Installation

```bash
pip install -e .
```

### Basic Usage

```python
from qlock import QLockEngine

# Initialize engine with desired mode
engine = QLockEngine(mode="fidelity")

# Process a quantum circuit
result = engine.process(circuit, identity="alice@example.com")

if result["status"] == "accepted":
    stabilized_circuit = result["circuit"]
    metrics = result["metrics"]
else:
    refusal_reason = result["verdict"]
```

### Available Modes

- **fidelity** - Primary mode for high-fidelity stabilization
- **witness_phase** - Phase-coherent stabilization with verification
- **watermark** - Identity locking only, no topology changes
- **scalar_guarded** - Strict boundary enforcement (never auto-enables)

## Benchmarks

| Metric | Without Q-LOCK | With Q-LOCK | Improvement |
|--------|----------------|-------------|-------------|
| Fidelity (4-qubit GHZ) | 0.947 | 0.989 | +4.4% |
| Variance | 0.023 | 0.008 | -65% |
| Coherence | 0.912 | 0.971 | +6.5% |

Results on low-noise regimes. High-noise circuits are explicitly refused by guard system.

See [docs/benchmarks.md](docs/benchmarks.md) for detailed results.

## Architecture

```
User Application
       ↓
  Q-LOCK Engine
  ├── Guards (safety checks)
  ├── Modes (stabilization strategies)
  ├── Metrics (performance tracking)
  └── History (provenance)
       ↓
Quantum Compiler
       ↓
  Hardware Backend
```

See [docs/architecture.md](docs/architecture.md) for system design.

## Safety Guarantees

Q-LOCK explicitly refuses operations rather than failing silently:

- **Noise Guard** - Refuses circuits above noise threshold (default: 0.15)
- **Scalar Guard** - Enforces hard boundaries in scalar mode
- **History Preservation** - Records all acceptances and refusals
- **Basin Preservation** - Maintains circuit identity and intent

See [docs/safety.md](docs/safety.md) for safety design.

## Documentation

- [Architecture](docs/architecture.md) - System design and components
- [Modes](docs/modes.md) - Operating mode descriptions
- [Safety](docs/safety.md) - Safety guarantees and refusal logic
- [Benchmarks](docs/benchmarks.md) - Performance results
- [Industry Positioning](docs/industry_positioning.md) - Why customers buy Q-LOCK

## Examples

See [examples/basic_usage.py](examples/basic_usage.py) for complete usage examples.

## Testing

```bash
pytest tests/
```

## Industry Use Cases

### Enterprise Quantum Teams
- Compliance and audit readiness
- Risk mitigation
- Production stability

### Quantum Service Providers
- Multi-tenant identity tracking
- Per-customer provenance
- Safety guarantees

### Research with Compliance Requirements
- Grant compliance
- Data integrity
- Reproducibility

See [docs/industry_positioning.md](docs/industry_positioning.md) for competitive differentiation.

## What Competitors Cannot Claim

Unlike error correction, optimizers, or noise mitigation:
- Q-LOCK preserves exact circuit intent
- Maintains complete procedural history
- Explicitly refuses unsafe operations
- Provides deterministic identity locking

## License

See [LICENSE](LICENSE) for licensing terms.

Core attractor logic is proprietary to AttraQtor Labs LLC.

## Contact

**AttraQtor Labs LLC**

- Website: https://AttraQtorLabs.com
- GitHub: https://github.com/AttraQter-Labs
- Email: nic_hensley@proton.me

## Contributing

This is a production repository. For enterprise licensing and integration inquiries, contact us directly.
