# src/codificacao_linha.py

from typing import List


def manchester_codificar(bits: List[int]) -> List[int]:
    """
    Codificação Manchester:
    - bit 1 -> [+1, -1]
    - bit 0 -> [-1, +1]

    Entrada:
        bits: lista de 0s e 1s
    Saída:
        lista de níveis (+1/-1), com comprimento 2 * len(bits)
    """
    niveis: List[int] = []

    for b in bits:
        if b == 1:
            niveis.extend([+1, -1])
        elif b == 0:
            niveis.extend([-1, +1])
        else:
            raise ValueError(f"Bit inválido na entrada: {b} (esperado 0 ou 1)")

    return niveis


def manchester_decodificar(niveis):
    """
    Decodificação Manchester robusta ao ruído.
    - [+1, -1] -> bit 1
    - [-1, +1] -> bit 0

    Se o par for inválido (ex.: [1, 1] ou [-1, -1]),
    usamos a média dos dois níveis:
        média > 0  -> bit 1
        média <= 0 -> bit 0
    """
    if len(niveis) % 2 != 0:
        raise ValueError("Quantidade de níveis não é múltiplo de 2.")

    bits = []

    for i in range(0, len(niveis), 2):
        par = niveis[i:i+2]

        # Caso perfeito (sem ruído)
        if par == [1, -1]:
            bits.append(1)
        elif par == [-1, 1]:
            bits.append(0)
        else:
            # Tratamento robusto ao ruído
            media = sum(par) / 2
            bits.append(1 if media > 0 else 0)

    return bits
