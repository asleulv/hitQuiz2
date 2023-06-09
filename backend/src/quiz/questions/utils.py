
def find_parts(t, p):
	delim = ' '
	tokens = t.split(delim)
	for i in range(len(tokens)):
		for j in range(i + 1, len(tokens) + 1):
			if p == delim.join(tokens[i:j]):
				return True
	return False

