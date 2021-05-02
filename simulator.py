from qubit import Qubit
from device import QuantumDevice
import numpy as np

KET_0 = np.array([
    [1],
    [0]
], dtype=complex)
H = np.array([
    [1, 1],
    [1, -1]
], dtype=complex) / np.sqrt(2)
X = np.array([
    [0, 1],
    [1, 0]
], dtype=complex) / np.sqrt(2)

class SimulatedQubit(Qubit):
    def __init__(self):
        self.reset()

    def h(self):
        self.state = H @ self.state

    def x(self):
        self.state = X @ self.state

    def measure(self) -> bool:
        pr0 = np.abs(self.state[0, 0]) ** 2
        sample = np.random.random() <= pr0
        return False if sample else True

    def reset(self):
        self.state = KET_0.copy()

class QuantumSimulator(QuantumDevice):
    def __init__(self):
        self.reset()

    def allocate_qubit(self) -> Qubit:
        qubit = SimulatedQubit()
        self.qubits.append(qubit)
        return qubit

    def deallocate_qubit(self, qubit: Qubit):
        self.qubits.remove(qubit)

    def reset(self):
        self.qubits = []