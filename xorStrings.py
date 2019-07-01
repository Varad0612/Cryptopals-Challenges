import binascii
from Crypto.Util.strxor import strxor

# Outputs xor of 2 hex strings
def xor(x, y):
	a = binascii.unhexlify(x)
	b = binascii.unhexlify(y)
	ans = strxor(a,b)
	return binascii.hexlify(ans).decode()

a = "1c0111001f010100061a024b53735009181c"
b = "686974207468652062756c6c257320657965"
print(xor(a,b))