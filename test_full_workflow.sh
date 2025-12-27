#!/bin/bash
set -e

echo "=========================================="
echo "Q-LOCK Full Workflow Test"
echo "=========================================="
echo ""

# Create timestamped output directory
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="./runs/test_${TIMESTAMP}"

echo "Output directory: ${OUTPUT_DIR}"
echo ""

# Test 1: Baseline
echo "Test 1: Running baseline mode..."
python q_lock_cli.py baseline \
    --circuit examples/test_circuit.qasm \
    --shots 512 \
    --output-dir "${OUTPUT_DIR}"
echo "✓ Baseline completed"
echo ""

# Test 2: Watermark
echo "Test 2: Running watermark mode..."
python q_lock_cli.py watermark \
    --circuit examples/test_circuit.qasm \
    --identity "test-workflow-user" \
    --shots 512 \
    --output-dir "${OUTPUT_DIR}"
echo "✓ Watermark completed"
echo ""

# Test 3: Fidelity
echo "Test 3: Running fidelity mode..."
python q_lock_cli.py fidelity \
    --circuit examples/test_circuit.qasm \
    --identity "test-workflow-user" \
    --shots 512 \
    --output-dir "${OUTPUT_DIR}"
echo "✓ Fidelity completed"
echo ""

# Test 4: Compare
echo "Test 4: Running compare mode..."
python q_lock_cli.py compare \
    --output-dir "${OUTPUT_DIR}"
echo "✓ Compare completed"
echo ""

# Verify outputs
echo "=========================================="
echo "Verifying outputs..."
echo "=========================================="
ls -lh "${OUTPUT_DIR}/"
echo ""

# Count files
JSON_COUNT=$(ls "${OUTPUT_DIR}"/*.json 2>/dev/null | wc -l)
CSV_COUNT=$(ls "${OUTPUT_DIR}"/*.csv 2>/dev/null | wc -l)

echo "Generated files:"
echo "  JSON files: ${JSON_COUNT}"
echo "  CSV files: ${CSV_COUNT}"
echo ""

if [ "${JSON_COUNT}" -ge 4 ] && [ "${CSV_COUNT}" -ge 3 ]; then
    echo "✅ All tests passed successfully!"
    exit 0
else
    echo "❌ Some output files are missing"
    exit 1
fi
