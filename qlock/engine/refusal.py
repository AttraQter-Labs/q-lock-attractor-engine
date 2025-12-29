"""
Refusal mechanism for Q-LOCK.

Q-LOCK will refuse to act rather than degrade a circuit.
This is a design guarantee.
"""


class Refusal(Exception):
    """
    Raised when an unsafe stabilization attempt is made.
    This is not an error; it is a protective invariant.
    
    Refusal is logged, not hidden.
    """
    
    def __init__(self, reason: str, details: dict = None):
        """
        Initialize refusal.
        
        Args:
            reason: Human-readable refusal reason
            details: Optional dictionary with additional context
        """
        self.reason = reason
        self.details = details or {}
        super().__init__(f"Refusal: {reason}")
    
    def to_dict(self):
        """Convert refusal to dictionary format."""
        return {
            "refused": True,
            "reason": self.reason,
            "details": self.details
        }
