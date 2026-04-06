# ImageShield - Technical Documentation

## Table of Contents

1. [Overview](#overview)
2. [LSB Steganography](#lsb-steganography)
3. [Quantum Encryption (BB84)](#quantum-encryption-bb84)
4. [OTP Protection](#otp-protection)
5. [Architecture](#architecture)
6. [Security Analysis](#security-analysis)
7. [Implementation Details](#implementation-details)

---

## Overview

ImageShield combines three cryptographic and steganographic techniques to provide layered security for hiding messages in images:

1. **LSB Steganography** - Hides data invisibly in image pixels
2. **BB84 Quantum Key Distribution** - Generates encryption keys using quantum principles
3. **OTP (One-Time Password)** - Simple symmetric encryption layer

The application is built with Streamlit for the web interface, Pillow for image processing, and Qiskit for quantum simulation.

---

## LSB Steganography

### What is LSB Steganography?

Least Significant Bit (LSB) steganography is a technique that hides data by replacing the least significant bits of pixel values in an image. Since the LSB contributes minimally to the overall pixel value, changing it produces imperceptible visual differences.

### How It Works

Each pixel in an RGB image has three color channels (Red, Green, Blue), each represented by an 8-bit value (0-255). ImageShield uses the **red channel** for encoding:

```
Original pixel: (11010110, G, B)  → Red = 214
Message bit: 1
Encoded pixel:  (11010111, G, B)  → Red = 215 (difference of 1)
```

### Encoding Process

1. **Message Preparation**
   - Append delimiter `$` to mark the end of the message
   - Convert each character to 8-bit binary representation
   - Example: `"Hi$"` → `01001000 01101001 00100100`

2. **Pixel Modification**
   - Iterate through image pixels sequentially
   - For each bit in the message:
     - Clear the LSB of the red channel: `pixel[0] & 254` (bitwise AND with 11111110)
     - Set the LSB to the message bit: `| message_bit` (bitwise OR)
   - Leave remaining pixels unchanged

3. **Image Output**
   - Save as PNG to preserve exact pixel values (JPEG compression would corrupt data)

### Decoding Process

1. Extract the LSB from the red channel of each pixel
2. Group bits into 8-bit bytes
3. Convert each byte to a character
4. Stop when delimiter `$` is encountered

### Code Implementation

```python
def encode_data(image, data):
    data += "$"  # Add delimiter
    data_bin = ''.join(format(ord(c), '08b') for c in data)
    pixels = list(image.getdata())
    out = []
    for i, px in enumerate(pixels):
        if i < len(data_bin):
            # Clear LSB and set to message bit
            out.append(((px[0] & 254) | int(data_bin[i]), px[1], px[2]))
        else:
            out.append(px)
    return out
```

### Capacity

- **1 bit per pixel** (using only red channel)
- For a 1920×1080 image: 2,073,600 pixels = 259,200 bytes ≈ 253 KB maximum message size

### Advantages

- Invisible to human eye
- Simple and fast
- No special decoding software needed (just this app)

### Limitations

- Vulnerable to image compression (use PNG, not JPEG)
- No encryption by default (message is readable if extracted)
- Statistical analysis can detect presence of hidden data

---

## Quantum Encryption (BB84)

### What is BB84?

BB84 (Bennett-Brassard 1984) is the first quantum key distribution (QKD) protocol. It uses quantum mechanics principles to generate a shared secret key between two parties, with the guarantee that any eavesdropping attempt will be detected.

### Why Use Quantum Encryption?

Traditional encryption relies on computational hardness (e.g., factoring large numbers). Quantum encryption offers:

- **Information-theoretic security**: Security based on physics, not computational assumptions
- **Eavesdropping detection**: Any measurement of quantum states disturbs them, revealing eavesdroppers
- **Future-proof**: Resistant to quantum computer attacks

### How BB84 Works (Simplified)

1. **Alice's Preparation**
   - Alice randomly chooses bits (0 or 1)
   - Alice randomly chooses bases (Z-basis or X-basis) for each bit
   - Alice encodes bits as quantum states:
     - Z-basis: 0 → |0⟩, 1 → |1⟩
     - X-basis: 0 → |+⟩, 1 → |−⟩

2. **Bob's Measurement**
   - Bob randomly chooses measurement bases (Z or X)
   - Bob measures the quantum states Alice sent

3. **Basis Reconciliation**
   - Alice and Bob publicly compare their basis choices (not the bit values)
   - They keep only the bits where they used the same basis
   - These matching bits form the shared secret key

4. **Error Detection**
   - Alice and Bob compare a subset of bits to check for eavesdropping
   - If error rate is low, the key is secure

### ImageShield's BB84 Simulation

Since we can't transmit actual quantum states over the internet, ImageShield **simulates** the BB84 protocol using Qiskit:

```python
def generate_bb84_key(length: int) -> list[int]:
    simulator = AerSimulator()
    key_bits = []
    
    while len(key_bits) < length:
        # Alice picks random bits and bases
        alice_bits = [random.randint(0, 1) for _ in range(length * 3)]
        alice_bases = [random.randint(0, 1) for _ in range(length * 3)]
        bob_bases = [random.randint(0, 1) for _ in range(length * 3)]
        
        for i in range(len(alice_bits)):
            qc = QuantumCircuit(1, 1)
            
            # Alice prepares qubit
            if alice_bits[i] == 1:
                qc.x(0)  # Flip to |1⟩
            if alice_bases[i] == 1:
                qc.h(0)  # Hadamard gate for X-basis
            
            # Bob measures
            if bob_bases[i] == 1:
                qc.h(0)  # Measure in X-basis
            qc.measure(0, 0)
            
            # Simulate measurement
            result = simulator.run(qc, shots=1).result()
            bob_bit = int(list(result.get_counts().keys())[0])
            
            # Keep bit only if bases match
            if alice_bases[i] == bob_bases[i]:
                key_bits.append(bob_bit)
                if len(key_bits) >= length:
                    break
    
    return key_bits[:length]
```

### Quantum States Used

- **|0⟩ (Z-basis 0)**: Computational basis state, measured as 0 in Z-basis
- **|1⟩ (Z-basis 1)**: Computational basis state, measured as 1 in Z-basis
- **|+⟩ (X-basis 0)**: Superposition (|0⟩ + |1⟩)/√2, measured as 0 in X-basis
- **|−⟩ (X-basis 1)**: Superposition (|0⟩ − |1⟩)/√2, measured as 1 in X-basis

### XOR Encryption with Quantum Key

Once the quantum key is generated, it's used to encrypt the message via XOR:

```python
def xor_encrypt(message: str, key_bits: list[int]) -> str:
    msg_bits = ''.join(format(ord(c), '08b') for c in message)
    # Extend key to cover full message
    extended_key = (key_bits * ((len(msg_bits) // len(key_bits)) + 1))[:len(msg_bits)]
    # XOR each bit
    encrypted_bits = ''.join(str(int(b) ^ k) for b, k in zip(msg_bits, extended_key))
    # Pack back into characters
    chars = [chr(int(encrypted_bits[i:i+8], 2)) for i in range(0, len(encrypted_bits), 8)]
    return ''.join(chars)
```

### Why This Approach?

1. **Educational Value**: Demonstrates quantum principles in a practical application
2. **Key Generation**: Uses true quantum randomness (simulated) for key generation
3. **Symmetric Encryption**: XOR with quantum key provides fast, secure encryption
4. **Layered Security**: Combines quantum key generation with classical steganography

### Limitations

- **Simulation Only**: Not using real quantum hardware or quantum communication channels
- **Key Distribution**: The quantum key must be shared separately (displayed in the UI)
- **No Eavesdropping Detection**: Since it's simulated, we can't detect eavesdropping
- **Educational Purpose**: Not intended for production cryptographic use

---

## OTP Protection

### What is OTP?

OTP (One-Time Password) in this context refers to a 6-digit numeric code used as a symmetric encryption key.

### How It Works

1. **Key Generation**
   ```python
   def generate_otp():
       return str(random.randint(100000, 999999))
   ```

2. **Encryption/Decryption**
   ```python
   def otp_crypt(text, otp):
       return ''.join(chr(ord(c) ^ int(otp[i % len(otp)])) for i, c in enumerate(text))
   ```
   
   - Each character in the message is XORed with a digit from the OTP
   - The OTP cycles if the message is longer than 6 characters
   - XOR is symmetric: `decrypt(encrypt(msg, key), key) = msg`

### Example

```
Message: "Hello"
OTP: "482910"

Encryption:
H (72) XOR 4 = 76 (L)
e (101) XOR 8 = 109 (m)
l (108) XOR 2 = 110 (n)
l (108) XOR 9 = 101 (e)
o (111) XOR 1 = 110 (n)

Encrypted: "Lmnen"
```

### Security

- **Weak Key Space**: Only 1,000,000 possible keys (6 digits)
- **Brute-Force Vulnerable**: Can be cracked quickly with automated tools
- **Cycling Key**: Reusing OTP digits weakens security for long messages
- **Best Use**: As an additional layer, not sole protection

---

## Architecture

### File Structure

```
image_steganography_project/
├── main.py              # Streamlit UI and application logic
├── styles.py            # CSS styling for the web interface
├── quantum_crypto.py    # BB84 simulation and quantum encryption
├── requirements.txt     # Python dependencies
├── README.md           # User documentation
└── DOCUMENTATION.md    # This file
```

### Data Flow

#### Encoding Flow

```
User Input (Message + Image)
    ↓
[Optional] OTP Encryption
    ↓
[Optional] Quantum Encryption (BB84 Key Generation → XOR)
    ↓
LSB Steganography (Embed in Image)
    ↓
Output: Encoded Image + Keys (if used)
```

#### Decoding Flow

```
Encoded Image
    ↓
LSB Extraction (Extract Hidden Bits)
    ↓
[Optional] Quantum Decryption (XOR with Key)
    ↓
[Optional] OTP Decryption
    ↓
Output: Original Message
```

### Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Image Processing**: Pillow (PIL fork)
- **Quantum Simulation**: Qiskit + Qiskit Aer
- **Styling**: Custom CSS injected via Streamlit

---

## Security Analysis

### Threat Model

**Assumptions:**
- Attacker has access to the encoded image
- Attacker knows LSB steganography is used
- Attacker does not have the OTP or quantum key

**Attack Vectors:**
1. **LSB Extraction**: Attacker extracts LSB bits from red channel
2. **Statistical Analysis**: Detect presence of hidden data via chi-square test
3. **Brute Force**: Try all possible OTP codes (1M combinations)
4. **Known Plaintext**: If attacker knows part of the message, can derive key

### Security Levels

| Mode | Security Level | Resistance |
|------|---------------|------------|
| LSB Only | Low | Vulnerable to extraction |
| LSB + OTP | Medium | Resistant to casual extraction, vulnerable to brute force |
| LSB + Quantum | High | Resistant to extraction and brute force (if key is secret) |
| LSB + OTP + Quantum | Very High | Multiple layers of protection |

### Best Practices

1. **Always use PNG format** - JPEG compression corrupts hidden data
2. **Use Quantum Mode for sensitive data** - Provides strong encryption
3. **Keep keys secret** - Never share OTP or quantum key publicly
4. **Use large images** - More pixels = more capacity and harder to detect
5. **Don't reuse keys** - Generate new OTP/quantum key for each message

---

## Implementation Details

### Key Functions

#### `encode_data(image, data)`
Embeds data into image using LSB steganography.

**Parameters:**
- `image`: PIL Image object
- `data`: String message to hide

**Returns:** List of modified pixel tuples

#### `decode_data(image)`
Extracts hidden data from image.

**Parameters:**
- `image`: PIL Image object with hidden data

**Returns:** Extracted message string

#### `generate_bb84_key(length)`
Simulates BB84 protocol to generate quantum key.

**Parameters:**
- `length`: Number of key bits to generate

**Returns:** List of random bits (0s and 1s)

#### `xor_encrypt(message, key_bits)`
Encrypts message using XOR with quantum key.

**Parameters:**
- `message`: Plaintext string
- `key_bits`: List of key bits from BB84

**Returns:** Encrypted string

#### `otp_crypt(text, otp)`
Encrypts/decrypts text using OTP.

**Parameters:**
- `text`: Input string
- `otp`: 6-digit OTP string

**Returns:** Encrypted/decrypted string

### Performance Considerations

- **Image Size**: Larger images take longer to process (linear time complexity)
- **Quantum Key Generation**: BB84 simulation is computationally expensive (O(n) quantum circuits)
- **Memory Usage**: Entire image is loaded into memory (consider streaming for very large images)

### Error Handling

- Invalid image formats are rejected
- Missing OTP/quantum key shows error message
- Corrupted encoded images may produce garbled output
- Delimiter `$` not found indicates no hidden message

---

## Future Enhancements

1. **Real Quantum Hardware**: Integrate with IBM Quantum or other quantum cloud services
2. **Multiple Channels**: Use all RGB channels for 3x capacity
3. **Compression Resistance**: Implement error correction codes
4. **Key Exchange Protocol**: Automate secure key sharing
5. **Steganography Detection**: Add tools to detect hidden data in images
6. **Advanced Encryption**: Support AES, RSA, or other standard algorithms

---

## References

1. Bennett, C. H., & Brassard, G. (1984). "Quantum cryptography: Public key distribution and coin tossing"
2. Qiskit Documentation: https://qiskit.org/documentation/
3. LSB Steganography: https://en.wikipedia.org/wiki/Steganography
4. BB84 Protocol: https://en.wikipedia.org/wiki/BB84

---

## Conclusion

ImageShield demonstrates how classical steganography can be enhanced with quantum-inspired cryptography to create a multi-layered security system. While the quantum simulation is educational rather than production-grade, it showcases the potential of quantum key distribution in practical applications.

The combination of LSB steganography (hiding), BB84 quantum encryption (securing), and OTP protection (additional layer) provides a robust framework for secret communication through images.

For questions or contributions, please visit the [GitHub repository](https://github.com/madhavchaturvedi005/image_steganography_project).
