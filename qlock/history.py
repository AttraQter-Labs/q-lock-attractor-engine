"""
Procedural history tracking for Q-LOCK.

Preserves procedural history (Π) instead of erasing it.
"""

from typing import Any, Dict, List, Optional
import time
import hashlib


class History:
    """
    Tracks procedural history of Q-LOCK operations.
    
    Maintains a record of all circuit processing events,
    preserving basin identity and operational provenance.
    """
    
    def __init__(self, max_entries: int = 10000):
        """
        Initialize history tracking.
        
        Args:
            max_entries: Maximum number of entries to retain
        """
        self.entries = []
        self.max_entries = max_entries
    
    def record_acceptance(
        self,
        original_circuit: Any,
        processed_circuit: Any,
        identity: str,
        mode: str,
    ) -> None:
        """
        Record an accepted circuit processing event.
        
        Args:
            original_circuit: Original input circuit
            processed_circuit: Processed output circuit
            identity: Identity string used
            mode: Operating mode used
        """
        entry = {
            "timestamp": time.time(),
            "status": "accepted",
            "identity_hash": self._hash_identity(identity),
            "mode": mode,
            "original_signature": self._signature(original_circuit),
            "processed_signature": self._signature(processed_circuit),
        }
        
        self._add_entry(entry)
    
    def record_refusal(
        self,
        circuit: Any,
        identity: str,
        reason: str,
    ) -> None:
        """
        Record a refused circuit processing event.
        
        Args:
            circuit: Circuit that was refused
            identity: Identity string used
            reason: Reason for refusal
        """
        entry = {
            "timestamp": time.time(),
            "status": "refused",
            "identity_hash": self._hash_identity(identity),
            "circuit_signature": self._signature(circuit),
            "refusal_reason": reason,
        }
        
        self._add_entry(entry)
    
    def _add_entry(self, entry: Dict[str, Any]) -> None:
        """
        Add entry to history with size management.
        
        Args:
            entry: History entry to add
        """
        self.entries.append(entry)
        
        if len(self.entries) > self.max_entries:
            self.entries = self.entries[-self.max_entries:]
    
    def get_entries(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get history entries.
        
        Args:
            limit: Optional limit on number of entries
            
        Returns:
            List of history entries (most recent first)
        """
        entries = list(reversed(self.entries))
        
        if limit is not None:
            entries = entries[:limit]
        
        return entries
    
    def last_entry(self) -> Optional[Dict[str, Any]]:
        """
        Get most recent history entry.
        
        Returns:
            Most recent entry or None if history is empty
        """
        return self.entries[-1] if self.entries else None
    
    def get_acceptance_count(self) -> int:
        """
        Get count of accepted entries.
        
        Returns:
            Number of accepted entries
        """
        return sum(1 for e in self.entries if e.get("status") == "accepted")
    
    def get_refusal_count(self) -> int:
        """
        Get count of refused entries.
        
        Returns:
            Number of refused entries
        """
        return sum(1 for e in self.entries if e.get("status") == "refused")
    
    def _hash_identity(self, identity: str) -> str:
        """
        Hash identity string for privacy.
        
        Args:
            identity: Identity string
            
        Returns:
            Hash of identity
        """
        return hashlib.sha256(identity.encode()).hexdigest()[:16]
    
    def _signature(self, circuit: Any) -> str:
        """
        Generate signature for circuit.
        
        Args:
            circuit: Quantum circuit
            
        Returns:
            Circuit signature
        """
        circuit_str = str(circuit)
        return hashlib.sha256(circuit_str.encode()).hexdigest()[:16]
