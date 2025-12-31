"""
Test scalar guard mechanism.

Verifies that scalar mode is properly gated and refused outside admissible regimes.
"""

try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False

from qlock import QLockEngine, Refusal
from qlock.engine.policy import is_scalar_allowed


def test_scalar_initialization_refused():
    """Scalar mode initialization should be refused."""
    try:
        QLockEngine(mode="scalar")
        raise AssertionError("Should have raised Refusal")
    except Refusal as exc:
        refusal = exc
        assert "scalar" in refusal.reason.lower()
        assert "policy" in refusal.reason.lower()


def test_scalar_policy_strict():
    """Scalar allowed only when ALL conditions met."""
    # All conditions good
    assert is_scalar_allowed(
        noise_level=0.01,
        phase_dispersion=0.05,
        procedural_disorder=0.10,
        topology_safe=True
    ) == True
    
    # Noise too high
    assert is_scalar_allowed(
        noise_level=0.10,  # Above 0.05 threshold
        phase_dispersion=0.05,
        procedural_disorder=0.10,
        topology_safe=True
    ) == False
    
    # Phase dispersion too high
    assert is_scalar_allowed(
        noise_level=0.01,
        phase_dispersion=0.15,  # Above 0.1 threshold
        procedural_disorder=0.10,
        topology_safe=True
    ) == False
    
    # Procedural disorder too high
    assert is_scalar_allowed(
        noise_level=0.01,
        phase_dispersion=0.05,
        procedural_disorder=0.20,  # Above 0.15 threshold
        topology_safe=True
    ) == False
    
    # Topology not safe
    assert is_scalar_allowed(
        noise_level=0.01,
        phase_dispersion=0.05,
        procedural_disorder=0.10,
        topology_safe=False
    ) == False


def test_scalar_never_auto_enabled():
    """Scalar mode must never be default or auto-enabled."""
    from qlock.engine.policy import DEFAULT_ALLOWED_MODES, EXPERIMENTAL_MODES
    
    assert "scalar" not in DEFAULT_ALLOWED_MODES
    assert "scalar" in EXPERIMENTAL_MODES


if __name__ == "__main__":
    if PYTEST_AVAILABLE:
        pytest.main([__file__, "-v"])
    else:
        # Run tests manually
        print("Running tests without pytest...")
        test_scalar_initialization_refused()
        test_scalar_policy_strict()
        test_scalar_never_auto_enabled()
        print("All tests passed!")
