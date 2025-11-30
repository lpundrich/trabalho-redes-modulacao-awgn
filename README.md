# Simulação de Codificação de Canal e Modulação Digital em Canal AWGN

Trabalho da disciplina **Redes de Computadores** – UNISINOS  
Aluno(a): *Luana Pündrich*  

Este projeto implementa um sistema completo de transmissão digital, incluindo:

- Conversão **texto ⇄ bits**
- **Codificação de linha Manchester**
- **Modulação digital BPSK e QPSK**
- **Canal AWGN** com controle de SNR em dB
- **Demodulação**
- **Cálculo da taxa de erro de bits (BER)**
- Geração de **gráficos BER × SNR** e **logs** dos testes

---

## 1. Estrutura do Projeto

```text
src/
  mensagem.py          # texto <-> bits
  codificacao_linha.py # codificação / decodificação Manchester
  modulacao.py         # BPSK e QPSK
  canal.py             # canal AWGN
main.py                # script principal (demonstrações e simulações)
results/
  pipeline_manchester_log.txt  # log da transmissão com Manchester
  ber_bpsk_qpsk.csv            # tabela BER x SNR
  ber_bpsk_qpsk.png            # gráfico BER x SNR
requirements.txt       # dependências Python

```

---

## 2. Como executar o projeto
### 2.1. Pré-requisitos

- Python **3.10+**
- `pip` funcionando corretamente

---

### 2.2. Criar ambiente virtual (recomendado)

No diretório do projeto:

```bash
python -m venv .venv
```


# Windows (CMD):
```.\.venv\Scripts\activate.bat```
# ou PowerShell:
```.\.venv\Scripts\Activate.ps1```

### 2.3. Instalar dependências
```pip install -r requirements.txt```

### 2.4. Executar as simulações
```python main.py```


A execução produz:

- Demonstração da transmissão com Manchester para SNR = 2, 5 e 10 dB
- Tabela comparativa BER × SNR para BPSK e QPSK
- Arquivos na pasta results/:
  - pipeline_manchester_log.txt
  - ber_bpsk_qpsk.csv
  - ber_bpsk_qpsk.png

---

## 3. Descrição do Funcionamento
### 3.1. Conversão texto ⇄ bits (```src/mensagem.py```)

```texto_para_bits(texto)```
Converte cada caractere ASCII em 8 bits (0 ou 1).

```bits_para_texto(bits)```
Reconstrói a string original a partir dos bits (múltiplo de 8).

### 3.2. Codificação de Linha – Manchester (```src/codificacao_linha.py```)

Codificação
```bit 1 → [+1, -1]```
```bit 0 → [-1, +1]```

```manchester_codificar(bits)```
Gera a sequência de níveis (+1/-1).

```manchester_decodificar(niveis)```
Faz o processo inverso, com decisão robusta ao ruído:
- Reconhece os pares ideais [+1, -1] e [-1, +1]
- Para pares inválidos (devidos ao ruído), decide pelo sinal médio.

### 3.3. Modulação Digital (src/modulacao.py)

BPSK

```bpsk_modular(bits)```
Mapeia bits em símbolos reais:

```0 → -1```
```1 → +1```

```bpsk_demodular(simbolos)```
Faz decisão por limiar:

```símbolo > 0 → 1```
```símbolo ≤ 0 → 0```

QPSK

```qpsk_modular(bits)```
- Agrupa bits em pares
- Usa mapeamento Gray
- Normaliza por 1/√2 para energia unitária

```qpsk_demodular(simbolos)```
- Recupera os bits a partir do quadrante (parte real/imag).


### 3.4. Canal AWGN (```src/canal.py```)

```adicionar_ruido_awgn(simbolos, snr_db)```
Adiciona ruído gaussiano branco ao sinal:
- Converte SNR de dB para linear
- Calcula a energia média dos símbolos
- Define a variância do ruído em função da SNR
- Gera ruído:
  - Real (BPSK)
  - Complexo (QPSK, em I e Q)
---

## 4. Testes, Logs e Gráficos
### 4.1. Pipeline completo com Manchester

A função:

```transmitir_mensagem_manchester(mensagem, snr_db)```

Executa:
1. texto → bits
1. bits → Manchester
3. canal AWGN
4. decisão de nível
5. decodificação
6. bits → texto
7. cálculo da BER

Resultados em:
```results/pipeline_manchester_log.txt```

### 4.2. Simulação BER × SNR – BPSK vs QPSK

Ainda no main.py, as funções:

simular_ber(bpsk_modular, bpsk_demodular, ...)
simular_ber(qpsk_modular, qpsk_demodular, ...)


fazem:

geração de 100.000 bits aleatórios

modulação (BPSK ou QPSK)

passagem pelo canal AWGN

demodulação

cálculo da BER para cada SNR em [0, 2, 4, 6, 8, 10] dB

Os resultados são apresentados em:

Tabela no terminal

Arquivo CSV: results/ber_bpsk_qpsk.csv

Gráfico: results/ber_bpsk_qpsk.png

---

## 5. Vídeo de Demonstração

Um vídeo curto (até 5 minutos) demonstra:

Estrutura do projeto

Execução do main.py

Exemplo da transmissão com Manchester para diferentes SNR

Gráfico comparativo BER × SNR para BPSK e QPSK
