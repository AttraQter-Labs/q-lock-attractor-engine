"""
Q-LOCK History: Procedural history (Π) preservation.

Maintains complete execution history without erasure.
"""

from typing import List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class HistoryEntry:
    """Single entry in procedural history."""
    timestamp: datetime
    mode: str
    input_summary: Dict[str, Any]
    output_summary: Dict[str, Any]
    metrics: Dict[str, float]
    verdict: str = "ACCEPTED"


class History:
    """
    Procedural history (Π) manager.
    
    Q-LOCK preserves complete procedural history instead of erasing it.
    This provides audit trails, reproducibility, and transparency.
    """
    
    def __init__(self):
        self.entries: List[HistoryEntry] = []
        
    def record(
        self,
        mode: str,
        input_circuit: Any,
        output_circuit: Any,
        metrics: Dict[str, float],
        verdict: str = "ACCEPTED"
    ):
        """
        Record a new entry in procedural history.
        
        Args:
            mode: Q-LOCK mode used
            input_circuit: Original input circuit
            output_circuit: Processed output circuit
            metrics: Computed metrics
            verdict: Execution verdict (ACCEPTED/REFUSED)
        """
        entry = HistoryEntry(
            timestamp=datetime.now(),
            mode=mode,
            input_summary=self._summarize_circuit(input_circuit),
            output_summary=self._summarize_circuit(output_circuit),
            metrics=metrics,
            verdict=verdict
        )
        self.entries.append(entry)
    
    def get_latest(self) -> Dict[str, Any]:
        """
        Get most recent history entry.
        
        Returns:
            Dictionary representation of latest entry
        """
        if not self.entries:
            return {}
        
        latest = self.entries[-1]
        return {
            "timestamp": latest.timestamp.isoformat(),
            "mode": latest.mode,
            "input_summary": latest.input_summary,
            "output_summary": latest.output_summary,
            "metrics": latest.metrics,
            "verdict": latest.verdict
        }
    
    def get_all(self) -> List[Dict[str, Any]]:
        """
        Get complete procedural history.
        
        Returns:
            List of all history entries as dictionaries
        """
        return [
            {
                "timestamp": entry.timestamp.isoformat(),
                "mode": entry.mode,
                "input_summary": entry.input_summary,
                "output_summary": entry.output_summary,
                "metrics": entry.metrics,
                "verdict": entry.verdict
            }
            for entry in self.entries
        ]
    
    def export_json(self, filepath: str):
        """
        Export history to JSON file.
        
        Args:
            filepath: Path to output JSON file
        """
        with open(filepath, 'w') as f:
            json.dump(self.get_all(), f, indent=2)
    
    def reset(self):
        """Clear history (use with caution - violates Π preservation principle)."""
        self.entries.clear()
    
    def _summarize_circuit(self, circuit: Any) -> Dict[str, Any]:
        """
        Create summary of circuit for history recording.
        
        Args:
            circuit: Circuit to summarize
            
        Returns:
            Dictionary with circuit metadata
        """
        summary = {
            "type": type(circuit).__name__
        }
        
        # Extract common circuit properties if available
        if hasattr(circuit, "num_qubits"):
            summary["num_qubits"] = circuit.num_qubits
        if hasattr(circuit, "depth"):
            summary["depth"] = circuit.depth()
        if hasattr(circuit, "size"):
            summary["size"] = circuit.size()
        
        return summary
