"""
Perturbation functions for Q-LOCK Attractor Engine.

This module provides utilities for computing identity-locked perturbations
to quantum circuit parameters.
"""

import numpy as np


def golden_phase_map(vec: np.ndarray) -> np.ndarray:
    """
    Apply golden-ratio inspired phase mapping to identity vector.
    
    This is a simplified public version of the proprietary attractor logic.
    
    Args:
        vec: Input identity vector
        
    Returns:
        Transformed identity signature vector
    """
    phi = (1 + np.sqrt(5)) / 2  # Golden ratio
    
    # Apply golden-ratio phase structure
    phases = np.exp(1j * 2 * np.pi * np.arange(len(vec)) * phi)
    transformed = vec * phases.real
    
    # Normalize
    norm = np.linalg.norm(transformed)
    if norm > 0:
        transformed = transformed / norm
        
    return transformed


def compute_perturbation(identity_sig: np.ndarray, gate_index: int, epsilon: float = 0.01) -> float:
    """
    Compute perturbation value for a specific gate.
    
    Args:
        identity_sig: Identity signature vector
        gate_index: Index of the gate to perturb
        epsilon: Perturbation scale factor
        
    Returns:
        Perturbation value to add to gate parameter
    """
    # Use identity signature to deterministically compute perturbation
    idx = gate_index % len(identity_sig)
    base_value = identity_sig[idx]
    
    # Small, bounded perturbation
    return epsilon * base_value
