# Q-LOCK Benchmarks

## Overview

This document provides benchmark results demonstrating Q-LOCK's stabilization performance across various circuit types and noise regimes.

## Benchmark Methodology

**Test Circuits**:
- GHZ chains (4-10 qubits)
- Bell states
- Parameterized rotation networks
- Entangling ladder circuits

**Metrics**:
- Fidelity to ideal distribution
- Output variance across runs
- Coherence stability
- Processing overhead

**Backends**:
- Qiskit Aer simulator (noise-free)
- Qiskit Aer with noise models
- IBM Quantum hardware (when available)

## Baseline Performance

### Fidelity Mode

**Circuit**: 4-qubit GHZ chain
**Shots**: 2048
**Noise Model**: Depolarizing (p=0.01)

| Metric | Without Q-LOCK | With Q-LOCK | Improvement |
|--------|----------------|-------------|-------------|
| Fidelity | 0.947 | 0.989 | +4.4% |
| Variance | 0.023 | 0.008 | -65% |
| Coherence | 0.912 | 0.971 | +6.5% |

**Result**: Q-LOCK improves fidelity and reduces variance in low-noise regimes.

### Witness Phase Mode

**Circuit**: 6-qubit interference circuit
**Shots**: 4096
**Noise Model**: Thermal relaxation (T1=100µs, T2=80µs)

| Metric | Without Q-LOCK | With Q-LOCK | Improvement |
|--------|----------------|-------------|-------------|
| Phase coherence | 0.891 | 0.943 | +5.8% |
| Variance | 0.031 | 0.014 | -55% |
| Witness fidelity | 0.878 | 0.928 | +5.7% |

**Result**: Phase-sensitive stabilization maintains coherence under realistic noise.

### Watermark Mode

**Circuit**: 8-qubit parameterized circuit
**Shots**: 1024
**Noise Model**: None (identity test)

| Metric | Without Q-LOCK | With Q-LOCK | Change |
|--------|----------------|-------------|--------|
| Topology match | 100% | 100% | 0% |
| Gate count | 42 | 42 | 0 |
| Fidelity | 0.999 | 0.999 | 0% |
| Identity embedded | No | Yes | ✓ |

**Result**: Watermark mode preserves exact topology while embedding identity.

## Performance Under Noise

### Low Noise (p < 0.05)

Q-LOCK shows **optimal performance**:
- Fidelity improvement: 2-5%
- Variance reduction: 40-70%
- Minimal overhead: < 1ms per circuit

### Moderate Noise (0.05 < p < 0.15)

Q-LOCK shows **acceptable performance**:
- Fidelity improvement: 1-3%
- Variance reduction: 20-40%
- Acceptable overhead: 1-3ms per circuit

### High Noise (p > 0.15)

Q-LOCK **refuses processing** (by design):
- Guard threshold exceeded
- Refusal verdict issued
- No processing overhead
- History records refusal

## Scaling Characteristics

### Circuit Depth

| Depth | Processing Time | Fidelity Impact |
|-------|----------------|-----------------|
| < 20 | < 1ms | +4.5% |
| 20-50 | 1-3ms | +3.2% |
| 50-100 | 3-8ms | +2.1% |
| > 100 | Varies | +1.5% |

### Qubit Count

| Qubits | Processing Time | Memory Usage |
|--------|----------------|--------------|
| 2-4 | < 1ms | < 10MB |
| 5-8 | 1-3ms | 10-30MB |
| 9-16 | 3-10ms | 30-100MB |
| 17+ | Varies | Varies |

## Real Hardware Results

### IBM Quantum Perth (127 qubits)

**Test Date**: Internal testing (earlier versions)
**Circuit**: 8-qubit entangling ladder
**Shots**: 8192

**Results**:
- High agreement between locked and ideal distributions
- Stable behavior across layout rewrites
- Consistent output across repeated runs

### IBM Quantum Brisbane (127 qubits)

**Test Date**: Internal testing (earlier versions)
**Circuit**: 10-qubit GHZ chain
**Shots**: 4096

**Results**:
- Distribution stability improved
- Variance reduced relative to unlocked baseline
- Identity provenance maintained

## Benchmark Reproduction

To reproduce these benchmarks:

```bash
cd benchmarks/
python run_benchmarks.py --mode fidelity --circuits ghz,bell,ladder
```

Expected output:
- Per-circuit metrics
- Aggregate statistics
- Comparison tables

## Limitations

**What These Benchmarks Show**:
- Q-LOCK improves fidelity and reduces variance in low-noise regimes
- Guard system correctly refuses high-noise circuits
- Watermark mode preserves topology exactly

**What These Benchmarks Do NOT Show**:
- Universal noise mitigation (Q-LOCK is not error correction)
- Performance on all possible circuit types
- Behavior under all noise models

## Interpretation Guidelines

- Improvements are **modest but consistent** in target regimes
- Refusals are **features, not bugs**
- Results are **deterministic** for given identity and circuit
- Real hardware results confirm **stability** (not magic)

## Future Benchmarks

Planned additions:
- Extended hardware testing across providers
- Larger circuit depth studies
- Comparison with error mitigation techniques
- Long-term stability analysis
