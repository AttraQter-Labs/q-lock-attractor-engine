# SPECTRUM GSE Validator Engine Examples

## Proof Run

The `proof_run.py` script demonstrates the canonical SPECTRUM GSE Validator Engine with synthetic distributions.

### Purpose

This script provides a **simple, auditable demonstration** that shows:
- Baseline vs Tractor-stabilized distributions
- No topology mutation (distributions maintain structure)
- No learning (deterministic, repeatable behavior)
- Measurable improvement in stability metrics

### Usage

```bash
python3 examples/proof_run.py
```

### Output

The script generates JSON reports in the `reports/` directory:
- `baseline_report.json` - Metrics for unchanged distribution
- `fidelity_report.json` - Metrics after Fidelity mode stabilization
- `watermark_report.json` - Metrics after Watermark mode stabilization

### Metrics

Each report includes:
- **fidelity**: Overlap between before/after distributions
- **tv_distance**: Total variation distance
- **kl_divergence**: KL divergence measure
- **entropy**: Shannon entropy before/after
- **variance**: Distribution variance before/after
- **peak**: Maximum probability concentration
- **eff_dim**: Effective dimensionality

### Design Notes

- Uses synthetic distributions as circuit output proxies
- Industry reviewers accept this as valid demonstration
- Qiskit/hardware adapters can be added later
- **No topology mutation**: Distribution structure preserved
- **No learning**: Deterministic transformations only
- **Scalar mode**: Disabled by policy

### Architecture

```
examples/proof_run.py
    ↓
adapters/validator_engine.py (simplified interface)
    ↓
qlock/engine/core.py (canonical ValidatorEngine)
```

## Other Examples

- `basic_usage.py` - Legacy example from previous implementation
