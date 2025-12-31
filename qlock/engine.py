"""
Central orchestration logic for Q-LOCK engine.

Handles mode selection, refusal verdicts, and metric aggregation.
"""

from typing import Any, Dict, Optional
from qlock.guards import Guard, NoiseGuard, ScalarGuard
from qlock.metrics import Metrics
from qlock.observer import Observer
from qlock.history import History
from qlock.modes.fidelity import FidelityMode
from qlock.modes.witness_phase import WitnessPhaseMode
from qlock.modes.watermark import WatermarkMode
from qlock.modes.scalar_guarded import ScalarGuardedMode


class QLockEngine:
    """
    Q-LOCK Attractor Engine for coherence stabilization.
    
    Provides mode arbitration, refusal handling, and metric aggregation
    for quantum circuit stabilization and safety.
    """
    
    SUPPORTED_MODES = {
        "fidelity": FidelityMode,
        "witness_phase": WitnessPhaseMode,
        "watermark": WatermarkMode,
        "scalar_guarded": ScalarGuardedMode,
    }
    
    def __init__(self, mode: str = "fidelity", config: Optional[Dict[str, Any]] = None):
        """
        Initialize Q-LOCK engine with specified mode.
        
        Args:
            mode: Operating mode (fidelity, witness_phase, watermark, scalar_guarded)
            config: Optional configuration dictionary
        """
        if mode not in self.SUPPORTED_MODES:
            raise ValueError(
                f"Unsupported mode '{mode}'. "
                f"Supported modes: {', '.join(self.SUPPORTED_MODES.keys())}"
            )
        
        self.mode = mode
        self.config = config or {}
        self.mode_handler = self.SUPPORTED_MODES[mode](self.config)
        
        self.guards = [NoiseGuard(self.config), ScalarGuard(self.config)]
        self.metrics = Metrics()
        self.observer = Observer()
        self.history = History()
        
        self.refused_count = 0
        self.processed_count = 0
    
    def process(self, circuit: Any, identity: str) -> Dict[str, Any]:
        """
        Process a quantum circuit through Q-LOCK stabilization.
        
        Args:
            circuit: Quantum circuit to process
            identity: Identity string for basin locking
            
        Returns:
            Dictionary containing:
                - status: "accepted" or "refused"
                - circuit: Processed circuit (if accepted)
                - verdict: Refusal reason (if refused)
                - metrics: Current metrics snapshot
                - history_entry: Procedural history entry
        """
        self.processed_count += 1
        
        verdict = self._evaluate_guards(circuit, identity)
        if verdict["refused"]:
            self.refused_count += 1
            self.history.record_refusal(circuit, identity, verdict["reason"])
            return {
                "status": "refused",
                "verdict": verdict["reason"],
                "metrics": self.metrics.snapshot(),
                "history_entry": self.history.last_entry(),
            }
        
        processed_circuit = self.mode_handler.apply(circuit, identity)
        
        self.observer.observe(circuit, processed_circuit)
        metrics_update = self.observer.compute_metrics()
        self.metrics.update(metrics_update)
        
        self.history.record_acceptance(circuit, processed_circuit, identity, self.mode)
        
        return {
            "status": "accepted",
            "circuit": processed_circuit,
            "metrics": self.metrics.snapshot(),
            "history_entry": self.history.last_entry(),
        }
    
    def _evaluate_guards(self, circuit: Any, identity: str) -> Dict[str, Any]:
        """
        Evaluate all guards to determine if processing should be refused.
        
        Args:
            circuit: Quantum circuit to evaluate
            identity: Identity string
            
        Returns:
            Dictionary with 'refused' boolean and 'reason' string
        """
        for guard in self.guards:
            verdict = guard.evaluate(circuit, identity, self.mode)
            if verdict["refused"]:
                return verdict
        
        return {"refused": False, "reason": None}
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get current metrics snapshot.
        
        Returns:
            Dictionary of current metrics
        """
        return self.metrics.snapshot()
    
    def get_history(self, limit: Optional[int] = None) -> list:
        """
        Get procedural history.
        
        Args:
            limit: Optional limit on number of entries to return
            
        Returns:
            List of history entries
        """
        return self.history.get_entries(limit)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get engine statistics.
        
        Returns:
            Dictionary containing processing statistics
        """
        return {
            "mode": self.mode,
            "processed_count": self.processed_count,
            "refused_count": self.refused_count,
            "acceptance_rate": (
                (self.processed_count - self.refused_count) / self.processed_count
                if self.processed_count > 0
                else 0.0
            ),
        }
