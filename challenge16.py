import secrets
from Crypto.Cipher import AES
from Crypto.Cipher.AES import block_size
import math

global_key = secrets.token_bytes(block_size)
iv = secrets.token_bytes(block_size)

def xor(a, b):
	ans = ""
	for x,y in zip(a,b):
		ans = ans + chr(x^y)
	return ans

# Pad string to n-byte block size
def pad_string(s, n):
	s_len = len(s)
	pad = ((math.ceil(s_len/n))*n) - s_len
	return s + bytes(chr(pad)*pad, "utf-8")

# Encrypt string after appropriate transformation
def encrypt(s):
	# Remove ';' and '=' from s
	s = s.replace(';', '')
	s = s.replace('=', '')
	s = "comment1=cooking%20MCs;userdata=" + s + ";comment2=%20like%20a%20pound%20of%20bacon"
	s = pad_string(bytes(s, 'utf-8'), block_size)

	# Encrypt with CBC	 mode
	enc_obj = AES.new(global_key, AES.MODE_CBC, iv)
	ciphertext = enc_obj.encrypt(s)
	return ciphertext

# Decrypt string
def decrypt(ciphertext):
	dec_obj = AES.new(global_key, AES.MODE_CBC, iv)
	if len(ciphertext)%16 != 0:
		return b""
	plaintext = dec_obj.decrypt(ciphertext)
	return plaintext

# Detect if ";admin=true" is present
def detect(s):
	s = s.decode("utf-8", "replace").split(';')
	for chunk in s:
		chunk = chunk.split('=')
		if chunk[0] == "admin" and chunk[1] == "true":
			return True
	return False


# Insert admin=true in plaintext
def attack():
	inp = "A"*5
	inp = inp + "xadminxtrue"
	ciphertext = encrypt(inp)
	block2 = ciphertext[block_size:2*block_size]
	for i in range(256):
		for j in range(256):
			tmp = block2[:5] + bytes(chr(i),"utf-8") + block2[6:11] + bytes(chr(j),"utf-8") + block2[12:]
			tmp = ciphertext[:block_size] + tmp + ciphertext[2*block_size:]
			pt = decrypt(tmp)
			if detect(pt):
				print(pt)
				return
	print("Failed")
	return

attack()



