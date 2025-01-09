import hashlib
import struct
import time

def compact_to_target(compact):
    """
    Converte o valor compactado de dificuldade (nBits) em um target real.
    """
    exponent = (compact >> 24) & 0xFF
    mantissa = compact & 0xFFFFFF

    if exponent <= 3:
        target = mantissa >> (8 * (3 - exponent))
    else:
        target = mantissa << (8 * (exponent - 3))
    return target

def generate_genesis_block(timestamp, pszTimestamp, pubkey, nBits, nTime=None, nNonce=None):
    """
    Gera o bloco gênesis baseado nos parâmetros fornecidos.
    """
    if nTime is None:
        nTime = int(timestamp)

    genesis = {
        "version": 1,
        "prev_block": "0" * 64,
        "merkle_root": hashlib.sha256(hashlib.sha256(pszTimestamp.encode('utf-8')).digest()).hexdigest(),
        "timestamp": nTime,
        "bits": nBits,
        "nonce": nNonce if nNonce is not None else 0,
    }

    target = compact_to_target(nBits)
    genesis_hash = calculate_hash(genesis)

    print("Iniciando mineração do bloco gênesis...")
    while int(genesis_hash, 16) > target:
        genesis["nonce"] += 1
        genesis_hash = calculate_hash(genesis)

    genesis["hash"] = genesis_hash
    return genesis

def calculate_hash(genesis):
    """
    Calcula o hash SHA-256 duplo do cabeçalho do bloco.
    """
    header = struct.pack("<L32s32sLLL",
                         genesis["version"],
                         bytes.fromhex(genesis["prev_block"]),
                         bytes.fromhex(genesis["merkle_root"]),
                         genesis["timestamp"],
                         genesis["bits"],
                         genesis["nonce"])
    return hashlib.sha256(hashlib.sha256(header).digest()).hexdigest()

if __name__ == "__main__":
    pszTimestamp = "Hashvive nasceu hoje!"  # Mensagem personalizada para o bloco gênesis
    pubkey = "04ffff001d010445"  # Exemplo de chave pública
    nBits = 0x1d00ffff  # Dificuldade inicial padrão do Bitcoin

    print("Gerando bloco gênesis...")
    genesis_block = generate_genesis_block(int(time.time()), pszTimestamp, pubkey, nBits)
    print("Bloco gênesis gerado com sucesso!")
    print("Hash:", genesis_block["hash"])
    print("Merkle Root:", genesis_block["merkle_root"])
    print("Nonce:", genesis_block["nonce"])
    print("Timestamp:", genesis_block["timestamp"])
