"""
Q-LOCK Attractor Engine - Root package initialization.
"""
# Note: q_lock_engine is a standalone module at the root level
try:
    from q_lock_engine import QLockAttractorEngine, QLockConfig
except ImportError:
    pass  # Allow tests to run even if module not fully installed

__version__ = "0.1.0"

