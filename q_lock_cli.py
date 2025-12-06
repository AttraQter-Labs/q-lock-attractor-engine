#!/usr/bin/env python
"""
q_lock_cli.py

Simple command-line interface for the Q-LOCK Attractor Engine.
"""

from __future__ import annotations

import sys
from textwrap import dedent

from qlock_engine import QLockAttractorEngine

try:
    from qiskit import QuantumCircuit
except Exception:
    QuantumCircuit = None  # type: ignore


BANNER = r"""
==============================
   Q-LOCK ATTRACTOR ENGINE
==============================
"""


def main() -> None:
    print(BANNER)
    identity = input("Enter identity string: ").strip()
    if not identity:
        print("No identity provided. Exiting.")
        return

    engine = QLockAttractorEngine(identity)

    if QuantumCircuit is None:
        print("\nQiskit not installed → running text-only mode.")
        print("You can still use this identity, but circuit locking requires Qiskit.")
        return

    print("\nPaste a small QASM2 circuit (end with a blank line):\n")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line.strip():
            break
        lines.append(line)

    qasm = "\n".join(lines).strip()
    if not qasm:
        print("No circuit provided. Exiting.")
        return

    locked = engine.lock(qasm)
    from qiskit.qasm2 import dumps as qasm2_dumps

    if hasattr(locked, "qasm2"):
        qasm_out = locked.qasm2()
    else:
        qasm_out = qasm2_dumps(locked)

    print("\n--- LOCKED CIRCUIT (QASM2) ---")
    print(qasm_out)


if __name__ == "__main__":
    main()
