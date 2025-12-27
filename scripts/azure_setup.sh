#!/bin/bash
#
# azure_setup.sh
# 
# Setup script for Q-LOCK Attractor Engine in Azure ML environments.
# This script installs all necessary Python dependencies without requiring
# root privileges or system-level installations.
#

set -e  # Exit on error

echo "========================================"
echo "Q-LOCK Attractor Engine - Azure ML Setup"
echo "========================================"
echo ""

# Detect Python version
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo "✓ Detected Python version: $PYTHON_VERSION"

# Check if Python 3.8 or 3.9
PYTHON_MAJOR=$(python -c 'import sys; print(sys.version_info.major)')
PYTHON_MINOR=$(python -c 'import sys; print(sys.version_info.minor)')

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo "ERROR: Python 3.8 or higher is required."
    echo "Current version: $PYTHON_VERSION"
    exit 1
fi

echo "✓ Python version compatible with Azure ML"
echo ""

# Upgrade pip (user space)
echo "Upgrading pip..."
python -m pip install --user --upgrade pip

# Install dependencies from pyproject.toml
echo ""
echo "Installing Q-LOCK dependencies..."
python -m pip install --user \
    "qiskit>=0.43.0,<2.0.0" \
    "qiskit-aer>=0.12.0,<1.0.0" \
    "qiskit-ibm-runtime>=0.9.0,<1.0.0" \
    "numpy>=1.20.0,<2.0.0" \
    "scipy>=1.7.0,<2.0.0" \
    "matplotlib>=3.3.0,<4.0.0" \
    "pandas>=1.3.0,<3.0.0"

echo ""
echo "Installing development dependencies..."
python -m pip install --user \
    "pytest>=7.0.0" \
    "jupyter>=1.0.0" \
    "jupyterlab>=3.0.0"

echo ""
echo "========================================"
echo "✓ Installation complete!"
echo "========================================"
echo ""
echo "Verify installation with:"
echo "  python -c 'import qiskit; print(qiskit.__version__)'"
echo ""
echo "Run CLI with:"
echo "  python q_lock_cli.py --help"
echo ""
