# Q-LOCK Attractor Engine

**Q-LOCK** is a quantum circuit *locking* and watermarking engine developed by **AttraQtor Labs, LLC** (owner: Nicholas Hensley).

It applies a **small, deterministic, identity‑locked perturbation** to quantum circuits so that:

- Circuits remain functionally equivalent for practical purposes.
- Each circuit carries a microscopic, cryptographic *scar* linked to a specific identity string.
- The locking is hardware‑agnostic and backend‑independent (Qiskit‑based reference implementation).

> This repository contains the **public reference engine**. The full EMLP / golden‑lattice internals used by AttraQtor Labs remain private.

---

## Features

- Identity‑locked latent vector using SHA‑256.
- Proprietary latent‑space transform (opaque, non‑trivial, norm‑bounded).
- Deterministic modification of rotation gates (`rx`, `ry`, `rz`) at the 1% level (configurable).
- Qiskit / Aer simulator integration for quick testing.
- Simple CLI driver (`q_lock_cli.py`) for interactive use.

---

## Quickstart (Python)

```bash
pip install qiskit qiskit-aer numpy
```

```python
from qiskit import QuantumCircuit
from qlock_engine import QLockAttractorEngine

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.rz(0.5, 0)

engine = QLockAttractorEngine("SovereigNicholas")
locked = engine.lock(qc)

print("Original:")
print(qc)
print("\nLocked:")
print(locked)

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
