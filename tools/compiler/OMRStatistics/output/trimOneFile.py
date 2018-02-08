import sys
f = open(sys.argv[1],'r')
r = open(sys.argv[1] + '.trimmed','w')


def trim(f, r):
	while True:
		x = f.readline()
		x = x.rstrip()
		if not x: break
		if not x in S: list.append(x)
		S.add(x)

	for line in list:
		r.write(line + "\n")

S = set()
list = []
trim(f, r)