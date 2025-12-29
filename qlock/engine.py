"""
Q-LOCK Engine: Central orchestration for coherence stabilization.

Handles mode selection, refusal logic, and metric aggregation.
"""

from typing import Dict, Any, Optional, Literal
from dataclasses import dataclass
from .guards import Guards
from .metrics import Metrics
from .observer import Observer
from .history import History
from .modes import fidelity, witness_phase, watermark, scalar_guarded


@dataclass
class QLockConfig:
    """Configuration for Q-LOCK engine execution."""
    mode: Literal["fidelity", "witness_phase", "watermark", "scalar_guarded"]
    identity: Optional[str] = None
    enable_refusal: bool = True
    noise_threshold: float = 0.15
    variance_limit: float = 0.25


@dataclass
class QLockResult:
    """Result of Q-LOCK engine execution."""
    success: bool
    mode: str
    verdict: str
    metrics: Dict[str, float]
    refusal_reason: Optional[str] = None
    history: Optional[Dict[str, Any]] = None


class QLockEngine:
    """
    Q-LOCK attractor-based coherence stabilization engine.
    
    This is NOT an optimizer, error corrector, or simulator.
    It is a control, stabilization, and refusal layer.
    
    Core capabilities:
    - Basin identity preservation
    - Fidelity and variance improvement in low-noise regimes
    - Explicit refusal of harmful contractions
    - Procedural history (Π) preservation
    """
    
    def __init__(self, config: QLockConfig):
        self.config = config
        self.guards = Guards(
            noise_threshold=config.noise_threshold,
            variance_limit=config.variance_limit
        )
        self.metrics = Metrics()
        self.observer = Observer()
        self.history = History()
        
    def execute(self, circuit: Any, params: Optional[Dict[str, Any]] = None) -> QLockResult:
        """
        Execute Q-LOCK on provided circuit with configured mode.
        
        Args:
            circuit: Input quantum circuit or computational graph
            params: Optional execution parameters
            
        Returns:
            QLockResult with execution outcome and metrics
        """
        params = params or {}
        
        # Pre-execution guard checks
        if self.config.enable_refusal:
            guard_result = self.guards.check_admissibility(circuit, params)
            if not guard_result["admissible"]:
                return QLockResult(
                    success=False,
                    mode=self.config.mode,
                    verdict="REFUSED",
                    metrics={},
                    refusal_reason=guard_result["reason"]
                )
        
        # Mode-specific execution
        try:
            if self.config.mode == "fidelity":
                result = fidelity.execute(circuit, params, self.observer)
            elif self.config.mode == "witness_phase":
                result = witness_phase.execute(circuit, params, self.observer)
            elif self.config.mode == "watermark":
                if not self.config.identity:
                    return QLockResult(
                        success=False,
                        mode=self.config.mode,
                        verdict="REFUSED",
                        metrics={},
                        refusal_reason="Identity required for watermark mode"
                    )
                result = watermark.execute(circuit, self.config.identity, params, self.observer)
            elif self.config.mode == "scalar_guarded":
                # Scalar mode requires explicit opt-in and stricter checks
                guard_result = self.guards.check_scalar_admissibility(circuit, params)
                if not guard_result["admissible"]:
                    return QLockResult(
                        success=False,
                        mode=self.config.mode,
                        verdict="REFUSED",
                        metrics={},
                        refusal_reason=guard_result["reason"]
                    )
                result = scalar_guarded.execute(circuit, params, self.observer)
            else:
                return QLockResult(
                    success=False,
                    mode=self.config.mode,
                    verdict="ERROR",
                    metrics={},
                    refusal_reason=f"Unknown mode: {self.config.mode}"
                )
            
            # Compute metrics
            metrics = self.metrics.compute(result["circuit"], circuit, self.observer)
            
            # Record history
            self.history.record(
                mode=self.config.mode,
                input_circuit=circuit,
                output_circuit=result["circuit"],
                metrics=metrics
            )
            
            return QLockResult(
                success=True,
                mode=self.config.mode,
                verdict="ACCEPTED",
                metrics=metrics,
                history=self.history.get_latest()
            )
            
        except Exception as e:
            return QLockResult(
                success=False,
                mode=self.config.mode,
                verdict="ERROR",
                metrics={},
                refusal_reason=f"Execution error: {str(e)}"
            )
    
    def get_history(self) -> Dict[str, Any]:
        """Return complete procedural history (Π)."""
        return self.history.get_all()
    
    def reset(self):
        """Reset engine state and history."""
        self.observer.reset()
        self.history.reset()
