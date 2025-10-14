# Introduction
This directory contains for a multi-controlled U gate in Qiskit using only arbitrary 1-qubit gates, CX , and Toffoli gates. The implementation methods used are based on [Barenco et al, "Elementary Gate for Quantum Computation," 1995](https://arxiv.org/pdf/quant-ph/9503016). 

# File Directory
- [`/images`](./images/) - contains images of reference material for easy embedding in Jupyter notebook
- [`multi-controlled-gate.ipynb`](./multi-controlled-gate.ipynb) - step-by-step implementation and verification of gate, with explanatory material and examples for small n: good for exploring the method
- `cU.py` - cleaned-up single-control U gate implementation
- `cnU.py` - cleaned-up multi-control U gate implementation
- `complexity-analysis.txt` - detailed analysis of asymptotic complexity, resources used in my implementation

