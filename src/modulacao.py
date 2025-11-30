# src/modulacao.py

import numpy as np
from typing import List


def bpsk_modular(bits: List[int]) -> np.ndarray:
    """
    Modulação BPSK:
    bit 0 -> -1
    bit 1 -> +1

    Retorna array NumPy de floats.
    """
    bits_np = np.array(bits)
    # transforma 0 -> -1 e 1 -> +1
    simbolos = 2 * bits_np - 1
    return simbolos.astype(float)


def bpsk_demodular(simbolos: np.ndarray) -> List[int]:
    """
    Demodulação BPSK:
    símbolo > 0  -> bit 1
    símbolo <= 0 -> bit 0
    """
    bits = (simbolos > 0).astype(int)
    return bits.tolist()



import numpy as np
from typing import List

# ... (suas funções BPSK já aqui em cima)

def qpsk_modular(bits: List[int]) -> np.ndarray:
    """
    Modulação QPSK com mapeamento Gray, normalizada para energia média 1.
    Usa 2 bits por símbolo.

    00 -> ( +1/sqrt(2) + j +1/sqrt(2) )
    01 -> ( -1/sqrt(2) + j +1/sqrt(2) )
    11 -> ( -1/sqrt(2) + j -1/sqrt(2) )
    10 -> ( +1/sqrt(2) + j -1/sqrt(2) )

    Supõe número de bits PAR.
    """
    if len(bits) % 2 != 0:
        raise ValueError("QPSK: número de bits deve ser par.")

    bits_np = np.array(bits).reshape(-1, 2)
    s = 1 / np.sqrt(2)

    simbolos = []
    for b0, b1 in bits_np:
        if b0 == 0 and b1 == 0:
            simbolos.append(s + 1j * s)
        elif b0 == 0 and b1 == 1:
            simbolos.append(-s + 1j * s)
        elif b0 == 1 and b1 == 1:
            simbolos.append(-s - 1j * s)
        elif b0 == 1 and b1 == 0:
            simbolos.append(s - 1j * s)
        else:
            raise ValueError(f"Bits inválidos: {b0}{b1}")

    return np.array(simbolos, dtype=complex)


def qpsk_demodular(simbolos: np.ndarray) -> List[int]:
    """
    Demodulação QPSK (decisão por quadrante) para o mesmo mapeamento Gray.
    """
    bits: List[int] = []
    for s in simbolos:
        i = s.real
        q = s.imag

        if i >= 0 and q >= 0:
            bits.extend([0, 0])
        elif i < 0 and q >= 0:
            bits.extend([0, 1])
        elif i < 0 and q < 0:
            bits.extend([1, 1])
        else:  # i >= 0 and q < 0
            bits.extend([1, 0])

    return bits
