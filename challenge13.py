import secrets
from Crypto.Cipher import AES
from Crypto.Cipher.AES import block_size
import math

global_key = secrets.token_bytes(block_size)

# Pad string to n-byte block size
def pad_string(s, n):
	s_len = len(s)
	pad = ((math.ceil(s_len/n))*n) - s_len
	return s + bytes(chr(pad)*pad, "utf-8")

# Parse cookie formt into a dictinary
def parser(inp):
	inp = inp.split("&")
	d = {}
	for item in inp:
		item = item.split("=")
		d[item[0]] = d[item[1]]
	return d

# Encode dic values in a=b&.. format
def encoder(d):
	out = ""
	for key, value in d.items():
		out = out + str(key) + "=" + str(value) + "&"
	return out[:len(out) - 1]

# Return profile for email
def profile_for(email):
	email = email.replace('&', '')
	email = email.replace('=', '')
	d = {}
	d['email'] = email
	d['uid'] = 10
	d['role'] = 'user'
	return d

# AES Encryption
def encrypt(encodedProfile):
	enc_obj = AES.new(global_key, AES.MODE_ECB)
	encodedProfile = pad_string(bytes(encodedProfile, 'utf-8'), block_size)
	ciphertext = enc_obj.encrypt(encodedProfile)
	return ciphertext

# AES Decryption
def decrypt(ciphertext):
	dec_obj = AES.new(global_key, AES.MODE_ECB)
	plaintext = dec_obj.decrypt(ciphertext)
	return plaintext

def oracle(plaintext):
	d = profile_for(plaintext)
	encoded_profile = encoder(d)
	return encrypt(encoded_profile)

# Attack to change role to admin
def attack():
	# email=fake@mail.com&uid=10&role=user 
	pt = "A"*10 + "admin" + "\0"*11
	ct = oracle(pt)
	cut = ct[block_size : block_size*2]
	pt = "fake@mail.com"
	ct = oracle(pt)
	ct = ct[ : 2*block_size]
	ct = ct + cut
	print(len(ct))
	return decrypt(ct).decode("utf-8")

print(attack())





