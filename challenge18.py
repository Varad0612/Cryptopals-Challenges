import secrets
from Crypto.Cipher import AES
from Crypto.Cipher.AES import block_size
import math
import random
import base64

class Oracle:

    # Initialize parameters
    def __init__(self):
        self.key = "YELLOW SUBMARINE"
        self.nonce = bytes(chr(0)*8, "utf-8")
        self.cipher = AES.new(self.key, AES.MODE_ECB)

    # XOR two byte strings
    def xor(self, a, b):
        s = b""
        for i in range(0, min(len(a), len(b))):
            s = s + bytes([a[i]^b[i]])
        return s

    # Encrypt message(raw bytes) and output ciphertext in base64 encoding
    def encrypt(self, msg):
        counter = 0
        ciphertext = b""
        for i in range(0, len(msg), 16):
            # Encrypt nonce||ctr
            ctr = bytes(chr(counter), "utf-8")
            ctr = ctr + bytes(chr(0)*(8-(len(ctr))), "utf-8")
            pad = self.cipher.encrypt(self.nonce + ctr)
            counter = counter + 1

            # Encrypt message
            ciphertext = ciphertext + self.xor(msg[i:i + 16], pad)
        return base64.b64encode(ciphertext)

    # Decrypt base64 encoded message and output plaintext(raw bytes)
    def decrypt(self, ciphertext):
        return base64.b64decode(self.encrypt(base64.b64decode(ciphertext)))

oracle = Oracle()
ans = oracle.encrypt(b"Hello there peasant")
print("Ciphertext: " + str(ans))
print(oracle.decrypt(ans))
