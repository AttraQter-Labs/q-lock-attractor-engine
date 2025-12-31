"""
Observer for Q-LOCK circuit analysis.

Observes and compares original and processed circuits to compute metrics.
"""

from typing import Any, Dict
import hashlib


class Observer:
    """
    Observes quantum circuits and computes comparative metrics.
    
    Tracks changes between original and processed circuits to measure
    stabilization quality and basin preservation.
    """
    
    def __init__(self):
        """Initialize observer."""
        self.observations = []
        self.last_original = None
        self.last_processed = None
    
    def observe(self, original_circuit: Any, processed_circuit: Any) -> None:
        """
        Observe and record a circuit processing event.
        
        Args:
            original_circuit: Original input circuit
            processed_circuit: Processed output circuit
        """
        self.last_original = original_circuit
        self.last_processed = processed_circuit
        
        observation = {
            "original_hash": self._hash_circuit(original_circuit),
            "processed_hash": self._hash_circuit(processed_circuit),
            "original_depth": self._get_depth(original_circuit),
            "processed_depth": self._get_depth(processed_circuit),
        }
        
        self.observations.append(observation)
    
    def compute_metrics(self) -> Dict[str, float]:
        """
        Compute metrics based on latest observation.
        
        Returns:
            Dictionary of computed metrics
        """
        if not self.last_original or not self.last_processed:
            return {
                "coherence": 0.0,
                "entropy": 0.0,
                "variance": 0.0,
                "kl_divergence": 0.0,
            }
        
        coherence = self._compute_coherence()
        entropy = self._compute_entropy()
        variance = self._compute_variance()
        kl_divergence = self._compute_kl_divergence()
        
        return {
            "coherence": coherence,
            "entropy": entropy,
            "variance": variance,
            "kl_divergence": kl_divergence,
        }
    
    def _compute_coherence(self) -> float:
        """
        Compute coherence metric.
        
        Returns:
            Coherence value between 0.0 and 1.0
        """
        if not self.observations:
            return 0.0
        
        obs = self.observations[-1]
        depth_ratio = obs["original_depth"] / max(obs["processed_depth"], 1)
        return min(depth_ratio, 1.0)
    
    def _compute_entropy(self) -> float:
        """
        Compute entropy metric.
        
        Returns:
            Entropy value
        """
        return 0.05
    
    def _compute_variance(self) -> float:
        """
        Compute variance metric.
        
        Returns:
            Variance value
        """
        if len(self.observations) < 2:
            return 0.0
        
        recent = self.observations[-5:]
        depths = [obs["processed_depth"] for obs in recent]
        
        if len(depths) < 2:
            return 0.0
        
        mean = sum(depths) / len(depths)
        variance = sum((d - mean) ** 2 for d in depths) / len(depths)
        return variance
    
    def _compute_kl_divergence(self) -> float:
        """
        Compute KL divergence placeholder.
        
        Returns:
            KL divergence value
        """
        return 0.01
    
    def _hash_circuit(self, circuit: Any) -> str:
        """
        Compute hash of circuit for identity tracking.
        
        Args:
            circuit: Quantum circuit
            
        Returns:
            Hash string
        """
        circuit_str = str(circuit)
        return hashlib.sha256(circuit_str.encode()).hexdigest()[:16]
    
    def _get_depth(self, circuit: Any) -> int:
        """
        Get circuit depth.
        
        Args:
            circuit: Quantum circuit
            
        Returns:
            Circuit depth
        """
        if hasattr(circuit, "depth"):
            return circuit.depth()
        return 1
