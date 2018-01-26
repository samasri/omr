import sys
f1 = open(sys.argv[1] + '.hierarchy','r')
r1 = open(sys.argv[1] + '.hierarchy.clean', 'w')
f2 = open(sys.argv[1] + '.overloads','r')
r2 = open(sys.argv[1] + '.overloads.clean', 'w')
f3 = open(sys.argv[1] + '.overrides','r')
r3 = open(sys.argv[1] + '.overrides.clean', 'w')

def removeSTD(f, r):
	while True:
		x = f.readline()
		x = x.rstrip()
		if not ("std::" in x): 
			list.append(x)
		if not x: break

	for line in list:
		r.write(line + "\n")

S = set()
list = []
removeSTD(f1, r1)
S = set()
list = []
removeSTD(f2, r2)
S = set()
list = []
removeSTD(f3, r3)