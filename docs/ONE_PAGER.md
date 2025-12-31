# SPECTRUM GSE — One Page Overview

**What It Is**
A stability engine that validates computational basins under procedural divergence.

**What It Does**
- Detects when mathematically equivalent operations diverge empirically
- Refuses unsafe stabilization attempts
- Preserves procedural history (Π)
- Operates deterministically

**What It Does NOT Do**
- Optimization
- Error correction
- Learning
- Topology mutation

**Key Property**
> SPECTRUM GSE refuses to act rather than degrade a system.

**Use When**
- Reproducibility fails
- Procedural order matters
- Theory ≠ empirical outcome

**Do Not Use When**
- You need optimization
- You need QEC
- Well-behaved systems without procedural sensitivity

**Version**
v1.0.0 — Behaviorally frozen

**Evidence**
- Canonical proof run: variance -46.1%, topology immutable
- CI enforcement: scalar refusal, no learning, no mutation
- 19 tests passing

**Modes**
- Fidelity (always safe)
- Witness+Phase (coherence stabilization)
- Watermark (identity locking)
- Scalar (experimental, gated, refused by default)

**Engines**
- ValidatorEngine: stability validation
- ExplorerEngine: hypothesis generation

**License**
Dual: Academic (free with citation) / Commercial (separate license required)

**Contact**
licensing@spectrumgse.com
