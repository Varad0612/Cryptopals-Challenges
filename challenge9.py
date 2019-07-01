# Pad string s to padLength
def pkcs7(s, padLength):
	s_len = len(s)
	pad = padLength - s_len
	s = s + chr(pad)*pad
	return bytes(s, "utf-8")

print(pkcs7("YELLOW SUBMARINE", 20))