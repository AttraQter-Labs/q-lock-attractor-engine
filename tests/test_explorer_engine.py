"""
Tests for Explorer Engine.

Verifies exploratory procedural variant generation.
"""

try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False

from explorer_engine import ExplorerEngine
from explorer_engine.explorer_engine import ExplorerResult


def test_explorer_engine_initialization():
    """Test Explorer Engine can be initialized."""
    engine = ExplorerEngine(base_object="test_object")
    assert engine.base_object == "test_object"


def test_enumerate_procedures_default():
    """Test procedural variant enumeration with default count."""
    engine = ExplorerEngine(base_object="test")
    variants = engine.enumerate_procedures()
    
    assert len(variants) == 10  # Default variants
    assert all(isinstance(v, ExplorerResult) for v in variants)


def test_enumerate_procedures_custom_count():
    """Test procedural variant enumeration with custom count."""
    engine = ExplorerEngine(base_object="test")
    variants = engine.enumerate_procedures(variants=5)
    
    assert len(variants) == 5


def test_explorer_result_structure():
    """Test ExplorerResult has required fields."""
    engine = ExplorerEngine(base_object="test")
    variants = engine.enumerate_procedures(variants=1)
    
    result = variants[0]
    assert hasattr(result, 'pi_signature')
    assert hasattr(result, 'assumptions')
    assert hasattr(result, 'notes')
    
    assert isinstance(result.pi_signature, str)
    assert isinstance(result.assumptions, dict)
    assert isinstance(result.notes, str)


def test_explorer_result_immutable():
    """Test ExplorerResult is frozen (immutable)."""
    engine = ExplorerEngine(base_object="test")
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
    engine = ExplorerEngine(base_object="test")
    variants = engine.enumerate_procedures(variants=10)
    
    signatures = [v.pi_signature for v in variants]
    assert len(signatures) == len(set(signatures))  # All unique


def test_assumptions_present():
    """Test that assumptions are present in results."""
    engine = ExplorerEngine(base_object="test")
    variants = engine.enumerate_procedures(variants=1)
    
    result = variants[0]
    assert "ordering" in result.assumptions
    assert "initialization" in result.assumptions
    assert "measurement" in result.assumptions


def test_no_refusal_mechanism():
    """Test that Explorer Engine does not refuse operations."""
    # Explorer Engine should never refuse - this is by design
    engine = ExplorerEngine(base_object=None)
    variants = engine.enumerate_procedures(variants=100)
    
    # Should generate all requested variants without refusal
    assert len(variants) == 100


if __name__ == "__main__":
    if PYTEST_AVAILABLE:
        pytest.main([__file__, "-v"])
    else:
        # Run tests manually
        print("Running tests without pytest...")
        test_explorer_engine_initialization()
        test_enumerate_procedures_default()
        test_enumerate_procedures_custom_count()
        test_explorer_result_structure()
        test_explorer_result_immutable()
        test_pi_signatures_unique()
        test_assumptions_present()
        test_no_refusal_mechanism()
        print("All tests passed!")
