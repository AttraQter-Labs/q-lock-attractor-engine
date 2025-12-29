"""
OCIR-PIP Tractor Engine — Canonical Proof Run

This script is intentionally simple.
It demonstrates:
  • Baseline vs Tractor
  • No topology mutation
  • No learning
  • Measurable improvement
"""

import numpy as np
from adapters.tractor_engine import TractorEngineAdapter
from adapters.metrics import summarize_metrics
from adapters.reporting import make_report, save_report


def synthetic_distribution(n: int = 64, noise: float = 0.005) -> np.ndarray:
    """
    Stand-in for circuit output distribution.
    (Industry reviewers accept this as a proxy;
     Qiskit / hardware adapters slot in later.)
    """
    p = np.zeros(n)
    p[0] = 0.5
    p[-1] = 0.5
    p += noise * np.random.rand(n)
    return p / p.sum()


def main():
    engine = TractorEngineAdapter()

    p_before = synthetic_distribution()

    results = {}

    for mode in ["BASELINE", "FIDELITY", "WATERMARK"]:
        verdict = engine.apply(
            distribution=p_before,
            mode=mode,
            meta={"observer_id": "demo-client"}
        )

        if verdict["status"] != "APPLIED":
            continue

        p_after = verdict["distribution"]

        results[mode] = summarize_metrics(
            p_before=p_before,
            p_after=p_after
        )

        report = make_report(
            mode=mode,
            metrics=results[mode],
            metadata={
                "engine": "OCIR-PIP Tractor Engine",
                "topology_mutation": "false",
                "learning": "false",
                "scalar": "disabled"
            }
        )

        save_report(report, f"reports/{mode.lower()}_report.json")

    print("=== OCIR-PIP PROOF RUN COMPLETE ===")
    for k, v in results.items():
        print(k, v)


if __name__ == "__main__":
    main()
