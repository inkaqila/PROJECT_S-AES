S_BOX = [0x9, 0x4, 0xA, 0xB, 0xD, 0x1, 0x8, 0x5, 0x6, 0x2, 0x0, 0x3, 0xC, 0xE, 0xF, 0x7]
INV_S_BOX = [0xA, 0x5, 0x9, 0xB, 0x1, 0x7, 0x8, 0xF, 0x6, 0x0, 0x2, 0x3, 0xC, 0x4, 0xD, 0xE]

RCON1 = 0x80  
RCON2 = 0x30  

def gf_add(a, b):
    return int(a) ^ int(b)

def gf_mul(a, b):
    a = int(a) & 0x0F
    b = int(b) & 0x0F
    p = 0
    for _ in range(4):
        if b & 1:
            p ^= a
        a <<= 1
        if a & 0x10:  
            a ^= 0x13
        b >>= 1
    return p & 0x0F

def sub_word(word):
    word = int(word) & 0xFF
    nibble_high = (word >> 4) & 0x0F
    nibble_low = word & 0x0F
    return (S_BOX[nibble_high] << 4) | S_BOX[nibble_low]

def rot_word(word):
    word = int(word) & 0xFF
    return ((word & 0x0F) << 4) | ((word >> 4) & 0x0F)

def key_expansion(key_16bit):
    key_16bit = int(key_16bit) & 0xFFFF
    w0 = (key_16bit >> 8) & 0xFF
    w1 = key_16bit & 0xFF
    
    w2 = w0 ^ sub_word(rot_word(w1)) ^ RCON1
    w3 = w2 ^ w1
    
    w4 = w2 ^ sub_word(rot_word(w3)) ^ RCON2
    w5 = w4 ^ w3
    
    return [
        (w0 << 8) | w1,  
        (w2 << 8) | w3,  
        (w4 << 8) | w5   
    ]

def int_to_state(block_16bit):
    block_16bit = int(block_16bit) & 0xFFFF
    return [
        [(block_16bit >> 12) & 0x0F, (block_16bit >> 4) & 0x0F], 
        [(block_16bit >> 8) & 0x0F,  block_16bit & 0x0F]         
    ]

def state_to_int(state):
    return (int(state[0][0]) << 12) | (int(state[1][0]) << 8) | (int(state[0][1]) << 4) | int(state[1][1])

def state_to_hex_list(state):
    formatted_state = []
    for row in state:
        formatted_row = []
        for x in row:
            val_int = int(x)
            hex_val = hex(val_int)[2:].upper()
            bin_val = bin(val_int)[2:].zfill(4)
            formatted_row.append(f"{hex_val} ({bin_val})")
        formatted_state.append(formatted_row)
    return formatted_state

def encrypt_with_logs(plaintext_16bit, key_16bit):
    logs = []
    plaintext_16bit = int(plaintext_16bit)
    key_16bit = int(key_16bit)
    keys = key_expansion(key_16bit)
    
    state = int_to_state(plaintext_16bit)
    logs.append({"step": "State Awal", "state": state_to_hex_list(state), "desc": "Plaintext dimasukkan ke State Matrix 2x2 (Column-Major)."})
    
    k0_state = int_to_state(keys[0])
    for r in range(2):
        for c in range(2):
            state[r][c] ^= k0_state[r][c]
    logs.append({"step": "Initial AddRoundKey", "state": state_to_hex_list(state), "desc": "State Matrix di-XOR dengan Kunci Awal (K0)."})
    
    state = [[S_BOX[int(x)] for x in row] for row in state]
    logs.append({"step": "Round 1: SubNibbles", "state": state_to_hex_list(state), "desc": "Setiap nibble disubstitusi menggunakan tabel S-Box S-AES."})
    
    state[1][0], state[1][1] = state[1][1], state[1][0] 
    logs.append({"step": "Round 1: ShiftRows", "state": state_to_hex_list(state), "desc": "Baris kedua dari matriks digeser ke kiri sejauh 1 nibble."})
    
    c00 = gf_add(gf_mul(1, state[0][0]), gf_mul(4, state[1][0]))
    c10 = gf_add(gf_mul(4, state[0][0]), gf_mul(1, state[1][0]))
    c01 = gf_add(gf_mul(1, state[0][1]), gf_mul(4, state[1][1]))
    c11 = gf_add(gf_mul(4, state[0][1]), gf_mul(1, state[1][1]))
    state = [[c00, c01], [c10, c11]]
    logs.append({"step": "Round 1: MixColumns", "state": state_to_hex_list(state), "desc": "Mengalikan setiap kolom dengan matriks konstan [[1,4],[4,1]] di GF(2^4)."})
    
    k1_state = int_to_state(keys[1])
    for r in range(2):
        for c in range(2):
            state[r][c] ^= k1_state[r][c]
    logs.append({"step": "Round 1: AddRoundKey", "state": state_to_hex_list(state), "desc": "State hasil MixColumns di-XOR dengan subkunci K1."})
    
    state = [[S_BOX[int(x)] for x in row] for row in state]
    logs.append({"step": "Round 2: SubNibbles", "state": state_to_hex_list(state), "desc": "Substitusi nibble kembali menggunakan tabel S-Box."})
    
    state[1][0], state[1][1] = state[1][1], state[1][0]
    logs.append({"step": "Round 2: ShiftRows", "state": state_to_hex_list(state), "desc": "Pergeseran baris kedua matriks state (tukar nibble)."})
    
    k2_state = int_to_state(keys[2])
    for r in range(2):
        for c in range(2):
            state[r][c] ^= k2_state[r][c]
    logs.append({"step": "Round 2: AddRoundKey (Final)", "state": state_to_hex_list(state), "desc": "Tahap terakhir, di-XOR dengan subkunci K2 untuk menghasilkan Ciphertext."})
    
    ciphertext = state_to_int(state)
    return ciphertext, keys, logs

