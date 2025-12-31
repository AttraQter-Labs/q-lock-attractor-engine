# When NOT to Use SPECTRUM GSE

SPECTRUM GSE is not appropriate when:

## 1. You Need Optimization
SPECTRUM GSE does not:
- Minimize cost functions
- Maximize fidelity
- Search parameter spaces
- Learn from data

If you need optimization, use dedicated optimizers.

## 2. You Need Error Correction
SPECTRUM GSE does not:
- Decode syndromes
- Apply correction gates
- Implement QEC codes
- Repair corrupted states

If you need QEC, use error correction frameworks.

## 3. You Need Compilation
SPECTRUM GSE does not:
- Transpile circuits
- Map to hardware topologies
- Route qubits
- Decompose gates

If you need compilation, use quantum compilers.

## 4. You Want Predictive Modeling
SPECTRUM GSE does not:
- Train models
- Predict outcomes
- Fit parameters
- Extrapolate trends

If you need prediction, use machine learning or statistical methods.

## 5. You Want Ensemble Methods
SPECTRUM GSE operates per-run, not per-ensemble.
It preserves procedural history (Π) rather than averaging it away.

If you need ensemble averaging, use statistical post-processing.

## 6. You Have Well-Behaved Systems
If your system is:
- Already stable
- Procedurally invariant
- Free of hidden assumptions
- Reproducible across runs

Then SPECTRUM GSE will validate this (good!), but may not provide additional value.

## Summary
SPECTRUM GSE is a diagnostic and validation tool.
It is not a substitute for:
- Domain expertise
- Theoretical analysis
- Standard quantum tooling
- Statistical methods
