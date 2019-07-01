import base64
from Crypto.Cipher import AES

def main():	
	f = open("ch10.txt", "r")	
	ciphertext = f.read().replace('\n', '')	
	f.close()	

	iv  = '\x00' * 16
	key = 'YELLOW SUBMARINE'

	decobj = AES.new(key, AES.MODE_CBC, iv)
	plaintext = decobj.decrypt(base64.b64decode(ciphertext))
	print(plaintext)

main()