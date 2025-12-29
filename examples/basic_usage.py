"""
Q-LOCK Basic Usage Example

Demonstrates core functionality of the Q-LOCK attractor-based
coherence stabilization engine.
"""

from qlock import QLockEngine, QLockConfig


def example_fidelity_mode():
    """Example: Basic fidelity mode usage."""
    print("=" * 60)
    print("Example 1: Fidelity Mode")
    print("=" * 60)
    
    # Create engine with fidelity mode (default)
    config = QLockConfig(mode="fidelity")
    engine = QLockEngine(config)
    
    # Mock circuit (replace with actual quantum circuit)
    class MockCircuit:
        def depth(self):
            return 10
        num_qubits = 4
    
    circuit = MockCircuit()
    
    # Execute Q-LOCK
    result = engine.execute(circuit, params={"estimated_noise": 0.08})
    
    # Check result
    if result.success:
        print(f"✓ Execution successful")
        print(f"  Mode: {result.mode}")
        print(f"  Verdict: {result.verdict}")
        print(f"  Metrics: {result.metrics}")
    else:
        print(f"✗ Execution refused: {result.refusal_reason}")
    
    print()


def example_watermark_mode():
    """Example: Watermark mode for identity-locking."""
    print("=" * 60)
    print("Example 2: Watermark Mode")
    print("=" * 60)
    
    # Create engine with watermark mode
    config = QLockConfig(
        mode="watermark",
        identity="enterprise-user-2025"
    )
    engine = QLockEngine(config)
    
    # Mock circuit
    class MockCircuit:
        def depth(self):
            return 15
        num_qubits = 6
    
    circuit = MockCircuit()
    
    # Execute Q-LOCK
    result = engine.execute(circuit, params={"estimated_noise": 0.05})
    
    # Check result
    if result.success:
        print(f"✓ Execution successful")
        print(f"  Identity fingerprint: {result.history.get('identity_fingerprint', 'N/A')[:16]}...")
        print(f"  Metrics: {result.metrics}")
    else:
        print(f"✗ Execution refused: {result.refusal_reason}")
    
    print()


def example_witness_phase_mode():
    """Example: WitnessPhase mode for phase-critical circuits."""
    print("=" * 60)
    print("Example 3: WitnessPhase Mode")
    print("=" * 60)
    
    # Create engine with witness_phase mode
    config = QLockConfig(mode="witness_phase")
    engine = QLockEngine(config)
    
    # Mock circuit
    class MockCircuit:
        def depth(self):
            return 20
        num_qubits = 8
    
    circuit = MockCircuit()
    
    # Execute Q-LOCK
    result = engine.execute(circuit, params={"estimated_noise": 0.10})
    
    # Check result
    if result.success:
        print(f"✓ Execution successful")
        print(f"  Phase tracking enabled")
        print(f"  Metrics: {result.metrics}")
    else:
        print(f"✗ Execution refused: {result.refusal_reason}")
    
    print()


def example_scalar_guarded_mode():
    """Example: Scalar guarded mode (maximum safety)."""
    print("=" * 60)
    print("Example 4: Scalar Guarded Mode")
    print("=" * 60)
    
    # Create engine with scalar_guarded mode
    config = QLockConfig(
        mode="scalar_guarded",
        noise_threshold=0.075,
        variance_limit=0.125
    )
    engine = QLockEngine(config)
    
    # Mock circuit
    class MockCircuit:
        def depth(self):
            return 12
        num_qubits = 5
    
    circuit = MockCircuit()
    
    # Attempt 1: Without confirmation (will refuse)
    print("Attempt 1: Without explicit confirmation")
    result = engine.execute(circuit, params={"estimated_noise": 0.05})
    print(f"  Result: {result.verdict}")
    print(f"  Reason: {result.refusal_reason}")
    
    # Attempt 2: With confirmation
    print("\nAttempt 2: With explicit confirmation")
    result = engine.execute(
        circuit,
        params={
            "estimated_noise": 0.05,
            "estimated_variance": 0.08,
            "scalar_mode_confirmed": True
        }
    )
    
    if result.success:
        print(f"  ✓ Execution successful")
        print(f"  Metrics: {result.metrics}")
    else:
        print(f"  ✗ Execution refused: {result.refusal_reason}")
    
    print()


def example_refusal_handling():
    """Example: Handling refusals gracefully."""
    print("=" * 60)
    print("Example 5: Refusal Handling")
    print("=" * 60)
    
    config = QLockConfig(mode="fidelity")
    engine = QLockEngine(config)
    
    class MockCircuit:
        def depth(self):
            return 50
        num_qubits = 10
    
    circuit = MockCircuit()
    
    # Attempt with high noise (will refuse)
    print("Attempting execution with high noise...")
    result = engine.execute(
        circuit,
        params={"estimated_noise": 0.20}  # Exceeds threshold
    )
    
    if not result.success:
        print(f"✗ Refused: {result.refusal_reason}")
        
        # Adjust parameters and retry
        print("\nRetrying with adjusted parameters...")
        result = engine.execute(
            circuit,
            params={"estimated_noise": 0.10}  # Within threshold
        )
        
        if result.success:
            print(f"✓ Retry successful!")
            print(f"  Metrics: {result.metrics}")
    
    print()


def example_history_export():
    """Example: Exporting procedural history."""
    print("=" * 60)
    print("Example 6: History Export")
    print("=" * 60)
    
    config = QLockConfig(mode="fidelity")
    engine = QLockEngine(config)
    
    class MockCircuit:
        def depth(self):
            return 8
        num_qubits = 4
    
    # Execute multiple times
    for i in range(3):
        circuit = MockCircuit()
        result = engine.execute(
            circuit,
            params={"estimated_noise": 0.05 + i * 0.02}
        )
        print(f"Execution {i+1}: {result.verdict}")
    
    # Get complete history
    history = engine.get_history()
    print(f"\nTotal executions in history: {len(history)}")
    
    # Export history
    engine.history.export_json("qlock_history.json")
    print("✓ History exported to qlock_history.json")
    
    print()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Q-LOCK Basic Usage Examples")
    print("=" * 60 + "\n")
    
    example_fidelity_mode()
    example_watermark_mode()
    example_witness_phase_mode()
    example_scalar_guarded_mode()
    example_refusal_handling()
    example_history_export()
    
    print("=" * 60)
    print("Examples complete!")
    print("=" * 60)