def decrypt_with_logs(ciphertext_16bit, key_16bit):
    logs = []
    ciphertext_16bit = int(ciphertext_16bit)
    key_16bit = int(key_16bit)
    keys = key_expansion(key_16bit)
    
    state = int_to_state(ciphertext_16bit)
    logs.append({"step": "State Ciphertext", "state": state_to_hex_list(state), "desc": "Ciphertext diinput ke State Matrix 2x2."})
    
    k2_state = int_to_state(keys[2])
    for r in range(2):
        for c in range(2):
            state[r][c] ^= k2_state[r][c]
    logs.append({"step": "Initial AddRoundKey (K2)", "state": state_to_hex_list(state), "desc": "State Awal Dekripsi di-XOR dengan subkunci K2."})
    
    state[1][0], state[1][1] = state[1][1], state[1][0]
    logs.append({"step": "Inverse Round 1: InvShiftRows", "state": state_to_hex_list(state), "desc": "Mengembalikan pergeseran baris kedua."})
    
    state = [[INV_S_BOX[int(x)] for x in row] for row in state]
    logs.append({"step": "Inverse Round 1: InvSubNibbles", "state": state_to_hex_list(state), "desc": "Substitusi balik menggunakan Inverse S-Box."})
    
    k1_state = int_to_state(keys[1])
    for r in range(2):
        for c in range(2):
            state[r][c] ^= k1_state[r][c]
    logs.append({"step": "Inverse Round 1: AddRoundKey (K1)", "state": state_to_hex_list(state), "desc": "State di-XOR dengan subkunci K1."})
    
    c00 = gf_add(gf_mul(9, state[0][0]), gf_mul(2, state[1][0]))
    c10 = gf_add(gf_mul(2, state[0][0]), gf_mul(9, state[1][0]))
    c01 = gf_add(gf_mul(9, state[0][1]), gf_mul(2, state[1][1]))
    c11 = gf_add(gf_mul(2, state[0][1]), gf_mul(9, state[1][1]))
    state = [[c00, c01], [c10, c11]]
    logs.append({"step": "Inverse Round 1: InvMixColumns", "state": state_to_hex_list(state), "desc": "Mengalikan kolom dengan invers matriks konstan [[9,2],[2,9]] di GF(2^4)."})
    
    state[1][0], state[1][1] = state[1][1], state[1][0]
    logs.append({"step": "Inverse Round 2: InvShiftRows", "state": state_to_hex_list(state), "desc": "Mengembalikan pergeseran baris kedua pada round final dekripsi."})
    
    state = [[INV_S_BOX[int(x)] for x in row] for row in state]
    logs.append({"step": "Inverse Round 2: InvSubNibbles", "state": state_to_hex_list(state), "desc": "Substitusi balik terakhir menggunakan Inverse S-Box."})
    
    k0_state = int_to_state(keys[0])
    for r in range(2):
        for c in range(2):
            state[r][c] ^= k0_state[r][c]
    logs.append({"step": "Inverse Round 2: AddRoundKey (K0)", "state": state_to_hex_list(state), "desc": "XOR terakhir dengan K0 untuk mengembalikan Plaintext asli."})
    
    plaintext = state_to_int(state)
    return plaintext, keys, logs