
def find_parts(t, p):
	tokens = t.split(' ')
	for i in range(len(tokens)):
		for j in range(i, len(tokens)):
			if p == ' '.join(tokens[i:j+1]):
				return True
	return False

