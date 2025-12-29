"""
Reporting utilities for OCIR-PIP Tractor Engine demonstrations.
"""

import json
from typing import Dict, Any
from pathlib import Path


def make_report(mode: str, metrics: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a standardized report dictionary.
    
    Args:
        mode: Stabilization mode used
        metrics: Dictionary of computed metrics
        metadata: Additional metadata
        
    Returns:
        Complete report dictionary
    """
    report = {
        "mode": mode,
        "metrics": metrics,
        "metadata": metadata,
        "report_version": "1.0"
    }
    
    return report


def save_report(report: Dict[str, Any], filepath: str) -> None:
    """
    Save report to JSON file.
    
    Args:
        report: Report dictionary
        filepath: Path to save the report
    """
    # Create parent directory if needed
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save as formatted JSON
    with open(filepath, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Report saved: {filepath}")


def load_report(filepath: str) -> Dict[str, Any]:
    """
    Load report from JSON file.
    
    Args:
        filepath: Path to the report file
        
    Returns:
        Report dictionary
    """
    with open(filepath, 'r') as f:
        return json.load(f)
