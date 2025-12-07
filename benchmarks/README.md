# Q-LOCK Benchmarks & Real-Hardware Evidence

This directory collects **reproducible benchmarks** and **real IBM Quantum
hardware runs** that were used to validate the Q-LOCK attractor engine.

## Contents

- `hardware_summary.md` – high-level summary of all hardware runs.
- `ibm_torino_*.png` – anonymized screenshots from IBM Quantum jobs
  (histograms + circuit diagrams).
- `sim_vs_hw_comparison.md` – comparison between Aer simulations and real
  hardware behaviour for the same circuits.

> **Note**  
> All screenshots are **heavily redacted** to remove any personal identifiers
> or IBM workspace metadata. Only the quantum-relevant parts  
> (backend name, histogram, circuit diagram) are kept.

## Reproducing the experiments

All experiments follow this pattern:

1. Prepare a reference circuit (e.g. GHZ-style or deep RX/RY/RZ ladder).
2. Run once **without Q-LOCK** on a noisy backend.
3. Run again **with Q-LOCK** applied using the public engine API.
4. Compare:
   - output distribution (KL-divergence vs. ideal),
   - state fidelity (when simulated),
   - stability across repeated runs.

The corresponding Python scripts will be added here in future revisions so
anyone with access to IBM Quantum can re-run the tests.
