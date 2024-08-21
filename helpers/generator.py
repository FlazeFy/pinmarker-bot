import random
import binascii
import googlemaps
import json
from typing import Final
with open('configs/google.json', 'r') as config_file:
    config = json.load(config_file)
MAPS_API_KEY: Final = config['MAPS_API_KEY']

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
    if length > 0:
        characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        res = ''
        
        char_count = len(characters)
        for _ in range(length):
            rand_index = random.randint(0, char_count - 1)
            res += characters[rand_index]
        
        return res
    else: 
        return "Cant't have parameter below 1"

def get_city_from_coordinate(latitude, longitude):
    gmaps = googlemaps.Client(key=MAPS_API_KEY)
    reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude))
    for result in reverse_geocode_result:
        for component in result['address_components']:
            if 'locality' in component['types']:
                return component['long_name']
    return None