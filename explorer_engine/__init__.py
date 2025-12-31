"""
Explorer Engine — Hypothesis & Procedural Exploration Engine

Purpose:
- Enumerate procedural variants (Π-space)
- Surface assumption sensitivity
- Expand hypothesis space
- Generate candidate runs for Validator Engine validation

This engine:
- DOES NOT enforce invariants
- DOES NOT stabilize basins
- DOES NOT refuse operations
- DOES NOT optimize or learn

It is the epistemic dual of the SPECTRUM GSE Validator Engine.
"""

from explorer_engine.explorer_engine import ExplorerEngine

__all__ = ["ExplorerEngine"]
