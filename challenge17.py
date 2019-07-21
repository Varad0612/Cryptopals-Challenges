import secrets
from Crypto.Cipher import AES
from Crypto.Cipher.AES import block_size
import math
import random
import base64

class Oracle:

	def __init__(self):
		self.key = secrets.token_bytes(block_size)
		self.iv = secrets.token_bytes(block_size)
		self.enc_obj = AES.new(self.key, AES.MODE_CBC, self.iv)
		self.ls = ['MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=', "MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",\
				"MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==", "MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",\
				"MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl", "MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",\
				"MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=", "MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"]

	def check_padding(self, s):
		n = len(s)
		c = s[n - 1]
		cnt = 1
		for i in range(n-2, -1, -1):
			if c != s[i] or (cnt == c or chr(cnt) == c):
				break
			cnt = cnt + 1
		if cnt == c or chr(cnt) == c:
			return True
		return False

	def encrypt(self):
		inp = base64.b64decode(self.ls[random.randint(0, len(self.ls)-1)])
		inp = self.pad_string(inp, 16)

		# Encrypt with CBC	 mode
		ciphertext = self.enc_obj.encrypt(inp)
		return [self.iv, ciphertext]

	def decrypt(self, ciphertext):
		plaintext = self.enc_obj.decrypt(ciphertext)
		return self.check_padding(plaintext)


	# Pad string to n-byte block size
	def pad_string(self,s, n):
		s_len = len(s)
		pad = ((math.ceil(s_len/n))*n) - s_len
		return s + bytes(chr(pad)*pad, "utf-8")

class Solution:

	def __init__(self):
		self.oracle = Oracle()
	def attack(self):
		iv, ciphertext = self.oracle.encrypt()
		blocks = [ciphertext[i : i + block_size] for i in range(0, len(ciphertext), block_size)]
		blocks.insert(0, iv)
		pt = ""
		for j in range(len(blocks)-1, 0, -1):
			block = blocks[j]
			ans = b""
			for i in range(block_size - 1, -1, -1):
				inp = ("A"*i).encode()
				pad_byte = block_size - i
				pad_string = b""
				k = i + 1
				for a in ans:
					pad_string = pad_string + bytes([(a^pad_byte)^blocks[j-1][k]])
					k = k + 1
				assert(len(pad_string) + len(inp) == 15)
				found = False
				for c in range(256):
					tmp = inp + bytes([c]) + pad_string
					tmp = tmp + block
					if self.oracle.decrypt(tmp):
						found = True
						dec = pad_byte^c
						ans = bytes([blocks[j-1][i]^(dec)]) + ans
						break
				if not found:
					print("No such character")
			pt = ans.decode() + pt
		return pt

sol = Solution()
print(sol.attack())
#oracle = Oracle()
#print(oracle.check_padding(b"aaa"))


