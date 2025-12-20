from qiskit import QuantumCircuit
import hashlib

def generate_watermark_circuit(identity="C-ΩΛ ReshnaPrime 2025"):
    seed = int(hashlib.sha256(identity.encode()).hexdigest(), 16) % 2**32
    qc = QuantumCircuit(5, 5)
    for i in range(5):
        if (seed >> i) & 1:
            qc.h(i)
        else:
            qc.x(i)
    qc.barrier()
    qc.measure(range(5), range(5))
    return qc

if __name__ == "__main__":
    circuit = generate_watermark_circuit()
    print(circuit.draw())
