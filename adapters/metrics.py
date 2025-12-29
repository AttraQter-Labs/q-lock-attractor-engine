"""
Metrics summarization for OCIR-PIP Tractor Engine demonstrations.
"""

import numpy as np


def summarize_metrics(p_before: np.ndarray, p_after: np.ndarray) -> dict:
    """
    Compute summary metrics comparing before/after distributions.
    
    Args:
        p_before: Distribution before stabilization
        p_after: Distribution after stabilization
        
    Returns:
        Dictionary of computed metrics
    """
    metrics = {}
    
    # Fidelity (overlap)
    metrics["fidelity"] = float(np.sum(np.sqrt(p_before * p_after)))
    
    # Total variation distance
    metrics["tv_distance"] = float(0.5 * np.sum(np.abs(p_before - p_after)))
    
    # KL divergence (with small epsilon for numerical stability)
    eps = 1e-10
    metrics["kl_divergence"] = float(np.sum(
        p_before * np.log((p_before + eps) / (p_after + eps))
    ))
    
    # Entropy before and after
    metrics["entropy_before"] = float(-np.sum(p_before * np.log(p_before + eps)))
    metrics["entropy_after"] = float(-np.sum(p_after * np.log(p_after + eps)))
    metrics["entropy_delta"] = metrics["entropy_after"] - metrics["entropy_before"]
    
    # Variance before and after
    metrics["variance_before"] = float(np.var(p_before))
    metrics["variance_after"] = float(np.var(p_after))
    metrics["variance_delta"] = metrics["variance_after"] - metrics["variance_before"]
    
    # Peak concentration (max probability)
    metrics["peak_before"] = float(np.max(p_before))
    metrics["peak_after"] = float(np.max(p_after))
    metrics["peak_delta"] = metrics["peak_after"] - metrics["peak_before"]
    
    # Effective dimension (inverse participation ratio)
    metrics["eff_dim_before"] = float(1.0 / np.sum(p_before ** 2))
    metrics["eff_dim_after"] = float(1.0 / np.sum(p_after ** 2))
    
    return metrics
