# Basin/Concentration Mode - Implementation Summary

## Overview

Added a new CLI mode `basin` to measure bias preservation and attractor stability, complementary to the existing `fidelity` mode. This addresses the request for Krystal scheduling-aligned metrics.

## Implementation Details

### New CLI Command

```bash
python q_lock_cli.py basin \
    --circuit examples/test_circuit.qasm \
    --identity "your-identity" \
    --shots 2048 \
    --output-dir ./runs/basin_demo
```

### Metrics Implemented

1. **Octave-binned probability mass** (log2 rank bins)
   - Bins states by their rank into octaves (2^0, 2^1, 2^2, etc.)
   - Measures how probability mass is distributed across rank bins
   - Function: `octave_binned_mass(counts, num_octaves=5)`

2. **Top-k mass** (k=1, 3, 5, 10)
   - Measures concentration in top-k most probable states
   - Higher values indicate more concentrated distributions
   - Function: `top_k_mass(counts, k)`

3. **Effective support** (1/sum p²)
   - Inverse participation ratio
   - Measures the effective number of states contributing to the distribution
   - Higher values = more uniform, lower values = more concentrated
   - Function: `effective_support(counts)`

4. **Gini coefficient**
   - Standard inequality measure (0 = perfect equality, 1 = maximum inequality)
   - Adapted from economics to measure distribution concentration
   - Function: `gini_coefficient(counts)`

### Visualization

Four-panel plot generated automatically:

1. **Octave Spectrum** - Probability mass by log2 rank bins
2. **CDF** - Cumulative distribution comparison (baseline vs locked)
3. **Lorenz Curve** - Inequality visualization with perfect equality line
4. **Top-k Mass** - Bar chart comparing concentration in top states

All plots compare baseline (no watermark) vs locked (watermarked) circuits.

### Output Format

**JSON Structure:**
```json
{
  "mode": "basin",
  "timestamp": "2025-12-27T03:11:37.060298",
  "identity": "basin-demo-user",
  "shots": 2048,
  "metrics": {
    "baseline": {
      "octave_binned_mass": {"0": 0.479, "1": 0.496, ...},
      "top_k_mass": {"1": 0.479, "3": 0.975, "5": 1.0, "10": 1.0},
      "effective_support": 2.22,
      "gini_coefficient": 0.450
    },
    "locked": {
      "octave_binned_mass": {"0": 0.473, "1": 0.499, ...},
      "top_k_mass": {"1": 0.473, "3": 0.972, "5": 1.0, "10": 1.0},
      "effective_support": 2.29,
      "gini_coefficient": 0.438
    }
  }
}
```

**Plot saved as:** `basin_plots_YYYYMMDD_HHMMSS.png`

### Integration with Compare Mode

The `compare` command now includes basin results:

```bash
python q_lock_cli.py compare --output-dir ./runs/basin_demo
```

Output displays:
- Basin metrics for baseline circuit
- Basin metrics for locked circuit
- Side-by-side comparison

## Design Philosophy

### Complementary to Fidelity Mode

- **Fidelity mode** measures distribution distance (TVD, KL divergence, Hellinger)
  - Answers: "How different are the distributions?"
  
- **Basin mode** measures bias preservation (concentration, support, inequality)
  - Answers: "How concentrated is the distribution? Is the attractor stable?"

### Krystal Scheduling Alignment

Basin metrics align with Krystal scheduling by:
- Measuring attractor stability through concentration metrics
- Quantifying bias preservation across baseline/locked runs
- Providing complementary view to distribution distance

## Testing

All tests pass:
```
✅ tests/test_import_engine.py::test_import PASSED
✅ tests/test_smoke.py::test_readme_exists PASSED  
✅ tests/test_smoke.py::test_core_dependencies_import PASSED
```

Basin mode tested with:
```bash
./test_basin_mode.sh
```

Output verified:
- ✅ JSON metrics correctly calculated
- ✅ Plots generated with 4 panels
- ✅ Compare mode includes basin results
- ✅ All metrics mathematically valid

## Sample Results

```
Baseline:
  Top-1 mass:         0.4790
  Top-5 mass:         1.0000
  Effective support:  2.22
  Gini coefficient:   0.4502

Locked:
  Top-1 mass:         0.4727
  Top-5 mass:         1.0000
  Effective support:  2.29
  Gini coefficient:   0.4377

Interpretation:
  • Higher top-k mass = more concentrated distribution
  • Higher effective support = more uniform distribution
  • Higher Gini = more inequality/concentration
```

## Files Modified

- `q_lock_cli.py` - Added basin metrics functions and cmd_basin()
- `test_basin_mode.sh` - Test script for basin mode

## No Breaking Changes

- Existing modes (baseline, watermark, fidelity, compare) unchanged
- Basin mode is purely additive
- All existing tests pass
- Backward compatible

## Commit

- Commit hash: `927abdc`
- Message: "Add basin/concentration mode for attractor stability metrics"
