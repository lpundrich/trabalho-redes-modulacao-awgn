## Explicação detalhada do código

1. Mensagem Texto ⇄ Bits
```text
mensagem.py
```

Este módulo cuida da interface entre o mundo humano (texto) e o mundo digital (bits).

![mensagem](img/mensagem.png)

```python
# src/mensagem.py

def texto_para_bits(texto: str) -> list[int]:
    """
    Converte uma string em uma lista de bits (0/1),
    usando codificação ASCII de 8 bits por caractere.
    """
    bits = []
    for char in texto:
        codigo = ord(char)                # inteiro ASCII
        bin_str = format(codigo, '08b')   # ex.: '01000001'
        bits.extend(int(b) for b in bin_str)
    return bits


def bits_para_texto(bits: list[int]) -> str:
    """
    Converte uma lista de bits (0/1) de volta para string.
    Assume que o número de bits é múltiplo de 8.
    """
    if len(bits) % 8 != 0:
        raise ValueError("Quantidade de bits não é múltiplo de 8.")

    chars = []
    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i+8]
        bin_str = ''.join(str(b) for b in byte_bits)
        codigo = int(bin_str, 2)
        chars.append(chr(codigo))

    return ''.join(chars)

```




---
**Função: texto_para_bits(texto)**
Objetivo: Transformar a string "REDES DE COMPUTADORES 2025" em uma lista de 0s e 1s.
Passos:
- Percorre cada caractere da string.
- Converte o caractere para seu código ASCII com ord(c).
    Ex.: 'R' → 82.
- Converte o número para binário de 8 bits, tipo "01010010".
- Quebra essa string em uma lista de inteiros [0,1,0,1,0,0,1,0].
- Vai acumulando tudo numa lista única de bits.

Entrada:
```text
"REDES DE COMPUTADORES 2025"
```

Saída (exemplo simplificado):
```text
[0,1,0,1,0,0,1,0, ... ]
```

Essa lista é o bits_tx que é usado no main.py e manda para:
- manchester_codificar (pipeline da mensagem)
- bpsk_modular / qpsk_modular (simulações)


**Função: bits_para_texto(bits)**
Objetivo:
Reconverter a sequência de bits recebidos em uma string legível.
Passos:
- Garante que o número de bits é múltiplo de 8.
- Agrupa de 8 em 8:
    - [0,1,0,1,0,0,1,0] → "01010010"
- Converte a string binária para inteiro → int("01010010", 2) → 82.
- Converte para caractere: chr(82) → 'R'.
- Junta todos os caracteres em uma string final.

Entrada:
```text
[0,1,0,1,0,0,1,0, ... ]
```

Saída:
```text
"REDES DE COMPUTADORES 2025"
```

Essa função é usada no pipeline Manchester, para reconstruir a mensagem mensagem_rx.
