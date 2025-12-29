"""
Scalar stabilization module.

Status:
- Experimental
- Gated
- Non-default
- Refusal-protected

Never invoked unless policy explicitly allows.
"""

from qlock.engine.refusal import Refusal


def apply_scalar(*args, **kwargs):
    """
    Scalar mode application.
    
    Raises:
        Refusal: Always raises - scalar mode is disabled by policy
    """
    raise Refusal(
        reason="Scalar mode is disabled by policy",
        details={
            "mode": "scalar",
            "status": "experimental",
            "default_enabled": False
        }
    )
