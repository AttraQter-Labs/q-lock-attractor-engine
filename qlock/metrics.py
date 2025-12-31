"""
Metrics collection for Q-LOCK engine.

Tracks coherence, entropy, variance, and KL divergence.
"""

from typing import Any, Dict
import time


class Metrics:
    """
    Collects and tracks Q-LOCK performance metrics.
    
    Monitors coherence, entropy, variance, and divergence measures
    to assess stabilization quality.
    """
    
    def __init__(self):
        """Initialize metrics tracking."""
        self.coherence_values = []
        self.entropy_values = []
        self.variance_values = []
        self.kl_divergence_values = []
        self.start_time = time.time()
        self.update_count = 0
    
    def update(self, metrics_dict: Dict[str, float]) -> None:
        """
        Update metrics with new observations.
        
        Args:
            metrics_dict: Dictionary containing metric values
        """
        self.update_count += 1
        
        if "coherence" in metrics_dict:
            self.coherence_values.append(metrics_dict["coherence"])
        
        if "entropy" in metrics_dict:
            self.entropy_values.append(metrics_dict["entropy"])
        
        if "variance" in metrics_dict:
            self.variance_values.append(metrics_dict["variance"])
        
        if "kl_divergence" in metrics_dict:
            self.kl_divergence_values.append(metrics_dict["kl_divergence"])
    
    def snapshot(self) -> Dict[str, Any]:
        """
        Get current metrics snapshot.
        
        Returns:
            Dictionary containing current metric statistics
        """
        return {
            "coherence": self._compute_stats(self.coherence_values),
            "entropy": self._compute_stats(self.entropy_values),
            "variance": self._compute_stats(self.variance_values),
            "kl_divergence": self._compute_stats(self.kl_divergence_values),
            "update_count": self.update_count,
            "elapsed_time": time.time() - self.start_time,
        }
    
    def _compute_stats(self, values: list) -> Dict[str, Any]:
        """
        Compute statistics for a list of values.
        
        Args:
            values: List of numeric values
            
        Returns:
            Dictionary with mean, min, max, latest
        """
        if not values:
            return {"mean": None, "min": None, "max": None, "latest": None}
        
        return {
            "mean": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
            "latest": values[-1],
        }
    
    def get_coherence(self) -> float:
        """
        Get latest coherence value.
        
        Returns:
            Latest coherence measurement
        """
        return self.coherence_values[-1] if self.coherence_values else 0.0
    
    def get_entropy(self) -> float:
        """
        Get latest entropy value.
        
        Returns:
            Latest entropy measurement
        """
        return self.entropy_values[-1] if self.entropy_values else 0.0
    
    def get_variance(self) -> float:
        """
        Get latest variance value.
        
        Returns:
            Latest variance measurement
        """
        return self.variance_values[-1] if self.variance_values else 0.0
    
    def get_kl_divergence(self) -> float:
        """
        Get latest KL divergence value.
        
        Returns:
            Latest KL divergence measurement
        """
        return self.kl_divergence_values[-1] if self.kl_divergence_values else 0.0
