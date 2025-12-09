from qiskit import QuantumCircuit
from .identity import identity_vector
from .perturbation import golden_phase_map, compute_perturbation


class QLockEngine:
    """
    Public Q-LOCK engine.

    - Takes an identity string.
    - Builds a high-dimensional identity signature.
    - Applies small, deterministic perturbations to rotation gates (rx/ry/rz).
    """

    def __init__(self, identity: str, latent_dim: int = 60000):
        base_vec = identity_vector(identity, dim=latent_dim)
        self.identity_sig = golden_phase_map(base_vec)

    def lock(self, qc: QuantumCircuit) -> QuantumCircuit:
        """
        Return a locked copy of the circuit.
        Logic is preserved; only small angle shifts are introduced.
        """
        locked = qc.copy()
        gate_index = 0

        for inst, qargs, cargs in locked.data:
            if inst.name in ("rx", "ry", "rz") and inst.params:
                delta = compute_perturbation(self.identity_sig, gate_index)
                inst.params[0] += delta
                gate_index += 1

        return locked
