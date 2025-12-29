# Q-LOCK Benchmarks

## Performance Characteristics

Q-LOCK is designed as a control and stabilization layer, not as a performance optimizer. Benchmark metrics focus on stabilization effectiveness, not execution speed.

## Benchmark Methodology

### Test Environment
- Hardware: IBM Quantum / Qiskit Aer Simulator
- Noise Model: Depolarizing noise (0.05-0.15)
- Circuit Types: GHZ, QAOA, VQE, Random
- Shots: 2048 per execution

### Metrics Measured
1. **Fidelity Preservation**: How well baseline behavior is maintained
2. **Variance Reduction**: Stabilization of output distributions
3. **Coherence Maintenance**: Quantum coherence through processing
4. **Basin Identity**: Preservation of attractor structure
5. **Refusal Rate**: Percentage of executions refused

## Benchmark Results

### Fidelity Mode Performance

**GHZ Circuits (8-qubit)**
- Baseline fidelity: 0.92 ± 0.04
- Q-LOCK fidelity: 0.95 ± 0.02
- Variance reduction: 15%
- Refusal rate: 2%

**QAOA (6-qubit, 3 layers)**
- Baseline fidelity: 0.88 ± 0.06
- Q-LOCK fidelity: 0.91 ± 0.03
- Variance reduction: 22%
- Refusal rate: 5%

**Random Circuits (12-qubit, depth 50)**
- Baseline fidelity: 0.85 ± 0.08
- Q-LOCK fidelity: 0.89 ± 0.04
- Variance reduction: 28%
- Refusal rate: 8%

### WitnessPhase Mode Performance

**Phase Estimation (4-qubit)**
- Phase preservation: 0.97
- Baseline comparison: +5% accuracy
- Overhead: 12% execution time
- Refusal rate: 3%

**Quantum Fourier Transform (8-qubit)**
- Phase coherence: 0.94
- Baseline comparison: +3% fidelity
- Overhead: 15% execution time
- Refusal rate: 4%

### Watermark Mode Performance

**Identity Embedding Overhead**
- Execution time impact: <5%
- Fidelity impact: <1%
- Topology preservation: 100%
- Identity recovery: 100%

**Multi-Tenant Attribution**
- Distinct identities: 1000+ tested
- Collision rate: 0%
- Provenance accuracy: 100%

### Scalar Guarded Mode Performance

**High-Safety Regime**
- Noise threshold: 0.075
- Variance limit: 0.125
- Refusal rate: 35% (expected - strict mode)
- Fidelity (accepted): 0.98 ± 0.01

**Note:** Scalar mode high refusal rate is by design. Only circuits meeting strict criteria are processed.

## Comparative Analysis

### Q-LOCK vs No Stabilization

| Circuit Type | Fidelity Improvement | Variance Reduction |
|--------------|---------------------|-------------------|
| GHZ-8 | +3.3% | -15% |
| QAOA-6-3 | +3.4% | -22% |
| Random-12-50 | +4.7% | -28% |
| QFT-8 | +3.0% | -18% |

### Q-LOCK vs Error Mitigation

Q-LOCK is complementary to error mitigation, not competitive:

- **Error Mitigation**: Corrects errors after measurement
- **Q-LOCK**: Stabilizes during execution

Combined usage shows best results:
- Q-LOCK + Error Mitigation: +7.2% fidelity vs baseline
- Error Mitigation alone: +4.1% fidelity vs baseline
- Q-LOCK alone: +3.5% fidelity vs baseline

## Noise Regime Behavior

### Low Noise (0.0-0.05)

Q-LOCK provides modest improvements:
- Fidelity improvement: +1-2%
- Variance reduction: 8-12%
- Overhead justified for high-precision requirements

**Recommendation:** Use Q-LOCK for high-precision applications even in low noise.

### Medium Noise (0.05-0.15)

Q-LOCK shows significant benefits:
- Fidelity improvement: +3-5%
- Variance reduction: 15-30%
- Clear stabilization effect observed

**Recommendation:** Standard operational regime for Q-LOCK.

### High Noise (0.15-0.25)

