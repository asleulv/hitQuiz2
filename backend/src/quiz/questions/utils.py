
def find_parts(t, p):
	delim = ' '
	tokens = t.split(delim)
	size = len(tokens)
	for i in range(size):
		for j in range(i + 1, size + 1):
			if p == delim.join(tokens[i:j]):
				return True
	return False
