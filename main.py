# main.py

import numpy as np
import matplotlib.pyplot as plt
import os
import csv

from src.modulacao import (
    bpsk_modular,
    bpsk_demodular,
    qpsk_modular,
    qpsk_demodular,
)
from src.canal import adicionar_ruido_awgn
from src.mensagem import texto_para_bits, bits_para_texto
from src.codificacao_linha import manchester_codificar, manchester_decodificar


def calcular_ber(bits_tx, bits_rx) -> float:
    """Calcula a taxa de erro de bits (BER)."""
    if len(bits_tx) != len(bits_rx):
        raise ValueError("Vetores de bits com tamanhos diferentes.")
    erros = sum(b1 != b2 for b1, b2 in zip(bits_tx, bits_rx))
    return erros / len(bits_tx)


def simular_ber(modular, demodular, snrs_db, num_bits: int, nome: str):
    """Simula BER x SNR para uma modulação genérica."""
    bers = []

    if nome.upper() == "QPSK" and num_bits % 2 != 0:
        num_bits += 1  # garante número par de bits

    print("\n" + "-" * 60)
    print(f"SIMULAÇÃO BER × SNR — {nome.upper()}")
    print(f"Bits por simulação: {num_bits:,}")
    print("-" * 60)

    for snr_db in snrs_db:
        bits_tx_np = np.random.randint(0, 2, size=num_bits)
        bits_tx = bits_tx_np.tolist()

        simbolos_tx = modular(bits_tx)
        simbolos_rx = adicionar_ruido_awgn(simbolos_tx, snr_db)
        bits_rx = demodular(simbolos_rx)

        # em QPSK, por segurança, corta qualquer excesso
        bits_rx = bits_rx[:len(bits_tx)]

        ber = calcular_ber(bits_tx, bits_rx)
        bers.append(ber)

        print(f"SNR = {snr_db:>2} dB | BER = {ber:.6e}")

    return bers


def transmitir_mensagem_manchester(mensagem: str, snr_db: float):
    """Pipeline completo com Manchester + canal AWGN."""

    bits_tx = texto_para_bits(mensagem)
    niveis_tx = manchester_codificar(bits_tx)
    niveis_tx_np = np.array(niveis_tx, dtype=float)

    niveis_rx_continuo = adicionar_ruido_awgn(niveis_tx_np, snr_db)

    # decisão de nível
    niveis_rx = [1 if v > 0 else -1 for v in niveis_rx_continuo]

    # decodificação
    bits_rx = manchester_decodificar(niveis_rx)
    mensagem_rx = bits_para_texto(bits_rx)

    # BER
    ber = calcular_ber(bits_tx, bits_rx)

    return mensagem_rx, ber, len(bits_tx)


def main():

    os.makedirs("results", exist_ok=True)

    # ============================================================
    # Parte 1 — Demonstração Manchester
    # ============================================================

    print("=" * 70)
    print("DEMONSTRAÇÃO: Manchester + Canal AWGN")
    print("=" * 70)

    mensagem = "REDES DE COMPUTADORES 2025"

    with open("results/pipeline_manchester_log.txt", "w", encoding="utf-8") as flog:
        flog.write("Demonstração do pipeline completo com Manchester + canal AWGN\n")
        flog.write(f"Mensagem original: {mensagem}\n\n")

        for snr_db in [2, 5, 10]:
            mensagem_rx, ber, nbits = transmitir_mensagem_manchester(mensagem, snr_db)

            bloco = (
                "-" * 60 + "\n"
                f"SNR = {snr_db} dB\n"
                f"Número de bits transmitidos: {nbits}\n"
                f"Mensagem transmitida : {mensagem}\n"
                f"Mensagem recebida    : {mensagem_rx}\n"
                f"BER = {ber:.6f}\n"
                + "-" * 60 + "\n\n"
            )

            print(bloco)
            flog.write(bloco)

    # ============================================================
    # Parte 2 — BER BPSK vs QPSK
    # ============================================================

    snrs_db = [0, 2, 4, 6, 8, 10]
    num_bits = 100_000

    bers_bpsk = simular_ber(bpsk_modular, bpsk_demodular, snrs_db, num_bits, "BPSK")
    bers_qpsk = simular_ber(qpsk_modular, qpsk_demodular, snrs_db, num_bits, "QPSK")

    print("\n" + "=" * 70)
    print("TABELA COMPARATIVA BER × SNR")
    print("=" * 70)
    print("SNR (dB) |   BER BPSK    |   BER QPSK")
    print("---------------------------------------------")

    for snr, ber_b, ber_q in zip(snrs_db, bers_bpsk, bers_qpsk):
        print(f"{snr:7d} | {ber_b:12.6e} | {ber_q:12.6e}")

    # salva CSV
    with open("results/ber_bpsk_qpsk.csv", "w", newline="", encoding="utf-8") as fcsv:
        writer = csv.writer(fcsv)
        writer.writerow(["SNR_dB", "BER_BPSK", "BER_QPSK"])
        for snr, ber_b, ber_q in zip(snrs_db, bers_bpsk, bers_qpsk):
            writer.writerow([snr, ber_b, ber_q])

    # ============================================================
    # Gráfico BPSK vs QPSK
    # ============================================================

    plt.figure()
    plt.semilogy(snrs_db, bers_bpsk, marker="o", label="BPSK")
    plt.semilogy(snrs_db, bers_qpsk, marker="s", label="QPSK")
    plt.xlabel("SNR (dB)")
    plt.ylabel("BER")
    plt.title("BER × SNR - BPSK vs QPSK")
    plt.grid(True, which="both")
    plt.legend()

    plt.savefig("results/ber_bpsk_qpsk.png", dpi=300)
    plt.close()  # evita erro em ambientes sem GUI


if __name__ == "__main__":
    main()