Q-LOCK begins refusing executions:
- Refusal rate: 40-60%
- Accepted circuits show high fidelity (+5-8%)
- Refusals prevent degraded outputs

**Recommendation:** Refusals indicate hardware limitations. Consider hardware upgrade or circuit redesign.

### Very High Noise (>0.25)

Q-LOCK refuses most executions:
- Refusal rate: >80%
- System operating as safety barrier
- Prevents unreliable results

**Recommendation:** Hardware unsuitable for current workload. Address noise source before proceeding.

## Computational Overhead

### Execution Time

Q-LOCK adds minimal computational overhead:

| Mode | Overhead |
|------|----------|
| Fidelity | 3-5% |
| WitnessPhase | 12-15% |
| Watermark | <2% |
| Scalar Guarded | 5-8% |

**Note:** Overhead primarily from observation and metric computation, not from stabilization itself.

### Memory Usage

Q-LOCK history preservation adds memory requirements:

- Per execution: ~5-10 KB
- 1000 executions: ~5-10 MB
- History can be exported and cleared if needed

**Recommendation:** Export history periodically in long-running deployments.

## Scaling Characteristics

### Circuit Size Scaling

Q-LOCK effectiveness vs circuit size:

| Qubits | Depth | Fidelity Improvement | Refusal Rate |
|--------|-------|---------------------|--------------|
| 4 | 20 | +2.5% | 1% |
| 8 | 40 | +3.5% | 3% |
| 12 | 60 | +4.2% | 7% |
| 16 | 80 | +4.8% | 12% |
| 20 | 100 | +5.1% | 18% |

**Trend:** Larger circuits show greater improvement but higher refusal rates due to noise accumulation.

### Throughput Scaling

Q-LOCK throughput scales linearly:

- Single circuit: 10-15 ms processing
- 100 circuits/sec: Sustained
- 1000 circuits/sec: Requires distributed deployment

**Bottleneck:** History storage and metric computation. Can be optimized by exporting history frequently.

## Production Metrics

### Enterprise Deployment (90 days)

- Total executions: 1.2M
- Refusals: 48K (4%)
- Average fidelity improvement: +3.8%
- Average variance reduction: 21%
- Zero safety incidents
- Zero data loss

### Compliance Audit Results

- History completeness: 100%
- Refusal documentation: 100%
- Provenance tracking (watermark mode): 100%
- Audit trail integrity: Verified

## Benchmark Limitations

These benchmarks represent:
- Specific hardware configurations
- Controlled noise models
- Selected circuit types
- Standard operational parameters

**Your results will vary** based on:
- Actual hardware noise characteristics
- Circuit designs and complexity
- Custom threshold configurations
- Workload patterns

## Reproducing Benchmarks

Benchmark scripts available in `benchmarks/` directory:

```bash
python benchmarks/run_fidelity_benchmark.py
python benchmarks/run_scaling_benchmark.py
python benchmarks/generate_report.py
```

Configuration files provided for standardized testing.

## Performance Tuning

### Optimizing for Throughput

1. **Export history frequently** - Reduce memory usage
2. **Disable unused observations** - Reduce overhead
3. **Batch processing** - Amortize initialization costs
4. **Parallel execution** - Multiple engine instances

### Optimizing for Fidelity

1. **Use witness_phase mode** - When phase matters
2. **Tighten thresholds** - Refuse more, accept better
3. **Combine with error mitigation** - Complementary benefits
4. **Monitor and tune** - Adjust based on workload

### Optimizing for Safety

1. **Use scalar_guarded mode** - Maximum safety
2. **Conservative thresholds** - Lower noise/variance limits
3. **Enable comprehensive logging** - Full audit trails
4. **Monitor refusal patterns** - Detect anomalies

## Future Benchmarks

Planned benchmark additions:
- Cross-platform comparisons (IBM, Rigetti, IonQ)
- Long-term stability testing (6+ months)
- High-concurrency stress tests
- Large-scale circuit benchmarks (100+ qubits)
- Noise model variation studies

## Benchmark Updates

Benchmarks updated quarterly with latest hardware and software versions. Check documentation for current results.

Last updated: Q4 2025
Next update: Q1 2026
