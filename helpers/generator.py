import random
import binascii

def get_UUID():
    random_bytes = random.randbytes(16)
    hex_str = binascii.hexlify(random_bytes).decode('utf-8')

    time_low = hex_str[0:8]
    time_mid = hex_str[8:12]
    time_hi_and_version = hex_str[12:16]
    clock_seq_hi_and_reserved = int(hex_str[16:18], 16) & 0x3f
    clock_seq_low = int(hex_str[18:20], 16)
    node = hex_str[20:32]

    uuid = f"{time_low}-{time_mid}-{time_hi_and_version}-{clock_seq_hi_and_reserved:02x}{clock_seq_low:02x}-{node}"
    
    return uuid

def get_token_validation(length: int) -> str:
    characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    res = ''
    
    char_count = len(characters)
    for _ in range(length):
        rand_index = random.randint(0, char_count - 1)
        res += characters[rand_index]
    
    return res