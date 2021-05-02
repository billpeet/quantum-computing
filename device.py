from qubit import Qubit
from abc import ABCMeta, abstractmethod
from contextlib import contextmanager

class QuantumDevice(metaclass=ABCMeta):
    @abstractmethod
    def allocate_qubit(self) -> Qubit:
        pass

    @abstractmethod
    def deallocate_qubit(self, qubit: Qubit):
        pass

    @contextmanager
    def using_qubit(self):
        qubit = self.allocate_qubit()
        try:
            yield qubit
        finally:
            qubit.reset()
            self.deallocate_qubit(qubit)