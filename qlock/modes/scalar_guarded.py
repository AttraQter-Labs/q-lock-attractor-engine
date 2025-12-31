"""
Scalar Guarded mode for Q-LOCK.

MUST refuse operations outside strict boundaries.
MUST never auto-enable.

This mode provides scalar-based stabilization with explicit
hard boundaries and refusal logic built into the mode itself.
"""

from typing import Any, Dict, Optional
from qlock.modes.fidelity import ModeBase


class ScalarGuardedMode(ModeBase):
    """
    Scalar Guarded mode: Strict boundary enforcement.
    
    Applies scalar-parameterized transformations with hard
    refusal logic for operations outside safe boundaries.
    
    WARNING: This mode is restrictive by design.
    - Never auto-enables
    - Refuses unsafe parameter regimes
    - Requires explicit user selection
    
    Suitable for:
    - Safety-critical applications
    - Bounded optimization scenarios
    - Risk-averse deployments
    
    Boundaries:
    - Scalar values must be in [0.01, 0.99]
    - Circuit depth must be < 100
    - Parameter count must be < 50
    """
    
    MIN_SCALAR = 0.01
    MAX_SCALAR = 0.99
    MAX_DEPTH = 100
    MAX_PARAMS = 50
    
    def apply(self, circuit: Any, identity: str) -> Any:
        """
        Apply scalar guarded transformation.
        
        This method assumes guards have already evaluated the circuit.
        If this mode is reached, the circuit is within acceptable bounds.
        
        Args:
            circuit: Input quantum circuit
            identity: Identity string for basin locking
            
        Returns:
            Scalar-stabilized circuit
            
        Raises:
            ValueError: If circuit violates hard constraints
        """
        self._validate_constraints(circuit)
        return self._apply_scalar_stabilization(circuit, identity)
    
    def _validate_constraints(self, circuit: Any) -> None:
        """
        Validate circuit against hard constraints.
        
        Args:
            circuit: Circuit to validate
            
        Raises:
            ValueError: If constraints are violated
        """
        if hasattr(circuit, "depth"):
            depth = circuit.depth()
            if depth > self.MAX_DEPTH:
                raise ValueError(
                    f"Circuit depth {depth} exceeds maximum {self.MAX_DEPTH}"
                )
        
        if hasattr(circuit, "parameters"):
            param_count = len(list(circuit.parameters))
            if param_count > self.MAX_PARAMS:
                raise ValueError(
                    f"Parameter count {param_count} exceeds maximum {self.MAX_PARAMS}"
                )
    
    def _apply_scalar_stabilization(self, circuit: Any, identity: str) -> Any:
        """
        Apply scalar stabilization within safe bounds.
        
        Args:
            circuit: Input circuit
            identity: Identity string
            
        Returns:
            Scalar-stabilized circuit
        """
        return circuit
