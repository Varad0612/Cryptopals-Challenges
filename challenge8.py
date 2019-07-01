import binascii
from Crypto.Cipher.AES import block_size

# Return contents of file as a string
def readFile(filename):
	f = open(filename, "r")
	content = []
	while True:
		line = f.readline()
		content.append(bytes.fromhex(line.strip()))
		if not line: 
			break
	return content

def count_repetitions(line):
	ls = [line[i : i + block_size] for i in range(0, len(line), block_size)]
	duplicates = len(ls) - len(set(ls))
	return duplicates

def detect_cipher(file_name):
	ans = []
	content = readFile(file_name)
	for line in content:
		cnt = count_repetitions(line)
		ans.append([cnt, line])
	ans.sort(key=lambda x: x[0])
	return ans[-1]



print(detect_cipher("ch8.txt"))