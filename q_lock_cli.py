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


# ========================================================================
# Basin/Concentration Metrics (Attractor Stability)
# ========================================================================

def octave_binned_mass(counts: Dict[str, int], num_octaves: int = 5) -> Dict[int, float]:
    """
    Calculate probability mass in octave (log2 rank) bins.
    
    Args:
        counts: Dictionary mapping states to counts
        num_octaves: Number of octave bins to create
        
    Returns:
        Dictionary mapping octave index to probability mass
    """
    total = sum(counts.values())
    sorted_probs = sorted([c / total for c in counts.values()], reverse=True)
    
    octave_masses = {}
    for octave in range(num_octaves):
        start_rank = 2 ** octave
        end_rank = 2 ** (octave + 1)
        
        # Sum probabilities in this octave
        mass = sum(sorted_probs[i] for i in range(len(sorted_probs)) 
                   if start_rank <= i + 1 < end_rank)
        octave_masses[octave] = mass
    
    return octave_masses


def top_k_mass(counts: Dict[str, int], k: int = 5) -> float:
    """
    Calculate probability mass concentrated in top-k states.
    
    Args:
        counts: Dictionary mapping states to counts
        k: Number of top states to consider
        
    Returns:
        Probability mass in top k states
    """
    total = sum(counts.values())
    sorted_counts = sorted(counts.values(), reverse=True)
    return sum(sorted_counts[:k]) / total


def effective_support(counts: Dict[str, int]) -> float:
    """
    Calculate effective support size (inverse participation ratio).
    
    Computed as 1 / sum(p_i^2), where p_i are probabilities.
    Higher values indicate more uniform distribution.
    
    Args:
        counts: Dictionary mapping states to counts
        
    Returns:
        Effective support (number of effectively occupied states)
    """
    total = sum(counts.values())
    probs = [c / total for c in counts.values()]
    sum_sq = sum(p ** 2 for p in probs)
    return 1.0 / sum_sq if sum_sq > 0 else 0.0


def gini_coefficient(counts: Dict[str, int]) -> float:
    """
    Calculate Gini coefficient (measure of inequality).
    
    0 = perfect equality, 1 = maximum inequality
    
    Args:
        counts: Dictionary mapping states to counts
        
    Returns:
        Gini coefficient
    """
    total = sum(counts.values())
    probs = sorted([c / total for c in counts.values()])
    n = len(probs)
    
    if n == 0:
        return 0.0
    
    # Calculate Gini coefficient
    cumsum = np.cumsum(probs)
    gini = (n + 1 - 2 * np.sum(cumsum) / cumsum[-1]) / n if cumsum[-1] > 0 else 0.0
    return gini


