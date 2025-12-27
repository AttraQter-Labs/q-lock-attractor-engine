"""
Fidelity metrics for Q-LOCK Attractor Engine.

This module provides utilities for calculating fidelity metrics between
baseline and watermarked quantum circuits. All computations run locally
using Qiskit Aer simulator - no Azure Quantum or cloud dependencies required.
"""

import math
from typing import Dict
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def entropy(counts: Dict[str, int]) -> float:
    """
    Calculate Shannon entropy of a probability distribution.
    
    Args:
        counts: Dictionary mapping states to counts
        
    Returns:
        float: Shannon entropy in bits
    """
    total = sum(counts.values())
    if total == 0:
        return 0.0
    return -sum((n / total) * math.log(n / total, 2) 
                for n in counts.values() if n > 0)


def total_variation_distance(p: Dict[str, int], q: Dict[str, int]) -> float:
    """
    Calculate Total Variation Distance between two distributions.
    
    Args:
        p: First distribution (counts dictionary)
        q: Second distribution (counts dictionary)
        
    Returns:
        float: TVD value in [0, 1]
    """
    all_states = set(p.keys()) | set(q.keys())
    total_p = sum(p.values())
    total_q = sum(q.values())
    
    tvd = 0.5 * sum(abs(p.get(s, 0) / total_p - q.get(s, 0) / total_q) 
                    for s in all_states)
    return tvd


def kl_divergence(p: Dict[str, int], q: Dict[str, int], epsilon: float = 1e-10) -> float:
    """
    Calculate Kullback-Leibler divergence from p to q.
    
    Args:
        p: First distribution (counts dictionary)
        q: Second distribution (counts dictionary)
        epsilon: Small value to avoid log(0)
        
    Returns:
        float: KL divergence value
    """
    all_states = set(p.keys()) | set(q.keys())
    total_p = sum(p.values())
    total_q = sum(q.values())
    
    kl = 0.0
    for s in all_states:
        p_s = p.get(s, 0) / total_p
        q_s = q.get(s, 0) / total_q
        if p_s > epsilon:
            kl += p_s * np.log((p_s + epsilon) / (q_s + epsilon))
    return kl


def hellinger_distance(p: Dict[str, int], q: Dict[str, int]) -> float:
    """
    Calculate Hellinger distance between two distributions.
    
    Args:
        p: First distribution (counts dictionary)
        q: Second distribution (counts dictionary)
        
    Returns:
        float: Hellinger distance in [0, 1]
    """
    all_states = set(p.keys()) | set(q.keys())
    total_p = sum(p.values())
    total_q = sum(q.values())
    
    h = np.sqrt(0.5 * sum(
        (np.sqrt(p.get(s, 0) / total_p) - np.sqrt(q.get(s, 0) / total_q)) ** 2
        for s in all_states
    ))
    return h


def compare_circuits(baseline_circuit: QuantumCircuit,
                    watermarked_circuit: QuantumCircuit,
                    shots: int = 1024) -> Dict[str, float]:
    """
    Compare baseline and watermarked circuits using fidelity metrics.
    
    This function runs both circuits on the local Qiskit Aer simulator
    and computes fidelity metrics.
    
    Args:
        baseline_circuit: Original circuit without watermarking
        watermarked_circuit: Circuit with identity-locked watermark
        shots: Number of simulation shots
        
    Returns:
        Dictionary containing fidelity metrics:
            - total_variation_distance
            - kl_divergence
            - hellinger_distance
            - baseline_counts
            - watermark_counts
    """
    sim = AerSimulator()
    
    # Simulate baseline
    circ_base = baseline_circuit.copy()
    if not any(inst.operation.name == "measure" for inst in circ_base.data):
        circ_base.measure_all()
    compiled_base = transpile(circ_base, sim)
    result_base = sim.run(compiled_base, shots=shots).result()
    counts_base = result_base.get_counts(0)
    
    # Simulate watermarked
    circ_lock = watermarked_circuit.copy()
    if not any(inst.operation.name == "measure" for inst in circ_lock.data):
        circ_lock.measure_all()
    compiled_lock = transpile(circ_lock, sim)
    result_lock = sim.run(compiled_lock, shots=shots).result()
    counts_lock = result_lock.get_counts(0)
    
    # Calculate metrics
    return {
        "total_variation_distance": total_variation_distance(counts_base, counts_lock),
        "kl_divergence": kl_divergence(counts_base, counts_lock),
        "hellinger_distance": hellinger_distance(counts_base, counts_lock),
        "baseline_counts": counts_base,
        "watermark_counts": counts_lock,
    }


if __name__ == "__main__":
    # Example usage
    from q_lock_engine import QLockAttractorEngine
    
    # Create a simple test circuit
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    
    # Create watermarked version
    engine = QLockAttractorEngine("test-identity")
    qc_locked = engine.lock(qc)
    
    # Compare
    results = compare_circuits(qc, qc_locked, shots=1024)
    
    print("Fidelity Metrics:")
    print(f"  TVD: {results['total_variation_distance']:.6f}")
    print(f"  KL:  {results['kl_divergence']:.6f}")
    print(f"  H:   {results['hellinger_distance']:.6f}")

