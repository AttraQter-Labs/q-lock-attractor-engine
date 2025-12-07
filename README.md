# Q-LOCK ATTRACTOR ENGINE  
**AttraQtor Labs LLC — Identity-Locked Quantum Circuit Stabilization**

> Deterministic, identity-locked perturbations that preserve circuit intent while stabilizing behavior under noise and compilation drift.

---

## 1. What This Is

The **Q-LOCK Attractor Engine** is a **pre-processing layer** for quantum circuits:

- It ingests a user’s **identity string** and a **QASM / QuantumCircuit**.
- It computes a **high-dimensional latent vector** from that identity.
- It applies a **tiny, structured perturbation** to rotation gates in the circuit.
- The perturbation is:
  - **Deterministic** for a given identity and circuit.
  - **Invertible at the logical level** (no change of algorithmic intent).
  - **Statistically stable** under compilation, layout changes, and moderate noise.

In plain language:

> You get a circuit that “looks and behaves” like your original,  
> but carries a **hidden, identity-locked signature** and often shows  
> **more stable output distributions** across runs and backends.

---

## 2. Why Enterprises Care

### 2.1 Deterministic Identity Locking

Each run is tagged by a **cryptographic identity hash** (derived from your identity string).  

This gives:

- **Provenance**: who generated/authorized a circuit.
- **Auditability**: internal teams can trace circuits back to origin.
- **Non-repudiation flavor**: two different identities almost surely produce different locked circuits.

No quantum keys, no classical tokens — just the identity string and the attractor logic.

---

### 2.2 Distribution-Preserving Perturbations

The engine is explicitly designed so that:

- On simulators with no noise, the **ideal output distribution** is effectively unchanged.
- Under realistic noise models (depolarizing / thermal relaxation), small tests often show:
  - **More stable histograms** across repeated runs.
  - Less variability when changing compilation settings.

This is **not** magic error correction. It is a **deterministic, structured “jitter” layer** that reshapes how the circuit sits in the noise landscape, without altering its logic.

---

### 2.3 Real Hardware Evidence (Earlier Versions)

Earlier internal versions of the attractor logic were tested on:

- **IBM Quantum hardware** (e.g., Perth, Brisbane, Toronto)
- High-depth circuits including:
  - GHZ chains
  - Entangling ladders
  - Parameterized rotation networks

Results consistently showed:

- **High agreement between locked and ideal distributions**, and
- **Stable behavior** across repeated shots and layout rewrites.

The current engine maintains the same conceptual architecture, with a more modular, enterprise-ready implementation.

> 📊 See `/benchmarks/` and the README “Hardware Benchmarks” section (once populated)  
>   for example histograms and real hardware runs.

---

## 3. High-Level Architecture

At a high level, the engine does this:

1. **Identity Encoding**
   - Take an arbitrary string, e.g.
     - `"alice@example.com"`
     - `"Team-A-Production-Key"`
     - `"Prof. Einstein"`
   - Hash it with a cryptographic hash (e.g., SHA-256).
   - Expand and normalize into a **high-dimensional real vector**.

2. **Latent-Space Attractor**
   - Map that vector into a very high-dimensional latent space (e.g. 60k+ dimensions).
   - Apply a **structured, unitary-based attractor iteration**:
     - Golden-ratio inspired phase structure.
     - Controlled contraction towards a stable fixed point.
   - The result is a **deterministic “identity signature vector”**.

3. **Circuit Feature Extraction**
   - Parse the circuit (QASM2 or `QuantumCircuit`) and extract:
     - Rotation angles (from `rx`, `ry`, `rz`, parameterized gates).
     - Gate counts / structural features (fallback path).
   - Normalize these into a feature vector.

4. **Fusion & Perturbation**
   - Fuse circuit features with the identity signature vector.
   - Compute a **small per-gate perturbation** for rotation angles.
   - Produce a **locked circuit**:
     - Algorithmically equivalent.
     - Identity-tagged implicitly.
     - Ready for simulation or hardware execution.

---

## 4. Current Public Capabilities

The public Q-LOCK engine in this repository provides:

- ✅ **Identity string input** (via CLI or notebook)
- ✅ **QASM 2.0 circuit intake**
- ✅ Optional **Qiskit `QuantumCircuit` intake**
- ✅ **Locked circuit output** in `QuantumCircuit` form
- ✅ **QASM2 export** of the locked circuit
- ✅ Optional **local simulation** (QASM simulator) for:
  - Counts histograms
  - Baseline distribution comparisons

The **core attractor logic** used to compute the identity perturbations is kept proprietary by AttraQtor Labs LLC and **not exposed in this repository**.

---

## 5. Quickstart

### 5.1 Requirements

Python 3.10+ recommended.

Install base dependencies:

```bash
pip install qiskit qiskit-aer numpy