def cmd_basin(args: argparse.Namespace) -> None:
    """
    Calculate basin/concentration metrics (attractor stability).
    
    Measures bias preservation rather than distribution distance.
    Complementary to fidelity mode, aligned with Krystal scheduling.
    """
    print(BANNER)
    print("Mode: BASIN (Concentration/Attractor Stability)\n")
    
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
    
    # Run watermarked/locked
    print("Running locked simulation...")
    engine = QLockAttractorEngine(identity)
    locked_qc = engine.lock(qc)
    circ_lock = locked_qc.copy()
    if not any(inst.operation.name == "measure" for inst in circ_lock.data):
        circ_lock.measure_all()
    compiled_lock = transpile(circ_lock, sim)
    result_lock = sim.run(compiled_lock, shots=args.shots).result()
    counts_lock = result_lock.get_counts(0)
    
    # Calculate basin/concentration metrics
    print("\nCalculating basin metrics...")
    
    # Octave-binned mass - convert keys to strings for JSON consistency
    octaves_base = {str(k): v for k, v in octave_binned_mass(counts_base, num_octaves=5).items()}
    octaves_lock = {str(k): v for k, v in octave_binned_mass(counts_lock, num_octaves=5).items()}
    
    # Top-k mass (k=1, 3, 5, 10) - convert keys to strings for JSON consistency
    topk_base = {str(k): top_k_mass(counts_base, k) for k in [1, 3, 5, 10]}
    topk_lock = {str(k): top_k_mass(counts_lock, k) for k in [1, 3, 5, 10]}
    
    # Effective support
    eff_support_base = effective_support(counts_base)
    eff_support_lock = effective_support(counts_lock)
    
    # Gini coefficient
    gini_base = gini_coefficient(counts_base)
    gini_lock = gini_coefficient(counts_lock)
    
    output_dir = ensure_output_dir(args.output_dir)
    
    # Prepare data
    data = {
        "mode": "basin",
        "timestamp": datetime.now().isoformat(),
        "identity": identity,
        "shots": args.shots,
        "metrics": {
            "baseline": {
                "octave_binned_mass": octaves_base,
                "top_k_mass": topk_base,
                "effective_support": eff_support_base,
                "gini_coefficient": gini_base,
            },
            "locked": {
                "octave_binned_mass": octaves_lock,
                "top_k_mass": topk_lock,
                "effective_support": eff_support_lock,
                "gini_coefficient": gini_lock,
            },
        },
        "baseline_counts": counts_base,
        "locked_counts": counts_lock,
    }
    
    # Save JSON
    save_results(data, output_dir, "basin")
    
    # Print summary
    print("\n--- BASIN METRICS (Attractor Stability) ---")
    print("\nBaseline:")
    print(f"  Top-1 mass:         {topk_base['1']:.4f}")
    print(f"  Top-5 mass:         {topk_base['5']:.4f}")
    print(f"  Top-10 mass:        {topk_base['10']:.4f}")
    print(f"  Effective support:  {eff_support_base:.2f}")
    print(f"  Gini coefficient:   {gini_base:.4f}")
    
    print("\nLocked:")
    print(f"  Top-1 mass:         {topk_lock['1']:.4f}")
    print(f"  Top-5 mass:         {topk_lock['5']:.4f}")
    print(f"  Top-10 mass:        {topk_lock['10']:.4f}")
    print(f"  Effective support:  {eff_support_lock:.2f}")
    print(f"  Gini coefficient:   {gini_lock:.4f}")
    
    print("\nInterpretation:")
    print("  • Higher top-k mass = more concentrated distribution")
    print("  • Higher effective support = more uniform distribution")
    print("  • Higher Gini = more inequality/concentration")
    
    # Generate plots
    print("\nGenerating plots...")
    try:
        import matplotlib
        matplotlib.use('Agg')  # Non-interactive backend
        import matplotlib.pyplot as plt
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Plot 1: Octave spectrum
        ax1 = axes[0, 0]
        octave_indices = sorted([int(k) for k in octaves_base.keys()])
        ax1.plot(octave_indices, [octaves_base[str(i)] for i in octave_indices], 
                'o-', label='Baseline', linewidth=2, markersize=8)
        ax1.plot(octave_indices, [octaves_lock[str(i)] for i in octave_indices], 
                's-', label='Locked', linewidth=2, markersize=8)
        ax1.set_xlabel('Octave (log2 rank bin)', fontsize=12)
        ax1.set_ylabel('Probability Mass', fontsize=12)
        ax1.set_title('Octave Spectrum (Rank-binned Mass)', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: CDF comparison
        ax2 = axes[0, 1]
        total_base = sum(counts_base.values())
        total_lock = sum(counts_lock.values())
        sorted_probs_base = sorted([c / total_base for c in counts_base.values()], reverse=True)
        sorted_probs_lock = sorted([c / total_lock for c in counts_lock.values()], reverse=True)
        
        cumsum_base = np.cumsum(sorted_probs_base)
        cumsum_lock = np.cumsum(sorted_probs_lock)
        
        ax2.plot(range(len(cumsum_base)), cumsum_base, '-', label='Baseline', linewidth=2)
        ax2.plot(range(len(cumsum_lock)), cumsum_lock, '-', label='Locked', linewidth=2)
        ax2.set_xlabel('State Rank', fontsize=12)
        ax2.set_ylabel('Cumulative Probability', fontsize=12)
        ax2.set_title('CDF (Cumulative Distribution)', fontsize=14, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Lorenz curve
        ax3 = axes[1, 0]
        lorenz_base = np.cumsum(sorted(sorted_probs_base)) / np.sum(sorted_probs_base)
        lorenz_lock = np.cumsum(sorted(sorted_probs_lock)) / np.sum(sorted_probs_lock)
        lorenz_x_base = np.linspace(0, 1, len(lorenz_base))
        lorenz_x_lock = np.linspace(0, 1, len(lorenz_lock))
        
        ax3.plot([0, 1], [0, 1], 'k--', label='Perfect Equality', linewidth=1)
        ax3.plot(lorenz_x_base, lorenz_base, '-', label='Baseline', linewidth=2)
        ax3.plot(lorenz_x_lock, lorenz_lock, '-', label='Locked', linewidth=2)
        ax3.set_xlabel('Cumulative Share of States', fontsize=12)
        ax3.set_ylabel('Cumulative Share of Probability', fontsize=12)
        ax3.set_title('Lorenz Curve (Inequality)', fontsize=14, fontweight='bold')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Top-k mass comparison
        ax4 = axes[1, 1]
        k_values = [1, 3, 5, 10]
        baseline_topk = [topk_base[str(k)] for k in k_values]
        locked_topk = [topk_lock[str(k)] for k in k_values]
        
        x = np.arange(len(k_values))
        width = 0.35
        ax4.bar(x - width/2, baseline_topk, width, label='Baseline', alpha=0.8)
        ax4.bar(x + width/2, locked_topk, width, label='Locked', alpha=0.8)
        ax4.set_xlabel('Top-k States', fontsize=12)
        ax4.set_ylabel('Probability Mass', fontsize=12)
        ax4.set_title('Top-k Mass Concentration', fontsize=14, fontweight='bold')
        ax4.set_xticks(x)
        ax4.set_xticklabels([f'k={k}' for k in k_values])
        ax4.legend()
        ax4.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        # Save plot
        plot_path = output_dir / f"basin_plots_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(plot_path, dpi=150, bbox_inches='tight')
        print(f"✓ Saved plots: {plot_path}")
        plt.close()
        
    except ImportError:
        print("  (matplotlib not available, skipping plots)")
    except Exception as e:
        print(f"  (Plot generation failed: {e})")


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
    """Compare results from baseline, watermark, fidelity, and/or basin runs."""
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
    basin_files = sorted(output_dir.glob("basin_*.json"))
    
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
    
    if basin_files:
        with open(basin_files[-1], "r") as f:
            results.append(("basin", json.load(f)))
    
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
        elif mode == "basin" and "metrics" in data:
            print("  Basin Metrics (Baseline):")
            baseline_metrics = data["metrics"].get("baseline", {})
            top_k = baseline_metrics.get('top_k_mass', {})
            # Handle both int and str keys
            top_1 = top_k.get(1, top_k.get('1', 'N/A'))
            print(f"    Top-1 mass: {top_1}")
            print(f"    Effective support: {baseline_metrics.get('effective_support', 'N/A')}")
            print(f"    Gini coefficient: {baseline_metrics.get('gini_coefficient', 'N/A')}")
            print("  Basin Metrics (Locked):")
            locked_metrics = data["metrics"].get("locked", {})
            top_k_locked = locked_metrics.get('top_k_mass', {})
            top_1_locked = top_k_locked.get(1, top_k_locked.get('1', 'N/A'))
            print(f"    Top-1 mass: {top_1_locked}")
            print(f"    Effective support: {locked_metrics.get('effective_support', 'N/A')}")
            print(f"    Gini coefficient: {locked_metrics.get('gini_coefficient', 'N/A')}")
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
    
    # Basin command (concentration/attractor stability)
    parser_basin = subparsers.add_parser(
        "basin",
        help="Calculate basin/concentration metrics (attractor stability)",
    )
    parser_basin.add_argument(
        "--identity",
        type=str,
        default=None,
        help="Identity string for watermarking",
    )
    parser_basin.add_argument(
        "--circuit",
        type=str,
        default=None,
        help="Path to QASM circuit file (or '-' for stdin)",
    )
    parser_basin.add_argument(
        "--shots",
        type=int,
        default=1024,
        help="Number of shots for simulation (default: 1024)",
    )
    parser_basin.add_argument(
        "--output-dir",
        type=str,
        default="./runs/default",
        help="Output directory for results (default: ./runs/default)",
    )
    parser_basin.set_defaults(func=cmd_basin)
    
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
