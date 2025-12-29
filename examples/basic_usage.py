"""
Basic usage example for Q-LOCK.

Demonstrates initialization, circuit processing, and metric retrieval.
"""

from qlock import QLockEngine


def example_fidelity_mode():
    """Example using fidelity mode."""
    print("=== Fidelity Mode Example ===\n")
    
    engine = QLockEngine(mode="fidelity")
    
    mock_circuit = MockCircuit(depth=10, num_qubits=4)
    identity = "alice@example.com"
    
    result = engine.process(mock_circuit, identity)
    
    print(f"Status: {result['status']}")
    print(f"Metrics: {result['metrics']}")
    print(f"History entry: {result['history_entry']}")
    print()


def example_witness_phase_mode():
    """Example using witness phase mode."""
    print("=== Witness Phase Mode Example ===\n")
    
    engine = QLockEngine(mode="witness_phase")
    
    mock_circuit = MockCircuit(depth=15, num_qubits=6)
    identity = "team-quantum-prod"
    
    result = engine.process(mock_circuit, identity)
    
    print(f"Status: {result['status']}")
    print(f"Metrics: {result['metrics']}")
    print()


def example_watermark_mode():
    """Example using watermark mode."""
    print("=== Watermark Mode Example ===\n")
    
    engine = QLockEngine(mode="watermark")
    
    mock_circuit = MockCircuit(depth=20, num_qubits=8)
    identity = "research-lab-alpha"
    
    result = engine.process(mock_circuit, identity)
    
    print(f"Status: {result['status']}")
    print("Watermark mode preserves exact topology")
    print()


def example_scalar_guarded_mode():
    """Example using scalar guarded mode."""
    print("=== Scalar Guarded Mode Example ===\n")
    
    engine = QLockEngine(mode="scalar_guarded")
    
    mock_circuit = MockCircuit(depth=5, num_qubits=3)
    identity = "safety-critical-app"
    
    result = engine.process(mock_circuit, identity)
    
    print(f"Status: {result['status']}")
    if result['status'] == 'refused':
        print(f"Refusal reason: {result['verdict']}")
    else:
        print("Accepted within safe boundaries")
    print()


def example_refusal():
    """Example demonstrating refusal."""
    print("=== Refusal Example ===\n")
    
    config = {"noise_threshold": 0.10}
    engine = QLockEngine(mode="fidelity", config=config)
    
    high_noise_circuit = MockCircuit(depth=50, num_qubits=10)
    identity = "test-user"
    
    result = engine.process(high_noise_circuit, identity)
    
    print(f"Status: {result['status']}")
    if result['status'] == 'refused':
        print(f"Verdict: {result['verdict']}")
        print("Circuit refused due to high noise estimate")
    print()


def example_history_tracking():
    """Example demonstrating history tracking."""
    print("=== History Tracking Example ===\n")
    
    engine = QLockEngine(mode="fidelity")
    
    for i in range(3):
        circuit = MockCircuit(depth=10 + i * 5, num_qubits=4)
        result = engine.process(circuit, f"user-{i}")
        print(f"Processed circuit {i + 1}: {result['status']}")
    
    print("\nHistory:")
    history = engine.get_history(limit=5)
    for entry in history:
        print(f"  {entry['status']} at {entry['timestamp']}")
    
    print("\nStats:")
    stats = engine.get_stats()
    print(f"  Processed: {stats['processed_count']}")
    print(f"  Refused: {stats['refused_count']}")
    print(f"  Acceptance rate: {stats['acceptance_rate']:.2%}")
    print()


class MockCircuit:
    """Mock circuit for demonstration purposes."""
    
    def __init__(self, depth, num_qubits):
        self.depth_value = depth
        self.num_qubits = num_qubits
        self.parameters = []
    
    def depth(self):
        return self.depth_value
    
    def __str__(self):
        return f"MockCircuit(depth={self.depth_value}, qubits={self.num_qubits})"


if __name__ == "__main__":
    print("Q-LOCK Basic Usage Examples\n")
    print("=" * 60)
    print()
    
    example_fidelity_mode()
    example_witness_phase_mode()
    example_watermark_mode()
    example_scalar_guarded_mode()
    example_refusal()
    example_history_tracking()
    
    print("=" * 60)
    print("\nAll examples completed successfully!")
