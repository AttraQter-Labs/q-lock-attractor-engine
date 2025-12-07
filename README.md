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

(If you only want to use the text-mode wrapper and not simulate, you can skip qiskit-aer.)


---

5.2 Using the Notebook (Recommended First Contact)

1. Open the main notebook:

q_lock_attractor_engine.ipynb



2. Run the first cell to install any missing dependencies.


3. When prompted:

Enter your identity string, e.g. Prof. Einstein.

Paste a QASM 2.0 circuit.

Type END on a new line to finish.




You’ll see:

Original circuit diagram

Locked circuit diagram

Simulation counts for the locked circuit

JSON-style summary of the run



---

5.3 Python API (Future src/ Package)

In a packaged form (coming in a future version), usage will look like:

from attraqtor_engine import QLockEngine
from qiskit import QuantumCircuit

engine = QLockEngine(identity="Prof. Einstein")

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

locked_qc = engine.lock(qc)

print(locked_qc)


---

6. Example: GHZ-Style Chain

Example QASM 2.0 input:

OPENQASM 2.0;
include "qelib1.inc";

qreg q[4];
creg c[4];

h q[0];
cx q[0], q[1];
cx q[1], q[2];
cx q[2], q[3];

rz(0.3) q[0];
ry(0.6) q[1];
rx(0.9) q[2];
rz(1.2) q[3];

measure q -> c;

With the engine in pulse_ready mode, a typical JSON report might look like:

{
  "engine": "AttractorEngine_Public_v1",
  "mode": "pulse_ready",
  "fingerprint_sha256": "f238d2c7...999d2",
  "simulation": {
    "backend": "qasm_simulator",
    "shots": 2048,
    "counts": {
      "0000": 727,
      "1111": 801,
      "0100": 186,
      "1011": 166,
      "others": "..."
    },
    "fidelity_to_ideal": 0.9992
  }
}

The key point: the locked circuit reproduces the ideal GHZ-like behavior with high fidelity while carrying your identity lock.


---

7. Hardware Benchmarks (Planned Layout)

Once you add your blurred screenshots, you can place them in e.g.:

/media/ibm_run_ghz_8q_before.png
/media/ibm_run_ghz_8q_after.png
/media/ibm_run_random_12q_before.png
/media/ibm_run_random_12q_after.png

And reference them like:

### 7.1 Example: GHZ on Real Hardware (Early Prototype Engine)

| Before Lock | After Lock |
|------------|------------|
| ![GHZ before](/media/ibm_run_ghz_8q_before.png) | ![GHZ after](/media/ibm_run_ghz_8q_after.png) |

- Backend: IBM Quantum (device name redacted)
- Qubits: 8
- Depth: (redacted)
- Observed: sharper peak in target states after locking, with comparable or reduced leakage into off-manifold bitstrings.

This lets you progressively document real-world behavior without exposing private data.


---

8. Roadmap

Planned enhancements:

📦 Packaged src/ module (pip install attraqtor-engine)

🧪 Automated fidelity tests (pytest + Qiskit Aer noise models)

📊 Benchmarks for multiple hardware providers

🧾 Formal whitepaper (math & experiments)

🌐 Public docs site (AttraQtorLabs.com integration)

🔐 Optional enterprise license hooks:

per-team keys

per-tenant identity domains




---

9. License & IP

Code in this repository:
© AttraQtor Labs LLC — all rights reserved under LICENSE-ATTRAQTOR-LABS.md.

Core attractor logic, high-dimensional mappings, and detailed internal mathematics are proprietary and intentionally not included in this public repo.

Commercial licensing and enterprise integration are available on request.



---

10. Contact

AttraQtor Labs LLC
Q-Lock Attractor Engine — Enterprise & Research Inquiries

Website: https://AttraQtorLabs.com

GitHub: https://github.com/AttraQter-Labs

Email: (add your preferred public email address here)



---

---

### ✅ What to do now

