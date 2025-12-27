#!/usr/bin/env python
"""
q_lock_cli.py

Enhanced command-line interface for the Q-LOCK Attractor Engine.
Supports baseline, watermark, fidelity, and compare modes.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import numpy as np

try:
    from qiskit import QuantumCircuit
    from qiskit.qasm2 import loads as qasm2_loads, dumps as qasm2_dumps
    QISKIT_AVAILABLE = True
except Exception:
    QuantumCircuit = None  # type: ignore
    qasm2_loads = None  # type: ignore
    qasm2_dumps = None  # type: ignore
    QISKIT_AVAILABLE = False

from q_lock_engine import QLockAttractorEngine


BANNER = r"""
==============================
   Q-LOCK ATTRACTOR ENGINE
==============================
"""


def ensure_output_dir(output_dir: str) -> Path:
    """Create output directory if it doesn't exist."""
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_results(data: Dict[str, Any], output_dir: Path, prefix: str) -> None:
    """Save results as both JSON and CSV."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save JSON
    json_path = output_dir / f"{prefix}_{timestamp}.json"
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2, default=str)
    print(f"✓ Saved JSON: {json_path}")
    
    # Save CSV if data is suitable
    try:
        import pandas as pd
        if "counts" in data and isinstance(data["counts"], dict):
            df = pd.DataFrame(list(data["counts"].items()), columns=["state", "count"])
            csv_path = output_dir / f"{prefix}_{timestamp}.csv"
            df.to_csv(csv_path, index=False)
            print(f"✓ Saved CSV: {csv_path}")
    except ImportError:
        print("  (pandas not available, skipping CSV export)")
    except Exception as e:
        print(f"  (CSV export failed: {e})")


def read_circuit_from_file_or_stdin(circuit_path: Optional[str] = None) -> str:
    """Read QASM circuit from file or stdin."""
    if circuit_path and circuit_path != "-":
        with open(circuit_path, "r") as f:
            return f.read().strip()
    else:
        print("Paste QASM circuit (end with blank line):\n")
        lines = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            if not line.strip():
                break
            lines.append(line)
        return "\n".join(lines).strip()


def cmd_baseline(args: argparse.Namespace) -> None:
    """Run baseline mode: simulate circuit without watermarking."""
    print(BANNER)
    print("Mode: BASELINE (no watermarking)\n")
    
    if not QISKIT_AVAILABLE:
        print("ERROR: Qiskit not installed. Install with: pip install qiskit qiskit-aer")
        sys.exit(1)
    
    qasm = read_circuit_from_file_or_stdin(args.circuit)
    if not qasm:
        print("ERROR: No circuit provided.")
        sys.exit(1)
    
    try:
        qc = qasm2_loads(qasm)
    except Exception as e:
        print(f"ERROR: Failed to parse QASM: {e}")
        sys.exit(1)
    
    # Simulate without locking
    from qiskit_aer import AerSimulator
    from qiskit import transpile
    
    sim = AerSimulator()
    circ = qc.copy()
    if not any(inst.operation.name == "measure" for inst in circ.data):
        circ.measure_all()
    
    compiled = transpile(circ, sim)
    result = sim.run(compiled, shots=args.shots).result()
    counts = result.get_counts(0)
    
    output_dir = ensure_output_dir(args.output_dir)
    
    data = {
        "mode": "baseline",
        "timestamp": datetime.now().isoformat(),
        "shots": args.shots,
        "num_qubits": qc.num_qubits,
        "depth": qc.depth(),
        "counts": counts,
    }
    
    save_results(data, output_dir, "baseline")
    
    print("\n--- BASELINE RESULTS ---")
    print(f"Shots: {args.shots}")
    print(f"Qubits: {qc.num_qubits}")
    print(f"Depth: {qc.depth()}")
    print(f"Top 5 states:")
    for state, count in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {state}: {count}")


def cmd_watermark(args: argparse.Namespace) -> None:
    """Run watermark mode: apply identity-locked perturbations."""
    print(BANNER)
    print("Mode: WATERMARK\n")
    
    if not QISKIT_AVAILABLE:
        print("ERROR: Qiskit not installed. Install with: pip install qiskit qiskit-aer")
        sys.exit(1)
    
    identity = args.identity or input("Enter identity string: ").strip()
    if not identity:
        print("ERROR: No identity provided.")
        sys.exit(1)
    
    qasm = read_circuit_from_file_or_stdin(args.circuit)
    if not qasm:
        print("ERROR: No circuit provided.")
        sys.exit(1)
    
    try:
        qc = qasm2_loads(qasm)
    except Exception as e:
        print(f"ERROR: Failed to parse QASM: {e}")
        sys.exit(1)
    
    # Apply watermark
    engine = QLockAttractorEngine(identity)
    locked_qc = engine.lock(qc)
    
    # Simulate locked circuit
    from qiskit_aer import AerSimulator
    from qiskit import transpile
    
    sim = AerSimulator()
    circ = locked_qc.copy()
    if not any(inst.operation.name == "measure" for inst in circ.data):
        circ.measure_all()
    
    compiled = transpile(circ, sim)
    result = sim.run(compiled, shots=args.shots).result()
    counts = result.get_counts(0)
    
    output_dir = ensure_output_dir(args.output_dir)
    
    # Compute identity fingerprint
    import hashlib
    fingerprint = hashlib.sha256(identity.encode()).hexdigest()
    
    data = {
        "mode": "watermark",
        "timestamp": datetime.now().isoformat(),
        "identity_fingerprint": fingerprint,
        "shots": args.shots,
        "num_qubits": locked_qc.num_qubits,
        "depth": locked_qc.depth(),
        "counts": counts,
        "locked_qasm": qasm2_dumps(locked_qc),
    }
    
    save_results(data, output_dir, "watermark")
    
    print("\n--- WATERMARK RESULTS ---")
    print(f"Identity: {identity}")
    print(f"Fingerprint: {fingerprint[:16]}...")
    print(f"Shots: {args.shots}")
    print(f"Qubits: {locked_qc.num_qubits}")
    print(f"Depth: {locked_qc.depth()}")
    print(f"Top 5 states:")
    for state, count in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {state}: {count}")


def total_variation_distance(p: Dict[str, int], q: Dict[str, int]) -> float:
    """Calculate Total Variation Distance between two distributions."""
    all_states = set(p.keys()) | set(q.keys())
    total_p = sum(p.values())
    total_q = sum(q.values())
    
    tvd = 0.5 * sum(abs(p.get(s, 0) / total_p - q.get(s, 0) / total_q) for s in all_states)
    return tvd


def kl_divergence(p: Dict[str, int], q: Dict[str, int], epsilon: float = 1e-10) -> float:
    """Calculate Kullback-Leibler divergence from p to q."""
    all_states = set(p.keys()) | set(q.keys())
    total_p = sum(p.values())
    total_q = sum(q.values())
    
    kl = 0.0
    for s in all_states:
        p_s = p.get(s, 0) / total_p
        q_s = q.get(s, 0) / total_q
        if p_s > epsilon:
            kl += p_s * np.log((p_s + epsilon) / (q_s + epsilon))
    return kl


def hellinger_distance(p: Dict[str, int], q: Dict[str, int]) -> float:
    """Calculate Hellinger distance between two distributions."""
    all_states = set(p.keys()) | set(q.keys())
    total_p = sum(p.values())
    total_q = sum(q.values())
    
    h = np.sqrt(0.5 * sum(
        (np.sqrt(p.get(s, 0) / total_p) - np.sqrt(q.get(s, 0) / total_q)) ** 2
        for s in all_states
    ))
    return h


def cmd_fidelity(args: argparse.Namespace) -> None:
    """Calculate fidelity metrics between baseline and watermark runs."""
    print(BANNER)
    print("Mode: FIDELITY\n")
    
    if not QISKIT_AVAILABLE:
        print("ERROR: Qiskit not installed. Install with: pip install qiskit qiskit-aer")
        sys.exit(1)
    
    identity = args.identity or input("Enter identity string: ").strip()
    if not identity:
        print("ERROR: No identity provided.")
        sys.exit(1)
    
    qasm = read_circuit_from_file_or_stdin(args.circuit)
    if not qasm:
        print("ERROR: No circuit provided.")
        sys.exit(1)
    
    try:
        qc = qasm2_loads(qasm)
    except Exception as e:
        print(f"ERROR: Failed to parse QASM: {e}")
        sys.exit(1)
    
    from qiskit_aer import AerSimulator
    from qiskit import transpile
    
    sim = AerSimulator()
    
    # Run baseline
    print("Running baseline simulation...")
    circ_base = qc.copy()
    if not any(inst.operation.name == "measure" for inst in circ_base.data):
        circ_base.measure_all()
    compiled_base = transpile(circ_base, sim)
    result_base = sim.run(compiled_base, shots=args.shots).result()
    counts_base = result_base.get_counts(0)
    
    # Run watermarked
    print("Running watermarked simulation...")
    engine = QLockAttractorEngine(identity)
    locked_qc = engine.lock(qc)
    circ_lock = locked_qc.copy()
    if not any(inst.operation.name == "measure" for inst in circ_lock.data):
        circ_lock.measure_all()
    compiled_lock = transpile(circ_lock, sim)
    result_lock = sim.run(compiled_lock, shots=args.shots).result()
    counts_lock = result_lock.get_counts(0)
    
    # Calculate metrics
    tvd = total_variation_distance(counts_base, counts_lock)
    kl = kl_divergence(counts_base, counts_lock)
    hellinger = hellinger_distance(counts_base, counts_lock)
    
    output_dir = ensure_output_dir(args.output_dir)
    
    data = {
        "mode": "fidelity",
        "timestamp": datetime.now().isoformat(),
        "identity": identity,
        "shots": args.shots,
        "metrics": {
            "total_variation_distance": tvd,
            "kl_divergence": kl,
            "hellinger_distance": hellinger,
        },
        "baseline_counts": counts_base,
        "watermark_counts": counts_lock,
    }
    
    save_results(data, output_dir, "fidelity")
    
    print("\n--- FIDELITY METRICS ---")
    print(f"Total Variation Distance: {tvd:.6f}")
    print(f"KL Divergence: {kl:.6f}")
    print(f"Hellinger Distance: {hellinger:.6f}")
    print("\nInterpretation:")
    print("  TVD ≈ 0: Distributions are very similar")
    print("  TVD ≈ 1: Distributions are very different")


def cmd_compare(args: argparse.Namespace) -> None:
    """Compare results from baseline, watermark, and/or fidelity runs."""
    print(BANNER)
    print("Mode: COMPARE\n")
    
    output_dir = Path(args.output_dir)
    if not output_dir.exists():
        print(f"ERROR: Output directory '{output_dir}' does not exist.")
        sys.exit(1)
    
    # Find recent result files
    baseline_files = sorted(output_dir.glob("baseline_*.json"))
    watermark_files = sorted(output_dir.glob("watermark_*.json"))
    fidelity_files = sorted(output_dir.glob("fidelity_*.json"))
    
    results = []
    
    # Load most recent of each type
    if baseline_files:
        with open(baseline_files[-1], "r") as f:
            results.append(("baseline", json.load(f)))
    
    if watermark_files:
        with open(watermark_files[-1], "r") as f:
            results.append(("watermark", json.load(f)))
    
    if fidelity_files:
        with open(fidelity_files[-1], "r") as f:
            results.append(("fidelity", json.load(f)))
    
    if not results:
        print("ERROR: No result files found in output directory.")
        sys.exit(1)
    
    # Create comparison summary
    print("\n" + "="*60)
    print("COMPARISON SUMMARY")
    print("="*60)
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "output_dir": str(output_dir),
        "compared_files": {},
    }
    
    for mode, data in results:
        print(f"\n{mode.upper()}:")
        print(f"  Timestamp: {data.get('timestamp', 'N/A')}")
        print(f"  Shots: {data.get('shots', 'N/A')}")
        
        if mode == "fidelity" and "metrics" in data:
            print("  Metrics:")
            for metric, value in data["metrics"].items():
                print(f"    {metric}: {value:.6f}")
        elif "counts" in data:
            counts = data["counts"]
            total = sum(counts.values())
            print(f"  Total counts: {total}")
            print(f"  Unique states: {len(counts)}")
            top_state = max(counts.items(), key=lambda x: x[1])
            print(f"  Top state: {top_state[0]} ({top_state[1]} counts)")
        
        summary["compared_files"][mode] = data
    
    # Save comparison
    comparison_path = output_dir / f"comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(comparison_path, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"\n✓ Saved comparison: {comparison_path}")
    
    # Try to create CSV comparison table
    try:
        import pandas as pd
        
        table_data = []
        for mode, data in results:
            row = {
                "mode": mode,
                "timestamp": data.get("timestamp", "N/A"),
                "shots": data.get("shots", "N/A"),
            }
            
            if mode == "fidelity" and "metrics" in data:
                row.update(data["metrics"])
            elif "counts" in data:
                counts = data["counts"]
                row["total_counts"] = sum(counts.values())
                row["unique_states"] = len(counts)
            
            table_data.append(row)
        
        df = pd.DataFrame(table_data)
        csv_path = output_dir / f"comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(csv_path, index=False)
        print(f"✓ Saved comparison CSV: {csv_path}")
        
        # Print table
        print("\n" + "="*60)
        print(df.to_string(index=False))
    except ImportError:
        print("\n(pandas not available, skipping CSV table)")
    except Exception as e:
        print(f"\n(Table creation failed: {e})")


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Q-LOCK Attractor Engine CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Baseline command
    parser_baseline = subparsers.add_parser(
        "baseline",
        help="Run circuit in baseline mode (no watermarking)",
    )
    parser_baseline.add_argument(
        "--circuit",
        type=str,
        default=None,
        help="Path to QASM circuit file (or '-' for stdin)",
    )
    parser_baseline.add_argument(
        "--shots",
        type=int,
        default=1024,
        help="Number of shots for simulation (default: 1024)",
    )
    parser_baseline.add_argument(
        "--output-dir",
        type=str,
        default="./runs/default",
        help="Output directory for results (default: ./runs/default)",
    )
    parser_baseline.set_defaults(func=cmd_baseline)
    
    # Watermark command
    parser_watermark = subparsers.add_parser(
        "watermark",
        help="Apply identity-locked watermark to circuit",
    )
    parser_watermark.add_argument(
        "--identity",
        type=str,
        default=None,
        help="Identity string for watermarking",
    )
    parser_watermark.add_argument(
        "--circuit",
        type=str,
        default=None,
        help="Path to QASM circuit file (or '-' for stdin)",
    )
    parser_watermark.add_argument(
        "--shots",
        type=int,
        default=1024,
        help="Number of shots for simulation (default: 1024)",
    )
    parser_watermark.add_argument(
        "--output-dir",
        type=str,
        default="./runs/default",
        help="Output directory for results (default: ./runs/default)",
    )
    parser_watermark.set_defaults(func=cmd_watermark)
    
    # Fidelity command
    parser_fidelity = subparsers.add_parser(
        "fidelity",
        help="Calculate fidelity metrics (TVD, KL, Hellinger)",
    )
    parser_fidelity.add_argument(
        "--identity",
        type=str,
        default=None,
        help="Identity string for watermarking",
    )
    parser_fidelity.add_argument(
        "--circuit",
        type=str,
        default=None,
        help="Path to QASM circuit file (or '-' for stdin)",
    )
    parser_fidelity.add_argument(
        "--shots",
        type=int,
        default=1024,
        help="Number of shots for simulation (default: 1024)",
    )
    parser_fidelity.add_argument(
        "--output-dir",
        type=str,
        default="./runs/default",
        help="Output directory for results (default: ./runs/default)",
    )
    parser_fidelity.set_defaults(func=cmd_fidelity)
    
    # Compare command
    parser_compare = subparsers.add_parser(
        "compare",
        help="Compare results from previous runs",
    )
    parser_compare.add_argument(
        "--output-dir",
        type=str,
        default="./runs/default",
        help="Output directory containing results (default: ./runs/default)",
    )
    parser_compare.set_defaults(func=cmd_compare)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main()
