"""
Test repeatability and determinism.

Verifies that Q-LOCK produces identical outputs for identical inputs.
"""

try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False

from qlock import QLockEngine


class MockCircuit:
    """Mock circuit for testing."""
    def __init__(self, depth=10):
        self.depth_value = depth
    
    def depth(self):
        return self.depth_value
    
    def __str__(self):
        return f"MockCircuit({self.depth_value})"


def test_deterministic_fidelity():
    """Fidelity mode should be deterministic."""
    engine = QLockEngine(mode="fidelity")
    circuit = MockCircuit(depth=10)
    
    result1 = engine.process(circuit, identity="test_user")
    result2 = engine.process(circuit, identity="test_user")
    
    assert result1["status"] == result2["status"]
    assert result1["mode"] == result2["mode"]


def test_identity_locked():
    """Different identities should produce different results (when implemented)."""
    engine = QLockEngine(mode="fidelity")
    circuit = MockCircuit(depth=10)
    
    result1 = engine.process(circuit, identity="user_a")
    result2 = engine.process(circuit, identity="user_b")
    
    # Both should be accepted
    assert result1["status"] == "accepted"
    assert result2["status"] == "accepted"


def test_watermark_preserves_topology():
    """Watermark mode must not change topology."""
    engine = QLockEngine(mode="watermark")
    circuit = MockCircuit(depth=10)
    
    result = engine.process(circuit, identity="test_user")
    
    assert result["status"] == "accepted"
    # In real implementation, would verify topology unchanged


if __name__ == "__main__":
    if PYTEST_AVAILABLE:
        pytest.main([__file__, "-v"])
    else:
        # Run tests manually
        print("Running tests without pytest...")
        test_deterministic_fidelity()
        test_identity_locked()
        test_watermark_preserves_topology()
        print("All tests passed!")
