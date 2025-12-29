"""
Test refusal mechanism.

Verifies that Q-LOCK refuses to act when stabilization would be unsafe.
"""

try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False

from qlock import QLockEngine, Refusal


def test_scalar_mode_refused_by_default():
    """Scalar mode should be refused by default policy."""
    try:
        engine = QLockEngine(mode="scalar")
        raise AssertionError("Should have raised Refusal")
    except Refusal as exc:
        assert "disabled by policy" in str(exc).lower()


def test_fidelity_mode_allowed():
    """Fidelity mode should always be allowed."""
    engine = QLockEngine(mode="fidelity")
    assert engine.mode == "fidelity"


def test_watermark_mode_allowed():
    """Watermark mode should be allowed."""
    engine = QLockEngine(mode="watermark")
    assert engine.mode == "watermark"


def test_witness_phase_mode_allowed():
    """Witness phase mode should be allowed."""
    engine = QLockEngine(mode="witness_phase")
    assert engine.mode == "witness_phase"


def test_refusal_logged():
    """Refusals should be logged."""
    engine = QLockEngine(mode="fidelity")
    
    # Attempting scalar via direct call would be refused
    # For now, just verify the log exists
    assert hasattr(engine, 'get_refusal_log')
    assert isinstance(engine.get_refusal_log(), list)


if __name__ == "__main__":
    if PYTEST_AVAILABLE:
        pytest.main([__file__, "-v"])
    else:
        # Run tests manually
        print("Running tests without pytest...")
        test_scalar_mode_refused_by_default()
        test_fidelity_mode_allowed()
        test_watermark_mode_allowed()
        test_witness_phase_mode_allowed()
        test_refusal_logged()
        print("All tests passed!")
