from qubit import Qubit
from device import QuantumDevice
import qutip as qt
import numpy as np
from typing import List

class QutipQubit(Qubit):
    id: int
    parent: "QutipSimulator"

    def __init__(self, parent_simulator: "QutipSimulator", id: int):
        self.parent = parent_simulator
        self.id = id

    def h(self):
        self.parent._apply(qt.hadamard_transform(), [self.id])

    def x(self):
        self.parent._apply(qt.sigmax(), [self.id])

    def measure(self) -> bool:
        projectors = [
            qt.gate_expand_1toN(
                qt.basis(2, outcome) * qt.basis(2, outcome).dag(),
                self.parent.capacity,
                self.id
            )
            for outcome in (0, 1)
        ]
        post_measurement_states = [
            projector * self.parent.register_state
            for projector in projectors
        ]
        probabilities = [
            post_measurement_state.norm() ** 2
            for post_measurement_state in post_measurement_states
        ]
        sample = np.random.choice([0, 1], p=probabilities)
        self.parent.register_state = post_measurement_states[sample].unit()
        return int(sample)

    def reset(self):
        if self.measure():
            self.x()


class QutipSimulator(QuantumDevice):
    capacity: int
    available_qubits: List[QutipQubit]
    register_state: qt.Qobj

    def __init__(self, capacity=3):
        self.capacity = capacity
        self.available_qubits = [
            QutipQubit(self, i)
            for i in range(capacity)
        ]
        self.register_state = qt.tensor(
            *[
                qt.basis(2, 0)
                for _ in range(capacity)
            ]
        )

    def allocate_qubit(self) -> Qubit:
        if self.available_qubits:
            return self.available_qubits.pop()

    def deallocate_qubit(self, qubit: Qubit):
        qubit.reset()
        self.available_qubits.append(qubit)

    def _apply(self, unitary: qt.Qobj, ids: List[int]):
        if len(ids) == 1:
            matrix = qt.gate_expand_1toN(
                unitary, self.capacity, ids[0]
            )
        else:
            raise ValueError("Only single-bit unitary matrices are supported.")
        self.register_state = matrix * self.register_state