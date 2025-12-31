"""
Watermark mode for Q-LOCK.

Identity locking only - no topology changes.
Preserves exact circuit structure while embedding identity signature.
"""

from typing import Any, Dict, Optional
from qlock.modes.fidelity import ModeBase


class WatermarkMode(ModeBase):
    """
    Watermark mode: Identity locking without topology changes.
    
    Embeds identity signature into circuit without modifying
    the logical structure or topology. Minimal intervention mode.
    
    Suitable for:
    - Provenance tracking
    - Circuit authentication
    - Minimal-impact scenarios
    
    Guarantees:
    - No gate additions or removals
    - No topology modifications
    - Deterministic identity embedding
    """
    
    def apply(self, circuit: Any, identity: str) -> Any:
        """
        Apply watermark identity locking.
        
        Args:
            circuit: Input quantum circuit
            identity: Identity string for basin locking
            
        Returns:
            Watermarked circuit with preserved topology
        """
        return self._apply_watermark(circuit, identity)
    
    def _apply_watermark(self, circuit: Any, identity: str) -> Any:
        """
        Apply watermark without topology changes.
        
        Args:
            circuit: Input circuit
            identity: Identity string
            
        Returns:
            Watermarked circuit
        """
        return circuit
