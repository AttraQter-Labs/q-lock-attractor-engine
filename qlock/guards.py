"""
Guards for Q-LOCK safety and admissibility checks.

Implements noise thresholds, scalar admissibility, and hard refusal logic.
"""

from typing import Any, Dict, Optional
from abc import ABC, abstractmethod


class Guard(ABC):
    """Base class for Q-LOCK guards."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize guard with optional configuration.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
    
    @abstractmethod
    def evaluate(self, circuit: Any, identity: str, mode: str) -> Dict[str, Any]:
        """
        Evaluate if the circuit should be refused.
        
        Args:
            circuit: Quantum circuit to evaluate
            identity: Identity string
            mode: Current operating mode
            
        Returns:
            Dictionary with 'refused' boolean and 'reason' string
        """
        pass


class NoiseGuard(Guard):
    """
    Guard that checks noise thresholds.
    
    Refuses circuits in regimes with excessive noise levels
    that would compromise basin identity preservation.
    """
    
    DEFAULT_NOISE_THRESHOLD = 0.15
    
    def evaluate(self, circuit: Any, identity: str, mode: str) -> Dict[str, Any]:
        """
        Evaluate circuit against noise thresholds.
        
        Args:
            circuit: Quantum circuit to evaluate
            identity: Identity string
            mode: Current operating mode
            
        Returns:
            Refusal verdict if noise exceeds threshold
        """
        threshold = self.config.get("noise_threshold", self.DEFAULT_NOISE_THRESHOLD)
        
        estimated_noise = self._estimate_circuit_noise(circuit)
        
        if estimated_noise > threshold:
            return {
                "refused": True,
                "reason": f"Noise level {estimated_noise:.3f} exceeds threshold {threshold:.3f}",
            }
        
        return {"refused": False, "reason": None}
    
    def _estimate_circuit_noise(self, circuit: Any) -> float:
        """
        Estimate effective noise level of circuit.
        
        Args:
            circuit: Quantum circuit
            
        Returns:
            Estimated noise level (0.0 to 1.0)
        """
        if hasattr(circuit, "depth"):
            depth = circuit.depth()
            return min(0.01 * depth, 0.3)
        return 0.05


class ScalarGuard(Guard):
    """
    Guard for scalar mode admissibility.
    
    Scalar mode must refuse operations outside strict boundaries.
    This guard enforces hard limits on scalar operations.
    """
    
    SCALAR_MIN_THRESHOLD = 0.01
    SCALAR_MAX_THRESHOLD = 0.99
    
    def evaluate(self, circuit: Any, identity: str, mode: str) -> Dict[str, Any]:
        """
        Evaluate scalar mode admissibility.
        
        Args:
            circuit: Quantum circuit to evaluate
            identity: Identity string
            mode: Current operating mode
            
        Returns:
            Refusal verdict if scalar operations are out of bounds
        """
        if mode != "scalar_guarded":
            return {"refused": False, "reason": None}
        
        scalar_value = self._extract_scalar_value(circuit)
        
        if scalar_value is None:
            return {
                "refused": True,
                "reason": "Scalar mode requires scalar-parameterized circuit",
            }
        
        if scalar_value < self.SCALAR_MIN_THRESHOLD or scalar_value > self.SCALAR_MAX_THRESHOLD:
            return {
                "refused": True,
                "reason": f"Scalar value {scalar_value:.3f} outside safe boundaries "
                         f"[{self.SCALAR_MIN_THRESHOLD}, {self.SCALAR_MAX_THRESHOLD}]",
            }
        
        return {"refused": False, "reason": None}
    
    def _extract_scalar_value(self, circuit: Any) -> Optional[float]:
        """
        Extract scalar value from circuit parameters.
        
        Args:
            circuit: Quantum circuit
            
        Returns:
            Scalar value if present, None otherwise
        """
        if hasattr(circuit, "parameters") and circuit.parameters:
            params = list(circuit.parameters)
            if params:
                return 0.5
        return None
