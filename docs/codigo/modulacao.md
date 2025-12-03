## Modulação – BPSK e QPSK ##

Funções que mapeiam bits em símbolos e fazem o processo inverso.


---

1. **BPSK**

**bpsk_modular**

Objetivo:
 Mapear cada bit em um símbolo real:
- 0 → −1
- 1 → +1

```python
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
```

Entrada: [0,1,0,1,...]

Saída: [-1, +1, -1, +1, ...] (como numpy.array)

Esses símbolos são passados para adicionar_ruido_awgn.

---

**bpsk_demodular**

Objetivo:
Converter os símbolos ruidosos de volta em bits.
Regra:
- se simbolo > 0 → 1
- se simbolo ≤ 0 → 0

```python
def bpsk_demodular(simbolos: np.ndarray) -> List[int]:
    """
    Demodulação BPSK:
    símbolo > 0  -> bit 1
    símbolo <= 0 -> bit 0
    """
    bits = (simbolos > 0).astype(int)
    return bits.tolist()
```

---

2. **QPSK**
Aqui entram símbolos complexos e 2 bits por símbolo.

**qpsk_modular**

Objetivo:
Agrupar bits de 2 em 2 e mapear em um ponto na constelação QPSK (I+jQ).
Passos:
- Garante número par de bits (no main.py isso já foi feito).
- Percorre a lista em passos de 2.
- Aplica mapeamento Gray, normalizado por 1/√2:

    ![Mapeamento Gray](img/mapeamentoGray.png)

- Cria um numpy.array complexo com esses símbolos.

```python
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
```

---

**qpsk_demodular**

Objetivo:
Pegar os símbolos complexos (com ruído) e voltar para os pares de bits.
Passos:
1.	Para cada símbolo s:
    - I = s.real
    - Q = s.imag
2.	Decide o par de bits com base no quadrante:
    - I > 0, Q > 0 → bits 00
    - I < 0, Q > 0 → bits 01
    - I < 0, Q < 0 → bits 11
    - I > 0, Q < 0 → bits 10
3.	Vai acumulando os bits numa lista.
Entrada: array de símbolos complexos (ruidosos)
Saída: lista de bits [0,0,0,1,1,1,1,0,...]
No main.py, esses bits são comparados com os bits transmitidos para cálculo de BER.

```python
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
```
