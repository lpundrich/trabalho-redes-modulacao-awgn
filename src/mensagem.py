# src/mensagem.py

def texto_para_bits(texto: str) -> list[int]:
    """
    Converte uma string em uma lista de bits (0/1),
    usando codificação ASCII de 8 bits por caractere.
    """
    bits = []
    for char in texto:
        codigo = ord(char)          # inteiro ASCII
        bin_str = format(codigo, '08b')  # ex.: '01000001'
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
