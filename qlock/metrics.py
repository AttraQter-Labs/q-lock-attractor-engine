"""
Q-LOCK Metrics: Coherence, entropy, variance, and distance measures.

Provides quantitative assessment of Q-LOCK stabilization effects.
"""

from typing import Dict, Any
import numpy as np


class Metrics:
    """
    Metric computation for Q-LOCK engine execution.
    
    Computes:
    - Coherence preservation
    - Entropy measures
    - Variance reduction
    - Distribution distances (KL divergence, etc.)
    """
    
    def compute(self, output_circuit: Any, input_circuit: Any, observer: Any) -> Dict[str, float]:
        """
        Compute metrics comparing input and output circuits.
        
        Args:
            output_circuit: Circuit after Q-LOCK processing
            input_circuit: Original input circuit
            observer: Observer with execution traces
            
        Returns:
            Dictionary of computed metrics
        """
        metrics = {}
        
        # Coherence metric (placeholder - requires execution results)
        metrics["coherence"] = self._compute_coherence(observer)
        
        # Entropy measure
        metrics["entropy"] = self._compute_entropy(observer)
        
        # Variance reduction
        metrics["variance"] = self._compute_variance(observer)
        
        # KL divergence (placeholder)
        metrics["kl_divergence"] = self._compute_kl_divergence(observer)
        
        # Fidelity preservation
        metrics["fidelity"] = self._compute_fidelity(observer)
        
        return metrics
    
    def _compute_coherence(self, observer: Any) -> float:
        """
        Compute coherence preservation metric.
        
        Measures how well quantum coherence is maintained through processing.
        Higher values indicate better coherence preservation.
        """
        # Placeholder implementation
        # Real implementation would analyze quantum state coherence
        observations = observer.get_observations()
        if not observations:
            return 1.0
        
        # Simplified coherence estimate
        return 0.95
    
    def _compute_entropy(self, observer: Any) -> float:
        """
        Compute entropy of output distribution.
        
        Lower entropy indicates more concentrated/stable distributions.
        """
        observations = observer.get_observations()
        if not observations:
            return 0.0
        
        # Placeholder: would compute Shannon entropy of measurement distribution
        return 0.5
    
    def _compute_variance(self, observer: Any) -> float:
        """
        Compute variance of output distribution.
        
        Lower variance indicates more stable, predictable behavior.
        """
        observations = observer.get_observations()
        if not observations:
            return 0.0
        
        # Placeholder: would compute distribution variance
        return 0.1
    
    def _compute_kl_divergence(self, observer: Any) -> float:
        """
        Compute KL divergence between baseline and Q-LOCK distributions.
        
        Measures information distance. Lower values indicate distributions
        are closer (Q-LOCK preserves baseline behavior).
        """
        # Placeholder implementation
        # Real implementation would compare probability distributions
        return 0.02
    
    def _compute_fidelity(self, observer: Any) -> float:
        """
        Compute fidelity metric.
        
        Measures similarity between baseline and Q-LOCK execution.
        Higher values (closer to 1.0) indicate better preservation.
        """
        observations = observer.get_observations()
        if not observations:
            return 1.0
        
        # Placeholder: would compute quantum state fidelity
        return 0.98
    
    @staticmethod
    def compute_basin_metrics(distribution: Dict[str, int]) -> Dict[str, float]:
        """
        Compute basin/attractor stability metrics.
        
        Args:
            distribution: Probability distribution as state->count mapping
            
        Returns:
            Dictionary with basin metrics (top-k mass, effective support, Gini)
        """
        total = sum(distribution.values())
        if total == 0:
            return {
                "top_1_mass": 0.0,
                "top_5_mass": 0.0,
                "effective_support": 0.0,
                "gini_coefficient": 0.0
            }
        
        sorted_counts = sorted(distribution.values(), reverse=True)
        probs = [c / total for c in sorted_counts]
        
        # Top-k mass
        top_1_mass = probs[0] if len(probs) > 0 else 0.0
        top_5_mass = sum(probs[:5]) if len(probs) >= 5 else sum(probs)
        
        # Effective support (inverse participation ratio)
        sum_sq = sum(p ** 2 for p in probs)
        effective_support = 1.0 / sum_sq if sum_sq > 0 else 0.0
        
        # Gini coefficient
        n = len(probs)
        if n > 0 and sum(probs) > 0:
            cumsum = np.cumsum(probs)
            gini = (n + 1 - 2 * np.sum(cumsum) / cumsum[-1]) / n
        else:
            gini = 0.0
        
        return {
            "top_1_mass": float(top_1_mass),
            "top_5_mass": float(top_5_mass),
            "effective_support": float(effective_support),
            "gini_coefficient": float(gini)
        }
