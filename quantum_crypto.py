"""
Quantum Key Distribution (BB84 Protocol) Simulation
Uses Qiskit to simulate quantum key generation for message encryption.
"""
import random
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def generate_bb84_key(length: int) -> list[int]:
    """
    Simulate BB84 QKD protocol to generate a shared secret key.
    Returns a list of bits (0s and 1s) of the requested length.
    """
    simulator = AerSimulator()
    key_bits = []

    while len(key_bits) < length:
        # Alice picks random bits and random bases (0=Z, 1=X)
        alice_bits = [random.randint(0, 1) for _ in range(length * 3)]
        alice_bases = [random.randint(0, 1) for _ in range(length * 3)]
        bob_bases = [random.randint(0, 1) for _ in range(length * 3)]

        for i in range(len(alice_bits)):
            qc = QuantumCircuit(1, 1)

            # Alice prepares qubit
            if alice_bits[i] == 1:
                qc.x(0)  # flip to |1>
            if alice_bases[i] == 1:
                qc.h(0)  # switch to X basis

            # Bob measures
            if bob_bases[i] == 1:
                qc.h(0)  # switch to X basis before measuring
            qc.measure(0, 0)

            result = simulator.run(qc, shots=1).result()
            bob_bit = int(list(result.get_counts().keys())[0])

            # Sift: keep only bits where bases match
            if alice_bases[i] == bob_bases[i]:
                key_bits.append(bob_bit)
                if len(key_bits) >= length:
                    break

    return key_bits[:length]


def xor_encrypt(message: str, key_bits: list[int]) -> str:
    """XOR each character's bits with the key, return encrypted string."""
    msg_bits = ''.join(format(ord(c), '08b') for c in message)
    # Extend key to cover full message
    extended_key = (key_bits * ((len(msg_bits) // len(key_bits)) + 1))[:len(msg_bits)]
    encrypted_bits = ''.join(str(int(b) ^ k) for b, k in zip(msg_bits, extended_key))
    # Pack back into characters
    chars = [chr(int(encrypted_bits[i:i+8], 2)) for i in range(0, len(encrypted_bits), 8)]
    return ''.join(chars)


def xor_decrypt(encrypted: str, key_bits: list[int]) -> str:
    """XOR decryption is symmetric — same operation as encrypt."""
    return xor_encrypt(encrypted, key_bits)


def key_bits_to_str(key_bits: list[int]) -> str:
    """Serialize key bits to a storable string."""
    return ''.join(str(b) for b in key_bits)


def str_to_key_bits(key_str: str) -> list[int]:
    """Deserialize key string back to bits."""
    return [int(b) for b in key_str]
