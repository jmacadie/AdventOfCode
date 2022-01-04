import hashlib
from typing import Tuple

def mine(key: str, depth: int) -> Tuple[int, str]:
    num = 0
    while True:
        test = key + str(num)
        hsh = hashlib.md5(test.encode('UTF-8')).hexdigest()
        if hsh[:depth] == '0' * depth:
            break
        num += 1
    return num, hsh

KEY = 'bgvyzdsv'
NUM, HSH = mine(KEY, 6)
print(f'Key: {KEY} & Number: {NUM} -> {HSH}')
