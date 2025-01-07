import hashlib
import struct
import time

# Parâmetros do Bloco Gênesis
pszTimestamp = "HashRevive - Revitalizando o legado das máquinas antigas"
pubkey = "04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f"
nTime = int(time.time())  # Use o timestamp atual
nBits = 0x1d00ffff  # Dificuldade inicial
nNonce = 0  # Começa com zero

# Recompensa inicial do bloco
genesisReward = 50 * 10**8  # 50 moedas em satoshis

# Função para criar o hash
def sha256d(data):
    return hashlib.sha256(hashlib.sha256(data).digest()).digest()

# Criar o header do bloco
def genesis_block(pszTimestamp, pubkey, nTime, nBits, nNonce):
    pszTimestamp = pszTimestamp.encode('utf-8')
    scriptSig = (
        struct.pack("<I", len(pszTimestamp)) + pszTimestamp +
        struct.pack("<I", len(bytes.fromhex(pubkey))) + bytes.fromhex(pubkey)
    )
    scriptPubKey = bytes.fromhex(pubkey)
    
    txNew = (
        struct.pack("<I", 1) +  # Versão da transação
        struct.pack("<B", 1) +  # Número de entradas
        bytes(32) +  # Hash do bloco anterior (vazio para gênesis)
        struct.pack("<I", 0xFFFFFFFF) +  # Index
        struct.pack("<B", len(scriptSig)) + scriptSig +
        struct.pack("<I", 0xFFFFFFFF) +  # Sequência
        struct.pack("<B", 1) +  # Número de saídas
        struct.pack("<Q", genesisReward) +  # Valor
        struct.pack("<B", len(scriptPubKey)) + scriptPubKey +
        struct.pack("<I", 0)  # Lock time
    )
    
    txNewHash = sha256d(txNew)
    hashMerkleRoot = sha256d(txNewHash)
    
    header = (
        struct.pack("<I", 1) +  # Versão do bloco
        bytes(32) +  # Hash do bloco anterior (vazio para gênesis)
        hashMerkleRoot +
        struct.pack("<I", nTime) +
        struct.pack("<I", nBits) +
        struct.pack("<I", nNonce)
    )
    return header, hashMerkleRoot

# Minerar o hash do Bloco Gênesis
def mine_genesis_block():
    global nNonce
    print(f"Minerando Bloco Gênesis com timestamp: {pszTimestamp}")
    print(f"Timestamp: {nTime}, Bits: {nBits}")
    
    header, merkle_root = genesis_block(pszTimestamp, pubkey, nTime, nBits, nNonce)
    target = (1 << (256 - nBits // (1 << 24))) - 1

    while True:
        hash_result = sha256d(header)
        if int.from_bytes(hash_result, 'big') < target:
            print(f"Hash encontrado: {hash_result.hex()}")
            print(f"Merkle Root: {merkle_root.hex()}")
            print(f"Nonce: {nNonce}")
            print(f"Bloco Gênesis minerado com sucesso!")
            break
        nNonce += 1
        header = genesis_block(pszTimestamp, pubkey, nTime, nBits, nNonce)[0]

mine_genesis_block()