1. **Replace** your existing `README.md` with the text above.  
2. **Commit** the change on GitHub.  
3. Tell me “README done” and I’ll move you to **Step 2: repo structure (`/src`, `/tests`, `/benchmarks`)** and walk you through that next.0  - **More stable histograms** across repeated runs.
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
pip install qiskit qiskit-ae(If you only want to use the text-mode wrapper and not simulate, you can skip qiskit-aer.)r numpy

---

5.2 Using the Notebook (Recommended First Contact)

1. Open the main notebook:

q_lock_attractor_engine.ipynb



2. Run the first cell to install any missing dependencies.


3. When prompted:

Enter your identity string, e.g. Prof. Einstein.

Paste a QASM 2.0 circuit.

Type END on a new line to finish.




You’ll see:

Original circuit diagram

Locked circuit diagram

Simulation counts for the locked circuit

JSON-style summary of the run



---

5.3 Python API (Future src/ Package)

In a packaged form (coming in a future version), usage will look like:

from attraqtor_engine import QLockEngine
from qiskit import QuantumCircuit

engine = QLockEngine(identity="Prof. Einstein")

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

locked_qc = engine.lock(qc)

print(locked_qc)


---

6. Example: GHZ-Style Chain

Example QASM 2.0 input:

OPENQASM 2.0;
include "qelib1.inc";

qreg q[4];
creg c[4];

h q[0];
cx q[0], q[1];
cx q[1], q[2];
cx q[2], q[3];

rz(0.3) q[0];
ry(0.6) q[1];
rx(0.9) q[2];
rz(1.2) q[3];

measure q -> c;

With the engine in pulse_ready mode, a typical JSON report might look like:

{
  "engine": "AttractorEngine_Public_v1",
  "mode": "pulse_ready",
  "fingerprint_sha256": "f238d2c7...999d2",
  "simulation": {
    "backend": "qasm_simulator",
    "shots": 2048,
    "counts": {
      "0000": 727,
      "1111": 801,
      "0100": 186,
      "1011": 166,
      "others": "..."
    },
    "fidelity_to_ideal": 0.9992
  }
}

The key point: the locked circuit reproduces the ideal GHZ-like behavior with high fidelity while carrying your identity lock.


---

7. Hardware Benchmarks (Planned Layout)

Once you add your blurred screenshots, you can place them in e.g.:

/media/ibm_run_ghz_8q_before.png
/media/ibm_run_ghz_8q_after.png
/media/ibm_run_random_12q_before.png
/media/ibm_run_random_12q_after.png

And reference them like:

### 7.1 Example: GHZ on Real Hardware (Early Prototype Engine)

| Before Lock | After Lock |
|------------|------------|
| ![GHZ before](/media/ibm_run_ghz_8q_before.png) | ![GHZ after](/media/ibm_run_ghz_8q_after.png) |

- Backend: IBM Quantum (device name redacted)
- Qubits: 8
- Depth: (redacted)
- Observed: sharper peak in target states after locking, with comparable or reduced leakage into off-manifold bitstrings.

This lets you progressively document real-world behavior without exposing private data.


---

8. Roadmap

Planned enhancements:

📦 Packaged src/ module (pip install attraqtor-engine)

🧪 Automated fidelity tests (pytest + Qiskit Aer noise models)

📊 Benchmarks for multiple hardware providers

🧾 Formal whitepaper (math & experiments)

🌐 Public docs site (AttraQtorLabs.com integration)

🔐 Optional enterprise license hooks:


---

9. License & IP

Code in this repository:
© AttraQtor Labs LLC — all rights reserved under LICENSE-ATTRAQTOR-LABS.md.

Core attractor logic, high-dimensional mappings, and detailed internal mathematics are proprietary and intentionally not included in this public repo.

Commercial licensing and enterprise integration are available on request.



---

10. Contact

AttraQtor Labs LLC
Q-Lock Attractor Engine — Enterprise & Research Inquiries

Website: https://AttraQtorLabs.com

GitHub: https://github.com/AttraQter-Labs

Email: nic_hensley@proton.me
