"""
Adapter module for ValidatorEngine.

Provides a simplified interface that accepts distributions directly.
"""

import numpy as np
from qlock.engine.core import ValidatorEngine, EngineContext, EngineMetrics, EngineRefusal


class ValidatorEngineAdapter:
    """
    Adapter for ValidatorEngine that works with probability distributions.
    
    Simplifies the canonical engine interface for demonstration purposes.
    """
    
    def __init__(self):
        """Initialize the adapter."""
        self.refusal_log = []
    
    def apply(self, distribution: np.ndarray, mode: str, meta: dict = None) -> dict:
        """
        Apply stabilization to a probability distribution.
        
        Args:
            distribution: Input probability distribution
            mode: Stabilization mode (BASELINE, FIDELITY, WATERMARK, WITNESS_PHASE)
            meta: Optional metadata
            
        Returns:
            Verdict dictionary with status and processed distribution
        """
        meta = meta or {}
        
        # BASELINE mode returns input unchanged
        if mode == "BASELINE":
            return {
                "status": "APPLIED",
                "distribution": distribution.copy(),
                "mode": "BASELINE",
                "metadata": meta
            }
        
        # Create context from distribution characteristics
        context = self._create_context_from_distribution(distribution)
        
        # Create initial metrics
        initial_metrics = self._create_initial_metrics(distribution)
        
        # Create engine
        engine = ValidatorEngine(context)
        
        # Map mode names
        mode_map = {
            "FIDELITY": "fidelity",
            "WATERMARK": "fidelity",  # Watermark uses fidelity internally
            "WITNESS_PHASE": "witness_phase"
        }
        
        if mode not in mode_map:
            return {
                "status": "REFUSED",
                "reason": f"Unknown mode: {mode}",
                "metadata": meta
            }
        
        try:
            # Apply stabilization
            final_metrics = engine.apply(initial_metrics, mode_map[mode])
            
            # Apply metrics back to distribution
            stabilized_dist = self._apply_metrics_to_distribution(
                distribution, initial_metrics, final_metrics
            )
            
            return {
                "status": "APPLIED",
                "distribution": stabilized_dist,
                "mode": mode,
                "initial_metrics": {
                    "coherence_r": initial_metrics.coherence_r,
                    "entropy_h": initial_metrics.entropy_h,
                    "variance_v": initial_metrics.variance_v,
                    "bias_retention": initial_metrics.bias_retention
                },
                "final_metrics": {
                    "coherence_r": final_metrics.coherence_r,
                    "entropy_h": final_metrics.entropy_h,
                    "variance_v": final_metrics.variance_v,
                    "bias_retention": final_metrics.bias_retention
                },
                "metadata": meta
            }
            
        except EngineRefusal as e:
            self.refusal_log.append({
                "mode": mode,
                "reason": str(e),
                "metadata": meta
            })
            return {
                "status": "REFUSED",
                "reason": str(e),
                "metadata": meta
            }
    
    def _create_context_from_distribution(self, dist: np.ndarray) -> EngineContext:
        """Create engine context from distribution characteristics."""
        # Estimate noise from distribution entropy
        entropy = -np.sum(dist * np.log(dist + 1e-10))
        noise = min(0.01, entropy / 10.0)
        
        # Estimate phase dispersion from variance
        variance = np.var(dist)
        phase_dispersion = min(0.15, variance * 2.0)
        
        # Estimate procedural disorder from distribution spread
        procedural_disorder = min(0.3, variance * 3.0)
        
        return EngineContext(
            noise=noise,
            depth=len(dist),
            phase_dispersion=phase_dispersion,
            procedural_disorder=procedural_disorder,
            topology="low"
        )
    
    def _create_initial_metrics(self, dist: np.ndarray) -> EngineMetrics:
        """Create initial metrics from distribution."""
        # Coherence based on peak concentration
        coherence_r = np.max(dist) / np.mean(dist)
        coherence_r = min(1.0, coherence_r / 10.0)
        
        # Entropy
        entropy_h = -np.sum(dist * np.log(dist + 1e-10)) / np.log(len(dist))
        
        # Variance
        variance_v = np.var(dist)
        
        # Bias retention (based on top-k concentration)
        sorted_dist = np.sort(dist)[::-1]
        bias_retention = np.sum(sorted_dist[:3]) / np.sum(dist)
        
        return EngineMetrics(
            coherence_r=coherence_r,
            entropy_h=entropy_h,
            variance_v=variance_v,
            bias_retention=bias_retention
        )
    
    def _apply_metrics_to_distribution(
        self, 
        dist: np.ndarray, 
        initial: EngineMetrics, 
        final: EngineMetrics
    ) -> np.ndarray:
        """
        Apply metric improvements back to distribution.
        
        This is a simplified transformation that demonstrates the effect.
        Real implementation would use the full attractor logic.
        """
        # Calculate improvement ratios
        entropy_ratio = final.entropy_h / (initial.entropy_h + 1e-10)
        variance_ratio = final.variance_v / (initial.variance_v + 1e-10)
        
        # Apply mild sharpening based on entropy reduction
        if entropy_ratio < 1.0:
            # Sharpen peaks slightly
            sharpened = dist ** (1.0 / (entropy_ratio + 0.5))
            dist = sharpened / sharpened.sum()
        
        # Apply variance reduction
        if variance_ratio < 1.0:
            # Reduce noise slightly
            mean_val = np.mean(dist)
            dist = dist + (mean_val - dist) * (1.0 - variance_ratio) * 0.1
            dist = np.maximum(dist, 0)
            dist = dist / dist.sum()
        
        return dist
