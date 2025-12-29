"""
OCIR-PIP TRACTOR ENGINE — CANONICAL REFERENCE IMPLEMENTATION
Version: Ω-LOCKED
Status: REVIEWABLE / SAFE / NON-OPTIMIZING

This file intentionally implements:
- Fidelity Mode
- Witness + Phase Mode
- Scalar Mode (GUARDED — REFUSAL ONLY)

This engine:
- DOES NOT learn
- DOES NOT mutate topology
- DOES NOT optimize objectives
- DOES NOT suppress procedural divergence (Π)
- DOES enforce refusal boundaries

This is a stability-preserving, basin-pulling engine.
"""

from dataclasses import dataclass
from typing import Dict, Any, Literal
import math


# =========================
# Engine Exceptions
# =========================

class EngineRefusal(Exception):
    """Raised when a mode is not admissible under current conditions."""
    pass


# =========================
# Engine State Model
# =========================

@dataclass(frozen=True)
class EngineMetrics:
    coherence_r: float
    entropy_h: float
    variance_v: float
    bias_retention: float


@dataclass(frozen=True)
class EngineContext:
    noise: float
    depth: int
    phase_dispersion: float
    procedural_disorder: float  # Π disorder measure
    topology: Literal["low", "medium", "high"]


# =========================
# Core Engine
# =========================

class TractorEngine:
    """
    Canonical Tractor Engine

    All operations are:
    - Deterministic
    - Bounded
    - Refusal-aware
    """

    SCALAR_NOISE_LIMIT = 0.003
    SCALAR_PHASE_LIMIT = 0.2
    SCALAR_PI_LIMIT = 0.4

    def __init__(self, context: EngineContext):
        self.context = context

    # -------------------------
    # Public Entry Point
    # -------------------------

    def apply(self, metrics: EngineMetrics, mode: str) -> EngineMetrics:
        if mode == "fidelity":
            return self._fidelity(metrics)

        if mode == "witness_phase":
            return self._witness_phase(metrics)

        if mode == "scalar":
            return self._scalar(metrics)

        raise ValueError(f"Unknown mode: {mode}")

    # -------------------------
    # Fidelity Mode
    # -------------------------

    def _fidelity(self, m: EngineMetrics) -> EngineMetrics:
        """
        Fidelity mode:
        - Pulls toward existing basin
        - Reduces entropy and variance
        - Does NOT increase coherence beyond lawful bounds
        """
        return EngineMetrics(
            coherence_r=min(1.0, m.coherence_r + 0.05),
            entropy_h=max(0.0, m.entropy_h - 0.1),
            variance_v=max(0.0, m.variance_v - 0.01),
            bias_retention=m.bias_retention
        )

    # -------------------------
    # Witness + Phase Mode
    # -------------------------

    def _witness_phase(self, m: EngineMetrics) -> EngineMetrics:
        """
        Witness + Phase:
        - Rank-1 stabilization
        - Phase-aligned contraction
        - Preserves Π-divergence
        """
        return EngineMetrics(
            coherence_r=min(1.0, m.coherence_r + 0.08),
            entropy_h=max(0.0, m.entropy_h - 0.15),
            variance_v=max(0.0, m.variance_v - 0.02),
            bias_retention=min(1.0, m.bias_retention + 0.05)
        )

    # -------------------------
    # Scalar Mode (GUARDED)
    # -------------------------

    def _scalar(self, m: EngineMetrics) -> EngineMetrics:
        """
        Scalar mode is ONLY allowed under strict admissibility.
        Otherwise: HARD REFUSAL.
        """

        if not self._scalar_admissible():
            raise EngineRefusal(
                "Scalar mode refused: outside admissibility surface"
            )

        # Scalar never improves coherence — only variance
        return EngineMetrics(
            coherence_r=m.coherence_r,
            entropy_h=m.entropy_h,
            variance_v=max(0.0, m.variance_v - 0.03),
            bias_retention=m.bias_retention
        )

    # -------------------------
    # Scalar Guard Logic
    # -------------------------

    def _scalar_admissible(self) -> bool:
        c = self.context

        if c.noise > self.SCALAR_NOISE_LIMIT:
            return False

        if c.phase_dispersion > self.SCALAR_PHASE_LIMIT:
            return False

        if c.procedural_disorder > self.SCALAR_PI_LIMIT:
            return False

        if c.topology == "high":
            return False

        return True


