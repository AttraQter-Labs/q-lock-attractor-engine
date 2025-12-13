# qlock/identity.py
#
# Minimal identity → vector embedding for Q-LOCK.
# This satisfies engine imports and gives a deterministic,
# normalized real-valued vector from any identity string.

from __future__ import annotations

import hashlib
from typing import Optional

import numpy as np


def identity_vector(identity: str,
                    dim: int = 64,
                    salt: Optional[str] = None) -> np.ndarray:
    """
    Deterministic embedding of an identity string into R^dim.

    Parameters
    ----------
    identity : str
        Arbitrary identity string (email, name, team key, etc.).
    dim : int, optional
        Output dimensionality of the embedding vector. Default is 64.
    salt : str, optional
        Optional extra string to mix into the hash (e.g. deployment key).

    Returns
    -------
    np.ndarray
        A (dim,) float32 vector with zero mean and unit variance.
    """
    if not isinstance(identity, str):
        raise TypeError(f"identity must be str, got {type(identity)}")

    # Build a stable message for hashing
    msg = identity if salt is None else f"{identity}::{salt}"

    # 32-byte SHA256 digest
    digest = hashlib.sha256(msg.encode("utf-8")).digest()

    # Repeat the digest until we have at least `dim` bytes
    repeat = (dim // len(digest)) + 1
    raw_bytes = (digest * repeat)[:dim]

    # Convert to uint8 then float32
    vec = np.frombuffer(bytes(raw_bytes), dtype=np.uint8).astype(np.float32)

    # Normalize: zero mean, unit variance (avoid div-by-zero)
    vec -= vec.mean()
    std = float(vec.std()) or 1.0
    vec /= std

    return vec
