# Introduction
This directory contains for a multi-controlled U gate in Qiskit using only arbitrary 1-qubit gates, CX , and Toffoli gates. The implementation methods used are based on [Barenco et al, "Elementary Gate for Quantum Computation," 1995](https://arxiv.org/pdf/quant-ph/9503016). 

# File Directory
- [`/images`](./images/) - contains images of reference material for easy embedding in Jupyter notebook
- [`multi-controlled-gate.ipynb`](./multi-controlled-gate.ipynb) - step-by-step implementation and verification of gate, with explanatory material and examples for small n: good for exploring the method
- [`cnU.py`](./cnU.py) - cleaned-up n-control U gate implementation
- [`complexity-analysis.md`](./complexity-analysis.md) - analysis of asymptotic complexity, resources used in this implementation

