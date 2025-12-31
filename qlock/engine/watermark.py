"""
Watermark mode:
Observer / identity locking.
No topology change.
No performance optimization.
"""

from typing import Any


def apply_watermark(circuit: Any, identity: str, config: dict = None) -> Any:
    """
    Apply watermark identity locking.
    
    Watermark mode:
    - Embeds identity signature
    - No topology changes
    - No performance optimization
    - Pure provenance tracking
    
    Args:
        circuit: Quantum circuit
        identity: Identity string for watermarking
        config: Optional configuration
        
    Returns:
        Watermarked circuit (topology unchanged)
    """
    # Identity locking logic would go here
    # For now, return circuit unchanged (preserves topology)
    return circuit
