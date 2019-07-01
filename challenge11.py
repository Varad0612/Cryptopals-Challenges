import secrets
import random
from Crypto.Cipher import AES
from Crypto.Cipher.AES import block_size
import math

# Generate a n-byte key
def generate_key(n):
	# Return type: bytes
	return secrets.token_bytes(n)

# Append 5-10 bytes before and after plaintext
def append_bytes(plaintext):
	pad1 = secrets.token_bytes(random.randint(5, 11))
	pad2 = secrets.token_bytes(random.randint(5, 11))
	return pad1 + plaintext + pad2

# Pad string to n-byte block size
def pad_string(s, n):
	s_len = len(s)
	pad = ((math.ceil(s_len/n))*n) - s_len
	return s + bytes(chr(pad)*pad, "utf-8")

# Encrypt data using a random key
def encryption_oracle(data):
	# Generate random 1-byte key
	key = generate_key(16)

	# Convert data string to bytes
	data = bytes(data, "utf-8")
	data = append_bytes(data)
	data = pad_string(data, 16)

	# Choose either CBC(0) OR ECB(1) mode
	mode = random.randint(0,1)
	ciphertext = ""
	if mode:
		enc_obj = AES.new(key, AES.MODE_ECB)
		ciphertext = enc_obj.encrypt(data)
	else:
		iv = generate_key(16)
		enc_obj = AES.new(key, AES.MODE_CBC, iv)
		ciphertext = enc_obj.encrypt(data)

	# Append mode so that we can verify the result of 'deistinguish'
	return [ciphertext, mode]

# Detect if the given ciphertext is in ECB mode
def is_ECB(ciphertext):
	ls = [ciphertext[i : i + block_size] for i in range(0, len(ciphertext), block_size)]
	duplicates = len(ls) - len(set(ls))
	#print("Duplicates : " + str(duplicates))
	if duplicates > 0:
		return True
	return False

def detect_mode(inp):
	cipher, ans = encryption_oracle(inp)
	mode = 0
	if is_ECB(cipher):
		mode = 1
	if mode == ans:
		return True
	return False

def main():
	for num_blocks in range(1, 10):
		inp = "A"*16*num_blocks
		success = 0
		for i in range(1000):
			if detect_mode(inp):
				success = success + 1
		print("Block Size : " + str(num_blocks) + " Sucess Rate : " + str(success/10))

main()























