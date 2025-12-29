"""
Type definitions for Q-LOCK.
"""

from typing import Dict, Any, List
from enum import Enum


class StabilizationMode(Enum):
    """Allowed stabilization modes."""
    FIDELITY = "fidelity"
    WATERMARK = "watermark"
    WITNESS_PHASE = "witness_phase"
    SCALAR = "scalar"


class CircuitStatus(Enum):
    """Circuit processing status."""
    ACCEPTED = "accepted"
    REFUSED = "refused"


class RefusalReason(Enum):
    """Standardized refusal reasons."""
    SCALAR_DISABLED = "scalar_mode_disabled_by_policy"
    EXCESSIVE_NOISE = "excessive_noise"
    PROCEDURAL_DISORDER = "excessive_procedural_disorder"
    UNSAFE_PHASE_SCALAR = "unsafe_phase_scalar_interaction"
    COHERENT_OVERROTATION = "coherent_overrotation"
    TOPOLOGY_PATHOLOGICAL = "topology_non_admissible"
