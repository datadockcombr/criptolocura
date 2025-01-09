import hashlib
import time
import struct

def generate_genesis_block(timestamp, pszTimestamp, pubkey, nBits, nTime=None, nNonce=None):
    if nTime is None:
        nTime = int(time.time())

    genesis = {
        "version": 1,
        "prev_block": "0" * 64,
        "merkle_root": hashlib.sha256(hashlib.sha256(pszTimestamp.encode('utf-8')).digest()).hexdigest(),
        "timestamp": nTime,
        "bits": nBits,
        "nonce": nNonce if nNonce is not None else 0,
    }

    genesis_hash = calculate_hash(genesis)
    while not is_valid_hash(genesis_hash, nBits):
        genesis["nonce"] += 1
        genesis_hash = calculate_hash(genesis)

    genesis["hash"] = genesis_hash
    return genesis

def calculate_hash(genesis):
    header = struct.pack("<L32s32sLLL",
                         genesis["version"],
                         bytes.fromhex(genesis["prev_block"]),
                         bytes.fromhex(genesis["merkle_root"]),
                         genesis["timestamp"],
                         genesis["bits"],
                         genesis["nonce"])
    return hashlib.sha256(hashlib.sha256(header).digest()).hexdigest()

def is_valid_hash(hash_hex, nBits):
    target = (1 << (256 - nBits)) - 1
    return int(hash_hex, 16) <= target

if __name__ == "__main__":
    pszTimestamp = "Hashvive nasceu hoje!"  # Sua mensagem personalizada para o bloco gênesis
    pubkey = "04ffff001d010445"  # Um exemplo de chave pública
    nBits = 0x1d00ffff  # Dificuldade inicial (Bitcoin padrão)

    print("Gerando bloco gênesis...")
    genesis_block = generate_genesis_block(time.time(), pszTimestamp, pubkey, nBits)
    print("Bloco gênesis gerado com sucesso!")
    print("Hash:", genesis_block["hash"])
    print("Merkle Root:", genesis_block["merkle_root"])
    print("Nonce:", genesis_block["nonce"])
    print("Timestamp:", genesis_block["timestamp"])
