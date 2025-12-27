"""
Setup script for Q-LOCK Attractor Engine
"""
from setuptools import setup, find_packages

setup(
    name="qlock",
    version="0.1.0",
    description="Q-LOCK Attractor Engine — Identity-Locked Quantum Circuit Stabilization",
    author="AttraQtor Labs LLC",
    author_email="nic_hensley@proton.me",
    python_requires=">=3.8",
    packages=find_packages(where="Src"),
    package_dir={"": "Src"},
    py_modules=["q_lock_engine", "q_lock_cli", "qlock_engine"],
    install_requires=[
        "qiskit>=0.43.0,<2.0.0",
        "qiskit-aer>=0.12.0,<1.0.0",
        "qiskit-ibm-runtime>=0.9.0,<1.0.0",
        "numpy>=1.20.0,<2.0.0",
        "scipy>=1.7.0,<2.0.0",
        "matplotlib>=3.3.0,<4.0.0",
        "pandas>=1.3.0,<3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "flake8>=5.0.0",
            "jupyter>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "qlock=q_lock_cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
