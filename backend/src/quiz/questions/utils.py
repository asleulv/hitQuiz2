import re

def find_parts(t, p):
	delim = ' '
	tokens = re.split(r'[,\s]', t) 
	size = len(tokens)
	plen = len(p)
	for i in range(size):
		for j in range(i + 1, size + 1):
			_t = delim.join(tokens[i:j])
			_tlen = len(_t)
			if _tlen > plen:
				break
			elif _tlen < plen:
				continue
			else: 
				if _t == p:
					return True
	return False
