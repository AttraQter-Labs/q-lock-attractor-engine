"""
Policy engine defining which stabilization modes are admissible.
This module is authoritative.
"""

DEFAULT_ALLOWED_MODES = [
    "fidelity",
    "watermark",
    "witness_phase"
]

EXPERIMENTAL_MODES = [
    "scalar"
]


def is_mode_allowed(mode: str) -> bool:
    """
    Check if a stabilization mode is allowed by policy.
    
    Args:
        mode: Mode name to check
        
    Returns:
        True if mode is in default allowed modes, False otherwise
    """
    return mode in DEFAULT_ALLOWED_MODES


def is_scalar_allowed(
    noise_level: float,
    phase_dispersion: float,
    procedural_disorder: float,
    topology_safe: bool
) -> bool:
    """
    Scalar mode is allowed only when ALL conditions are satisfied.
    
    Args:
        noise_level: Estimated noise level
        phase_dispersion: Phase dispersion measure
        procedural_disorder: Procedural disorder measure
        topology_safe: Whether topology is non-pathological
        
    Returns:
        True if ALL scalar conditions are met, False otherwise
    """
    NOISE_THRESHOLD = 0.05
    PHASE_THRESHOLD = 0.1
    DISORDER_THRESHOLD = 0.15
    
    return (
        noise_level <= NOISE_THRESHOLD and
        phase_dispersion <= PHASE_THRESHOLD and
        procedural_disorder <= DISORDER_THRESHOLD and
        topology_safe
    )
