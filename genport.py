def genport(word):
	return (sum(a*27**b for b,a in enumerate(min(26, max(0, ord(a) - ord('a') + 1)) for a in reversed(word))) % (63<<10)) + (1<<10)

