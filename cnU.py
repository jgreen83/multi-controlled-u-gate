"""
PACKAGED: multi-controlled-u-gate

usage example: 

import cnU

U = [[0, 1], [1, 0]] #any unitary 2x2 matrix
n = 8 #any positive integer

C = cnU.multi_controlled_U_gate(Operator(U), n)
C.draw(output="mpl", style="bw")

"""

from qiskit.circuit import QuantumCircuit, QuantumRegister, AncillaRegister
from qiskit.quantum_info import Statevector, Operator
from qiskit.circuit.library import UnitaryGate
from qiskit.synthesis import OneQubitEulerDecomposer

import matplotlib.pyplot as plt

import numpy as np

def controlled_U_gate(U):
    
    #decompose U into a z-y-z angle decomposition
    #U = e^ix * Rz(a)Ry(b)Rz(c)
    basis = 'ZYZ'
    angles = OneQubitEulerDecomposer(basis).angles_and_phase(U)

    Rz1 = Operator([[np.exp(-1j*angles[0]/2), 0], [0, np.exp(1j*angles[0]/2)]])
    Ry = Operator([[np.cos(angles[1]/2), -np.sin(angles[1]/2)],
                   [np.sin(angles[1]/2), np.cos(angles[1]/2)]])
    Rz2 = Operator([[np.exp(-1j*angles[2]/2), 0], [0, np.exp(1j*angles[2]/2)]])

    #define A,B,C
    A = Operator(Rz1 @ Operator([[np.cos(angles[1]/4), -np.sin(angles[1]/4)],
                   [np.sin(angles[1]/4), np.cos(angles[1]/4)]]))
    B = Operator(Operator([[np.cos(angles[1]/4), np.sin(angles[1]/4)],
                   [-np.sin(angles[1]/4), np.cos(angles[1]/4)]]) @ Operator([[np.exp(-1j*(-angles[2]/2 - angles[0]/2)/2), 0], [0, np.exp(1j*(-angles[2]/2 - angles[0]/2)/2)]]))
    C = Operator([[np.exp(-1j*(angles[2]/2 - angles[0]/2)/2), 0], [0, np.exp(1j*(angles[2]/2 - angles[0]/2)/2)]])

    X = Operator([[0, 1], [1, 0]])

    #now define quantum circuit
    quantum_registerXs = QuantumRegister(size=1, name="x")
    quantum_registerY = QuantumRegister(size=1, name="y")

    cUckt = QuantumCircuit(quantum_registerXs,quantum_registerY, name="controlled-U")

    cUckt.append(UnitaryGate(C), [quantum_registerY[0]]) #gates are applied in reverse order to match multiplication order
    cUckt.cx(quantum_registerXs[0], quantum_registerY[0])
    cUckt.append(UnitaryGate(B), [quantum_registerY[0]])
    cUckt.cx(quantum_registerXs[0], quantum_registerY[0])
    cUckt.append(UnitaryGate(A), [quantum_registerY[0]])
    cUckt.p(angles[3], quantum_registerXs[0]) #controlled global phase equiv to single phase on control qubit
    
    return cUckt

def multi_controlled_U_gate(U,n):
    #solve for unitary V such that V^2 = U
    eigvals, eigvecs = np.linalg.eig(U.data)
    D = np.diag(np.sqrt(eigvals))
    V = Operator(eigvecs @ D @ np.linalg.inv(eigvecs))
    Vadj = V.adjoint()

    if n == 1:
        return controlled_U_gate(U)
    else:
        #define circuit recursively
        n_minus_1ckt = multi_controlled_U_gate(V, n-1).to_gate()
        n_minus_1ckt.name = f"{n-1}-controlled-V"

        cV = controlled_U_gate(V).to_gate()
        cV.name = "controlled-V"
        cV_adj = controlled_U_gate(Vadj).to_gate()
        cV_adj.name = "controlled-V†"

        #assembling
        quantum_registerXs = QuantumRegister(size=n, name="x")
        quantum_registerY = QuantumRegister(size=1,name="y")
        cUckt = QuantumCircuit(quantum_registerXs,quantum_registerY, name=f"{n}-controlled-U")

        cUckt.compose(cV, qubits=[quantum_registerXs[n-1],quantum_registerY[0]],inplace=True)
        cUckt.mcx(quantum_registerXs[0:n-1], quantum_registerXs[n-1])
        cUckt.compose(cV_adj, qubits=[quantum_registerXs[n-1],quantum_registerY[0]],inplace=True)
        cUckt.mcx(quantum_registerXs[0:n-1], quantum_registerXs[n-1])
        
        regList = [quantum_registerXs[i] for i in range(n-1)]
        regList.append(quantum_registerY[0])

        cUckt.compose(n_minus_1ckt, qubits=regList,inplace=True) 

    
    return cUckt