"""
Public client stub.
No secret logic.
Safe for distribution.
"""

from typing import Any, Dict, Optional
from qlock.engine.core import QLockEngine


class QLockClient:
    """
    Public API client for Q-LOCK.
    
    This is a safe distribution interface with no proprietary logic exposed.
    """
    
    def __init__(self, mode: str = "fidelity", config: Optional[Dict[str, Any]] = None):
        """
        Initialize Q-LOCK client.
        
        Args:
            mode: Stabilization mode (fidelity, watermark, witness_phase)
            config: Optional configuration
        """
        self.engine = QLockEngine(mode=mode, config=config)
    
    def stabilize(self, circuit: Any, identity: str) -> Dict[str, Any]:
        """
        Stabilize a quantum circuit.
        
        Args:
            circuit: Quantum circuit (Qiskit QuantumCircuit or QASM string)
            identity: Identity string for procedural locking
            
        Returns:
            Result dictionary with status and stabilized circuit or refusal reason
        """
        return self.engine.process(circuit, identity)
    
    def get_refusals(self):
        """Get log of refusals."""
        return self.engine.get_refusal_log()
