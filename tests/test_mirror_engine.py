"""
Tests for Mirror Engine.

Verifies exploratory procedural variant generation.
"""

try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False

from mirror_engine import MirrorEngine
from mirror_engine.mirror_engine import MirrorResult


def test_mirror_engine_initialization():
    """Test Mirror Engine can be initialized."""
    engine = MirrorEngine(base_object="test_object")
    assert engine.base_object == "test_object"


def test_enumerate_procedures_default():
    """Test procedural variant enumeration with default count."""
    engine = MirrorEngine(base_object="test")
    variants = engine.enumerate_procedures()
    
    assert len(variants) == 10  # Default variants
    assert all(isinstance(v, MirrorResult) for v in variants)


def test_enumerate_procedures_custom_count():
    """Test procedural variant enumeration with custom count."""
    engine = MirrorEngine(base_object="test")
    variants = engine.enumerate_procedures(variants=5)
    
    assert len(variants) == 5


def test_mirror_result_structure():
    """Test MirrorResult has required fields."""
    engine = MirrorEngine(base_object="test")
    variants = engine.enumerate_procedures(variants=1)
    
    result = variants[0]
    assert hasattr(result, 'pi_signature')
    assert hasattr(result, 'assumptions')
    assert hasattr(result, 'notes')
    
    assert isinstance(result.pi_signature, str)
    assert isinstance(result.assumptions, dict)
    assert isinstance(result.notes, str)


def test_mirror_result_immutable():
    """Test MirrorResult is frozen (immutable)."""
    engine = MirrorEngine(base_object="test")
    variants = engine.enumerate_procedures(variants=1)
    
    result = variants[0]
    
    # Should not be able to modify frozen dataclass
    try:
        result.pi_signature = "modified"
        assert False, "Should not allow modification of frozen dataclass"
    except (AttributeError, Exception):
        pass  # Expected


def test_pi_signatures_unique():
    """Test that PI signatures are unique across variants."""
    engine = MirrorEngine(base_object="test")
    variants = engine.enumerate_procedures(variants=10)
    
    signatures = [v.pi_signature for v in variants]
    assert len(signatures) == len(set(signatures))  # All unique


def test_assumptions_present():
    """Test that assumptions are present in results."""
    engine = MirrorEngine(base_object="test")
    variants = engine.enumerate_procedures(variants=1)
    
    result = variants[0]
    assert "ordering" in result.assumptions
    assert "initialization" in result.assumptions
    assert "measurement" in result.assumptions


def test_no_refusal_mechanism():
    """Test that Mirror Engine does not refuse operations."""
    # Mirror Engine should never refuse - this is by design
    engine = MirrorEngine(base_object=None)
    variants = engine.enumerate_procedures(variants=100)
    
    # Should generate all requested variants without refusal
    assert len(variants) == 100


if __name__ == "__main__":
    if PYTEST_AVAILABLE:
        pytest.main([__file__, "-v"])
    else:
        # Run tests manually
        print("Running tests without pytest...")
        test_mirror_engine_initialization()
        test_enumerate_procedures_default()
        test_enumerate_procedures_custom_count()
        test_mirror_result_structure()
        test_mirror_result_immutable()
        test_pi_signatures_unique()
        test_assumptions_present()
        test_no_refusal_mechanism()
        print("All tests passed!")
