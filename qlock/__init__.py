"""
Q-LOCK: Attractor-Based Coherence Stabilization Engine

An enterprise-grade control and stabilization layer for quantum circuits
and high-noise computational systems.
"""

from .engine import QLockEngine, QLockConfig, QLockResult
from .guards import Guards
from .metrics import Metrics
from .observer import Observer
from .history import History

__version__ = "1.0.0"
__all__ = [
    "QLockEngine",
    "QLockConfig",
    "QLockResult",
    "Guards",
    "Metrics",
    "Observer",
    "History",
]
