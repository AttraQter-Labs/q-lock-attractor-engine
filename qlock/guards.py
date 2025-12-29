"""
Q-LOCK Guards: Safety and admissibility checks.

Implements hard refusal logic for unsafe operational regimes.
"""

from typing import Dict, Any


class Guards:
    """
    Guard system for Q-LOCK engine.
    
    Enforces:
    - Noise threshold limits
    - Variance constraints
    - Scalar mode admissibility
    - Hard refusal of unsafe configurations
    """
    
    def __init__(self, noise_threshold: float = 0.15, variance_limit: float = 0.25):
        self.noise_threshold = noise_threshold
        self.variance_limit = variance_limit
        
    def check_admissibility(self, circuit: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if circuit/params are admissible for Q-LOCK execution.
        
        Args:
            circuit: Input circuit or computational graph
            params: Execution parameters
            
        Returns:
            Dict with 'admissible' bool and 'reason' string
        """
        # Noise level check
        estimated_noise = params.get("estimated_noise", 0.0)
        if estimated_noise > self.noise_threshold:
            return {
                "admissible": False,
                "reason": f"Noise level {estimated_noise:.3f} exceeds threshold {self.noise_threshold}"
            }
        
        # Variance check
        estimated_variance = params.get("estimated_variance", 0.0)
        if estimated_variance > self.variance_limit:
            return {
                "admissible": False,
                "reason": f"Variance {estimated_variance:.3f} exceeds limit {self.variance_limit}"
            }
        
        # Circuit complexity check
        if hasattr(circuit, "depth"):
            depth = circuit.depth()
            if depth > 1000:
                return {
                    "admissible": False,
                    "reason": f"Circuit depth {depth} exceeds maximum supported depth (1000)"
                }
        
        return {
            "admissible": True,
            "reason": "Passed all guard checks"
        }
    
    def check_scalar_admissibility(self, circuit: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Strict admissibility check for scalar_guarded mode.
        
        Scalar mode operates under stricter constraints and will refuse
        execution outside narrow operational boundaries.
        
        Args:
            circuit: Input circuit or computational graph
            params: Execution parameters
            
        Returns:
            Dict with 'admissible' bool and 'reason' string
        """
        # First check standard admissibility
        base_check = self.check_admissibility(circuit, params)
        if not base_check["admissible"]:
            return base_check
        
        # Scalar mode requires explicit opt-in
        if not params.get("scalar_mode_confirmed", False):
            return {
                "admissible": False,
                "reason": "Scalar mode requires explicit confirmation (scalar_mode_confirmed=True)"
            }
        
        # Stricter noise threshold for scalar mode
        estimated_noise = params.get("estimated_noise", 0.0)
        scalar_noise_threshold = self.noise_threshold * 0.5
        if estimated_noise > scalar_noise_threshold:
            return {
                "admissible": False,
                "reason": f"Scalar mode noise {estimated_noise:.3f} exceeds strict threshold {scalar_noise_threshold:.3f}"
            }
        
        # Stricter variance limit for scalar mode
        estimated_variance = params.get("estimated_variance", 0.0)
        scalar_variance_limit = self.variance_limit * 0.5
        if estimated_variance > scalar_variance_limit:
            return {
                "admissible": False,
                "reason": f"Scalar mode variance {estimated_variance:.3f} exceeds strict limit {scalar_variance_limit:.3f}"
            }
        
        # Check for unsafe parameter regimes
        if params.get("temperature", 1.0) > 1.5:
            return {
                "admissible": False,
                "reason": "Temperature parameter exceeds scalar mode safety limit (1.5)"
            }
        
        return {
            "admissible": True,
            "reason": "Passed all scalar mode guard checks"
        }
    
    def update_thresholds(self, noise_threshold: float = None, variance_limit: float = None):
        """Update guard thresholds dynamically."""
        if noise_threshold is not None:
            self.noise_threshold = noise_threshold
        if variance_limit is not None:
            self.variance_limit = variance_limit
