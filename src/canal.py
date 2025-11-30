# src/canal.py

import numpy as np

def adicionar_ruido_awgn(simbolos: np.ndarray, snr_db: float) -> np.ndarray:
    """
    Adiciona ruído AWGN a um vetor de símbolos (reais ou complexos).
    """
    snr_linear = 10 ** (snr_db / 10)

    # Energia média dos símbolos (vale para BPSK e QPSK normalizada)
    energia_simbolo = np.mean(np.abs(simbolos) ** 2)

    # Variância total do ruído
    sigma2 = energia_simbolo / snr_linear

    if np.iscomplexobj(simbolos):
        # Para sinal complexo, ruído em I e Q com sigma2/2 cada
        ruido_real = np.sqrt(sigma2 / 2) * np.random.randn(len(simbolos))
        ruido_imag = np.sqrt(sigma2 / 2) * np.random.randn(len(simbolos))
        ruido = ruido_real + 1j * ruido_imag
    else:
        # Para BPSK (real)
        ruido = np.sqrt(sigma2) * np.random.randn(len(simbolos))

    return simbolos + ruido
