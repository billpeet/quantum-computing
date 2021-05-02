from device import QuantumDevice
from qubit import Qubit
from simulator import QuantumSimulator
from typing import List

def random_bit(device: QuantumDevice) -> bool:
    with device.using_qubit() as q:
        q.h()
        result = q.measure()
    return result

def prepare_message_qubit(message: bool, basis: bool, q: Qubit):
    if message:
        q.x()
    if basis:
        q.h()

def measure_message_qubit(basis: bool, q: Qubit):
    if basis:
        q.h()
    result = q.measure()
    return result

def convert_to_hex(bits: List[bool]) -> str:
    return hex(int(
        "".join(["1" if bit else "0" for bit in bits]),
        2
    ))

def send_single_bit(sender_device: QuantumDevice, receiver_device: QuantumDevice) -> tuple:
    sender_message = random_bit(sender_device)
    sender_basis = random_bit(sender_device)

    receiver_basis = random_bit(receiver_device)

    with sender_device.using_qubit() as q:
        prepare_message_qubit(sender_message, sender_basis, q)

        # Send message

        receiver_message = measure_message_qubit(receiver_basis, q)
    return ((sender_message, sender_basis), (receiver_message, receiver_basis))

def simulate_bb84(n_bits: int) -> tuple:
    sender_device = QuantumSimulator()
    receiver_device = QuantumSimulator()

    key = []
    n_rounds = 0

    while len(key) < n_bits:
        n_rounds += 1
        ((rec_message, rec_basis), (sen_message, sen_basis)) = \
            send_single_bit(sender_device, receiver_device)
        if sen_basis == rec_basis:
            assert sen_message == rec_message
            key.append(rec_message)
    
    print(f"Took {n_rounds} rounds to generate a {n_bits}-bit key.")

if __name__ == "__main__":
    simulate_bb84(256)