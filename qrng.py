from device import QuantumDevice
from simulator import QuantumSimulator
from qutipsim import QutipSimulator

def qrng(dev: QuantumDevice) -> bool:
    with dev.using_qubit() as qubit:
        qubit.h()
        return qubit.measure()

if __name__ == "__main__":
    dev = QutipSimulator()

    results = { True: 0, False: 0 }
    iters = 10_000
    for i in range(iters):
        res = qrng(dev)
        # print(f"res={res}")
        results[res] += 1

    print(f"Results:")
    for kvp in results:
        print(f"{kvp}={results[kvp]} ({100 * results[kvp] / iters}%)")

