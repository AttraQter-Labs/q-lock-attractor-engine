# Q-LOCK Architecture

## System Overview

Q-LOCK is an attractor-based coherence stabilization engine designed for quantum circuits and high-noise computational systems. It operates as a control and refusal layer, not as an optimizer or error corrector.

## Core Components

### 1. Engine (`qlock/engine.py`)

Central orchestration component that:
- Manages mode selection and execution
- Enforces refusal policies
- Aggregates metrics
- Maintains procedural history (Π)

**Key Classes:**
- `QLockEngine`: Main engine class
- `QLockConfig`: Configuration dataclass
- `QLockResult`: Execution result dataclass

### 2. Guards (`qlock/guards.py`)

Safety enforcement layer that:
- Validates operational parameters
- Checks noise and variance thresholds
- Enforces scalar mode restrictions
- Issues hard refusals for unsafe configurations

**Thresholds:**
- Standard noise threshold: 0.15
- Standard variance limit: 0.25
- Scalar mode operates at 50% of standard thresholds

### 3. Metrics (`qlock/metrics.py`)

Quantitative assessment module providing:
- Coherence preservation measurement
- Entropy computation
- Variance analysis
- KL divergence calculation
- Basin/attractor stability metrics

### 4. Observer (`qlock/observer.py`)

Execution trace collection system:
- Records circuit execution events
- Captures measurements and state transitions
- Provides filtered observation retrieval
- Supports pause/resume functionality

### 5. History (`qlock/history.py`)

Procedural history (Π) manager:
- Maintains complete execution record
- Never erases history (by design)
- Exports audit trails
- Enables reproducibility

## Operational Modes

### Fidelity Mode (Primary)

High-fidelity stabilization optimizing for:
- Minimal drift from baseline behavior
- Basin identity preservation
- Low distributional distance

**Use when:** Standard quantum circuit stabilization is required

### WitnessPhase Mode

Phase-aware stabilization providing:
- Phase evolution tracking
- Phase coherence preservation
- Phase-sensitive attractor logic

**Use when:** Phase information is critical to circuit behavior

### Watermark Mode

Identity-locking without topology changes:
- Deterministic signature embedding
- Provenance tracking
- No circuit logic modification

**Use when:** Circuit attribution and tracking is required

### Scalar Guarded Mode (Restricted)

Strictly controlled operations:
- Requires explicit opt-in
- Operates under 50% of standard thresholds
- Hard refusal outside narrow boundaries
- Never auto-enables

**Use when:** Maximum safety guarantees are required (rare)

## Execution Flow

```
Input Circuit → Guards Check → Mode Selection → Processing → Metrics → History → Result
                     ↓                                                             ↓
                 [REFUSED]                                                    [ACCEPTED]
```

### Guard Check Phase
1. Noise level validation
2. Variance validation
3. Circuit complexity check
4. Mode-specific constraints (if scalar mode)

### Processing Phase
1. Mode-specific transformation application
2. Observer records all events
3. Basin identity preservation
4. No erasure of procedural steps

### Metric Phase
1. Coherence measurement
2. Entropy computation
3. Variance analysis
4. Distribution distance calculation

### History Phase
1. Record complete execution
2. Input/output summaries
3. Metrics snapshot
4. Verdict logging

## Stack Integration

Q-LOCK fits in the control layer of quantum computing stacks:

```
Application Layer
    ↓
Compiler/Optimizer
    ↓
Q-LOCK Control Layer  ← [Controls, stabilizes, refuses]
    ↓
Error Correction
    ↓
Hardware Abstraction
    ↓
Physical Hardware
```

**Position:** Between compilation and error correction
**Role:** Control and safety enforcement, not optimization

## Refusal Policy

Q-LOCK explicitly refuses execution when:
- Noise exceeds thresholds
- Variance exceeds limits
- Circuit complexity is unsupported
- Scalar mode preconditions not met
- Temperature parameters are unsafe

Refusals include detailed reason strings for debugging and compliance.

## History Preservation (Π)

Unlike systems that erase intermediate steps, Q-LOCK maintains complete procedural history:

**Benefits:**
- Full audit trails
- Reproducibility
- Compliance support
- Debugging capability
- Process transparency

**Export:** History can be exported to JSON for external analysis

## Design Principles

1. **Explicit over Implicit**: All operations are explicit and logged
2. **Refuse over Guess**: Hard refusal of unsafe operations
3. **Preserve over Erase**: Complete history maintained
4. **Control over Optimize**: Stabilization, not optimization
5. **Safety over Performance**: Conservative operational boundaries
