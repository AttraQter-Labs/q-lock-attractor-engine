"""
q_lock_engine.py

Core Q-LOCK Attractor Engine module.
Identity-locked, hardware-agnostic quantum circuit watermarking.
"""

from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from typing import Any, Dict, Optional

import numpy as np

try:
    from qiskit import QuantumCircuit, transpile
    from qiskit_aer import AerSimulator
    QISKIT_AVAILABLE = True
except Exception:  # pragma: no cover
    QuantumCircuit = Any  # type: ignore
    AerSimulator = Any    # type: ignore
    transpile = None      # type: ignore
    QISKIT_AVAILABLE = False


# ------------------------------------------------------------------
# Identity encoding
# ------------------------------------------------------------------

def identity_vector(identity: str, dim: int = 100_200) -> np.ndarray:
    """
    Encode an identity string into a deterministic, normalized real vector.

    The details of this embedding are part of AttraQtor Labs' proprietary
    attractor logic; the implementation here is intentionally simple,
    side‑effect‑free, and stable across platforms.
    """
    digest = hashlib.sha256(identity.encode("utf-8")).digest()
    base = np.frombuffer(digest, dtype=np.uint8).astype(np.float64) / 255.0

    if dim <= 0:
        raise ValueError("dim must be positive")

    reps = math.ceil(dim / base.size)
    tiled = np.tile(base, reps)[:dim]

    tiled -= tiled.mean()
    norm = np.linalg.norm(tiled)
    if norm == 0.0:
        return np.zeros(dim, dtype=np.float64)
    return tiled / norm


# ------------------------------------------------------------------
# Private latent transform (opaque attractor core)
# ------------------------------------------------------------------

def _latent_transform(v: np.ndarray) -> np.ndarray:
    """
    Proprietary latent-space transformation.

    Public guarantee:
        - deterministic
        - norm-bounded
        - invertibility or internal structure are *not* guaranteed and
          are intentionally obscured for IP protection.

    This is a lightweight stand‑in for the full EMLP + golden‑lattice
    engine used internally at AttraQtor Labs.
    """
    v = v.astype(np.float64)
    # Small non-linear squash + mixing that preserves scale on average
    w = np.tanh(0.12 * v)
    # Simple orthogonal-like mixing via FFT phase shuffle
    fft = np.fft.rfft(w)
    phases = np.exp(1j * np.linspace(0.0, 2.0 * math.pi, fft.size))
    mixed = np.fft.irfft(fft * phases, n=v.size).real
    mixed -= mixed.mean()
    n = np.linalg.norm(mixed)
    return mixed / n if n > 0 else mixed


# ------------------------------------------------------------------
# Public engine configuration and API
# ------------------------------------------------------------------

@dataclass
class QLockConfig:
    latent_dim: int = 100_200
    epsilon_angle: float = 0.01  # strength of angle perturbations


class QLockAttractorEngine:
    """
    Q-LOCK Attractor Engine

    • identity: stable observer / user / system identifier
    • config:  controls latent dimension and perturbation scale

    Public behavior:
        1. Extract a feature vector from the input circuit.
        2. Combine with identity embedding.
        3. Run through proprietary latent transform.
        4. Feed back into circuit as small, deterministic angle perturbations.
    """

    def __init__(self, identity: str, config: Optional[QLockConfig] = None):
        self.identity = identity
        self.config = config or QLockConfig()
        self._id_vec = identity_vector(identity, self.config.latent_dim)

    # --------------------- Circuit helpers ---------------------

    def _circuit_to_features(self, qc: "QuantumCircuit") -> np.ndarray:
        angles = []
        for inst_tuple in qc.data:
            inst = getattr(inst_tuple, "operation", inst_tuple[0])
            params = getattr(inst, "params", [])
            if params:
                try:
                    angles.append(float(params[0]))
                except Exception:
                    continue
        if not angles:
            # fallback: gate counts
            counts: Dict[str, int] = {}
            for inst_tuple in qc.data:
                inst = getattr(inst_tuple, "operation", inst_tuple[0])
                name = inst.name
                counts[name] = counts.get(name, 0) + 1
            angles = list(counts.values()) or [0.0]

        v = np.array(angles, dtype=np.float64)
        v -= v.mean()
        std = v.std()
        if std > 0:
            v /= std

        if v.size < self.config.latent_dim:
            reps = math.ceil(self.config.latent_dim / v.size)
            v = np.tile(v, reps)[: self.config.latent_dim]
        elif v.size > self.config.latent_dim:
            v = v[: self.config.latent_dim]
        return v

    def _apply_latent_to_circuit(self, qc: "QuantumCircuit", latent: np.ndarray) -> "QuantumCircuit":
        if not QISKIT_AVAILABLE:
            return qc

        eps = self.config.epsilon_angle
        out = qc.copy()
        real = latent.real
        n = real.size
        idx = 0
        new_data = []

        for inst_tuple in out.data:
            inst = getattr(inst_tuple, "operation", inst_tuple[0])
            qargs = getattr(inst_tuple, "qubits", inst_tuple[1] if len(inst_tuple) > 1 else [])
            cargs = getattr(inst_tuple, "clbits", inst_tuple[2] if len(inst_tuple) > 2 else [])
            name = inst.name.lower()
            params = list(getattr(inst, "params", []))

            if name in {"rx", "ry", "rz"} and params:
                scale = 1.0 + eps * real[idx % n]
                try:
                    params[0] = float(params[0]) * scale
                except Exception:
                    pass
                idx += 1

            try:
                new_inst = inst.__class__(*params)
            except Exception:
                new_inst = inst

            new_data.append((new_inst, list(qargs), list(cargs)))

        out.data = new_data
        return out

    # ---------------------- Public methods ---------------------

    def lock(self, circuit_or_qasm: Any) -> Any:
        """
        Lock a circuit or QASM2 string.

        If Qiskit is unavailable or parsing fails, returns the input unchanged.
        """
        if not QISKIT_AVAILABLE:
            return circuit_or_qasm

        from qiskit.qasm2 import loads as qasm2_loads

        if isinstance(circuit_or_qasm, str):
            try:
                qc = qasm2_loads(circuit_or_qasm)
            except Exception:
                return circuit_or_qasm
        elif isinstance(circuit_or_qasm, QuantumCircuit):
            qc = circuit_or_qasm
        else:
            return circuit_or_qasm

        features = self._circuit_to_features(qc)
        latent_in = 0.7 * features + 0.3 * self._id_vec
        latent_out = _latent_transform(latent_in)

        return self._apply_latent_to_circuit(qc, latent_out)

    def simulate(self, qc: "QuantumCircuit", shots: int = 1024) -> Dict[str, int]:
        """
        Convenience wrapper:
            transpile → measure_all → simulate on Aer → return counts.
        """
        if not QISKIT_AVAILABLE:
            raise RuntimeError("Qiskit + qiskit-aer required for simulation.")

        sim = AerSimulator()
        circ = qc.copy()
        circ.measure_all()
        compiled = transpile(circ, sim)
        result = sim.run(compiled, shots=shots).result()
        return result.get_counts(0)
