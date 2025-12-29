"""
Q-LOCK: Attractor-Based Coherence Stabilization and Safety Engine

A control, stabilization, and refusal layer for quantum circuits
and high-noise computational systems.
"""

from qlock.engine import QLockEngine
from qlock.guards import Guard, NoiseGuard, ScalarGuard
from qlock.metrics import Metrics
from qlock.observer import Observer
from qlock.history import History

__version__ = "0.1.0"
__all__ = [
    "QLockEngine",
    "Guard",
    "NoiseGuard",
    "ScalarGuard",
    "Metrics",
    "Observer",
    "History",
]
