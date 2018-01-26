import sys
f1 = open(sys.argv[1] + '.hierarchy','r')
r1 = open(sys.argv[1] + '.hierarchy.trimmed', 'w')
f2 = open(sys.argv[1] + '.overloads','r')
r2 = open(sys.argv[1] + '.overloads.trimmed', 'w')
f3 = open(sys.argv[1] + '.overrides','r')
r3 = open(sys.argv[1] + '.overrides.trimmed', 'w')


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
trim(f1, r1)
S = set()
list = []
trim(f2, r2)
S = set()
list = []
trim(f3, r3)