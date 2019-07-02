def check_padding(s):
	n = len(s)
	c = s[n - 1]
	cnt = 1
	for i in range(n-2, -1, -1):
		if c != s[i]:
			break
		cnt = cnt + 1
	if chr(cnt) != c:
		raise Exception('Improper Padding')

	return s[ : n-cnt]

print(check_padding("ICE ICE BABY\x04\x04\x04\x04"))
