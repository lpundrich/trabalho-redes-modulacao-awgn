# Simulação de Codificação de Canal e Modulação Digital em Canal AWGN

Trabalho da disciplina **Redes de Computadores** – UNISINOS
Aluno(a): **Luana Pündrich**

Este projeto implementa duas cadeias de transmissão digital, permitindo estudar:

* Conversão **texto ⇄ bits**
* **Codificação de linha Manchester**
* **Canal AWGN** com controle de SNR (ruído)
* **Modulação digital BPSK e QPSK**
* **Demodulação**
* **Cálculo da taxa de erro de bits (BER)**
* Geração de **gráficos BER × SNR** e **logs** dos testes

---

## 1. Estrutura do Projeto

```text
src/
  mensagem.py          # texto <-> bits
  codificacao_linha.py # codificação / decodificação Manchester
  modulacao.py         # BPSK e QPSK
  canal.py             # canal AWGN
main.py                # script principal (pipelines e simulações)
results/
  pipeline_manchester_log.txt  # log da transmissão Manchester
  ber_bpsk_qpsk.csv            # tabela BER x SNR
  ber_bpsk_qpsk.png            # gráfico BER x SNR
requirements.txt               # dependências Python
```

---

## 2. Como executar o projeto

### 2.1. Pré-requisitos

* Python **3.10+**
* `pip` instalado

---

### 2.2. Criar ambiente virtual (recomendado)

No diretório do projeto:

```bash
python -m venv .venv
```

Ativar:

**CMD**

```bash
.\.venv\Scripts\activate.bat
```

**PowerShell**

```bash
.\.venv\Scripts\Activate.ps1
```

---

### 2.3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

### 2.4. Executar o projeto

```bash
python main.py
```

A execução produz:

* Pipeline Manchester com SNR = 2, 5 e 10 dB
* Tabela BER × SNR para BPSK e QPSK
* Arquivos em `results/`:

  * `pipeline_manchester_log.txt`
  * `ber_bpsk_qpsk.csv`
  * `ber_bpsk_qpsk.png`

---

## 3. Descrição do Funcionamento do Sistema

O projeto possui **duas pipelines independentes**:

---

### Pipeline 1 — Transmissão de Texto com Codificação Manchester

```
texto → bits → codificação Manchester → canal AWGN
      → decisão de nível → decodificação Manchester
      → bits → texto → cálculo da BER
```

---

### 3.1. Conversão texto ⇄ bits (`src/mensagem.py`)

**`texto_para_bits(texto)`**
Converte cada caractere ASCII em uma sequência de 8 bits.

**`bits_para_texto(bits)`**
Reconstrói o texto original (bits devem ser múltiplos de 8).

---

### 3.2. Codificação Manchester (`src/codificacao_linha.py`)

**Regras:**

```
1 → [+1, -1]
0 → [-1, +1]
```

**`manchester_codificar(bits)`**
Gera sequência de níveis.

**`manchester_decodificar(niveis)`**
Desfaz a codificação com tolerância ao ruído:

* reconhece pares ideais
* para pares inválidos → usa média dos dois sinais

---

### Pipeline 2 — Simulação BER × SNR para BPSK e QPSK

```
bits aleatórios → modulação (BPSK/QPSK) → canal AWGN
     → demodulação → bits → cálculo da BER
     → geração de gráfico BER × SNR
```

---

### 3.3. Modulação Digital (`src/modulacao.py`)

#### BPSK

```
0 → -1
1 → +1
```

**`bpsk_modular(bits)`**
Gera símbolos reais.

**`bpsk_demodular(simbolos)`**
Decisão por limiar:

* > 0 → 1
* ≤0 → 0

---

#### QPSK (2 bits por símbolo)

Usa **mapeamento Gray normalizado**:

```
00 →  +1/√2 + j +1/√2
01 →  -1/√2 + j +1/√2
11 →  -1/√2 - j -1/√2
10 →  +1/√2 - j -1/√2
```

**`qpsk_modular(bits)`**
Agrupa bits em pares e gera símbolos complexos.

**`qpsk_demodular(simbolos)`**
Decide o par de bits com base no quadrante (I/Q).

---

### 3.4. Canal AWGN (`src/canal.py`)

**`adicionar_ruido_awgn(simbolos, snr_db)`**
Adiciona ruído Gaussiano ao sinal.

Processo:

* Converte SNR (dB → linear)
* Calcula energia média dos símbolos
* Calcula variância do ruído
* Gera ruído:

  * real → BPSK
  * complexo → QPSK

---

## 4. Testes, Logs e Gráficos

### 4.1. Pipeline Manchester

A função:

```python
transmitir_mensagem_manchester(mensagem, snr_db)
```

Executa:

1. texto → bits
2. codificação Manchester
3. canal AWGN
4. decisão de nível
5. decodificação
6. bits → texto
7. cálculo da BER

Resultados:
`results/pipeline_manchester_log.txt`

---

### 4.2. Simulação BER × SNR — BPSK e QPSK

Funções:

```python
simular_ber(bpsk_modular, bpsk_demodular, ...)
simular_ber(qpsk_modular, qpsk_demodular, ...)
```

Realizam:

* geração de 100.000 bits aleatórios
* modulação
* canal AWGN
* demodulação
* cálculo da BER em SNR = 0, 2, 4, 6, 8, 10 dB

Saídas:

* tabela no terminal
* `results/ber_bpsk_qpsk.csv`
* `results/ber_bpsk_qpsk.png`

---

