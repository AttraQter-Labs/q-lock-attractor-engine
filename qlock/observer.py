"""
Q-LOCK Observer: Execution trace collection and monitoring.

Captures circuit execution behavior for metric computation.
"""

from typing import List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Observation:
    """Single observation from circuit execution."""
    timestamp: datetime
    event_type: str
    data: Dict[str, Any]


class Observer:
    """
    Observer for Q-LOCK engine execution.
    
    Collects execution traces, measurements, and intermediate states
    for metric computation and history recording.
    """
    
    def __init__(self):
        self.observations: List[Observation] = []
        self._active = True
        
    def record(self, event_type: str, data: Dict[str, Any]):
        """
        Record an observation during execution.
        
        Args:
            event_type: Type of event (e.g., 'measurement', 'gate', 'state')
            data: Event-specific data
        """
        if self._active:
            obs = Observation(
                timestamp=datetime.now(),
                event_type=event_type,
                data=data
            )
            self.observations.append(obs)
    
    def get_observations(self, event_type: str = None) -> List[Observation]:
        """
        Retrieve recorded observations.
        
        Args:
            event_type: Optional filter by event type
            
        Returns:
            List of observations (filtered if event_type specified)
        """
        if event_type:
            return [obs for obs in self.observations if obs.event_type == event_type]
        return self.observations
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics of observations.
        
        Returns:
            Dictionary with observation counts and metadata
        """
        event_counts = {}
        for obs in self.observations:
            event_counts[obs.event_type] = event_counts.get(obs.event_type, 0) + 1
        
        return {
            "total_observations": len(self.observations),
            "event_counts": event_counts,
            "start_time": self.observations[0].timestamp if self.observations else None,
            "end_time": self.observations[-1].timestamp if self.observations else None
        }
    
    def pause(self):
        """Pause observation recording."""
        self._active = False
    
    def resume(self):
        """Resume observation recording."""
        self._active = True
    
    def reset(self):
        """Clear all observations."""
        self.observations.clear()
        self._active = True
