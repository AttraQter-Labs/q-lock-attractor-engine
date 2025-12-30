"""
Mirror Engine — Hypothesis & Procedural Exploration Engine

Purpose:
- Enumerate procedural variants (Π-space)
- Surface assumption sensitivity
- Expand hypothesis space
- Generate candidate runs for Tractor Engine validation

This engine:
- DOES NOT enforce invariants
- DOES NOT stabilize basins
- DOES NOT refuse operations
- DOES NOT optimize or learn

It is the epistemic dual of the OCIR-PIP Tractor Engine.
"""

from mirror_engine.mirror_engine import MirrorEngine

__all__ = ["MirrorEngine"]
