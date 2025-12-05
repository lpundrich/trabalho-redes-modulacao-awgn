# Simulação de Codificação de Canal e Modulação Digital em Canal AWGN

O projeto é dividido em duas pipelines.
- A primeira transmite uma mensagem real usando codificação Manchester e simula um canal com ruído AWGN para observar a recuperação da informação e calcular a BER:

texto → bits → codificação Manchester → canal AWGN  → decodificação Manchester → bits → texto + cálculo da BER (Bit Error Rate).
<br>


- A segunda pipeline é dedicada à análise estatística: gera bits aleatórios, aplica modulação BPSK e QPSK, passa pelo mesmo canal ruidoso e calcula curvas BER×SNR que mostram o desempenho de cada modulação:

bits → modulação (BPSK/QPSK) → canal AWGN → demodulação → bits →Cálculo de BER →gráfico BER x SNR
<br>


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
- O nível de ruído é controlado pelo SNR (Signal-to-Noise Ratio) em dB (2, 5, 10 dB etc).
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

![BER](img/BERformula.png)

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