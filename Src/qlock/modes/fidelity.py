import math
from qiskit import QuantumCircuit, execute
from azure.identity import AzureCliCredential
from azure.quantum import Workspace
from azure.quantum.qiskit import AzureQuantumProvider

# Configuration
N_QUBITS = 27
SHOTS = 4096
RX_BASE = 0.05
RZ_BASE = 0.03
RX_H = 0.11
RZ_H = 0.07
TARGET = "quantinuum.sim.h2-1sc"  # Sim backend (can update)

def entropy(counts):
    total = sum(counts.values())
    return -sum((n / total) * math.log(n / total, 2) for n in counts.values())

def connect_workspace():
    cred = AzureCliCredential()
    ws = Workspace(
        subscription_id="YOUR_SUBSCRIPTION_ID",
        resource_group="ReshnaPrime",
        name="QlockPrime",
        location="westus",
        credential=cred
    )
    return ws

def main():
    print("🔒 Running Hensley Attractor Fidelity Lock...")
    ws = connect_workspace()
    provider = AzureQuantumProvider(workspace=ws)
    backend = provider.get_backend(TARGET)

    # BASELINE circuit
    qc_base = QuantumCircuit(N_QUBITS, N_QUBITS)
    for q in range(N_QUBITS):
        qc_base.rx(RX_BASE, q)
        qc_base.rz(RZ_BASE, q)
        qc_base.measure(q, q)

    job1 = backend.run(qc_base, shots=SHOTS)
    res1 = job1.result()
    counts1 = res1.get_counts()
    H_base = entropy(counts1)

    # HENSLEY attractor circuit
    qc_h = QuantumCircuit(N_QUBITS, N_QUBITS)
    for q in range(N_QUBITS):
        qc_h.rx(RX_H, q)
        qc_h.rz(RZ_H, q)
        qc_h.measure(q, q)

    job2 = backend.run(qc_h, shots=SHOTS)
    res2 = job2.result()
    counts2 = res2.get_counts()
    H_hens = entropy(counts2)

    print("\n========== RESULTS ==========")
    print(f"Baseline entropy : {H_base:.6f}")
    print(f"Hensley entropy  : {H_hens:.6f}")

    if H_hens < H_base:
        print("🎯 HENSLEY ATTRACTOR WINS — more concentration")
    elif H_hens > H_base:
        print("⚠️ Baseline was more concentrated this run")
    else:
        print("ℹ️ Equal entropy")

    print("✨ Completed clean execution.")

if __name__ == "__main__":
    main()
