"""
Q-LOCK Engine Tests

Minimal placeholder tests for Q-LOCK functionality.
"""

import pytest
from qlock import QLockEngine, QLockConfig
from qlock.guards import Guards
from qlock.metrics import Metrics
from qlock.observer import Observer
from qlock.history import History


class MockCircuit:
    """Mock circuit for testing."""
    def __init__(self, num_qubits=4, circuit_depth=10):
        self.num_qubits = num_qubits
        self._depth = circuit_depth
    
    def depth(self):
        return self._depth


def test_engine_initialization():
    """Test engine initializes correctly."""
    config = QLockConfig(mode="fidelity")
    engine = QLockEngine(config)
    
    assert engine.config.mode == "fidelity"
    assert isinstance(engine.guards, Guards)
    assert isinstance(engine.metrics, Metrics)
    assert isinstance(engine.observer, Observer)
    assert isinstance(engine.history, History)


def test_fidelity_mode_execution():
    """Test fidelity mode executes successfully."""
    config = QLockConfig(mode="fidelity")
    engine = QLockEngine(config)
    circuit = MockCircuit()
    
    result = engine.execute(circuit, params={"estimated_noise": 0.08})
    
    assert result.success == True
    assert result.mode == "fidelity"
    assert result.verdict == "ACCEPTED"
    assert len(result.metrics) > 0


def test_noise_threshold_refusal():
    """Test refusal when noise exceeds threshold."""
    config = QLockConfig(mode="fidelity", noise_threshold=0.15)
    engine = QLockEngine(config)
    circuit = MockCircuit()
    
    result = engine.execute(circuit, params={"estimated_noise": 0.20})
    
    assert result.success == False
    assert result.verdict == "REFUSED"
    assert "noise" in result.refusal_reason.lower()


def test_variance_threshold_refusal():
    """Test refusal when variance exceeds limit."""
    config = QLockConfig(mode="fidelity", variance_limit=0.25)
    engine = QLockEngine(config)
    circuit = MockCircuit()
    
    result = engine.execute(circuit, params={"estimated_variance": 0.30})
    
    assert result.success == False
    assert result.verdict == "REFUSED"
    assert "variance" in result.refusal_reason.lower()


def test_watermark_mode_requires_identity():
    """Test watermark mode refuses without identity."""
    config = QLockConfig(mode="watermark", identity=None)
    engine = QLockEngine(config)
    circuit = MockCircuit()
    
    result = engine.execute(circuit)
    
    assert result.success == False
    assert "identity" in result.refusal_reason.lower()


def test_watermark_mode_with_identity():
    """Test watermark mode succeeds with identity."""
    config = QLockConfig(mode="watermark", identity="test-user")
    engine = QLockEngine(config)
    circuit = MockCircuit()
    
    result = engine.execute(circuit, params={"estimated_noise": 0.05})
    
    assert result.success == True
    assert result.mode == "watermark"


def test_scalar_mode_requires_confirmation():
    """Test scalar mode refuses without confirmation."""
    config = QLockConfig(mode="scalar_guarded")
    engine = QLockEngine(config)
    circuit = MockCircuit()
    
    result = engine.execute(circuit, params={"estimated_noise": 0.05})
    
    assert result.success == False
    assert "confirmation" in result.refusal_reason.lower()


def test_scalar_mode_with_confirmation():
    """Test scalar mode succeeds with confirmation."""
    config = QLockConfig(mode="scalar_guarded")
    engine = QLockEngine(config)
    circuit = MockCircuit()
    
    result = engine.execute(
        circuit,
        params={
            "estimated_noise": 0.05,
            "estimated_variance": 0.08,
            "scalar_mode_confirmed": True
        }
    )
    
    assert result.success == True
    assert result.mode == "scalar_guarded"


def test_history_recording():
    """Test history is recorded correctly."""
    config = QLockConfig(mode="fidelity")
    engine = QLockEngine(config)
    circuit = MockCircuit()
    
    # Execute twice
    engine.execute(circuit, params={"estimated_noise": 0.05})
    engine.execute(circuit, params={"estimated_noise": 0.08})
    
    history = engine.get_history()
    
    assert len(history) == 2
    assert history[0]["mode"] == "fidelity"
    assert history[1]["mode"] == "fidelity"


def test_observer_recording():
    """Test observer records events."""
    observer = Observer()
    
    observer.record("test_event", {"key": "value"})
    observer.record("test_event", {"key": "value2"})
    
    observations = observer.get_observations()
    
    assert len(observations) == 2
    assert observations[0].event_type == "test_event"


def test_guards_admissibility():
    """Test guards check admissibility correctly."""
    guards = Guards(noise_threshold=0.15, variance_limit=0.25)
    circuit = MockCircuit()
    
    # Should pass
    result = guards.check_admissibility(
        circuit,
        {"estimated_noise": 0.10, "estimated_variance": 0.20}
    )
    assert result["admissible"] == True
    
    # Should fail (noise)
    result = guards.check_admissibility(
        circuit,
        {"estimated_noise": 0.20, "estimated_variance": 0.20}
    )
    assert result["admissible"] == False


def test_metrics_computation():
    """Test metrics are computed."""
    metrics = Metrics()
    observer = Observer()
    circuit = MockCircuit()
    
    result = metrics.compute(circuit, circuit, observer)
    
    assert "coherence" in result
    assert "entropy" in result
    assert "variance" in result
    assert "fidelity" in result


def test_basin_metrics():
    """Test basin metrics computation."""
    distribution = {
        "00": 500,
        "01": 300,
        "10": 150,
        "11": 50
    }
    
    metrics = Metrics.compute_basin_metrics(distribution)
    
    assert "top_1_mass" in metrics
    assert "top_5_mass" in metrics
    assert "effective_support" in metrics
    assert "gini_coefficient" in metrics
    assert 0.0 <= metrics["top_1_mass"] <= 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
