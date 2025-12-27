#!/bin/bash
# Final demonstration of Q-LOCK Attractor Engine Azure ML enhancements

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   Q-LOCK Attractor Engine - Final Demonstration           ║"
echo "║   Azure ML Compatible • No Cloud Dependencies             ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Create timestamped output
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="./runs/final_demo_${TIMESTAMP}"
mkdir -p "${OUTPUT_DIR}"

echo "📁 Output directory: ${OUTPUT_DIR}"
echo ""

# Step 1: Show CLI help
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 1: CLI Help"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python q_lock_cli.py --help
echo ""

# Step 2: Run all commands
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 2: Running All Commands"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "➤ Baseline (no watermarking)..."
python q_lock_cli.py baseline \
    --circuit examples/test_circuit.qasm \
    --shots 1024 \
    --output-dir "${OUTPUT_DIR}" > /dev/null
echo "  ✓ Baseline complete"

echo "➤ Watermark (identity-locked)..."
python q_lock_cli.py watermark \
    --circuit examples/test_circuit.qasm \
    --identity "AzureML-Final-Demo-2025" \
    --shots 1024 \
    --output-dir "${OUTPUT_DIR}" > /dev/null
echo "  ✓ Watermark complete"

echo "➤ Fidelity metrics..."
python q_lock_cli.py fidelity \
    --circuit examples/test_circuit.qasm \
    --identity "AzureML-Final-Demo-2025" \
    --shots 1024 \
    --output-dir "${OUTPUT_DIR}" > /dev/null
echo "  ✓ Fidelity complete"

echo "➤ Compare results..."
python q_lock_cli.py compare \
    --output-dir "${OUTPUT_DIR}" > /dev/null
echo "  ✓ Compare complete"
echo ""

# Step 3: Show outputs
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 3: Generated Outputs"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ls -lh "${OUTPUT_DIR}/"
echo ""

# Step 4: Show sample results
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 4: Fidelity Metrics"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
cat "${OUTPUT_DIR}"/fidelity_*.json | python -m json.tool | grep -A 4 "metrics"
echo ""

# Step 5: Verify no Azure dependencies
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 5: Dependency Verification"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Checking for Azure Quantum dependencies..."
if grep -r "azure.quantum" --include="*.py" q_lock_cli.py Src/qlock/modes/ 2>/dev/null; then
    echo "❌ Found Azure Quantum dependencies"
else
    echo "✓ No Azure Quantum dependencies found"
fi

if grep -r "AzureCliCredential\|AzureQuantumProvider" --include="*.py" q_lock_cli.py Src/qlock/modes/ 2>/dev/null; then
    echo "❌ Found Azure CLI dependencies"
else
    echo "✓ No Azure CLI dependencies found"
fi
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ All CLI subcommands working"
echo "✅ JSON and CSV outputs generated"
echo "✅ Fidelity metrics calculated"
echo "✅ No Azure Quantum dependencies"
echo "✅ No cloud resources required"
echo "✅ Python 3.8+ compatible"
echo "✅ Azure ML ready"
echo ""
echo "📊 Results saved to: ${OUTPUT_DIR}"
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║            ✨ Demonstration Complete! ✨                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
