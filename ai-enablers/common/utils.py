import re
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os

def clean_special_char(x):
    x = re.sub('[^A-Za-z0-9]+', ' ', x)
    return x

def decrypt(ciphertext ):
    bytes1 = [0xb1, 0xed, 0x71, 0x66, 0x15, 0xbb, 0x74, 0x8c,
                0x9d, 0x7e, 0x33, 0x12, 0x64, 0xbf, 0x6d, 0x59, 0x0b, 0x38,
                0xbd, 0x9d, 0x12, 0x20, 0x01, 0x5f, 0xe6, 0x14, 0xd1, 0xc8,
                0x4c, 0x56, 0x6a, 0xc2]
    bytes2 = [0x60, 0x8d, 0xfd, 0xd8, 0x0f, 0x4f, 0x7a, 0x53, 0x96,
                0xb8, 0x70, 0x53, 0x26, 0xaf, 0x85, 0xda]
    bytes1 = bytes(bytes1)
    bytes2 = bytes(bytes2)
    key = bytes1  # 32 bytes for AES-256
    iv = bytes2  # 16 bytes for AES
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_text = decryptor.update(base64.b64decode(ciphertext)) + decryptor.finalize()
    return decrypted_text.decode('utf-8')