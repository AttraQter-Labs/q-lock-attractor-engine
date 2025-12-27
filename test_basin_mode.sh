#!/bin/bash
set -e

echo "=========================================="
echo "Q-LOCK Basin Mode Test"
echo "=========================================="
echo ""

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="./runs/basin_demo_${TIMESTAMP}"

echo "Output directory: ${OUTPUT_DIR}"
echo ""

# Run basin mode
echo "Running basin mode..."
python q_lock_cli.py basin \
    --circuit examples/test_circuit.qasm \
    --identity "basin-demo-user" \
    --shots 2048 \
    --output-dir "${OUTPUT_DIR}"

echo ""
echo "Listing outputs..."
ls -lh "${OUTPUT_DIR}/"

echo ""
echo "Sample JSON:"
head -20 "${OUTPUT_DIR}"/basin_*.json

echo ""
echo "✅ Basin mode test complete!"
