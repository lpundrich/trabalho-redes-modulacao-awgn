# Simulação de Codificação de Canal e Modulação Digital em Canal AWGN

O trabalho implementa, em Python, uma cadeia completa de transmissão digital, parecida com o que acontece num sistema real de comunicação (modem, Wi-Fi, rádio digital):
texto → bits → codificação Manchester → modulação (BPSK/QPSK) → canal AWGN → demodulação → decodificação Manchester → bits → texto + cálculo da BER

```mermaid
flowchart TD

    A[Início] --> B[Mensagem de Texto<br>(ex: 'REDES DE COMPUTADORES 2025')]
    B --> C[Conversão Texto → Bits<br>(ASCII 8 bits por caractere)]
    C --> D[Codificação Manchester<br>0 → (-1,+1)<br>1 → (+1,-1)]
    D --> E[Modulação Digital]
    
    E -->|BPSK| E1[BPSK<br>0 → -1<br>1 → +1]
    E -->|QPSK| E2[QPSK<br>2 bits → símbolo complexo]

    E1 --> F[Canal AWGN<br>Adição de ruído<br>SNR = 0–10 dB]
    E2 --> F

    F --> G[Demodulação]
    G -->|BPSK| G1[Decisão por limiar<br>x>0 → 1<br>x<=0 → 0]
    G -->|QPSK| G2[Decisão por quadrante<br>I/Q]

    G1 --> H[Decodificação Manchester<br>Pares (+1,-1) ou (-1,+1)]
    G2 --> H
    
    H --> I[Bits Recebidos]
    I --> J[Conversão Bits → Texto]
    J --> K[Comparação TX vs RX<br>Cálculo da BER]

    K --> L[Fim]
```



## 1. Geração de mensagem
- Usa uma mensagem de texto: REDES DE COMPUTADORES 2025.
- Converte cada caractere para 8 bits (ASCII): Ex.: 'R' → 01010010.

## 2. Codificação de linha Manchester
- Cada bit é mapeado em dois níveis (+1 e −1) no tempo:
    - bit 0 → [-1, +1]
    - bit 1 → [+1, -1]
- Isso gera uma forma de onda digital com uma transição no meio de cada bit, facilitando sincronismo entre transmissor e receptor.

## 3. Transmissão pelo canal com ruído (AWGN)
- Essa sequência de níveis (+1/−1) passa por um canal AWGN (Additive White Gaussian Noise → ruído branco gaussiano aditivo).
- O nível de ruído é controlado pelo SNR em dB (2, 5, 10 dB etc).
- O canal “suja” a forma de onda, simulando interferência, ruído térmico etc.

## 4. Decisão de nível + decodificação Manchester
- O receptor observa o sinal ruidoso e, em cada amostra, decide:
    - valor > 0 → +1
    - valor ≤ 0 → −1
- A partir dos pares [+1, −1] / [−1, +1], reconstrói os bits:
    - [+1, −1] → 1
    - [-1, +1] → 0
- Em pares “estranhos” (por causa do ruído), a decodificação usa a média dos dois níveis para decidir o bit — isso deixa o sistema mais robusto.

## 5. Reconstrução do texto e BER
- Os bits recebidos são agrupados de 8 em 8 e convertidos de volta para caracteres.
- Compara-se bit a bit com a sequência original → calcula a BER (Bit Error Rate):
    ```text
    BER = (número de bits errados) / (número total de bits)

- Os resultados para SNR = 2, 5, 10 dB vão para:
    - terminal
    - results/pipeline_manchester_log.txt.

## 6. Simulação estatística BER × SNR com BPSK e QPSK
- Além da mensagem fixa, o programa gera 100.000 bits aleatórios.
- Faz duas versões de modulação:
    - BPSK: 0 → −1, 1 → +1
    - QPSK: 2 bits por símbolo, mapeados em pontos complexos (I/Q) com mapeamento Gray.
- Em cada SNR (0, 2, 4, 6, 8, 10 dB):
    - Modula → passa pelo AWGN → demodula → calcula BER.
- Resultado:
    - tabela no terminal
    - arquivo results/ber_bpsk_qpsk.csv
    - gráfico results/ber_bpsk_qpsk.png comparando as curvas.