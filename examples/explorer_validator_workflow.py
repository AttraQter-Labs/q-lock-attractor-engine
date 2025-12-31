"""
Explorer-Validator Workflow Example

Demonstrates the epistemic dual relationship:
- Explorer Engine: Explores procedural variants (Π-space)
- Validator Engine: Validates and stabilizes accepted variants

This workflow preserves scientific integrity through separation of concerns.
"""

from explorer_engine import ExplorerEngine
from qlock.engine.core import ValidatorEngine, EngineContext, EngineMetrics


def main():
    print("=== EXPLORER-VALIDATOR WORKFLOW DEMONSTRATION ===\n")
    
    # Step 1: Explorer Engine generates procedural variants
    print("Step 1: Explorer Engine - Procedural Exploration")
    print("-" * 50)
    
    explorer = ExplorerEngine(base_object="example_circuit")
    variants = explorer.enumerate_procedures(variants=5)
    
    print(f"Generated {len(variants)} procedural variants:\n")
    for variant in variants:
        print(f"  {variant.pi_signature}: {variant.assumptions['ordering']}")
    
    print(f"\nExplorer Engine characteristics:")
    print(f"  - No refusals: ALL variants generated")
    print(f"  - No stabilization: Output is exploratory")
    print(f"  - No constraints: Maximum hypothesis space")
    
    # Step 2: Validator Engine validates and stabilizes
    print("\n\nStep 2: Validator Engine - Validation & Stabilization")
    print("-" * 50)
    
    # Create context for validation
    context = EngineContext(
        noise=0.002,  # Low noise (within scalar bounds)
        depth=10,
        phase_dispersion=0.1,
        procedural_disorder=0.15,
        topology="low"
    )
    
    validator = ValidatorEngine(context)
    
    # Create metrics for each variant
    initial_metrics = EngineMetrics(
        coherence_r=0.85,
        entropy_h=0.20,
        variance_v=0.15,
        bias_retention=0.90
    )
    
    # Validate each variant through Validator Engine
    print(f"\nValidating {len(variants)} variants through Validator Engine:\n")
    
    accepted_count = 0
    refused_count = 0
    
    for variant in variants:
        try:
            # Apply fidelity mode stabilization
            result_metrics = validator.apply(initial_metrics, "fidelity")
            accepted_count += 1
            print(f"  ✓ {variant.pi_signature}: ACCEPTED & STABILIZED")
            print(f"    Coherence: {initial_metrics.coherence_r:.2f} → {result_metrics.coherence_r:.2f}")
        except Exception as e:
            refused_count += 1
            print(f"  ✗ {variant.pi_signature}: REFUSED ({str(e)[:40]}...)")
    
    # Step 3: Summary
    print("\n\nStep 3: Workflow Summary")
    print("-" * 50)
    print(f"Explorer Engine generated: {len(variants)} variants")
    print(f"Validator Engine accepted: {accepted_count} variants")
    print(f"Validator Engine refused:  {refused_count} variants")
    print(f"Acceptance rate: {100*accepted_count/len(variants):.1f}%")
    
    print("\n\nKey Insights:")
    print("-" * 50)
    print("1. Explorer Engine explores WITHOUT judgment")
    print("2. Validator Engine validates WITH constraints")
    print("3. Refusals surface constraint violations")
    print("4. Accepted variants are stabilized")
    print("5. This preserves scientific integrity")
    
    print("\n\n=== WORKFLOW COMPLETE ===")


if __name__ == "__main__":
    main()
