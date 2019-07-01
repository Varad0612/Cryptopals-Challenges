import sys
import base64
from Crypto.Cipher import AES

key = "YELLOW SUBMARINE"

# Return contents of file as a string
def readFile(filename):
	f = open(filename, "r")
	content = base64.b64decode(f.read())
	f.close()
	return content

def decrypt(file_name):
	content = readFile(file_name)
	decipher = AES.new(key, AES.MODE_ECB)
	return decipher.decrypt(content)

print(decrypt("ch7.txt"))

