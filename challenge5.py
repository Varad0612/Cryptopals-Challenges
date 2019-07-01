def encrypt(plaintext, key):
	pt_len = len(plaintext)
	key_len = len(key)

	q = int(pt_len/key_len)
	r = pt_len % key_len

	print(q)
	print(r)

	new_key = key*q
	new_key = new_key + key[:r]

	cipher = ""
	for a,b in zip(plaintext, new_key):
		enc = hex(ord(a)^ord(b))[2:]
		l = len(enc)
		cipher = cipher + "0"*(2-l) + enc
	return cipher

p = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
k = "ICE"
print(encrypt(p, k))