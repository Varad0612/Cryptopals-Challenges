from collections import defaultdict
import binascii
from Crypto.Util.strxor import strxor_c

# Outputs xor of 2 hex strings
def xor(x, y):
	a = binascii.unhexlify(x)
	ans = strxor_c(a,y)
	return ans

def singleByteXOR(s):
	s_len = len(s)
	scores = []
	for i in range(0, 256):
		ans = xor(s, i)
		sc = score(ans)
		scores.append([sc, ans, i])
	scores.sort(key=lambda x: x[0])
	scores = scores[::-1]
	return scores


# Get the score for the text using frequency analysis
def score(s):
	freq = {'a' : 0.08167, 'b' : 0.01492, 'c' : 0.02782, 'd' : 0.04253, 'e' : 0.12702, 'f' : 0.02228, 'g' : 0.02015, 'h' : 0.06094, 'i' : 0.06966, 'j' : 0.00153, 'k' : 0.00772, 'l' : 0.04025, 'm' : 0.02406, 'n' : 0.06749, 'o' : 0.07507, 'p' : 0.01929, 'q' : 0.00095, 'r' : 0.05987, 's' : 0.06327, 't' : 0.09056, 'u' : 0.02758, 'v' : 0.00978, 'w' : 0.02360, 'x' : 0.00150, 'y' : 0.01974, 'z' : 0.00074}
	count = defaultdict(int)

	score = 0
	for c in s:
		score = score + freq.get(chr(c).lower(), 0)
	return score

s = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
l = singleByteXOR(s)[:10]
for i in l:
	print(str(i[0]) + " : " + str(i[1]))
	print(i[2])



