import sys
import base64
from collections import defaultdict
import binascii
from Crypto.Util.strxor import strxor_c,strxor


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
	freq = {' ' : 0.12702,'a' : 0.08167, 'b' : 0.01492, 'c' : 0.02782, 'd' : 0.04253, 'e' : 0.12702, 'f' : 0.02228, 'g' : 0.02015, 'h' : 0.06094, 'i' : 0.06966, 'j' : 0.00153, 'k' : 0.00772, 'l' : 0.04025, 'm' : 0.02406, 'n' : 0.06749, 'o' : 0.07507, 'p' : 0.01929, 'q' : 0.00095, 'r' : 0.05987, 's' : 0.06327, 't' : 0.09056, 'u' : 0.02758, 'v' : 0.00978, 'w' : 0.02360, 'x' : 0.00150, 'y' : 0.01974, 'z' : 0.00074}
	count = defaultdict(int)

	score = 0
	for c in s:
		score = score + freq.get(chr(c).lower(), 0)
	return score

# Get binary rep of string
def getBinary(s):
	res = ""
	for c in s:
		tmp = bin(ord(c))[2:]
		n = len(tmp)
		res = res + (8-n)*"0" + tmp
	return res

# Get HD between two ascii strings
def hammingDistance(a, b):

	hd = 0
	for b1, b2 in zip(a, b):
		tmp = b1^b2
		hd = hd + sum([1 for bit in bin(tmp) if bit == '1'])
	return hd

# Return contents of file as a string
def readFile(filename):
	f = open(filename, "r")
	content = base64.b64decode(f.read())
	f.close()
	return content

# Get the correct keysize
def keySize():
	txt = readFile("ch6.txt")
	min_dist = sys.maxsize
	ans = -1
	for i in range(2, 41):
		a = txt[:i]
		b = txt[i:2*i]
		c = txt[2*i:3*i]
		d = txt[3*i:4*i]
		d1 = hammingDistance(a, b)
		d2 = hammingDistance(c, b)
		d3 = hammingDistance(c, d)
		d4 = hammingDistance(a, d)
		norm_dist = (d1 + d2 + d3 + d4)/(4*i)
		#print("KEYSIZE: " + str(i) + " Distance : " + str(norm_dist))

		if norm_dist < min_dist:
			min_dist = norm_dist
			ans = i
	return ans

def getChunks():
	keysz = keySize()
	txt = readFile("ch6.txt")

	i = 0
	chunks = []
	while i < len(txt):
		chunks.append(txt[i : i + keysz])
		i = i + keys
	return chunks

def transpose():
	chunks = getChunks()
	keysz = keySize()
	blocks = []

	for i in range(keysz):
		tmp = b""
		for c in chunks:
			if(len(c) > i):
				tmp = tmp + bytes([c[i]])
		blocks.append(tmp)
	return blocks

def getKey():
	blocks = transpose()
	j = 0
	for b in blocks:
		sc = singleByteXOR(b.hex())
		f = open("out" + str(j), "a")
		for i in sc:
			#print(str(i[0]) + " : " + str(i[1]) +  " -- " + str(i[2]))
			f.write("Score : " + str(i[0]) + "\n")
			f.write("Char : " + str(i[2]) + "\n")
			f.write(str(i[1]) + "\n")
			f.write("==============================================\n")
		f.close()
		j = j + 1

# Outputs xor of 2 hex strings
def xor2(x, y):
	a = binascii.unhexlify(x)
	b = binascii.unhexlify(y)
	ans = strxor(a,b)
	return ans.decode("utf-8")

def decrypt():
	key = "nnt"
	chunks = getChunks()
	ans = []
	for c in chunks:
		a = key.encode("utf-8").hex()
		b = c.hex()

		if(len(b) < len(a)):
			a = a[:len(b)]
		res = xor2(a, b)
		ans.append(res)
	print("".join(ans))






# a = b'this is a test'
# b = b'wokka wokka!!!'
# print(hammingDistance(a, b))
#print(readFile("ch6.txt"))
#print(keySize())
#print(getChunks())
#print(transpose())
#getKey()
decrypt()
