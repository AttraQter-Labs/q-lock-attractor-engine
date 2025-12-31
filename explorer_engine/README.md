# Explorer Engine

The Explorer Engine is the exploratory counterpart to the SPECTRUM GSE Validator Engine.

## What it does
- Enumerates procedural variants (Π-space)
- Surfaces hidden assumptions
- Generates hypotheses
- Produces divergence intentionally

## What it does NOT do
- No stabilization
- No optimization
- No learning
- No refusal
- No invariant enforcement

## Intended use
Explorer Engine output is **fed into** the Validator Engine for validation,
refusal detection, and basin analysis.

This separation preserves scientific integrity.

## Usage

```python
from explorer_engine import ExplorerEngine

# Create engine with base object
engine = ExplorerEngine(base_object=my_circuit)

# Generate procedural variants
variants = engine.enumerate_procedures(variants=10)

# Examine variants
for variant in variants:
    print(f"Π signature: {variant.pi_signature}")
    print(f"Assumptions: {variant.assumptions}")
    print(f"Notes: {variant.notes}")
```

## Relationship to Validator Engine

The Explorer Engine and Validator Engine form an epistemic pair within SPECTRUM GSE:

| Property | Explorer Engine | Validator Engine |
|----------|-----------------|------------------|
| Purpose | Exploration | Stabilization |
| Output | Divergent | Convergent |
| Refusals | No | Yes |
| Constraints | None | Strict |
| Learning | No | No |
| Optimization | No | No |

**Workflow:**
1. Explorer Engine generates procedural variants (unconstrained)
2. Variants are passed to Validator Engine for validation
3. Validator Engine applies constraints and may refuse variants
4. Valid variants are stabilized by Validator Engine
5. Refusals surface constraint violations for analysis

This separation ensures:
- Exploratory freedom in hypothesis generation
- Rigorous validation before stabilization
- Clear distinction between generation and validation
- Scientific integrity through explicit constraint enforcement
