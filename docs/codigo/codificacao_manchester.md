## Codificação Manchester ##

Esse arquivo implementa a codificação de linha, que mexe na forma do sinal no tempo, não na modulação em si.


```python
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
            niveis.extend([-[-1, +1]])
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
```

---

**manchester_codificar**
Objetivo:
Transformar cada bit em um par de níveis +1/−1 de acordo com a Manchester.

Regra utilizada:
- bit 0 → [-1, +1]
- bit 1 → [+1, -1]

Entrada:
```[0, 1, 0, 1, ...]```

Saída:
```[-1, +1, +1, -1, +1, +1, -1, ...]```

No main.py, esse resultado é transformado em np.array e mandado para o canal AWGN.

---

**manchester_decodificar(niveis)**
Objetivo:
Fazer o caminho inverso: pegar os pares de níveis (+1/−1) e recuperar os bits.

Passos:
1. Caminhar de 2 em 2 elementos:
2. Decidir o bit:
    - Se par == [-1, +1] → bit 0
    - Se par == [+1, -1] → bit 1
    - Se for algo do tipo [1, 1] ou [-1, -1] (por causa do ruído), faz:

```python
media = sum(par) / 2
bits.append(1 if media > 0 else 0)
```

Isso torna a decodificação robusta ao ruído do canal AWGN.


3. Retorna a lista de bits decodificados.

Entrada:
Uma sequência com ruído já decidido para +1/-1, tipo:
```[+1, -1, -1, +1, +1, -1, ...]```

Saída:
```[1, 0, 1, ...]```

No main.py, esses bits vão para bits_para_texto e para o cálculo de BER.

