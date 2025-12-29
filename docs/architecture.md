# Q-LOCK Architecture

## System Overview

Q-LOCK is an attractor-based coherence stabilization and safety engine positioned as a pre-processing control layer in the quantum computing stack.

## Positioning in the Stack

```
User Application Layer
         ↓
    Q-LOCK Engine
         ↓
  Quantum Compiler
         ↓
   Hardware Backend
```

Q-LOCK sits **before** compilation and execution, operating on high-level circuit representations.

## Core Components

### 1. Engine (`engine.py`)

Central orchestration hub that:
- Selects and dispatches to appropriate modes
- Evaluates guard conditions
- Aggregates metrics
- Manages procedural history
- Issues refusal verdicts when necessary

### 2. Guards (`guards.py`)

Safety enforcement layer:
- **NoiseGuard**: Evaluates estimated noise levels against thresholds
- **ScalarGuard**: Enforces hard boundaries for scalar mode operations
- Guards issue refusal verdicts to prevent harmful contractions

### 3. Modes (`modes/`)

Stabilization strategies:
- **FidelityMode**: Primary mode for high-fidelity stabilization
- **WitnessPhaseMode**: Phase-coherent stabilization with verification
- **WatermarkMode**: Identity locking only, no topology changes
- **ScalarGuardedMode**: Bounded scalar operations with strict refusal logic

### 4. Metrics (`metrics.py`)

Tracks:
- Coherence levels
- Entropy measures
- Variance across operations
- KL divergence (distribution comparison)

### 5. Observer (`observer.py`)

Observes circuit transformations and computes comparative metrics between original and processed circuits.

### 6. History (`history.py`)

Preserves procedural history (Π):
- Records all acceptance and refusal events
- Maintains basin identity provenance
- Never erases operational history

## Data Flow

```
Input: Circuit + Identity
         ↓
    Guards Evaluate
         ↓
   [Refused?] → Yes → Refusal Verdict + History Entry
         ↓ No
   Mode Apply Transformation
         ↓
   Observer Compute Metrics
         ↓
   History Record Acceptance
         ↓
Output: Stabilized Circuit + Metrics + History Entry
```

## Design Principles

1. **Explicit Refusal**: System explicitly refuses unsafe operations rather than failing silently
2. **Basin Preservation**: Identity-locked basins are preserved across transformations
3. **History Preservation**: Procedural history (Π) is maintained, not erased
4. **Mode Isolation**: Each mode is independent with well-defined boundaries
5. **Guard Composition**: Multiple guards can evaluate independently

## Integration Points

Q-LOCK integrates with:
- Qiskit circuits via `QuantumCircuit` objects
- QASM 2.0 text representations
- Custom circuit formats (extensible)

## Extensibility

New modes can be added by:
1. Inheriting from `ModeBase`
2. Implementing `apply(circuit, identity)` method
3. Registering in `QLockEngine.SUPPORTED_MODES`

New guards can be added by:
1. Inheriting from `Guard`
2. Implementing `evaluate(circuit, identity, mode)` method
3. Adding to `QLockEngine.__init__` guards list
