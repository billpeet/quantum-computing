from abc import ABCMeta, abstractmethod

class Qubit(metaclass=ABCMeta):
    @abstractmethod
    def h(self):
        pass

    @abstractmethod
    def x(self):
        pass

    @abstractmethod
    def measure(self) -> bool:
        pass

    @abstractmethod
    def reset(self):
        pass