# =========================
# Compatibility Layer for Legacy API
# =========================

from typing import Optional
from qlock.engine.refusal import Refusal


class QLockEngine:
    """
    Q-LOCK Engine - Compatibility wrapper for TractorEngine.
    
    Maintains backward compatibility while using canonical implementation.
    """
    
    def __init__(self, mode: str = "fidelity", config: Optional[Dict[str, Any]] = None):
        """
        Initialize Q-LOCK engine.
        
        Args:
            mode: Stabilization mode (fidelity, witness_phase, watermark, scalar)
            config: Optional configuration dictionary
            
        Raises:
            ValueError: If mode is not recognized
            Refusal: If scalar mode is requested (disabled by policy)
        """
        self.config = config or {}
        
        # Validate mode
        if mode not in ["fidelity", "watermark", "witness_phase", "scalar"]:
            raise ValueError(f"Unknown mode: {mode}")
        
        # Check policy for scalar
        if mode == "scalar":
            raise Refusal(
                reason="Scalar mode is disabled by policy",
                details={"mode": "scalar", "policy": "experimental_gated"}
            )
        
        self.mode = mode
        self._refusal_log = []
    
    def process(self, circuit: Any, identity: str) -> Dict[str, Any]:
        """
        Process circuit through Q-LOCK stabilization pipeline.
        
        Args:
            circuit: Quantum circuit to stabilize
            identity: Identity string for basin locking
            
        Returns:
            Dictionary with status, circuit (if accepted), or refusal reason
        """
        try:
            # Create context from circuit analysis
            context = self._create_context(circuit)
            
            # Create initial metrics
            initial_metrics = self._extract_metrics(circuit)
            
            # Create tractor engine
            engine = TractorEngine(context)
            
            # Map mode names
            mode_map = {
                "fidelity": "fidelity",
                "witness_phase": "witness_phase",
                "watermark": "fidelity",  # Watermark uses fidelity internally
                "scalar": "scalar"
            }
            
            # Apply stabilization
            final_metrics = engine.apply(initial_metrics, mode_map[self.mode])
            
            return {
                "status": "accepted",
                "circuit": circuit,  # In real impl, would modify circuit
                "mode": self.mode,
                "metrics": {
                    "coherence": final_metrics.coherence_r,
                    "entropy": final_metrics.entropy_h,
                    "variance": final_metrics.variance_v,
                    "bias_retention": final_metrics.bias_retention
                }
            }
            
        except EngineRefusal as e:
            # Convert to Refusal
            refusal = Refusal(reason=str(e))
            self._refusal_log.append(refusal.to_dict())
            return {
                "status": "refused",
                "reason": str(e),
                "details": {}
            }
        except Refusal as r:
            # Log refusal
            self._refusal_log.append(r.to_dict())
            return {
                "status": "refused",
                "reason": r.reason,
                "details": r.details
            }
    
    def _create_context(self, circuit: Any) -> EngineContext:
        """Create engine context from circuit."""
        # Simplified - real implementation would analyze circuit
        depth = circuit.depth() if hasattr(circuit, 'depth') else 10
        
        return EngineContext(
            noise=0.05,
            depth=depth,
            phase_dispersion=0.08,
            procedural_disorder=0.10,
            topology="low"
        )
    
    def _extract_metrics(self, circuit: Any) -> EngineMetrics:
        """Extract initial metrics from circuit."""
        # Simplified - real implementation would analyze circuit
        return EngineMetrics(
            coherence_r=0.85,
            entropy_h=0.20,
            variance_v=0.15,
            bias_retention=0.90
        )
    
    def get_refusal_log(self):
        """Get log of all refusals."""
        return list(self._refusal_log)
