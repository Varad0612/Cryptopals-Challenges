import secrets
import random
from Crypto.Cipher import AES
from Crypto.Cipher.AES import block_size
import math
import base64

global_key = secrets.token_bytes(block_size)
prefix_count = random.randint(0, 100)
global_prefix = secrets.token_bytes(prefix_count)

# Generate a n-byte key
def generate_key(n):
	# Return type: bytes
	return secrets.token_bytes(n)

# Pad string to n-byte block size
def pad_string(s, n):
	s_len = len(s)
	pad = ((math.ceil(s_len/n))*n) - s_len
	return s + bytes(chr(pad)*pad, "utf-8")

# Encrypt data using a random key
def encryption_oracle(data):

	# String to append
	app = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg\naGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq\ndXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg\nYnkK"
	
	# Convert data string to bytes
	data = bytes(data, "utf-8")
	data = global_prefix + data + base64.b64decode(app)
	data = pad_string(data, 16)

	# Encrypt with ECB mode
	enc_obj = AES.new(global_key, AES.MODE_ECB)
	ciphertext = enc_obj.encrypt(data)
	return ciphertext

# Explananion : Inpute of len k results in exactly n blocks
# For k+1 bytes, the number of blocks incresases by one
# The difference in the len of the two ciphertexts gives the block size
def find_block_size():
	i = 1
	inp = "A"*i
	out1 = encryption_oracle(inp)
	out2 = out1
	while(len(out2) == len(out1)):
		i = i + 1
		inp = "A"*i
		out2 = encryption_oracle(inp)
	return len(out2) - len(out1)

# Detect if the given ciphertext is in ECB mode
def is_ECB(ciphertext):
	ls = [ciphertext[i : i + block_size] for i in range(0, len(ciphertext), block_size)]
	duplicates = len(ls) - len(set(ls))
	if duplicates > 0:
		return True
	return False

# Get number of blocks of secret string
def get_num_blocks():
	block_size = find_block_size()
	ciphertext = encryption_oracle("")
	return int(len(ciphertext)/block_size)

# Length of common prefix of given strings
def matching_bytes(a, b):
	i = 0
	while(i < len(a) and i < len(b)):
		if a[i] != b[i]:
			break
		i = i + 1
	if i == 0:
		return 0
	return i

# Get block length of the prefix string and secret string
def get_blocks():
	prev = encryption_oracle("")
	out = encryption_oracle("A")
	least_match = int(matching_bytes(prev, out) / block_size)
	min_bytes_to_append = 0
	block_prefix = least_match
	for i in range(2,block_size + 1):
		inp = "A"*i
		out = encryption_oracle(inp)
		match = matching_bytes(prev, out)
		n = int(match/block_size)
		if match % block_size == 0 and n == least_match + 1:
			min_bytes_to_append = i - 1
			block_prefix = n
			break
		prev = out
	sec_block_num = int(len(prev)/block_size) - block_prefix
	return [min_bytes_to_append, block_prefix, sec_block_num]


# Recover the secret string
def attack():
	# Store cleartext answer
	decrypted_string = ""

	# Get block size
	block_size = find_block_size()

	# Get number of blocks to decrypt
	min_bytes, prefix_block, num_blocks = get_blocks()

	# Prefix to append
	pre = "A"*min_bytes

	# Iterate over all block
	for block in range(num_blocks):

		# Recover single 'block'
		for i in range(block_size - 1,-1,-1):
			# Dummy input
			inp = pre + "A"*i
			ciphertext = encryption_oracle(inp)

			# Check all possible char values
			for j in range(0, 255):
				inp2 = inp + decrypted_string + chr(j)
				output = encryption_oracle(inp2)

				# Check if match found
				if ciphertext[block_size * (block + prefix_block) : block_size * (block + prefix_block) + block_size] == output[block_size * (block + prefix_block) : block_size * (block + prefix_block) + block_size]:
					# Append character to decrypted string
					decrypted_string = decrypted_string + chr(j)
					break
	return decrypted_string

def check_matching_bytes():
	x = "A"*5 + "C"*3
	y = "A"*3 + "C"*9
	n = matching_bytes(x, y)
	if n != 3:
		return False
	x = "A"*5 + "C"*3
	y = "A"*7 + "C"*9
	n = matching_bytes(x, y)
	if n != 5:
		return False
	return True

print(attack())























