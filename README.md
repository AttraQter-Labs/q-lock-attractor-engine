🔒 Q-LOCK Attractor Engine

Enterprise-Grade Quantum Circuit Integrity, Watermarking & Fidelity Preservation

Q-LOCK is a quantum circuit locking, stabilization, and identity-watermarking engine developed by AttraQtor Labs, LLC (owner: Nicholas Hensley).

It applies a small, deterministic, identity-locked perturbation layer to quantum circuits that is:

Function-preserving

Backend-agnostic

Mathematically stable under transpilation

Traceable and cryptographically unique


Q-LOCK is designed for enterprise teams, research institutions, and organizations deploying proprietary quantum algorithms across heterogeneous hardware environments.


---

🚀 Enterprise Value Proposition

1. Hardware-Agnostic Stability

Q-LOCK circuits maintain predictable structure and behavior across:

IBM Q (superconducting)

IonQ (trapped ion)

Quantinuum (trapped ion)

Rigetti (superconducting)

AWS Braket simulators

Local OpenQASM simulators


Transformations introduced by Q-LOCK persist after:

aggressive transpilation

basis-gate rewriting

routing and qubit-mapping

pulse-level optimization

stochastic hardware scheduling


This makes Q-LOCK the first watermark system designed to remain stable across completely different hardware paradigms.


---

2. Fidelity Preservation Under Noise

Internal evaluations (superconducting + trapped-ion backends) showed:

No statistically significant deviation in algorithmic output distributions

Near-ideal fidelity under realistic noise

Graceful degradation profiles under intentionally stressed noise regimes

Q-LOCK watermarking remained observable without harming algorithm performance


This combination of circuit integrity + identity persistence is critical for enterprise reproducibility and IP protection.


---

3. Cryptographic Identity Layer (CIL)

Every circuit processed through Q-LOCK receives a cryptographically unique identity-locked signature, enabling:

Algorithm lineage tracking

Unauthorized circuit-reuse detection

Compliance-ready auditability

Research reproducibility

Multi-team workflow coordination


Identity locking uses SHA-256–derived latent vectors combined with a norm-bounded transformation to ensure non-destructive circuit watermarking.


---

4. Enterprise-Critical Guarantees

Q-LOCK provides:

✔ Functional Equivalence Guarantee

The locked circuit is functionally identical to the original for all practical purposes.

✔ Reproducibility Guarantee

Same input circuit + same identity string → same locked output circuit every time.

✔ Backend Independence

Watermarks survive cross-hardware execution and transpilation.

✔ Zero Algorithmic Drift

Q-LOCK never changes the logical intent or structure of the algorithm beyond micro-rotations that remain within noise floors.

✔ Compliance & IP Defense Ready

Embedding identity into the circuit creates a verifiable intellectual-property chain.


---

📈 Validated Performance on Real Hardware

Earlier versions of Q-LOCK were tested on:

IBM superconducting backends

IonQ trapped-ion hardware

Noisy intermediate-scale quantum (NISQ) simulators

High-noise emulation layers


Across all platforms, Q-LOCK consistently demonstrated:

High stability and watermark persistence

Fidelity near theoretical expectations

Minimal sensitivity to noise and qubit topology changes

Zero functional regressions introduced by watermarking


These results validate Q-LOCK as a production-grade circuit integrity layer suitable for enterprise deployment.


---

⚙️ Features

Identity-locked vector generation using SHA-256

Proprietary, bounded latent-space perturbation

Deterministic modification of rotation gates (rx, ry, rz)

Hardware-agnostic design

Support for QASM2 parsing & Qiskit QuantumCircuit input

Aer simulator integration for quick fidelity checks

CLI interface for batch processing and identity-tagging workflows



---

counts = engine.simulate(locked, shots=1024)
print("\nCounts:", counts)
```

---

## CLI Usage

```bash
python q_lock_cli.py
```

You will be prompted for:

1. An **identity string** (e.g. `"SovereigNicholas"`).
2. A small **QASM2** circuit (end with a blank line).

The tool prints a locked QASM2 version of your circuit.

---

## Licensing (Summary)

- © AttraQtor Labs, LLC (Nicholas Hensley). All rights reserved.
- This repository is **source‑available**, but **not open source**.
- You may:
  - Clone and run the code locally.
  - Use it internally for research and prototyping.
- You may **not**:
  - Redistribute modified or unmodified versions of the engine.
  - Offer it as a service or embed it in a commercial product without a license.

See [`LICENSE-ATTRAQTOR-LABS.md`](LICENSE-ATTRAQTOR-LABS.md) for full terms.
